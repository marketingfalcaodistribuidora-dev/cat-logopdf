"""Devolve aos cards o que acompanhava a palavra "lançamento" e confere se nada se perdeu."""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_cards import DADOS, paragrafos, rotulos  # noqa: E402
from limpar_notas import sem_lancamento  # noqa: E402

arq = json.load(open(os.path.join(DADOS, "catalogo_ordenado.json"), encoding="utf-8"))
ANTES = json.load(open(os.path.join(DADOS, "patches_lancamentos.json"), encoding="ascii"))
com_data = {}
for l in arq["linhas"]:
    campos = " | ".join((l["aplicacao"], l["ref"], l["similares"], l["info"]))
    if re.search(r"lan[cç]amentos?\s+\d", campos, re.I):
        com_data[l["cod_original"]] = dict(l, montadora_exibida="")

patches = []
for o in ANTES:
    if not o["nome"].startswith("Dados "):
        continue
    linha = com_data.get(o["nome"][6:])
    if not linha:
        continue
    fixos = [p for p in o["paras"] if (len(p) == 1 and p[0][1] == "b") or "".join(r[0] for r in p).startswith("Montadora:")]
    paras = fixos + [rotulos(e, 6.5) for e in paragrafos(linha)]
    if paras != o["paras"]:
        patches.append(dict(o, paras=paras, existe=bool(o["paras"])))

for x in patches:
    caminho = os.path.join(DADOS, "paginas", "%05d.json" % x["p"])
    d = json.load(open(caminho, encoding="ascii"))
    novo = ["t", x["x"], x["y"], x["w"], x["h"], x["paras"], x["nome"], x["al"]]
    for i, o in enumerate(d["ops"]):
        if o[0] == "t" and o[6] == x["nome"] and o[1] == x["x"] and o[2] == x["y"]:
            d["ops"][i] = novo
            break
    else:
        d["ops"].append(novo)
    with open(caminho, "w", encoding="ascii") as f:
        json.dump(d, f, ensure_ascii=True, separators=(",", ":"))
with open(os.path.join(DADOS, "patches_datas.json"), "w", encoding="ascii") as f:
    json.dump(patches, f, ensure_ascii=True, separators=(",", ":"))

# Conferência: toda descrição e todo item de variação continuam nas páginas
textos, linhas_tabela = set(), set()
for f in glob.glob(os.path.join(DADOS, "paginas", "*.json")):
    for o in json.load(open(f, encoding="ascii"))["ops"]:
        if o[0] == "t":
            for p in o[5]:
                textos.add("".join(r[0] for r in p))
            if str(o[6]).startswith("Cód "):
                linhas_tabela.add(o[6][4:])
sem_desc, sem_item = [], []
for l in arq["linhas"]:
    d = sem_lancamento(l["descricao"])
    if d not in textos and (d + " (continuação)") not in textos:
        sem_desc.append(l["cod_original"])
    for v in l["variacoes"].split("\n"):
        c = v.partition(" – ")[0].strip()
        if c and c not in linhas_tabela:
            sem_item.append(c)
resto = sum(len(re.findall(r"lan[cç]amento", json.dumps(json.load(open(f, encoding="ascii"))["ops"], ensure_ascii=False), re.I))
            for f in glob.glob(os.path.join(DADOS, "paginas", "*.json")))
print(json.dumps(dict(quadros_restaurados=len(patches), recriados=sum(not x["existe"] for x in patches),
                      exemplo=["".join(r[0] for r in p)[:60] for p in (patches[0]["paras"] if patches else [])],
                      descricoes_faltando=len(set(sem_desc)), ex_desc=sorted(set(sem_desc))[:8],
                      itens_faltando=len(set(sem_item)), ex_item=sorted(set(sem_item))[:8],
                      palavra_lancamento_restante=resto), ensure_ascii=False))
