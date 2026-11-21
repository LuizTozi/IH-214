"""Merge the two CiteScore 2025 collections and rank the D3 candidate portfolio."""

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/d3"
CLAUDE = ROOT / "claude/outputs/D3_CITESCORE_2025_COLETA_NAVEGADOR.csv"
COLLECTION = DATA / "citescore_2025_coleta.csv"
API_CHECK = DATA / "citescore_2025_api_check.csv"
RANKING = DATA / "ranking_2025.csv"
RESEARCH_YEAR = 2026
HALF_LIFE = 7.6


def read_csv(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path, rows, fields):
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def merge_scores():
    old_rows, browser_rows = read_csv(COLLECTION), read_csv(CLAUDE)
    old = {r["issn"]: r for r in old_rows}
    browser = {r["issn"]: r for r in browser_rows}
    if len(old) != len(old_rows) or len(browser) != len(browser_rows):
        raise ValueError("Duplicate ISSN in a source collection")
    assert len(browser) >= 26 and len(old) >= 23
    checked_rows = read_csv(API_CHECK) if API_CHECK.exists() else []
    checked = {r["issn_portfolio"]: r for r in checked_rows}
    if len(checked) != len(checked_rows):
        raise ValueError("Duplicate ISSN in API check")
    if checked and any(r["estado"] == "diverge" for r in checked_rows):
        raise ValueError("API disagrees with browser collection")
    works = {r["id"]: r for name in ("works.csv", "title_search.csv", "chain_metadata.csv") for r in read_csv(DATA / name)}
    portfolio = {}
    for key, _ in candidate_ids():
        work = works[key]
        if work["issn"]:
            portfolio.setdefault(work["issn"], []).append(work)
    rows = []
    for issn in sorted(old.keys() | browser.keys() | checked.keys()):
        a, b = old.get(issn, {}), browser.get(issn, {})
        c = checked.get(issn, {})
        if a.get("citescore_2025") and b.get("citescore_2025"):
            if float(a["citescore_2025"]) != float(b["citescore_2025"]):
                raise ValueError(f"Conflicting CiteScore 2025 for {issn}")
        for value in (a.get("citescore_2025"), b.get("citescore_2025")):
            if value and c.get("citescore_api") and float(value) != float(c["citescore_api"]):
                raise ValueError(f"API CiteScore conflict for {issn}")
        if a.get("scopus_source_id") and b.get("scopus_source_id"):
            if a["scopus_source_id"] != b["scopus_source_id"]:
                raise ValueError(f"Conflicting Scopus source ID for {issn}")
        for value in (a.get("scopus_source_id"), b.get("scopus_source_id")):
            if value and c.get("scopus_source_id") and value != c["scopus_source_id"]:
                raise ValueError(f"API source ID conflict for {issn}")
        score = b.get("citescore_2025") or a.get("citescore_2025") or c.get("citescore_api", "")
        members = portfolio.get(issn, [])
        source_id = b.get("scopus_source_id") or a.get("scopus_source_id") or c.get("scopus_source_id", "")
        api_status = c.get("estado", "")
        if score and api_status in {"coincide", "novo_valor_confirmado"}:
            origin = "Scopus Preview + Elsevier Serial Title API" if b.get("citescore_2025") else "Elsevier Serial Title API"
        elif b.get("citescore_2025"):
            origin = "Scopus Preview, coleta Claude"
        elif score:
            origin = a.get("origem_valor") or "exportacao Scopus, coleta Codex"
        else:
            origin = ""
        row = {
            "issn": issn,
            "titulo_portfolio": a.get("titulo_portfolio") or b.get("titulo_scopus") or (members[0]["journal"] if members else ""),
            "ids_portfolio": a.get("ids_portfolio") or b.get("ids_portfolio") or " | ".join(x["id"] for x in members),
            "tipo_fonte": b.get("tipo_fonte") or a.get("tipo_fonte") or c.get("tipo_fonte", ""),
            "citescore_2025": score,
            "titulo_scopus": b.get("titulo_scopus") or a.get("titulo_scopus") or c.get("titulo_scopus", ""),
            "issn_exibido_scopus": b.get("issn_exibido_scopus") or a.get("issn_exibido_scopus", ""),
            "scopus_source_id": source_id,
            "url_fonte": b.get("url_fonte") or a.get("url_fonte") or ("https://www.scopus.com/sourceid/" + source_id if source_id else ""),
            "data_consulta": c.get("data_consulta") or b.get("data_consulta") or a.get("data_consulta", ""),
            "correspondencia": b.get("correspondencia") or a.get("correspondencia") or ("issn_api" if source_id else ""),
            "estado": "citescore_2025_api_conferido" if score and api_status in {"coincide", "novo_valor_confirmado"} else "citescore_2025_conferido" if score else "sem_fonte_scopus_api_404" if api_status == "http_404" else "sem_indicador_2025",
            "origem_valor": origin,
            "observacao": b.get("observacao") or a.get("observacao", ""),
        }
        if api_status and " Conferencia API:" not in row["observacao"]:
            row["observacao"] += f" Conferencia API: {api_status}; {c.get('issn_consultado', issn)}; {c.get('data_consulta', '')}."
        if issn == "2352-1457":
            assert row["scopus_source_id"] == "21100448300"
            row["observacao"] += " Fonte confirmada na aba de anais de ext_list_Oct_2026.xlsx; DOI do estudo confirmado na ScienceDirect."
        if issn == "1229-9626":
            row["correspondencia"] = "titulo_e_doi_editor"
            row["observacao"] = row["observacao"].replace(" Confirmar pelo DOI antes de atribuir.", "")
            row["observacao"] += " DOI 10.1007/s42405-022-00505-z confirmado no site da Springer; ISSN OpenAlex divergente preservado."
        if issn == "0191-2216":
            row["correspondencia"] = "titulo_e_doi_editor"
            row["observacao"] = row["observacao"].replace(" Confirmar pelo DOI antes de atribuir.", "")
            row["observacao"] += " DOI 10.1109/CDC56724.2024.10886225 confirmado no IEEE Xplore; ISSN OpenAlex divergente preservado."
        rows.append(row)
    assert len(rows) >= 26 and sum(bool(r["citescore_2025"]) for r in rows) >= 25
    return rows


