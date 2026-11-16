"""Leitura de páginas em 'tabela livre' (listas de códigos + caixinhas de acessórios), sem depender das molduras.

ler_pagina(p, ...) -> lista de registros (pagina, card, codigo, descricao, _titulo, foto_spec)
  - linha "CÓDIGO  descrição" -> item de lista; linhas consecutivas alinhadas formam um grupo (1 produto com variações)
  - código sem descrição na mesma linha -> acessório; descrição = texto próximo (acima/abaixo, mesma coluna)
Uso de depuração: python tabela_livre.py <pag> <saida.png>  (desenha grupos/acessórios e as fotos escolhidas)
"""
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from capitulos import PDF, WORK  # noqa: E402

CODE = re.compile(r"^\d{5,12}$")


_CIRIL = str.maketrans("хХвВаАеЕоОсСрРтТмМнНк", "xXBBaAeEoOcCpPTTMMHHk")  # letras cirílicas parecidas usadas no PDF


def _spans(p):
    raw = json.load(open(os.path.join(WORK, "raw", f"p{p:03d}.json"), encoding="utf-8"))
    vistos, out, imgs = set(), [], []
    for c in raw["cards"]:
        for ln in c["lines"]:
            for s in ln:
                k = (s["t"], round(s["x"]), round(s["y"]))
                if s["t"].strip() and k not in vistos:
                    vistos.add(k)
                    out.append(dict(s, t=s["t"].strip().translate(_CIRIL)))
        for i in c["images"]:
            b = tuple(round(v, 1) for v in i["bbox"])
            if b not in [tuple(x) for x in imgs]:
                imgs.append(list(b))
    # junta trechos vermelhos numéricos colados (ex.: "27420" + "155")
    out.sort(key=lambda s: (round(s["y"]), s["x"]))
    res = []
    for s in out:
        u = res[-1] if res else None
        if (u and u["red"] and s["red"] and abs(u["y"] - s["y"]) < 1.5 and 0 <= s["x"] - u["x1"] < 4
                and re.fullmatch(r"[\d ]+", u["t"]) and re.fullmatch(r"[\d ]+", s["t"])):
            res[-1] = dict(u, t=u["t"] + s["t"], x1=s["x1"])
        else:
            res.append(s)
    return res, imgs


_DXL = re.compile(r"(?<![\d.,/])([\d.,/]+)(\s*MM)?\s*X\s*[\d.,/]+(?:\s+\d/\d+)?(?:\s*MM)?\b")


def _diam(desc):
    desc = re.sub(r"^10\.9\s+", "", desc)
    m = _DXL.search(desc)
    return m.group(1) if m else ""


def _is_code(s):
    return s["red"] and CODE.match(s["t"].replace(" ", ""))


def _titulo(descs):
    """Título do grupo: descrição mais comum sem o comprimento (ex.: 'PF ACO ... R INT - 10MM', 'INOX PF 06MM MA R INTEIRA')."""
    norm = []
    for d in descs:
        d = re.sub(r"^10\.9\s+", "", d)
        m = _DXL.search(d)
        if m:
            dm = m.group(1)
            if re.fullmatch(r"\d+", dm):
                dm = dm + ('"' if re.search(r"UNC|UNF|BSW|POL", d) else "MM")
            if m.start() == 0:
                norm.append(f"{d[m.end():].strip()} - {dm}")
            else:
                norm.append(re.sub(r"\s+", " ", d[:m.start()] + dm + d[m.end():]).strip())
        else:
            norm.append(d)
    tit, n = Counter(norm).most_common(1)[0]
    if n == 1 and len(norm) > 1:  # todas diferentes: o montar.py usa o prefixo comum das descrições
        return ""
    return tit


