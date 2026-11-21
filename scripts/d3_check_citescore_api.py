"""Check Scopus CiteScore 2025 collections against the Elsevier Serial Title API.

The API key is read only from ELSEVIER_API_KEY. Results contain no credential.
"""

import argparse
import csv
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/d3"
COLLECTION = DATA / "citescore_2025_coleta.csv"
RANKING = DATA / "ranking_2025.csv"
OUTPUT = DATA / "citescore_2025_api_check.csv"
API = "https://api.elsevier.com/content/serial/title/issn/"
CURRENT_ISSN = {"1229-9626": "2093-274X", "0191-2216": "0743-1546"}


def read_csv(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def as_list(value):
    return value if isinstance(value, list) else [value] if value else []


def metric_2025(entry):
    years = (entry.get("citeScoreYearInfoList") or {}).get("citeScoreYearInfo")
    for year in as_list(years):
        if str(year.get("@year")) != "2025" or year.get("@status") != "Complete":
            continue
        for group in as_list(year.get("citeScoreInformationList")):
            for item in as_list(group.get("citeScoreInfo")):
                if item.get("docType") == "all":
                    return float(item["citeScore"])
    return None


def fetch(issn, key):
    endpoint = API + quote(issn.replace("-", "")) + "?view=CITESCORE"
    request = Request(endpoint, headers={"Accept": "application/json", "X-ELS-APIKey": key})
    with urlopen(request, timeout=30) as response:
        data = json.load(response)
    return as_list((data.get("serial-metadata-response") or {}).get("entry"))


def normalize(title):
    return re.sub(r"[^a-z0-9]+", "", title.casefold())


def targets():
    existing = read_csv(COLLECTION)
    candidates = {r["issn"]: r for r in read_csv(RANKING) if r["situacao_indicador"] == "fonte_sem_citescore_coletado"}
    result = [dict(issn=r["issn"], expected_id=r["scopus_source_id"], expected_title=r["titulo_scopus"] or r["titulo_portfolio"], old_metric=r["citescore_2025"], kind=r["tipo_fonte"]) for r in existing if r["scopus_source_id"] or r["issn"] == "2014-4865"]
    for issn, r in sorted(candidates.items()):
        if issn not in {x["issn"] for x in result}:
            result.append(dict(issn=issn, expected_id="", expected_title="", old_metric="", kind="periodico", portfolio_title=r["id"]))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, help="Maximum number of API requests for a pilot")
    parser.add_argument("--issn", help="Check only this portfolio ISSN")
    args = parser.parse_args()
    key = os.environ.get("ELSEVIER_API_KEY", "").strip()
    if not key:
        parser.error("ELSEVIER_API_KEY is not set")
    works = {r["id"]: r for name in ("works.csv", "title_search.csv", "chain_metadata.csv") for r in read_csv(DATA / name)}
    checks = []
    all_targets = targets()
    if args.issn:
        all_targets = [r for r in all_targets if r["issn"] == args.issn]
    for target in all_targets[:args.limit]:
        issn = target["issn"]
        query_issn = CURRENT_ISSN.get(issn, issn)
        row = dict(issn_portfolio=issn, issn_consultado=query_issn, scopus_source_id="", titulo_scopus="", citescore_api="", citescore_coleta=target["old_metric"], estado="", data_consulta=datetime.now(timezone.utc).isoformat(timespec="seconds"), tipo_fonte=target["kind"])
        try:
            entries = fetch(query_issn, key)
            if target["expected_id"]:
                matches = [e for e in entries if str(e.get("source-id")) == target["expected_id"]]
            else:
                title = target["expected_title"] or works[target["portfolio_title"]]["journal"]
                matches = [e for e in entries if normalize(e.get("dc:title", "")) == normalize(title)]
            if len(matches) != 1:
                row["estado"] = "identidade_ambigua_ou_ausente"
            else:
                entry = matches[0]
                row["scopus_source_id"] = str(entry.get("source-id", ""))
                row["titulo_scopus"] = entry.get("dc:title", "")
                metric = metric_2025(entry)
                if metric is None:
                    row["estado"] = "metrica_2025_ausente"
                else:
                    row["citescore_api"] = f"{metric:g}"
                    if target["old_metric"]:
                        row["estado"] = "coincide" if float(target["old_metric"]) == metric else "diverge"
                    else:
                        row["estado"] = "novo_valor_confirmado"
        except HTTPError as error:
            row["estado"] = f"http_{error.code}"
        except (URLError, TimeoutError, ValueError, KeyError):
            row["estado"] = "erro_requisicao_ou_resposta"
        checks.append(row)
        print(issn, row["estado"], row["citescore_api"])
        if row["estado"] in {"http_401", "http_403", "http_429"}:
            break
    if args.issn and OUTPUT.exists():
        previous = [r for r in read_csv(OUTPUT) if r["issn_portfolio"] != args.issn]
        checks = previous + checks
        checks.sort(key=lambda r: r["issn_portfolio"])
    fields = list(checks[0]) if checks else []
    if fields:
        with OUTPUT.open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(checks)
    print("Checks recorded:", len(checks), "in", OUTPUT)


if __name__ == "__main__":
    main()
