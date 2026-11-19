"""Compara o texto do PDF original com o que entrou nos dados de cada produto.

Lista as linhas do PDF cujas palavras não aparecem nos dados da página e as associa
ao código de produto mais próximo. Não altera nenhum dado.
"""
import collections
import csv
import glob
import json
import os
import re
import sys
import unicodedata

import fitz

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = glob.glob(os.path.join(BASE, "_fonte", "*.pdf"))[0]
SAIDA = os.path.join(BASE, "Catalogo_Atualizado_dados", "auditoria_texto.csv")
CAMPOS = ("codigo", "descricao", "cod_ref", "variacoes", "aplicacao", "info", "marca", "montadora", "itens", "tipo")


def tokens(t):
    t = "".join(c for c in unicodedata.normalize("NFD", str(t or "")) if unicodedata.category(c) != "Mn").upper()
    return re.findall(r"[A-Z0-9]+", t)


def main():
    por_pag = collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(BASE, "dados", "cap*.json"))):
        if not re.fullmatch(r"cap\d+\.json", os.path.basename(f)):
            continue
        for p in json.load(open(f, encoding="utf-8")):
            for n in re.findall(r"\d+", str(p["pagina"])):
                por_pag[int(n)].append(p)

    doc = fitz.open(PDF)
    perdas = collections.defaultdict(list)
    linhas_total = linhas_perdidas = 0
    for n, prods in sorted(por_pag.items()):
        pg = doc[n - 1]
        conhecidos = set()
        for p in prods:
            for c in CAMPOS:
                conhecidos.update(tokens(p.get(c)))
        codigos = []
        for p in prods:
            for c in re.findall(r"[0-9@][0-9A-Za-z]{3,}", str(p["codigo"])):
                for r in pg.search_for(c)[:2]:
                    codigos.append((r, p))
        if not codigos:
            continue
        for bloco in pg.get_text("dict")["blocks"]:
            for lin in bloco.get("lines", []):
                texto = " ".join(s["text"] for s in lin["spans"]).strip()
                x0, y0, x1, y1 = lin["bbox"]
                if y0 < 85 or y0 > 812:
                    continue
                tk = [t for t in tokens(texto) if len(t) > 1]
                if len(tk) < 2 or sum(ch.isalpha() for ch in texto) < 8:
                    continue
                linhas_total += 1
                if sum(t in conhecidos for t in tk) / len(tk) >= 0.6:
                    continue
                linhas_perdidas += 1
                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2

                def dist(item):
                    r = item[0]
                    dy = 0 if r.y0 <= cy <= r.y1 else min(abs(cy - r.y0), abs(cy - r.y1))
                    dx = 0 if r.x0 <= cx <= r.x1 else min(abs(cx - r.x0), abs(cx - r.x1))
                    return dx * 1.2 + dy
                alvo = min(codigos, key=dist)[1]
                perdas[(n, str(alvo["codigo"]), str(alvo["descricao"]))].append(texto)

    with open(SAIDA, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pagina_pdf", "codigo", "descricao", "linhas_faltando", "caracteres_faltando", "texto_faltando"])
        for (n, c, d), ls in sorted(perdas.items()):
            w.writerow([n, c, d, len(ls), sum(map(len, ls)), " / ".join(ls)])

    por_faixa = collections.Counter()
    por_cap = collections.Counter()
    for (n, c, d), ls in perdas.items():
        tam = sum(map(len, ls))
        por_faixa["ate 40" if tam <= 40 else "41 a 150" if tam <= 150 else "151 a 400" if tam <= 400 else "mais de 400"] += 1
        por_cap[n // 50 * 50] += 1
    print(json.dumps(dict(paginas=len(por_pag), linhas_analisadas=linhas_total, linhas_faltando=linhas_perdidas,
                          produtos_afetados=len(perdas), por_tamanho=por_faixa,
                          por_faixa_de_pagina=sorted(por_cap.items())), ensure_ascii=False))
    for k, ls in perdas.items():
        if k[1] == "6070004":
            print(k, ls)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