def ler_pagina(p, tol=2.6, gap_max=14, gap_primeiro=45, dif_tam=3.5, min_desc=6, ignorar=(), area=None, separar_diam=True):
    spans, imgs = _spans(p)
    if area:
        x0, y0, x1, y1 = area
        spans = [s for s in spans if x0 <= (s["x"] + s["x1"]) / 2 <= x1 and y0 <= s["y"] <= y1]
    codes = [s for s in spans if _is_code(s) and s["t"].replace(" ", "") not in ignorar]
    usados = set()
    itens, acess = [], []

    def linha(c, excl):
        lin = sorted([s for s in spans if s is not c and id(s) not in excl and abs(s["y"] - c["y"]) < tol
                      and s["x"] >= c["x1"] - 1], key=lambda s: s["x"])
        partes, xa = [], c["x1"]
        for s in lin:
            lim = gap_max if partes else gap_primeiro
            if _is_code(s) or s["x"] - xa > lim or (partes and abs(s["size"] - partes[0]["size"]) > 1.2)                     or (not partes and abs(s["size"] - c["size"]) > dif_tam):
                break
            partes.append(s)
            xa = s["x1"]
        txt = re.sub(r"\s+", " ", " ".join(s["t"] for s in partes)).strip(" |-–")
        return partes, txt

    def tem_desc(txt):
        return len(txt) >= min_desc and re.search(r"[A-Z]", txt, re.I)

    # 1ª passada: o que não tem descrição na mesma linha é acessório (caixinha);
    # linha isolada com texto curto (ex.: "ARR.LISA Z" da caixinha vizinha) também
    cand = []
    for c in codes:
        txt = linha(c, set())[1]
        (cand if tem_desc(txt) else acess).append((c, txt) if tem_desc(txt) else c)
    for c, txt in cand:
        vizinhos = [o for o, _ in cand if o is not c and abs(o["y"] - c["y"]) < 3.2 * max(4, c["size"])
                    and abs(o["x1"] - c["x1"]) < 12]
        if not vizinhos and len(txt) < 15:
            acess.append(c)
    # 2ª passada: textos ao redor de cada acessório ficam reservados para ele (o mais próximo)
    reserva = {id(c): [] for c in acess}
    for s in spans:
        if _is_code(s) or s["size"] >= 14 or (s["x1"] - s["x"]) >= 200:
            continue
        sx = (s["x"] + s["x1"]) / 2
        perto = [(abs(sx - (c["x"] + c["x1"]) / 2) + abs(s["y"] - c["y"]) * 0.5, c) for c in acess
                 if abs(sx - (c["x"] + c["x1"]) / 2) < 45 and -28 < s["y"] - c["y"] < 36]
        if perto:
            reserva[id(min(perto, key=lambda t: t[0])[1])].append(s)
    excl = {id(s) for v in reserva.values() for s in v}
    for c in sorted(codes, key=lambda s: (s["y"], s["x"])):
        if c in acess:
            continue
        partes, txt = linha(c, excl)
        if not tem_desc(txt):
            partes, txt = linha(c, set())
        for s in partes:
            usados.add(id(s))
        itens.append(dict(c=c, desc=txt, x=partes[0]["x"], y=c["y"], x1=max([c["x1"]] + [s["x1"] for s in partes])))
    # grupos: itens com o mesmo x e espaçamento regular
    grupos = []
    for it in sorted(itens, key=lambda i: (i["y"], i["x"])):
        for g in grupos:
            u = g[-1]
            if (abs(u["x"] - it["x"]) < 8 or abs(u["c"]["x"] - it["c"]["x"]) < 8) and 0 < it["y"] - u["y"] < 3.2 * max(4, u["c"]["size"])                     and (not separar_diam or _diam(u["desc"]) == _diam(it["desc"])):
                g.append(it)
                break
        else:
            grupos.append([it])
    out = []
    n = 0
    for g in sorted(grupos, key=lambda g: (g[0]["y"], g[0]["x"])):
        n += 1
        gx0, gy0 = min(i["x"] for i in g), min(i["y"] for i in g)
        gx1, gy1 = max(i["x1"] for i in g), max(i["y"] for i in g) + 8
        tit = _titulo([i["desc"] for i in g]) if len(g) > 1 else ""
        foto = _foto_grupo(imgs, gx0, gy0, gx1, gy1) or (max(imgs, key=lambda b: (b[2] - b[0]) * (b[3] - b[1])) if imgs else None)
        for i in g:
            out.append(dict(pagina=p, card=n, codigo=i["c"]["t"].replace(" ", ""), descricao=i["desc"], _titulo=tit,
                            foto_spec={"rect": foto} if foto else None, _bbox=[gx0, gy0, gx1, gy1]))
    for c in acess:
        n += 1
        cx = (c["x"] + c["x1"]) / 2
        viz = [s for s in reserva[id(c)] if id(s) not in usados]
        desc = re.sub(r"\s+", " ", " ".join(s["t"] for s in sorted(viz, key=lambda s: (round(s["y"]), s["x"])))).strip()
        foto = _foto_acess(imgs, c)
        out.append(dict(pagina=p, card=n, codigo=c["t"].replace(" ", ""), descricao=desc, _nao_agrupar=True,
                        foto_spec={"rect": foto} if foto else None, _bbox=[c["x"], c["y"], c["x1"], c["y"] + c["size"]]))
    return out


