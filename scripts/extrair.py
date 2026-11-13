"""Extrai cards de produtos de um intervalo de páginas do catálogo.

Uso: python extrair.py <pdf> <pag_ini> <pag_fim> <saida_dir>

Para cada página gera:
  - raw/pNNN.json   : cards com linhas de texto (cor, tamanho, posição), códigos vermelhos e imagens
  - dump/pNNN.txt   : versão legível para revisão
  - review/pNNN.png : página renderizada com o número de cada card desenhado
"""
import json
import os
import re
import sys

import pymupdf as fitz

CODE_RE = re.compile(r"^\d{5,12}$")


def is_red(color):
    r, g, b = (color >> 16) & 255, (color >> 8) & 255, color & 255
    return r > 170 and g < 100 and b < 110


def card_rects(page):
    rects = []
    for dr in page.get_drawings():
        r = dr["rect"]
        if "s" not in (dr.get("type") or ""):
            continue
        if r.width < 60 or r.height < 30:
            continue
        if r.y1 < 90:  # cabeçalho
            continue
        if r.width > page.rect.width * 0.98 and r.height > page.rect.height * 0.9:
            continue
        rects.append(fitz.Rect(r))
    # remove duplicados próximos
    out = []
    for r in sorted(rects, key=lambda r: (round(r.y0), round(r.x0))):
        if any(abs(r.x0 - o.x0) < 3 and abs(r.y0 - o.y0) < 3 and abs(r.x1 - o.x1) < 3 and abs(r.y1 - o.y1) < 3 for o in out):
            continue
        out.append(r)
    return out


def smallest_container(rects, pt):
    best, besta = None, None
    for i, r in enumerate(rects):
        if r.contains(pt):
            a = r.width * r.height
            if besta is None or a < besta:
                best, besta = i, a
    return best


def group_lines(spans):
    """Agrupa spans em linhas pela sobreposição vertical."""
    spans = sorted(spans, key=lambda s: ((s["bbox"][1] + s["bbox"][3]) / 2, s["bbox"][0]))
    lines = []
    for s in spans:
        cy = (s["bbox"][1] + s["bbox"][3]) / 2
        h = s["bbox"][3] - s["bbox"][1]
        placed = False
        for ln in lines:
            if abs(ln["cy"] - cy) < max(2.5, min(h, ln["h"]) * 0.45):
                ln["spans"].append(s)
                placed = True
                break
        if not placed:
            lines.append({"cy": cy, "h": h, "spans": [s]})
    for ln in lines:
        ln["spans"].sort(key=lambda s: s["bbox"][0])
    lines.sort(key=lambda ln: ln["cy"])
    return lines


def main():
    pdf, a, b, outdir = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    for sub in ("raw", "dump", "review"):
        os.makedirs(os.path.join(outdir, sub), exist_ok=True)
    doc = fitz.open(pdf)
    for pno in range(a, b + 1):
        page = doc[pno - 1]
        rects = card_rects(page)
        cards = [{"id": i + 1, "rect": [round(v, 1) for v in r], "spans": [], "images": []} for i, r in enumerate(rects)]
        loose = {"id": 0, "rect": [0, 0, page.rect.width, page.rect.height], "spans": [], "images": []}

        for blk in page.get_text("dict")["blocks"]:
            for ln in blk.get("lines", []):
                for s in ln["spans"]:
                    t = s["text"].strip()
                    if not t:
                        continue
                    bb = fitz.Rect(s["bbox"])
                    if bb.y1 < 85 and bb.x0 > 150:
                        continue  # título do cabeçalho
                    item = {
                        "t": t,
                        "bbox": [round(v, 1) for v in bb],
                        "size": round(s["size"], 1),
                        "color": "%06x" % s["color"],
                        "red": is_red(s["color"]),
                        "font": s["font"],
                    }
                    k = smallest_container(rects, (bb.tl + bb.br) / 2)
                    (cards[k] if k is not None else loose)["spans"].append(item)

        for im in page.get_image_info(xrefs=True):
            bb = fitz.Rect(im["bbox"]) & page.rect
            if bb.is_empty or bb.width < 4 or bb.height < 4:
                continue
            k = smallest_container(rects, (bb.tl + bb.br) / 2)
            item = {"bbox": [round(v, 1) for v in bb], "xref": im["xref"], "px": [im["width"], im["height"]],
                    "tf": [round(v, 3) for v in im["transform"]]}
            (cards[k] if k is not None else loose)["images"].append(item)

        allcards = ([loose] if (loose["spans"] or loose["images"]) else []) + cards
        dump = [f"===== PÁGINA {pno}  ({len(cards)} cards)"]
        for c in allcards:
            lines = group_lines(c["spans"])
            c["lines"] = [
                [{"t": s["t"], "red": s["red"], "size": s["size"], "x": s["bbox"][0], "x1": s["bbox"][2], "y": s["bbox"][1]} for s in ln["spans"]]
                for ln in lines
            ]
            c["codes"] = [s["t"] for s in c["spans"] if s["red"] and CODE_RE.match(s["t"].replace(" ", ""))]
            dump.append(f"--- card {c['id']} rect={c['rect']} codes={len(c['codes'])} imgs={[ (round(i['bbox'][2]-i['bbox'][0]), round(i['bbox'][3]-i['bbox'][1])) for i in c['images']]}")
            for ln in c["lines"]:
                dump.append("   " + " | ".join(("*" if s["red"] else "") + s["t"] + f"<{s['size']:.0f}>" for s in ln))
            del c["spans"]
        with open(os.path.join(outdir, "raw", f"p{pno:03d}.json"), "w", encoding="utf-8") as f:
            json.dump({"page": pno, "cards": allcards}, f, ensure_ascii=False)
        with open(os.path.join(outdir, "dump", f"p{pno:03d}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(dump) + "\n")

        # página de revisão com números dos cards
        shape = page.new_shape()
        for c in cards:
            r = fitz.Rect(c["rect"])
            shape.draw_rect(fitz.Rect(r.x0, r.y0, r.x0 + 16, r.y0 + 12))
            shape.finish(color=(0, 0, 1), fill=(0, 0, 1))
        shape.commit()
        for c in cards:
            r = fitz.Rect(c["rect"])
            page.insert_text((r.x0 + 2, r.y0 + 10), str(c["id"]), fontsize=9, color=(1, 1, 1))
        page.get_pixmap(dpi=int(os.environ.get("REVIEW_DPI", "80"))).save(os.path.join(outdir, "review", f"p{pno:03d}.png"))
    print("ok", a, b)


if __name__ == "__main__":
    main()
