"""Testes do lado ar e do acoplamento com o terminal (D4.2, etapas 3 a 5)."""

import unittest
from decimal import Decimal

from d4_dia import family_requests, generate_day
from d4_sim import run_cell

ONE = {"counter": 1, "baggage": 1, "security": 1}
S = Decimal


def row(fid, t, charge, arrivals, bag=45):
    """Pedido montado à mão; chegadas em segundos absolutos (None = ausente)."""
    std = t + 900 + 60 * charge
    return {"id": fid, "request_s": S(t), "target_departure_s": S(std),
            "manifest_close_s": S(std - 900), "declared_charge_min": charge,
            "manifest": [{"id": f"{fid}-P{i}", "arrival_s": None if a is None else S(a),
                          "bag_service_s": S(bag)} for i, a in enumerate(arrivals, 1)]}


def flight(result, fid):
    return result["flights"][fid]


class TestAirsideFCFS(unittest.TestCase):
    def test_isolated_flight_matches_verified_durations(self):
        r = run_cell([row("A", 3000, 30, [2100, 2100])], ONE, 5, "fcfs")
        f = flight(r, "A")
        self.assertEqual(f["state"], "departed")
        self.assertEqual(f["touchdown_s"], 3000)
        self.assertEqual(f["liftoff_s"] - f["touchdown_s"], S("2329.0"))   # 279,8 + 1800 + 2 x 124,6
        self.assertEqual(f["stand_exit_s"] - f["stand_entry_s"], S("2195.7"))
        self.assertEqual(f["await_s"], 0)
        self.assertTrue(f["punctual"])
        occupied = [(res, a, b) for res, _, a, b in r["intervals"] if res.endswith("_occupied")]
        self.assertEqual(sorted(occupied), sorted([
            ("tlof_occupied", 3000, S("3037.7")), ("route_occupied", S("3037.7"), S("3060.5")),
            ("stand_occupied", S("3060.5"), S("5256.2")), ("route_occupied", S("5256.2"), S("5279.0")),
            ("tlof_occupied", S("5279.0"), S("5329.0"))]))

    def test_route_spaces_simultaneous_arrivals(self):
        r = run_cell([row("A", 3000, 30, [2100]), row("B", 3000, 30, [2100])], ONE, 5, "fcfs")
        self.assertEqual([flight(r, k)["touchdown_s"] for k in "AB"], [3000, S("3060.5")])
        self.assertEqual([flight(r, k)["stand"] for k in "AB"], [1, 2])

    def test_diversion_after_window_removes_passengers(self):
        rows = [row("A", 3000, 30, [2100]), row("B", 3100, 30, [2200, 3500])]
        r = run_cell(rows, ONE, 1, "fcfs")
        b = flight(r, "B")
        self.assertEqual((b["state"], b["diverted_s"]), ("diverted", 3400))
        self.assertEqual(r["passengers"]["B-P1"]["state"], "left_lounge_diversion")
        self.assertEqual(r["passengers"]["B-P2"]["state"], "not_arrived_diversion")
        self.assertEqual(r["metrics"]["diverted"], 1)

    def test_window_end_is_inclusive(self):
        # A rota limita: cinco toques a cada 60,5 s desde 3000 s; o sexto voo toca em 3302,5 s.
        first = [row(f"F{i}", 3000, 30, [2100]) for i in range(5)]
        ok = run_cell(first + [row("X", S("3002.5"), 30, [2100])], ONE, 6, "fcfs")
        self.assertEqual(flight(ok, "X")["touchdown_s"], S("3302.5"))      # exatamente t + 300 s
        late = run_cell(first + [row("X", S("3002.4"), 30, [2100])], ONE, 6, "fcfs")
        self.assertEqual(flight(late, "X")["state"], "diverted")            # precisaria de 300,1 s

    def test_group_retains_aircraft(self):
        # R = 0: aeronave pronta em t + 180; passageiro chega em t e fica pronto em t + 315.
        r = run_cell([row("A", 3000, 0, [3000])], ONE, 5, "fcfs")
        f = flight(r, "A")
        self.assertEqual(f["ready_board_s"], 3180)
        self.assertEqual(f["await_s"], 135)
        self.assertEqual(f["liftoff_s"], S("3539.4"))
        self.assertEqual(r["metrics"]["retained_flights"], 1)

    def test_departure_blocked_by_arrival_on_route(self):
        rows = [row("A", 3000, 0, [2100]), row("B", S("3321.6"), 0, [2400])]
        r = run_cell(rows, ONE, 5, "fcfs")
        a = flight(r, "A")
        self.assertEqual(a["ready_depart_s"], S("3331.6"))
        self.assertEqual(a["stand_exit_s"], S("3382.1"))
        self.assertEqual(a["stand_blocked_s"], S("50.5"))

    def test_empty_group(self):
        r = run_cell([row("A", 3000, 0, [None, None]), row("B", 3000, 30, [None])], ONE, 5, "fcfs")
        self.assertEqual(flight(r, "A")["state"], "cancelled_empty")
        self.assertEqual(flight(r, "B")["state"], "departed")
        self.assertTrue(flight(r, "B")["empty"])
        self.assertEqual(r["metrics"]["departed_empty"], 1)

    def test_pending_at_horizon(self):
        r = run_cell([row("A", 28000, 30, [27500])], ONE, 5, "fcfs")
        self.assertEqual(flight(r, "A")["state"], "pending")
        self.assertIsNone(flight(r, "A")["liftoff_s"])
        self.assertEqual(r["metrics"]["pending"], 1)

    def test_stand_count_does_not_change_terminal_without_exits(self):
        rows = [row(f"F{i}", 3000 + 3600 * i, 30, [2400 + 3600 * i, 2500 + 3600 * i]) for i in range(4)]
        five = run_cell(rows, ONE, 5, "fcfs")
        four = run_cell(rows, ONE, 4, "fcfs")
        self.assertEqual(five["metrics"]["diverted"] + four["metrics"]["diverted"], 0)
        self.assertEqual(five["summary"], four["summary"])

    def test_invariants_on_generated_day(self):
        rows = family_requests(generate_day(12), 8, 30)
        for policy in ("fcfs", "agenda"):
            for stands in (4, 5):
                r = run_cell(rows, {**ONE, "counter": 2}, stands, policy)
                m = r["metrics"]
                self.assertEqual(m["offered"], len(rows))
                self.assertEqual(m["offered"], m["cancelled_empty"] + m["refused"] + m["diverted"]
                                 + m["departed"] + m["pending"])
                check_resources(self, r, stands)
                check_boarding_and_passengers(self, r, rows)

    def test_deterministic(self):
        rows = family_requests(generate_day(1), 6, 30)
        self.assertEqual(run_cell(rows, ONE, 5, "fcfs")["metrics"],
                         run_cell(rows, ONE, 5, "fcfs")["metrics"])


