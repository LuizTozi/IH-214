import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from phase_a import simulate

SCENARIO = Path(__file__).resolve().parents[1] / "data/scenarios/phase_a_verification.json"


class TestPhaseA(unittest.TestCase):
    def run_case(self, times, *, occupancy=10, separation=0, horizon=40,
                 windows=None, policy="fcfs"):
        data = {
            "scenario_id": "test", "kind": "synthetic_verification",
            "basis": "Deterministic verification fixture",
            "horizon_s": horizon, "separation_s": separation,
            "requests": [
                {"id": str(i), "request_s": time, "occupancy_s": occupancy,
                 "window_s": windows[i] if windows else None}
                for i, time in enumerate(times)
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scenario.json"
            path.write_text(json.dumps(data))
            return simulate(path, policy)

    def test_protocol_traces(self):
        cases = [
            ([], 0, []),
            ([0], 0, [(0, 10, 10)]),
            ([0, 0], 0, [(0, 10, 10), (10, 20, 20)]),
            ([0, 10], 0, [(0, 10, 10), (10, 20, 20)]),
            ([0, 5], 3, [(0, 10, 13), (13, 23, 26)]),
        ]
        for times, separation, expected in cases:
            with self.subTest(times=times, separation=separation):
                result = self.run_case(times, separation=separation)
                rows = result["requests"]
                actual = [(row["planned_touchdown_s"], row["planned_exit_s"],
                           row["planned_release_s"]) for row in rows]
                self.assertEqual(actual, expected)
                self.assertEqual(result["summary"]["states_at_horizon"]["released"], len(times))

    def test_saturation_matches_closed_form(self):
        result = self.run_case([0] * 100, separation=3, horizon=1301)
        releases = [row["planned_release_s"] for row in result["requests"]]
        self.assertEqual(releases, [13 * i for i in range(1, 101)])
        summary = result["summary"]
        self.assertEqual(summary["states_at_horizon"]["released"], 100)
        self.assertEqual(summary["physical_utilization"], Decimal(1000) / 1301)
        self.assertEqual(summary["post_exit_restriction_fraction"], Decimal(300) / 1301)

    def test_horizon_excludes_events_at_close(self):
        result = self.run_case([0, 1], separation=3, horizon=13)
        self.assertEqual([row["state"] for row in result["requests"]],
                         ["separation", "waiting"])
        self.assertEqual(result["summary"]["observed_wait_count"], 1)
        self.assertTrue(all(row["t_s"] < 13 for row in result["events"]))

    def test_tie_order_with_fractional_times(self):
        result = self.run_case([0, 0.3], occupancy=0.1, separation=0.2, horizon=1)
        at_tie = [row["event"] for row in result["events"] if row["t_s"] == Decimal("0.3")]
        self.assertEqual(at_tie, ["release", "request", "touchdown"])

    def test_reservations_fill_free_gap(self):
        result = self.run_case([0, 1], windows=[[20, 20], [1, 10]],
                               separation=3, policy="scheduled")
        self.assertEqual([row["planned_touchdown_s"] for row in result["requests"]], [20, 1])
        self.assertEqual(result["summary"]["states_at_horizon"]["released"], 2)

    def test_same_fixture_compares_policies(self):
        scheduled = simulate(SCENARIO, "scheduled")
        fcfs = simulate(SCENARIO, "fcfs")
        self.assertEqual(scheduled["inputs"], fcfs["inputs"])
        self.assertEqual(scheduled["summary"]["states_at_horizon"]["rejected"], 1)
        self.assertEqual(fcfs["summary"]["states_at_horizon"]["released"], 3)

    def test_invalid_occupancy(self):
        with self.assertRaisesRegex(ValueError, "occupancy_s"):
            self.run_case([0], occupancy=0)

    def test_scheduled_requires_window(self):
        with self.assertRaisesRegex(ValueError, "requires window_s"):
            self.run_case([0], policy="scheduled")

    def test_request_must_precede_horizon(self):
        with self.assertRaisesRegex(ValueError, "before the horizon"):
            self.run_case([40])


if __name__ == "__main__":
    unittest.main()
