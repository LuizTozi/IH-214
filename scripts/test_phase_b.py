import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from phase_b import simulate

SCENARIO = Path(__file__).resolve().parents[1] / "data/scenarios/phase_b_towed_verification.json"


class TestPhaseB(unittest.TestCase):
    def test_same_requests_and_distinct_admission_rules(self):
        scheduled = simulate(SCENARIO, "scheduled")
        fcfs = simulate(SCENARIO, "fcfs")
        self.assertEqual(scheduled["scenario"], fcfs["scenario"])
        self.assertEqual([row["state"] for row in scheduled["requests"]],
                         ["completed", "rejected", "in_system"])
        self.assertEqual([row["state"] for row in fcfs["requests"]],
                         ["completed", "in_system", "waiting"])

    def test_allocations_exclude_overlap(self):
        for policy in ("fcfs", "scheduled"):
            result = simulate(SCENARIO, policy)
            for resource in ("tlof", "stand", "taxiway"):
                periods = [x for x in result["observed_resource_intervals"]
                           if x["resource"] == resource]
                self.assertTrue(periods)
                for left, right in zip(periods, periods[1:]):
                    self.assertLessEqual(left["end_s"], right["start_s"])
            trip = result["requests"][0]
            expected = {
                "planned_taxi_in_s": "37.7", "planned_stand_entry_s": "60.5",
                "planned_taxi_out_s": "100.5", "planned_departure_entry_s": "123.3",
                "planned_tlof_release_s": "136.3",
            }
            for name, value in expected.items():
                self.assertEqual(trip[name], Decimal(value))

    def test_stand_blocks_until_departure_destination_is_free(self):
        data = json.loads(SCENARIO.read_text())
        data["separation_s"] = 90
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scenario.json"
            path.write_text(json.dumps(data))
            result = simulate(path, "fcfs")
        trip = result["requests"][0]
        self.assertEqual(trip["planned_stand_blocked_s"], Decimal("27.2"))
        self.assertEqual(trip["planned_taxi_out_s"], Decimal("127.7"))

    def test_rounded_scenario_values_follow_approved_components(self):
        data = json.loads(SCENARIO.read_text(), parse_float=Decimal)
        speed = Decimal("2.63")
        self.assertEqual(data["taxi_s"], (60 / speed).quantize(Decimal("0.1")))
        self.assertTrue(all(row["occupancy_s"] ==
                            (32 + 15 / speed).quantize(Decimal("0.1"))
                            for row in data["requests"]))
