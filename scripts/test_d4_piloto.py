"""Testes do filtro e do dimensionamento do piloto D4.3."""

import math
import tempfile
import unittest
from pathlib import Path

from d4_experimento import cells
from d4_piloto import T_975_DF29, paired_differences, summarize, write_csv, write_report


def row(seed, policy, config, departures, counter, security):
    return {
        "seed": str(seed), "family": "referencia", "policy": policy, "config": config,
        "departures_per_h": str(departures), "counter_mean_wait_s": str(counter),
        "security_mean_wait_s": str(security),
    }


class TestPilot(unittest.TestCase):
    def fixture(self):
        rows = []
        for seed, offset in ((1, 0), (2, 1), (3, 2)):
            rows.extend([
                row(seed, "fcfs", "Base", 5 + offset, 100 + offset, 40 + offset),
                row(seed, "agenda", "Base", 6 + 2 * offset, 90 + offset, 30 + offset),
                row(seed, "fcfs", "S4", 4 + offset, 100 + offset, 40 + offset),
                row(seed, "agenda", "S4", 5 + offset, 90 + offset, 30 + offset),
                row(seed, "fcfs", "B2", 5 + offset, 20 + offset, 50 + offset),
                row(seed, "agenda", "B2", 6 + offset, 10 + offset, 40 + offset),
                row(seed, "fcfs", "I2", 5 + offset, 100 + offset, 5 + offset),
                row(seed, "agenda", "I2", 6 + offset, 90 + offset, 4 + offset),
            ])
        return rows

    def test_reference_filter_has_eight_cells(self):
        self.assertEqual(len(list(cells(["referencia"]))), 8)
        self.assertEqual(len(list(cells())), 48)
        with self.assertRaises(ValueError):
            list(cells(["inexistente"]))

    def test_differences_follow_declared_direction(self):
        differences, n = paired_differences(self.fixture())
        self.assertEqual(n, 3)
        self.assertEqual(differences["stands_fcfs"], [1.0, 1.0, 1.0])
        self.assertEqual(differences["balcao_agenda"], [-80.0, -80.0, -80.0])
        self.assertEqual(differences["inspecao_fcfs"], [-35.0, -35.0, -35.0])

    def test_sample_dispersion_and_required_n(self):
        summaries = {item["contrast"]: item for item in summarize(self.fixture())}
        policy = summaries["politica_base"]
        self.assertEqual(policy["mean_difference"], 2.0)
        self.assertEqual(policy["sd_difference"], 1.0)
        self.assertAlmostEqual(policy["pilot_halfwidth_95"], T_975_DF29 / math.sqrt(3))
        self.assertEqual(policy["required_replications"],
                         math.ceil((T_975_DF29 / 0.25) ** 2))

    def test_outputs_are_reproducible(self):
        summaries = summarize(self.fixture())
        with tempfile.TemporaryDirectory() as folder:
            csv_path = Path(folder) / "summary.csv"
            report_path = Path(folder) / "report.md"
            write_csv(summaries, csv_path)
            write_report(summaries, report_path, "pilot.csv")
            self.assertIn("required_replications", csv_path.read_text(encoding="utf-8"))
            self.assertIn("Número fixado para a D4.4", report_path.read_text(encoding="utf-8"))

    def test_report_names_minimum_when_it_governs(self):
        summaries = summarize(self.fixture())
        for item in summaries:
            item["required_replications"] = 2
        with tempfile.TemporaryDirectory() as folder:
            report_path = Path(folder) / "report.md"
            write_report(summaries, report_path, "pilot.csv")
            report = report_path.read_text(encoding="utf-8")
            self.assertIn("mínimo predefinido de 30 réplicas", report)


if __name__ == "__main__":
    unittest.main()
