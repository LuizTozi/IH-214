"""Figura D4: decolagens com passageiros por hora segundo a demanda, Base (5 stands)
contra S4 (4 stands), um painel por política.

Fonte: data/d4/resumo_celulas_d4_5.csv (média e IC t de 95%, 30 réplicas).
Gráfico de linhas: a demanda é um eixo ordenado; a distância entre as linhas é o
ganho do quinto stand, que cresce com a demanda.
Uso: python gen_fig_d4_vazao.py [--lang en]
Saída: figures/fig_d4_vazao_demanda{,_en}.{pdf,png}.
"""

import matplotlib.pyplot as plt

from estilo_d4 import (BLUE, CELLS, ORANGE, TEXT_WIDTH_IN, apply_style, cells, comma, estimate,
                       language, save, suffix)

FAMILIES = (("demanda_baixa", 4), ("referencia", 6), ("demanda_alta", 8))
CONFIG = {"Base": {"color": BLUE, "marker": "o", "linestyle": "-", "offset": -0.06},
          "S4": {"color": ORANGE, "marker": "s", "linestyle": "--", "offset": 0.06}}
TEXT = {
    "pt": {"x": "Taxa nominal de pedidos (pedidos/h)",
           "y": "Decolagens com passageiros (h$^{-1}$)",
           "labels": {"Base": "5 stands (Base)", "S4": "4 stands (S4)"},
           "panels": {"fcfs": "(a) FCFS local", "agenda": "(b) Admissão antecipada"},
           "title": "Vazão por demanda: 5 contra 4 stands"},
    "en": {"x": "Nominal request rate (requests/h)",
           "y": "Passenger departures (h$^{-1}$)",
           "labels": {"Base": "5 stands (Base)", "S4": "4 stands (S4)"},
           "panels": {"fcfs": "(a) Local FCFS", "agenda": "(b) Advance admission"},
           "title": "Throughput by demand: 5 versus 4 stands"},
}


def main():
    lang = language()
    text = TEXT[lang]
    apply_style()
    index = cells()
    fig, axes = plt.subplots(1, 2, figsize=(TEXT_WIDTH_IN, 2.6), sharey=True)
    for ax, policy in zip(axes, ("fcfs", "agenda")):
        for config, style in CONFIG.items():
            rates, means, low, high = [], [], [], []
            for family, rate in FAMILIES:
                mean, lo, hi = estimate(index[(family, config, policy, "departures_per_h")])
                rates.append(rate + style["offset"])
                means.append(mean)
                low.append(mean - lo)
                high.append(hi - mean)
            ax.errorbar(rates, means, yerr=[low, high], label=text["labels"][config],
                        color=style["color"], marker=style["marker"],
                        linestyle=style["linestyle"], capsize=3, elinewidth=1, zorder=3)
        ax.set_xticks([rate for _, rate in FAMILIES])
        ax.set_xlabel(text["x"])
        ax.set_title(text["panels"][policy], loc="left")
        ax.yaxis.set_major_formatter(comma(1, lang))
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel(text["y"])
    axes[0].legend(loc="upper left")
    fig.tight_layout()
    save(fig, "fig_d4_vazao_demanda" + suffix(lang), text["title"],
         f"Fonte: {CELLS.relative_to(CELLS.parents[2])}; média e IC t de 95%, n = 30")


if __name__ == "__main__":
    main()
