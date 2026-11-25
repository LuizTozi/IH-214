"""Executa as células da D4 (D4.1 v2.1) e grava uma linha por família × configuração ×
política × réplica, com versão do código, semente e identificador do dia oferecido.

Cada réplica é um dia gerado por d4_dia a partir da semente; todas as células da
réplica usam o mesmo dia (pareamento). 66 execuções por réplica (D4.1 v2.4).

Uso: python d4_experimento.py --seeds 1 2 3 --out data/d4/resultados.csv \\
         [--days-dir data/d4/dias] [--families referencia demanda_alta]
"""

import argparse
import csv
import hashlib
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

from d4_dia import GENERATOR_VERSION, family_requests, generate_day, save_day
from d4_sim import run_cell

ROOT = Path(__file__).resolve().parent.parent

@dataclass(frozen=True)
class Family:
    rate: int = 6
    charge: int = 30
    absence: float = 0.0
    arrival: str = "fc_morning"
    window_s: int = 300
    std_offset_s: int = 900


FAMILIES = {
    "referencia": Family(),
    "demanda_baixa": Family(rate=4),
    "demanda_alta": Family(rate=8),
    "sem_recarga": Family(charge=0),
    "recarga_longa": Family(charge=60),
    "ausencia_15": Family(absence=0.15),
    "chegada_lcc_tarde": Family(arrival="lcc_afternoon"),
    "janela_150": Family(window_s=150),
    "janela_600": Family(window_s=600),
    "partida_600": Family(std_offset_s=600),
    "partida_1200": Family(std_offset_s=1200),
}
ONE = {"counter": 1, "baggage": 1, "security": 1}
# configuração: (stands, servidores por estação)
# I2 (segundo posto de inspeção) saiu na D4.1 v2.2: com balcão determinístico de 180 s
# e inspeção de 90 s, nunca há fila na inspeção com um balcão, e I2 reproduzia a Base
# em todas as colunas (D4.4 v1, 360 de 360 linhas). Ver deliverables/D4_1_cenarios.md.
CONFIGS = {
    "Base": (5, ONE),
    "S4": (4, ONE),
    "B2": (5, {**ONE, "counter": 2}),
}


def cells(families=None):
    selected = FAMILIES if families is None else families
    unknown = set(selected) - set(FAMILIES)
    if unknown:
        raise ValueError(f"unknown families: {sorted(unknown)}")
    for family in FAMILIES:
        if family not in selected:
            continue
        for config in CONFIGS:
            for policy in ("fcfs", "agenda"):
                yield family, config, policy


def code_version():
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", "scripts"], cwd=ROOT,
                           check=True, capture_output=True, text=True).stdout.strip()
    return head + ("-modificado" if dirty else "")


def day_id(day):
    text = json.dumps(day, default=float, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def flatten(result):
    row = dict(result["metrics"])
    for station, values in result["summary"].items():
        for key, value in values.items():
            row[f"{station}_{key}"] = value
    return row


def run(seeds, out, days_dir=None, families=None):
    version = code_version()
    rows = []
    for seed in seeds:
        day = generate_day(seed)
        ident = day_id(day)
        if days_dir is not None:
            save_day(day, Path(days_dir) / f"dia_{seed:04d}.json")
        for family, config, policy in cells(families):
            spec = FAMILIES[family]
            stands, servers = CONFIGS[config]
            requests = family_requests(day, spec.rate, spec.charge, absence=spec.absence,
                                       arrival=spec.arrival, std_offset_s=spec.std_offset_s)
            result = run_cell(requests, servers, stands, policy, window_s=spec.window_s)
            rows.append({"seed": seed, "day_id": ident, "family": family, "config": config,
                         "policy": policy, "perfect": False, "rate_per_h": spec.rate,
                         "absence": spec.absence, "arrival": spec.arrival, "window_s": spec.window_s,
                         "std_offset_s": spec.std_offset_s, "charge_min": spec.charge, "n_stands": stands,
                         "counters": servers["counter"], "security_posts": servers["security"],
                         "code_version": version, "generator_version": GENERATOR_VERSION,
                         **flatten(result)})
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--seeds", type=int, nargs="+", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--days-dir", type=Path)
    parser.add_argument("--families", nargs="+", choices=FAMILIES)
    args = parser.parse_args()
    rows = run(args.seeds, args.out, args.days_dir, args.families)
    per_replication = len(list(cells(args.families)))
    print(f"{args.out}: {len(rows)} linhas "
          f"({len(args.seeds)} réplicas × {per_replication} células)")
