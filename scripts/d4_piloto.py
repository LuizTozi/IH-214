"""Analisa o piloto de precisão da D4.3 a partir do CSV do experimento.

Calcula os sete contrastes pareados predefinidos em
data/d4/plano_piloto_d4_3.md e grava uma tabela reproduzível. O relatório em
Markdown é deliberadamente descritivo: o piloto dimensiona as rodadas finais
e não fornece os resultados substantivos do artigo.
"""

import argparse
import csv
import math
import statistics
from pathlib import Path


PILOT_REPLICATIONS = 30
T_975_DF29 = 2.045229642132703

CONTRASTS = (
    ("politica_base", "agenda - FCFS, Base", "departures_per_h", "agenda", "Base",
     "fcfs", "Base", 0.25, "decolagens/h"),
    ("stands_fcfs", "Base - S4, FCFS", "departures_per_h", "fcfs", "Base",
     "fcfs", "S4", 0.25, "decolagens/h"),
    ("stands_agenda", "Base - S4, agenda", "departures_per_h", "agenda", "Base",
     "agenda", "S4", 0.25, "decolagens/h"),
    ("balcao_fcfs", "B2 - Base, FCFS", "counter_mean_wait_s", "fcfs", "B2",
     "fcfs", "Base", 30.0, "s"),
    ("balcao_agenda", "B2 - Base, agenda", "counter_mean_wait_s", "agenda", "B2",
     "agenda", "Base", 30.0, "s"),
    ("inspecao_fcfs", "I2 - Base, FCFS", "security_mean_wait_s", "fcfs", "I2",
     "fcfs", "Base", 30.0, "s"),
    ("inspecao_agenda", "I2 - Base, agenda", "security_mean_wait_s", "agenda", "I2",
     "agenda", "Base", 30.0, "s"),
)


def read_rows(path):
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def paired_differences(rows):
    reference = [row for row in rows if row["family"] == "referencia"]
    by_seed = {}
    for row in reference:
        key = (row["policy"], row["config"])
        bucket = by_seed.setdefault(int(row["seed"]), {})
        if key in bucket:
            raise ValueError(f"duplicate cell for seed {row['seed']}: {key}")
        bucket[key] = row

    output = {definition[0]: [] for definition in CONTRASTS}
    for seed, cell_rows in sorted(by_seed.items()):
        for name, _, metric, policy_a, config_a, policy_b, config_b, _, _ in CONTRASTS:
            try:
                raw_a = cell_rows[(policy_a, config_a)][metric]
                raw_b = cell_rows[(policy_b, config_b)][metric]
            except KeyError as exc:
                raise ValueError(f"missing cell or metric for seed {seed}: {exc}") from exc
            if raw_a == "" or raw_b == "":
                continue
            output[name].append(float(raw_a) - float(raw_b))
    return output, len(by_seed)


def summarize(rows):
    differences, replications = paired_differences(rows)
    summaries = []
    for name, label, _, _, _, _, _, target, unit in CONTRASTS:
        values = differences[name]
        if len(values) < 2:
            raise ValueError(f"{name}: at least two valid pairs are required")
        sd = statistics.stdev(values)
        halfwidth = T_975_DF29 * sd / math.sqrt(len(values))
        required = max(2, math.ceil((T_975_DF29 * sd / target) ** 2))
        summaries.append({
            "contrast": name,
            "label": label,
            "unit": unit,
            "valid_pairs": len(values),
            "pilot_replications": replications,
            "mean_difference": statistics.mean(values),
            "sd_difference": sd,
            "pilot_halfwidth_95": halfwidth,
            "target_halfwidth": target,
            "required_replications": required,
        })
    return summaries


def write_csv(rows, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows, path, source):
    max_required = max(row["required_replications"] for row in rows)
    chosen = max(PILOT_REPLICATIONS, max_required)
    if PILOT_REPLICATIONS > max_required:
        limiting = (f"mínimo predefinido de {PILOT_REPLICATIONS} réplicas; o maior requisito "
                    f"estimado foi {max_required}")
    else:
        limiting = "; ".join(row["label"] for row in rows
                              if row["required_replications"] == max_required)
    lines = [
        "# D4.3 — Resultado do piloto de precisão",
        "",
        f"Fonte: `{source}`. Plano anterior aos dados: `data/d4/plano_piloto_d4_3.md`.",
        "",
        "O piloto serve apenas ao dimensionamento. Suas médias não serão combinadas com as rodadas",
        "definitivas nem tratadas como resultados do artigo.",
        "",
        "| Contraste | Pares | Média | DP pareado | Semilargura 95% | Alvo | n requerido |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['label']} | {row['valid_pairs']} | {row['mean_difference']:.3f} "
            f"{row['unit']} | {row['sd_difference']:.3f} | "
            f"{row['pilot_halfwidth_95']:.3f} | {row['target_halfwidth']:.3f} | "
            f"{row['required_replications']} |"
        )
    lines.extend([
        "",
        f"Número fixado para a D4.4: **{chosen} réplicas independentes**.",
        "",
        "Critério limitante: " + limiting + ".",
        "",
        "O cálculo usa `ceil((t_0.975,29 × s / h)^2)`, com diferenças dentro da réplica.",
        "A escolha é o maior requisito entre os contrastes e o mínimo de 30 réplicas.",
        "",
    ])
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    summaries = summarize(read_rows(args.input))
    write_csv(summaries, args.out)
    write_report(summaries, args.report, args.input)
    chosen = max(PILOT_REPLICATIONS, *(row["required_replications"] for row in summaries))
    print(f"{args.out}: {len(summaries)} contrastes; D4.4 = {chosen} réplicas")


if __name__ == "__main__":
    main()
