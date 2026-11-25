"""Gera a figura D4 de vazão por demanda a partir do resumo arquivado."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "d4" / "resumo_celulas_d4_5.csv"
OUTPUT = ROOT / "figures" / "fig_d4_vazao_demanda"
FAMILIES = (("demanda_baixa", 4), ("referencia", 6), ("demanda_alta", 8))
STYLES = {
    "fcfs": {"label": "FCFS local", "color": "#0072B2", "marker": "o", "linestyle": "-"},
    "agenda": {"label": "Admissão antecipada", "color": "#D55E00", "marker": "s",
               "linestyle": "--"},
}


def load():
    with SOURCE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    indexed = {(row["family"], row["config"], row["policy"], row["metric"]): row
               for row in rows}
    data = {}
    for policy in STYLES:
        values = []
        for family, rate in FAMILIES:
            row = indexed[(family, "Base", policy, "departures_per_h")]
            values.append((rate, float(row["mean"]), float(row["ci_low"]),
                           float(row["ci_high"])))
        data[policy] = values
    return data


def main():
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 10,
        "axes.labelsize": 10,
        "legend.fontsize": 9,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "axes.spines.top": False,
        "axes.spines.right": False,
    })
    fig, ax = plt.subplots(figsize=(6.75, 3.1))
    for policy, values in load().items():
        style = STYLES[policy]
        x = [item[0] for item in values]
        mean = [item[1] for item in values]
        low = [item[2] for item in values]
        high = [item[3] for item in values]
        errors = [[m - lo for m, lo in zip(mean, low)],
                  [hi - m for m, hi in zip(mean, high)]]
        ax.errorbar(x, mean, yerr=errors, label=style["label"], color=style["color"],
                    marker=style["marker"], linestyle=style["linestyle"], linewidth=1.8,
                    markersize=5, capsize=3, zorder=3)
    ax.set_xlabel("Taxa nominal de pedidos no período de oferta (pedidos/h)")
    ax.set_ylabel("Decolagens com passageiros (h$^{-1}$)")
    ax.set_xticks([4, 6, 8])
    ax.grid(axis="y", alpha=0.25, linestyle="--", linewidth=0.6)
    ax.legend(frameon=False, loc="upper left")
    fig.savefig(OUTPUT.with_suffix(".pdf"), metadata={
        "Title": "Vazão por demanda na configuração-base",
        "Subject": "Fonte: data/d4/resumo_celulas_d4_5.csv; média e IC t de 95%, n=30",
    })
    fig.savefig(OUTPUT.with_suffix(".png"), dpi=300)
    plt.close(fig)
    print(f"{OUTPUT.with_suffix('.pdf')} e {OUTPUT.with_suffix('.png')}")


if __name__ == "__main__":
    main()
