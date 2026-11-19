"""Planeja todas as páginas do catálogo em uma grade de 4 colunas (máximo 4 x 5).

Cada card usa o menor tamanho em que o texto cabe: 1, 2 ou 4 colunas.
Grava uma lista de operações de desenho por página, que o script do Affinity executa.
"""
import csv
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analisar_cards import BASE, altura, larg, linhas  # noqa: E402
from ordenar_catalogo import COLUNAS  # noqa: E402
from limpar_notas import limpar, sem_lancamento  # noqa: E402
import ajustes_cards  # noqa: E402

DADOS = os.path.join(BASE, "Catalogo_Atualizado_dados")
PAGINAS = os.path.join(DADOS, "paginas")
IMG = os.path.join(DADOS, "img")
AREA_L, AREA_A = 2126, 2988
CW, GX, GY, MIN_H = 482, 66, 58, 540
PX = 300 / 72
AM, AZ, PT, BR, CZ, PR = [245, 207, 24], [15, 40, 255], [17, 17, 17], [255, 255, 255], [243, 243, 243], [16, 16, 16]
fotos = {}


def largura(span):
    return span * CW + (span - 1) * GX


def paragrafos(p):
    pares = []
    if p.get("montadora_exibida"):
        pares.append("Montadora: " + p["montadora_exibida"])
    for rotulo, campo in (("Aplicação: ", "aplicacao"), ("Ref.: ", "ref"), ("Similares: ", "similares"), ("", "info")):
        valor = limpar(p[campo])
        if valor:
            pares.append(rotulo + valor)
    return pares


ROTULO = re.compile(r"^\s*[A-Za-zÀ-ÿ][^:|]{0,34}:(?=\s|$)")


def partes_rotulo(seg):
    """Separa os rótulos do início do trecho (ex.: 'Similares: Conversão:') do valor."""
    rotulos = ""
    resto = seg
    for _ in range(2):
        m = ROTULO.match(resto)
        if not m or len(m.group(0).split()) > 5 or m.group(0).strip().lower().startswith("http"):
            break
        rotulos += m.group(0)
        resto = resto[m.end():]
    return rotulos, resto


def rotulos(texto, pt):
    """Parágrafo com os rótulos dos campos em negrito; o texto não é alterado."""
    runs = []
    for i, seg in enumerate(texto.split(" | ")):
        if i:
            runs.append([" | ", "r", pt, PT])
        rot, resto = partes_rotulo(seg)
        if rot:
            runs.append([rot, "b", pt, PT])
        if resto:
            runs.append([resto, "r", pt, PT])
    return runs


def folga(texto, pt=6.5):
    extra = 0
    for seg in texto.split(" | "):
        rot = partes_rotulo(seg)[0]
        if rot:
            extra += larg(rot, "b", pt) - larg(rot, "r", pt)
    return extra


def alt_extras(extras, w):
    return sum(linhas(e, "r", 6.5, w - folga(e)) * 6.5 * PX * 1.2 for e in extras) * 1.04 + 6 * len(extras)


def alt_texto(desc, extras, w):
    base = altura([(desc, "b", 7)], w) * 1.04 + 6 if desc else 0
    return base + alt_extras(extras, w)


def t(x, y, w, h, paras, nome, al="l"):
    return ["t", round(x), round(y), round(w), round(h), paras, nome, al]


def r(x, y, w, h, cor, nome, raio=0):
    return ["r", round(x), round(y), round(w), round(h), cor, nome, raio]


def faixa(x, y, w):
    d = 18
    return ["p", [[x + d, y], [x + w, y], [x + w - d, y + 68], [x, y + 68]], AM, "Faixa"]


def selo_info(marca):
    if not marca:
        return None
    w = larg(marca, "b", 6) + 28
    if w <= 213:
        return dict(w=max(119, w), h=58, n=1)
    n = linhas(marca, "b", 6, 185)
    return dict(w=213, h=58 + (n - 1) * 30, n=n)


