"""Gera a lista de quadros de texto a trocar, sem mudar a posição de nenhum card."""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_cards import DADOS, rotulos  # noqa: E402
from limpar_notas import limpar  # noqa: E402

ROTULO = re.compile(r"^(Aplicação|Ref\.|Similares|Montadora): ")
patches = []
for arq in sorted(glob.glob(os.path.join(DADOS, "paginas", "*.json"))):
    d = json.load(open(arq, encoding="ascii"))
    novos_ops, mudou = [], False
    for o in d["ops"]:
        if o[0] != "t" or not str(o[6]).startswith("Dados "):
            novos_ops.append(o)
            continue
        paras, alterado = [], False
        for para in o[5]:
            texto = "".join(r[0] for r in para)
            if len(para) == 1 and para[0][1] == "b":  # descrição do produto
                paras.append(para)
                continue
            m = ROTULO.match(texto)
            pre = m.group(0) if m else ""
            valor = limpar(texto[len(pre):])
            novo = pre + valor if valor else ""
            if novo == texto:
                paras.append(para)
                continue
            alterado = True
            if novo:
                paras.append(rotulos(novo, para[0][2]))
        if alterado:
            mudou = True
            patches.append(dict(p=d["p"], nome=o[6], x=o[1], y=o[2], w=o[3], h=o[4], paras=paras, al=o[7]))
            if paras:
                novos_ops.append(o[:5] + [paras] + o[6:])
        else:
            novos_ops.append(o)
    if mudou:
        d["ops"] = novos_ops
        with open(arq, "w", encoding="ascii") as f:
            json.dump(d, f, ensure_ascii=True, separators=(",", ":"))
with open(os.path.join(DADOS, "patches_notas.json"), "w", encoding="ascii") as f:
    json.dump(patches, f, ensure_ascii=True, separators=(",", ":"))
print("quadros a trocar", len(patches), "| paginas", len({x["p"] for x in patches}), "| quadros que somem", sum(1 for x in patches if not x["paras"]))
