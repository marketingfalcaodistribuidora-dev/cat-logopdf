# Capítulo 36 - Lanternas Traseiras e Acessórios (págs. 434-436)
# Cards com par LD/LE (ou um só código): código vermelho + "PDR- ..." na mesma linha; referência Pradolux (PLxxxx) em similares;
# card com vários códigos = 1 produto (itens LD / LE). Foto = retângulo do card.
import json
import os
import re

from capitulos import WORK
from tabela_livre import _spans

TIPOS = [(r"(?:^|\s)LENTE?(?:\s|$)", "LENTE"), (r"MOLD|MOLDURA|ACABAMENTO", "MOLDURA"), (r"(?:^|\s)SUP(?:\s|$)|SUPORTE", "SUPORTE"),
         (r"CHICOTE", "CHICOTE"), (r"SOQUETE", "SOQUETE"), (r"FAROL|MODULO|BLOCO", "FAROL"), (r"LANT|LANTERNA", "LANTERNA"), (r"ACABAMENTO", "ACABAMENTO"), (r"GELADEIRA", "GELADEIRA")]


def POS_PROC(r):
    for rx, t in TIPOS:
        if re.search(rx, r["descricao"]):
            r["tipo"] = t
            break
AJ = {}
ADD = []
NOTAS = ["Págs. 434-435 (Pradolux e outras): o código Pradolux (PLxxxx) de cada peça está em similares; cards com lado direito (LD) e "
         "esquerdo (LE) viram um produto com os dois códigos."]
MANUAIS = set(range(434, 437))
_PL = re.compile(r"\bP[Ll]\s?[0-9][0-9.\s]*[0-9](?:\s*-\s*L[DE])?")
_MONT = [(r"\bMBB?\b|MERCEDES|ATEGO|ACCELO|AXOR|ACTROS|ATRON|\bL ?1\d{3}", "Mercedes-Benz"), (r"\bVW\b|VOLKS|CONSTELLATION|DELIVERY",
         "Volkswagen"), (r"FORD|CARGO", "Ford"), (r"SCANIA", "Scania"), (r"VOLVO|\bVL\b|\bFH\b|\bFM\b|\bVM\b", "Volvo"),
         (r"IVECO|TECTOR|STRALIS|DAILY", "Iveco"), (r"\bDAF\b", "DAF"), (r"\bMAN\b|TGX", "MAN"), (r"FACCHINI", "Facchini"),
         (r"RANDON", "Randon"), (r"GUERRA", "Guerra"), (r"AGRALE", "Agrale")]


def _mont(t):
    return ", ".join(dict.fromkeys(m for rx, m in _MONT if re.search(rx, t, re.I)))


def _linhas(ss):
    out = []
    for s in sorted(ss, key=lambda s: (s["y"], s["x"])):
        if out and abs(out[-1]["y"] - s["y"]) < 3:
            out[-1]["ss"].append(s)
        else:
            out.append({"y": s["y"], "ss": [s]})
    for l in out:
        l["ss"].sort(key=lambda s: s["x"])
        l["t"] = re.sub(r"\s+", " ", " ".join(s["t"].strip() for s in l["ss"])).strip()
    return out


def ler(p):
    raw = json.load(open(os.path.join(WORK, "raw", f"p{p:03d}.json"), encoding="utf-8"))
    sp, _ = _spans(p)
    regs = []
    for c in raw["cards"]:
        if not c["id"]:
            continue
        x0, y0, x1, y1 = c["rect"]
        cs = [s for s in sp if x0 - 1 <= (s["x"] + s["x1"]) / 2 <= x1 + 1 and y0 - 1 <= s["y"] + 2 <= y1 + 1]
        cods = [s for s in cs if s["red"] and re.fullmatch(r"\d{7}", s["t"].strip()) and s["size"] >= 7]
        if not cods:
            continue
        lins = _linhas(cs)
        usadas = set()
        itens = []
        for s in cods:
            li = next(i for i, l in enumerate(lins) if s in l["ss"])
            d = [x["t"] for x in lins[li]["ss"] if x is not s and x["x"] > s["x"]]
            usadas.add(li)
            # continuação: linhas logo abaixo com fonte parecida e sem outro código
            j = li + 1
            while j < len(lins) and lins[j]["y"] - lins[j - 1]["y"] < 14 and not any(x in cods for x in lins[j]["ss"]) \
                    and abs(lins[j]["ss"][0]["size"] - s["size"]) < 3 and not _PL.fullmatch(lins[j]["t"]):
                d.append(lins[j]["t"])
                usadas.add(j)
                j += 1
            itens.append((s["t"].strip(), re.sub(r"\s+", " ", " ".join(d)).strip(" -")))
        resto = [l["t"] for i, l in enumerate(lins) if i not in usadas]
        pls = []
        for t in resto:
            pls += [m.group(0).strip() for m in _PL.finditer(t)]
        info = [t for t in (_PL.sub("", t).strip(" -|") for t in resto) if t and not re.fullmatch(r"\d{3}", t)]
        texto = " ".join(d for _, d in itens) + " " + " ".join(info)
        for cod, d in itens:
            regs.append(dict(pagina=p, card=c["id"], codigo=cod, descricao=d, cod_ref="", variacoes=" / ".join(dict.fromkeys(pls)),
                             aplicacao="", info=" | ".join(info), marca="Pradolux", montadora=_mont(texto),
                             foto_spec={"rect": [round(v, 1) for v in c["rect"]]}, _titulo=""))
    return regs


