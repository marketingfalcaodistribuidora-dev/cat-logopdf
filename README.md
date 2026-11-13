# Catálogo Falcão 2026 — planilha de produtos

Leitura do PDF **CATÁLOGO 2026 13-11-2026.pdf** (641 páginas), capítulo por capítulo, card por card.

- `Catalogo_Falcao_2026.xlsx` — planilha final: aba *Resumo*, aba *Todos os produtos* e uma aba por categoria.
  Ordenação dentro de cada categoria: marca (montadora/aplicação) → marca do produto → tipo → tamanho crescente.
- `Fotos Catálogo 2026/` — fotos dos produtos, uma pasta por categoria, cada arquivo nomeado com a descrição e o código interno.
- `dados/capNN.json` — registros de cada capítulo.
- `ajustes/capNN.py` — correções feitas na revisão visual de cada página (marcas por logo, tipos, referências).
- `scripts/` — extração (`extrair.py`), montagem (`montar.py`) e geração da planilha (`gerar_planilha.py`).