def selo_ops(marca, s, x, y):
    if not s:
        return []
    return [r(x, y, s["w"], s["h"], AZ, "Selo marca", 10),
            t(x + 6, y + 16, s["w"] - 12, s["h"] - 18, [[[marca, "b", 6, BR]]], "Marca", "c")]


def foto_ops(p, x, y, w, h):
    cod = p["cod_original"]
    if not p["imagem"]:
        return [r(x, y, w, h, CZ, "Quadro de imagem " + cod),
                t(x, y + h / 2 - 16, w, 34, [[["IMAGEM INDISPONÍVEL", "b", 5, [120, 120, 120]]]], "Sem imagem", "c")]
    if p["imagem"] not in fotos:
        nome = "%05d%s" % (len(fotos), os.path.splitext(p["imagem"])[1].lower())
        fotos[p["imagem"]] = nome
        destino = os.path.join(IMG, nome)
        if not os.path.exists(destino):
            shutil.copyfile(p["imagem"], destino)
    return [["i", round(x), round(y), round(w), round(h), fotos[p["imagem"]], cod]]


def pt_cabe(txt, estilo, w):
    for pt in (10, 9, 8, 7):
        if larg(txt, estilo, pt) <= w:
            return pt
    return None


def pt_ajustado(txt, estilo, w):
    """Reduz a fonte só o necessário para o texto caber em uma linha."""
    return round(10 * w / larg(txt, estilo, 10) - 0.05, 1)


def card_simples(p):
    desc, extras = p["descricao"], paragrafos(p)
    rot = "cód." + p["cod_original"]
    s = selo_info(p["marca"])
    th1 = alt_texto(desc, extras, 477)
    pt1 = pt_cabe(rot, "bi", CW - 70)
    if pt1 and th1 <= 360:
        ix = 87 if not s else max(0, min(87, CW - s["w"] - 269))
        iw = 261 if not s else min(261, CW - s["w"] - 8 - ix)

        def draw(X, Y):
            return [faixa(X, Y, CW), t(X + 20, Y + 12, CW - 40, 50, [[[rot, "bi", pt1, PT]]], "Código", "c")] + \
                foto_ops(p, X + ix, Y + 88, iw, 263) + selo_ops(p["marca"], s, X + CW - s["w"] if s else 0, Y + 84) + \
                [t(X, Y + 362, 477, th1 + 12, [[[desc, "b", 7, PT]]] + [rotulos(e, 6.5) for e in extras],
                   "Dados " + p["cod_original"])]
        return dict(span=1, h=max(MIN_H, 362 + th1 + 12), draw=draw, modelo="1 coluna")
    for span, tw in ((2, 750), (4, 1846)):
        W = largura(span)
        pt2 = pt_cabe(rot, "bi", W - 70) or (pt_ajustado(rot, "bi", W - 70) if span == 4 else None)
        topo = 84 + (s["h"] + 10 if s else 4)
        th = alt_texto(desc, extras, tw)
        if pt2 and (th <= 760 or span == 4):
            def draw(X, Y, W=W, pt2=pt2, topo=topo, th=th, tw=tw):
                return [faixa(X, Y, W), t(X + 20, Y + 12, W - 40, 50, [[[rot, "bi", pt2, PT]]], "Código", "c")] + \
                    foto_ops(p, X, Y + 88, 261, 263) + selo_ops(p["marca"], s, X + W - s["w"] if s else 0, Y + 84) + \
                    [t(X + 280, Y + topo, tw, th + 12, [[[desc, "b", 7, PT]]] + [rotulos(e, 6.5) for e in extras],
                       "Dados " + p["cod_original"])]
            return dict(span=span, h=max(362, topo + th + 22), draw=draw, modelo="%d colunas" % span)
    raise ValueError("código sem espaço: " + p["cod_original"])


def linhas_lista(p):
    saida = []
    for l in p["variacoes"].split("\n"):
        if l.strip():
            c, _, d = l.partition(" – ")
            saida.append((c.strip(), d.strip()))
    return saida