for _p in range(434, 436):
    ADD.extend(ler(_p))


def F(p, c, **kw):
    regs = [r for r in ADD if r["pagina"] == p and r["codigo"] == c]
    assert regs, f"{c} não está na pág. {p}"
    for r in regs:
        r.update(kw)


def T(p, c, titulo, descs, **kw):
    """Define o card: título do produto e descrição de cada código (transcritas da imagem)."""
    regs = [r for r in ADD if r["pagina"] == p and r["card"] == c]
    assert {r["codigo"] for r in regs} == set(descs), (p, c, [r["codigo"] for r in regs])
    for r in regs:
        r.update(descricao=descs[r["codigo"]], _titulo=titulo if len(descs) > 1 else "", **kw)
        if len(descs) == 1:
            r["_nao_agrupar"] = True


def LDLE(base, ld, le, sufixo=""):
    return {ld: f"{base} LD{sufixo}", le: f"{base} LE{sufixo}"}


# 434 (pág. impressa 433): lanternas traseiras
T(434, 1, "LANTERNA TRAS LED RANDON COMPLETA 2013", {"7000162": "LANTERNA TRAS LED RANDON LD COMPLETA 2013",
                                                    "7000163": "LANTERNA TRAS LED RANDON LE COMPLETA 2013"},
  variacoes="", info="Importado", marca="", montadora="Randon")
T(434, 2, "PDR- SUP UNIVE TRAS 24V C/ 42 LEDS BICOLOR", {"7043367": "PDR- SUP UNIVE TRAS 24V C/ 42 LEDS BICOLOR LD",
                                                        "7043467": "PDR- SUP UNIVE TRAS 24V C/ 42 LEDS BICOLOR LE"},
  variacoes="PL27003367 - LD / PL27003467 - LE", info="", montadora="")
T(434, 3, "PDR- LANT MB TRAS LED 24V VIG S/SIRENE", {"7042069": "PDR- LANT MB TRAS LED 24V S/ VIG S/SIRENE RE",
                                                    "7042169": "PDR- LANT MB TRAS LED 24V C/ VIG S/SIRENE"},
  variacoes="PL20703369 - LD / PL20703469 - LE", info="Suporte traseiro 10 LEDs BV c/ré - lado direito / lado esquerdo",
  montadora="Mercedes-Benz")
T(434, 4, "PDR- SUP TRAS LANT LED C/ CONECTOR", {"7047969": "PDR- SUP TRAS LANT LED LD C/ CONECTOR",
                                                "7048069": "PDR- SUP TRAS LANT LED LE C/ CONECTOR"},
  variacoes="PL2600.79.69 - LD / PL2600.80.69 - LE", info="", montadora="")
T(434, 5, "LANTERNA TRASEIRA 1500 MÓDULOS BIVOLT", {"7041501": "LANTERNA TRASEIRA 1500 MÓDULOS BIVOLT - LADO DIREITO",
                                                   "7041500": "LANTERNA TRASEIRA 1500 MÓDULOS BIVOLT - LADO ESQUERDO"},
  variacoes="PL15000167 - LD / PL15000267 - LE", info="", montadora="")
T(434, 6, "PDR- LANT TRAS TRIPLE X LIGHT 24V BIC", {"7043347": "PDR- LANT TRAS TRIPLE X LIGHT 24V LD BIC",
                                                   "7043447": "PDR- LANT TRAS TRIPLE X LIGHT 24V LE BIC"},
  variacoes="PL1452.33.47 - LD / PL1452.34.47 - LE", marca="Multilight", montadora="",
  info="Lanterna traseira Triplo X LED com 40 LEDs e triângulo retrorrefletor para implementos | LED 24V bivolt | Universal")
T(434, 7, "SUP UNIVERSAL TRAS 10 LEDS BIV VM CR", {"7062069": "SUP UNIVERSAL TRAS 10 LEDS BIV VM CR LD",
                                                  "7062169": "SUP UNIVERSAL TRAS 10 LEDS BIV VM CR LE"},
  variacoes="", info="", marca="Multilight", montadora="Randon")
