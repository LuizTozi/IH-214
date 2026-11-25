"""Agenda da D4 (D4.1 v2.1): admissão antecipada no instante do pedido.

Em t, a agenda monta o calendário dos compromissos já admitidos, com a previsão
atualizada de cada voo, e procura o primeiro toque viável em [t, t + 300 s]
(PAR-055). Reserva o stand de menor índice que permita esse toque; sem toque
viável, recusa. Nenhuma decisão consulta pedidos ou chegadas futuras.

Uso dos recursos por um voo com toque em τ e saída do stand em x (d4_param):
TLOF [τ, τ + 40,7) e [x, x + 75,8); rota [τ, τ + 60,5) e [x, x + 22,8);
stand [τ, x). Intervalos semiabertos; a separação está incluída no TLOF.

Previsão da prontidão do grupo:
- quem já chegou: projeção das filas observadas (Terminal.forecast_ready);
- reserva ainda não chegada: fechamento do manifesto + durações declaradas,
  sem fila (a previsão mais tardia compatível com o fechamento);
- informação perfeita: chegada e bagagem realizadas; ausências conhecidas;
- após o fechamento do manifesto, só os confirmados entram na previsão.
"""

from d4_param import (ARR_ROUTE, ARR_TLOF, ATTACH, BAG_FORECAST, COUNTER_DECLARED,
                      DEP_ROUTE, DEP_TLOF, PER_PAX, SECURITY_DECLARED, STAND_INBOUND, WINDOW)
from d4_terminal import to_ms

GRID_MS = 1_000      # passo de busca complementar aos candidatos exatos


def stand_exit(ready_board, pax_ready):
    """Saída do stand: embarque sequencial na ordem de prontidão, depois rebocador."""
    avail = ready_board
    for ready in sorted(pax_ready):
        avail = max(avail, ready) + PER_PAX
    return avail + ATTACH


def usage(tau, exit_ms):
    return {"tlof": [(tau, tau + ARR_TLOF), (exit_ms, exit_ms + DEP_TLOF)],
            "route": [(tau, tau + ARR_ROUTE), (exit_ms, exit_ms + DEP_ROUTE)],
            "stand": [(tau, exit_ms)]}


def overlaps(spans, others):
    return any(a < d and c < b for a, b in spans for c, d in others)


def group_forecast(airside, fid, ready_now, now):
    """Previsão de prontidão dos passageiros do voo que ainda não começaram a embarcar."""
    f, row = airside.flights[fid], airside.rows[fid]
    closed = now >= f["close_ms"]
    out = []
    for p in row["manifest"]:
        pid = p["id"]
        if pid in f["taken"]:
            continue
        absent = p["arrival_s"] is None
        if (airside.perfect or closed) and absent:
            continue                      # ausência conhecida
        if pid in ready_now:
            out.append(ready_now[pid])
        elif airside.perfect:
            out.append(to_ms(p["arrival_s"]) + COUNTER_DECLARED + to_ms(p["bag_service_s"])
                       + SECURITY_DECLARED)
        else:
            out.append(max(now, f["close_ms"]) + COUNTER_DECLARED + BAG_FORECAST
                       + SECURITY_DECLARED)
    # Projeções partem de agora; quem está na sala de espera mantém o instante real.
    return out


def forecast_exit(airside, fid, entry_or_tau, now, ready_now):
    f = airside.flights[fid]
    pax = group_forecast(airside, fid, ready_now, now)
    if f["ready_depart_ms"] is not None:
        projected = now
    elif f["ready_board_ms"] is not None:
        projected = stand_exit(max(f["avail_ms"], now), pax)
    else:
        entry = f["stand_entry_ms"] if f["stand_entry_ms"] is not None else entry_or_tau + ARR_ROUTE
        projected = stand_exit(entry + STAND_INBOUND + f["charge_ms"], pax)
    # D4.1 v2.2: o calendário usa a previsão atualizada, sem o piso da saída planejada,
    # pois a execução não retém a aeronave pronta até o plano.
    return max(projected, now)


def calendar(airside, now, ready_now):
    cal = {"tlof": [], "route": [], "stand": {k: [] for k in range(len(airside.stands))}}
    waiting = {k: [] for k in cal["stand"]}
    for fid, f in airside.flights.items():
        if f["liftoff_ms"] is not None:
            if f["liftoff_ms"] + 3_000 > now:
                cal["tlof"].append((f["liftoff_ms"], f["liftoff_ms"] + 3_000))
            continue
        if f["state"] == "admitted":
            waiting[f["planned_stand"]].append(fid)
            continue
        if f["touchdown_ms"] is None:
            continue                       # recusado, cancelado ou ainda sem decisão
        t0, k = f["touchdown_ms"], f["stand"]
        cal["tlof"].append((t0, t0 + ARR_TLOF))
        cal["route"].append((t0, t0 + ARR_ROUTE))
        if f["stand_exit_ms"] is not None:     # já saiu do stand, em partida
            x = f["stand_exit_ms"]
            cal["tlof"].append((x, x + DEP_TLOF))
            cal["route"].append((x, x + DEP_ROUTE))
            continue
        x = forecast_exit(airside, fid, t0, now, ready_now)
        for name, spans in usage(t0, x).items():
            (cal["stand"][k] if name == "stand" else cal[name]).extend(spans)
    for k, fids in waiting.items():
        previous = max([b for _, b in cal["stand"][k]], default=now)
        for fid in sorted(fids, key=lambda i: airside.flights[i]["planned_touchdown_ms"]):
            f = airside.flights[fid]
            tau = max(f["planned_touchdown_ms"], now, previous)
            x = forecast_exit(airside, fid, tau, now, ready_now)
            for name, spans in usage(tau, x).items():
                (cal["stand"][k] if name == "stand" else cal[name]).extend(spans)
            previous = x
    return cal


def decide(airside, fid):
    """Retorna (toque_ms, índice_do_stand, saída_planejada_ms) ou None (recusa)."""
    now = airside.env.now
    f = airside.flights[fid]
    ready_now = airside.terminal.forecast_ready(perfect=airside.perfect)
    cal = calendar(airside, now, ready_now)
    pax = group_forecast(airside, fid, ready_now, now)

    def exit_for(tau):
        return stand_exit(tau + ARR_ROUTE + STAND_INBOUND + f["charge_ms"], pax)

    span = exit_for(now) - now
    ends = [b for spans in (cal["tlof"], cal["route"]) for _, b in spans]
    ends += [b for spans in cal["stand"].values() for _, b in spans]
    candidates = {now + i * GRID_MS for i in range(WINDOW // GRID_MS + 1)}
    candidates |= {e - offset for e in ends for offset in (0, span)}
    for tau in sorted(c for c in candidates if now <= c <= now + WINDOW):
        x = exit_for(tau)
        use = usage(tau, x)
        if overlaps(use["tlof"], cal["tlof"]) or overlaps(use["route"], cal["route"]):
            continue
        for k in range(len(airside.stands)):
            if not overlaps(use["stand"], cal["stand"][k]):
                return tau, k, x
    return None
