"""Figura D4: para onde vai a espera quando se acrescenta o segundo balcão (B2 contra Base).

Fonte: data/d4/resumo_celulas_d4_5.csv, família de referência. Barras: média por réplica;
barras de erro: IC t de 95% (n = 30). Painel (a): espera até o início do atendimento em
cada estação, entre visitas com início observado. Painel (b): espera do fim da inspeção ao
início do embarque (VAR-045), entre embarcados; inclui 51,6 s de caminhada e acesso.
As populações diferem entre painéis; as médias não se somam. Barras partem do zero.
Uso: python gen_fig_d4_espera.py [--lang en]
Saída: figures/fig_d4_espera{,_en}.{pdf,png}.
"""

import matplotlib.pyplot as plt
import numpy as np

from estilo_d4 import (CELLS, GREEN, SKY, TEXT_WIDTH_IN, apply_style, cells, comma, estimate,
                       language, save, suffix)

REF = "referencia"
BARS = (  # (configuração, política, cor, hachura, rótulo pt, rótulo en)
    ("Base", "fcfs", SKY, "", "Base, FCFS", "Base, FCFS"),
    ("B2", "fcfs", GREEN, "", "B2, FCFS", "B2, FCFS"),
    ("Base", "agenda", SKY, "////", "Base, agenda", "Base, advance"),
    ("B2", "agenda", GREEN, "////", "B2, agenda", "B2, advance"),
)
STATIONS = (("Balcão", "Check-in", "counter_mean_wait_s"),
            ("Bagagem", "Baggage", "baggage_mean_wait_s"),
            ("Inspeção", "Security", "security_mean_wait_s"))
LOUNGE = (("Fim da inspeção\naté o embarque", "End of security\nto boarding",
           "post_security_mean_s"),)
TEXT = {
    "pt": {"y": "Espera média (s)", "a": "(a) Espera até o atendimento, por estação",
           "b": "(b) Após a inspeção", "title": "Deslocamento da espera com o segundo balcão"},
    "en": {"y": "Mean wait (s)", "a": "(a) Wait until service, by station",
           "b": "(b) After security", "title": "Waiting shift with the second counter"},
}


def bars(ax, groups, index, digits, lang):
    width = 0.8 / len(BARS)
    x = np.arange(len(groups))
    for i, (config, policy, color, hatch, label_pt, label_en) in enumerate(BARS):
        values = [estimate(index[(REF, config, policy, group[2])]) for group in groups]
        means = [m for m, _, _ in values]
        err = [[m - lo for m, lo, _ in values], [hi - m for m, _, hi in values]]
        positions = x + (i - (len(BARS) - 1) / 2) * width
        ax.bar(positions, means, width * 0.92, yerr=err, color=color, hatch=hatch,
               edgecolor="white", linewidth=0.6, label=label_pt if lang == "pt" else label_en,
               error_kw={"elinewidth": 0.9, "capsize": 2, "ecolor": "#333333"}, zorder=3)
        for xi, mean in zip(positions, means):
            if mean == 0:                       # sem fila: deixa o zero visível
                ax.text(xi, 0, "0", ha="center", va="bottom", fontsize=7, color="#555555")
    ax.set_xticks(x)
    ax.set_xticklabels([group[0] if lang == "pt" else group[1] for group in groups])
    ax.yaxis.set_major_formatter(comma(digits, lang))
    ax.grid(axis="x", visible=False)


def main():
    lang = language()
    text = TEXT[lang]
    apply_style()
    plt.rcParams["hatch.color"] = "white"
    index = cells()
    fig, (left, right) = plt.subplots(
        1, 2, figsize=(TEXT_WIDTH_IN, 2.7), gridspec_kw={"width_ratios": [2.4, 1]})
    bars(left, STATIONS, index, 0, lang)
    left.set_ylabel(text["y"])
    left.set_title(text["a"], loc="left")
    bars(right, LOUNGE, index, 0, lang)
    right.set_title(text["b"], loc="left")
    right.set_ylim(bottom=0)                    # barras sempre a partir do zero
    handles, labels = left.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.03))
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    save(fig, "fig_d4_espera" + suffix(lang), text["title"],
         f"Fonte: {CELLS.relative_to(CELLS.parents[2])}; média e IC t de 95%, n = 30")


if __name__ == "__main__":
    main()
