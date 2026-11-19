import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from phase_d import simulate

TRACE = Path(__file__).resolve().parents[1] / "data/scenarios/phase_d_terminal_verification.json"


class TestPhaseD(unittest.TestCase):
    def test_paired_groups_and_slots(self):
        scheduled = simulate(TRACE, "scheduled")
        fcfs = simulate(TRACE, "fcfs")
        self.assertEqual(scheduled["scenario"], fcfs["scenario"])
        self.assertEqual(scheduled["station_visits"], fcfs["station_visits"])
        self.assertEqual([r["state"] for r in scheduled["requests"]],
                         ["completed", "rejected", "in_system", "cancelled_empty"])
        self.assertEqual((scheduled["departed"], fcfs["departed"]), (1, 2))
        pax = {r["id"]: r for r in fcfs["passengers"]}
        self.assertEqual(pax["P32"]["state"], "late")
        self.assertEqual(pax["P22"]["state"], "absent")
        for person in pax.values():
            if "boarding_start_s" in person:
                self.assertLessEqual(person["planned_terminal_ready_s"], person["boarding_start_s"])
        self.assertIn("await_passenger", [s["operation"] for s in fcfs["requests"][0]["planned_stand_stages"]])

    def test_inclusive_limits_and_exclusivity(self):
        r = simulate(TRACE, "fcfs")
        self.assertEqual(r["station_los"]["counter"]["within"], 2)
        self.assertTrue(any(v["wait_s"] == 180 for v in r["station_visits"]))
        self.assertIsNone(r["station_los"]["baggage"]["ratio"])
        for resource in r["utilization"]:
            periods = [i for i in r["observed_resource_intervals"] if i["resource"] == resource]
            for a, b in zip(periods, periods[1:]):
                self.assertLessEqual(a["end_s"], b["start_s"])

    def test_departure_markers_and_censoring(self):
        data = json.loads(TRACE.read_text())
        data["horizon_s"] = 725
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test.json"
            path.write_text(json.dumps(data))
            r = simulate(path, "fcfs")
            self.assertEqual(r["departed"], 1)
            m = r["simulated_departure_measurements"][0]
            self.assertEqual(m["elapsed_s"], {"taxi": Decimal("22.8"), "occupancy": 50,
                                               "separation": None})
            self.assertEqual(m["event_s"]["liftoff"], Decimal("724.4"))
            self.assertIsNone(m["event_s"]["release"])
            data["horizon_s"] = 201
            path.write_text(json.dumps(data))
            short = simulate(path, "scheduled")
            self.assertEqual(short["station_los"]["counter"]["censored"], 2)
            self.assertEqual(short["boarding_wait_sample"], 0)
