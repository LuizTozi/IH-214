"""Testes da análise pareada da D4.5."""

import tempfile
import unittest
from pathlib import Path

from d4_analise import (cell_summaries, ci, contrast, contrast_summaries, index_rows,
                        numeric, write_report)


def row(seed, family, config, policy, departed, offered=10, counter=20, security=5):
    values = {
        "seed": str(seed), "family": family, "config": config, "policy": policy,
        "departed": str(departed), "departed_empty": "0", "offered": str(offered),
        "punctual": str(departed), "retained_flights": "0", "counter_complete": "10",
        "security_complete": "10", "counter_within_limit": "8",
        "security_within_limit": "9", "departures_per_h": str(departed / 8),
        "counter_mean_wait_s": str(counter), "security_mean_wait_s": str(security),
    }
    for key in ("cancelled_empty", "refused", "diverted", "pending", "liftoffs_per_h",
                "mean_lateness_s", "mean_await_s", "mean_stand_blocked_s",
                "post_security_mean_s", "post_security_p95_s", "utilization_tlof",
                "arrival_to_board_mean_s", "boarded_counter_wait_mean_s",
                "utilization_route", "utilization_stands", "held_stands",
                "counter_p95_wait_s", "counter_censored_at_horizon", "counter_left_refusal",
                "counter_left_diversion", "baggage_mean_wait_s", "baggage_p95_wait_s",
                "baggage_complete", "security_p95_wait_s", "security_censored_at_horizon",
                "security_left_refusal", "security_left_diversion", "boarded_passengers",
                "lost_passengers"):
        values.setdefault(key, "0")
    return values


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

    def test_primary_only_in_reference_family(self):
        rows = []
        for seed in range(1, 31):
            for family in ("referencia", "demanda_baixa", "demanda_alta", "sem_recarga",
                           "recarga_longa", "servico_variavel"):
                for config in ("Base", "S4", "B2"):
                    for policy in ("fcfs", "agenda"):
                        rows.append(row(seed, family, config, policy, 8 + seed % 3))
            for family in ("info_perfeita", "info_perfeita_sem_recarga"):
                for config in ("Base", "S4", "B2"):
                    rows.append(row(seed, family, config, "agenda", 8 + seed % 2))
        contrasts = contrast_summaries(rows, "test")
        primary = {(c["family"], c["contrast"]) for c in contrasts
                   if c["classification"] == "primary"}
        self.assertEqual({family for family, _ in primary}, {"referencia"})
        self.assertEqual({name for _, name in primary},
                         {"policy_Base", "stands_fcfs", "stands_agenda",
                          "counter_fcfs", "counter_agenda"})
        cells = cell_summaries(rows, "test")
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "report.md"
            write_report(cells, contrasts, path, "results.csv")
            report = path.read_text(encoding="utf-8")
            self.assertIn("Agenda − FCFS", report)
            self.assertIn("Denominadores", report)
            self.assertNotIn("I2", report)

    def test_departures_exclude_empty_flights_in_coverage(self):
        item = row(1, "referencia", "Base", "fcfs", 8)
        item["departed_empty"] = "2"
        self.assertEqual(numeric(item, "coverage_offered"), 0.6)
        self.assertEqual(numeric(item, "retained_fraction"), 0.0)


if __name__ == "__main__":
    unittest.main()
