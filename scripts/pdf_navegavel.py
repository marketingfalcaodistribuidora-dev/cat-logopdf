"""Deixa o PDF exportado do Affinity navegável: links no índice e marcadores por capítulo.

Funciona com o PDF exportado em páginas simples ou em páginas duplas (spreads).
Uso: python scripts/pdf_navegavel.py <pdf exportado> <pdf de saída>
"""
import json
import os
import sys

import fitz

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS = os.path.join(BASE, "Catalogo_Atualizado_dados")
PAG_L, PAG_A = 2480, 3508  # tamanho de uma página em px no documento


def main(entrada, saida):
    plano = json.load(open(os.path.join(DADOS, "plano.json"), encoding="utf-8"))
    doc = fitz.open(entrada)
    total = plano["total"]
    duplas = 1 + (total - 1 + 1) // 2
    if doc.page_count == total:
        em_duplas = False
    elif doc.page_count == duplas:
        em_duplas = True
    else:
        raise SystemExit("O PDF tem %d páginas; o esperado era %d (simples) ou %d (duplas)." % (doc.page_count, total, duplas))

    def pagina_pdf(n):
        """Converte a página do catálogo (0 = capa) na página do PDF."""
        return (n + 1) // 2 if em_duplas else n

    # o link abre a primeira página de produtos, logo depois da capa do capítulo
    destinos = {"%d. %s" % (c["num"], c["nome"]): c["pagina"] for c in plano["capitulos"]}
    links = 0
    for n in range(2, 2 + plano["indice"]):
        ops = json.load(open(os.path.join(DADOS, "paginas", "%05d.json" % n), encoding="ascii"))["ops"]
        pagina = doc[pagina_pdf(n)]
        sx = pagina.rect.width / (PAG_L * 2 if em_duplas else PAG_L)
        sy = pagina.rect.height / PAG_A
        x0 = 0 if em_duplas or n % 2 == 1 else PAG_L
        for o in ops:
            if o[0] != "t" or not str(o[6]).startswith("Índice "):
                continue
            destino = destinos.get(o[6][len("Índice "):])
            if destino is None:
                continue
            ret = fitz.Rect((o[1] - x0) * sx, o[2] * sy, (o[1] - x0 + 1030) * sx, (o[2] + o[4]) * sy)
            pagina.insert_link({"kind": fitz.LINK_GOTO, "from": ret, "page": pagina_pdf(destino), "to": fitz.Point(0, 0)})
            links += 1

    toc = [[1, "Capa", 1], [1, "Índice", pagina_pdf(2) + 1]]
    for parte, titulo in ((1, "Montadoras"), (2, "Categorias")):
        caps = [c for c in plano["capitulos"] if c["parte"] == parte]
        toc.append([1, titulo, pagina_pdf(caps[0]["pagina"] - 1) + 1])
        toc += [[2, c["nome"], pagina_pdf(c["pagina"] - 1) + 1] for c in caps]
    doc.set_toc(toc)
    doc.set_pagelayout("SinglePage")  # abre mostrando uma página por vez
    doc.set_pagemode("UseOutlines")  # abre com os marcadores visíveis
    doc.save(saida, garbage=3, deflate=True)
    print(json.dumps(dict(paginas_pdf=doc.page_count, duplas=em_duplas, links=links, marcadores=len(toc)), ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
