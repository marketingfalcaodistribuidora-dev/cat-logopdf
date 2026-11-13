"""Renderiza um recorte de página em alta resolução para revisão: python zoom.py <pag> <x0> <y0> <x1> <y1> <dpi> <saida>"""
import sys, os
import pymupdf as fitz
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from capitulos import PDF
p, x0, y0, x1, y1, dpi, out = sys.argv[1:8]
d = fitz.open(PDF)
d[int(p) - 1].get_pixmap(dpi=int(dpi), clip=fitz.Rect(float(x0), float(y0), float(x1), float(y1))).save(out)
