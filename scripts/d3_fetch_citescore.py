"""Collect verified CiteScore 2025 values from Elsevier's Serial Title API.

Set ELSEVIER_API_KEY in the process environment. The key is never stored here.
"""

import argparse
import csv
import json
import os
import tempfile
import time
from datetime import date
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
COLLECTION = ROOT / "data/d3/citescore_2025_coleta.csv"
API = "https://api.elsevier.com/content/serial/title/issn/"
CURRENT_ISSN = {"1229-9626": "2093-274X"}  # Current ISSN in Scopus list, October 2026.


def as_list(value):
    return value if isinstance(value, list) else [value] if value else []


def cite_score_2025(entry):
    info = entry.get("citeScoreYearInfoList") or {}
    for year in as_list(info.get("citeScoreYearInfo")):
        if str(year.get("@year")) != "2025" or year.get("@status") != "Complete":
            continue
        for group in as_list(year.get("citeScoreInformationList")):
            for item in as_list(group.get("citeScoreInfo")):
                if item.get("docType") == "all":
                    return float(item["citeScore"])
    return None


def fetch(issn, key):
    url = API + quote(issn.replace("-", "")) + "?view=CITESCORE"
    req = Request(url, headers={"Accept": "application/json", "X-ELS-APIKey": key})
    with urlopen(req, timeout=25) as response:
        payload = json.load(response)
    entries = as_list((payload.get("serial-metadata-response") or {}).get("entry"))
    return url, entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, help="Fetch at most this many sources for a pilot")
    args = parser.parse_args()
    key = os.environ.get("ELSEVIER_API_KEY", "").strip()
    if not key:
        parser.error("ELSEVIER_API_KEY is not set")
    with COLLECTION.open(newline="") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames
        rows = list(reader)
    done = 0
    attempted = 0
    for row in rows:
        if row["citescore_2025"] or not row["scopus_source_id"]:
            continue
        if args.limit is not None and attempted >= args.limit:
            break
        issn = CURRENT_ISSN.get(row["issn"], row["issn"])
        attempted += 1
        try:
            url, entries = fetch(issn, key)
            matches = [e for e in entries if str(e.get("source-id")) == row["scopus_source_id"]]
            if len(matches) != 1:
                print(f"{row['issn']}: source ID mismatch; skipped")
                continue
            score = cite_score_2025(matches[0])
            if score is None:
                print(f"{row['issn']}: no complete CiteScore 2025 in API response")
                continue
            row["citescore_2025"] = f"{score:g}"
            row["titulo_scopus"] = matches[0].get("dc:title", row["titulo_scopus"])
            row["data_consulta"] = date.today().isoformat()
            row["estado"] = "metrica_2025_api_conferida"
            row["observacao"] = f"Elsevier Serial Title API; view=CITESCORE; ano=2025; status=Complete; docType=all; ISSN consultado={issn}; {url}"
            done += 1
            print(f"{row['issn']}: CiteScore 2025 = {score:g}")
            time.sleep(0.2)
        except HTTPError as exc:
            print(f"{row['issn']}: HTTP {exc.code}; no value recorded")
            if exc.code in (401, 403, 429):
                break
        except (URLError, TimeoutError, ValueError, KeyError) as exc:
            print(f"{row['issn']}: {type(exc).__name__}; no value recorded")
    if done:
        with tempfile.NamedTemporaryFile("w", newline="", dir=COLLECTION.parent, delete=False) as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
            temp = stream.name
        os.replace(temp, COLLECTION)
    print(f"Values recorded: {done}")


if __name__ == "__main__":
    main()
