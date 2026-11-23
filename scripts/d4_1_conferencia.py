"""Confere, com o simulador da Fase D, as durações usadas nas estimativas da D4.1 v2.1.

Roda um voo isolado por combinação de recarga (0, 30, 60 min) e grupo (1 a 4
passageiros), sem fila e sem acaso, e compara com as fórmulas da especificação:

    ocupação do stand   = 146,5 + R + 124,6 n
    toque -> decolagem  = 279,8 + R + 124,6 n
    folga até a STD     = (t + 900 + R) - decolagem, com toque em t
    prontidão no terminal (1 passageiro, sem fila) = 180 + bagagem + 90

Uso: python scripts/d4_1_conferencia.py  (grava data/d4/conferencia_d4_1.csv)
"""

import copy
import csv
import json
import sys
import tempfile
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from phase_d import simulate  # noqa: E402

TEMPLATE = ROOT / "data/scenarios/phase_d_terminal_verification.json"
OUTPUT = ROOT / "data/d4/conferencia_d4_1.csv"
REQUEST_S = 2000          # pedido longe da abertura: grupo pronto antes da aeronave
BAG_S = 45                # média de PAR-028, para o teste de prontidão
STD_SLACK_S = 900         # PAR-056: STD = t + 900 + R

# Fórmulas da especificação (D4.1 v2.1), em segundos.
STAND_FIXED = Decimal("146.5")    # 27 + 65,8 + 26,7 + 27
TOUCH_TO_LIFT = Decimal("279.8")  # 37,7 + 22,8 + 146,5 + 22,8 + 50
PER_PAX = Decimal("124.6")        # 31,9 + 19,7 + 73


def one_flight(template, charge_min, n):
    scenario = copy.deepcopy(template)
    scenario["scenario_id"] = f"d4_1_check_R{charge_min}_n{n}"
    scenario["horizon_s"] = 20000
    request = copy.deepcopy(template["requests"][0])
    request.update(id="C1", request_s=REQUEST_S, manifest_close_s=REQUEST_S,
                   target_departure_s=REQUEST_S + STD_SLACK_S + 60 * charge_min,
                   window_s=[REQUEST_S, REQUEST_S], declared_charge_min=charge_min,
                   manifest=[{"id": f"P{i}", "arrival_s": 0, "bag_service_s": BAG_S}
                             for i in range(1, n + 1)])
    scenario["requests"] = [request]
    return scenario


def run(scenario):
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "scenario.json"
        path.write_text(json.dumps(scenario))
        return simulate(path, "scheduled")


def main():
    template = json.loads(TEMPLATE.read_text())
    rows = []
    for charge_min in (0, 30, 60):
        R = Decimal(60 * charge_min)
        for n in (1, 2, 3, 4):
            report = run(one_flight(template, charge_min, n))
            flight = next(d for d in report["simulated_departure_measurements"] if d["id"] == "C1")
            plan = next(q for q in report["requests"] if q["id"] == "C1")
            touchdown = Decimal(str(plan["planned_touchdown_s"]))
            liftoff = Decimal(str(flight["event_s"]["liftoff"]))
            stand = sum(Decimal(str(i["end_s"])) - Decimal(str(i["start_s"]))
                        for i in report["observed_resource_intervals"]
                        if i["id"] == "C1" and i["resource"] == "stand" and i["state"] == "occupied")
            rows.append({
                "recarga_min": charge_min, "passageiros": n,
                "stand_sim_s": stand, "stand_formula_s": STAND_FIXED + R + PER_PAX * n,
                "toque_decolagem_sim_s": liftoff - touchdown,
                "toque_decolagem_formula_s": TOUCH_TO_LIFT + R + PER_PAX * n,
                "folga_std_sim_s": REQUEST_S + STD_SLACK_S + R - liftoff,
                "folga_std_formula_s": STD_SLACK_S - TOUCH_TO_LIFT - PER_PAX * n,
                "toque_s": touchdown,
            })
    one = run(one_flight(template, 30, 1))
    ready = Decimal(str(next(p for p in one["passengers"] if p["id"] == "P1")["planned_terminal_ready_s"]))

    ok = all(r["stand_sim_s"] == r["stand_formula_s"]
             and r["toque_decolagem_sim_s"] == r["toque_decolagem_formula_s"]
             and r["folga_std_sim_s"] == r["folga_std_formula_s"]
             and r["toque_s"] == REQUEST_S for r in rows)
    ok_ready = ready == 180 + BAG_S + 90

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    for r in rows:
        print(r["recarga_min"], r["passageiros"], r["stand_sim_s"], r["toque_decolagem_sim_s"],
              r["folga_std_sim_s"])
    print(f"prontidão no terminal (1 passageiro, bagagem {BAG_S} s): {ready} s")
    print("CONFERE" if ok and ok_ready else "DIVERGE")
    return 0 if ok and ok_ready else 1


if __name__ == "__main__":
    sys.exit(main())
