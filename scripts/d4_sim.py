"""Lado ar da D4 (D4.1 v2.1) acoplado ao terminal: uma célula = configuração × política.

Recursos: um TLOF (com separação após cada saída), uma rota bidirecional unitária e
N stands, cada um com carregador e gate próprios (SUPOSTO, PAR-057).

- Chegada: exige TLOF, rota e stand livres ao mesmo tempo. Ocupa o TLOF por 37,7 s
  (depois 3 s de separação) e a rota até a entrada no stand (60,5 s após o toque).
- No stand: rebocador, desembarque, saída pelo gate, recarga declarada; depois,
  embarque individual e sequencial dos confirmados, na ordem em que ficam prontos
  na sala de espera (a espera da aeronave por eles é a retenção pelo grupo);
  por fim, prender o rebocador.
- Partida: exige rota e TLOF; o stand é liberado na saída. Decolagem 22,8 + 50 s
  após a saída do stand; depois, 3 s de separação.

Alocação: um controlador concede, entre as solicitações elegíveis, a de menor
chave (FCFS: instante da solicitação; agenda: instante planejado), com empate pelo
número de ordem. Varreduras ocorrem após as liberações do mesmo instante.

- FCFS: a aeronave que não inicia a chegada até t + 300 s desvia, e o terminal é
  avisado (PAR-055, PAR-062).
- Agenda: decide em t pelo módulo d4_agenda; recusa avisa o terminal. Na execução
  (D4.1 v2.2), o toque não ocorre antes do instante planejado e usa o stand
  reservado. A saída planejada é prioridade, não horário mínimo: a aeronave pronta
  antes do plano sai assim que rota e TLOF estiverem livres, como na renegociação
  de uma reserva compatível com o plano de recursos (LIT-008, §5.2.1.2, p. 82).
  Entre solicitações prontas prevalece o menor horário planejado; uma demora
  propaga o início até a primeira disponibilidade conjunta (não há bloqueio por
  compromisso ainda não pronto).
"""

from decimal import Decimal
from math import ceil

import simpy

from d4_param import (ARR_ROUTE, ARR_TLOF, ATTACH, BOARD, DEP_OCC, ENTER, OCC_ARR, SEP,
                      STAND_INBOUND, TAXI, TOLERANCE, WALK, WINDOW)
from d4_terminal import Terminal, passengers_from_family, summarize, to_ms, to_s

POLICIES = ("fcfs", "agenda")


