"""Integração da D4.2 (etapa 5): uma réplica completa pelas 42 células (D4.1 v2.3)."""

import csv
import tempfile
import unittest
from pathlib import Path

from d4_experimento import CONFIGS, FAMILIES, cells, run


class TestExperimentRunner(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = tempfile.TemporaryDirectory()
        out = Path(cls.folder.name) / "res.csv"
        cls.rows = run([3], out, days_dir=Path(cls.folder.name) / "dias")
        with out.open(encoding="utf-8") as handle:
            cls.csv_rows = list(csv.DictReader(handle))
        cls.day_file = Path(cls.folder.name) / "dias" / "dia_0003.json"

    @classmethod
    def tearDownClass(cls):
        cls.folder.cleanup()

    def test_42_distinct_cells_per_replication(self):
        self.assertEqual(len(list(cells())), 42)
        keys = {(r["family"], r["config"], r["policy"]) for r in self.rows}
        self.assertEqual(len(keys), 42)
        self.assertEqual(len(self.csv_rows), 42)
        self.assertTrue(self.day_file.exists())

    def test_pairing_uses_one_day(self):
        self.assertEqual(len({r["day_id"] for r in self.rows}), 1)
        self.assertEqual(len({r["code_version"] for r in self.rows}), 1)
        for family, (rate, _, _, _) in FAMILIES.items():
            offered = {r["offered"] for r in self.rows if r["family"] == family}
            self.assertEqual(len(offered), 1, family)    # mesma demanda em todas as células

    def test_policy_specific_outcomes_and_balance(self):
        for r in self.rows:
            self.assertEqual(r["offered"], r["cancelled_empty"] + r["refused"] + r["diverted"]
                             + r["departed"] + r["pending"])
            if r["policy"] == "fcfs":
                self.assertEqual(r["refused"], 0)
                self.assertFalse(r["perfect"])
            else:
                self.assertEqual(r["diverted"], 0)
            self.assertTrue(0 <= r["utilization_stands"] <= 1)
            self.assertTrue(0 <= r["utilization_tlof"] <= 1)

    def test_terminal_unchanged_by_stands_when_no_exits(self):
        # Base e S4 só diferem no terminal por recusas ou desvios (resultado esperado).
        for family in FAMILIES:
            for policy in ("fcfs", "agenda"):
                cell = {r["config"]: r for r in self.rows
                        if r["family"] == family and r["policy"] == policy}
                if not cell:
                    continue
                base, s4 = cell["Base"], cell["S4"]
                if base["refused"] + base["diverted"] + s4["refused"] + s4["diverted"] == 0:
                    for key in base:
                        if key.startswith(("counter_", "baggage_", "security_")):
                            self.assertEqual(base[key], s4[key], (family, policy, key))

    def test_configs_cover_the_three_contrasts(self):
        # I2 saiu na D4.1 v2.2: reproduzia a Base por construção (serviços determinísticos).
        self.assertEqual(set(CONFIGS), {"Base", "S4", "B2"})


if __name__ == "__main__":
    unittest.main()