def score(metric, year, citations, recency_weight=1, citation_weight=1):
    return metric - recency_weight * (RESEARCH_YEAR - year) / HALF_LIFE + citation_weight * citations / (RESEARCH_YEAR + 1 - year)


def candidate_ids():
    primary = [(r["id"], r["disposicao"]) for r in read_csv(DATA / "triagem.csv") if r["disposicao"] in {"avancar", "incluir"}]
    chain = [(r["work"].rsplit("/", 1)[-1], r["decisao_resumo"]) for r in read_csv(DATA / "chain_screening.csv") if r["decisao_resumo"] in {"avancar", "incluir"}]
    candidates = primary + chain
    ids = [item[0] for item in candidates]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate candidate ID")
    return candidates


def make_ranking(metrics):
    by_issn = {r["issn"]: r for r in metrics}
    works = {r["id"]: r for name in ("works.csv", "title_search.csv", "chain_metadata.csv") for r in read_csv(DATA / name)}
    rows = []
    for key, disposition in candidate_ids():
        work = works[key]
        source = by_issn.get(work["issn"], {})
        metric = source.get("citescore_2025", "")
        year, citations = int(work["year"]), int(work["citations"])
        missing_state = "preprint_sem_indicador" if work["issn"] == "2331-8422" else "fonte_sem_citescore_coletado" if work["issn"] else "sem_issn"
        row = {
            "posicao": "", "id": key, "doi": work["doi"], "issn": work["issn"],
            "ano": year, "citacoes": citations, "selecao": disposition,
            "tipo_fonte": source.get("tipo_fonte", ""),
            "scopus_source_id": source.get("scopus_source_id", ""),
            "citescore_2025": metric, "central": "", "atualidade": "", "citacoes_x3": "",
            "situacao_indicador": source.get("estado", missing_state),
        }
        if metric:
            value = float(metric)
            row["central"] = round(score(value, year, citations), 6)
            row["atualidade"] = round(score(value, year, citations, 3, 1), 6)
            row["citacoes_x3"] = round(score(value, year, citations, 1, 3), 6)
        rows.append(row)
    rows.sort(key=lambda r: (r["central"] == "", -float(r["central"] or 0), r["id"]))
    for position, row in enumerate((r for r in rows if r["central"] != ""), 1):
        row["posicao"] = position
    return rows


def main():
    metrics = merge_scores()
    ranking = make_ranking(metrics)
    write_csv(COLLECTION, metrics, list(metrics[0]))
    write_csv(RANKING, ranking, list(ranking[0]))
    print("Merged sources:", len(metrics), "with CiteScore 2025:", sum(bool(r["citescore_2025"]) for r in metrics))
    print("Candidates:", len(ranking), "ranked:", sum(bool(r["posicao"]) for r in ranking))
    print("Indicator states:", dict(Counter(r["situacao_indicador"] for r in ranking)))


if __name__ == "__main__":
    main()
