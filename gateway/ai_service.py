"""Lightweight prediction and alert services for FreshChain.

The gateway intentionally keeps the on-PC model small and explainable.  The
forecast is a time-series trend model fitted on route points (or live IA1
telemetry when no route has been collected yet).  It returns an interval and
never pretends to have a high-confidence answer when there are too few
samples.
"""

from __future__ import annotations

import math
import time
import warnings
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable

try:  # SARIMAX is optional: the gateway must still start if deps are missing.
    import numpy as np
    import pandas as pd
    from statsmodels.tsa.statespace.sarimax import SARIMAX

    SARIMAX_AVAILABLE = True
except Exception:  # pragma: no cover - exercised only on a minimal install
    np = None
    pd = None
    SARIMAX = None
    SARIMAX_AVAILABLE = False


METRICS = ("temperature", "humidity")
UNITS = {"temperature": "掳C", "humidity": "%", "lux": "lx"}
PHYSICAL = {
    "temperature": (-40.0, 80.0),
    "humidity": (0.0, 100.0),
    "lux": (0.0, 200000.0),
}


def _finite(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _iso(ms: int | None) -> str | None:
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000, timezone.utc).astimezone().isoformat(timespec="seconds")


def _clamp(metric: str, value: float) -> float:
    low, high = PHYSICAL[metric]
    return max(low, min(high, value))


@dataclass
class Thresholds:
    temp_watch: float = 28.0
    temp_warning: float = 30.0
    temp_critical: float = 32.0
    humidity_watch: float = 70.0
    humidity_warning: float = 75.0
    humidity_critical: float = 85.0
    lux_watch: float = 20.0
    lux_warning: float = 10.0
    horizon_min: int = 10
    cooldown_sec: int = 60