class Airside:
    def __init__(self, env, terminal, n_stands, policy, perfect=False):
        if policy not in POLICIES:
            raise ValueError(f"policy must be one of {POLICIES}")
        if perfect and policy != "agenda":
            raise ValueError("perfect information applies only to the agenda")
        if type(n_stands) is not int or n_stands < 1:
            raise ValueError("n_stands must be a positive integer")
        self.env, self.terminal = env, terminal
        self.policy, self.perfect = policy, perfect
        self.tlof_holder, self.tlof_free_at, self.route_holder = None, 0, None
        self.stands = [None] * n_stands
        self.pending, self.seq = [], 0
        self.flights, self.rows, self.boarding = {}, {}, {}
        self.intervals = []        # [recurso, chave, início_ms, fim_ms ou None]

    # ---------- registro de ocupação ----------
    def _open(self, resource, key):
        span = [resource, key, self.env.now, None]
        self.intervals.append(span)
        return span

    def _close(self, span):
        span[3] = self.env.now

    # ---------- controlador de recursos ----------
    def _request(self, kind, fid, key, eligible_from=0, stand=None):
        req = {"kind": kind, "fid": fid, "key": key, "from": eligible_from, "stand": stand,
               "event": self.env.event(), "seq": self.seq}
        self.seq += 1
        self.pending.append(req)
        self._scan_at(max(self.env.now, eligible_from))
        return req

    def _scan_at(self, at):
        self.env.process(self._deferred_scan(at - self.env.now))

    def _deferred_scan(self, delay):
        yield self.env.timeout(delay)
        yield self.env.timeout(0)          # deixa as liberações do mesmo instante primeiro
        self.scan()

    def scan(self):
        granted = True
        while granted:
            granted = False
            for req in sorted(self.pending, key=lambda r: (r["key"], r["seq"])):
                stand = self._grantable(req)
                if stand is not False:
                    self.pending.remove(req)
                    req["event"].succeed(stand)
                    if req["kind"] == "arr":
                        self.stands[stand] = req["fid"]
                    self.tlof_holder = self.route_holder = req["fid"]
                    granted = True
                    break

    def _grantable(self, req):
        now = self.env.now
        if now < req["from"] or self.route_holder is not None:
            return False
        if self.tlof_holder is not None or now < self.tlof_free_at:
            return False
        if req["kind"] == "dep":
            return None
        if req["stand"] is not None:
            return req["stand"] if self.stands[req["stand"]] is None else False
        free = [i for i, holder in enumerate(self.stands) if holder is None]
        return free[0] if free else False

    def _release_tlof(self, span):
        self._close(span)
        self.tlof_holder = None
        self.tlof_free_at = self.env.now + SEP
        sep = self._open("tlof_separation", None)
        sep[3] = self.tlof_free_at
        self._scan_at(self.tlof_free_at)

    def _release_route(self, span):
        self._close(span)
        self.route_holder = None
        self._scan_at(self.env.now)

    # ---------- voo ----------
    def start(self, row):
        fid = row["id"]
        self.rows[fid] = row
        self.flights[fid] = {
            "id": fid, "request_ms": to_ms(row["request_s"]), "state": "requested",
            "std_ms": to_ms(row["target_departure_s"]), "close_ms": to_ms(row["manifest_close_s"]),
            "charge_ms": 60_000 * row["declared_charge_min"],
            "present": [p["id"] for p in row["manifest"] if p["arrival_s"] is not None],
            "reservations": [p["id"] for p in row["manifest"]],
            "planned_touchdown_ms": None, "planned_exit_ms": None, "planned_stand": None,
            "touchdown_ms": None, "stand": None, "stand_entry_ms": None, "ready_board_ms": None,
            "avail_ms": None, "boarded": [], "taken": [], "await_ms": 0, "ready_depart_ms": None,
            "stand_exit_ms": None, "liftoff_ms": None, "diverted_ms": None, "refused_ms": None,
        }
        self.env.process(self._flight(fid))

    def _flight(self, fid):
        f = self.flights[fid]
        yield self.env.timeout(f["request_ms"] - self.env.now)
        if f["close_ms"] <= self.env.now and not f["present"]:
            f["state"] = "cancelled_empty"         # grupo vazio antes da alocação
            return
        if 0 < f["close_ms"] - self.env.now <= WINDOW:
            raise ValueError(f"{fid}: manifest closes inside the touchdown window (not specified)")
        if self.policy == "fcfs":
            req = self._request("arr", fid, key=self.env.now)
            self.env.process(self._divert_after(req, self.env.now + WINDOW))
        else:
            import d4_agenda
            plan = d4_agenda.decide(self, fid)
            if plan is None:
                f["state"], f["refused_ms"] = "refused", self.env.now
                self.terminal.cancel_flight(fid, "refusal")
                return
            f["planned_touchdown_ms"], f["planned_stand"], f["planned_exit_ms"] = plan
            f["state"] = "admitted"
            req = self._request("arr", fid, key=plan[0], eligible_from=plan[0], stand=plan[1])
        f["state"] = f["state"] if f["state"] == "admitted" else "waiting_touchdown"
        stand = yield req["event"]
        if stand is None:
            return                                   # desviado
        yield from self._cycle(fid, stand)

    def _divert_after(self, req, deadline):
        yield self.env.timeout(deadline - self.env.now)
        yield self.env.timeout(0)                  # liberações do instante final primeiro
        self.scan()                                # toque em t + 300 s ainda é permitido
        if req in self.pending:
            self.pending.remove(req)
            f = self.flights[req["fid"]]
            f["state"], f["diverted_ms"] = "diverted", self.env.now
            self.terminal.cancel_flight(req["fid"], "diversion")
            req["event"].succeed(None)

    def _cycle(self, fid, stand):
        f, env = self.flights[fid], self.env
        f["state"], f["touchdown_ms"], f["stand"] = "on_ground", env.now, stand
        # Posse (exclusividade) e ocupação física são registradas separadamente.
        tlof = self._open("tlof", fid)
        tlof_occ = self._open("tlof_occupied", fid)
        route = self._open("route", fid)
        stand_span = self._open("stand", stand + 1)
        yield env.timeout(OCC_ARR)
        self._close(tlof_occ)
        self._release_tlof(tlof)
        route_occ = self._open("route_occupied", fid)
        yield env.timeout(TAXI)
        self._close(route_occ)
        self._release_route(route)
        f["stand_entry_ms"] = env.now
        stand_occ = self._open("stand_occupied", stand + 1)
        yield env.timeout(STAND_INBOUND + f["charge_ms"])
        f["ready_board_ms"] = f["avail_ms"] = env.now
        if env.now < f["close_ms"]:
            yield env.timeout(f["close_ms"] - env.now)
        lounge = self.terminal.lounge(fid)
        for _ in f["present"]:
            got = lounge.get()                    # próximo confirmado pronto
            yield got
            f["await_ms"] += env.now - f["avail_ms"]
            pid = got.value
            f["taken"].append(pid)
            f["avail_ms"] = env.now + WALK + ENTER + BOARD
            yield env.timeout(WALK + ENTER)
            self.boarding[pid] = env.now          # início do embarque
            yield env.timeout(BOARD)
            f["boarded"].append(pid)
        yield env.timeout(ATTACH)
        f["ready_depart_ms"] = env.now
        if self.policy == "fcfs":
            req = self._request("dep", fid, key=env.now)
        else:   # agenda: a saída planejada é só chave de prioridade (D4.1 v2.2)
            req = self._request("dep", fid, key=f["planned_exit_ms"])
        yield req["event"]
        f["stand_exit_ms"] = env.now
        self._close(stand_occ)
        self._close(stand_span)
        self.stands[stand] = None
        self._scan_at(env.now)
        tlof = self._open("tlof", fid)              # reservado durante o táxi
        route = self._open("route", fid)
        route_occ = self._open("route_occupied", fid)
        yield env.timeout(TAXI)
        self._close(route_occ)
        self._release_route(route)
        tlof_occ = self._open("tlof_occupied", fid)
        yield env.timeout(DEP_OCC)
        f["liftoff_ms"] = env.now
        f["state"] = "departed"
        self._close(tlof_occ)
        self._release_tlof(tlof)