GEO = {2: dict(fw=220, tx=236, tw=794, cw=210, dw=570), 4: dict(fw=283, tx=480, tw=1646, cw=340, dw=1280)}


def card_lista(p, itens, span, cont=False, com_extras=True):
    g, W = GEO[span], largura(span)
    titulo = p["descricao"] + (" (continuação)" if cont else "")
    pt = pt_cabe(titulo, "bi", W - 80)
    if pt is None:
        if span < 4:
            return None
        pt = pt_ajustado(titulo, "bi", W - 80)
    s = selo_info(p["marca"])
    y = 136
    tabela = []
    for c, d in itens:
        h = max(1, linhas(d, "r", 7, g["dw"])) * 34 + 8
        tabela.append((c, d, y, h))
        y += h
    extras = paragrafos(p) if com_extras else []
    eh = alt_extras(extras, g["tw"]) if extras else 0
    minimo = 88 + g["fw"] + (s["h"] + 18 if s else 12)
    H = max(minimo, y + (eh + 16 if extras else 0) + 16)

    def draw(X, Y):
        ops = [faixa(X, Y, W), t(X + 34, Y + 12, W - 70, 50, [[[titulo, "bi", pt, PT]]], "Título")]
        ops += foto_ops(p, X, Y + 88, g["fw"], g["fw"]) + selo_ops(p["marca"], s, X, Y + 88 + g["fw"] + 8)
        tx = X + g["tx"]
        ops += [r(tx, Y + 88, g["tw"], 42, PT, "Cabeçalho tabela"),
                t(tx + 12, Y + 96, g["cw"], 30, [[["CÓDIGO", "b", 6.5, BR]]], "Col código"),
                t(tx + g["cw"] + 12, Y + 96, g["dw"], 30, [[["DESCRIÇÃO", "b", 6.5, BR]]], "Col descrição")]
        for i, (c, d, ry, h) in enumerate(tabela):
            if i % 2:
                ops.append(r(tx, Y + ry - 3, g["tw"], h, CZ, "Linha"))
            ops.append(t(tx + 12, Y + ry, g["cw"], h, [[[c, "bi", 7, PT]]], "Cód " + c))
            if d:
                ops.append(t(tx + g["cw"] + 12, Y + ry, g["dw"], h, [[[d, "r", 7, PT]]], "Desc " + c))
        if extras:
            ops.append(t(tx, Y + y + 10, g["tw"], eh + 12, [rotulos(e, 6.5) for e in extras],
                         "Dados " + p["cod_original"]))
        return ops
    return dict(span=span, h=H, draw=draw, modelo="lista %d colunas" % span)


def cards_de(p):
    if not p["variacoes"]:
        return [card_simples(p)]
    itens = linhas_lista(p)
    c = card_lista(p, itens, 2)
    if c and c["h"] <= 1100:
        return [c]
    c = card_lista(p, itens, 4)
    if c["h"] <= AREA_A:
        return [c]
    partes, atual, soma = [], [], 0
    for it in itens:
        h = max(1, linhas(it[1], "r", 7, GEO[4]["dw"])) * 34 + 8
        if soma + h > AREA_A - 420:
            partes.append(atual)
            atual, soma = [], 0
        atual.append(it)
        soma += h
    partes.append(atual)
    return [card_lista(p, q, 4, cont=i > 0, com_extras=i == len(partes) - 1) for i, q in enumerate(partes)]


