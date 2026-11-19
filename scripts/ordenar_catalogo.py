"""Gera a ordem final do catálogo a partir da planilha oficial.

Parte 1: um capítulo por montadora (A-Z), agrupado por categoria.
Parte 2: um capítulo por categoria, na ordem atual do catálogo.
Os campos dos produtos são copiados da planilha sem nenhuma alteração.
"""
import collections
import csv
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analisar_cards import BASE, carregar, classificar  # noqa: E402

SAIDA = os.path.join(BASE, "Catalogo_Atualizado_dados")
NUM = r"(\d+(?:[.,]\d+)?)"
DENOMINADORES = {2, 4, 8, 16, 32, 64}
# Montadoras pequenas: o produto também conta quando a marca é citada na aplicação, referências ou similares
MENCOES = {
    "Agco": r"\bAGCO\b", "Audi": r"\bAUDI\b", "Chrysler-Dodge": r"\bCHRYSL?ER[- ]DODGE\b", "Citroën": r"\bCITRO[EË]N\b",
    "Dodge": r"\bDODGE\b", "Fiat Allis": r"\bFIAT[- ]?ALLIS\b", "FNM": r"\bFNM\b", "John Deere": r"\bJOHN\s*DEERE\b",
    "Marcopolo": r"\bMARCOPOLO\b", "Nissan": r"\bNISSAN\b", "Peugeot": r"\bPEUGEOT\b", "Puma": r"\bPUMA\b",
    "Schiffer": r"\bSCHIFFER\b", "Seat": r"\bSEAT\b", "Usicamp": r"\bUSICAMP\b",
}
# Categorias sem capítulo próprio: todos os produtos já estão no capítulo da montadora
CAPITULOS_REMOVIDOS = {"Peças Volvo": ["Volvo"], "Peças Mercedes-Benz": ["Mercedes-Benz"],
                       "Peças Volkswagen e Ford": ["Volkswagen", "Ford"], "Peças Scania": ["Scania"]}


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn").casefold()


def n(v):
    return float(v.replace(",", "."))


def polegadas(t):
    """Frações como 3/4 e 1.1/2; ignora modelos como 112/113."""
    achados = []
    for m in re.finditer(r"(?<![\d/.,])(?:(\d+)[.\- ])?(\d{1,2})/(\d{1,2})(?![\d/])", t):
        inteiro, a, b = int(m.group(1) or 0), int(m.group(2)), int(m.group(3))
        if b in DENOMINADORES and a < b:
            achados.append(inteiro + a / b)
    for m in re.finditer(r"(?<![\d/.,])(\d{1,2})\s*(?:\"|''|POL\b)", t):
        achados.append(float(m.group(1)))
    return achados


def medidas(texto):
    """Devolve {unidade: valor} com a primeira ocorrência de cada unidade."""
    t = texto.upper()
    r = {}
    regras = [
        ("dentes", NUM + r"\s*(?:D|DENTES)\b", 1),
        ("estrias", NUM + r"\s*(?:E|ESTRIAS)\b", 1),
        ("mm", NUM + r"\s*MM\b", 1),
        ("ml", NUM + r"\s*ML\b", 1),
        ("ml", NUM + r"\s*(?:L|LT|LTS|LITROS?)\b", 1000),
        ("g", NUM + r"\s*(?:G|GR)\b", 1),
        ("g", NUM + r"\s*KG\b", 1000),
        ("t", NUM + r"\s*(?:T|TON|TONELADAS?)\b", 1),
    ]
    for un, rx, fator in regras:
        m = re.search(rx, t)
        if m and un not in r:
            r[un] = n(m.group(1)) * fator
    pol = polegadas(t)
    if pol:
        r["pol"] = pol[0]
    m = re.search(NUM + r"\s*X\s*" + NUM, t)
    if m:
        r["dim"] = n(m.group(1))
    return r


def familia(p):
    """Descrição sem os números: itens iguais diferem apenas na medida."""
    t = sem_acento(p["descricao"]).upper()
    t = re.sub(r"\d+(?:[.,/\-]\d+)*\s*(?:MM|ML|LTS?|LITROS?|KG|GR?|TON|T|D|E|\"|'')?\b", " ", t)
    t = re.sub(r"\bX\b|[\"'()]", " ", t)
    return p["tipo"] + " | " + re.sub(r"\s+", " ", t).strip()


def codigo_chave(c):
    return (0, int(c), "") if c.isdigit() else (1, 0, c)


PRIORIDADE = ["dentes", "estrias", "mm", "pol", "ml", "g", "t", "dim"]


