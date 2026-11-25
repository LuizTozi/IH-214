import json
import math
from collections import Counter
from statistics import mean

from d4_param import GROUP_WEIGHTS, SECURITY_TIMES_S, ARRIVAL_PROFILES
from d4_dia import arrival_lead
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from d4_dia import (BASE_RATE, FIRST_REQUEST_S, HORIZON_S, PARAMS, family_requests,
                    generate_day, load_day, save_day)

MS = Decimal("0.001")


def is_ms(value):
    return Decimal(value) == Decimal(value).quantize(MS)


class TestDayGenerator(unittest.TestCase):
    def test_same_seed_same_day_and_different_seed_differs(self):
        self.assertEqual(generate_day(7), generate_day(7))
        self.assertNotEqual(generate_day(7)["requests"], generate_day(8)["requests"])

    def test_bounds_and_resolution(self):
        day = generate_day(11)
        self.assertTrue(day["requests"])
        times = [r["request_s"] for r in day["requests"]]
        self.assertEqual(times, sorted(times))
        for r in day["requests"]:
            self.assertTrue(FIRST_REQUEST_S <= r["request_s"] < HORIZON_S)
            self.assertTrue(is_ms(r["request_s"]))
            self.assertTrue(0 <= r["mark"] < 1)
            self.assertTrue(1 <= len(r["reservations"]) <= 4)
            for p in r["reservations"]:
                self.assertTrue(0 <= p["lead_u"] < 1)
                self.assertTrue(30 <= p["bag_s"] <= 60 and is_ms(p["bag_s"]))
                self.assertTrue(0 <= p["absence_u"] < 1)
        ids = [p["id"] for r in day["requests"] for p in r["reservations"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_thinning_is_nested_and_preserves_attributes(self):
        day = generate_day(3)
        by_rate = {rate: family_requests(day, rate, 30) for rate in (4, 6, 8)}
        ids = {rate: [r["id"] for r in rows] for rate, rows in by_rate.items()}
        self.assertEqual(len(ids[8]), len(day["requests"]))
        self.assertTrue(set(ids[4]) <= set(ids[6]) <= set(ids[8]))
        full = {r["id"]: r for r in by_rate[8]}
        for rate in (4, 6):
            for r in by_rate[rate]:
                self.assertEqual(r, full[r["id"]])

    def test_family_timing_follows_spec(self):
        day = generate_day(5)
        for charge in (0, 30, 60):
            for r in family_requests(day, 6, charge):
                std = r["request_s"] + 900 + 60 * charge
                self.assertEqual(r["target_departure_s"], std)
                self.assertEqual(r["manifest_close_s"], std - 900)
                self.assertEqual(r["declared_charge_min"], charge)
                for p in r["manifest"]:
                    if p["arrival_s"] is None:
                        continue
                    self.assertGreaterEqual(p["arrival_s"], 0)
                    self.assertLessEqual(p["arrival_s"], r["manifest_close_s"])
                    self.assertTrue(30 <= p["bag_service_s"] <= 60)

    def test_arrivals_shift_with_charge_only(self):
        day = generate_day(9)
        base = {r["id"]: r for r in family_requests(day, 6, 30)}
        for r in family_requests(day, 6, 0):
            other = base[r["id"]]
            for a, b in zip(r["manifest"], other["manifest"]):
                if a["arrival_s"] is not None:
                    self.assertEqual(b["arrival_s"] - a["arrival_s"], 1800)
                self.assertEqual(a["bag_service_s"], b["bag_service_s"])

    def test_rates_and_proportions_over_many_days(self):
        days = [generate_day(seed) for seed in range(300)]
        hours = (HORIZON_S - FIRST_REQUEST_S) / 3600
        requests = [r for d in days for r in d["requests"]]
        rate = len(requests) / (len(days) * hours)
        self.assertAlmostEqual(rate, BASE_RATE, delta=0.2)          # ~4 erros-padrão
        kept = sum(r["mark"] < 0.75 for r in requests) / len(requests)
        self.assertAlmostEqual(kept, 0.75, delta=0.02)
        seats = [len(r["reservations"]) for r in requests]
        counts = Counter(seats)
        for k, weight in GROUP_WEIGHTS.items():
            self.assertAlmostEqual(counts[k] / len(seats), weight / sum(GROUP_WEIGHTS.values()), delta=.017)
        sample = [p for d in days for r in family_requests(d, 8, 30, absence=.15) for p in r["manifest"]]
        self.assertAlmostEqual(mean(p["arrival_s"] is None for p in sample), .15, delta=.01)
        self.assertAlmostEqual(mean(float(p["counter_service_s"]) for p in sample), 164, delta=4)
        self.assertEqual(len(SECURITY_TIMES_S), 2389)
        self.assertTrue({p["security_service_s"] for p in sample} <= set(SECURITY_TIMES_S))
        self.assertAlmostEqual(mean(p["security_service_s"] for p in sample), mean(SECURITY_TIMES_S), delta=2)

    def test_compressed_conditional_weibull(self):
        for profile, (scale, shape, xmax) in ARRIVAL_PROFILES.items():
            cdf = lambda x: 1 - math.exp(-(x / scale) ** shape)
            for u in (0, .1, .5, .9, .999999):
                lead = float(arrival_lead(u, profile))
                self.assertTrue(900 <= lead <= 3600)
                x = 1 + (lead - 900) * (xmax - 1) / 2700
                self.assertAlmostEqual((cdf(x) - cdf(1)) / (cdf(xmax) - cdf(1)), u, delta=.00001)

    def test_sensitivity_reuses_reservations_and_durations(self):
        day = generate_day(20001)
        base = family_requests(day, 6, 30)
        varied = family_requests(day, 6, 30, absence=.15, arrival="lcc_afternoon", std_offset_s=600)
        for r, s in zip(base, varied, strict=True):
            self.assertEqual(r["target_departure_s"] - s["target_departure_s"], 300)
            for p, q in zip(r["manifest"], s["manifest"], strict=True):
                self.assertIsNotNone(p["arrival_s"])
                for key in ("id", "bag_service_s", "counter_service_s", "security_service_s"):
                    self.assertEqual(p[key], q[key])
    def test_archive_roundtrip(self):
        day = generate_day(21)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "dia.json"
            save_day(day, path)
            self.assertEqual(load_day(path), day)
            self.assertEqual(json.loads(path.read_text())["seed"], 21)

    def test_params_cite_registry(self):
        for key in ("arrival_lead_s", "absence_probability", "reserved_seats", "manifest_close_s",
                    "std_offset_s", "bag_service_s", "base_rate_per_h", "first_request_s",
                    "horizon_s"):
            self.assertIn("PAR-", PARAMS[key]["source"])


if __name__ == "__main__":
    unittest.main()
