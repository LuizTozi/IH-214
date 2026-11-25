"""Figura D4: para onde vai a espera quando se acrescenta o segundo balcão (B2 contra Base).

Fonte: data/d4/resumo_celulas_d4_5.csv, família de referência. Barras: média por réplica;
barras de erro: IC t de 95% (n = 30). Painel (a): espera até o início do atendimento em
cada estação, entre visitas com início observado. Painel (b): espera do fim da inspeção ao
início do embarque (VAR-045), entre embarcados; inclui 51,6 s de caminhada e acesso.
As populações diferem entre painéis; as médias não se somam.
Saída: figures/fig_d4_espera.{pdf,png}.
"""

import matplotlib.pyplot as plt
import numpy as np

from estilo_d4 import (CELLS, GREEN, SKY, TEXT_WIDTH_IN, apply_style, cells, comma, estimate,
                       save)

REF = "referencia"
BARS = (  # (configuração, política, cor, hachura, rótulo)
    ("Base", "fcfs", SKY, "", "Base, FCFS"),
    ("B2", "fcfs", GREEN, "", "B2, FCFS"),
    ("Base", "agenda", SKY, "////", "Base, agenda"),
    ("B2", "agenda", GREEN, "////", "B2, agenda"),
)
STATIONS = (("Balcão", "counter_mean_wait_s"), ("Bagagem", "baggage_mean_wait_s"),
            ("Inspeção", "security_mean_wait_s"))
LOUNGE = (("Fim da inspeção\naté o embarque", "post_security_mean_s"),)


def bars(ax, groups, index, digits):
    width = 0.8 / len(BARS)
    x = np.arange(len(groups))
    for i, (config, policy, color, hatch, label) in enumerate(BARS):
        values = [estimate(index[(REF, config, policy, metric)]) for _, metric in groups]
        means = [m for m, _, _ in values]
        err = [[m - lo for m, lo, _ in values], [hi - m for m, _, hi in values]]
        ax.bar(x + (i - (len(BARS) - 1) / 2) * width, means, width * 0.92, yerr=err,
               color=color, hatch=hatch, edgecolor="white", linewidth=0.6, label=label,
               error_kw={"elinewidth": 0.9, "capsize": 2, "ecolor": "#333333"}, zorder=3)
        for xi, mean in zip(x + (i - (len(BARS) - 1) / 2) * width, means):
            if mean == 0:                       # sem fila: deixa o zero visível
                ax.text(xi, 0, "0", ha="center", va="bottom", fontsize=7, color="#555555")
    ax.set_xticks(x)
    ax.set_xticklabels([name for name, _ in groups])
    ax.yaxis.set_major_formatter(comma(digits))
    ax.grid(axis="x", visible=False)


def main():
    apply_style()
    plt.rcParams["hatch.color"] = "white"
    index = cells()
    fig, (left, right) = plt.subplots(
        1, 2, figsize=(TEXT_WIDTH_IN, 2.7), gridspec_kw={"width_ratios": [2.4, 1]})
    bars(left, STATIONS, index, 0)
    left.set_ylabel("Espera média (s)")
    left.set_title("(a) Espera até o atendimento, por estação", loc="left")
    bars(right, LOUNGE, index, 0)
    right.set_title("(b) Após a inspeção", loc="left")
    right.set_ylim(bottom=0)                    # barras sempre a partir do zero
    handles, labels = left.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.03))
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, "fig_d4_espera", "Deslocamento da espera com o segundo balcão",
         f"Fonte: {CELLS.relative_to(CELLS.parents[2])}; média e IC t de 95%, n = 30")


if __name__ == "__main__":
    main()
