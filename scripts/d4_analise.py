"""Resume as rodadas definitivas D4.4 e calcula contrastes pareados da D4.5 (D4.1 v2.2).

Saídas:
- resumo longo das células, com IC t de 95% entre réplicas e denominadores;
- contrastes de política e recursos em cada família não perfeita;
- contrastes da informação perfeita contra sua família-controle;
- síntese em Markdown cujos números vêm todos das tabelas acima.

Classificação (D4.1, "Contrastes principais e exploratórios"): só a família de
referência tem contrastes principais; famílias de sensibilidade são exploratórias.
"""

import argparse
import csv
import math
import statistics
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REFERENCE = "referencia"
REGULAR_FAMILIES = ("referencia", "demanda_baixa", "demanda_alta", "sem_recarga",
                    "recarga_longa")
PERFECT_CONTROLS = {
    "info_perfeita": "referencia",
    "info_perfeita_sem_recarga": "sem_recarga",
}
CONFIGS = ("Base", "S4", "B2")
POLICIES = ("fcfs", "agenda")

# Quantis t bilaterais de 95%, graus de liberdade 1--30.
T_975 = (None, 12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262,
         2.228, 2.201, 2.179, 2.160, 2.145, 2.131, 2.120, 2.110, 2.101, 2.093,
         2.086, 2.080, 2.074, 2.069, 2.064, 2.060, 2.056, 2.052, 2.048, 2.045,
         2.042)

