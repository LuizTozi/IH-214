"""Deriva parâmetros do modelo a partir dos dados abertos de Janssen et al. (2020).

Fonte: S. A. M. Janssen, R. van der Sommen, A. Dilweg, A. Sharpanskykh, Data-Driven
Analysis of Airport Security Checkpoint Operations, Aerospace 7, 69 (2020); dados em
4TU.ResearchData, DOI 10.4121/uuid:6246e6a6-d149-420f-a6a4-7afd08f154b5 (CC BY 4.0),
arquivo security_checkpoint_data.xlsx (MD5 b7ea8a9669d6e692fec358704589ad9a), baixado
para data/raw/janssen2020/ (fora do Git).

Saídas:
1. Tempo de serviço efetivo da inspeção: intervalo entre passagens sucessivas pelo
   detector de metais (WTMD) na mesma faixa, somente quando o passageiro seguinte já
   havia terminado de entregar a bagagem antes da passagem anterior (fila presente).
   Nesses períodos o servidor está ocupado, e o intervalo de saída é o tempo de serviço.
2. Tamanho do grupo de viagem (coluna W do README), para a distribuição de reservas.
3. Tempo próprio de inspeção por passageiro, para um posto de ocupação única (decisão do
   autor, 25/11/2026): entrega da bagagem + revista manual + detecção de explosivos +
   retirada da bagagem, sem as esperas por outros passageiros ou funcionários. O modelo
   reamostra estes valores observados, sem supor uma distribuição.

Uso: python -I fontes_janssen.py ../data/raw/janssen2020/security_checkpoint_data.xlsx ../data/fontes/
"""

import csv
import math
import re
import statistics
import sys
import zipfile
from collections import Counter
from pathlib import Path

COLUMNS = {"K": "drop_start", "M": "drop_end", "N": "wtmd", "Q": "pat_start", "R": "pat_end",
           "S": "etd_start", "T": "etd_end", "U": "reclaim_start", "V": "reclaim_end",
           "W": "group"}                              # README.pdf, tabela de colunas


def seconds(value):
    """Converte hhmmss (texto ou número, com ou sem zero à esquerda) em segundos."""
    digits = re.sub(r"\D", "", str(value))
    if not digits or len(digits) > 6:
        return None
    digits = digits.zfill(6)
    h, m, s = int(digits[:2]), int(digits[2:4]), int(digits[4:])
    if m > 59 or s > 59 or h > 23:
        return None
    return 3600 * h + 60 * m + s


def read_sheets(path):
    z = zipfile.ZipFile(path)
    names = z.namelist()
    strings = []
    if "xl/sharedStrings.xml" in names:
        xml = z.read("xl/sharedStrings.xml").decode("utf-8")
        for si in re.findall(r"<si>(.*?)</si>", xml, flags=re.S):
            strings.append("".join(re.findall(r"<t[^>]*>([^<]*)</t>", si)))
    workbook = z.read("xl/workbook.xml").decode("utf-8")
    sheet_names = re.findall(r'<sheet [^>]*name="([^"]+)"', workbook)
    sheets = {}
    for i, name in enumerate(sheet_names, start=1):
        xml = z.read(f"xl/worksheets/sheet{i}.xml").decode("utf-8")
        rows = []
        for row in re.findall(r"<row [^>]*>(.*?)</row>", xml, flags=re.S)[1:]:   # sem cabeçalho
            record = {}
            for col, attrs, val in re.findall(
                    r'<c r="([A-Z]+)\d+"([^>]*?)(?:/>|>(?:<f>[^<]*</f>)?(?:<v>([^<]*)</v>)?</c>)',
                    row):
                if col in COLUMNS and val:
                    record[COLUMNS[col]] = strings[int(val)] if 't="s"' in attrs else val
            rows.append(record)
        sheets[name] = rows
    return sheets


def summary(values):
    values = sorted(values)
    n = len(values)
    mean = statistics.mean(values)
    sd = statistics.stdev(values)
    q = lambda p: values[min(n - 1, math.ceil(p * n) - 1)]
    return {"n": n, "mean_s": round(mean, 2), "sd_s": round(sd, 2), "cv": round(sd / mean, 3),
            "p05_s": q(0.05), "median_s": q(0.50), "p95_s": q(0.95),
            "min_s": values[0], "max_s": values[-1]}


def main(xlsx, out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    sheets = read_sheets(xlsx)
    headways, groups, used = [], Counter(), Counter()
    for name, rows in sheets.items():
        passengers = []
        for r in rows:
            wtmd, drop_end = seconds(r.get("wtmd", "")), seconds(r.get("drop_end", ""))
            if r.get("group", "").strip().isdigit():
                groups[int(r["group"])] += 1
            if wtmd is not None and drop_end is not None:
                passengers.append((wtmd, drop_end))
        passengers.sort()
        for (w_prev, _), (w_next, drop_next) in zip(passengers, passengers[1:]):
            # Fila presente: o seguinte terminou a entrega antes da passagem anterior.
            if drop_next <= w_prev and 0 < w_next - w_prev <= 600:
                headways.append(w_next - w_prev)
                used[name] += 1
    own = []
    for rows in sheets.values():
        for r in rows:
            t = {k: seconds(r.get(k, "")) for k in COLUMNS.values() if k != "group"}
            if None in (t["drop_start"], t["drop_end"], t["reclaim_start"], t["reclaim_end"]):
                continue
            parts = [t["drop_end"] - t["drop_start"], t["reclaim_end"] - t["reclaim_start"]]
            for a, b in (("pat_start", "pat_end"), ("etd_start", "etd_end")):
                if t[a] is not None and t[b] is not None and t[b] >= t[a]:
                    parts.append(t[b] - t[a])
            if all(0 <= x <= 600 for x in parts):
                own.append(sum(parts))
    with (out / "janssen_tempo_proprio.csv").open("w", newline="", encoding="utf-8") as h:
        h.write("own_time_s\n" + "\n".join(str(x) for x in sorted(own)) + "\n")
    print("tempo próprio de inspeção:", summary(own))
    service = summary(headways)
    with (out / "janssen_servico_inspecao.csv").open("w", newline="", encoding="utf-8") as h:
        writer = csv.DictWriter(h, fieldnames=list(service), lineterminator="\n")
        writer.writeheader()
        writer.writerow(service)
    with (out / "janssen_intervalos_inspecao.csv").open("w", newline="", encoding="utf-8") as h:
        h.write("headway_s\n" + "\n".join(str(x) for x in sorted(headways)) + "\n")
    total = sum(groups.values())
    with (out / "janssen_tamanho_grupo.csv").open("w", newline="", encoding="utf-8") as h:
        writer = csv.writer(h, lineterminator="\n")
        writer.writerow(["group_size", "passengers", "share"])
        for size in sorted(groups):
            writer.writerow([size, groups[size], round(groups[size] / total, 4)])
    print("serviço efetivo da inspeção:", service)
    print("intervalos por aba:", dict(used))
    print("tamanho do grupo (passageiros):", dict(sorted(groups.items())), "total", total)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
