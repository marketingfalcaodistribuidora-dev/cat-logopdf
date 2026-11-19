"""Completa os produtos com as frases do PDF original que ficaram de fora da planilha.

Cada frase é copiada do PDF sem alteração e só entra no produto quando as molduras e linhas
divisórias do card confirmam o dono. Casos duvidosos vão para a lista de revisão.
Sem --aplicar, apenas gera os relatórios.
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
SAIDA = os.path.join(BASE, "Catalogo_Atualizado_dados")
CAMPOS = ("codigo", "descricao", "cod_ref", "variacoes", "aplicacao", "info", "marca", "montadora", "itens", "tipo")
ROTULOS = set("COD CODIGO ORIGINAL ORIG REF REFERENCIA APLICACAO APLICACOES AP CONVERSAO OBS NO NR DE DA DO DAS DOS E A O "
              "PARA COM EM C S SIMILAR SIMILARES DIMENSOES MEDIDA MEDIDAS MARCA MODELO INT EXT COMP VEICULO VEICULOS "
              "FABRICANTE SUBST SUBSTITUI FOTO ILUSTRATIVA LANCAMENTO LANCAMENTOS".split())
TITULOS = re.compile(r"^(descri[cç][aã]o( do produto| completa)?|detalhes adicionais|caracter[ií]sticas( adicionais)?|"
                     r"especifica[cç][oõ]es( t[eé]cnicas)?|informa[cç][oõ]es t[eé]cnicas?|fabricante( c[oó]digo)?|"
                     r"modo de usar|ve[ií]culo)\s*:?$", re.I)
LISTA_INDICE = re.compile(r"^(-\s*\d{3,5}\b|R-\d+)")
PAGINAS_INDICE = {273, 290, 348} | set(range(531, 543))  # índices e tabelas de aplicação em várias colunas


def tokens(t):
    t = "".join(c for c in unicodedata.normalize("NFD", str(t or "")) if unicodedata.category(c) != "Mn").upper()
    return re.findall(r"[A-Z0-9]+", t)


def junto(t):
    return "".join(tokens(t))


def separadores(pg):
    segs = []
    for d in pg.get_drawings():
        r = d["rect"]
        w, h = r.width, r.height
        if min(w, h) < 4 and max(w, h) >= 40:
            segs.append((r.x0, r.y0, r.x1, r.y1))
        elif w >= 150 and h >= 50:
            segs += [(r.x0, r.y0, r.x1, r.y0), (r.x0, r.y1, r.x1, r.y1), (r.x0, r.y0, r.x0, r.y1), (r.x1, r.y0, r.x1, r.y1)]
    return segs


def bloqueado(a, b, segs):
    for x0, y0, x1, y1 in segs:
        if y1 - y0 <= x1 - x0:  # horizontal
            y = (y0 + y1) / 2
            if (a[1] - y) * (b[1] - y) < 0:
                x = a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1])
                if x0 - 1 <= x <= x1 + 1:
                    return True
        else:
            x = (x0 + x1) / 2
            if (a[0] - x) * (b[0] - x) < 0:
                y = a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0])
                if y0 - 1 <= y <= y1 + 1:
                    return True
    return False


def linhas_da_pagina(pg):
    saida = []
    for bloco in pg.get_text("dict")["blocks"]:
        for lin in bloco.get("lines", []):
            texto, fim = "", None
            for s in lin["spans"]:
                if fim is not None and s["bbox"][0] - fim > 1.2 and not texto.endswith(" "):
                    texto += " "
                texto += s["text"]
                fim = s["bbox"][2]
            texto = re.sub(r"\s+", " ", texto).strip()
            x0, y0, x1, y1 = lin["bbox"]
            if texto and 85 <= y0 <= 812:
                saida.append(dict(t=texto, x0=x0, y0=y0, x1=x1, y1=y1))
    return saida


def frases(linhas):
    """Monta frases seguindo os blocos do PDF, para não misturar colunas vizinhas."""
    saida, atual, i = [], "", 0
    while i < len(linhas):
        l = linhas[i]
        t, tabela = l["t"], False
        if i + 1 < len(linhas):
            m = linhas[i + 1]
            if abs(m["y0"] - l["y0"]) < 3 and m["x0"] > l["x1"] and len(t) < 30 and len(m["t"]) < 20 \
                    and (t.endswith(":") or re.match(r"^[\d(±<>]", m["t"])):
                t, tabela = t + " " + m["t"], True
                i += 1
        i += 1
        novo = bool(re.match(r"^[•·▪\-–*]\s*", t)) or tabela
        t = re.sub(r"^[•·▪\-–*:]+\s*", "", t).strip()
        if not t or TITULOS.match(t):
            continue
        if atual.endswith("-") and t[:1].islower():
            atual = atual[:-1] + t
        elif atual and not novo and not re.search(r"[.:;!?]$", atual):
            atual += " " + t
        else:
            if atual:
                saida.append(atual)
            atual = t
    if atual:
        saida.append(atual)
    return saida


CABECALHO = set("CODIGO COR EMBALAGEM CAIXA MODELO MOTOR ANO LINHA CATEGORIA MONTADORA QTD UNIDADE TIPO POTENCIA FABRICANTE "
                "VISTA PARTE".split())


def sem_titulo(s, p):
    """Tira do trecho o código e a descrição do próprio produto, que o card já mostra."""
    for c in re.findall(r"[0-9@][0-9A-Za-z]{3,}", str(p["codigo"])):
        s = re.sub(r"(?<![0-9A-Za-z])" + re.escape(c) + r"(?![0-9A-Za-z])", " ", s)
    s = re.sub(re.escape(str(p["descricao"])), " ", s, flags=re.I)
    return re.sub(r"\s+", " ", s.replace(chr(92) + "n", " ")).strip(" -|")


def analisar():
    por_pag = collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(BASE, "dados", "cap*.json"))):
        nome = os.path.basename(f)
        if re.fullmatch(r"cap\d+\.json", nome):
            for i, p in enumerate(json.load(open(f, encoding="utf-8"))):
                for n in re.findall(r"\d+", str(p["pagina"])):
                    por_pag[int(n)].append(((nome, i), p))

    doc = fitz.open(PDF)
    itens = {}
    duvidas = collections.defaultdict(list)
    for n, prods in sorted(por_pag.items()):
        if n in PAGINAS_INDICE:
            continue
        pg = doc[n - 1]
        segs = separadores(pg)
        pontos = []
        achados = set()
        for chave, p in prods:
            for c in re.findall(r"[0-9@][0-9A-Za-z]{3,}", str(p["codigo"])):
                for r in pg.search_for(c):
                    pontos.append((((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2), chave))
                    achados.add(chave)
        if not pontos:
            continue
        ref = dict(prods)
        outras = {k: set(tokens(p["descricao"])) for k, p in prods}
        por_dono = collections.defaultdict(list)
        for l in linhas_da_pagina(pg):
            c = ((l["x0"] + l["x1"]) / 2, (l["y0"] + l["y1"]) / 2)
            melhor = {}
            for pt, chave in pontos:
                if bloqueado(c, pt, segs):
                    continue
                d = abs(c[0] - pt[0]) * 1.2 + abs(c[1] - pt[1])
                melhor[chave] = min(d, melhor.get(chave, 1e9))
            ordem = sorted(melhor.items(), key=lambda x: x[1])
            if not ordem:
                continue
            if len(ordem) > 1 and ordem[1][1] < ordem[0][1] * 1.4:
                por_dono[None].append(l)
            elif len(achados) < len(prods) and not segs:
                por_dono[None].append(l)
            else:
                por_dono[ordem[0][0]].append(l)
        for dono, linhas in por_dono.items():
            if dono is None:
                continue
            p = ref[dono]
            conhecido, colado = set(), ""
            for campo in CAMPOS:
                conhecido.update(tokens(p.get(campo)))
                colado += junto(p.get(campo))
            item = itens.setdefault(dono, dict(p=p, paginas=set(), novas=[], chaves=set()))
            codigos_vizinhos = {c for k, q in prods if k != dono for c in re.findall(r"[0-9@][0-9A-Za-z]{3,}", str(q["codigo"]))}
            for s in frases(linhas):
                s = sem_titulo(s, p)
                tk = [x for x in tokens(s) if len(x) > 1]
                letras = sum(ch.isalpha() for ch in s)
                if len(tk) < 2 or LISTA_INDICE.match(s) or (letras < 12 and not (":" in s and len(s) >= 10)):
                    continue
                if all(x in CABECALHO for x in tk) or s.endswith(":") or "___" in s or any(len(x) > 28 for x in tokens(s)):
                    continue
                if codigos_vizinhos & set(re.findall(r"[0-9@][0-9A-Za-z]{3,}", s)):
                    continue
                novos = [x for x in tk if x not in conhecido and x not in ROTULOS]
                if not novos or len(novos) / len(tk) < 0.25 or junto(s) in colado:
                    continue
                if any(k != dono and sum(x in d for x in tk) / len(tk) >= 0.8 for k, d in outras.items()):
                    continue
                chave = " ".join(tokens(s))
                if chave not in item["chaves"]:
                    item["chaves"].add(chave)
                    item["novas"].append(s)
                    item["paginas"].add(n)
        for l in por_dono.get(None, []):
            tk = [x for x in tokens(l["t"]) if len(x) > 1]
            if sum(ch.isalpha() for ch in l["t"]) >= 12 and len(tk) >= 3 and not LISTA_INDICE.match(l["t"]):
                pagina = set()
                for _, p in prods:
                    for campo in CAMPOS:
                        pagina.update(tokens(p.get(campo)))
                if sum(x not in pagina and x not in ROTULOS for x in tk) / len(tk) >= 0.4:
                    duvidas[n].append(l["t"])
    return {k: v for k, v in itens.items() if v["novas"]}, duvidas


def pagina_confiavel(n):
    """Páginas de cards com texto corrido, em que a revisão confirmou o dono de cada frase."""
    return (274 <= n <= 288 or 291 <= n <= 314 or 549 <= n <= 640) and n not in {552, 581, 585, 586, 615, 623}


def info_final(item):
    cobertos = set()
    for s in item["novas"]:
        cobertos.update(tokens(s))
    velhos = []
    for s in str(item["p"].get("info") or "").split(" | "):
        tk = tokens(s)
        if s.strip() and sum(x not in cobertos for x in tk) / max(1, len(tk)) > 0.15:
            velhos.append(s.strip())
    return " | ".join(velhos + item["novas"])


def main():
    aplicar = "--aplicar" in sys.argv
    itens, duvidas = analisar()
    linhas, pendentes = [], []
    for (cap, i), item in sorted(itens.items()):
        if not all(pagina_confiavel(n) for n in item["paginas"]):
            pendentes.append(item)
            continue
        linhas.append(dict(cap=cap, i=i, codigo=item["p"]["codigo"], descricao=item["p"]["descricao"],
                           paginas=",".join(map(str, sorted(item["paginas"]))), caracteres=sum(map(len, item["novas"])),
                           antes=item["p"].get("info") or "", acrescentado=" || ".join(item["novas"]), depois=info_final(item)))
    with open(os.path.join(SAIDA, "texto_recuperado.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, ["cap", "i", "codigo", "descricao", "paginas", "caracteres", "antes", "acrescentado", "depois"])
        w.writeheader()
        w.writerows(linhas)
    with open(os.path.join(SAIDA, "texto_para_revisar.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pagina_pdf", "texto_sem_dono_confirmado"])
        for n, ls in sorted(duvidas.items()):
            for l in ls:
                w.writerow([n, l])
        for item in pendentes:
            w.writerow([",".join(map(str, sorted(item["paginas"]))), "%s | %s | %s" % (item["p"]["codigo"], item["p"]["descricao"], " || ".join(item["novas"]))])
    if aplicar:
        por_arq = collections.defaultdict(list)
        for l in linhas:
            por_arq[l["cap"]].append(l)
        for cap, grupo in por_arq.items():
            f = os.path.join(BASE, "dados", cap)
            dados = json.load(open(f, encoding="utf-8"))
            for l in grupo:
                dados[l["i"]]["info"] = l["depois"]
            with open(f, "w", encoding="utf-8", newline="") as fh:
                json.dump(dados, fh, ensure_ascii=False, indent=1)
    print(json.dumps(dict(produtos_completados=len(linhas), caracteres=sum(l["caracteres"] for l in linhas),
                          produtos_para_revisao_manual=len(pendentes), linhas_em_duvida=sum(map(len, duvidas.values())), paginas_com_duvida=len(duvidas), aplicado=aplicar),
                     ensure_ascii=False))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