# métrica: denominador da média condicional dentro da réplica (None = contagem ou taxa)
CELL_METRICS = {
    "offered": None,
    "cancelled_empty": None,
    "refused": None,
    "diverted": None,
    "departed": None,
    "departed_empty": None,
    "pending": None,
    "departures_per_h": None,          # VAR-016: só voos com passageiros
    "liftoffs_per_h": None,            # todas as decolagens, inclusive vazias
    "coverage_offered": "offered",     # voos com passageiros / pedidos oferecidos
    "punctual_fraction": "departed",
    "mean_lateness_s": "departed",
    "retained_fraction": "carrying_departed",
    "mean_await_s": "carrying_departed",
    "mean_stand_blocked_s": "departed",
    "post_security_mean_s": "boarded_passengers",
    "post_security_p95_s": "boarded_passengers",
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


def carrying(row):
    return float(row["departed"]) - float(row["departed_empty"])


def ratio(numerator, denominator):
    return numerator / denominator if denominator else None


def numeric(row, metric):
    if metric == "coverage_offered":
        return carrying(row) / float(row["offered"])
    if metric == "punctual_fraction":
        return ratio(float(row["punctual"]), float(row["departed"]))
    if metric == "retained_fraction":
        return ratio(float(row["retained_flights"]), carrying(row))
    if metric == "counter_within_limit_fraction":
        return ratio(float(row["counter_within_limit"]), float(row["counter_complete"]))
    if metric == "security_within_limit_fraction":
        return ratio(float(row["security_within_limit"]), float(row["security_complete"]))
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
        return int(carrying(row))
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


def classification(family, primary):
    return "primary" if family == REFERENCE and primary else "exploratory"


def contrast_summaries(rows, version):
    indexed = index_rows(rows)
    seeds = sorted({int(row["seed"]) for row in rows})
    output = []

    def add(scope, family, name, direction, metric, a, b, label):
        stats = contrast(indexed, seeds, *a, *b, metric)
        output.append({
            "analysis_version": version,
            "scope": scope,
            "family": family,
            "contrast": name,
            "direction": direction,
            "metric": metric,
            "classification": label,
            **stats,
        })

    for family in REGULAR_FAMILIES:
        for config in CONFIGS:
            add("policy", family, f"policy_{config}", "agenda - FCFS", "departures_per_h",
                (family, config, "agenda"), (family, config, "fcfs"),
                classification(family, config == "Base"))
        for policy in POLICIES:
            add("stands", family, f"stands_{policy}", "Base - S4", "departures_per_h",
                (family, "Base", policy), (family, "S4", policy),
                classification(family, True))
            add("counter", family, f"counter_{policy}", "B2 - Base", "counter_mean_wait_s",
                (family, "B2", policy), (family, "Base", policy),
                classification(family, True))
            add("counter_los", family, f"counter_los_{policy}", "B2 - Base",
                "counter_within_limit_fraction", (family, "B2", policy),
                (family, "Base", policy), "exploratory")
            # Para onde vai a espera poupada no balcão: sala de embarque (VAR-045).
            add("lounge", family, f"lounge_{policy}", "B2 - Base", "post_security_mean_s",
                (family, "B2", policy), (family, "Base", policy), "exploratory")

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


def fmt(value, digits):
    return "—" if value is None else f"{value:.{digits}f}"


def write_report(cells, contrasts, path, source):
    cell_index = {(row["family"], row["config"], row["policy"], row["metric"]): row
                  for row in cells}
    contrast_index = {(row["family"], row["contrast"], row["metric"]): row
                      for row in contrasts}

    def effect(family, name, metric, digits=3):
        row = contrast_index[(family, name, metric)]
        if row["sd"] in (None, "") or float(row["sd"]) == 0:
            return f"{fmt(float(row['mean']), digits)} (sem variação entre réplicas)"
        return (f"{fmt(float(row['mean']), digits)} "
                f"[{fmt(float(row['ci_low']), digits)}; {fmt(float(row['ci_high']), digits)}]")

    def value(family, config, policy, metric, digits=3):
        row = cell_index[(family, config, policy, metric)]
        if row["mean"] in (None, ""):
            return "—"
        if row["ci_low"] in (None, ""):
            return fmt(float(row["mean"]), digits)
        return (f"{fmt(float(row['mean']), digits)} "
                f"[{fmt(float(row['ci_low']), digits)}; {fmt(float(row['ci_high']), digits)}]")

    def total(family, config, policy, metric):
        return int(cell_index[(family, config, policy, metric)]["denominator_total"])

    version = contrasts[0]["analysis_version"]
    lines = [
        "# D4.5 — Síntese reproduzível dos contrastes (D4.1 v2.2)",
        "",
        f"Fonte: `{source}`. Analisador: `{version}`. Cada estimativa usa as réplicas",
        "independentes válidas; as diferenças são calculadas dentro da réplica e resumidas por",
        "média e intervalo t bilateral de 95%. Proporções são médias das razões por réplica.",
        "Todos os números desta síntese vêm de `resumo_celulas_d4_5.csv` e",
        "`contrastes_d4_5.csv`.",
        "",
        "## Contrastes principais na família de referência",
        "",
        "| Contraste (sentido) | Política | Média [IC 95%] | Unidade |",
        "|---|---|---:|---|",
        f"| Agenda − FCFS, Base | — | {effect(REFERENCE, 'policy_Base', 'departures_per_h')} | decolagens com passageiros/h |",
        f"| Base − S4 | FCFS | {effect(REFERENCE, 'stands_fcfs', 'departures_per_h')} | decolagens com passageiros/h |",
        f"| Base − S4 | Agenda | {effect(REFERENCE, 'stands_agenda', 'departures_per_h')} | decolagens com passageiros/h |",
        f"| B2 − Base | FCFS | {effect(REFERENCE, 'counter_fcfs', 'counter_mean_wait_s', 1)} | s |",
        f"| B2 − Base | Agenda | {effect(REFERENCE, 'counter_agenda', 'counter_mean_wait_s', 1)} | s |",
        "",
        "## Balanço e mecanismos por demanda na configuração-base",
        "",
        "| Indicador por réplica | Política | 4 pedidos/h | 6 pedidos/h | 8 pedidos/h |",
        "|---|---|---:|---:|---:|",
    ]
    demand = ("demanda_baixa", REFERENCE, "demanda_alta")
    for label, metric, digits in (
        ("Pedidos oferecidos", "offered", 2),
        ("Recusados", "refused", 2),
        ("Desviados", "diverted", 2),
        ("Decolados com passageiros (vazios à parte)", "departures_per_h", 3),
        ("Decolagens vazias", "departed_empty", 2),
        ("Pendentes no horizonte", "pending", 2),
        ("Cobertura dos oferecidos", "coverage_offered", 3),
        ("Espera média no balcão (s)", "counter_mean_wait_s", 1),
        ("Conformidade ao limite do balcão (180 s)", "counter_within_limit_fraction", 3),
        ("Fração retida pelo grupo", "retained_fraction", 3),
        ("Espera após a inspeção, média (s)", "post_security_mean_s", 1),
        ("Bloqueio do stand após prontidão (s)", "mean_stand_blocked_s", 1),
    ):
        for policy in POLICIES:
            cols = " | ".join(value(f, "Base", policy, metric, digits) for f in demand)
            lines.append(f"| {label} | {policy.upper() if policy == 'fcfs' else 'Agenda'} | {cols} |")

    lines.extend([
        "",
        "A linha de decolados com passageiros está em decolagens/h (VAR-016).",
        "",
        "## Terminal: Base e B2 na referência",
        "",
        "| Indicador por réplica | Base FCFS | B2 FCFS | Base agenda | B2 agenda |",
        "|---|---:|---:|---:|---:|",
    ])
    for label, metric, digits in (
        ("Espera média no balcão (s)", "counter_mean_wait_s", 1),
        ("P95 da espera no balcão (s)", "counter_p95_wait_s", 1),
        ("Conformidade ao limite do balcão", "counter_within_limit_fraction", 3),
        ("Espera média na bagagem (s)", "baggage_mean_wait_s", 1),
        ("Espera média na inspeção (s)", "security_mean_wait_s", 1),
        ("Espera após a inspeção, média (s)", "post_security_mean_s", 1),
        ("Espera após a inspeção, P95 (s)", "post_security_p95_s", 1),
        ("Fração retida pelo grupo", "retained_fraction", 3),
    ):
        cols = " | ".join(value(REFERENCE, c, p, metric, digits)
                          for p in POLICIES for c in ("Base", "B2"))
        lines.append(f"| {label} | {cols} |")
    lines.extend([
        "",
        "Contrastes pareados B2 − Base (exploratórios): conformidade ao limite do balcão "
        f"{effect(REFERENCE, 'counter_los_fcfs', 'counter_within_limit_fraction')} (FCFS) e "
        f"{effect(REFERENCE, 'counter_los_agenda', 'counter_within_limit_fraction')} (agenda); "
        "espera média após a inspeção "
        f"{effect(REFERENCE, 'lounge_fcfs', 'post_security_mean_s', 1)} s (FCFS) e "
        f"{effect(REFERENCE, 'lounge_agenda', 'post_security_mean_s', 1)} s (agenda).",
        "",
        "Denominadores totais (30 réplicas): espera no balcão "
        + ", ".join(f"{c} {p.upper() if p == 'fcfs' else 'agenda'} "
                    f"{total(REFERENCE, c, p, 'counter_mean_wait_s'):,}".replace(",", ".")
                    for p in POLICIES for c in ("Base", "B2"))
        + "; voos com passageiros "
        + ", ".join(f"{c} {p.upper() if p == 'fcfs' else 'agenda'} "
                    f"{total(REFERENCE, c, p, 'retained_fraction'):,}".replace(",", ".")
                    for p in POLICIES for c in ("Base", "B2"))
        + ".",
        "",
        "## Sensibilidade do contraste de política na Base (exploratória)",
        "",
        "| Família | Agenda − FCFS, decolagens com passageiros/h: média [IC 95%] |",
        "|---|---:|",
    ])
    for family, label in (
        ("demanda_baixa", "4 pedidos/h"),
        (REFERENCE, "6 pedidos/h, recarga 30 min (principal)"),
        ("demanda_alta", "8 pedidos/h"),
        ("sem_recarga", "6 pedidos/h, sem recarga"),
        ("recarga_longa", "6 pedidos/h, recarga 60 min"),
    ):
        lines.append(f"| {label} | {effect(family, 'policy_Base', 'departures_per_h')} |")

    lines.extend([
        "",
        "## Informação perfeita na agenda (exploratória)",
        "",
        "| Família e configuração | Perfeita − declarada, decolagens com passageiros/h | Recusas por réplica |",
        "|---|---:|---:|",
    ])
    for family, label in (("info_perfeita", "Recarga 30 min"),
                          ("info_perfeita_sem_recarga", "Sem recarga")):
        for config in CONFIGS:
            lines.append(
                f"| {label}, {config} | "
                f"{effect(family, f'information_{config}', 'departures_per_h')} | "
                f"{effect(family, f'information_{config}', 'refused', 2)} |"
            )
    lines.extend([
        "",
        "Os resultados são de um cenário sintético com chegadas uniformes supostas, serviços",
        "determinísticos no balcão e na inspeção, recursos vazios na abertura e horizonte",
        "terminante de 8 h. Médias de espera descrevem somente visitas com início observado e",
        "devem ser lidas junto às recusas, aos desvios, à censura e aos denominadores.",
        "",
    ])
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--cells-out", type=Path, required=True)
    parser.add_argument("--contrasts-out", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    rows = read_rows(args.input)
    version = analysis_version()
    cells = cell_summaries(rows, version)
    contrasts = contrast_summaries(rows, version)
    write_csv(cells, args.cells_out)
    write_csv(contrasts, args.contrasts_out)
    write_report(cells, contrasts, args.report, args.input)
    print(f"{args.cells_out}: {len(cells)} resumos; "
          f"{args.contrasts_out}: {len(contrasts)} contrastes")


if __name__ == "__main__":
    main()
