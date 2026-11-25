"""Figura D4: contrastes pareados com IC de 95% (gráfico de pontos e intervalos).

Fonte: data/d4/contrastes_d4_5.csv. Cada ponto é a média das diferenças dentro da
réplica; a barra é o IC t de 95% (n = 30). Marcadores cheios: contrastes principais
definidos antes das rodadas (família de referência); vazios: exploratórios.
Dois painéis porque as unidades diferem (decolagens/h e segundos).
Uso: python gen_fig_d4_contrastes.py [--lang en]
Saída: figures/fig_d4_contrastes{,_en}.{pdf,png}.
"""

import matplotlib.pyplot as plt

from estilo_d4 import (CONTRASTS, GRAY, GREEN, POLICY, TEXT_WIDTH_IN, apply_style, comma,
                       contrasts, estimate, language, save, suffix)

REF = "referencia"
FCFS, AGENDA = POLICY["fcfs"]["color"], POLICY["agenda"]["color"]
# (rótulo pt, rótulo en, família, contraste, métrica, cor)
FLOW = (
    ("Base − S4, FCFS", "Base − S4, FCFS", REF, "stands_fcfs", "departures_per_h", FCFS),
    ("Base − S4, agenda", "Base − S4, advance", REF, "stands_agenda", "departures_per_h",
     AGENDA),
    ("Agenda − FCFS, 6 pedidos/h", "Advance − FCFS, 6 requests/h", REF, "policy_Base",
     "departures_per_h", GRAY),
    ("Agenda − FCFS, 4 pedidos/h", "Advance − FCFS, 4 requests/h", "demanda_baixa",
     "policy_Base", "departures_per_h", GRAY),
    ("Agenda − FCFS, 8 pedidos/h", "Advance − FCFS, 8 requests/h", "demanda_alta",
     "policy_Base", "departures_per_h", GRAY),
    ("Agenda − FCFS, sem recarga", "Advance − FCFS, no charging", "sem_recarga",
     "policy_Base", "departures_per_h", GRAY),
    ("Agenda − FCFS, recarga 60 min", "Advance − FCFS, 60-min charging", "recarga_longa",
     "policy_Base", "departures_per_h", GRAY),
)
WAIT = (
    ("Balcão, FCFS", "Check-in, FCFS", REF, "counter_fcfs", "counter_mean_wait_s", FCFS),
    ("Balcão, agenda", "Check-in, advance", REF, "counter_agenda", "counter_mean_wait_s",
     AGENDA),
    ("Após a inspeção, FCFS", "Post-security, FCFS", REF, "lounge_fcfs",
     "post_security_mean_s", GREEN),
    ("Após a inspeção, agenda", "Post-security, advance", REF, "lounge_agenda",
     "post_security_mean_s", GREEN),
)
TEXT = {
    "pt": {"flow_x": "Diferença em decolagens com passageiros/h", "flow_t": "(a) Partidas",
           "wait_x": "Diferença B2 − Base na espera média (s)",
           "wait_t": "(b) Espera do passageiro", "primary": "Principal",
           "exploratory": "Exploratório", "title": "Contrastes pareados da D4"},
    "en": {"flow_x": "Difference in passenger departures/h", "flow_t": "(a) Departures",
           "wait_x": "B2 − Base difference in mean wait (s)",
           "wait_t": "(b) Passenger waiting", "primary": "Primary",
           "exploratory": "Exploratory", "title": "D4 paired contrasts"},
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
        1, 2, figsize=(TEXT_WIDTH_IN, 2.9), gridspec_kw={"width_ratios": [1.15, 1]})
    panel(left, FLOW, index, 1, text["flow_x"], text["flow_t"], lang)
    panel(right, WAIT, index, 0, text["wait_x"], text["wait_t"], lang)
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
