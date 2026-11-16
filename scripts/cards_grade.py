"""Leitor de páginas de cards em grade (molduras do PDF sobrepostas): ler(p) -> registros.
Grade pelas bordas das molduras; título (fonte >= 9,5) = descrição; texto rotulado (Subst. o cód. original, Material,
Dimensões, Aplicação, Compatível, MESMA TH, SUPORTE REI...) separado em referência / similares / aplicação / informações."""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from capitulos import WORK  # noqa: E402
from tabela_livre import _spans  # noqa: E402

_LAB = re.compile(r"(Subst\.?\s*(?:o\s*)?c[óo]d\.?\s*original\s*:?|Substitui\s*(?:o\s*)?(?:N[ºo°]\.?\s*)?Orig(?:inal)?\.?\s*:?|"
                  r"REF\.?\s*ORIG(?:INAL)?\s*:?|Material\s*:|Dimens[õo]es?\s*:|DIMENS[ÃA]O\s*:|Aplica[çc](?:[ãa]o|[õo]es)\s*:|"
                  r"Compat[ií]vel(?:\s*com\s*o\s*ve[ií]culo)?\s*:?|Produtos\s*relacionados\s*:|Embalagem\s*:|C[ÓO]D\s*:|"
                  r"MESMA\s+TH\s*-?|SUPORTE\s+REI\b)", re.I)


def _linhas(ss, tol=2.4):
    out = []
    for s in sorted(ss, key=lambda s: (s["y"], s["x"])):
        if out and abs(out[-1][0] - s["y"]) < tol:
            out[-1][1].append(s)
        else:
            out.append([s["y"], [s]])
    return [" ".join(x["t"].strip() for x in sorted(l[1], key=lambda s: s["x"])) for l in out]


