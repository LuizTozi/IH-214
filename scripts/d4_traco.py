"""Traço de eventos da D4.6: bloqueio de chegada por falta de stand (contraste Base − S4).

Escolhe, no dia arquivado da semente indicada, o primeiro pedido desviado sob FCFS na
configuração S4 (família de referência) que é atendido na Base, e registra o estado de
cada stand na janela de toque [t, t + 300 s] nas duas configurações.

Uso: python d4_traco.py --day ../data/d4/dias_d4_4/dia_20001.json --out ../data/d4/traco_d4_6.md
"""

import argparse
from pathlib import Path

from d4_dia import family_requests, load_day
from d4_experimento import CONFIGS, FAMILIES
from d4_param import WINDOW
from d4_sim import run_cell


def run(day, config):
    spec = FAMILIES["referencia"]
    stands, servers = CONFIGS[config]
    return run_cell(family_requests(day, spec.rate, spec.charge), servers, stands, "fcfs")


def stand_rows(result, start, end):
    """Ocupações de stand (posse) que intersectam [start, end]."""
    rows = []
    for resource, key, a, b in result["intervals"]:
        if resource == "stand" and a <= end and b >= start:
            holder = next(fid for fid, f in result["flights"].items()
                          if f["stand"] == key and f["touchdown_s"] == a)
            f = result["flights"][holder]
            rows.append((key, holder, a, f["ready_depart_s"], b))
    return sorted(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    day = load_day(args.day)
    s4, base = run(day, "S4"), run(day, "Base")
    fid = next(fid for fid, f in sorted(s4["flights"].items(),
                                         key=lambda item: item[1]["request_s"])
               if f["state"] == "diverted" and base["flights"][fid]["state"] == "departed")
    t = s4["flights"][fid]["request_s"]
    end = t + WINDOW // 1000
    lines = [
        "# D4.6 — Traço de eventos: chegada bloqueada por falta de stand",
        "",
        f"Dia `{args.day.name}` (semente {day['seed']}), família de referência, FCFS. "
        f"Pedido **{fid}** em t = {t} s; janela de toque até t + 300 s = {end} s.",
        "Gerado por `scripts/d4_traco.py`; tempos em segundos desde a abertura.",
        "",
    ]
    for label, result in (("S4 (4 stands)", s4), ("Base (5 stands)", base)):
        f = result["flights"][fid]
        lines += [f"## {label}: {fid} → {f['state']}", "",
                  "| Stand | Voo que ocupa | Toque | Pronto para partir | Saída do stand |",
                  "|---:|---|---:|---:|---:|"]
        for key, holder, a, ready, b in stand_rows(result, t, end):
            mark = " **(este pedido)**" if holder == fid else ""
            lines.append(f"| {key} | {holder}{mark} | {a} | {ready or '—'} | {b} |")
        if f["state"] == "diverted":
            lines.append("")
            lines.append(f"Todos os stands seguem ocupados até {end} s; a aeronave desvia em "
                         f"{f['diverted_s']} s e os passageiros do voo são avisados nesse instante.")
        else:
            lines.append("")
            lines.append(f"Toque em {f['touchdown_s']} s no stand {f['stand']}; decolagem em "
                         f"{f['liftoff_s']} s, com {f['boarded']} passageiro(s).")
        lines.append("")
    lines.append("Mecanismo: com 4 stands, os ciclos com recarga de 30 min mantêm "
                 "todas as posições ocupadas durante a janela de 300 s; o quinto stand absorve o "
                 "pedido. É o bloqueio de chegada por estacionamento cheio discutido por Onat et "
                 "al. (D001), aqui medido no cenário sintético.")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()