def ordenar_familia(itens):
    """Define medida_valor, medida_unidade e medida_status de cada item."""
    if len(itens) == 1:
        itens[0].update(medida_valor="", medida_unidade="", medida_status="item_unico")
        return itens
    achados = []
    for p in itens:
        primeira = p["variacoes"].split("\n")[0] if p["variacoes"] else ""
        achados.append(medidas(p["descricao"] + " " + primeira))
    comuns = [u for u in PRIORIDADE if all(u in a for a in achados)]
    escolhida = next((u for u in comuns if len({a[u] for a in achados}) == len(itens)), None)
    if escolhida is None:
        escolhida = next((u for u in comuns if len({a[u] for a in achados}) > 1), None)
    if escolhida is None:
        for p in itens:
            p.update(medida_valor="", medida_unidade="", medida_status="nao_identificada")
        return sorted(itens, key=lambda p: codigo_chave(p["cod_primeiro"]))
    for p, a in zip(itens, achados):
        p.update(medida_valor=a[escolhida], medida_unidade=escolhida, medida_status="ok")
    return sorted(itens, key=lambda p: (p["medida_valor"], codigo_chave(p["cod_primeiro"])))


def ordenar_grupo(produtos):
    fam = collections.defaultdict(list)
    for p in produtos:
        fam[familia(p)].append(dict(p, familia=familia(p)))
    saida = []
    for chave in sorted(fam, key=sem_acento):
        saida += ordenar_familia(fam[chave])
    return saida


def norm(t):
    return re.sub(r"\s+", " ", sem_acento(t)).strip()


def pontos(d):
    """Quanto mais letras e números, mais completa é a descrição."""
    return len(re.findall(r"[0-9A-Za-zÀ-ÿ]", d))


def unificar_descricoes(P):
    """Código repetido com descrições diferentes passa a usar a mais completa."""
    cand = collections.defaultdict(list)
    for p in P:
        cods = [c.strip() for c in p["codigo"].split(" / ")]
        if len(cods) == 1 and not p["variacoes"]:
            cand[cods[0]].append(p["descricao"])
        for l in p["variacoes"].split("\n"):
            c, sep, d = l.partition(" – ")
            if sep and d.strip():
                cand[c.strip()].append(d.strip())
    melhor = {c: max(ds, key=pontos) for c, ds in cand.items() if len({norm(d) for d in ds}) > 1}
    trocas = []
    for p in P:
        cods = [c.strip() for c in p["codigo"].split(" / ")]
        if len(cods) == 1 and not p["variacoes"] and cods[0] in melhor and p["descricao"] != melhor[cods[0]]:
            trocas.append((cods[0], p["categoria"], p["descricao"], melhor[cods[0]]))
            p["descricao_planilha"] = p["descricao"]
            p["descricao"] = melhor[cods[0]]
        if p["variacoes"]:
            novas = []
            for l in p["variacoes"].split("\n"):
                c, sep, d = l.partition(" – ")
                if sep and d.strip() and c.strip() in melhor and d.strip() != melhor[c.strip()]:
                    trocas.append((c.strip(), p["categoria"], d.strip(), melhor[c.strip()]))
                    l = c + sep + melhor[c.strip()]
                novas.append(l)
            p["variacoes"] = "\n".join(novas)
    return melhor, trocas


COLUNAS = [
    "parte", "capitulo_num", "capitulo", "ordem", "categoria", "montadora", "marca", "tipo", "familia",
    "medida_valor", "medida_unidade", "medida_status", "modelo_card", "cod_original", "descricao", "ref",
    "variacoes", "similares", "aplicacao", "info", "imagem", "imagem_nome", "paginas_origem",
    "descricao_planilha", "montadora_exibida",
]


def linha(p, parte, num, cap, ordem):
    foto = os.path.join(BASE, p["foto"]).replace("/", "\\") if p["foto"] else ""
    return dict(
        parte=parte, capitulo_num=num, capitulo=cap, ordem=ordem, categoria=p["categoria"],
        montadora=p["montadora"], marca=p["marca"], tipo=p["tipo"], familia=p["familia"],
        medida_valor=p["medida_valor"], medida_unidade=p["medida_unidade"], medida_status=p["medida_status"],
        modelo_card=p["modelo"], cod_original=p["codigo"], descricao=p["descricao"], ref=p["ref"],
        variacoes=p["variacoes"], similares=p["similares"], aplicacao=p["aplicacao"], info=p["info"],
        imagem=foto, imagem_nome=os.path.basename(foto), paginas_origem=p["paginas"],
        descricao_planilha=p.get("descricao_planilha", ""), montadora_exibida="",
    )


