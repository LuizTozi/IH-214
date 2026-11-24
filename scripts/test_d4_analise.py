"""Testes da análise pareada da D4.5."""

import tempfile
import unittest
from pathlib import Path

from d4_analise import ci, contrast, index_rows, numeric, write_report


def row(seed, family, config, policy, departed, offered=10, counter=20, security=5):
    return {
        "seed": str(seed), "family": family, "config": config, "policy": policy,
        "departed": str(departed), "departed_empty": "0", "offered": str(offered),
        "punctual": str(departed), "retained_flights": "0", "counter_complete": "10",
        "security_complete": "10", "counter_within_limit": "8",
        "security_within_limit": "9", "departures_per_h": str(departed / 8),
        "counter_mean_wait_s": str(counter), "security_mean_wait_s": str(security),
    }


class TestAnalysis(unittest.TestCase):
    def test_derived_denominators(self):
        item = row(1, "referencia", "Base", "fcfs", 8)
        self.assertEqual(numeric(item, "coverage_offered"), 0.8)
        self.assertEqual(numeric(item, "punctual_fraction"), 1.0)
        self.assertEqual(numeric(item, "counter_within_limit_fraction"), 0.8)

    def test_ci_uses_replications(self):
        stats = ci([float(value) for value in range(1, 31)])
        self.assertEqual(stats["n_valid"], 30)
        self.assertEqual(stats["mean"], 15.5)
        self.assertLess(stats["ci_low"], stats["mean"])
        self.assertGreater(stats["ci_high"], stats["mean"])

    def test_contrast_is_within_seed_and_directional(self):
        rows = []
        for seed in range(1, 31):
            rows.append(row(seed, "referencia", "Base", "agenda", 8 + seed))
            rows.append(row(seed, "referencia", "Base", "fcfs", 7 + seed))
        stats = contrast(index_rows(rows), list(range(1, 31)),
                         "referencia", "Base", "agenda",
                         "referencia", "Base", "fcfs", "departures_per_h")
        self.assertAlmostEqual(stats["mean"], 0.125)
        self.assertAlmostEqual(stats["sd"], 0.0)

    def test_duplicate_cell_is_rejected(self):
        item = row(1, "referencia", "Base", "fcfs", 8)
        with self.assertRaises(ValueError):
            index_rows([item, dict(item)])

    def test_report_keeps_direction_and_denominators_visible(self):
        cells = []
        contrasts = []
        for policy in ("fcfs", "agenda"):
            for metric in ("offered", "refused", "diverted", "departed", "pending",
                           "coverage_offered", "counter_mean_wait_s", "retained_fraction",
                           "mean_await_s", "mean_stand_blocked_s", "utilization_stands"):
                cells.append({"analysis_version": "test", "family": "referencia",
                              "config": "Base", "policy": policy, "metric": metric,
                              "mean": 1.0, "ci_low": 0.5, "ci_high": 1.5})
        families = ("referencia", "demanda_baixa", "demanda_alta", "sem_recarga",
                    "recarga_longa")
        for family in families:
            contrasts.append({"analysis_version": "test", "family": family,
                              "contrast": "policy_Base", "metric": "departures_per_h",
                              "mean": -0.1, "ci_low": -0.2, "ci_high": 0.0})
        for name, metric in (("stands_fcfs", "departures_per_h"),
                             ("stands_agenda", "departures_per_h"),
                             ("counter_fcfs", "counter_mean_wait_s"),
                             ("counter_agenda", "counter_mean_wait_s"),
                             ("security_fcfs", "security_mean_wait_s"),
                             ("security_agenda", "security_mean_wait_s")):
            contrasts.append({"analysis_version": "test", "family": "referencia",
                              "contrast": name, "metric": metric,
                              "mean": 1.0, "ci_low": 0.5, "ci_high": 1.5})
        for family in ("info_perfeita", "info_perfeita_sem_recarga"):
            for config in ("Base", "S4", "B2", "I2"):
                contrasts.append({"analysis_version": "test", "family": family,
                                  "contrast": f"information_{config}",
                                  "metric": "departures_per_h", "mean": 0.1,
                                  "ci_low": 0.0, "ci_high": 0.2})
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "report.md"
            write_report(cells, contrasts, path, "results.csv")
            report = path.read_text(encoding="utf-8")
            self.assertIn("Agenda − FCFS", report)
            self.assertIn("denominadores", report)


if __name__ == "__main__":
    unittest.main()
