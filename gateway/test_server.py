import json
import tempfile
import unittest
from pathlib import Path

from ai_service import AlertService, ForecastService
from server import Store, _distance_m, now_ms


class StoreTests(unittest.TestCase):
    def test_telemetry_snapshot_and_track(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Store(Path(directory) / "test.db")
            store.record_telemetry("ia1", {"temperature": 26.5, "environment_status": "normal"})
            store.record_telemetry("st1", {"gps_valid": 1, "latitude": 31.2, "longitude": 121.4, "alarm": 0})
            snapshot = store.snapshot()
            self.assertEqual(snapshot["latest"]["ia1"]["temperature"], 26.5)
            self.assertEqual(len(snapshot["track"]), 1)
            self.assertEqual(store.history("ia1")[0]["temperature"], 26.5)
            store.close()

    def test_invalid_node_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Store(Path(directory) / "test.db")
            with self.assertRaises(ValueError):
                store.record_telemetry("other", {})
            store.close()

    def test_repeated_alarm_state_is_deduplicated(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Store(Path(directory) / "test.db")
            abnormal = {"temperature": 32.0, "environment_status": "abnormal"}
            store.record_telemetry("ia1", abnormal)
            store.record_telemetry("ia1", abnormal)
            self.assertEqual(len(store.snapshot()["events"]), 1)
            store.close()


class RunTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.temp.name) / "runs.db")
        self.store.record_telemetry(
            "st1",
            {"gps_valid": 1, "latitude": 31.2304, "longitude": 121.4737},
        )

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def _add_point(self, lat, lon, temperature):
        self.store.record_telemetry("ia1", {"temperature": temperature, "humidity": 60, "lux": 100})
        self.store.record_telemetry("st1", {"gps_valid": 1, "latitude": lat, "longitude": lon})
        self.store._flush_pending_locked(now_ms(), force=True)

    def test_run_lifecycle_and_map(self):
        run = self.store.start_run("unit", "test route")
        self.assertEqual(run["status"], "active")
        with self.assertRaises(ValueError):
            self.store.start_run("duplicate", "test route")
        self._add_point(31.2304, 121.4737, 27.1)
        self._add_point(31.2305, 121.4738, 27.8)
        self._add_point(31.2306, 121.4739, 28.4)
        stopped = self.store.stop_run(run["id"])
        self.assertEqual(stopped["status"], "completed")
        self.assertEqual(stopped["points"], 3)
        self.assertEqual(stopped["valid_points"], 3)
        result = self.store.build_map(run["id"], "temperature")
        self.assertTrue(result["enough"])
        self.assertEqual(len(result["points"]), 3)
        self.assertEqual(result["route"][0], [31.2304, 121.4737])
        self.assertAlmostEqual(result["min"], 27.1, places=3)
        self.assertEqual(self.store.display_run()["id"], run["id"])

    def test_run_requires_gps(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Store(Path(directory) / "nogps.db")
            with self.assertRaises(ValueError):
                store.start_run("no gps", "test")
            store.close()

    def test_missing_environment_is_marked(self):
        run = self.store.start_run("missing", "test route")
        self.store.record_telemetry("st1", {"gps_valid": 1, "latitude": 31.231, "longitude": 121.474})
        self.store._flush_pending_locked(now_ms(), force=True)
        stopped = self.store.stop_run(run["id"])
        self.assertEqual(stopped["points"], 1)
        self.assertEqual(stopped["valid_points"], 0)
        with self.store.lock:
            row = self.store.db.execute(
                "SELECT quality, temperature FROM route_points WHERE run_id=?", (run["id"],)
            ).fetchone()
        self.assertEqual(row["quality"], "missing_env")
        self.assertIsNone(row["temperature"])


class AIServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.temp.name) / "ai.db")
        base = now_ms() - 60_000
        for index, temperature in enumerate([26.0, 26.8, 27.5, 28.4, 29.2, 30.1]):
            self.store.record_telemetry(
                "ia1",
                {
                    "temperature": temperature,
                    "humidity": 60 + index,
                    "lux": 80,
                    "mode": "auto",
                    "fan": 0,
                    "light": 0,
                },
                received_ms=base + index * 10_000,
            )

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def test_forecast_uses_recent_series_and_returns_interval(self):
        forecast = ForecastService(self.store).forecast(horizon_min=10)
        self.assertTrue(forecast["available"])
        self.assertEqual(forecast["source"], "telemetry")
        temperature = forecast["temperature"]
        self.assertTrue(temperature["available"])
        self.assertGreater(temperature["predicted"], temperature["current"])
        self.assertLessEqual(temperature["lower"], temperature["predicted"])
        self.assertGreaterEqual(temperature["upper"], temperature["predicted"])
        self.assertGreater(temperature["confidence"], 0)
        self.assertEqual(len(temperature["path"]), 11)
        self.assertEqual(temperature["path"][0]["value"], temperature["current"])

    def test_single_scope_uses_telemetry_series(self):
        series = self.store.telemetry_series("ia1", minutes=30, limit=1200)
        self.assertEqual(series["source"], "telemetry")
        self.assertGreaterEqual(len(series["points"]), 3)
        forecast = ForecastService(self.store).forecast(horizon_min=10, scope="single")
        self.assertEqual(forecast["scope"], "single")
        self.assertEqual(forecast["source"], "telemetry")
        self.assertTrue(forecast["available"])

    def test_alert_is_persisted_deduplicated_and_acknowledged(self):
        forecast = ForecastService(self.store).forecast(horizon_min=10)
        service = AlertService(self.store)
        created = service.evaluate(forecast)
        self.assertTrue(any(alert["metric"] == "temperature" for alert in created))
        # Same level within the 60 s cooldown must not create a second row.
        again = service.evaluate(forecast)
        self.assertEqual(again, [])
        alerts = self.store.list_alerts(10)
        self.assertEqual(len([a for a in alerts if a["metric"] == "temperature"]), 1)
        acked = self.store.acknowledge_alert(alerts[0]["id"])
        self.assertTrue(acked["acknowledged"])


class GeometryTests(unittest.TestCase):
    def test_distance_is_zero_for_same_point(self):
        self.assertAlmostEqual(_distance_m(31.2, 121.4, 31.2, 121.4), 0.0, places=5)

    def test_distance_is_positive(self):
        self.assertGreater(_distance_m(31.2, 121.4, 31.2001, 121.4001), 10)


if __name__ == "__main__":
    unittest.main()


