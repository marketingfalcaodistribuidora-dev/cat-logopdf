"""Capítulos do catálogo (páginas do PDF, conferidas visualmente — o sumário impresso está desatualizado)."""
import os

# Cópia da versão de 641 páginas (o arquivo original em LANÇAMENTOS/2026 foi sobrescrito em 13/11/2026 16:40 por um PDF de 1 página)
_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.environ.get("CATALOGO_PDF", os.path.join(_BASE, "_fonte", "CATALOGO 2026 13-11-2026 - 641 paginas.pdf"))
WORK = os.environ.get("CATALOGO_WORK", r"C:\Users\compr\AppData\Local\Temp\claude\a46a2b403393fd63\0aab3699-aca8-47b5-9877-4abc5c7d3b0f\scratchpad\work")

CAPITULOS = {
    1: {"nome": "Importados", "ini": 4, "fim": 11},
    2: {"nome": "Cuícas, Catracas e Acessórios", "ini": 12, "fim": 19},
    3: {"nome": "Reparo Freio", "ini": 20, "fim": 32},
    4: {"nome": "Sapata e Lona Freio", "ini": 33, "fim": 39},
    5: {"nome": "Mola Freio e Rebite Lona", "ini": 40, "fim": 42},
    6: {"nome": "Anel Elástico, Rolete e Trava", "ini": 43, "fim": 47},
    7: {"nome": "Anel Pista, Buchas e Eixos", "ini": 48, "fim": 56},
}