class TestAgenda(unittest.TestCase):
    def test_isolated_flight_planned_at_request_equals_fcfs(self):
        rows = [row("A", 3000, 30, [2100, 2100])]
        agenda, fcfs = run_cell(rows, ONE, 5, "agenda"), run_cell(rows, ONE, 5, "fcfs")
        a = flight(agenda, "A")
        self.assertEqual((a["planned_touchdown_s"], a["planned_stand"]), (3000, 1))
        self.assertEqual(a["planned_exit_s"], S("5256.2"))
        self.assertEqual(a["liftoff_s"], flight(fcfs, "A")["liftoff_s"])

    def test_simultaneous_requests_reserve_arrival_and_departure(self):
        # Em 3060,5 s (rota livre) a partida de B ocuparia o TLOF em [5192,1; 5267,9),
        # sobre a partida reservada de A [5131,6; 5207,4). A agenda reserva também a
        # partida: B toca em 3075,8 s e sai do stand quando a partida de A termina.
        r = run_cell([row("A", 3000, 30, [2100]), row("B", 3000, 30, [2100])], ONE, 5, "agenda")
        a, b = flight(r, "A"), flight(r, "B")
        self.assertEqual([a["planned_touchdown_s"], b["planned_touchdown_s"]], [3000, S("3075.8")])
        self.assertEqual([a["stand"], b["stand"]], [1, 2])
        self.assertEqual(b["planned_exit_s"], S("5207.4"))
        self.assertEqual(b["stand_exit_s"], b["planned_exit_s"])

    def test_refusal_at_decision_removes_passengers(self):
        rows = [row("A", 3000, 30, [2100]), row("B", 3100, 30, [2200, 3500])]
        r = run_cell(rows, ONE, 1, "agenda")
        b = flight(r, "B")
        self.assertEqual((b["state"], b["refused_s"]), ("refused", 3100))
        self.assertEqual(r["passengers"]["B-P1"]["state"], "left_lounge_refusal")
        self.assertEqual(r["passengers"]["B-P1"]["exit_s"], 3100)
        self.assertEqual(r["passengers"]["B-P2"]["state"], "not_arrived_refusal")
        self.assertEqual(r["metrics"]["refused"], 1)

    def test_pessimistic_forecast_holds_aircraft_until_planned_exit(self):
        rows = [row("A", 3000, 30, [3500])]          # ainda não chegou na decisão
        base = flight(run_cell(rows, ONE, 5, "agenda"), "A")
        self.assertEqual(base["planned_exit_s"], S("5266.6"))   # 4800 + 315 + 124,6 + 27
        self.assertEqual(base["ready_depart_s"], S("5131.6"))
        self.assertEqual((base["stand_exit_s"], base["stand_blocked_s"]), (S("5266.6"), S("135.0")))
        perfect = flight(run_cell(rows, ONE, 5, "agenda", perfect=True), "A")
        self.assertEqual(perfect["planned_exit_s"], S("5131.6"))
        self.assertEqual(perfect["stand_blocked_s"], 0)

    def test_longer_bag_than_forecast_delays_exit_beyond_plan(self):
        # Decisão em 3000 s com o passageiro no balcão; bagagem prevista 45 s, realizada 60 s.
        rows = [row("A", 3000, 0, [2950], bag=60)]
        r = run_cell(rows, ONE, 5, "agenda")
        a = flight(r, "A")
        self.assertEqual(a["planned_exit_s"], S("3416.6"))
        self.assertEqual(a["stand_exit_s"], S("3431.6"))
        self.assertEqual(r["metrics"]["late_vs_plan"], 1)
        p = flight(run_cell(rows, ONE, 5, "agenda", perfect=True), "A")
        self.assertEqual(p["planned_exit_s"], p["stand_exit_s"])

    def test_decision_ignores_future_requests(self):
        alone = run_cell([row("A", 3000, 30, [2100])], ONE, 1, "agenda")
        later = run_cell([row("A", 3000, 30, [2100]), row("B", 3200, 30, [2300])], ONE, 1, "agenda")
        keys = ("planned_touchdown_s", "planned_stand", "planned_exit_s")
        self.assertEqual([flight(alone, "A")[k] for k in keys], [flight(later, "A")[k] for k in keys])

    def test_perfect_information_requires_agenda(self):
        with self.assertRaises(ValueError):
            run_cell([row("A", 3000, 30, [2100])], ONE, 5, "fcfs", perfect=True)