class ForecastService:
    """Fit a small trend model and return a human-readable forecast."""

    version = "freshchain-ai-sarimax-3.0"

    def __init__(self, store: Any) -> None:
        self.store = store

    def forecast(self, run_id: int | None = None, horizon_min: int = 10,
                 scope: str = "region") -> dict[str, Any]:
        horizon_min = max(1, min(int(horizon_min or 10), 60))
        if scope == "single":
            series = self.store.telemetry_series("ia1", minutes=30, limit=2400)
        else:
            series = self.store.ai_series(run_id=run_id, limit=2400)
        points = series.get("points", [])
        # Do not attach stale latest values when the node is offline and the
        # series is empty; the dashboard should show "waiting", not old data.
        current = self.store.current_environment() if points else {}
        source = series.get("source", "route_points")
        generated_ms = int(time.time() * 1000)

        result: dict[str, Any] = {
            "ok": True,
            "generated_ms": generated_ms,
            "generated_at": _iso(generated_ms),
            "scope": scope,
            "run_id": series.get("run_id", run_id),
            "horizon_min": horizon_min,
            "target_ms": None,
            "source": source,
            "runs": series.get("runs", 0),
            "samples": len(points),
            "model": {
                "name": "linear-trend",
                "version": self.version,
                "description": "鏈€灏忎簩涔樿秼鍔?+ 娈嬪樊缃俊鍖洪棿",
            },
            "current": current,
            "temperature": self._metric(points, "temperature", horizon_min, current),
            "humidity": self._metric(points, "humidity", horizon_min, current),
            "available": False,
            "message": "",
        }
        metric_models = {result["temperature"].get("model"), result["humidity"].get("model")}
        if "SARIMAX" in metric_models:
            result["model"] = {
                "name": "SARIMAX",
                "version": self.version,
                "description": "SARIMAX + 鏃?鍛ㄥ倕閲屽彾澶栫敓鍙橀噺 + 80% 棰勬祴鍖洪棿",
            }
        available = bool(result["temperature"].get("available") or result["humidity"].get("available"))
        result["available"] = available
        if not points:
            result["ok"] = False
            result["message"] = (
                "鏆傛棤鍗曠偣閬ユ祴鏁版嵁锛岀瓑寰?IA1 涓婃姤"
                if scope == "single"
                else "鏆傛棤鍘嗗彶璺嚎鐐规垨瀹炴椂鐜鏁版嵁锛屽畬鎴愪竴鍦堝悗鍐嶅垎鏋?
            )
        elif not available:
            result["ok"] = False
            result["message"] = "鏈夋晥鏍锋湰灏戜簬 3 涓紝鏆備笉鍋氶娴?
        else:
            result["message"] = (
                "鍗曠偣瀹炴椂瓒嬪娍棰勬祴宸叉洿鏂?
                if scope == "single"
                else "璺嚎瓒嬪娍棰勬祴宸叉洿鏂?
            )
            if result["temperature"].get("available"):
                result["target_ms"] = result["temperature"].get("target_ms")
        return result

    @staticmethod
    def _time_exog(timestamps: Any) -> Any:
        """Calendar features that let SARIMAX learn daily and weekly cycles."""
        stamps = pd.to_datetime(timestamps, unit="ms") if not isinstance(timestamps, pd.DatetimeIndex) else timestamps
        hour = stamps.hour + stamps.minute / 60.0 + stamps.second / 3600.0
        day = stamps.dayofweek / 7.0
        return np.column_stack([
            # Two daily Fourier harmonics: one broad day/night cycle and one
            # faster morning/evening shape.
            np.sin(2.0 * np.pi * hour / 24.0),
            np.cos(2.0 * np.pi * hour / 24.0),
            np.sin(4.0 * np.pi * hour / 24.0),
            np.cos(4.0 * np.pi * hour / 24.0),
            np.sin(2.0 * np.pi * day),
            np.cos(2.0 * np.pi * day),
        ])

    def _sarimax_metric(self, pairs: list[tuple[int, float]], metric: str,
                        horizon_min: int, current: dict[str, Any]) -> dict[str, Any] | None:
        """Fit SARIMAX with daily/weekly Fourier exog.

        A 144-step seasonal ARIMA state is too slow for a 5-second dashboard
        poll on this PC.  The daily cycle is therefore encoded as Fourier
        exogenous features, which is still a SARIMAX model and fits in well
        under a second for the gateway's 30-minute / 2400-point windows.
        """
        if not SARIMAX_AVAILABLE or len(pairs) < 12:
            return None
        try:
            raw_index = pd.to_datetime([ts for ts, _ in pairs], unit="ms")
            values = pd.Series([value for _, value in pairs], index=raw_index, dtype="float64")
            series = values.resample("10s").mean().dropna()
            resample_seconds = 10
            if len(series) < 12:
                series = values.resample("30s").mean().dropna()
                resample_seconds = 30
            if len(series) < 12:
                return None
            steps = horizon_min * (60 // resample_seconds)
            seasonal_order = (0, 0, 0, 0)

            # Gaps in telemetry are common.  SARIMAX is fitted on a regular
            # RangeIndex; timestamps are reattached when building the chart.
            series_times = series.index
            series = pd.Series(series.to_numpy(dtype=float), index=pd.RangeIndex(len(series)))
            exog = self._time_exog(series_times)

            order = (1, 1, 1) if len(series) >= 30 else (1, 1, 0)
            future_index = pd.date_range(
                start=series_times[-1] + pd.Timedelta(seconds=resample_seconds),
                periods=steps,
                freq=f"{resample_seconds}s",
            )
            future_exog = self._time_exog(future_index)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                fitted = SARIMAX(
                    series,
                    exog=exog,
                    order=order,
                    seasonal_order=seasonal_order,
                    trend="n",
                    enforce_stationarity=False,
                    enforce_invertibility=False,
                ).fit(disp=False)
                forecast = fitted.get_forecast(steps=steps, exog=future_exog)
            mean = np.asarray(forecast.predicted_mean, dtype=float)
            interval = np.asarray(forecast.conf_int(alpha=0.20), dtype=float)
            if not len(mean) or not np.all(np.isfinite(mean[-1])):
                return None

            last_ts = int(pairs[-1][0])
            base_current = _finite(current.get(metric))
            if base_current is None:
                base_current = float(series.iloc[-1])
            predicted = _clamp(metric, float(mean[-1]))
            lower = _clamp(metric, float(interval[-1, 0]))
            upper = _clamp(metric, float(interval[-1, 1]))
            if upper < lower:
                lower, upper = upper, lower

            path: list[dict[str, Any]] = [{
                "ts_ms": last_ts,
                "value": round(base_current, 2),
                "lower": round(base_current, 2),
                "upper": round(base_current, 2),
            }]
            total_steps = len(mean)
            for minute in range(1, horizon_min + 1):
                index_at = min(total_steps - 1, minute * (steps // horizon_min) - 1)
                path.append({
                    "ts_ms": last_ts + minute * 60_000,
                    "value": round(_clamp(metric, float(mean[index_at])), 2),
                    "lower": round(_clamp(metric, float(interval[index_at, 0])), 2),
                    "upper": round(_clamp(metric, float(interval[index_at, 1])), 2),
                })

            width = max(0.0, upper - lower)
            confidence = max(0.35, min(0.90, 0.90 - width * 0.04))
            delta = predicted - base_current
            return {
                "metric": metric,
                "unit": UNITS[metric],
                "current": round(base_current, 2),
                "available": True,
                "samples": len(series),
                "raw_samples": len(pairs),
                "model": "SARIMAX",
                "order": list(order),
                "seasonal_order": list(seasonal_order),
                "seasonal_period": 144,
                "seasonal_mode": "fourier-exog",
                "exog": ["hour_sin", "hour_cos", "hour2_sin", "hour2_cos", "weekday_sin", "weekday_cos"],
                "resample_seconds": resample_seconds,
                "horizon_min": horizon_min,
                "target_ms": last_ts + horizon_min * 60_000,
                "predicted": round(predicted, 2),
                "lower": round(lower, 2),
                "upper": round(upper, 2),
                "delta": round(delta, 2),
                "confidence": round(confidence, 2),
                "trend": "rising" if delta > 0.3 else "falling" if delta < -0.3 else "stable",
                "reason": (
                    "SARIMAX{} + 鏃?鍛ㄥ倕閲屽彾澶栫敓椤癸紝鍩轰簬 {} 涓獅}绉掗噸閲囨牱鐐?.format(
                        order, len(series), resample_seconds
                    )
                ),
                "r2": None,
                "path": path,
            }
        except Exception:
            # Convergence failures and too-short series fall back to the
            # deterministic least-squares implementation below.
            return None

    def _metric(self, points: list[dict[str, Any]], metric: str, horizon_min: int,
                current: dict[str, Any]) -> dict[str, Any]:
        pairs: list[tuple[int, float]] = []
        for point in points:
            value = _finite(point.get(metric))
            ts = point.get("ts_ms")
            if value is None or ts is None:
                continue
            low, high = PHYSICAL[metric]
            if value < low or value > high:
                continue
            pairs.append((int(ts), value))
        pairs.sort(key=lambda item: item[0])
        base_current = _finite(current.get(metric))
        if base_current is None and pairs:
            base_current = pairs[-1][1]
        result: dict[str, Any] = {
            "metric": metric,
            "unit": UNITS[metric],
            "current": round(base_current, 2) if base_current is not None else None,
            "available": False,
            "samples": len(pairs),
            "model": "insufficient",
            "horizon_min": horizon_min,
            "target_ms": None,
            "predicted": None,
            "lower": None,
            "upper": None,
            "delta": None,
            "confidence": 0.0,
            "reason": "鏈夋晥鏍锋湰灏戜簬 3 涓?,
        }
        if len(pairs) < 3:
            return result

        # Prefer a real time-series model when statsmodels is available.
        # A linear fallback keeps the gateway usable on a minimal install.
        if SARIMAX_AVAILABLE:
            sarimax_result = self._sarimax_metric(pairs, metric, horizon_min, current)
            if sarimax_result is not None:
                return sarimax_result

        # Use seconds relative to the first sample to keep the normal equations
        # well-conditioned even for long-running datasets.
        t0 = pairs[0][0]
        xs = [(ts - t0) / 1000.0 for ts, _ in pairs]
        ys = [value for _, value in pairs]
        n = len(xs)
        mean_x = sum(xs) / n
        mean_y = sum(ys) / n
        sxx = sum((x - mean_x) ** 2 for x in xs)
        if sxx <= 1e-9:
            return result
        sxy = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
        slope = sxy / sxx
        # Clamp implausible extrapolation: max ~12掳C / 10 min or 30%RH / 10 min.
        max_slope = 0.02 if metric == "temperature" else 0.05
        slope = max(-max_slope, min(max_slope, slope))
        intercept = mean_y - slope * mean_x
        last_x = xs[-1]
        target_x = last_x + horizon_min * 60.0
        predicted = intercept + slope * target_x
        predicted = _clamp(metric, predicted)

        residuals = [y - (intercept + slope * x) for x, y in zip(xs, ys)]
        residual_std = math.sqrt(sum(r * r for r in residuals) / max(1, n - 2))
        interval = 1.96 * residual_std * math.sqrt(1 + 1 / n)
        lower = _clamp(metric, predicted - interval)
        upper = _clamp(metric, predicted + interval)

        # R虏 and sample count both matter; small samples are explicitly
        # de-rated instead of being presented as a confident AI result.
        ss_tot = sum((y - mean_y) ** 2 for y in ys)
        r2 = 1.0 - (sum(r * r for r in residuals) / ss_tot) if ss_tot > 1e-9 else 0.0
        r2 = max(0.0, min(1.0, r2))
        confidence = 0.30 + 0.45 * r2 + 0.20 * min(1.0, n / 30.0)
        confidence = max(0.0, min(0.92, confidence))

        base_current = base_current if base_current is not None else ys[-1]
        delta = predicted - base_current
        path: list[dict[str, Any]] = []
        for step in range(0, horizon_min + 1):
            x = last_x + step * 60.0
            value = base_current if step == 0 else _clamp(metric, intercept + slope * x)
            path.append({
                "ts_ms": int(pairs[-1][0] + step * 60_000),
                "value": round(value, 2),
                "lower": round(_clamp(metric, value - interval), 2),
                "upper": round(_clamp(metric, value + interval), 2),
            })
        result.update({
            "available": True,
            "model": "linear-trend",
            "target_ms": int(pairs[-1][0] + horizon_min * 60_000),
            "predicted": round(predicted, 2),
            "lower": round(lower, 2),
            "upper": round(upper, 2),
            "delta": round(delta, 2),
            "confidence": round(confidence, 2),
            "trend": "rising" if delta > 0.3 else "falling" if delta < -0.3 else "stable",
            "reason": "鍩轰簬 {} 涓牱鏈殑绾挎€ц秼鍔块娴?.format(n),
            "r2": round(r2, 3),
            "path": path,
        })
        return result


class AlertService:
    """Turn current values and forecasts into four-level, deduplicated alerts."""

    def __init__(self, store: Any, command: Callable[[str, dict[str, Any]], Any] | None = None,
                 thresholds: Thresholds | None = None, auto_control: bool = False) -> None:
        self.store = store
        self.command = command
        self.thresholds = thresholds or Thresholds()
        self.auto_control = bool(auto_control)

    def evaluate(self, forecast: dict[str, Any]) -> list[dict[str, Any]]:
        current = forecast.get("current") or {}
        run_id = forecast.get("run_id")
        mode = str(current.get("mode") or "auto")
        created: list[dict[str, Any]] = []
        for metric in ("temperature", "humidity", "lux"):
            item = forecast.get(metric) if metric in METRICS else None
            cur = _finite(current.get(metric))
            if metric == "lux":
                # Lux is a current-state alert, not a future forecast.
                pred = None
                if cur is None:
                    continue
            else:
                item = item or {}
                pred = _finite(item.get("predicted"))
                if cur is None and pred is None:
                    continue
            level, threshold, reason = self._level(metric, cur, pred, forecast.get("horizon_min", 10))
            if level == "normal":
                continue
            action = self._action(metric, level, mode)
            message = self._message(metric, level, cur, pred, threshold, reason)
            alert = self.store.record_alert(
                run_id=run_id,
                level=level,
                metric=metric,
                current=cur,
                predicted=pred,
                threshold=threshold,
                message=message,
                action=action,
                source="prediction" if pred is not None and (cur is None or self._prediction_triggered(metric, cur, pred)) else "current",
                confidence=item.get("confidence", 0.0) if isinstance(item, dict) else 0.0,
                payload={"reason": reason, "mode": mode, "forecast": item},
            )
            if alert is None:
                continue
            created.append(alert)
            self._maybe_auto_control(metric, level, mode, current)
        return created

    def _prediction_triggered(self, metric: str, cur: float, pred: float) -> bool:
        if metric == "temperature":
            return pred > self.thresholds.temp_watch and cur <= self.thresholds.temp_watch
        if metric == "humidity":
            return pred > self.thresholds.humidity_watch and cur <= self.thresholds.humidity_watch
        return False

    def _level(self, metric: str, cur: float | None, pred: float | None, horizon: int) -> tuple[str, float, str]:
        t = self.thresholds
        if metric == "temperature":
            if (cur is not None and cur > t.temp_critical) or (cur is not None and pred is not None and pred - cur > 3.0):
                return "critical", t.temp_critical, "褰撳墠娓╁害瓒呰繃涓ラ噸闃堝€硷紝鎴?10 鍒嗛挓鍗囨俯瓒呰繃 3掳C"
            if (cur is not None and cur > t.temp_warning) or (pred is not None and pred > t.temp_warning):
                return "warning", t.temp_warning, "褰撳墠鎴栭娴嬫俯搴﹁秴杩囪鍛婇槇鍊?
            if pred is not None and pred > t.temp_watch:
                return "watch", t.temp_watch, "棰勬祴娓╁害灏嗚秴杩囧叧娉ㄩ槇鍊?
        elif metric == "humidity":
            if (cur is not None and cur > t.humidity_critical) or (cur is not None and pred is not None and pred - cur > 10.0):
                return "critical", t.humidity_critical, "褰撳墠婀垮害瓒呰繃涓ラ噸闃堝€硷紝鎴?10 鍒嗛挓鍗囨箍瓒呰繃 10%"
            if (cur is not None and cur > t.humidity_warning) or (pred is not None and pred > t.humidity_warning):
                return "warning", t.humidity_warning, "褰撳墠鎴栭娴嬫箍搴﹁秴杩囪鍛婇槇鍊?
            if pred is not None and pred > t.humidity_watch:
                return "watch", t.humidity_watch, "棰勬祴婀垮害灏嗚秴杩囧叧娉ㄩ槇鍊?
        elif metric == "lux":
            if cur is not None and cur < t.lux_warning:
                return "warning", t.lux_warning, "褰撳墠鍏夌収浣庝簬璀﹀憡闃堝€?
            if cur is not None and cur < t.lux_watch:
                return "watch", t.lux_watch, "褰撳墠鍏夌収浣庝簬鍏虫敞闃堝€?
        return "normal", 0.0, ""

    def _action(self, metric: str, level: str, mode: str) -> str:
        if metric == "lux":
            return "寤鸿鎵撳紑琛ュ厜鐏? if level in {"watch", "warning"} else "妫€鏌ュ厜鐓?
        if metric in {"temperature", "humidity"}:
            if mode == "manual":
                return "寤鸿鎵嬪姩鎵撳紑椋庢墖" if level in {"watch", "warning", "critical"} else "妫€鏌ョ幆澧?
            return "鑷姩鎵撳紑椋庢墖" if level in {"warning", "critical"} else "鍏虫敞娓╂箍搴﹀彉鍖?
        return "妫€鏌ョ幆澧?

    def _message(self, metric: str, level: str, cur: float | None, pred: float | None,
                 threshold: float, reason: str) -> str:
        label = {"watch": "鍏虫敞", "warning": "璀﹀憡", "critical": "涓ラ噸"}.get(level, level)
        parts = ["{} {}棰勮".format(label, "娓╁害" if metric == "temperature" else "婀垮害" if metric == "humidity" else "鍏夌収")]
        if cur is not None:
            parts.append("褰撳墠 {:.1f}{}".format(cur, UNITS[metric]))
        if pred is not None:
            parts.append("棰勬祴 {:.1f}{}".format(pred, UNITS[metric]))
        if threshold:
            parts.append("闃堝€?{:.1f}{}".format(threshold, UNITS[metric]))
        return "锛?.join(parts) + "锛? + reason

    def _maybe_auto_control(self, metric: str, level: str, mode: str, current: dict[str, Any]) -> None:
        if not self.auto_control or self.command is None or mode == "manual":
            return
        if level not in {"warning", "critical"}:
            return
        if metric in {"temperature", "humidity"} and not current.get("fan"):
            self.command("ia1", {"action": "fan", "value": 1})
        elif metric == "lux" and not current.get("light"):
            self.command("ia1", {"action": "light", "value": 1})