def run_cell(rows, servers, n_stands, policy, perfect=False, horizon_s=28800):
    """Executa uma célula com os pedidos de uma família (d4_dia.family_requests)."""
    env = simpy.Environment()
    terminal = Terminal(env, servers)
    for person in sorted(passengers_from_family(rows), key=lambda p: (p["arrival_s"], p["id"])):
        terminal.admit(person)
    airside = Airside(env, terminal, n_stands, policy, perfect)
    for row in sorted(rows, key=lambda r: (r["request_s"], r["id"])):
        airside.start(row)
    horizon = to_ms(horizon_s)
    env.run(until=horizon)
    return collect(airside, terminal, horizon, servers, n_stands, policy, perfect)


def collect(airside, terminal, horizon, servers, n_stands, policy, perfect):
    def seen(ms):
        return to_s(ms) if ms is not None and ms < horizon else None

    flights = {}
    for fid, f in airside.flights.items():
        state = f["state"]
        if state not in ("cancelled_empty", "refused", "diverted") and seen(f["liftoff_ms"]) is None:
            state = "pending"
        flights[fid] = {
            "state": state, "request_s": to_s(f["request_ms"]), "std_s": to_s(f["std_ms"]),
            "stand": None if f["stand"] is None else f["stand"] + 1,
            "planned_touchdown_s": to_s(f["planned_touchdown_ms"]),
            "planned_stand": None if f["planned_stand"] is None else f["planned_stand"] + 1,
            "planned_exit_s": to_s(f["planned_exit_ms"]),
            "touchdown_s": seen(f["touchdown_ms"]), "stand_entry_s": seen(f["stand_entry_ms"]),
            "ready_board_s": seen(f["ready_board_ms"]), "ready_depart_s": seen(f["ready_depart_ms"]),
            "stand_exit_s": seen(f["stand_exit_ms"]), "liftoff_s": seen(f["liftoff_ms"]),
            "diverted_s": seen(f["diverted_ms"]), "refused_s": seen(f["refused_ms"]),
            "await_s": to_s(f["await_ms"]), "empty": not f["present"],
            "boarded": len([p for p in f["boarded"] if airside.boarding[p] < horizon]),
            "stand_blocked_s": (to_s(f["stand_exit_ms"] - f["ready_depart_ms"])
                                if seen(f["stand_exit_ms"]) is not None else None),
            "outside_window": (f["touchdown_ms"] is not None
                               and f["touchdown_ms"] > f["request_ms"] + WINDOW),
            "punctual": (seen(f["liftoff_ms"]) is not None
                         and f["liftoff_ms"] <= f["std_ms"] + TOLERANCE),
        }
    passengers = {pid: {"state": r["state"], "flight": r["flight"],
                        "arrival_s": to_s(r["arrival_ms"]), "ready_s": seen(r["ready_ms"]),
                        "exit_s": seen(r["exit_ms"]),
                        "boarding_start_s": seen(airside.boarding.get(pid))}
                  for pid, r in terminal.passengers.items()}
    intervals = [(res, key, to_s(a), to_s(min(b, horizon) if b is not None else horizon))
                 for res, key, a, b in airside.intervals if a < horizon]
    return {"flights": flights, "passengers": passengers, "intervals": intervals,
            "summary": summarize(terminal.visits, horizon),
            "metrics": metrics(flights, passengers, intervals, horizon, n_stands),
            "config": {"servers": dict(servers), "n_stands": n_stands, "policy": policy,
                       "perfect": perfect, "horizon_s": to_s(horizon)}}


