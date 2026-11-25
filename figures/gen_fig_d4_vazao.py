"""Figura D4: decolagens com passageiros por hora segundo a demanda, na configuração-base.

Fonte: data/d4/resumo_celulas_d4_5.csv (média e IC t de 95%, 30 réplicas).
Gráfico de linhas: a demanda é um eixo ordenado e as duas políticas são comparadas
no mesmo dia oferecido. Saída: figures/fig_d4_vazao_demanda.{pdf,png}.
"""

import matplotlib.pyplot as plt

from estilo_d4 import (CELLS, POLICY, POLICY_EN, TEXT_WIDTH_IN, apply_style, cells, comma,
                       estimate, language, save, suffix)

FAMILIES = (("demanda_baixa", 4), ("referencia", 6), ("demanda_alta", 8))
OFFSET = {"fcfs": -0.06, "agenda": 0.06}   # afasta as barras de erro sobrepostas


TEXT = {
    "pt": {"x": "Taxa nominal de pedidos no período de oferta (pedidos/h)",
           "y": "Decolagens com passageiros (h$^{-1}$)",
           "title": "Vazão por demanda na configuração-base"},
    "en": {"x": "Nominal request rate during the offer period (requests/h)",
           "y": "Passenger departures (h$^{-1}$)",
           "title": "Throughput by demand in the Base configuration"},
}


def main():
    lang = language()
    text = TEXT[lang]
    apply_style()
    index = cells()
    fig, ax = plt.subplots(figsize=(TEXT_WIDTH_IN, 2.6))
    for policy, style in POLICY.items():
        rates, means, low, high = [], [], [], []
        for family, rate in FAMILIES:
            mean, lo, hi = estimate(index[(family, "Base", policy, "departures_per_h")])
            rates.append(rate + OFFSET[policy])
            means.append(mean)
            low.append(mean - lo)
            high.append(hi - mean)
        ax.errorbar(rates, means, yerr=[low, high],
                    label=style["label"] if lang == "pt" else POLICY_EN[policy],
                    color=style["color"], marker=style["marker"],
                    linestyle=style["linestyle"], capsize=3, elinewidth=1, zorder=3)
    ax.set_xticks([rate for _, rate in FAMILIES])
    ax.set_xlabel(text["x"])
    ax.set_ylabel(text["y"])
    ax.yaxis.set_major_formatter(comma(1, lang))
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper left")
    save(fig, "fig_d4_vazao_demanda" + suffix(lang), text["title"],
         f"Fonte: {CELLS.relative_to(CELLS.parents[2])}; média e IC t de 95%, n = 30")


if __name__ == "__main__":
    main()
