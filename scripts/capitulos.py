"""Capítulos do catálogo (páginas do PDF, conferidas visualmente — o sumário impresso está desatualizado)."""
import os

PDF = os.environ.get("CATALOGO_PDF", r"C:\Users\compr\OneDrive\Área de Trabalho\LANÇAMENTOS\2026\CATÁLOGO 2026 13-11-2026.pdf")
WORK = os.environ.get("CATALOGO_WORK", r"C:\Users\compr\AppData\Local\Temp\claude\a46a2b403393fd63\0aab3699-aca8-47b5-9877-4abc5c7d3b0f\scratchpad\work")

CAPITULOS = {
    1: {"nome": "Importados", "ini": 4, "fim": 11},
    2: {"nome": "Cuícas, Catracas e Acessórios", "ini": 12, "fim": 19},
}
