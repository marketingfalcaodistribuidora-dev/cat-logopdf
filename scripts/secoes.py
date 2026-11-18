"""Páginas de lista dividida em caixas (molduras): cada caixa = 1 produto, os códigos da lista viram itens.
ler(p, titulos=None): usa tabela_livre.ler_pagina para código+descrição e reagrupa pela menor moldura do raw que contém o código.
Título da caixa = maior texto não-código da caixa (ou titulos[card_id]); foto = maior imagem da caixa."""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from capitulos import WORK  # noqa: E402
from tabela_livre import _spans, ler_pagina  # noqa: E402


def caixas(p):
    raw = json.load(open(os.path.join(WORK, "raw", f"p{p:03d}.json"), encoding="utf-8"))
    return [c for c in raw["cards"] if c["id"]]


def _dentro(r, x, y):
    return r[0] - 1 <= x <= r[2] + 1 and r[1] - 1 <= y <= r[3] + 1


def ler(p, titulos=None, min_tit=10, **kw):
    titulos = titulos or {}
    sp, imgs = _spans(p)
    cx = caixas(p)
    itens = ler_pagina(p, **kw)
    out = []
    for it in itens:
        bx = it.get("_bbox") or [0, 0, 0, 0]
        x, y = bx[0] + 2, bx[1] + 2
        cand = [c for c in cx if _dentro(c["rect"], x, y)]
        c = min(cand, key=lambda c: (c["rect"][2] - c["rect"][0]) * (c["rect"][3] - c["rect"][1])) if cand else None
        it = dict(it)
        if c:
            r = c["rect"]
            it["card"] = c["id"]
            if c["id"] in titulos:
                tit = titulos[c["id"]]
            else:
                tx = [s for s in sp if _dentro(r, (s["x"] + s["x1"]) / 2, s["y"]) and s["size"] >= min_tit
                      and not re.fullmatch(r"[\d\s]+", s["t"].strip())]
                big = max((s["size"] for s in tx), default=0)
                tit = " ".join(s["t"].strip() for s in sorted([s for s in tx if s["size"] >= big - 0.5], key=lambda s: (s["y"], s["x"])))
            it["_titulo"] = re.sub(r"\s+", " ", tit).strip()
            fotos = [b for b in imgs if _dentro(r, (b[0] + b[2]) / 2, (b[1] + b[3]) / 2) and (b[2] - b[0]) * (b[3] - b[1]) > 400]
            if fotos:
                it["foto_spec"] = {"rect": [round(v, 1) for v in max(fotos, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))]}
            it.pop("_nao_agrupar", None)
        out.append(it)
    return out