def abertura(cap, x0):
    """Capa do capítulo: faixa amarela em diagonal, nome grande centralizado e logo no rodapé."""
    nome = cap["nome"]
    pt, n = 120, 1
    for pt in (120, 110, 100, 90, 80, 72, 64, 58, 52, 46, 40):
        n = linhas(nome, "bi", pt, 1960)
        palavra_cabe = max(larg(w, "bi", pt) for w in nome.split()) <= 1960  # nunca quebrar no meio da palavra
        if palavra_cabe and n <= 3 and n * pt * PX * 1.15 <= 1150:
            break
    alt = n * pt * PX * 1.15
    y = 2230 - alt / 2
    return [r(x0, 0, 2480, 3508, PR, "Abertura fundo"),
            ["p", [[x0, 0], [x0 + 2480, 0], [x0 + 2480, 820], [x0, 1420]], AM, "Abertura diagonal"],
            ["p", [[x0, 1520], [x0 + 2480, 920], [x0 + 2480, 962], [x0, 1562]], AM, "Abertura faixa"],
            t(x0 + 142, y - 330, 2196, 260, [[["//", "bi", 60, AM]]], "Abertura marca", "c"),
            ["h", round(x0 + 142), round(y), 2196, round(alt + 40), [[[nome, "bi", pt, BR]]], "Capítulo: " + nome, "c"],
            r(x0 + 980, y + alt + 90, 520, 18, AM, "Abertura filete"),
            ["logo", x0 + 852, 3090]]


def arte_final(x0, nome):
    return [r(x0, 0, 2480, 3508, PR, nome + " fundo"),
            ["p", [[x0, 0], [x0 + 2480, 0], [x0 + 2480, 700], [x0, 1620]], AM, nome + " diagonal"],
            t(x0 + 142, 1900, 2196, 110, [[["CATÁLOGO 2027", "b", 20, BR]]], nome + " título", "r"),
            t(x0 + 142, 2030, 2196, 170, [[["LINHA PESADA", "bi", 36, AM]]], nome + " linha", "r"),
            r(x0 + 1538, 2230, 800, 12, AM, nome + " filete"),
            t(x0 + 142, 2270, 2196, 100, [[["Autopeças para caminhões e carretas", "r", 18, BR]]], nome + " subtítulo", "r"),
            t(x0 + 142, 3080, 1200, 210, [[["0800 7038260", "r", 16, AM]], [["75 3622-8260", "r", 16, AM]]], nome + " contato"),
            ["logo", x0 + 1560, 3090]]


def titulo_pagina(nome, x0):
    return t(x0 + 142, 95, 2126, 135, [[["//", "bi", 24, AM], [nome, "bi", 20, [8, 10, 10]], ["//", "bi", 24, AM]]],
             "Título da seção")


def x_pagina(p):
    return 0 if p % 2 == 1 else 2480


