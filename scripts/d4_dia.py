"""Gera o dia oferecido da D4 (especificação D4.1 v2.1) antes de qualquer política.

Um dia contém os pedidos a 8/h e, para cada pedido, uma marca de afinamento e as
reservas com ausência, antecedência de chegada e duração da bagagem. Tudo é
sorteado antes da admissão, vinculado ao pedido e ao passageiro. Por isso, uma
recusa não desloca os sorteios seguintes e as famílias de 4, 6 e 8 pedidos/h
compartilham os mesmos pedidos (afinamento por marca).

Cada fonte de acaso tem um gerador próprio, semeado por texto (seed/fonte).
Só se usa `random()`; as transformações são explícitas, para que o mesmo
número de semente gere o mesmo dia em outras versões do Python.

Uso: python d4_dia.py --seed 1 --out data/d4/dias/dia_0001.json
"""

import argparse
import json
import math
import random
from decimal import ROUND_HALF_EVEN, Decimal
from pathlib import Path

GENERATOR_VERSION = "d4_dia 1.1 (D4.1 v2.3)"
MS = Decimal("0.001")

# Valores e procedência conforme data/parameter_registry.csv.
PARAMS = {
    "horizon_s": {"value": 28800, "source": "PAR-050"},
    "first_request_s": {"value": 2700, "source": "PAR-051 (oferta a partir de 2700 s)"},
    "base_rate_per_h": {"value": 8, "source": "PAR-051 (fluxo comum a 8/h, afinado)"},
    "reserved_seats": {"value": [1, 4], "source": "PAR-052 (uniforme discreta)"},
    "absence_probability": {"value": 0.10, "source": "PAR-053"},
    "arrival_lead_s": {"value": [900, 3600],
                       "source": "PAR-054 (Feldhoff 2022; forma uniforme SUPOSTA)"},
    "bag_service_s": {"value": [30, 60], "source": "PAR-028"},
    "std_offset_s": {"value": 900, "source": "PAR-056 (STD = t + 900 s + recarga)"},
    "manifest_close_s": {"value": -900, "source": "PAR-059 (relativo à STD)"},
}
HORIZON_S = PARAMS["horizon_s"]["value"]
FIRST_REQUEST_S = PARAMS["first_request_s"]["value"]
BASE_RATE = PARAMS["base_rate_per_h"]["value"]
CHARGES_MIN = (0, 30, 60)  # PAR-002


def ms(value):
    return Decimal(repr(value)).quantize(MS, rounding=ROUND_HALF_EVEN)


def uniform_ms(rng, low, high):
    return ms(low + (high - low) * rng.random())


def streams(seed):
    # counter_service e security_service (v1.1): uniformes por reserva para a família de
    # serviço variável. Correntes próprias, então os demais sorteios não mudam.
    names = ("requests", "marks", "seats", "absence", "lead", "bag",
             "counter_service", "security_service")
    return {name: random.Random(f"{seed}/{name}") for name in names}


def generate_day(seed):
    if type(seed) is not int or seed < 0:
        raise ValueError("seed must be a nonnegative integer")
    rng = streams(seed)
    seats_low, seats_high = PARAMS["reserved_seats"]["value"]
    lead_low, lead_high = PARAMS["arrival_lead_s"]["value"]
    bag_low, bag_high = PARAMS["bag_service_s"]["value"]
    p_absent = PARAMS["absence_probability"]["value"]
    mean_gap = 3600 / BASE_RATE

    requests = []
    t = Decimal(FIRST_REQUEST_S)
    while True:
        # Poisson homogêneo: intervalos exponenciais pela inversa da distribuição.
        t += ms(-math.log(1.0 - rng["requests"].random()) * mean_gap)
        if t >= HORIZON_S:
            break
        key = f"R{len(requests) + 1:04d}"
        n = seats_low + int(rng["seats"].random() * (seats_high - seats_low + 1))
        reservations = [{
            "id": f"{key}-P{k}",
            "absent": rng["absence"].random() < p_absent,
            "lead_s": uniform_ms(rng["lead"], lead_low, lead_high),
            "bag_s": uniform_ms(rng["bag"], bag_low, bag_high),
            "counter_u": rng["counter_service"].random(),
            "security_u": rng["security_service"].random(),
        } for k in range(1, n + 1)]
        requests.append({"id": key, "request_s": t, "mark": rng["marks"].random(),
                         "reservations": reservations})
    return {"seed": seed, "generator_version": GENERATOR_VERSION, "params": PARAMS,
            "requests": requests}


def exponential_ms(mean_s, u):
    """Duração exponencial com a média dada, pela inversa da distribuição (SUPOSTA, PAR-063)."""
    return ms(-math.log(1.0 - u) * mean_s)


def family_requests(day, rate_per_h, charge_min, variable_service=False):
    """Pedidos de uma família: afinamento por marca e horários relativos à STD.

    Com variable_service, balcão e inspeção usam durações exponenciais com as médias
    declaradas (180 s e 90 s), sorteadas por passageiro antes da política (PAR-063).
    Sem ele, as durações são as constantes de PAR-046 e PAR-047.
    """
    if not 0 < rate_per_h <= BASE_RATE:
        raise ValueError(f"rate must be in (0, {BASE_RATE}] requests/h")
    if charge_min not in CHARGES_MIN:
        raise ValueError(f"declared charge must be one of {CHARGES_MIN} min")
    keep = Decimal(rate_per_h) / Decimal(BASE_RATE)
    rows = []
    for r in day["requests"]:
        if Decimal(repr(r["mark"])) >= keep:
            continue
        std = r["request_s"] + PARAMS["std_offset_s"]["value"] + 60 * charge_min
        rows.append({
            "id": r["id"],
            "request_s": r["request_s"],
            "target_departure_s": std,
            "manifest_close_s": std + PARAMS["manifest_close_s"]["value"],
            "declared_charge_min": charge_min,
            "manifest": [{"id": p["id"],
                          "arrival_s": None if p["absent"] else std - p["lead_s"],
                          "bag_service_s": p["bag_s"],
                          "counter_service_s": (exponential_ms(180, p["counter_u"])
                                                if variable_service else None),
                          "security_service_s": (exponential_ms(90, p["security_u"])
                                                 if variable_service else None)}
                         for p in r["reservations"]],
        })
    return rows


def save_day(day, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(day, default=float, indent=1, ensure_ascii=False) + "\n",
                    encoding="utf-8")


def load_day(path):
    day = json.loads(Path(path).read_text(encoding="utf-8"), parse_float=Decimal)
    for r in day["requests"]:
        r["request_s"] = Decimal(r["request_s"])
        r["mark"] = float(r["mark"])
        for p in r["reservations"]:
            p["lead_s"], p["bag_s"] = Decimal(p["lead_s"]), Decimal(p["bag_s"])
            p["counter_u"], p["security_u"] = float(p["counter_u"]), float(p["security_u"])
    day["params"]["absence_probability"]["value"] = float(
        day["params"]["absence_probability"]["value"])
    return day


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    day = generate_day(args.seed)
    save_day(day, args.out)
    print(f"{args.out}: {len(day['requests'])} pedidos a {BASE_RATE}/h, semente {args.seed}")