def check_resources(test, result, stands):
    spans = result["intervals"]
    for resource, cap in (("tlof", 1), ("route", 1)):
        rows = sorted((a, b) for res, _, a, b in spans if res == resource)
        for (a1, b1), (a2, _) in zip(rows, rows[1:]):
            test.assertGreaterEqual(a2, b1, f"{resource} overlap")
    tlof = sorted((a, b) for res, _, a, b in spans if res == "tlof_separation")
    occupied = sorted((a, b) for res, _, a, b in spans if res == "tlof")
    for _, sep_end in tlof:
        for a, _ in occupied:
            test.assertFalse(sep_end - 3 < a < sep_end, "TLOF used during separation")
    for k in range(1, stands + 1):
        rows = sorted((a, b) for res, key, a, b in spans if res == "stand" and key == k)
        for (a1, b1), (a2, _) in zip(rows, rows[1:]):
            test.assertGreaterEqual(a2, b1, f"stand {k} overlap")
    test.assertFalse(any(res == "stand" and not 1 <= key <= stands for res, key, _, _ in spans))


def check_boarding_and_passengers(test, result, rows):
    walk_enter = S("51.6")                     # 31,9 + 19,7 s até o início do embarque
    starts = {}
    for pid, p in result["passengers"].items():
        if p["boarding_start_s"] is not None:
            test.assertGreaterEqual(p["boarding_start_s"], p["ready_s"] + walk_enter)
            starts.setdefault(p["flight"], []).append(p["boarding_start_s"])
    for flight_starts in starts.values():
        flight_starts.sort()
        for a, b in zip(flight_starts, flight_starts[1:]):
            test.assertGreaterEqual(b - a, S("124.6"))     # embarque sequencial
    reservations = sum(len(r["manifest"]) for r in rows)
    absent = sum(p["arrival_s"] is None for r in rows for p in r["manifest"])
    states = [p["state"] for p in result["passengers"].values()]
    boarded = sum(p["boarding_start_s"] is not None for p in result["passengers"].values())
    lost = sum(st.startswith(("left_", "not_arrived_")) for st in states)
    test.assertEqual(len(states), reservations - absent)
    test.assertEqual(result["metrics"]["boarded_passengers"], boarded)
    test.assertEqual(result["metrics"]["lost_passengers"], lost)
    test.assertLessEqual(boarded + lost, reservations - absent)   # o resto segue em curso


if __name__ == "__main__":
    unittest.main()
