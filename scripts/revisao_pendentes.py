"""Decisões da revisão manual dos 174 produtos com texto do PDF sem dono confirmado.

Cada trecho aceito é copiado do PDF; as únicas mudanças são cortes do texto de cards vizinhos
e a troca de rótulos colados (ex.: "Ref. OriginalOEM PN" -> "Ref. Original:").
Uso: python scripts/revisao_pendentes.py [--aplicar]
"""
import collections
import json
import os
import re
import sys
import unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PEND = json.load(open(os.path.join(BASE, "Catalogo_Atualizado_dados", "pendentes_texto.json"), encoding="utf-8"))


def seg(k, j=0):
    return PEND[k]["novas"][j]


def corta(k, j, fim):
    s = seg(k, j)
    return s[:s.index(fim)].strip() if fim in s else s


def diafragma(k, j):
    s = seg(k, j)
    return s.replace("Ref. OriginalOEM PN ", "Ref. Original: ").replace(" Ref. AplicaçãoApplication ", " | Aplicação: ")


def equivalentes(k):
    return seg(k).replace("Códigos de Marcas Equivalentes ", "Códigos equivalentes: ")


ACEITOS = {
    0: [corta(0, 0, " REPARO CATRACA")], 1: [corta(1, 0, " REPARO CATRACA")],
    2: [seg(2)], 4: [corta(4, 0, " JOGO DE GUIA")],
    5: ["MERITOR ELSA195/ELSA225 | Aplicação: B10B / B12 / FH12 / FH16 / FM10 / Fm12 / Fm7 / FM9 / NH12 / Nl10 / Nl12 | Referência: 1696446, 64225252"],
    6: [seg(6)], 8: [seg(8)], 9: [seg(9)], 17: [seg(17)], 19: [seg(19)],
    20: [diafragma(20, 0)], 21: [diafragma(21, 0)], 22: [diafragma(22, 0)], 23: [diafragma(23, 1)], 24: [diafragma(24, 0)],
    25: [diafragma(25, 0)], 26: [diafragma(26, 0)], 27: [diafragma(27, 0)], 28: [diafragma(28, 0)], 29: [diafragma(29, 1)],
    30: [diafragma(30, 0)], 31: [diafragma(31, 1)], 32: [diafragma(32, 1)],
    34: [seg(34)], 35: [seg(35)],
    47: [equivalentes(47)], 48: [equivalentes(48)], 49: [equivalentes(49)], 50: [equivalentes(50)], 51: [equivalentes(51)],
    55: [seg(55)], 56: [seg(56)], 57: [seg(57)], 58: [seg(58)], 59: [seg(59)], 60: [seg(60)], 61: [seg(61)], 62: [seg(62)],
    65: [seg(65)], 66: [seg(66)], 67: [seg(67)], 68: [seg(68)], 69: [seg(69)], 70: [seg(70)],
    81: [corta(81, 0, " FOTO ILUSTRATIVA")], 84: [seg(84)], 86: [seg(86)], 88: [seg(88)], 89: [seg(89)],
    100: [seg(100)], 101: [seg(101, 0), seg(101, 1)], 102: [seg(102)], 103: [seg(103)], 104: [seg(104)], 105: [seg(105)],
    107: [re.sub(r"\s*Ÿ\s*", " | ", seg(107, j)).strip(" |") for j in range(3)],
    111: [seg(111)], 114: [seg(114)], 115: [seg(115)], 116: [seg(116, 1)], 117: [seg(117)], 118: [seg(118)],
    131: [equivalentes(131)], 137: [seg(137)], 152: [seg(152)],
    153: [seg(153, j) for j in range(len(PEND[153]["novas"]))],
    154: [seg(154, j) for j in range(len(PEND[154]["novas"]))],
    166: [" ".join(PEND[166]["novas"])], 167: [seg(167)], 168: [seg(168)],
}


def tokens(t):
    t = "".join(c for c in unicodedata.normalize("NFD", str(t or "")) if unicodedata.category(c) != "Mn").upper()
    return re.findall(r"[A-Z0-9]+", t)


def main():
    aplicar = "--aplicar" in sys.argv
    por_arq = collections.defaultdict(list)
    for k, textos in ACEITOS.items():
        p = PEND[k]
        por_arq[p["cap"]].append((p["i"], p["codigo"], [t for t in textos if t]))
    mudados = 0
    for cap, grupo in por_arq.items():
        f = os.path.join(BASE, "dados", cap)
        dados = json.load(open(f, encoding="utf-8"))
        for i, cod, textos in grupo:
            assert dados[i]["codigo"] == cod, (cap, i, cod)
            novos = set()
            for t in textos:
                novos.update(tokens(t))
            velhos = [s.strip() for s in str(dados[i].get("info") or "").split(" | ")
                      if s.strip() and sum(x not in novos for x in tokens(s)) / max(1, len(tokens(s))) > 0.15]
            dados[i]["info"] = " | ".join(velhos + textos)
            mudados += 1
        if aplicar:
            with open(f, "w", encoding="utf-8", newline="") as fh:
                json.dump(dados, fh, ensure_ascii=False, indent=1)
    rejeitados = [k for k in range(len(PEND)) if k not in ACEITOS]
    with open(os.path.join(BASE, "Catalogo_Atualizado_dados", "texto_nao_incorporado.csv"), "w", encoding="utf-8-sig") as f:
        f.write("pagina_pdf;codigo;descricao;trecho_do_pdf\n")
        for k in rejeitados:
            p = PEND[k]
            f.write("%s;%s;%s;%s\n" % (",".join(map(str, p["paginas"])), p["codigo"], p["descricao"], " || ".join(p["novas"]).replace(";", ",")))
    print(json.dumps(dict(aceitos=len(ACEITOS), produtos_atualizados=mudados, nao_incorporados=len(rejeitados), aplicado=aplicar)))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
