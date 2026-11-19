import unittest
from decimal import Decimal
from pathlib import Path

from phase_c import simulate

SCENARIO = Path(__file__).resolve().parents[1] / "data/scenarios/phase_c_stand_verification.json"


class TestPhaseC(unittest.TestCase):
    def test_same_declarations_distinct_admission(self):
        scheduled = simulate(SCENARIO, "scheduled")
        fcfs = simulate(SCENARIO, "fcfs")
        self.assertEqual(scheduled["scenario"], fcfs["scenario"])
        self.assertEqual([r["state"] for r in scheduled["requests"]],
                         ["completed", "rejected", "in_system"])
        self.assertEqual([r["state"] for r in fcfs["requests"]],
                         ["completed", "completed", "in_system"])
        self.assertEqual(fcfs["requests"][0]["planned_tlof_release_s"], Decimal("2175.5"))

    def test_charging_nested_between_passenger_movements(self):
        result = simulate(SCENARIO, "fcfs")
        intervals = result["observed_resource_intervals"]
        for row, minutes in zip(result["requests"], (30, 0, 60)):
            stages = {s["operation"]: s for s in row["planned_stand_stages"]}
            observed = [i for i in intervals if i["id"] == row["id"] and i["resource"] == "charger"]
            end_exit = stages["exit_gate"]["end_s"]
            start_entry = stages["enter_gate"]["start_s"]
            self.assertEqual(start_entry - end_exit, minutes * 60)
            if minutes:
                self.assertEqual((stages["charge"]["start_s"], stages["charge"]["end_s"]),
                                 (end_exit, start_entry))
                self.assertEqual(len(observed), 1)
                self.assertEqual(observed[0]["start_s"], end_exit)
                self.assertEqual(observed[0]["end_s"], min(start_entry, 6000))
                stand = next(i for i in intervals if i["id"] == row["id"]
                             and i["resource"] == "stand" and i["state"] == "occupied")
                self.assertLessEqual(stand["start_s"], end_exit)
                self.assertGreaterEqual(stand["end_s"], observed[0]["end_s"])
            else:
                self.assertNotIn("charge", stages)
                self.assertFalse(observed)
