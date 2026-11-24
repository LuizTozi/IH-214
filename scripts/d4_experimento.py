"""Executa as células da D4 (D4.1 v2.1) e grava uma linha por família × configuração ×
política × réplica, com versão do código, semente e identificador do dia oferecido.

Cada réplica é um dia gerado por d4_dia a partir da semente; todas as células da
réplica usam o mesmo dia (pareamento). 48 execuções por réplica.

Uso: python d4_experimento.py --seeds 1 2 3 --out data/d4/resultados.csv \\
         [--days-dir data/d4/dias] [--families referencia demanda_alta]
"""

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path

from d4_dia import GENERATOR_VERSION, family_requests, generate_day, save_day
from d4_sim import run_cell

ROOT = Path(__file__).resolve().parent.parent

# família: (pedidos/h, recarga em min, informação perfeita)
FAMILIES = {
    "referencia": (6, 30, False),
    "demanda_baixa": (4, 30, False),
    "demanda_alta": (8, 30, False),
    "sem_recarga": (6, 0, False),
    "recarga_longa": (6, 60, False),
    "info_perfeita": (6, 30, True),
    "info_perfeita_sem_recarga": (6, 0, True),
}
ONE = {"counter": 1, "baggage": 1, "security": 1}
# configuração: (stands, servidores por estação)
CONFIGS = {
    "Base": (5, ONE),
    "S4": (4, ONE),
    "B2": (5, {**ONE, "counter": 2}),
    "I2": (5, {**ONE, "security": 2}),
}


def cells(families=None):
    selected = FAMILIES if families is None else families
    unknown = set(selected) - set(FAMILIES)
    if unknown:
        raise ValueError(f"unknown families: {sorted(unknown)}")
    for family, (rate, charge, perfect) in FAMILIES.items():
        if family not in selected:
            continue
        for config in CONFIGS:
            for policy in (("agenda",) if perfect else ("fcfs", "agenda")):
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
            rate, charge, perfect = FAMILIES[family]
            stands, servers = CONFIGS[config]
            result = run_cell(family_requests(day, rate, charge), servers, stands, policy, perfect)
            rows.append({"seed": seed, "day_id": ident, "family": family, "config": config,
                         "policy": policy, "perfect": perfect, "rate_per_h": rate,
                         "charge_min": charge, "n_stands": stands,
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
