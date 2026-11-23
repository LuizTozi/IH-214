import unittest
from decimal import Decimal

from d4_dia import family_requests, generate_day
from d4_terminal import passengers_from_family, run_terminal

ONE = {"counter": 1, "baggage": 1, "security": 1}


def pax(pid, arrival, bag=45, flight="F1"):
    return {"id": pid, "flight": flight, "arrival_s": Decimal(arrival), "bag_s": Decimal(bag)}


def visits_of(result, pid):
    return {v["station"]: v for v in result["visits"] if v["id"] == pid}


class TestTerminal(unittest.TestCase):
    def test_single_passenger_path(self):
        r = run_terminal([pax("A", 0)], ONE)
        v = visits_of(r, "A")
        self.assertEqual([v[s]["start_s"] for s in ("counter", "baggage", "security")], [0, 180, 225])
        self.assertEqual(r["passengers"]["A"]["ready_s"], 315)
        self.assertEqual(r["passengers"]["A"]["state"], "in_lounge")

    def test_two_servers_work_in_parallel(self):
        people = [pax(p, 0) for p in "ABC"]
        one = run_terminal(people, ONE)
        two = run_terminal(people, {**ONE, "counter": 2})
        starts = lambda r: [visits_of(r, p)["counter"]["start_s"] for p in "ABC"]
        self.assertEqual(starts(one), [0, 180, 360])
        self.assertEqual(starts(two), [0, 0, 180])
        servers = [visits_of(two, p)["counter"]["server"] for p in "ABC"]
        self.assertEqual(servers, [1, 2, 1])   # menor índice livre

    def test_capacity_never_exceeded_on_generated_day(self):
        day = generate_day(4)
        people = passengers_from_family(family_requests(day, 8, 30))
        for counters in (1, 2):
            r = run_terminal(people, {**ONE, "counter": counters})
            for station, cap in (("counter", counters), ("baggage", 1), ("security", 1)):
                # fim None = atendimento ainda em curso no horizonte (intervalo aberto)
                spans = [(v["start_s"], v["end_s"] if v["end_s"] is not None else Decimal("Infinity"))
                         for v in r["visits"]
                         if v["station"] == station and v["start_s"] is not None]
                for t, _ in spans:
                    busy = sum(a <= t < b for a, b in spans)
                    self.assertLessEqual(busy, cap)
            for v in r["visits"]:
                if v["start_s"] is not None:
                    self.assertGreaterEqual(v["start_s"], v["entry_s"])

    def test_diversion_while_in_queue_leaves_at_once(self):
        people = [pax("A", 0), pax("B", 0, flight="F2"), pax("C", 0, flight="F3")]
        r = run_terminal(people, ONE, cancels=[(100, "F2", "diversion")])
        b = visits_of(r, "B")["counter"]
        self.assertIsNone(b["start_s"])
        self.assertEqual((b["exit_s"], b["exit_reason"]), (100, "diversion"))
        self.assertEqual(set(visits_of(r, "B")), {"counter"})
        self.assertEqual(visits_of(r, "C")["counter"]["start_s"], 180)  # fila anda
        self.assertEqual(r["passengers"]["B"]["state"], "left_diversion")

    def test_refusal_during_service_finishes_then_leaves(self):
        r = run_terminal([pax("A", 0)], ONE, cancels=[(100, "F1", "refusal")])
        v = visits_of(r, "A")
        self.assertEqual(set(v), {"counter"})
        self.assertEqual((v["counter"]["end_s"], v["counter"]["exit_s"]), (180, 180))
        self.assertEqual(v["counter"]["exit_reason"], "refusal")
        self.assertEqual(r["passengers"]["A"]["state"], "left_refusal")

    def test_cancel_before_arrival_means_no_show(self):
        r = run_terminal([pax("A", 500)], ONE, cancels=[(100, "F1", "refusal")])
        self.assertEqual(r["visits"], [])
        self.assertEqual(r["passengers"]["A"]["state"], "not_arrived_refusal")

    def test_cancel_in_lounge_removes_passenger(self):
        r = run_terminal([pax("A", 0)], ONE, cancels=[(400, "F1", "diversion")])
        self.assertEqual(r["passengers"]["A"]["state"], "left_lounge_diversion")
        self.assertEqual(r["passengers"]["A"]["exit_s"], 400)
        self.assertEqual(r["lounge"], [])

    def test_wait_at_limit_is_compliant_and_horizon_censors(self):
        # B espera exatamente 180 s no balcão: conforme (limite inclusivo).
        r = run_terminal([pax("A", 0), pax("B", 0)], ONE)
        self.assertEqual(visits_of(r, "B")["counter"]["wait_s"], 180)
        self.assertEqual(r["summary"]["counter"]["within_limit"], 2)
        # Horizonte em 100 s: B ainda está na fila -> espera censurada.
        cut = run_terminal([pax("A", 0), pax("B", 0)], ONE, horizon_s=100)
        s = cut["summary"]["counter"]
        self.assertEqual((s["complete"], s["censored_at_horizon"]), (1, 1))

    def test_summary_counts_exits(self):
        people = [pax("A", 0), pax("B", 0, flight="F2"), pax("C", 0, flight="F3")]
        r = run_terminal(people, ONE, cancels=[(100, "F2", "diversion"), (50, "F3", "refusal")])
        s = r["summary"]["counter"]
        self.assertEqual((s["left_diversion"], s["left_refusal"]), (1, 1))
        self.assertEqual(s["complete"], 1)

    def test_deterministic(self):
        people = passengers_from_family(family_requests(generate_day(2), 6, 30))
        self.assertEqual(run_terminal(people, ONE), run_terminal(people, ONE))

    def test_absent_reservations_are_excluded(self):
        rows = family_requests(generate_day(6), 8, 0)
        people = passengers_from_family(rows)
        absent = sum(p["arrival_s"] is None for r in rows for p in r["manifest"])
        total = sum(len(r["manifest"]) for r in rows)
        self.assertEqual(len(people), total - absent)


if __name__ == "__main__":
    unittest.main()