T(434, 8, "LANT.LED MULTIFUNCOES C/BALIZADOR 24V", {"7060879": "LANT.LED MULTIFUNCOES C/BALIZADOR 24V LD",
                                                   "7060880": "LANT.LED MULTIFUNCOES C/BALIZADOR 24V LE"},
  variacoes="", info="", marca="", montadora="")
T(434, 9, "", {"7040786": "PDR-LANT MB TRASEIRA UNIVERSAL C/VIGIA"}, variacoes="PL07860209",
  info="Lanterna traseira tricolor c/ vigia âmbar vermelha e crist", montadora="Mercedes-Benz")
T(434, 10, "LANTERNA LIBRERATO TRAS LED 2018 HN", {"7002180": "LANTERNA LIBRERATO TRAS LED LD 2018 HN",
                                                  "7002018": "LANTERNA LIBRERATO TRAS LED LE 2018 HN"},
  variacoes="", info="", marca="", montadora="Librelato")
NOTAS.append("Pág. 434: no card 3, 7042069 está 'S/ VIG' e 7042169 'C/ VIG'; o card 10 está impresso 'LIBRERATO' (logo Librelato).")
# 435 (pág. impressa 434): molduras sobrepostas -> registros manuais
ADD[:] = [r for r in ADD if r["pagina"] != 435]
_b = dict(pagina=435, cod_ref="", variacoes="", aplicacao="", info="", marca="", montadora="")
ADD += [
    dict(_b, card=1, codigo="7061142", descricao="SUP UNIVERSAL TRAS 10 LEDS BIV VM CR LD C/REF", marca="GLR",
         _titulo="SUP UNIVERSAL TRAS 10 LEDS BIV VM CR C/REF", foto_spec={"rect": [30, 100, 290, 300]}),
    dict(_b, card=1, codigo="7061143", descricao="SUP UNIVERSAL TRAS 10 LEDS BIV VM CR LE C/REF", marca="GLR",
         _titulo="SUP UNIVERSAL TRAS 10 LEDS BIV VM CR C/REF", foto_spec={"rect": [30, 100, 290, 300]}),
    dict(_b, card=3, codigo="5100112", descricao="CHICOTE 5 VIAS LANTERNA GUERRA ETE7760", variacoes="ETE7760", montadora="Guerra",
         _nao_agrupar=True, foto_spec={"rect": [355, 130, 570, 300]}),
    dict(_b, card=4, codigo="70116912", descricao="ACABAMENTO PROT DE CICLISTA CURVADO", marca="Facchini", _nao_agrupar=True,
         info="Acessório | Material: plástico | Truck | Acabamento protetor de ciclista curvado / acabamento protetor caminhão",
         aplicacao="Carretas baú e truck modelo Facchini", montadora="Facchini", foto_spec={"rect": [40, 560, 290, 740]}),
    dict(_b, card=5, codigo="70116911", descricao="ACABAMENTO PROT DE CICLISTA RETO", marca="Facchini", _nao_agrupar=True,
         info="Material: plástico | Truck | Acabamento protetor de ciclista reto / acabamento protetor caminhão reto",
         aplicacao="Carretas baú e truck modelo Facchini", montadora="Facchini", foto_spec={"rect": [310, 560, 570, 740]})]
NOTAS.append("Pág. 435: 5100112 (chicote 5 vias lanterna Guerra) também está no cap. 33 (pág. 405).")
# 436 (pág. impressa 435): geladeira portátil
ADD.append(dict(pagina=436, card=1, codigo="7001224", descricao="GELADEIRA PORTATIL 40 LITROS", cod_ref="", variacoes="",
                aplicacao="Freezer home / car / outdoor", marca="", montadora="", _nao_agrupar=True,
                info="12V/24V | Medidas do produto embalado (A x L x P): 43 x 70 x 39 cm | Medidas total do produto (A x L x P): 40 x 67cm "
                     "x 36 cm | Material: polietileno, plástico ABS isotérmico, poliuretano, ACM, alumínio | Modelo: 381 | Potência: 48 W | "
                     "Voltagem: 12v 24v / 110v 220v | Peso do produto: 15,3 kg | Capacidade de 40 litros, com dois compartimentos "
                     "individuais, freezer e compartimento de armazenamento refrigerado; temperatura exibida e definida no painel de "
                     "controle com a unidade Celsius ou Fahrenheit | Capacidade: 57 latas (350ml), 28 garrafas (550ml), 15 garrafas (750ml)",
                foto_spec={"rect": [40, 280, 360, 610]}))
