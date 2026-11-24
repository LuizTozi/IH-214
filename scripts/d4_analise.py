"""Resume as rodadas definitivas D4.4 e calcula contrastes pareados da D4.5.

Saídas:
- resumo longo das 48 células, com IC t de 95% entre réplicas e denominadores;
- contrastes de política e recursos em cada família não perfeita;
- contrastes da informação perfeita contra sua família-controle.
"""

import argparse
import csv
import math
import statistics
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REGULAR_FAMILIES = ("referencia", "demanda_baixa", "demanda_alta", "sem_recarga",
                    "recarga_longa")
PERFECT_CONTROLS = {
    "info_perfeita": "referencia",
    "info_perfeita_sem_recarga": "sem_recarga",
}
CONFIGS = ("Base", "S4", "B2", "I2")
POLICIES = ("fcfs", "agenda")

# Quantis t bilaterais de 95%, graus de liberdade 1--30.
T_975 = (None, 12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262,
         2.228, 2.201, 2.179, 2.160, 2.145, 2.131, 2.120, 2.110, 2.101, 2.093,
         2.086, 2.080, 2.074, 2.069, 2.064, 2.060, 2.056, 2.052, 2.048, 2.045,
         2.042)

CELL_METRICS = {
    "offered": None,
    "cancelled_empty": None,
    "refused": None,
    "diverted": None,
    "departed": None,
    "pending": None,
    "departures_per_h": None,
    "coverage_offered": "offered",
    "punctual_fraction": "departed",
    "mean_lateness_s": "departed",
    "retained_fraction": "carrying_departed",
    "mean_await_s": "carrying_departed",
    "mean_stand_blocked_s": "departed",
    "terminal_to_board_p95_s": "boarded_passengers",
    "utilization_tlof": None,
    "utilization_route": None,
    "utilization_stands": None,
    "held_stands": None,
    "counter_mean_wait_s": "counter_complete",
    "counter_p95_wait_s": "counter_complete",
    "counter_within_limit_fraction": "counter_complete",
    "counter_censored_at_horizon": None,
    "counter_left_refusal": None,
    "counter_left_diversion": None,
    "baggage_mean_wait_s": "baggage_complete",
    "baggage_p95_wait_s": "baggage_complete",
    "security_mean_wait_s": "security_complete",
    "security_p95_wait_s": "security_complete",
    "security_within_limit_fraction": "security_complete",
    "security_censored_at_horizon": None,
    "security_left_refusal": None,
    "security_left_diversion": None,
    "boarded_passengers": None,
    "lost_passengers": None,
}


def analysis_version():
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", "scripts"], cwd=ROOT,
                           check=True, capture_output=True, text=True).stdout.strip()
    return head + ("-modificado" if dirty else "")


def read_rows(path):
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def numeric(row, metric):
    if metric == "coverage_offered":
        return float(row["departed"]) / float(row["offered"])
    if metric == "punctual_fraction":
        denominator = float(row["departed"])
        return float(row["punctual"]) / denominator if denominator else None
    if metric == "retained_fraction":
        denominator = float(row["departed"]) - float(row["departed_empty"])
        return float(row["retained_flights"]) / denominator if denominator else None
    if metric == "counter_within_limit_fraction":
        denominator = float(row["counter_complete"])
        return float(row["counter_within_limit"]) / denominator if denominator else None
    if metric == "security_within_limit_fraction":
        denominator = float(row["security_complete"])
        return float(row["security_within_limit"]) / denominator if denominator else None
    raw = row[metric]
    return None if raw == "" else float(raw)


def ci(values):
    values = [value for value in values if value is not None]
    if not values:
        return {"n_valid": 0, "mean": None, "sd": None, "halfwidth_95": None,
                "ci_low": None, "ci_high": None}
    mean = statistics.mean(values)
    if len(values) == 1:
        return {"n_valid": 1, "mean": mean, "sd": None, "halfwidth_95": None,
                "ci_low": None, "ci_high": None}
    sd = statistics.stdev(values)
    df = len(values) - 1
    if df >= len(T_975):
        raise ValueError("t critical table supports at most 31 valid replications")
    halfwidth = T_975[df] * sd / math.sqrt(len(values))
    return {"n_valid": len(values), "mean": mean, "sd": sd,
            "halfwidth_95": halfwidth, "ci_low": mean - halfwidth,
            "ci_high": mean + halfwidth}


