"""Figura D4: contrastes pareados dos dois incrementos de recurso, com IC de 95%.

Fonte: data/d4/contrastes_d4_5.csv. Cada ponto é a média das diferenças dentro da
réplica; a barra é o IC t de 95% (n = 30). Marcadores cheios: contrastes principais
definidos antes das rodadas (família de referência); vazios: exploratórios.
(a) Quinto stand (Base − S4) em cada família de sensibilidade, sob FCFS.
(b) Segundo balcão (B2 − Base) na referência: espera no balcão entre visitas e, para os
mesmos passageiros embarcados, espera no balcão, espera após a inspeção e tempo da
chegada ao embarque; mais a espera no balcão sob serviço exponencial (suposto).
Uso: python gen_fig_d4_contrastes.py [--lang en]
Saída: figures/fig_d4_contrastes{,_en}.{pdf,png}.
"""

import matplotlib.pyplot as plt

from estilo_d4 import (BLUE, CONTRASTS, GRAY, GREEN, VERMILLION, TEXT_WIDTH_IN, apply_style,
                       comma, contrasts, estimate, language, save, suffix)

REF = "referencia"
# (rótulo pt, rótulo en, família, contraste, métrica, cor)
STANDS = (
    ("6 pedidos/h, 30 min", "6 requests/h, 30 min", REF, "stands_fcfs", "departures_per_h",
     BLUE),
    ("4 pedidos/h, 30 min", "4 requests/h, 30 min", "demanda_baixa", "stands_fcfs",
     "departures_per_h", GRAY),
    ("8 pedidos/h, 30 min", "8 requests/h, 30 min", "demanda_alta", "stands_fcfs",
     "departures_per_h", GRAY),
    ("6 pedidos/h, sem recarga", "6 requests/h, no charging", "sem_recarga", "stands_fcfs",
     "departures_per_h", GRAY),
    ("6 pedidos/h, 60 min", "6 requests/h, 60 min", "recarga_longa", "stands_fcfs",
     "departures_per_h", GRAY),
    ("Serviço exponencial", "Exponential service", "servico_variavel", "stands_fcfs",
     "departures_per_h", GRAY),
)
COUNTER = (
    ("Balcão, todas as visitas", "Check-in, all visits", REF, "counter_fcfs",
     "counter_mean_wait_s", BLUE),
    ("Balcão, embarcados", "Check-in, boarded", REF, "boarded_counter_fcfs",
     "boarded_counter_wait_mean_s", GREEN),
    ("Após a inspeção, embarcados", "Post-security, boarded", REF, "lounge_fcfs",
     "post_security_mean_s", GREEN),
    ("Chegada ao embarque, embarcados", "Arrival to boarding, boarded", REF,
     "door_to_board_fcfs", "arrival_to_board_mean_s", GREEN),
    ("Balcão, serviço exponencial", "Check-in, exponential service", "servico_variavel",
     "counter_fcfs", "counter_mean_wait_s", VERMILLION),
)
TEXT = {
    "pt": {"a_x": "Base − S4 (decolagens com passageiros/h)", "a_t": "(a) Quinto stand, FCFS",
           "b_x": "B2 − Base (s)", "b_t": "(b) Segundo balcão, FCFS",
           "primary": "Principal", "exploratory": "Exploratório",
           "title": "Contrastes pareados dos incrementos de recurso"},
    "en": {"a_x": "Base − S4 (passenger departures/h)", "a_t": "(a) Fifth stand, FCFS",
           "b_x": "B2 − Base (s)", "b_t": "(b) Second check-in counter, FCFS",
           "primary": "Primary", "exploratory": "Exploratory",
           "title": "Paired contrasts of the resource increments"},
}


def panel(ax, items, index, digits, xlabel, title, lang):
    for y, (_pt, _en, family, name, metric, color) in enumerate(items):
        row = index[(family, name, metric)]
        mean, lo, hi = estimate(row)
        primary = row["classification"] == "primary"
        ax.errorbar(mean, y, xerr=[[mean - lo], [hi - mean]], fmt="o", color=color,
                    markerfacecolor=color if primary else "white", markeredgewidth=1.4,
                    capsize=2.5, elinewidth=1.1, zorder=3)
    ax.axvline(0, color="#444444", linewidth=0.8, zorder=1)
    ax.set_yticks(range(len(items)))
    ax.set_yticklabels([item[0] if lang == "pt" else item[1] for item in items])
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(comma(digits, lang))
    ax.set_xlabel(xlabel)
    ax.set_title(title, loc="left")
    ax.grid(axis="y", visible=False)


def main():
    lang = language()
    text = TEXT[lang]
    apply_style()
    index = contrasts()
    fig, (left, right) = plt.subplots(
        1, 2, figsize=(TEXT_WIDTH_IN, 2.9), gridspec_kw={"width_ratios": [1, 1.1]})
    panel(left, STANDS, index, 2, text["a_x"], text["a_t"], lang)
    panel(right, COUNTER, index, 0, text["b_x"], text["b_t"], lang)
    handles = [
        plt.Line2D([], [], marker="o", color="#333333", linestyle="", label=text["primary"]),
        plt.Line2D([], [], marker="o", color="#333333", markerfacecolor="white",
                   linestyle="", label=text["exploratory"]),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.04))
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "fig_d4_contrastes" + suffix(lang), text["title"],
         f"Fonte: {CONTRASTS.relative_to(CONTRASTS.parents[2])}; média e IC t de 95%, n = 30")


if __name__ == "__main__":
    main()
