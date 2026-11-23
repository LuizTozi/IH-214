"""Terminal da D4 (D4.1 v2.1): balcão, bagagem e inspeção com um ou dois servidores.

Cada estação é uma fila FCFS única, sem abandono, atendida por c servidores
(`simpy.Resource(capacity=c)`); o passageiro da frente ocupa o servidor livre de
menor índice. A recusa (agenda) ou o desvio (FCFS) do voo, comunicado em um
instante, retira os passageiros do terminal (PAR-062):

- ainda não chegou: não comparece;
- em fila: sai no próprio instante, com espera censurada;
- em atendimento: conclui o serviço em curso e sai;
- na sala de espera (após a inspeção): é retirado da sala.

Empate no mesmo instante entre o aviso e o início do atendimento: prevalece o
aviso, e o servidor é devolvido sem atendimento.

O tempo interno é inteiro em milissegundos, como no VertiSim (Onat, licença MIT,
https://github.com/eminb61/vertisim), de onde também vem o padrão de retirar
passageiros da sala de espera por predicado (`FilterStore`). A saída da fila
combina a espera pela vez com o evento de aviso (`req | aviso`), padrão de
desistência da documentação da SimPy (licença MIT). O código abaixo foi escrito
para este projeto; não há trecho copiado desses repositórios.
"""

from decimal import Decimal
from math import ceil

import simpy

from d4_param import BAG_FORECAST, BAG_HIGH, BAG_LOW, COUNTER_DECLARED, SECURITY_DECLARED

STATIONS = ("counter", "baggage", "security")
SERVICE_S = {"counter": 180, "security": 90}            # PAR-046, PAR-047
WAIT_LIMIT_S = {"counter": 180, "baggage": None, "security": 180}   # PAR-026
REASONS = ("refusal", "diversion")


def to_ms(seconds):
    value = Decimal(seconds) * 1000
    if value != value.to_integral_value():
        raise ValueError(f"{seconds} s exceeds millisecond resolution")
    return int(value)


def to_s(ms):
    return None if ms is None else Decimal(ms) / 1000


