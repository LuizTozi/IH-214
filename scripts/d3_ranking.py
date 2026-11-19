"""Calculate exploratory InOrdinatio 2.0 scores from the frozen bibliographic exports."""
import argparse
import csv
import hashlib
import re
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

DATA = Path(__file__).resolve().parents[1] / "data/d3"


def cite_scores(workbook):
    scores = {}
    with ZipFile(workbook) as archive:
        strings = ["".join(node.itertext())
                   for node in ET.fromstring(archive.read("xl/sharedStrings.xml"))]
        with archive.open("xl/worksheets/sheet4.xml") as sheet:
            for _, row in ET.iterparse(sheet, events=("end",)):
                if row.tag.endswith("}row"):
                    cells = {}
                    for cell in row.findall("{*}c"):
                        value = cell.findtext("{*}v")
                        if value is not None:
                            column = re.sub(r"\d+", "", cell.get("r"))
                            cells[column] = strings[int(value)] if cell.get("t") == "s" else value
                    if cells.get("E") and cells["E"] != "CiteScore":
                        for column in "ABC":
                            if cells.get(column):
                                scores.setdefault(cells[column], set()).add(float(cells["E"]))
                    row.clear()
    return scores


def score(metric, year, citations, recency_weight, citation_weight):
    return metric - recency_weight * (2026 - year) / 7.6 + citation_weight * citations / (2027-year)


def records(name):
    with (DATA / name).open() as stream:
        return list(csv.DictReader(stream))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workbook", type=Path)
    args = parser.parse_args()
    metrics = cite_scores(args.workbook)
    works = {r["id"]: r for f in ("works.csv", "title_search.csv") for r in records(f)}
    eligible = [e["id"] for e in records("triagem.csv") if e["disposicao"] == "avancar"]
    chain = {r["id"]: r for r in records("chain_metadata.csv")}
    for record in records("chain_screening.csv"):
        if record["decisao_resumo"] == "avancar":
            key = record["work"].split("/")[-1]
            eligible.append(key)
            works[key] = chain[key]
    table = []
    for key in eligible:
        r = works[key]
        values = metrics.get(r["issn"], set())
        row = dict(id=r["id"], doi=r["doi"], issn=r["issn"], ano=r["year"],
                   citacoes=r["citations"], citescore_2021="", central="", atualidade="", citacoes_x3="")
        if len(values) == 1:
            value = next(iter(values))
            row["citescore_2021"] = value
            for field, weights in (("central", (1, 1)), ("atualidade", (3, 1)), ("citacoes_x3", (1, 3))):
                row[field] = round(score(value, int(r["year"]), int(r["citations"]), *weights), 6)
        table.append(row)
    table.sort(key=lambda r: (r["central"] == "", -(r["central"] or 0), r["id"]))
    with (DATA / "ranking.csv").open("w") as dest:
        writer = csv.DictWriter(dest, fieldnames=table[0])
        writer.writeheader()
        writer.writerows(table)
    print("RankIn.xlsm SHA-256", hashlib.sha256(args.workbook.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