def main():
    os.makedirs(SAIDA, exist_ok=True)
    P = carregar()
    melhor, trocas = unificar_descricoes(P)
    with open(os.path.join(SAIDA, "descricoes_unificadas.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["codigo", "categoria", "descricao_na_planilha", "descricao_adotada"])
        w.writerows(sorted(trocas))
    categorias = []
    for p in P:
        p["modelo"] = classificar(p)
        p["cod_primeiro"] = p["codigo"].split(" / ")[0].strip()
        if p["categoria"] not in categorias:
            categorias.append(p["categoria"])

    linhas, capitulos = [], []
    por_montadora = collections.defaultdict(list)
    for p in P:
        for m in re.split(r"\s*,\s*", p["montadora"]):
            if m:
                por_montadora[m].append(p)

    num = 0
    # Produto sem montadora de um capítulo removido entra no capítulo da montadora correspondente
    for p in P:
        if p["categoria"] in CAPITULOS_REMOVIDOS and not p["montadora"].strip():
            for m in CAPITULOS_REMOVIDOS[p["categoria"]]:
                por_montadora[m].append(p)

    for m, rx in MENCOES.items():
        padrao = re.compile(rx, re.I)
        ja = {id(p) for p in por_montadora[m]}
        for p in P:
            if id(p) not in ja and any(padrao.search(p[c]) for c in ("descricao", "aplicacao", "ref", "similares", "variacoes", "info")):
                por_montadora[m].append(p)

    # Montadora com um único produto vai para o capítulo "Outras Montadoras"
    unicas = {m: ps[0] for m, ps in por_montadora.items() if len(ps) == 1}
    for mont in sorted((m for m in por_montadora if m not in unicas), key=sem_acento):
        num += 1
        ordem = 0
        for cat in categorias:
            grupo = [p for p in por_montadora[mont] if p["categoria"] == cat]
            for p in ordenar_grupo(grupo):
                ordem += 1
                linhas.append(linha(p, "1-Montadoras", num, mont, ordem))
        capitulos.append(dict(parte=1, num=num, nome=mont, produtos=ordem))
    if unicas:
        num += 1
        juntos = {}
        for m in sorted(unicas, key=sem_acento):
            juntos.setdefault(id(unicas[m]), (unicas[m], []))[1].append(m)
        ordem = 0
        for p, nomes in juntos.values():
            ordem += 1
            item = dict(p, familia=familia(p), medida_valor="", medida_unidade="", medida_status="item_unico")
            l = linha(item, "1-Montadoras", num, "Outras Montadoras", ordem)
            l["montadora_exibida"] = ", ".join(nomes)
            linhas.append(l)
        capitulos.append(dict(parte=1, num=num, nome="Outras Montadoras", produtos=ordem))
        print("Outras Montadoras:", ", ".join(sorted(unicas, key=sem_acento)))
    for cat in [c for c in categorias if c not in CAPITULOS_REMOVIDOS]:
        num += 1
        ordem = 0
        for p in ordenar_grupo([p for p in P if p["categoria"] == cat]):
            ordem += 1
            linhas.append(linha(p, "2-Categorias", num, cat, ordem))
        capitulos.append(dict(parte=2, num=num, nome=cat, produtos=ordem))

    with open(os.path.join(SAIDA, "catalogo_ordenado.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, COLUNAS)
        w.writeheader()
        w.writerows(linhas)
    with open(os.path.join(SAIDA, "catalogo_ordenado.json"), "w", encoding="utf-8") as f:
        json.dump(dict(capitulos=capitulos, linhas=linhas), f, ensure_ascii=False)

    # Inconsistências: apenas listadas, nunca corrigidas
    duplicados = collections.defaultdict(set)
    for c, _, antes, depois in trocas:
        duplicados[c].update([antes, depois])
    parte2 = [l for l in linhas if l["parte"].startswith("2")]
    sem_medida = [l for l in parte2 if l["medida_status"] == "nao_identificada"]
    with open(os.path.join(SAIDA, "inconsistencias.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tipo", "codigo", "categoria", "descricao"])
        for p in P:
            if not p["montadora"]:
                w.writerow(["sem montadora", p["codigo"], p["categoria"], p["descricao"]])
            if not p["foto"]:
                w.writerow(["imagem ausente", p["codigo"], p["categoria"], p["descricao"]])
        for c, d in sorted(duplicados.items()):
            w.writerow(["codigo duplicado (descricao unificada)", c, "", "adotada: " + melhor[c] + " || na planilha: " + " || ".join(sorted(d - {melhor[c]}))])
        for l in sem_medida:
            w.writerow(["medida nao identificada", l["cod_original"], l["categoria"], l["descricao"]])

    status = collections.Counter(l["medida_status"] for l in parte2)
    print(json.dumps(dict(
        capitulos_montadora=sum(c["parte"] == 1 for c in capitulos),
        capitulos_categoria=sum(c["parte"] == 2 for c in capitulos),
        cards_parte1=len(linhas) - len(parte2), cards_parte2=len(parte2),
        medida_parte2=status, codigos_duplicados=len(duplicados), descricoes_trocadas=len(trocas),
        sem_montadora=sum(not p["montadora"] for p in P), sem_foto=sum(not p["foto"] for p in P),
        menores_capitulos=sorted(((c["produtos"], c["nome"]) for c in capitulos if c["parte"] == 2))[:6],
    ), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
