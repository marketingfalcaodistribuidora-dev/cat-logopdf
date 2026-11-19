"""Mede o texto real de cada produto nos modelos de card do Affinity.

Lê a planilha oficial (única fonte) e, com as métricas da fonte Arial, indica o
menor modelo em que todos os campos cabem. Não altera nenhum dado.
Saída: JSON com o resumo e CSV com o modelo indicado para cada produto.
"""
import csv
import collections
import json
import os
import re
import sys

import openpyxl
from PIL import Image, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "analise_cards")
PT = 300 / 72  # documento em 300 dpi
FONTES = {
    "r": "C:/Windows/Fonts/arial.ttf",
    "b": "C:/Windows/Fonts/arialbd.ttf",
    "bi": "C:/Windows/Fonts/arialbi.ttf",
}
_f = {k: ImageFont.truetype(v, 200) for k, v in FONTES.items()}
_cache = {}


def larg(txt, estilo, pt):
    k = (txt, estilo)
    if k not in _cache:
        _cache[k] = _f[estilo].getlength(txt) / 200
    return _cache[k] * pt * PT


def linhas(txt, estilo, pt, largura):
    """Quantas linhas o texto ocupa na largura dada (px a 300 dpi)."""
    total = 0
    for par in str(txt).split("\n"):
        atual = 0.0
        n = 1
        esp = larg(" ", estilo, pt)
        for p in par.split():
            w = larg(p, estilo, pt)
            if w > largura:  # palavra maior que a linha quebra no meio
                n += int(w // largura)
                w = w % largura
            if atual and atual + esp + w > largura:
                n += 1
                atual = w
            else:
                atual += (esp if atual else 0) + w
        total += n
    return total


def altura(blocos, largura):
    return sum(linhas(t, e, pt, largura) * pt * PT * 1.2 for t, e, pt in blocos if t)


# Medidas lidas de Modelo_Miolo (layout 4 x 5) e MODELOS_CARDS (modelos 1 a 4)
MODELOS = {
    "A_4x5": dict(por_pagina=20, larg=477, alt=176, pt_d=7, pt_t=6.5),
    "B_3x3": dict(por_pagina=9, larg=640, alt=340, pt_d=9.5, pt_t=7.5),
    "C_3x3_aplicacao": dict(por_pagina=9, larg=640, alt=520, pt_d=9.5, pt_t=6.5),
}
FAIXA_UTIL = 400  # largura útil da faixa amarela inclinada (px)
SELO_UTIL = 100  # largura útil do selo azul de marca (px)
LISTA_LINHAS = 8  # linhas de variação do modelo 4 (180 x 47 mm)


def blocos(p, m):
    return [
        (p["descricao"], "b", m["pt_d"]),
        ("Aplicação: " + p["aplicacao"] if p["aplicacao"] else "", "r", m["pt_t"]),
        ("Ref.: " + p["ref"] if p["ref"] else "", "r", m["pt_t"]),
        ("Similares: " + p["similares"] if p["similares"] else "", "r", m["pt_t"]),
        (p["info"], "r", m["pt_t"]),
    ]


def classificar(p):
    if p["variacoes"]:
        n = len([l for l in p["variacoes"].split("\n") if l.strip()])
        return "D_lista" if n <= LISTA_LINHAS else "E_lista_longa"
    cod_ok = larg("cód." + p["codigo"], "bi", 10) <= FAIXA_UTIL
    selo_ok = not p["marca"] or larg(p["marca"], "b", 6) <= SELO_UTIL
    for nome, m in MODELOS.items():
        if nome == "A_4x5" and not (cod_ok and selo_ok):
            continue
        if altura(blocos(p, m), m["larg"]) <= m["alt"]:
            return nome
    return "F_nao_cabe"


def carregar():
    wb = openpyxl.load_workbook(os.path.join(BASE, "Catalogo_Falcao_2026.xlsx"))
    ws = wb["Todos os produtos"]
    saida = []
    for r in ws.iter_rows(min_row=2):
        v = ["" if c.value is None else str(c.value).strip() for c in r]
        saida.append(dict(
            categoria=v[0], montadora=v[1], marca=v[2], tipo=v[3], codigo=v[4],
            descricao=v[5], ref=v[6], variacoes=v[7], similares=v[8], aplicacao=v[9],
            info=v[10], foto=(r[11].hyperlink.target if r[11].hyperlink else ""), paginas=v[12],
        ))
    return saida


def main():
    os.makedirs(SAIDA, exist_ok=True)
    P = carregar()
    for p in P:
        p["modelo"] = classificar(p)
    cont = collections.Counter(p["modelo"] for p in P)

    # Trocas de modelo dentro de cada capítulo, na ordem de leitura
    trocas, blocos_cap = 0, collections.Counter()
    ordem = collections.defaultdict(list)
    for p in P:
        ordem[p["categoria"]].append(p["modelo"])
    for cat, seq in ordem.items():
        n = 1 + sum(1 for a, b in zip(seq, seq[1:]) if a != b)
        blocos_cap[cat] = n
        trocas += n

    fotos = [os.path.join(BASE, p["foto"]) for p in P if p["foto"]]
    baixa, tam = 0, 0
    for f in sorted(set(fotos)):
        tam += os.path.getsize(f)
        with Image.open(f) as im:
            if min(im.size) < 260:  # 22 mm a 300 dpi
                baixa += 1

    resumo = dict(
        produtos=len(P),
        modelos=dict(cont),
        sem_marca=sum(not p["marca"] for p in P),
        sem_aplicacao=sum(not p["aplicacao"] for p in P),
        sem_ref=sum(not p["ref"] for p in P),
        com_info=sum(bool(p["info"]) for p in P),
        com_similares=sum(bool(p["similares"]) for p in P),
        sem_montadora=sum(not p["montadora"] for p in P),
        sem_foto=sum(not p["foto"] for p in P),
        codigo_nao_cabe_faixa=sum(larg("cód." + p["codigo"], "bi", 10) > FAIXA_UTIL for p in P),
        marca_nao_cabe_selo=sum(bool(p["marca"]) and larg(p["marca"], "b", 6) > SELO_UTIL for p in P),
        blocos_de_mesclagem_parte2=trocas,
        capitulos_com_um_so_modelo=sum(1 for n in blocos_cap.values() if n == 1),
        maior_fragmentacao=blocos_cap.most_common(5),
        fotos_arquivos=len(set(fotos)),
        fotos_mb=round(tam / 1048576),
        fotos_abaixo_300dpi_no_quadro=baixa,
    )
    with open(os.path.join(SAIDA, "resumo.json"), "w", encoding="utf-8") as f:
        json.dump(resumo, f, ensure_ascii=False, indent=1)
    with open(os.path.join(SAIDA, "modelo_por_produto.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["categoria", "codigo", "descricao", "modelo"])
        for p in P:
            w.writerow([p["categoria"], p["codigo"], p["descricao"], p["modelo"]])
    print(json.dumps(resumo, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