class Terminal:
    """Estações e sala de espera; o lado ar chama `cancel_flight` e `board`."""

    def __init__(self, env, servers):
        if set(servers) != set(STATIONS) or not all(c in (1, 2) for c in servers.values()):
            raise ValueError("servers must give 1 or 2 servers for counter, baggage and security")
        self.env = env
        self.servers = dict(servers)
        self.resources = {s: simpy.Resource(env, capacity=c) for s, c in servers.items()}
        self.free = {s: [True] * c for s, c in servers.items()}
        self.lounges = {}          # voo -> sala de espera do grupo (ordem de prontidão)
        self.persons = {}
        self.notices = {}          # voo -> evento de aviso (recusa ou desvio)
        self.reasons = {}
        self.visits = []
        self.passengers = {}

    def notice(self, flight):
        if flight not in self.notices:
            self.notices[flight] = self.env.event()
        return self.notices[flight]

    def lounge(self, flight):
        """Sala de espera do voo; o lado ar retira os passageiros por `get()`."""
        if flight not in self.lounges:
            self.lounges[flight] = simpy.FilterStore(self.env)
        return self.lounges[flight]

    def cancel_flight(self, flight, reason):
        if reason not in REASONS:
            raise ValueError(f"reason must be one of {REASONS}")
        event = self.notice(flight)
        if not event.triggered:
            self.reasons[flight] = reason
            event.succeed(reason)

    def admit(self, person):
        pid = person["id"]
        if pid in self.passengers:
            raise ValueError(f"duplicate passenger {pid}")
        self.persons[pid] = person
        self.passengers[pid] = {"id": pid, "flight": person["flight"],
                                "arrival_ms": to_ms(person["arrival_s"]),
                                "state": "scheduled", "ready_ms": None, "exit_ms": None}
        self.env.process(self._journey(person))

    def _leave(self, row, state):
        row["state"], row["exit_ms"] = state, self.env.now

    def _journey(self, person):
        row = self.passengers[person["id"]]
        notice = self.notice(person["flight"])
        delay = row["arrival_ms"] - self.env.now
        if delay < 0:
            raise ValueError(f"{person['id']} arrives before the current time")
        yield self.env.timeout(delay) | notice
        if notice.triggered:
            self._leave(row, f"not_arrived_{self.reasons[person['flight']]}")
            return
        row["state"] = "in_terminal"
        for station in STATIONS:
            service = to_ms(person["bag_s"] if station == "baggage" else SERVICE_S[station])
            visit = {"id": person["id"], "flight": person["flight"], "station": station,
                     "entry_ms": self.env.now, "start_ms": None, "end_ms": None,
                     "server": None, "exit_ms": None, "exit_reason": None}
            self.visits.append(visit)
            resource = self.resources[station]
            request = resource.request()
            yield request | notice
            if notice.triggered:             # aviso antes ou no mesmo instante da vez
                if request.triggered:
                    resource.release(request)
                else:
                    request.cancel()
                visit["exit_ms"], visit["exit_reason"] = self.env.now, self.reasons[person["flight"]]
                self._leave(row, f"left_{self.reasons[person['flight']]}")
                return
            server = self.free[station].index(True)
            self.free[station][server] = False
            visit["start_ms"], visit["server"] = self.env.now, server + 1
            yield self.env.timeout(service)
            visit["end_ms"] = self.env.now
            self.free[station][server] = True
            resource.release(request)
            if notice.triggered:             # concluiu o serviço em curso e sai
                visit["exit_ms"], visit["exit_reason"] = self.env.now, self.reasons[person["flight"]]
                self._leave(row, f"left_{self.reasons[person['flight']]}")
                return
        row["state"], row["ready_ms"] = "in_lounge", self.env.now
        lounge = self.lounge(person["flight"])
        yield lounge.put(person["id"])
        yield notice
        if person["id"] in lounge.items:
            yield lounge.get(lambda p: p == person["id"])
            self._leave(row, f"left_lounge_{self.reasons[person['flight']]}")

    def forecast_ready(self, perfect=False):
        """Previsão do instante de prontidão de quem já chegou (D4.1 v2.1).

        Projeta o estado observado das filas sem novas chegadas: balcão e inspeção
        pelas durações declaradas; bagagem em curso pela média de U(30, 60) s
        condicionada ao tempo decorrido; bagagem não iniciada por 45 s. Com
        informação perfeita, a bagagem usa a duração realizada. Quem está na sala
        de espera já está pronto. Retorna {passageiro: instante_ms}.
        """
        now = self.env.now
        ready = {pid: r["ready_ms"] for pid, r in self.passengers.items()
                 if r["state"] == "in_lounge"}
        current = {}
        for order, visit in enumerate(self.visits):
            if self.passengers[visit["id"]]["state"] == "in_terminal":
                current[visit["id"]] = (order, visit)

        def duration(pid, station):
            if station == "counter":
                return COUNTER_DECLARED
            if station == "security":
                return SECURITY_DECLARED
            return to_ms(self.persons[pid]["bag_s"]) if perfect else BAG_FORECAST

        def remaining(pid, visit):
            elapsed = now - visit["start_ms"]
            if visit["station"] != "baggage":
                return duration(pid, visit["station"]) - elapsed
            if perfect:
                return to_ms(self.persons[pid]["bag_s"]) - elapsed
            if elapsed < BAG_LOW:
                return BAG_FORECAST - elapsed
            return (elapsed + BAG_HIGH) // 2 - elapsed     # média condicionada

        # Estação por estação: quem está em atendimento ocupa um servidor até
        # terminar; os demais (fila atual + vindos da estação anterior) são
        # atendidos em ordem de chegada pelo servidor livre mais cedo.
        coming = []           # (instante disponível na estação, ordem, passageiro)
        for station in STATIONS:
            free = [now] * self.servers[station]
            leaving = []
            queue = list(coming)
            for pid, (order, visit) in current.items():
                if visit["station"] != station:
                    continue
                if visit["start_ms"] is None:
                    queue.append((visit["entry_ms"], order, pid))
                else:
                    slot = free.index(min(free))
                    free[slot] = now + remaining(pid, visit)
                    leaving.append((free[slot], order, pid))
            for avail, order, pid in sorted(queue):
                slot = free.index(min(free))
                free[slot] = max(avail, free[slot]) + duration(pid, station)
                leaving.append((free[slot], order, pid))
            coming = leaving
        for t, _, pid in coming:
            ready[pid] = t
        return ready