def metrics(flights, passengers, intervals, horizon, n_stands):
    hours = Decimal(horizon) / 3_600_000
    states = [f["state"] for f in flights.values()]
    departed = [f for f in flights.values() if f["state"] == "departed"]
    carrying = [f for f in departed if not f["empty"]]
    landed = [f for f in flights.values() if f["touchdown_s"] is not None]
    lateness = [max(Decimal(0), f["liftoff_s"] - f["std_s"]) for f in departed]
    # Espera após o processamento: fim da inspeção até o início do embarque (VAR-045).
    # Inclui caminhada e acesso à aeronave (51,6 s) e a espera pela aeronave ou pelo grupo.
    post = sorted(p["boarding_start_s"] - p["ready_s"] for p in passengers.values()
                  if p["boarding_start_s"] is not None)
    lost = sum(p["state"].startswith(("left_", "not_arrived_")) for p in passengers.values())

    def busy(resource, key=None):
        return sum(b - a for res, k, a, b in intervals if res == resource and (key is None or k == key))

    def mean(values):
        values = list(values)
        return sum(values) / len(values) if values else None

    return {
        "offered": len(states),
        "cancelled_empty": states.count("cancelled_empty"),
        "refused": states.count("refused"),
        "diverted": states.count("diverted"),
        "departed": len(departed),
        "departed_empty": len(departed) - len(carrying),
        "pending": states.count("pending"),
        # VAR-016: decolagens com passageiros; as vazias ficam em liftoffs_per_h.
        "departures_per_h": len(carrying) / hours,
        "liftoffs_per_h": len(departed) / hours,
        "punctual": sum(f["punctual"] for f in departed),
        "mean_lateness_s": mean(lateness),
        "retained_flights": sum(f["await_s"] > 0 for f in carrying),
        "mean_await_s": mean(f["await_s"] for f in carrying),
        "mean_stand_blocked_s": mean(f["stand_blocked_s"] for f in departed),
        "mean_air_wait_s": mean(f["touchdown_s"] - f["request_s"] for f in landed),
        "outside_window": sum(f["outside_window"] for f in flights.values()),
        "late_vs_plan": sum(f["planned_exit_s"] is not None and f["stand_exit_s"] is not None
                            and f["stand_exit_s"] > f["planned_exit_s"] for f in flights.values()),
        "boarded_passengers": len(post),
        "lost_passengers": lost,
        "post_security_mean_s": mean(post),
        "post_security_p95_s": post[ceil(0.95 * len(post)) - 1] if post else None,
        # Ocupação física / (unidades × horizonte); a posse inclui reserva e separação.
        "utilization_tlof": busy("tlof_occupied") / to_s(horizon),
        "utilization_route": busy("route_occupied") / to_s(horizon),
        "utilization_stands": busy("stand_occupied") / (n_stands * to_s(horizon)),
        "held_stands": busy("stand") / (n_stands * to_s(horizon)),
    }
