"""Renderiza 2 páginas lado a lado (área útil): python dupla.py <p1> <p2> <dpi> <saida>"""
import sys, os
import pymupdf as fitz
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from capitulos import PDF
p1, p2, dpi, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
d = fitz.open(PDF)
ims = []
for p in (p1, p2):
    pix = d[p - 1].get_pixmap(dpi=dpi, clip=fitz.Rect(20, 85, 575, 808))
    ims.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
W = sum(i.width for i in ims) + 10
sh = Image.new("RGB", (W, max(i.height for i in ims)), "white")
sh.paste(ims[0], (0, 0)); sh.paste(ims[1], (ims[0].width + 10, 0))
sh.save(out)