def passengers_from_family(rows):
    """Converte os pedidos de uma família (d4_dia) em passageiros presentes."""
    return [{"id": p["id"], "flight": r["id"], "arrival_s": p["arrival_s"],
             "bag_s": p["bag_service_s"]}
            for r in rows for p in r["manifest"] if p["arrival_s"] is not None]


def summarize(visits, horizon_ms):
    summary = {}
    for station in STATIONS:
        rows = [v for v in visits if v["station"] == station and v["entry_ms"] < horizon_ms]
        waits = sorted(v["start_ms"] - v["entry_ms"] for v in rows
                       if v["start_ms"] is not None and v["start_ms"] < horizon_ms)
        limit = WAIT_LIMIT_S[station]
        summary[station] = {
            "complete": len(waits),
            "censored_at_horizon": sum((v["start_ms"] is None or v["start_ms"] >= horizon_ms)
                                       and v["exit_ms"] is None for v in rows),
            "left_refusal": sum(v["start_ms"] is None and v["exit_reason"] == "refusal" for v in rows),
            "left_diversion": sum(v["start_ms"] is None and v["exit_reason"] == "diversion"
                                  for v in rows),
            "mean_wait_s": to_s(sum(waits) / len(waits)) if waits else None,
            "p95_wait_s": to_s(waits[ceil(0.95 * len(waits)) - 1]) if waits else None,
            "within_limit": sum(w <= limit * 1000 for w in waits) if limit is not None else None,
            "limit_s": limit,
        }
    return summary


def run_terminal(people, servers, cancels=(), horizon_s=28800):
    """Executa só o terminal, com avisos (instante_s, voo, motivo) predefinidos."""
    env = simpy.Environment()
    terminal = Terminal(env, servers)
    for person in sorted(people, key=lambda p: (p["arrival_s"], p["id"])):
        terminal.admit(person)

    def announce(at_ms, flight, reason):
        yield env.timeout(at_ms)
        terminal.cancel_flight(flight, reason)

    for at, flight, reason in cancels:
        env.process(announce(to_ms(at), flight, reason))
    horizon_ms = to_ms(horizon_s)
    env.run(until=horizon_ms)

    def seen(ms):
        return to_s(ms) if ms is not None and ms < horizon_ms else None

    visits = [{"id": v["id"], "flight": v["flight"], "station": v["station"],
               "entry_s": to_s(v["entry_ms"]), "start_s": seen(v["start_ms"]),
               "end_s": seen(v["end_ms"]), "server": v["server"] if seen(v["start_ms"]) is not None else None,
               "wait_s": (to_s(v["start_ms"] - v["entry_ms"])
                          if seen(v["start_ms"]) is not None else None),
               "exit_s": seen(v["exit_ms"]), "exit_reason": v["exit_reason"]}
              for v in terminal.visits]
    passengers = {pid: {"state": r["state"], "ready_s": seen(r["ready_ms"]),
                        "exit_s": seen(r["exit_ms"])}
                  for pid, r in terminal.passengers.items()}
    lounge = [pid for store in terminal.lounges.values() for pid in store.items]
    return {"visits": visits, "passengers": passengers, "lounge": lounge,
            "summary": summarize(terminal.visits, horizon_ms), "servers": dict(servers)}
