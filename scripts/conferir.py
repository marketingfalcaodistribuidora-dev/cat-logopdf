"""Conferência de completude: todo código vermelho (5+ dígitos) do texto das páginas do capítulo
deve estar nos registros. Uso: python conferir.py <cap>"""
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from capitulos import CAPITULOS, WORK  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n = int(sys.argv[1])
cap = CAPITULOS[n]
regs = json.load(open(os.path.join(BASE, "dados", f"cap{n:02d}.json"), encoding="utf-8"))
tem = Counter(r["codigo"] for r in regs)
pdf = Counter()
onde = {}
for p in range(cap["ini"], cap["fim"] + 1):
    raw = json.load(open(os.path.join(WORK, "raw", f"p{p:03d}.json"), encoding="utf-8"))
    for c in raw["cards"]:
        for ln in c["lines"]:
            # junta trechos vermelhos numéricos adjacentes
            buf = ""
            for s in ln + [{"t": "", "red": False}]:
                if s["red"] and re.fullmatch(r"[\d ]+", s["t"]):
                    buf += s["t"].replace(" ", "")
                    continue
                if len(buf) >= 5:
                    pdf[buf] += 1
                    onde.setdefault(buf, f"p{p}.{c['id']}")
                buf = ""
                if s["red"]:
                    for m in re.findall(r"\b\d{6,12}\b", s["t"]):
                        pdf[m] += 1
                        onde.setdefault(m, f"p{p}.{c['id']}")
texto = " ".join(" ".join(str(r.get(f, "")) for f in ("descricao", "cod_ref", "variacoes", "aplicacao", "info")) for r in regs)
texto_dig = re.sub(r"[^0-9 ]", "", texto.replace(".", "").replace("-", ""))
como_ref = sorted(k for k in pdf if k not in tem and (k in texto or k in texto_dig.replace(" ", "")))
faltam = sorted(k for k in pdf if k not in tem and k not in como_ref)
extras = sorted(k for k in tem if k not in pdf)
print(f"Capítulo {n}: {len(regs)} registros | códigos vermelhos no PDF: {len(pdf)} distintos | na planilha: {len(tem)} distintos")
print("Vermelhos que são referências (estão nas colunas de referência/aplicação):", len(como_ref))
print("Vermelhos do PDF que NÃO estão na planilha:", [(k, onde[k]) for k in faltam] or "nenhum")
print("Códigos da planilha sem texto vermelho correspondente (lidos de imagem/manual):", extras or "nenhum")
