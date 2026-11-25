"""Quantifica a revisão conjunta v2.4 - v2.3 na Base FCFS, com dias pareados pela semente.

Da raiz: python scripts/d4_comparar_versoes.py > data/d4/comparacao_versoes.csv
O commit antigo e o arquivo atual são necessários; não combina as versões numa amostra.
"""
import csv
import io
import subprocess
import sys
from pathlib import Path

from d4_analise import ci

BASELINE = "8fafba5"
FILE = "data/d4/resultados_d4_4.csv"
ROOT = Path(__file__).resolve().parents[1]


def reference(rows):
    return {int(r["seed"]): r for r in rows
            if (r["family"], r["config"], r["policy"]) == ("referencia", "Base", "fcfs")}


def main():
    old = subprocess.check_output(["git", "show", f"{BASELINE}:{FILE}"], cwd=ROOT, text=True)
    previous = reference(csv.DictReader(io.StringIO(old)))
    with (ROOT / FILE).open() as h:
        current = reference(csv.DictReader(h))
    if previous.keys() != current.keys() or len(current) != 30:
        raise ValueError("Expected the same 30 seeds in both designs")
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(["baseline", "family", "config", "policy", "metric", "n_days", "previous_mean",
                     "current_mean", "paired_change", "ci_low", "ci_high"])
    for metric in ("departures_per_h", "counter_mean_wait_s", "security_mean_wait_s"):
        before = [float(previous[k][metric]) for k in sorted(current)]
        after = [float(current[k][metric]) for k in sorted(current)]
        delta = ci([b - a for a, b in zip(before, after)])
        writer.writerow([BASELINE, "referencia", "Base", "fcfs", metric, delta["n_valid"],
                         ci(before)["mean"], ci(after)["mean"], delta["mean"],
                         delta["ci_low"], delta["ci_high"]])


if __name__ == "__main__":
    main()
