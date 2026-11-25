"""Gera a lista de referências do artigo em inglês no estilo do modelo AERO2027.

Estilo do modelo (aero2027/modelo_oficial_AERO2027.docx):
    M. N. R. Ashfold, P. W. May, C. A. Rego, N. M. Everitt, Chem. Soc. Rev., 23, 21 – 30, (1994).
Iniciais e sobrenome, veículo, volume em negrito, páginas e (ano). Os metadados vêm
apenas de references/references.bib. Os nomes de periódicos ficam por extenso, porque
o projeto não tem fonte para as abreviaturas oficiais.

A numeração segue a ordem da primeira citação (\\cite{...}) no artigo.

Uso: python gerar_referencias.py artigo_aero2027_en.tex ../../references/references.bib referencias_aero.tex
"""

import re
import sys
from pathlib import Path


def read_entries(bib_text):
    """Lê as entradas do .bib, com campos entre chaves aninhadas ou macros simples."""
    entries = {}
    for match in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", bib_text):
        kind, key = match.group(1).lower(), match.group(2)
        i, depth = match.end(), 1
        while depth:                                   # fim da entrada
            depth += {"{": 1, "}": -1}.get(bib_text[i], 0)
            i += 1
        body = bib_text[match.end():i - 1]
        fields, j = {}, 0
        while True:
            m = re.compile(r"\s*(\w+)\s*=\s*").match(body, j)
            if not m:
                break
            name, j = m.group(1).lower(), m.end()
            if body[j] == "{":
                depth, start = 0, j
                while True:
                    depth += {"{": 1, "}": -1}.get(body[j], 0)
                    j += 1
                    if depth == 0:
                        break
                value = body[start + 1:j - 1]
            else:                                      # macro (ex.: month = mar) ou número
                m2 = re.compile(r"[^,]+").match(body, j)
                value, j = m2.group(0).strip(), m2.end()
            fields[name] = " ".join(value.split())
            m3 = re.compile(r"\s*,").match(body, j)
            if not m3:
                break
            j = m3.end()
        entries[key] = (kind, fields)
    return entries


def initials(given):
    out = []
    for part in given.split():
        pieces = [p for p in part.split("-") if p]
        out.append("-".join(p[0] + "." if not p.endswith(".") else p for p in pieces))
    return " ".join(out)


def person(name):
    name = name.strip()
    if name.startswith("{") and name.endswith("}"):    # autor institucional
        return name[1:-1]
    if "," in name:
        last, given = [s.strip() for s in name.split(",", 1)]
        return f"{initials(given)} {last}".strip()
    parts = name.split()
    return f"{initials(' '.join(parts[:-1]))} {parts[-1]}".strip()


def authors(field):
    names = [person(n) for n in re.split(r"\s+and\s+", field)]
    return ", ".join(names)


def venue(kind, f):
    if kind == "article":
        return f.get("journal", "")
    if kind == "inproceedings":
        return f.get("booktitle", "")
    if kind == "techreport":
        number = f.get("number")
        institution = f.get("institution", "")
        return f"{institution}, {number}" if number else institution
    if kind == "mastersthesis":
        return f"Master's thesis, {f.get('school', '')}"
    return f.get("howpublished", f.get("publisher", ""))


def item(kind, f):
    who, where = authors(f["author"]), venue(kind, f)
    if where.startswith(who):                          # autor institucional = instituição
        where = where[len(who):].lstrip(", ")
    parts = [who, where]
    if f.get("volume"):
        parts.append(r"\textbf{" + f["volume"] + "}")
    if f.get("pages"):
        parts.append(f["pages"].replace("--", " -- "))
    if not f.get("volume") and not f.get("pages"):
        if f.get("doi"):
            parts.append(r"doi:\nolinkurl{" + f["doi"] + "}")
        elif f.get("url"):
            parts.append(r"\url{" + f["url"] + "}")
    parts.append(f"({f['year']})")
    return ", ".join(p for p in parts if p) + "."


def main(tex_path, bib_path, out_path):
    tex = Path(tex_path).read_text(encoding="utf-8")
    tex = re.sub(r"(?m)(?<!\\)%.*$", "", tex)         # ignora comentários (não o \% escapado)
    order = []
    for group in re.findall(r"\\cite\{([^}]+)\}", tex):
        for key in (k.strip() for k in group.split(",")):
            if key not in order:
                order.append(key)
    entries = read_entries(Path(bib_path).read_text(encoding="utf-8"))
    missing = [k for k in order if k not in entries]
    if missing:
        raise SystemExit(f"chaves ausentes do .bib: {missing}")
    lines = ["% Gerado por gerar_referencias.py a partir de references/references.bib.",
             "% Não editar à mão.", r"\begin{thebibliography}{99}"]
    for key in order:
        kind, fields = entries[key]
        lines.append(rf"\bibitem{{{key}}} {item(kind, fields)}")
    lines.append(r"\end{thebibliography}")
    Path(out_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{out_path}: {len(order)} referências")


if __name__ == "__main__":
    main(*sys.argv[1:4])
