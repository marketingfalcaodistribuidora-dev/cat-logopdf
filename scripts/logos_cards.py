"""Folha com os logos pequenos de cada card (1 linha por card) de um intervalo de páginas: python logos_cards.py p0 p1 saida"""
import json, os, sys
import pymupdf as fitz
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from capitulos import PDF, WORK
p0, p1, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
d = fitz.open(PDF)
rows = []
for p in range(p0, p1 + 1):
    raw = json.load(open(os.path.join(WORK, "raw", f"p{p:03d}.json"), encoding="utf-8"))
    for c in raw["cards"]:
        if c["id"] == 0:
            continue
        tiles = []
        for i in c["images"]:
            r = fitz.Rect(i["bbox"])
            if r.width * r.height < 4000 and r.width > 8 and r.height > 6:
                pix = d[p - 1].get_pixmap(dpi=110, clip=r)
                im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                im = im.resize((max(1, int(im.width * 34 / im.height)), 34))
                tiles.append(im)
        cod = c["codes"][0] if c["codes"] else "-"
        w = 140 + sum(t.width + 6 for t in tiles)
        row = Image.new("RGB", (max(w, 200), 38), "white")
        ImageDraw.Draw(row).text((2, 12), f"{p}.{c['id']} {cod}", fill="red")
        x = 140
        for t in tiles:
            row.paste(t, (x, 2)); x += t.width + 6
        rows.append(row)
W = max(r.width for r in rows)
cols = 2
h = (len(rows) + cols - 1) // cols
sh = Image.new("RGB", (W * cols, 38 * h), "white")
for k, r in enumerate(rows):
    sh.paste(r, ((k // h) * W, (k % h) * 38))
sh.save(out)