def _foto_grupo(imgs, x0, y0, x1, y1):
    """Maior imagem acima/ao lado da lista; entre as grandes, a mais à direita (à esquerda costuma ficar a chave de boca)."""
    cand = []
    for b in imgs:
        cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        a = (b[2] - b[0]) * (b[3] - b[1])
        if x0 - 30 <= cx <= x1 + 10 and y0 - 140 <= cy <= y1 and (b[2] - b[0]) < 300:
            cand.append((a, cx, b))
    if not cand:
        return None
    mx = max(a for a, _, _ in cand)
    return max([c for c in cand if c[0] >= 0.3 * mx], key=lambda c: c[1])[2]


def _foto_acess(imgs, c):
    """Imagem acima/abaixo do código (mesma coluna) ou, na falta, à esquerda na mesma altura."""
    cx, cy = (c["x"] + c["x1"]) / 2, c["y"]
    best, dist = None, 1e9
    for b in imgs:
        bx, by = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        if (b[2] - b[0]) >= 120:
            continue
        if abs(bx - cx) < 40 and abs(by - cy) < 55:
            d = abs(by - cy) + abs(bx - cx)
        elif abs(by - cy) < 30 and 0 < cx - bx < 140:
            d = 100 + (cx - bx)
        else:
            continue
        if d < dist:
            best, dist = b, d
    return best


if __name__ == "__main__":
    import pymupdf as fitz
    from PIL import Image, ImageDraw
    p, saida = int(sys.argv[1]), sys.argv[2]
    regs = ler_pagina(p)
    d = fitz.open(PDF)
    esc = 2.2
    pix = d[p - 1].get_pixmap(matrix=fitz.Matrix(esc, esc))
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    dr = ImageDraw.Draw(im)
    cores = ["blue", "green", "magenta", "orange", "purple", "brown"]
    for r in regs:
        cor = cores[r["card"] % len(cores)]
        x0, y0, x1, y1 = r["_bbox"]
        dr.rectangle([x0 * esc - 2, y0 * esc - 2, x1 * esc + 2, y1 * esc + 2], outline=cor, width=2)
        dr.text((x0 * esc - 18, y0 * esc), str(r["card"]), fill=cor)
        if r.get("foto_spec"):
            fx0, fy0, fx1, fy1 = r["foto_spec"]["rect"]
            dr.rectangle([fx0 * esc, fy0 * esc, fx1 * esc, fy1 * esc], outline=cor, width=1)
            dr.text((fx0 * esc + 2, fy0 * esc + 2), "F" + str(r["card"]), fill=cor)
    im.save(saida)
    for r in regs:
        print(r["card"], r["codigo"], "|", r.get("_titulo", ""), "|", r["descricao"])