def _grade(big):
    linhas = []
    for s in sorted(big, key=lambda s: s["y"]):
        if linhas and s["y"] - linhas[-1][-1]["y"] < 15:
            linhas[-1].append(s)
        else:
            linhas.append([s])
    ncol = max(len(l) for l in linhas)
    larg = 545 / ncol
    tops = [min(s["y"] for s in l) - 12 for l in linhas] + [806]
    out = {}
    for i, l in enumerate(linhas):
        for s in l:
            k = min(int(((s["x"] + s["x1"]) / 2 - 25) // larg), ncol - 1)
            out[id(s)] = [25 + k * larg, tops[i], 25 + (k + 1) * larg, tops[i + 1]]
    return out


def ler(p, grade=None, tam_cod=6, idx=None, marca=""):
    idx = idx or {}
    """grade: None = molduras do PDF (com fallback), True = grade inferida pelos códigos."""
    raw = json.load(open(os.path.join(WORK, "raw", f"p{p:03d}.json"), encoding="utf-8"))
    sp, imgs = _spans(p)
    big = [s for s in sp if s["red"] and re.fullmatch(r"\d{7,9}", s["t"]) and s["size"] >= tam_cod]
    # códigos secundários (MESMA TH / SUPORTE REI / IABV) não são âncora
    sec = [s for s in sp if re.search(r"MESMA\s*TH|SUPORTE\s*REI|IABV\s*$|^IABV|REF\.?\s*ORIG|REFER[ÊE]NCIA|Subst", s["t"], re.I)]
    big = [s for s in big if not any(abs(x["y"] - s["y"]) < 14 and abs(x["x"] - s["x"]) < 140 and x["y"] <= s["y"] + 7
                                     and re.search(r"SUPORTE\s*REI|MESMA", x["t"], re.I) and x["x"] <= s["x"] + 40
                                     for x in sec)
           and not any(re.search(r"REF|Subst|REFER", x["t"], re.I) and (abs(x["y"] - s["y"]) < 4 and x["x"] < s["x"] and s["x"] - x["x1"] < 30
                                                                       or 0 < s["y"] - x["y"] < 13 and abs(x["x"] - s["x"]) < 12 and s["size"] < 10)
                       for x in sec)]
    cards = [c for c in raw["cards"] if c["id"] != 0]

    def dentro(r, s):
        return r[0] - 1 <= (s["x"] + s["x1"]) / 2 <= r[2] + 1 and r[1] - 1 <= s["y"] + 3 <= r[3] + 1
    rect_de = {}
    if not grade:
        # grade pelas bordas de todas as molduras (as molduras do PDF se sobrepõem)
        def _clus(vs):
            out = []
            for v in sorted(vs):
                if out and v - out[-1][-1] < 6:
                    out[-1].append(v)
                else:
                    out.append([v])
            return [sum(c) / len(c) for c in out]
        xs = _clus([c["rect"][0] for c in cards] + [c["rect"][2] for c in cards])
        ys = _clus([c["rect"][1] for c in cards] + [c["rect"][3] for c in cards])
        for s in big:
            cx, cy = (s["x"] + s["x1"]) / 2, s["y"] + 3
            xa = [x for x in xs if x <= cx]
            xb = [x for x in xs if x > cx]
            ya = [y for y in ys if y <= cy]
            yb = [y for y in ys if y > cy]
            if xa and xb and ya and yb:
                rect_de[id(s)] = [max(xa), max(ya), min(xb), min(yb)]
    g = _grade(big) if big else {}
    regs = []
    for n, s in enumerate(sorted(big, key=lambda s: (round(s["y"] / 20), s["x"]))):
        x0, y0, x1, y1 = rect_de.get(id(s)) or g[id(s)]
        cs = [t for t in sp if t is not s and x0 - 1 <= (t["x"] + t["x1"]) / 2 <= x1 + 1 and y0 - 1 <= t["y"] + t["size"] / 2 <= y1 + 1]
        codigo = s["t"]
        tit_tam = sorted({round(t["size"]) for t in cs if not t["red"] and t["y"] > s["y"] - 4}, reverse=True)
        titulo = [t for t in cs if not t["red"] and t["size"] >= 9.5 and t["y"] >= s["y"] - 30
                  and not _LAB.search(t["t"]) and t["y"] <= s["y"] + 45]
        resto = [t for t in cs if t not in titulo]
        tit = re.sub(r"\s+", " ", " ".join(_linhas(titulo))).strip()
        txt = re.sub(r"\s+", " ", " ".join(_linhas(resto))).strip()
        partes = _LAB.split(txt)
        campos = {"_": [partes[0].strip()]}
        for k in range(1, len(partes) - 1, 2):
            lab = re.sub(r"[^a-z]", "", partes[k].lower())[:5]
            campos.setdefault(lab, []).append(partes[k + 1].strip(" -/:"))
        ref = campos.get("subst", []) + campos.get("refor", []) + campos.get("subst", [])[:0]
        ref = [x for x in dict.fromkeys(ref) if x]
        sim = [f"MESMA TH {x.split()[0]}" for x in campos.get("mesma", []) if x]
        sim += [f"Suporte Rei {x.split()[0]}" for x in campos.get("supor", []) if x]
        sim += [f"Cód. {x.split()[0]}" for x in campos.get("cd", []) if x]
        apl = campos.get("aplic", [])
        info = []
        for lab, nome in (("mater", "Material"), ("dimen", "Dimensões"), ("compa", "Compatível"), ("produ", "Produtos relacionados"),
                          ("embal", "Embalagem")):
            info += [f"{nome}: {x}" for x in campos.get(lab, []) if x]
        info = [x for x in campos["_"] if x] + info
        # sobras após o 1º token de MESMA/SUPORTE REI/CÓD
        for lab in ("mesma", "supor", "cd"):
            for x in campos.get(lab, []):
                sobra = " ".join(x.split()[1:])
                if sobra:
                    info.append(sobra)
        fotos = [b for b in imgs if x0 - 2 <= (b[0] + b[2]) / 2 <= x1 + 2 and y0 - 2 <= (b[1] + b[3]) / 2 <= y1 + 2]
        foto = max(fotos, key=lambda b: (b[2] - b[0]) * (b[3] - b[1])) if fotos else None
        desc = (re.sub(r"^-\s*\d{3,5}(-\d+)?\s+", "", idx[codigo]).strip(" .'") if codigo in idx
                else re.sub(r"^-\s*\d{3,5}(-\d+)?\s+", "", tit).strip(" .'"))
        regs.append(dict(pagina=p, card=n + 1, codigo=codigo, descricao=desc, marca=marca,
                         cod_ref=" / ".join(ref), variacoes=" / ".join(dict.fromkeys(sim)), aplicacao=" / ".join(apl),
                         info=" | ".join(x for x in info if x), _nao_agrupar=True, foto_spec={"rect": foto} if foto else None,
                         _texto=tit + " " + txt))
    return regs


