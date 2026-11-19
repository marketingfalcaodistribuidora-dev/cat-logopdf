"""Tira "Parte X" das aberturas e os textos de lançamento, sem mover nenhum card."""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_cards import DADOS, rotulos  # noqa: E402
from limpar_notas import limpar, sem_lancamento  # noqa: E402

ROTULO = re.compile(r"^(Aplicação|Ref\.|Similares|Montadora): ")
ANTIGO, NOVO = "Lançamentos - Suportes de Mola", "Suportes de Mola"
patches = []


def registra(p, o, paras, h1=False, novo_nome=None):
    patches.append(dict(p=p, nome=o[6], x=o[1], y=o[2], w=o[3], h=o[4], paras=paras, al=o[7],
                        h1=h1, novo_nome=novo_nome or o[6]))


for arq in sorted(glob.glob(os.path.join(DADOS, "paginas", "*.json"))):
    d = json.load(open(arq, encoding="ascii"))
    ops, mudou = [], False
    for o in d["ops"]:
        if o[0] == "t" and o[6] == "Abertura parte":
            registra(d["p"], o, [])
            mudou = True
            continue
        if o[0] not in "th" or len(o) < 8:
            ops.append(o)
            continue
        nome = str(o[6])
        if ANTIGO in json.dumps(o[5], ensure_ascii=False):
            paras = [[[r[0].replace(ANTIGO, NOVO)] + r[1:] for r in p] for p in o[5]]
            novo_nome = nome.replace(ANTIGO, NOVO)
            registra(d["p"], o, paras, h1=o[0] == "h", novo_nome=novo_nome)
            ops.append(o[:5] + [paras, novo_nome] + o[7:])
            mudou = True
            continue
        if nome.startswith("Desc "):
            paras = [[[sem_lancamento(r[0])] + r[1:] for r in p] for p in o[5]]
            if paras != o[5]:
                registra(d["p"], o, paras)
                o = o[:5] + [paras] + o[6:]
                mudou = True
            ops.append(o)
            continue
        if not nome.startswith("Dados "):
            ops.append(o)
            continue
        paras, alterado = [], False
        for para in o[5]:
            texto = "".join(r[0] for r in para)
            if len(para) == 1 and para[0][1] == "b":
                limpo = sem_lancamento(texto)
                alterado = alterado or limpo != texto
                paras.append([[limpo] + para[0][1:]])
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
            registra(d["p"], o, paras)
            mudou = True
            if paras:
                ops.append(o[:5] + [paras] + o[6:])
        else:
            ops.append(o)
    if mudou:
        d["ops"] = ops
        with open(arq, "w", encoding="ascii") as f:
            json.dump(d, f, ensure_ascii=True, separators=(",", ":"))

with open(os.path.join(DADOS, "patches_lancamentos.json"), "w", encoding="ascii") as f:
    json.dump(patches, f, ensure_ascii=True, separators=(",", ":"))

caminho = os.path.join(DADOS, "plano.json")
plano = json.load(open(caminho, encoding="utf-8"))
for c in plano["capitulos"]:
    c["nome"] = c["nome"].replace(ANTIGO, NOVO)
with open(caminho, "w", encoding="utf-8") as f:
    json.dump(plano, f, ensure_ascii=False, indent=0)

resto = 0
for arq in glob.glob(os.path.join(DADOS, "paginas", "*.json")):
    t = json.dumps(json.load(open(arq, encoding="ascii"))["ops"], ensure_ascii=False)
    resto += len(re.findall(r"lan[cç]amento", t, re.I)) + t.count("Abertura parte")
print("quadros a ajustar", len(patches), "| apagados", sum(1 for x in patches if not x["paras"]), "| restantes", resto)