def main():
    arq = json.load(open(os.path.join(DADOS, "catalogo_ordenado.json"), encoding="utf-8"))
    shutil.rmtree(IMG, ignore_errors=True)  # os nomes dependem da ordem dos capítulos
    for pasta in (PAGINAS, IMG):
        os.makedirs(pasta, exist_ok=True)
    for f in os.listdir(PAGINAS):
        os.remove(os.path.join(PAGINAS, f))

    for cap in arq["capitulos"]:
        cap["nome"] = cap["nome"].replace("Lançamentos - Suportes de Mola", "Suportes de Mola")
    for l in arq["linhas"]:
        l["descricao"] = sem_lancamento(l["descricao"])
        l["variacoes"] = "\n".join(sem_lancamento(x) for x in l["variacoes"].split("\n"))
    por_cap = {}
    for l in arq["linhas"]:
        por_cap.setdefault(l["capitulo_num"], []).append(l)

    # Cada capítulo vira uma lista de páginas (linhas de cards já posicionadas)
    planos, avisos = [], []
    for cap in arq["capitulos"]:
        paginas, linhas_pag, y = [], [], 0
        fila, usado = [], 0

        def fecha():
            nonlocal fila, usado, linhas_pag, y
            if not fila:
                return
            alt = max(c["h"] for c, _ in fila)
            if y + alt > AREA_A:
                paginas.append(linhas_pag)
                linhas_pag, y = [], 0
            linhas_pag.append((y, list(fila)))
            y += alt + GY
            fila, usado = [], 0

        for l in por_cap[cap["num"]]:
            for c in cards_de(l):
                if c["h"] > AREA_A:
                    avisos.append("%s: card maior que a página" % l["cod_original"])
                if usado + c["span"] > 4:
                    fecha()
                fila.append((c, l))
                usado += c["span"]
        fecha()
        if linhas_pag:
            paginas.append(linhas_pag)
        planos.append(dict(cap=cap, paginas=paginas))

    entradas = len(planos) + 2
    pags_indice = max(1, -(-entradas // 128))
    p = 2 + pags_indice
    for pl in planos:
        pl["inicio"] = p
        p += 1 + len(pl["paginas"])
    total = p + 1  # última página: fundo

    def grava(n, ops):
        ops = ajustes_cards.aplicar(ops)
        with open(os.path.join(PAGINAS, "%05d.json" % n), "w", encoding="ascii") as f:
            json.dump(dict(p=n, ops=ops), f, ensure_ascii=True, separators=(",", ":"))

    grava(1, arte_final(x_pagina(1), "Contracapa"))
    grava(total - 1, arte_final(x_pagina(total - 1), "Fundo"))

    # Índice em duas colunas
    itens = [("h", "PARTE 1 · MONTADORAS", None)]
    for i, pl in enumerate(planos):
        if pl["cap"]["parte"] == 2 and planos[i - 1]["cap"]["parte"] == 1:
            itens.append(("h", "PARTE 2 · CATEGORIAS", None))
        itens.append(("i", "%d. %s" % (pl["cap"]["num"], pl["cap"]["nome"]), pl["inicio"] + 1))
    for np in range(pags_indice):
        x0 = x_pagina(2 + np)
        ops = [titulo_pagina("Índice", x0)]
        for j, (k, nome, pag) in enumerate(itens[np * 128:(np + 1) * 128]):
            col, lin = j // 64, j % 64
            X, Y = x0 + 142 + col * 1096, 343 + lin * 46
            if k == "h":
                ops.append(r(X, Y, 1030, 40, PT, "Índice parte"))
                ops.append(t(X + 12, Y + 6, 1000, 32, [[[nome, "b", 7, AM]]], "Índice parte texto"))
            else:
                pt_i = 8 if larg(nome, "r", 8) <= 890 else pt_ajustado(nome, "r", 890) * 0.8
                ops.append(t(X, Y + 4, 900, 38, [[[nome, "r", pt_i, PT]]], "Índice " + nome))
                ops.append(t(X + 900, Y + 4, 130, 38, [[[str(pag), "b", 8, PT]]], "Índice página", "r"))
        grava(2 + np, ops)

    resumo = {}
    for pl in planos:
        cap = pl["cap"]
        grava(pl["inicio"], abertura(cap, x_pagina(pl["inicio"])))
        for i, linhas_pag in enumerate(pl["paginas"]):
            n = pl["inicio"] + 1 + i
            x0 = x_pagina(n)
            ops = [titulo_pagina(cap["nome"], x0)]
            for y, fila in linhas_pag:
                col = 0
                for c, l in fila:
                    ops += c["draw"](x0 + 142 + col * (CW + GX), 343 + y)
                    col += c["span"]
                    l["modelo_card"], l["pagina_catalogo"] = c["modelo"], n + 1
                    resumo[c["modelo"]] = resumo.get(c["modelo"], 0) + 1
            grava(n, ops)

    with open(os.path.join(DADOS, "catalogo_ordenado.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, COLUNAS + ["pagina_catalogo"])
        w.writeheader()
        w.writerows(arq["linhas"])
    plano = dict(total=total, indice=pags_indice,
                 capitulos=[dict(num=x["cap"]["num"], nome=x["cap"]["nome"], parte=x["cap"]["parte"],
                                 pagina=x["inicio"] + 1, paginas=len(x["paginas"]) + 1) for x in planos])
    with open(os.path.join(DADOS, "plano.json"), "w", encoding="utf-8") as f:
        json.dump(plano, f, ensure_ascii=False, indent=0)
    print(json.dumps(dict(paginas_total=total, paginas_indice=pags_indice, cards=sum(resumo.values()), modelos=resumo,
                          fotos=len(fotos), avisos=len(avisos), exemplos=avisos[:8],
                          media_cards_por_pagina=round(sum(resumo.values()) / sum(len(x["paginas"]) for x in planos), 1)),
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