def denominator(row, name):
    if name is None:
        return None
    if name == "carrying_departed":
        return int(row["departed"]) - int(row["departed_empty"])
    return int(row[name])


def cell_summaries(rows, version):
    grouped = {}
    for row in rows:
        key = (row["family"], row["config"], row["policy"])
        grouped.setdefault(key, []).append(row)
    output = []
    for (family, config, policy), group in sorted(grouped.items()):
        for metric, denominator_name in CELL_METRICS.items():
            values = [numeric(row, metric) for row in group]
            stats = ci(values)
            denoms = ([denominator(row, denominator_name) for row in group]
                      if denominator_name else [])
            output.append({
                "analysis_version": version,
                "family": family,
                "config": config,
                "policy": policy,
                "metric": metric,
                **stats,
                "denominator_name": denominator_name or "replications",
                "denominator_total": sum(denoms) if denoms else len(group),
            })
    return output


def index_rows(rows):
    indexed = {}
    for row in rows:
        key = (int(row["seed"]), row["family"], row["config"], row["policy"])
        if key in indexed:
            raise ValueError(f"duplicate cell: {key}")
        indexed[key] = row
    return indexed


def contrast(indexed, seeds, family_a, config_a, policy_a, family_b, config_b, policy_b,
             metric):
    differences = []
    for seed in seeds:
        a = numeric(indexed[(seed, family_a, config_a, policy_a)], metric)
        b = numeric(indexed[(seed, family_b, config_b, policy_b)], metric)
        differences.append(None if a is None or b is None else a - b)
    return ci(differences)


def contrast_summaries(rows, version):
    indexed = index_rows(rows)
    seeds = sorted({int(row["seed"]) for row in rows})
    output = []

    def add(scope, family, name, direction, metric, a, b, classification):
        stats = contrast(indexed, seeds, *a, *b, metric)
        output.append({
            "analysis_version": version,
            "scope": scope,
            "family": family,
            "contrast": name,
            "direction": direction,
            "metric": metric,
            "classification": classification,
            **stats,
        })

    for family in REGULAR_FAMILIES:
        for config in CONFIGS:
            add("policy", family, f"policy_{config}", "agenda - FCFS", "departures_per_h",
                (family, config, "agenda"), (family, config, "fcfs"),
                "primary" if config == "Base" else "exploratory")
        for policy in POLICIES:
            add("stands", family, f"stands_{policy}", "Base - S4", "departures_per_h",
                (family, "Base", policy), (family, "S4", policy), "primary")
            add("counter", family, f"counter_{policy}", "B2 - Base", "counter_mean_wait_s",
                (family, "B2", policy), (family, "Base", policy), "primary")
            add("security", family, f"security_{policy}", "I2 - Base",
                "security_mean_wait_s", (family, "I2", policy),
                (family, "Base", policy), "primary")

    for perfect, control in PERFECT_CONTROLS.items():
        for config in CONFIGS:
            for metric in ("departures_per_h", "refused", "mean_await_s",
                           "mean_stand_blocked_s"):
                add("information", perfect, f"information_{config}",
                    "perfect - declared", metric, (perfect, config, "agenda"),
                    (control, config, "agenda"), "exploratory")
    return output


def write_csv(rows, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--cells-out", type=Path, required=True)
    parser.add_argument("--contrasts-out", type=Path, required=True)
    args = parser.parse_args()
    rows = read_rows(args.input)
    version = analysis_version()
    cells = cell_summaries(rows, version)
    contrasts = contrast_summaries(rows, version)
    write_csv(cells, args.cells_out)
    write_csv(contrasts, args.contrasts_out)
    print(f"{args.cells_out}: {len(cells)} resumos; "
          f"{args.contrasts_out}: {len(contrasts)} contrastes")


if __name__ == "__main__":
    main()
