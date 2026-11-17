"""FreshChain local gateway.

The gateway is deliberately dependency-light: the HTTP server, SQLite storage,
demo simulator, and dashboard are built on the Python standard library.  MQTT
support is optional and uses paho-mqtt when it is installed.
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import os
import sqlite3
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable
from urllib.parse import parse_qs, urlparse

from ai_service import AlertService, ForecastService, Thresholds


ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"
DEFAULT_DB = ROOT / "freshchain.db"
LOG = logging.getLogger("freshchain")

IA1_TOPIC = "freshchain/ia1/telemetry"
ST1_TOPIC = "freshchain/st1/telemetry"
IA1_COMMAND_TOPIC = "freshchain/ia1/command"
ST1_COMMAND_TOPIC = "freshchain/st1/command"
EVENT_TOPIC = "freshchain/event"
NODE_ONLINE_SECONDS = 15
MAP_UNITS = {"temperature": "掳C", "humidity": "%", "lux": "lx"}


def now_ms() -> int:
    return int(time.time() * 1000)


def iso_ms(epoch_ms: int | None) -> str | None:
    if epoch_ms is None:
        return None
    return datetime.fromtimestamp(epoch_ms / 1000, timezone.utc).astimezone().isoformat(timespec="seconds")


def finite_number(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


@dataclass
class RuntimeState:
    latest: dict[str, dict[str, Any]] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)
    track: list[dict[str, Any]] = field(default_factory=list)
    commands: list[dict[str, Any]] = field(default_factory=list)
    broker_connected: bool = False
    demo: bool = False
    started_at: int = field(default_factory=now_ms)


class Store:
    """Thread-safe state and SQLite persistence."""

    def __init__(self, db_path: Path, reset: bool = False) -> None:
        self.db_path = db_path
        self.lock = threading.RLock()
        self.state = RuntimeState()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if reset and self.db_path.exists():
            self.db_path.unlink()
        self.db = sqlite3.connect(self.db_path, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self._ia1_recent: list[tuple[int, dict[str, Any]]] = []
        self._pending_st1: list[tuple[int, dict[str, Any]]] = []
        self._aligner_stop = False
        self._init_db()
        self._abort_stale_runs()
        self._load_recent()
        self._aligner_thread = threading.Thread(
            target=self._align_loop, name="freshchain-aligner", daemon=True
        )
        self._aligner_thread.start()

    def _init_db(self) -> None:
        with self.db:
            self.db.executescript(
                """
                CREATE TABLE IF NOT EXISTS telemetry (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    received_ms INTEGER NOT NULL,
                    node TEXT NOT NULL,
                    payload TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_telemetry_node_time
                    ON telemetry(node, received_ms DESC);
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    received_ms INTEGER NOT NULL,
                    node TEXT,
                    level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    payload TEXT
                );
                CREATE INDEX IF NOT EXISTS idx_events_time
                    ON events(received_ms DESC);
                CREATE TABLE IF NOT EXISTS commands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sent_ms INTEGER NOT NULL,
                    node TEXT NOT NULL,
                    payload TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    label TEXT,
                    route_name TEXT,
                    started_ms INTEGER NOT NULL,
                    ended_ms INTEGER,
                    status TEXT NOT NULL CHECK(status IN ('active','completed','aborted')),
                    notes TEXT
                );
                CREATE INDEX IF NOT EXISTS idx_runs_time
                    ON runs(started_ms DESC);
                CREATE TABLE IF NOT EXISTS route_points (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER NOT NULL,
                    seq INTEGER NOT NULL,
                    gps_ms INTEGER NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    ia1_ms INTEGER,
                    temperature REAL,
                    humidity REAL,
                    lux REAL,
                    ia1_delta_ms INTEGER,
                    quality TEXT NOT NULL DEFAULT 'ok',
                    FOREIGN KEY(run_id) REFERENCES runs(id)
                );
                CREATE INDEX IF NOT EXISTS idx_route_run_seq
                    ON route_points(run_id, seq);
                CREATE INDEX IF NOT EXISTS idx_route_run_time
                    ON route_points(run_id, gps_ms);
                CREATE TABLE IF NOT EXISTS forecasts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER,
                    created_ms INTEGER NOT NULL,
                    target_ms INTEGER,
                    horizon_min INTEGER NOT NULL,
                    latitude REAL,
                    longitude REAL,
                    metric TEXT NOT NULL CHECK(metric IN ('temperature','humidity')),
                    value REAL NOT NULL,
                    lower REAL,
                    upper REAL,
                    model TEXT NOT NULL,
                    confidence REAL,
                    FOREIGN KEY(run_id) REFERENCES runs(id)
                );
                CREATE INDEX IF NOT EXISTS idx_forecast_run_metric
                    ON forecasts(run_id, metric, created_ms DESC);
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER,
                    ts_ms INTEGER NOT NULL,
                    level TEXT NOT NULL CHECK(level IN ('watch','warning','critical')),
                    metric TEXT NOT NULL,
                    current_value REAL,
                    predicted_value REAL,
                    threshold REAL,
                    message TEXT NOT NULL,
                    action TEXT,
                    source TEXT,
                    confidence REAL,
                    acknowledged_ms INTEGER,
                    payload TEXT
                );
                CREATE INDEX IF NOT EXISTS idx_alerts_time
                    ON alerts(ts_ms DESC);
                CREATE INDEX IF NOT EXISTS idx_alerts_metric_level
                    ON alerts(metric, level, ts_ms DESC);
                """
            )

    def _abort_stale_runs(self) -> None:
        with self.db:
            self.db.execute(
                "UPDATE runs SET status = 'aborted', ended_ms = ?, "
                "notes = COALESCE(notes || ' | ', '') || 'gateway restarted' "
                "WHERE status = 'active'",
                (now_ms(),),
            )

    def _load_recent(self) -> None:
        with self.lock:
            rows = self.db.execute(
                "SELECT received_ms, node, payload FROM telemetry ORDER BY id DESC LIMIT 400"
            ).fetchall()
            for row in reversed(rows):
                payload = self._decode(row[2])
                self._apply_telemetry(row[1], payload, row[0], persist=False)
            event_rows = self.db.execute(
                "SELECT received_ms, node, level, message, payload FROM events ORDER BY id DESC LIMIT 50"
            ).fetchall()
            self.state.events = [
                {
                    "time": iso_ms(row[0]),
                    "node": row[1],
                    "level": row[2],
                    "message": row[3],
                    "payload": self._decode(row[4]) if row[4] else None,
                }
                for row in reversed(event_rows)
            ]

    @staticmethod
    def _decode(raw: str | None) -> dict[str, Any]:
        if not raw:
            return {}
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return {"raw": raw}
        return data if isinstance(data, dict) else {"value": data}

    def _apply_telemetry(self, node: str, payload: dict[str, Any], received_ms: int, persist: bool) -> None:
        payload = dict(payload)
        payload["node"] = node
        payload["received_ms"] = received_ms
        payload["received_at"] = iso_ms(received_ms)
        self.state.latest[node] = payload

        if node == "st1":
            lat = finite_number(payload.get("latitude"))
            lon = finite_number(payload.get("longitude"))
            if payload.get("gps_valid") and lat is not None and lon is not None:
                self.state.track.append(
                    {"lat": lat, "lon": lon, "time": payload["received_at"], "alarm": bool(payload.get("alarm"))}
                )
                self.state.track = self.state.track[-300:]

        if persist:
            self.db.execute(
                "INSERT INTO telemetry(received_ms, node, payload) VALUES (?, ?, ?)",
                (received_ms, node, json.dumps(payload, ensure_ascii=False)),
            )
            self.db.commit()

    def record_telemetry(self, node: str, payload: dict[str, Any], received_ms: int | None = None) -> None:
        if node not in {"ia1", "st1"}:
            raise ValueError("node must be ia1 or st1")
        if not isinstance(payload, dict):
            raise ValueError("telemetry payload must be an object")
        received_ms = received_ms or now_ms()
        with self.lock:
            previous = self.state.latest.get(node, {})
            previous_environment = previous.get("environment_status")
            previous_alarm = bool(previous.get("alarm"))
            self._apply_telemetry(node, payload, received_ms, persist=True)
            if (
                node == "ia1"
                and payload.get("environment_status") in {"warning", "abnormal", "fault"}
                and payload.get("environment_status") != previous_environment
            ):
                self.add_event(node, "warning", f"浜у湴鐜鐘舵€侊細{payload.get('environment_status')}", payload)
            if node == "st1" and payload.get("alarm") and not previous_alarm:
                self.add_event(node, "alarm", "杩愯緭鑺傜偣瑙﹀彂鎶ヨ", payload)
            self._handle_run_telemetry(node, payload, received_ms)

    def add_event(self, node: str | None, level: str, message: str, payload: dict[str, Any] | None = None) -> None:
        with self.lock:
            event = {
                "time": iso_ms(now_ms()),
                "node": node,
                "level": level,
                "message": message,
                "payload": payload,
            }
            self.state.events.append(event)
            self.state.events = self.state.events[-100:]
            self.db.execute(
                "INSERT INTO events(received_ms, node, level, message, payload) VALUES (?, ?, ?, ?, ?)",
                (now_ms(), node, level, message, json.dumps(payload, ensure_ascii=False) if payload else None),
            )
            self.db.commit()

    def record_command(self, node: str, payload: dict[str, Any]) -> None:
        with self.lock:
            item = {"time": iso_ms(now_ms()), "node": node, "payload": payload}
            self.state.commands.append(item)
            self.state.commands = self.state.commands[-50:]
            self.db.execute(
                "INSERT INTO commands(sent_ms, node, payload) VALUES (?, ?, ?)",
                (now_ms(), node, json.dumps(payload, ensure_ascii=False)),
            )
            self.db.commit()

    def snapshot(self) -> dict[str, Any]:
        with self.lock:
            latest = {node: dict(payload) for node, payload in self.state.latest.items()}
            now = now_ms()
            nodes: dict[str, dict[str, Any]] = {}
            for node in ("ia1", "st1"):
                payload = latest.get(node, {})
                last_seen_ms = payload.get("received_ms")
                age_sec = None
                if last_seen_ms:
                    age_sec = round(max(0.0, (now - int(last_seen_ms)) / 1000.0), 1)
                nodes[node] = {
                    "online": bool(age_sec is not None and age_sec <= NODE_ONLINE_SECONDS),
                    "age_sec": age_sec,
                    "last_seen": payload.get("received_at"),
                    "last_seen_ms": last_seen_ms,
                }
            return {
                "latest": latest,
                "nodes": nodes,
                "events": list(reversed(self.state.events[-50:])),
                "track": list(self.state.track),
                "broker_connected": self.state.broker_connected,
                "demo": self.state.demo,
                "started_at": iso_ms(self.state.started_at),
                "run": self.display_run(),
                "alerts": self.list_alerts(5),
            }

    def close(self) -> None:
        self._aligner_stop = True
        with self.lock:
            self.db.close()
        self._aligner_thread.join(timeout=1.0)

    def history(self, node: str, limit: int = 100) -> list[dict[str, Any]]:
        limit = max(1, min(limit, 1000))
        with self.lock:
            rows = self.db.execute(
                "SELECT received_ms, node, payload FROM telemetry WHERE node = ? ORDER BY id DESC LIMIT ?",
                (node, limit),
            ).fetchall()
            result = []
            for row in reversed(rows):
                payload = self._decode(row[2])
                payload["node"] = row[1]
                payload["received_at"] = iso_ms(row[0])
                result.append(payload)
            return result

    def telemetry_series(self, node: str = "ia1", minutes: int = 30, limit: int = 1200) -> dict[str, Any]:
        """Return recent telemetry for the single-point time-series view.

        The single-point mode is deliberately independent of route points:
        the car can stay still while the user watches one location over time.
        """
        minutes = max(1, min(int(minutes), 1440))
        limit = max(30, min(int(limit), 5000))
        now = now_ms()
        since_ms = now - minutes * 60_000
        with self.lock:
            last_seen_ms = self.state.latest.get(node, {}).get("received_ms")
            age_sec = None
            if last_seen_ms:
                age_sec = max(0.0, (now - int(last_seen_ms)) / 1000.0)
            if age_sec is None or age_sec > NODE_ONLINE_SECONDS:
                return {
                    "source": "telemetry",
                    "node": node,
                    "minutes": minutes,
                    "run_id": None,
                    "runs": 0,
                    "online": False,
                    "age_sec": round(age_sec, 1) if age_sec is not None else None,
                    "points": [],
                }
            rows = self.db.execute(
                "SELECT received_ms, payload FROM telemetry WHERE node = ? "
                "AND received_ms >= ? ORDER BY id DESC LIMIT ?",
                (node, since_ms, limit),
            ).fetchall()
            points: list[dict[str, Any]] = []
            for row in reversed(rows):
                payload = self._decode(row["payload"])
                values = {
                    "temperature": finite_number(payload.get("temperature")),
                    "humidity": finite_number(payload.get("humidity")),
                    "lux": finite_number(payload.get("lux")),
                }
                if all(value is None for value in values.values()):
                    continue
                points.append({
                    "run_id": None,
                    "seq": 0,
                    "ts_ms": row["received_ms"],
                    "latitude": None,
                    "longitude": None,
                    "mode": payload.get("mode"),
                    "fan": payload.get("fan"),
                    "light": payload.get("light"),
                    **values,
                })
            return {"source": "telemetry", "node": node, "minutes": minutes,
                    "run_id": None, "runs": 0, "online": True,
                    "age_sec": round(age_sec, 1) if age_sec is not None else None,
                    "points": points}

    # ------------------------------------------------------------------
    # AI data access and alert persistence
    # ------------------------------------------------------------------

    def current_environment(self) -> dict[str, Any]:
        """Return the latest IA1 environment values used by the AI layer."""
        with self.lock:
            payload = dict(self.state.latest.get("ia1", {}))
        return payload

    def ai_series(self, run_id: int | None = None, limit: int = 2400) -> dict[str, Any]:
        """Return the best available time series for forecasting.

        Route points are preferred because they are GPS/environment paired.
        Before a route is complete, live IA1 telemetry is a useful fallback.
        """
        limit = max(30, min(int(limit), 5000))
        with self.lock:
            if run_id is not None:
                rows = self.db.execute(
                    "SELECT p.run_id, p.seq, p.gps_ms, p.latitude, p.longitude, "
                    "p.temperature, p.humidity, p.lux "
                    "FROM route_points p JOIN runs r ON r.id = p.run_id "
                    "WHERE p.run_id = ? AND p.quality = 'ok' "
                    "ORDER BY p.gps_ms DESC LIMIT ?",
                    (int(run_id), limit),
                ).fetchall()
            else:
                rows = self.db.execute(
                    "SELECT p.run_id, p.seq, p.gps_ms, p.latitude, p.longitude, "
                    "p.temperature, p.humidity, p.lux "
                    "FROM route_points p JOIN runs r ON r.id = p.run_id "
                    "WHERE p.quality = 'ok' "
                    "ORDER BY p.gps_ms DESC LIMIT ?",
                    (limit,),
                ).fetchall()
            points: list[dict[str, Any]] = []
            for row in reversed(rows):
                values = {
                    "temperature": finite_number(row["temperature"]),
                    "humidity": finite_number(row["humidity"]),
                    "lux": finite_number(row["lux"]),
                }
                if all(value is None for value in values.values()):
                    continue
                points.append({
                    "run_id": row["run_id"],
                    "seq": row["seq"],
                    "ts_ms": row["gps_ms"],
                    "latitude": row["latitude"],
                    "longitude": row["longitude"],
                    **values,
                })
            if points:
                latest_run = run_id if run_id is not None else points[-1]["run_id"]
                distinct_runs = len({point["run_id"] for point in points})
                return {
                    "source": "route_points",
                    "run_id": latest_run,
                    "runs": distinct_runs,
                    "points": points,
                }

            if run_id is not None:
                return {"source": "route_points", "run_id": run_id, "runs": 0, "points": []}

            # Fallback: recent live IA1 telemetry, useful before the first route.
            telemetry_rows = self.db.execute(
                "SELECT received_ms, payload FROM telemetry WHERE node = 'ia1' "
                "ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
            for row in reversed(telemetry_rows):
                payload = self._decode(row["payload"])
                values = {
                    "temperature": finite_number(payload.get("temperature")),
                    "humidity": finite_number(payload.get("humidity")),
                    "lux": finite_number(payload.get("lux")),
                }
                if all(value is None for value in values.values()):
                    continue
                points.append({
                    "run_id": None,
                    "seq": 0,
                    "ts_ms": row["received_ms"],
                    "latitude": None,
                    "longitude": None,
                    **values,
                })
            return {"source": "telemetry", "run_id": None, "runs": 0, "points": points}

    def _alert_row(self, row: sqlite3.Row) -> dict[str, Any]:
        return {
            "id": row["id"],
            "run_id": row["run_id"],
            "time": iso_ms(row["ts_ms"]),
            "ts_ms": row["ts_ms"],
            "level": row["level"],
            "metric": row["metric"],
            "current": row["current_value"],
            "predicted": row["predicted_value"],
            "threshold": row["threshold"],
            "message": row["message"],
            "action": row["action"],
            "source": row["source"],
            "confidence": row["confidence"],
            "acknowledged": row["acknowledged_ms"] is not None,
            "acknowledged_at": iso_ms(row["acknowledged_ms"]) if row["acknowledged_ms"] else None,
            "payload": self._decode(row["payload"]) if row["payload"] else None,
        }

    def record_alert(self, *, run_id: int | None, level: str, metric: str,
                     current: float | None, predicted: float | None,
                     threshold: float | None, message: str, action: str | None,
                     source: str = "current", confidence: float = 0.0,
                     payload: dict[str, Any] | None = None,
                     cooldown_sec: int = 60) -> dict[str, Any] | None:
        """Persist an alert unless the same metric/level fired recently."""
        if level not in {"watch", "warning", "critical"}:
            return None
        ts_ms = now_ms()
        with self.lock:
            exists = self.db.execute(
                "SELECT id FROM alerts WHERE metric = ? AND level = ? AND ts_ms >= ? "
                "ORDER BY id DESC LIMIT 1",
                (metric, level, ts_ms - max(0, cooldown_sec) * 1000),
            ).fetchone()
            if exists is not None:
                return None
            cursor = self.db.execute(
                "INSERT INTO alerts(run_id, ts_ms, level, metric, current_value, "
                "predicted_value, threshold, message, action, source, confidence, payload) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    run_id, ts_ms, level, metric, current, predicted, threshold,
                    message, action, source, confidence,
                    json.dumps(payload, ensure_ascii=False) if payload else None,
                ),
            )
            self.db.commit()
            row = self.db.execute("SELECT * FROM alerts WHERE id = ?", (cursor.lastrowid,)).fetchone()
            alert = self._alert_row(row)
            self.add_event("ai", "alarm" if level == "critical" else "warning", message, alert)
            return alert

    def list_alerts(self, limit: int = 30, run_id: int | None = None) -> list[dict[str, Any]]:
        limit = max(1, min(int(limit), 200))
        with self.lock:
            if run_id is None:
                rows = self.db.execute(
                    "SELECT * FROM alerts ORDER BY id DESC LIMIT ?", (limit,)
                ).fetchall()
            else:
                rows = self.db.execute(
                    "SELECT * FROM alerts WHERE run_id = ? ORDER BY id DESC LIMIT ?",
                    (int(run_id), limit),
                ).fetchall()
            return [self._alert_row(row) for row in rows]

    def acknowledge_alert(self, alert_id: int) -> dict[str, Any] | None:
        with self.lock:
            self.db.execute(
                "UPDATE alerts SET acknowledged_ms = ? WHERE id = ? AND acknowledged_ms IS NULL",
                (now_ms(), int(alert_id)),
            )
            self.db.commit()
            row = self.db.execute("SELECT * FROM alerts WHERE id = ?", (int(alert_id),)).fetchone()
            return self._alert_row(row) if row else None

    # ------------------------------------------------------------------
    # Route runs and GPS/environment pairing
    # ------------------------------------------------------------------

    @staticmethod
    def _run_row(row: sqlite3.Row | None) -> dict[str, Any] | None:
        if row is None:
            return None
        return {
            "id": row["id"],
            "label": row["label"],
            "route_name": row["route_name"],
            "started_ms": row["started_ms"],
            "started_at": iso_ms(row["started_ms"]),
            "ended_ms": row["ended_ms"],
            "ended_at": iso_ms(row["ended_ms"]) if row["ended_ms"] else None,
            "status": row["status"],
            "notes": row["notes"],
            "points": row["points"] if "points" in row.keys() else 0,
            "valid_points": row["valid_points"] if "valid_points" in row.keys() else 0,
        }

    def _active_run_locked(self) -> sqlite3.Row | None:
        return self.db.execute(
            "SELECT * FROM runs WHERE status = 'active' ORDER BY id DESC LIMIT 1"
        ).fetchone()

    def start_run(self, label: str | None = None, route_name: str | None = None) -> dict[str, Any]:
        with self.lock:
            if self._active_run_locked() is not None:
                raise ValueError("宸叉湁姝ｅ湪閲囬泦鐨勮矾绾匡紝璇峰厛缁撴潫璺嚎")
            st1 = self.state.latest.get("st1", {})
            if not st1.get("gps_valid"):
                raise ValueError("GPS 灏氭湭瀹氫綅锛岃鍒板澶栫瓑寰呭畾浣嶅悗鍐嶅紑濮嬭矾绾?)
            started_ms = now_ms()
            cursor = self.db.execute(
                "INSERT INTO runs(label, route_name, started_ms, status) VALUES (?, ?, ?, 'active')",
                (label or datetime.now().strftime("%Y-%m-%d %H:%M:%S"), route_name or "榛樿璺嚎", started_ms),
            )
            self.db.commit()
            self._pending_st1.clear()
            run = self.db.execute("SELECT * FROM runs WHERE id = ?", (cursor.lastrowid,)).fetchone()
            return self._run_row(run) or {}

    def stop_run(self, run_id: int, status: str = "completed") -> dict[str, Any]:
        if status not in {"completed", "aborted"}:
            raise ValueError("status 蹇呴』鏄?completed 鎴?aborted")
        with self.lock:
            row = self.db.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
            if row is None:
                raise ValueError("璺嚎涓嶅瓨鍦?)
            if row["status"] != "active":
                raise ValueError("璇ヨ矾绾垮凡缁忕粨鏉?)
            # Pair the tail of the route immediately instead of dropping the last few points.
            self._flush_pending_locked(now_ms(), force=True)
            ended_ms = now_ms()
            self.db.execute(
                "UPDATE runs SET ended_ms = ?, status = ? WHERE id = ?",
                (ended_ms, status, run_id),
            )
            self.db.commit()
            return self.get_run(run_id) or {}

    def current_run(self) -> dict[str, Any] | None:
        with self.lock:
            row = self.db.execute(
                "SELECT r.*, "
                "(SELECT COUNT(*) FROM route_points p WHERE p.run_id = r.id) AS points, "
                "(SELECT COUNT(*) FROM route_points p WHERE p.run_id = r.id AND p.quality = 'ok') AS valid_points "
                "FROM runs r WHERE r.status = 'active' ORDER BY r.id DESC LIMIT 1"
            ).fetchone()
            return self._run_row(row)

    def display_run(self) -> dict[str, Any] | None:
        active = self.current_run()
        if active is not None:
            return active
        runs = self.list_runs(1)
        return runs[0] if runs else None

    def list_runs(self, limit: int = 20) -> list[dict[str, Any]]:
        limit = max(1, min(limit, 100))
        with self.lock:
            rows = self.db.execute(
                "SELECT r.*, "
                "(SELECT COUNT(*) FROM route_points p WHERE p.run_id = r.id) AS points, "
                "(SELECT COUNT(*) FROM route_points p WHERE p.run_id = r.id AND p.quality = 'ok') AS valid_points "
                "FROM runs r ORDER BY r.id DESC LIMIT ?",
                (limit,),
            ).fetchall()
            return [self._run_row(row) or {} for row in rows]

    def get_run(self, run_id: int) -> dict[str, Any] | None:
        with self.lock:
            row = self.db.execute(
                "SELECT r.*, "
                "(SELECT COUNT(*) FROM route_points p WHERE p.run_id = r.id) AS points, "
                "(SELECT COUNT(*) FROM route_points p WHERE p.run_id = r.id AND p.quality = 'ok') AS valid_points "
                "FROM runs r WHERE r.id = ?",
                (run_id,),
            ).fetchone()
            return self._run_row(row)

    def _handle_run_telemetry(self, node: str, payload: dict[str, Any], received_ms: int) -> None:
        with self.lock:
            if node == "ia1":
                self._ia1_recent.append((received_ms, dict(payload)))
                cutoff = received_ms - 10_000
                self._ia1_recent = [item for item in self._ia1_recent if item[0] >= cutoff]
                return
            if node == "st1" and payload.get("gps_valid") and self._active_run_locked() is not None:
                self._pending_st1.append((received_ms, dict(payload)))

    def _nearest_ia1_locked(self, gps_ms: int) -> tuple[dict[str, Any] | None, int | None]:
        best: dict[str, Any] | None = None
        best_delta: int | None = None
        for ia1_ms, payload in self._ia1_recent:
            delta = abs(ia1_ms - gps_ms)
            if best_delta is None or delta < best_delta:
                best = dict(payload, _ia1_ms=ia1_ms)
                best_delta = delta
        if best is None or best_delta is None or best_delta > 2500:
            return None, best_delta
        return best, best_delta

    def _flush_pending_locked(self, current_ms: int, force: bool = False) -> int:
        active = self._active_run_locked()
        if active is None:
            self._pending_st1.clear()
            return 0
        ready: list[tuple[int, dict[str, Any]]] = []
        keep: list[tuple[int, dict[str, Any]]] = []
        for gps_ms, payload in self._pending_st1:
            if force or current_ms - gps_ms >= 2500:
                ready.append((gps_ms, payload))
            else:
                keep.append((gps_ms, payload))
        self._pending_st1 = keep
        if not ready:
            return 0
        run_id = int(active["id"])
        seq = self.db.execute(
            "SELECT COALESCE(MAX(seq), 0) + 1 FROM route_points WHERE run_id = ?",
            (run_id,),
        ).fetchone()[0]
        count = 0
        for gps_ms, payload in ready:
            latitude = finite_number(payload.get("latitude"))
            longitude = finite_number(payload.get("longitude"))
            if latitude is None or longitude is None:
                continue
            env, delta = self._nearest_ia1_locked(gps_ms)
            quality = "ok" if env is not None else "missing_env"
            self.db.execute(
                "INSERT INTO route_points("
                "run_id, seq, gps_ms, latitude, longitude, ia1_ms, temperature, humidity, lux, ia1_delta_ms, quality"
                ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    run_id,
                    seq,
                    gps_ms,
                    latitude,
                    longitude,
                    None if env is None else env.get("_ia1_ms"),
                    None if env is None else finite_number(env.get("temperature")),
                    None if env is None else finite_number(env.get("humidity")),
                    None if env is None else finite_number(env.get("lux")),
                    delta,
                    quality,
                ),
            )
            seq += 1
            count += 1
        self.db.commit()
        return count

    def _align_loop(self) -> None:
        while not self._aligner_stop:
            time.sleep(0.2)
            if self._aligner_stop:
                break
            try:
                with self.lock:
                    self._flush_pending_locked(now_ms())
            except Exception:  # pragma: no cover - background safety
                LOG.exception("route aligner failed")

    # ------------------------------------------------------------------
    # Temperature / humidity / light map
    # ------------------------------------------------------------------

    def build_map(self, run_id: int, metric: str = "temperature", cols: int = 60, rows: int = 60) -> dict[str, Any]:
        if metric not in MAP_UNITS:
            raise ValueError("metric 蹇呴』鏄?temperature銆乭umidity 鎴?lux")
        cols = max(10, min(int(cols), 100))
        rows = max(10, min(int(rows), 100))
        with self.lock:
            run = self.get_run(run_id)
            if run is None:
                raise ValueError("璺嚎涓嶅瓨鍦?)
            points = self.db.execute(
                "SELECT seq, gps_ms, latitude, longitude, temperature, humidity, lux, quality "
                "FROM route_points WHERE run_id = ? ORDER BY seq",
                (run_id,),
            ).fetchall()
        route = [[row["latitude"], row["longitude"]] for row in points]
        samples: list[tuple[float, float, float]] = []
        point_payload: list[dict[str, Any]] = []
        for row in points:
            value = finite_number(row[metric])
            if value is None:
                continue
            lat = finite_number(row["latitude"])
            lon = finite_number(row["longitude"])
            if lat is None or lon is None:
                continue
            samples.append((lat, lon, value))
            point_payload.append(
                {
                    "lat": lat,
                    "lon": lon,
                    "value": value,
                    "quality": row["quality"],
                }
            )
        if not samples:
            return {
                "run_id": run_id,
                "metric": metric,
                "unit": MAP_UNITS[metric],
                "enough": False,
                "points": [],
                "route": route,
            }
        lat0 = sum(item[0] for item in samples) / len(samples)
        lon0 = sum(item[1] for item in samples) / len(samples)
        cos_lat0 = math.cos(math.radians(lat0))
        xy: list[tuple[float, float, float]] = []
        for lat, lon, value in samples:
            x = math.radians(lon - lon0) * cos_lat0 * 6371000.0
            y = math.radians(lat - lat0) * 6371000.0
            xy.append((x, y, value))
        min_x = min(item[0] for item in xy)
        max_x = max(item[0] for item in xy)
        min_y = min(item[1] for item in xy)
        max_y = max(item[1] for item in xy)
        if max_x - min_x < 1.0:
            max_x = min_x + 1.0
        if max_y - min_y < 1.0:
            max_y = min_y + 1.0
        max_distance = 80.0
        values: list[list[float | None]] = []
        for row_index in range(rows):
            line: list[float | None] = []
            y = min_y + (max_y - min_y) * row_index / max(1, rows - 1)
            for col_index in range(cols):
                x = min_x + (max_x - min_x) * col_index / max(1, cols - 1)
                numerator = 0.0
                denominator = 0.0
                nearest = float("inf")
                for px, py, value in xy:
                    distance_sq = (x - px) ** 2 + (y - py) ** 2
                    nearest = min(nearest, distance_sq)
                    weight = 1.0 / (distance_sq + 1e-6)
                    numerator += weight * value
                    denominator += weight
                if denominator == 0.0 or nearest > max_distance ** 2:
                    line.append(None)
                else:
                    line.append(round(numerator / denominator, 3))
            values.append(line)
        return {
            "run_id": run_id,
            "metric": metric,
            "unit": MAP_UNITS[metric],
            "enough": len(samples) >= 3,
            "points": point_payload,
            "route": route,
            "values": values,
            "cols": cols,
            "rows": rows,
            "min": round(min(item[2] for item in samples), 3),
            "max": round(max(item[2] for item in samples), 3),
            "avg": round(sum(item[2] for item in samples) / len(samples), 3),
            "bounds": {
                "min_lat": min(item[0] for item in samples),
                "max_lat": max(item[0] for item in samples),
                "min_lon": min(item[1] for item in samples),
                "max_lon": max(item[1] for item in samples),
            },
        }


class MqttBridge:
    def __init__(self, store: Store, host: str, port: int, username: str | None, password: str | None) -> None:
        self.store = store
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client: Any = None
        self.available = False
        try:
            import paho.mqtt.client as mqtt  # type: ignore

            self.mqtt = mqtt
            self.available = True
        except ImportError:
            LOG.warning("paho-mqtt not installed; MQTT bridge is disabled")
            self.mqtt = None

    def start(self) -> None:
        if not self.available:
            return
        try:
            # Unique per process: two gateway windows must not kick each other off.
            client_id = f"freshchain-gateway-{os.getpid()}"
            try:
                client = self.mqtt.Client(self.mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
            except AttributeError:
                client = self.mqtt.Client(client_id=client_id)
            if self.username:
                client.username_pw_set(self.username, self.password or "")
            client.on_connect = self._on_connect
            client.on_disconnect = self._on_disconnect
            client.on_message = self._on_message
            self.client = client
            client.connect_async(self.host, self.port, keepalive=30)
            client.loop_start()
        except Exception as exc:  # pragma: no cover - depends on broker state
            LOG.warning("MQTT connection failed: %s", exc)

    def _on_connect(self, client: Any, userdata: Any, flags: Any, reason_code: Any, properties: Any = None) -> None:
        reason = getattr(reason_code, "value", reason_code)
        connected = reason == 0
        self.store.state.broker_connected = connected
        if connected:
            client.subscribe([(IA1_TOPIC, 0), (ST1_TOPIC, 0), (EVENT_TOPIC, 0)])
            LOG.info("Connected to MQTT broker %s:%s", self.host, self.port)

    def _on_disconnect(self, client: Any, userdata: Any, flags: Any = None, reason_code: Any = None, properties: Any = None) -> None:
        self.store.state.broker_connected = False

    def _on_message(self, client: Any, userdata: Any, msg: Any) -> None:
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            if msg.topic == IA1_TOPIC:
                self.store.record_telemetry("ia1", payload)
            elif msg.topic == ST1_TOPIC:
                self.store.record_telemetry("st1", payload)
            elif msg.topic == EVENT_TOPIC and isinstance(payload, dict):
                self.store.add_event(payload.get("node"), payload.get("level", "info"), payload.get("message", "璁惧浜嬩欢"), payload)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            LOG.warning("Ignoring invalid MQTT message on %s: %s", msg.topic, exc)

    def publish_command(self, node: str, payload: dict[str, Any]) -> bool:
        if not self.client or not self.store.state.broker_connected:
            return False
        topic = IA1_COMMAND_TOPIC if node == "ia1" else ST1_COMMAND_TOPIC
        # Compact JSON is required by the firmware's exact string matcher.
        info = self.client.publish(topic, json.dumps(payload, ensure_ascii=False, separators=(",", ":")), qos=0, retain=False)
        return getattr(info, "rc", 1) == 0


@dataclass
class DemoModel:
    store: Store
    interval: float = 2.0
    running: bool = True
    transport_started: bool = False
    muted: bool = False
    fan_manual: int | None = None
    light_manual: int | None = None
    track_index: int = 0
    geofence_center: tuple[float, float] = (31.2304, 121.4737)
    geofence_radius_m: float = 80.0
    ia1_mode: str = "auto"

    def start(self) -> None:
        thread = threading.Thread(target=self._loop, name="freshchain-demo", daemon=True)
        thread.start()

    def command(self, node: str, payload: dict[str, Any]) -> None:
        action = payload.get("action")
        if node == "ia1":
            if action == "set_mode":
                self.ia1_mode = payload.get("mode", "auto")
                if self.ia1_mode == "auto":
                    self.fan_manual = None
                    self.light_manual = None
            elif action == "fan":
                self.ia1_mode = "manual"
                self.fan_manual = 1 if payload.get("value") else 0
            elif action == "light":
                self.ia1_mode = "manual"
                self.light_manual = 1 if payload.get("value") else 0
        elif node == "st1":
            if action == "start_transport":
                self.transport_started = True
                self.track_index = 0
                self.muted = False
                self.store.add_event("st1", "info", "杩愯緭浠诲姟宸插紑濮?)
            elif action == "end_transport":
                self.transport_started = False
                self.store.add_event("st1", "info", "杩愯緭浠诲姟宸茬粨鏉?)
            elif action == "set_geofence":
                lat = finite_number(payload.get("latitude"))
                lon = finite_number(payload.get("longitude"))
                radius = finite_number(payload.get("radius_m"))
                if lat is not None and lon is not None:
                    self.geofence_center = (lat, lon)
                if radius is not None and radius > 1:
                    self.geofence_radius_m = radius
                self.store.add_event("st1", "info", "鐢靛瓙鍥存爮宸叉洿鏂?, {"center": self.geofence_center, "radius_m": self.geofence_radius_m})
            elif action == "silence":
                self.muted = True
                self.store.add_event("st1", "info", "鎶ヨ宸叉秷闊?)

    def _loop(self) -> None:
        tick = 0
        while self.running:
            tick += 1
            # IA1: values deliberately approach thresholds so the demo visibly changes.
            temperature = 26.0 + 5.5 * math.sin(tick / 6.0)
            humidity = 62.0 + 16.0 * math.sin(tick / 8.0 + 0.7)
            lux = 28.0 + 35.0 * math.sin(tick / 5.0 + 1.4)
            if self.ia1_mode == "auto":
                fan = int(temperature > 30.0 or humidity > 75.0)
                light = int(lux < 20.0)
            else:
                fan = int(self.fan_manual or 0)
                light = int(self.light_manual or 0)
            env_status = "abnormal" if fan or light else "normal"
            self.store.record_telemetry(
                "ia1",
                {
                    "temperature": round(temperature, 2),
                    "humidity": round(humidity, 2),
                    "lux": round(max(lux, 0), 2),
                    "fan": fan,
                    "light": light,
                    "mode": self.ia1_mode,
                    "environment_status": env_status,
                },
            )

            # ST1: remain in the geofence initially, then leave it after start_transport.
            if self.transport_started:
                self.track_index += 1
            step = min(self.track_index, 12)
            lat = self.geofence_center[0] + step * 0.00008
            lon = self.geofence_center[1] + step * 0.00005
            distance = _distance_m(self.geofence_center[0], self.geofence_center[1], lat, lon)
            alarm = int(self.transport_started and distance > self.geofence_radius_m)
            if alarm:
                zone_status = "out_of_zone"
            elif self.transport_started:
                zone_status = "in_transit"
            else:
                zone_status = "in_zone"
            self.store.record_telemetry(
                "st1",
                {
                    "gps_valid": 1,
                    "latitude": round(lat, 6),
                    "longitude": round(lon, 6),
                    "speed": 1.2 if self.transport_started else 0.0,
                    "zone_status": zone_status,
                    "alarm": alarm,
                    "buzzer": int(alarm and not self.muted),
                    "transport_status": "in_transit" if self.transport_started else "ready",
                },
            )
            time.sleep(self.interval)


def _distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    earth = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return earth * 2 * math.atan2(math.sqrt(a), math.sqrt(max(0.0, 1 - a)))


class App:
    def __init__(self, args: argparse.Namespace) -> None:
        self.store = Store(Path(args.db).resolve(), reset=args.reset_db)
        self.store.state.demo = args.demo
        self.mqtt = MqttBridge(self.store, args.mqtt_host, args.mqtt_port, args.mqtt_username, args.mqtt_password)
        self.demo = DemoModel(self.store, interval=args.demo_interval) if args.demo else None
        self.command_handlers: list[Callable[[str, dict[str, Any]], None]] = []
        if self.demo:
            self.command_handlers.append(self.demo.command)
        self.forecast_service = ForecastService(self.store)
        self.alert_service = AlertService(
            self.store,
            self.command,
            auto_control=bool(args.ai_auto_control),
        )

    def start(self) -> None:
        if not self.demo:
            self.mqtt.start()
        if self.demo:
            self.demo.start()

    def command(self, node: str, payload: dict[str, Any]) -> dict[str, Any]:
        if node not in {"ia1", "st1"}:
            raise ValueError("node must be ia1 or st1")
        self.store.record_command(node, payload)
        published = self.mqtt.publish_command(node, payload)
        for handler in self.command_handlers:
            handler(node, payload)
        return {"ok": True, "published": published, "demo_applied": bool(self.demo)}

    def start_run(self, label: str | None, route_name: str | None, start_transport: bool = True) -> dict[str, Any]:
        run = self.store.start_run(label, route_name)
        transport = None
        if start_transport:
            transport = self.command("st1", {"action": "start_transport"})
        return {"ok": True, "run": run, "transport": transport}

    def stop_run(self, run_id: int, status: str = "completed", end_transport: bool = True) -> dict[str, Any]:
        run = self.store.stop_run(run_id, status)
        transport = None
        if end_transport:
            transport = self.command("st1", {"action": "end_transport"})
        return {"ok": True, "run": run, "transport": transport}

    def map_for_run(self, run_id: int | None, metric: str, cols: int, rows: int) -> dict[str, Any]:
        if run_id is None:
            runs = self.store.list_runs(1)
            if not runs:
                raise ValueError("杩樻病鏈夎矾绾挎暟鎹?)
            run_id = int(runs[0]["id"])
        return self.store.build_map(run_id, metric, cols, rows)

    def ai_snapshot(self, run_id: int | None = None, horizon_min: int = 10,
                    scope: str = "region") -> dict[str, Any]:
        forecast = self.forecast_service.forecast(run_id=run_id, horizon_min=horizon_min, scope=scope)
        created = self.alert_service.evaluate(forecast)
        return {
            "ok": True,
            "forecast": forecast,
            "new_alerts": created,
            "alerts": self.store.list_alerts(20, run_id=run_id),
            "thresholds": self.alert_service.thresholds.__dict__,
            "auto_control": self.alert_service.auto_control,
        }


def read_body(handler: BaseHTTPRequestHandler) -> dict[str, Any]:
    try:
        length = int(handler.headers.get("Content-Length", "0"))
        raw = handler.rfile.read(length).decode("utf-8") if length else "{}"
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError("JSON body must be an object")
        return data
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid JSON body: {exc}") from exc


def make_handler(app: App) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        server_version = "FreshChain/1.0"

        def log_message(self, format: str, *args: Any) -> None:
            LOG.info("%s - %s", self.address_string(), format % args)

        def _send_json(self, payload: Any, status: int = HTTPStatus.OK) -> None:
            raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def _send_file(self, path: Path, content_type: str) -> None:
            if not path.is_file():
                self._send_json({"error": "not found"}, HTTPStatus.NOT_FOUND)
                return
            raw = path.read_bytes()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            if parsed.path in {"/", "/index.html"}:
                self._send_file(STATIC / "index.html", "text/html; charset=utf-8")
            elif parsed.path == "/app.js":
                self._send_file(STATIC / "app.js", "text/javascript; charset=utf-8")
            elif parsed.path == "/style.css":
                self._send_file(STATIC / "style.css", "text/css; charset=utf-8")
            elif parsed.path == "/api/state":
                self._send_json(app.store.snapshot())
            elif parsed.path == "/api/history":
                query = parse_qs(parsed.query)
                node = query.get("node", ["ia1"])[0]
                try:
                    limit = int(query.get("limit", ["100"])[0])
                except ValueError:
                    limit = 100
                self._send_json({"node": node, "items": app.store.history(node, limit)})
            elif parsed.path == "/api/runs":
                query = parse_qs(parsed.query)
                try:
                    limit = int(query.get("limit", ["20"])[0])
                except ValueError:
                    limit = 20
                self._send_json({"items": app.store.list_runs(limit)})
            elif parsed.path.startswith("/api/runs/"):
                try:
                    run_id = int(parsed.path.rsplit("/", 1)[-1])
                    run = app.store.get_run(run_id)
                except (ValueError, TypeError):
                    run = None
                if run is None:
                    self._send_json({"error": "璺嚎涓嶅瓨鍦?}, HTTPStatus.NOT_FOUND)
                else:
                    self._send_json({"run": run})
            elif parsed.path == "/api/map":
                query = parse_qs(parsed.query)
                metric = query.get("metric", ["temperature"])[0]
                try:
                    run_id = int(query["run_id"][0]) if "run_id" in query else None
                    cols = int(query.get("cols", ["60"])[0])
                    rows = int(query.get("rows", ["60"])[0])
                except (ValueError, TypeError):
                    self._send_json({"error": "run_id/cols/rows 鍙傛暟涓嶅悎娉?}, HTTPStatus.BAD_REQUEST)
                    return
                self._send_json(app.map_for_run(run_id, metric, cols, rows))
            elif parsed.path in {"/api/ai", "/api/forecast"}:
                query = parse_qs(parsed.query)
                try:
                    run_id = int(query["run_id"][0]) if "run_id" in query else None
                    horizon = int(query.get("horizon", ["10"])[0])
                except (ValueError, TypeError):
                    self._send_json({"error": "run_id/horizon 鍙傛暟涓嶅悎娉?}, HTTPStatus.BAD_REQUEST)
                    return
                scope = "single" if query.get("scope", ["region"])[0] == "single" else "region"
                self._send_json(app.ai_snapshot(run_id, horizon, scope=scope))
            elif parsed.path == "/api/series":
                query = parse_qs(parsed.query)
                try:
                    minutes = int(query.get("minutes", ["30"])[0])
                    limit = int(query.get("limit", ["1200"])[0])
                except (ValueError, TypeError):
                    self._send_json({"error": "minutes/limit 鍙傛暟涓嶅悎娉?}, HTTPStatus.BAD_REQUEST)
                    return
                node = query.get("node", ["ia1"])[0]
                self._send_json(app.store.telemetry_series(node, minutes, limit))
            elif parsed.path == "/api/alerts":
                query = parse_qs(parsed.query)
                try:
                    run_id = int(query["run_id"][0]) if "run_id" in query else None
                    limit = int(query.get("limit", ["30"])[0])
                except (ValueError, TypeError):
                    self._send_json({"error": "run_id/limit 鍙傛暟涓嶅悎娉?}, HTTPStatus.BAD_REQUEST)
                    return
                self._send_json({"items": app.store.list_alerts(limit, run_id=run_id)})
            else:
                self._send_json({"error": "not found"}, HTTPStatus.NOT_FOUND)

        def do_POST(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            try:
                body = read_body(self)
                if parsed.path == "/api/command":
                    result = app.command(str(body.get("node", "")), body.get("payload", {}))
                    self._send_json(result)
                elif parsed.path == "/api/run/start":
                    result = app.start_run(
                        body.get("label"),
                        body.get("route_name"),
                        bool(body.get("start_transport", True)),
                    )
                    self._send_json(result)
                elif parsed.path == "/api/run/stop":
                    run_id = body.get("run_id")
                    if run_id is None:
                        current = app.store.current_run()
                        if current is None:
                            raise ValueError("褰撳墠娌℃湁姝ｅ湪閲囬泦鐨勮矾绾?)
                        run_id = current["id"]
                    result = app.stop_run(
                        int(run_id),
                        str(body.get("status", "completed")),
                        bool(body.get("end_transport", True)),
                    )
                    self._send_json(result)
                elif parsed.path.startswith("/api/alerts/") and parsed.path.endswith("/ack"):
                    parts = parsed.path.strip("/").split("/")
                    if len(parts) != 4:
                        raise ValueError("棰勮 ID 涓嶅悎娉?)
                    alert = app.store.acknowledge_alert(int(parts[2]))
                    if alert is None:
                        self._send_json({"error": "棰勮涓嶅瓨鍦?}, HTTPStatus.NOT_FOUND)
                    else:
                        self._send_json({"ok": True, "alert": alert})
                elif parsed.path == "/api/ai/analyze":
                    result = app.ai_snapshot(
                        int(body["run_id"]) if body.get("run_id") is not None else None,
                        int(body.get("horizon", 10)),
                    )
                    self._send_json(result)
                elif parsed.path == "/api/event":
                    app.store.add_event(body.get("node"), body.get("level", "info"), body.get("message", "浜嬩欢"), body)
                    self._send_json({"ok": True})
                else:
                    self._send_json({"error": "not found"}, HTTPStatus.NOT_FOUND)
            except ValueError as exc:
                self._send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            except Exception as exc:  # pragma: no cover - defensive HTTP boundary
                LOG.exception("request failed")
                self._send_json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)

    return Handler


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="FreshChain local gateway")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--db", default=str(DEFAULT_DB))
    parser.add_argument("--reset-db", action="store_true")
    parser.add_argument("--demo", action="store_true", help="run built-in IA1/ST1 simulator")
    parser.add_argument("--demo-interval", type=float, default=2.0)
    parser.add_argument("--mqtt-host", default="127.0.0.1")
    parser.add_argument("--mqtt-port", type=int, default=1884)
    parser.add_argument("--mqtt-username")
    parser.add_argument("--mqtt-password")
    parser.add_argument("--ai-auto-control", action="store_true",
                        help="allow warning/critical AI alerts to publish fan/light commands")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    args = parse_args()
    app = App(args)
    app.start()
    server = ThreadingHTTPServer((args.host, args.port), make_handler(app))
    LOG.info("FreshChain gateway listening at http://%s:%s", args.host, args.port)
    LOG.info("mode=%s db=%s", "demo" if args.demo else "mqtt", app.store.db_path)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        LOG.info("stopping")
    finally:
        server.server_close()
        app.store.close()


if __name__ == "__main__":
    main()


