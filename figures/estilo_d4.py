"""Estilo comum das figuras da D4 (skill academic-plotting, fluxo de dados com matplotlib).

- Tipografia serifada com métricas de Times (Liberation Serif), que cobre os acentos.
- Paleta Okabe-Ito, segura para daltonismo; FCFS e agenda mantêm as mesmas cores
  em todas as figuras.
- Vírgula decimal, como no manuscrito.
- Exportação em PDF vetorial (para o LaTeX) e PNG a 300 dpi.
"""

import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")                      # sem janela; só arquivos
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parent.parent
CELLS = ROOT / "data" / "d4" / "resumo_celulas_d4_5.csv"
CONTRASTS = ROOT / "data" / "d4" / "contrastes_d4_5.csv"
FIGURES = ROOT / "figures"

TEXT_WIDTH_IN = 6.3                        # 16 cm: A4 com margens de 2,5 cm (main.tex)

# Okabe-Ito
BLUE, VERMILLION, SKY, GREEN, ORANGE, GRAY = (
    "#0072B2", "#D55E00", "#56B4E9", "#009E73", "#E69F00", "#7F7F7F")
POLICY = {
    "fcfs": {"label": "FCFS local", "color": BLUE, "marker": "o", "linestyle": "-"},
    "agenda": {"label": "Admissão antecipada", "color": VERMILLION, "marker": "s",
               "linestyle": "--"},
}
POLICY_EN = {"fcfs": "Local FCFS", "agenda": "Advance admission"}


def language():
    """Idioma pedido na linha de comando: --lang pt (padrão) ou --lang en."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=("pt", "en"), default="pt")
    return parser.parse_args().lang


def suffix(lang):
    return "" if lang == "pt" else "_en"


def apply_style():
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Liberation Serif", "Times New Roman", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 9, "axes.titlesize": 9.5, "axes.titleweight": "bold",
        "axes.labelsize": 9, "xtick.labelsize": 8.5, "ytick.labelsize": 8.5,
        "legend.fontsize": 8.5, "legend.frameon": False,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.18, "grid.linestyle": "-",
        "axes.axisbelow": True,
        "lines.linewidth": 1.8, "lines.markersize": 5,
        "figure.dpi": 300, "savefig.dpi": 300, "savefig.bbox": "tight",
        "pdf.fonttype": 42,                # fontes TrueType embutidas no PDF
    })


def comma(digits, lang="pt"):
    """Formatador de eixo: vírgula decimal em português, ponto em inglês; sinal de menos."""
    sep = "," if lang == "pt" else "."
    return FuncFormatter(
        lambda value, _pos: f"{value:.{digits}f}".replace(".", sep).replace("-", "\u2212"))


def read(path):
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def cells():
    return {(r["family"], r["config"], r["policy"], r["metric"]): r for r in read(CELLS)}


def contrasts():
    return {(r["family"], r["contrast"], r["metric"]): r for r in read(CONTRASTS)}


def estimate(row):
    """(média, limite inferior, limite superior) de uma linha de resumo."""
    return float(row["mean"]), float(row["ci_low"]), float(row["ci_high"])


def save(fig, name, title, source):
    for suffix in (".pdf", ".png"):
        path = FIGURES / f"{name}{suffix}"
        metadata = ({"Title": title, "Subject": source} if suffix == ".pdf"
                    else {"Title": title, "Description": source})
        fig.savefig(path, metadata=metadata)
    plt.close(fig)
    print(f"{FIGURES / name}.pdf e .png")
