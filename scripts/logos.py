"""Folha de contato com as imagens pequenas (logos) de cada card, para identificar marcas.

Uso: python logos.py <pag_ini> <pag_fim> <saida.png>
"""
import json
import os
import sys

import pymupdf as fitz
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from capitulos import PDF, WORK  # noqa: E402


def main():
    a, b, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    maxside = float(os.environ.get("LOGO_MAX", "70"))
    doc = fitz.open(PDF)
    rows = []
    for pno in range(a, b + 1):
        raw = json.load(open(os.path.join(WORK, "raw", f"p{pno:03d}.json"), encoding="utf-8"))
        page = doc[pno - 1]
        for c in raw["cards"]:
            crect = fitz.Rect(c["rect"])
            ims = []
            for i in c["images"]:
                r = fitz.Rect(i["bbox"]) & crect
                if r.is_empty or r.width < 6 or r.height < 6:
                    continue
                if r.width <= maxside * 1.8 and r.height <= maxside and r.width * r.height < maxside * maxside:
                    ims.append(r)
            # agrupa logos sobrepostos (máscaras duplicadas)
            merged = []
            for r in sorted(ims, key=lambda r: (r.y0, r.x0)):
                for m in merged:
                    if (m & r).get_area() > 0.5 * min(m.get_area(), r.get_area()):
                        m |= r
                        break
                else:
                    merged.append(fitz.Rect(r))
            if not merged:
                continue
            tiles = []
            for r in merged:
                pix = page.get_pixmap(dpi=150, clip=r + (-1, -1, 1, 1))
                tiles.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
            rows.append((f"p{pno}.{c['id']}", tiles))
    if not rows:
        print("sem logos")
        return
    H = 60
    lines = []
    for label, tiles in rows:
        scaled = [t.resize((max(1, int(t.width * H / t.height)), H)) if t.height != H else t for t in tiles]
        w = 70 + sum(t.width + 8 for t in scaled)
        im = Image.new("RGB", (w, H + 6), "white")
        d = ImageDraw.Draw(im)
        d.text((2, H // 2 - 5), label, fill="red")
        x = 70
        for t in scaled:
            im.paste(t, (x, 3))
            x += t.width + 8
        lines.append(im)
    W = min(1400, max(l.width for l in lines))
    sheet = Image.new("RGB", (W, sum(l.height for l in lines)), "white")
    y = 0
    for l in lines:
        sheet.paste(l, (0, y))
        y += l.height
    sheet.save(out)
    print(out, len(rows), "cards com logos")


if __name__ == "__main__":
    main()
