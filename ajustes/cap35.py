# Capítulo 35 - Faróis e Lanternas Pradolux (págs. 418-433; 418 = divisória)
# Cards com par LD/LE (ou um só código): código vermelho + "PDR- ..." na mesma linha; referência Pradolux (PLxxxx) em similares;
# card com vários códigos = 1 produto (itens LD / LE). Foto = retângulo do card.
import json
import os
import re

from capitulos import WORK
from tabela_livre import _spans

TIPOS = [(r"(?:^|\s)LENTE?(?:\s|$)", "LENTE"), (r"MOLD|MOLDURA|ACABAMENTO", "MOLDURA"), (r"(?:^|\s)SUP(?:\s|$)|SUPORTE", "SUPORTE"),
         (r"CHICOTE", "CHICOTE"), (r"SOQUETE", "SOQUETE"), (r"FAROL|MODULO|BLOCO", "FAROL"), (r"LANT|LANTERNA", "LANTERNA")]


def POS_PROC(r):
    for rx, t in TIPOS:
        if re.search(rx, r["descricao"]):
            r["tipo"] = t
            break
AJ = {}
ADD = []
NOTAS = ["Págs. 419-433 (Pradolux): o código Pradolux (PLxxxx) de cada peça está em similares; cards com lado direito (LD) e "
         "esquerdo (LE) viram um produto com os dois códigos."]
MANUAIS = set(range(418, 434))
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


for _p in range(419, 434):
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


MB = "Mercedes-Benz"
# 419 (pág. impressa 418)
T(419, 1, "PDR- MODULO MB ATRON-ATEGO ALTA 2012-2021", LDLE("PDR- MODULO MB ATRON-ATEGO ALTA 2012-2021", "7044123", "7044223"),
  variacoes="PL7029.01.22 - LD / PL7029.02.22 - LE", info="Módulo ótico luz alta | Lente em policarbonato",
  aplicacao="Caminhões MB Atron e Atego 2012-2021")
T(419, 2, "PDR- MODULO MB ATRON-ATEGO BAIXA 2012-2021", LDLE("PDR- MODULO MB ATRON-ATEGO BAIXA 2012-2021", "7046122", "7046223"),
  variacoes="PL7033.01.22 - LD / PL7033.02.22 - LE", info="Pl7033 – módulo ótico luz baixa", aplicacao="MB Actros, Atron e Atego")
T(419, 3, "PDR- FAROL MB DUPLO ANTRON 2012-2021 DIREC", LDLE("PDR- FAROL MB DUPLO ANTRON 2012-2021 DIREC", "7049522", "7049523"),
  variacoes="PL7028.91.22 - LD / PL7028.92.22 - LE", info="Pl7028 – farol principal foco duplo com direcional", aplicacao="MB Atron")
T(419, 4, "PDR- FAROL MB ACCELO 2008", LDLE("PDR- FAROL MB ACCELO 2008", "7043123", "7047122"),
  variacoes="PL7026.01.22 - LD / PL7026.02.22 - LE", info="Farol principal luz alta e baixa | Lente em policarbonato",
  aplicacao="Caminhões MB Accelo modelo 2008 em diante")
T(419, 5, "PDR- FAROL MB PRINC ACTROS CR", {"7041122": "PDR- FAROL MB PRINC ACTROS LD CR", "7041222": "PDR- FAROL MB PRINC ACTROS LE CR"},
  variacoes="PL60320122 - LD / PL60320222 - LE", info="Pl6032 – farol principal", aplicacao="MB Actros")
T(419, 6, "PDR- FAROL MB ANO 2000- MODELO 1620", LDLE("PDR- FAROL MB ANO 2000- MODELO 1620", "7043122", "7043222"),
  variacoes="PL7002.01.22 - LD / PL7002.02.22 - LE",
  info="Farol principal com foco duplo | Disponibilidade de lado esquerdo e direito | Utiliza lâmpada H1",
  aplicacao="Modelo: 1620, 710, 712, 715, 812 e 814")
T(419, 7, "PDR- FAROL MB PRINCIPAL AXOR CR NINO", {"7046030": "PDR- FAROL MB PRINCIPAL AXOR CR LD NINO",
                                                   "7046130": "PDR- FAROL MB PRINCIPAL AXOR CR LE NINO"},
  variacoes="PL6030.01.22 - LD / PL6030.02.22 - LE", cod_ref="9408200261 (LD) / 9408200161 (LE)",
  info="Farol principal com conectores e soquetes tipo originais | Lâmpadas H1 / H7", aplicacao="MB Axor")
T(419, 8, "PDR- LENT FAROL MB PRINC ACTROS CR", {"7046022": "PDR- LENT FAROL MB PRINC ACTROS LD CR",
                                                 "7046023": "PDR- LENT FAROL MB PRINC ACTROS LE CR"},
  variacoes="PL60310122 - LD / PL60310222 - LE", info="")
T(419, 9, "", {"7049922": "PDR- MB SOQUETE NYLON P/LANT PL0520 PL0588"}, variacoes="PL9922.17.96", info="")
T(419, 10, "PDR- LANT MB AXOR PISCA DIANT S/SOQUETE", LDLE("PDR- LANT MB AXOR PISCA DIANT S/SOQUETE", "7040592", "7041592"),
  variacoes="PL0592.01.02 - LD / PL0592.02.02 - LE", info="")
# 420 (pág. impressa 419)
T(420, 1, "PDR- MOLD P/FAROL LANT AUX MB AXOR", LDLE("PDR- MOLD P/FAROL LANT AUX MB AXOR", "7040116", "7040216"),
  variacoes="PL60310116 - LD / PL60310216 - LE", info="Pl6031")
T(420, 2, "FAROL MB AUXILIAR ACTROS", LDLE("FAROL MB AUXILIAR ACTROS", "5110156", "5110056"),
  cod_ref="9438200156 (LD) / 9438200056 (LE)", variacoes="", info="Importado", marca="")
T(420, 3, "FAROL MB PRINC ACTROS", LDLE("FAROL MB PRINC ACTROS", "5111561", "5111461"),
  cod_ref="9438201561 (LD) / 9438201461 (LE)", variacoes="", info="Importado", marca="")
T(420, 4, "FAROL MB AUXILIAR AXOR", {"5110010": "FAROL MB AUXILIAR AXOR L/D", "5110009": "FAROL MB AUXILIAR AXOR L/E"},
  cod_ref="9408200156 (LD) / 9408200056 (LE)", variacoes="", info="Importado", marca="")
T(420, 5, "PDR- MODULO MB ACTRONS ALTA 2012-2021", LDLE("PDR- MODULO MB ACTRONS ALTA 2012-2021", "7045123", "7045124"),
  info="Bloco óptico farol redondo luz alta MB Actros modelo Orion (2016 a 2019)")
T(420, 6, "", {"7040035": "PDR- LANT MB AXOR LATERAL S/SOQ AM CINZA"}, variacoes="PL04760035", info="")
T(420, 7, "", {"7040476": "PDR- LANT S/SOQUETE LATERAL MB AXOR CR CZ AC"}, variacoes="PL04760022", info="",
  aplicacao="Axor 2041, 2540, 2544, 4140 após 2006 (fora de estrada)")
T(420, 8, "", {"7040466": "PDR- LANT S/SOQUETE LATERAL TIPO MB 1938S AM"}, variacoes="PL04660021", info="",
  cod_ref="A 941 826 1021")
T(420, 9, "", {"7049917": "PDR- CHICOTE C/SOQUETE CACHIMBO 2P UNI P/LANT"}, variacoes="PL99173794", info="",
  aplicacao="MB e universal para lanternas Pl0466, PL0476 e Pl0520")
# 421 (pág. impressa 420)
_EST = "PDR- LENT LANT ATEGO ESTRIBO ACRILICO"
T(421, 1, _EST + " CR/AM LE", {"7043577": _EST + " CR LE", "7041577": _EST + " AM LE"},
  variacoes="PL05760222 - LD / PL05770221 - LE", aplicacao="MB Atego",
  info="Lente p/ lanterna estribo | Texto do card: 7043577 'MB Atego - lado direito - amarelo - PL05760222'; "
       "7041577 'MB Atego - lado esquerdo - amarelo - PL05770221'")
T(421, 2, _EST + " CR/AM LD", {"7042577": _EST + " CR LD", "7040577": _EST + " AM LD"},
  variacoes="PL05770122 - LD / PL05770222 - LE", aplicacao="MB Atego",
  info="Lente p/ lanterna estribo | Texto do card: 7042577 'MB Atego - lado direito - cristal - PL05770122'; "
       "7040577 'MB Atego - lado esquerdo - cristal - PL05770222'")
T(421, 3, "PDR- LANT ATEGO ESTRIBO ACRILICO AM", LDLE("PDR- LANT ATEGO ESTRIBO ACRILICO AM", "7042121", "7042221"),
  variacoes="PL05760121 - LD / PL05760221 - LE", cod_ref="9738200421", aplicacao="MB Atego", info="Lanterna estribo | Amarelo")
T(421, 4, "PDR- LANT ATEGO ESTRIBO ACRILICO CR", LDLE("PDR- LANT ATEGO ESTRIBO ACRILICO CR", "7043121", "7043221"),
  variacoes="PL05760122 - LD / PL05760222 - LE", aplicacao="MB Atego", info="Lanterna estribo | Cristal")
T(421, 5, "PDR- LANT MB DIANT AM", {"7041101": "PDR- LANT MB DIANT LD AM", "7041201": "PDR- LANT MB DIANT LE AM"},
  variacoes="PL05280101 - LD / PL05280201 - LE", aplicacao="MB 708 / 709 / 710 / 712 / 912", info="Lanterna direcional | Amarelo")
T(421, 6, "PDR- LANT MB DIANT CR", {"7041102": "PDR- LANT MB DIANT LD CR", "7041202": "PDR- LANT MB DIANT LE CR"},
  variacoes="PL05280102 - LD / PL05280202 - LE", aplicacao="MB 708 / 709 / 710 / 712 / 912", info="Lanterna direcional | Cristal")
T(421, 7, "PDR- LANT MB DIANT S/SOQ REFLE ACRILICO", LDLE("PDR- LANT MB DIANT S/SOQ REFLE ACRILICO", "7040348", "7040349"),
  variacoes="PL03480322 - LD / PL03480422 - LE", aplicacao="MB Atron", info="Lanterna direcional e delimitadora - refletivo")
T(421, 8, "", {"7040580": "PDR- LANT MB DELIMITADORA CABINE CR ACRILICO"}, variacoes="PL05800022", cod_ref="0028205056",
  info="Lanterna delimitadora cabine esq/dir")
T(421, 9, "", {"7040007": "PDR- LANT MB DELIMITADORA CABINE VMCR"}, variacoes="PL05320007", aplicacao="Accelo, Atego, Axor",
  info="Lanterna delimitadora cabine MB VMCR")
NOTAS.append("Pág. 421: nos cards 1 e 2 (lentes de lanterna de estribo Atego) a descrição em vermelho, o lado e a cor do texto "
             "explicativo não batem entre si; foram mantidos como impressos (texto do card em informações).")
# 422 (pág. impressa 421): lanternas dianteiras MB 14/16/18 (bicudo)
_A = "MB 14/16/18"
for _c, _tit, _ld, _le, _dld, _dle, _pl, _inf, _apl in [
        (1, "PDR- LANT MB DIANT S/VIGIA 1989 A 1998 AM", "7040101", "7040201", "PDR- LANT MB DIANT S/VIGIA LD 1989 A 1998 AM",
         "PDR- LANT MB DIANT S/VIGIA LE 1989 A 1998 AM", "PL04480101 - LD / PL04480201 - LE", "Lanterna dianteira | Amarelo",
         "MB 14/16/18 (89 a 98) - Mercedes-Benz bicudo"),
        (2, "PDR- LANT MB DIANT C/VIGIA 98 EM DIANTE AM", "7044501", "7044601", "PDR- LANT MB DIANT C/VIGIA LD 98 EM DIANTE AM",
         "PDR- LANT MB DIANT C/VIGIA LE 98 EM DIANTE AM", "PL04484501 - LD / PL04484601 - LE", "Lanterna pisca/seta com vigia | Amarelo",
         "MB HPN 1620 (98 a 2011)"),
        (3, "PDR- LANT MB LISA DIANT S/VIGIA 89 A 98 AM", "7042301", "7042401", "PDR- LANT MB LISA DIANT S/VIGIA LD 89 A 98 AM",
         "PDR- LANT MB LISA DIANT S/VIGIA LE 89 A 98 AM", "PL04482301 - LD / PL04482401 - LE",
         "Lanterna direcional lente lisa | S/ vigia | Amarela", "MB 14/16/18 (89 a 2011)"),
        (4, "PDR- LANT MB LISA DIANT C/VIGIA 98 AM", "7042501", "7042601", "PDR- LANT MB LISA DIANT C/VIGIA LD 98 AM",
         "PDR- LANT MB LISA DIANT C/VIGIA LE 98 AM", "PL04482501 - LD / PL04482601 - LE",
         "Lanterna direcional lente lisa | C/ vigia | Amarela", "MB 14/16/18 (89 a 2011)"),
        (5, "PDR- LANT MB DIANT S/VIGIA 1989 A 1998 CR", "7040448", "7040449", "PDR- LANT MB DIANT S/VIGIA LD 1989 A 1998 CR",
         "PDR- LANT MB DIANT S/VIGIA LE 1989 A 1998 CR", "PL04480302 - LD / PL04480402 - LE",
         "Lanterna dianteira | Cristal | C/ cúpula s/ vigia", "MB 14/16/18 (89 a 98)"),
        (6, "PDR- LANT MB LISA DIANT S/VIGIA 89 A 98 CR", "7042302", "7042402", "PDR- LANT MB LISA DIANT S/VIGIA LD 89 A 98 CR",
         "PDR- LANT MB LISA DIANT S/VIGIA LE 89 A 98 CR", "PL04482302 - LD / PL04482402 - LE", "Lanterna lisa dianteira s/ vigia | Cristal",
         "MB 14/16/18 (89 a 98)"),
        (7, "PDR- LANT MB LISA DIANT C/VIGIA 98 CR", "7042502", "7042602", "PDR- LANT MB LISA DIANT S/VIGIA LD 98 CR",
         "PDR- LANT MB LISA DIANT C/VIGIA LE 98 CR", "PL04482502 - LD / PL04482602 - LE", "Lanterna lisa dianteira c/ vigia | Cristal",
         "MB (98 em diante)"),
        (8, "PDR- LANT MB DIANT C/VIGIA 98 EM DIANTE CR", "7040402", "7040403", "PDR- LANT MB DIANT C/VIGIA LD 98 EM DIANTE CR",
         "PDR- LANT MB DIANT C/VIGIA LE 98 EM DIANTE CR", "PL04480502 - LD / PL04480602 - LE", "Lanterna dianteira c/ vigia | Cristal",
         "MB 14/16/18 (98 em diante)")]:
    T(422, _c, _tit, {_ld: _dld, _le: _dle}, variacoes=_pl, info=_inf, aplicacao=_apl)
NOTAS.append("Pág. 422: 7042502 está impresso como 'S/VIGIA LD 98 CR', no mesmo card do 7042602 'C/VIGIA LE 98 CR'.")
# 423 (pág. impressa 422): lentes de farol MB (conversão = nº original)
_LF = "LENTE FAROL PRINCIPAL MB"
_AX = "0008260210, 0008264310, 0048260790, 0048262690 e 9408200261"
for _c, _cod, _d, _ref, _apl in [
        (1, "7004410", _LF + " ATEGO LISA LE", "", "Atego 1518, 1718, 2425, 2428 de 2006 até 2012"),
        (2, "7004510", _LF + " ATEGO LISA LD", "", "Atego 1518, 1718, 2425, 2428 de 2006 até 2012"),
        (3, "7003048", _LF + " ACTROS VIDRO LISO LD", "0008264610", "Mercedes-Benz Actros"),
        (4, "7005784", _LF + " ATEGO LE 0048261990", "0048261990 e 9738202661", "Atego 2006 a 2011"),
        (5, "7004628", _LF + " ATEGO LD 0048261290", "0048261990 e 9738202661", "Atego 2006 a 2011"),
        (6, "7003031", _LF + " ACTROS VIDRO LISO LE", "0008264610", "Mercedes-Benz Actros"),
        (7, "7005769", _LF + " AXOR VIDRO DIANT LE", _AX, "Axor"),
        (8, "7005784", _LF + " AXOR VIDRO DIANT LD", _AX, "Axor")]:
    T(423, _c, "", {_cod: _d}, cod_ref=_ref, aplicacao=_apl, variacoes="", info="", marca="")
T(423, 9, "PDR- MOLD BRANCA P/LANT C/ADESIVO PL0448", {"7040415": "PDR- MOLD BRANCA P/LANT C/ADESIVO PL0448 LE",
                                                     "7040414": "PDR- MOLD BRANCA P/LANT C/ADESIVO PL0448 LD"},
  variacoes="PL04480814 (LE) / PL04480714 (LD)", cod_ref="6948847174 (LE) / 6948847274 (LD)", info="")
NOTAS.append("Pág. 423: o código 7005784 aparece em dois cards (lente farol principal MB Atego LE e lente farol principal MB Axor "
             "vidro diant LD); 7005784 (Atego LE) e 7004628 (Atego LD) trazem a mesma conversão (0048261990 e 9738202661).")
# 424 (pág. impressa 423): lanternas traseiras MB
ADD[:] = [r for r in ADD if not (r["pagina"] == 424 and r["codigo"] == "5518425")]  # mini-cards do chicote 5518425 (cap. 33)
_CH = "Chicote usado: 5518425 (chicote 7 vias lanterna 7665 SC/MB)"
T(424, 1, "PDR- LANT MB TRAS S/ VIGIA S/ SIRENE DE RE", {"7044129": "PDR- LANT MB TRAS LD S/ VIGIA S/ SIRENE DE RE",
                                                       "7044229": "PDR- LANT MB TRAS LE S/ VIGIA S/ SIRENE DE RE"},
  variacoes="PL09124129 - LD / PL09124229 - LE", aplicacao="MB Actros", info="")
T(424, 2, "PDR- LANT MB TRAS LED 24V", {"7043369": "PDR- LANT MB TRAS LD S/ VIGIA S/ SIRENE DE RE",
                                       "7043469": "PDR- LANT MB TRAS LE LED 24V C/ VIG S/SIRENE"},
  variacoes="PL0912.33.69 - LD / PL0912.34.69 - LE", aplicacao="MB Accelo, Atego, Axor",
  info="LD: com 64 LEDs, sem sirene de ré e sem vigia | LE: com 70 LEDs, sem sirene de ré e com vigia | LED 24V")
T(424, 3, "LANTERNA TRAS MBB ACTROS", {"7002428": "LANTERNA TRAS LD MBB ACTROS", "7002429": "LANTERNA TRAS LE MBB ACTROS"},
  variacoes="", info="Importado | " + _CH, marca="")
T(424, 4, "LANTERNA LED TRAS MBB ACTROS", {"7002426": "LANTERNA LED TRAS LD MBB ACTROS", "7002427": "LANTERNA LED TRAS LE MBB ACTROS"},
  variacoes="", info="Importado | " + _CH, marca="")
T(424, 8, "", {"7040913": "PDR- LENT LANT ACTROS TRAS ACRILICO PL09130029"}, variacoes="PL09130029", cod_ref="A 002 544 63 03",
  aplicacao="Caminhões, implementos, lanternas traseiras, reposição", info="")
T(424, 9, "PDR- LANT MB LED BIVOLT BORD REFORC C/VIGIA", {"7040716": "PDR- LANT MB LED BIVOLT BORD REFORC C/VIGIA LED - COM VIGIA LD",
                                                       "7042209": "PDR- LANT MB TRAS CAM BORD REFORC VIGIA TRI LE"},
  variacoes="PL07162249 - LD / PL0716.22.09 - LE", info="Lanterna traseira para caminhões Ford / MB", montadora="Mercedes-Benz, Ford")
T(424, 10, "", {"7042209": "PDR- LANT MB TRAS CAM BORD REFORC VIGIA TRI"}, variacoes="PL071622209", info="")
NOTAS.append("Pág. 424: o código 7042209 aparece em dois cards (como LE da lanterna LED bivolt bordo reforçado 7040716 e em card "
             "próprio, lanterna tras cam bord reforc vigia tri); os mini-cards do chicote 5518425 estão no cap. 33.")
# 425 (pág. impressa 424): faróis / módulos Ford Cargo
_FC = dict(montadora="Ford")
T(425, 1, "", {"7047022": "PDR- MODULO FORD OTICO FAROL ALTO 2000 A 2006"}, variacoes="PL7011", info="Módulo ótico farol luz alta",
  aplicacao="Ford Cargo", **_FC)
T(425, 2, "", {"7049022": "PDR- MODULO FORD OTICO FAROL BAIX 2000 A 2006"}, variacoes="PL7013", info="Módulo ótico farol luz baixa",
  aplicacao="Ford Cargo", **_FC)
T(425, 3, "", {"7040022": "PDR- MODULO FORD OTICO FAROL LUZ ALTA 2012"}, variacoes="PL7007.00.22",
  info="Módulo ótico farol luz alta", aplicacao="Ford Cargo 2006", **_FC)
T(425, 4, "", {"7041022": "PDR- MODULO FORD OTICO FAROL LUZ BAIXA 2012"}, variacoes="PL7009.00.22",
  info="Módulo ótico farol luz baixa", aplicacao="Ford Cargo 2006", **_FC)
T(425, 5, "PDR- MODULO FORD OTICO FAROL 816 E 1116", LDLE("PDR- MODULO FORD OTICO FAROL 816 E 1116", "7042123", "7042223"),
  variacoes="PL7023.01.22 - LD / PL7023.02.22 - LE", info="PL7023 – módulo ótico para farol principal",
  aplicacao="Ford Cargo 2012 até 2019", **_FC)
T(425, 6, "PDR- FAROL FORD LUZ BAIXA 2012 MOD 1319", {"7045122": "PDR- FAROL FORD LUZ BAIXA 2012 LD MOD 1319",
                                                     "7045222": "PDR- FAROL FORD LUZ BAIXA 2012 LE MOD 1319"},
  variacoes="PL7008.01.22 - LD / PL7008.02.22 - LE", info="Farol principal de luz baixa | Utiliza lâmpada H-7",
  aplicacao="Ford Cargo modelos 1319, 1519, 1719, 1723, 1729, 1933, 2623 e 3133 de 2012 em diante (cabine Panda)", **_FC)
T(425, 7, "PDR- FAROL FORD HORIZONTAL 2006-2012", LDLE("PDR- FAROL FORD HORIZONTAL 2006-2012", "7049122", "7049222"),
  variacoes="PL7014.01.22 - LD / PL7014.02.22 - LE",
  info="Farol principal com foco duplo traçado horizontal | Com soquete preto | Utiliza lâmpada H-7 com lente em policarbonato",
  aplicacao="Ford Cargo com traçado horizontal para modelos de 2006 a 2012", **_FC)
T(425, 8, "PDR- FAROL FORD LUZ ALTA ANO 2012 MOD 1319", {"7044122": "PDR- FAROL FORD LUZ ALTA ANO 2012 LD MOD 1319",
                                                        "7044222": "PDR- FAROL FORD LUZ ALTA ANO 2012 LE MOD 1319"},
  variacoes="PL7006.01.22 - LD / PL7006.02.22 - LE",
  info="Farol principal de luz alta | Utiliza lâmpada H-7 com lente em policarbonato e carcaça em nylon",
  aplicacao="Ford Cargo modelos 1319, 1519, 1719, 1729, 1933, 2623 e 3133 de 2012 em diante (cabine Panda)", **_FC)
T(425, 9, "PDR- FAROL FORD HORIZONTAL ANOS 2000-2006", {"7040322": "PDR- FAROL FORD HORIZONTAL ANOS 2000-2006 LD",
                                                       "7046222": "PDR- FAROL FORD HORIZONTAL ANOS 2000-2006 LE"},
  variacoes="PL7010.01.22 - LD / PL7010.02.22 - LE",
  info="Farol principal com foco duplo traçado horizontal | Com soquete amarelo | Lâmpada H-7, lente em policarbonato e carcaça em nylon",
  aplicacao="Ford Cargo com traçado horizontal para modelos de 2000 a 2006", **_FC)
T(425, 10, "PDR- FAROL FORD DIAGONAL ANOS 2000-2006", {"7048122": "PDR- FAROL FORD DIAGONAL ANOS 2000-2006 LD",
                                                      "7048222": "PDR- FAROL FORD DIAGONAL ANOS 2000-2006 LE"},
  variacoes="PL7012.01.22 - LD / PL7012.02.22 - LE",
  info="Farol principal com foco duplo traçado diagonal | Com soquete amarelo | Lâmpada H-7, lente em policarbonato e carcaça em nylon",
  aplicacao="Ford Cargo com traçado diagonal para modelos de 2000 a 2006", **_FC)
# 426 (pág. impressa 425): faróis e lanternas VW / Ford
_VW = dict(montadora="Volkswagen")
T(426, 1, "PDR- FAROL VW TITAN/WORKER DUPLO H1 2003", {"7040123": "PDR- FAROL VW TITAN/WORKER DUPLO H1 LD 2003",
                                                      "7040223": "PDR- FAROL VW TITAN/WORKER DUPLO H1 LE 2003"},
  variacoes="PL7020.01.22 - LD / PL7020.02.22 - LE", info="Farol principal com foco duplo horizontal | Lente em policarbonato | "
                                                          "Com soquete preto", aplicacao="Caminhões VW Titan/Worker duplo de 2003 em diante", **_VW)
T(426, 2, "PDR- FAROL VOLKS CONSTELLATION 2006", LDLE("PDR- FAROL VOLKS CONSTELLATION 2006", "7042122", "7042222"),
  variacoes="PL7000.01.22 - LD / PL7000.02.22 - LE",
  info="Pl7000 – farol principal com foco simples | Utiliza lâmpada H-4 | Lente em policarbonato e carcaça em nylon | "
       "Serve inclusive no cavalo mecânico",
  aplicacao="Caminhões VW Constellation 2006 em diante (15180, 13180, 24250 e 26260)", **_VW)
T(426, 3, "PDR- FAROL VW PRINCIPAL 2006-2017", LDLE("PDR- FAROL VW PRINCIPAL 2006-2017", "7041123", "7041223"),
  variacoes="PL7022.01.22 - LD / PL7022.02.22 - LE", info="Farol principal luz alta e baixa | Lente em policarbonato",
  aplicacao="Caminhões VW Delivery", **_VW)
T(426, 4, "", {"7040986": "PDR- LANT VW CONSTELLATION LD CR PL09860102"}, variacoes="PL09860102",
  info="Lanterna dianteira VW Constellation - lado direito - cristal", **_VW)
T(426, 5, "", {"7040482": "PDR- LANT VW TRANS P/CAMINHOES 2011 VM CR"}, variacoes="PL04822107", cod_ref="2S2945096 / 2S2945095",
  info="", **_VW)
T(426, 6, "", {"7040483": "PDR- LENT LANT VW TRANS CAMINHOES 2011 VM CR"}, variacoes="PL04832107 / gl0794",
  cod_ref="2r0945223", info="", **_VW)
T(426, 7, "", {"7040109": "LANTERNA MARMITAO S/VIGIA PRADOLUX"}, variacoes="", cod_ref="Ford 98 HU13404AA / VW T12 945 096 / "
  "Ford 98 HU13405AA / VW T12 945 095", info="Utiliza lâmpada: P21W (1141), P21/5W (1034), PY21W (1056)",
  montadora="Ford, Volkswagen")
T(426, 8, "", {"7002172": "LANT MARMITAO FORD/VW C/VIGIA."}, variacoes="", info="", marca="", montadora="Ford, Volkswagen")
T(426, 9, "LANT LED TRAS C/VIGIA VW/DELIVERY", {"7006054": "LANT LED TRAS C/VIGIA VW/DELIVERY LE 85007161",
                                               "7006055": "LANT LED TRAS S/VIGIA VW/DELIVERY LD 85007151"},
  variacoes="", cod_ref="OEM: 85007161 (LE) / 85007151 (LD)", info="7006054 com vigia", marca="", **_VW)
NOTAS.append("Pág. 426: no card 9, 7006054 está 'C/VIGIA ... LE' e 7006055 'S/VIGIA ... LD'.")
# 427 (pág. impressa 426): lanternas VW e farol Iveco Stralis
T(427, 1, "", {"7040534": "PDR- LANT VOLKS DIANT C/CUPULA CR PL05340302"}, variacoes="PL05340302",
  info="Lanterna dianteira para caminhão VW c/ cúpula - cristal", **_VW)
T(427, 2, "", {"7040536": "PDR- LENT LANT VOLKS DIANT C/CUPULA CR PL0535"}, variacoes="PL05350002",
  info="Lente para lanterna Pl0534 - cristal", **_VW)
T(427, 3, "", {"7040501": "PDR- LANT VOLKS DIANT AM PL05340001"}, variacoes="PL05340001",
  info="Lanterna dianteira para caminhões VW - amarela", **_VW)
T(427, 4, "", {"7040535": "PDR- LENT LANT VOLKS DIANT C/CUPULA AM PL05350001"}, variacoes="PL05350001",
  info="Lente para lanterna Pl0534 - amarela", **_VW)
T(427, 5, "", {"7040001": "PDR- LANT VW CONSTELLATION ESTIBO AM"}, variacoes="PL08960001", info="", **_VW)
T(427, 9, "PDR- FAROL STRALIS APOS 2010 CR NINO", {"7040102": "PDR- FAROL STRALIS APOS 2010 LD CR NINO",
                                                  "7040202": "PDR- FAROL STRALIS APOS 2010 LD CR NINO"},
  variacoes="PL60240102 / PL60240202", info="Ano de fabricação: fabricados a partir de 2010", montadora="Iveco")
NOTAS.append("Pág. 427: 7040102 e 7040202 (farol Stralis) estão impressos com a mesma descrição 'LD'; pela referência PL6024.02 o "
             "7040202 deve ser o LE. Os cards 6, 7 e 8 da página estão vazios e o 10 traz só o logo Iveco.")
# 428 (pág. impressa 427): faróis e lentes Volvo (importados)
_VV = dict(montadora="Volvo", marca="")
_VM = ("VM 17 210 2003-2010; VM 17 240 2004/2005; VM 23 240 2004/2005; VM 260 2006-2010; VM 310 2006-2010")
T(428, 1, "FAROL VOLVO VM ATÉ 2013", {"5110728": "FAROL VOLVO VM ATÉ 2013 L/D", "5110727": "FAROL VOLVO VM ATÉ 2013 L/E"},
  variacoes="", cod_ref="89210728 (LD)", aplicacao=_VM,
  info="Importado | Farol principal Volvo VM até 2013 | Padrão montadora | Não acompanham as lâmpadas", **_VV)
T(428, 2, "FAROL PRINCIPAL PARA CAMINHÃO VOLVO FH D13 DE 2010 A 2014",
  {"5110020": "FAROL PRINCIPAL PARA CAMINHÃO VOLVO FH D13 DE 2010 A 2014 LADO DIREITO",
   "5110019": "FAROL PRINCIPAL PARA CAMINHÃO VOLVO FH D13 DE 2010 A 2014 LADO ESQUERDO"},
  variacoes="", cod_ref="21035637 (LD) / 21035638 (LE)", info="Importado", **_VV)
T(428, 3, "FAROL VOLVO FH12/FM12 04/09", {"5110898": "FAROL VOLVO LE FH12/FM12 04/09", "5110899": "FAROL VOLVO LD FH12/FM12 04/09"},
  variacoes="Similares Volvo: 20713720 / 20360898 / 20861583 (LE); 20713721 / 20360899 / 20762994 / F-182 (LD)",
  cod_ref="20360898 (LE) / 20360899 (LD)", aplicacao="Volvo FH12 FM12 2004 2005 2006 2007", info="Importado", **_VV)
T(428, 4, "FAROL AUXILIAR NEBLINA LONGO ALCANCE VOLVO FH12 FH16",
  {"5117917": "FAROL AUXILIAR NEBLINA LONGO ALCANCE LD DIREITO VOLVO FH12 FH16",
   "5117918": "FAROL AUXILIAR NEBLINA LONGO ALCANCE LE ESQUERDO VOLVO FH12 FH16"},
  variacoes="", cod_ref="21297917 (LD) / 21297918 (LE)", info="Importado", **_VV)
T(428, 5, "ACABAMENTO EXT FAROL VOLVO FH APOS 2021", {"5114117": "ACABAMENTO EXT FAROL VOLVO FH APOS 2021 LE",
                                                     "5115098": "ACABAMENTO EXT FAROL VOLVO FH APOS 2021 LD"},
  variacoes="", cod_ref="84224117 / 84415098", aplicacao="Volvo FH após 2021",
  info="O texto do card diz 'LD' nas duas referências (84224117 e 84415098)", **_VV)
T(428, 6, "PDR- FAROL FH PRINC LED PC CR 2009/2014", {"7040122": "PDR- FAROL FH PRINC LED LD PC CR 2009/2014",
                                                     "7040222": "PDR- FAROL FH PRINC LED LE PC CR 2009/2014"},
  variacoes="PL6018.01.22 - LD / PL6018.02.22 - LE",
  info="Farol principal | Com direcional, LED luz diurna e soquete tipo original | Lente em policarbonato | Não acompanha lâmpada",
  aplicacao="VL FH13 e FM13 2009 até 2016", montadora="Volvo")
T(428, 7, "FAROL VOLVO FH AUXILIAR FH 16 (PL 6010)", {"5111151": "FAROL VOLVO FH AUXILIAR FH 16 LD (PL 6010)",
                                                     "5111152": "FAROL VOLVO FH AUXILIAR FH 16 LE (PL 6010)"},
  variacoes="PL 6010", cod_ref="21221151 / 21221152", info="Importado", **_VV)
T(428, 8, "LENTE FAROL PRINC FH/FM 2009 A 2014", {"7002120": "LENTE FAROL PRINC FH/FM 2009 A 2014 LD",
                                                 "7002119": "LENTE FAROL PRINC FH/FM 2009 A 2014 LE"}, variacoes="", info="", **_VV)
T(428, 9, "LENTE FAROL AUXILIAR FH/FM 2009.. VIDRO", {"7007035": "LENTE FAROL AUXILIAR FH/FM 2009.. LD VIDRO",
                                                     "7007103": "LENTE FAROL AUXILIAR FH/FM 2009.. LE VIDRO"},
  variacoes="Códigos similares: 21035690 / 21120482 / 21297917 (LD); 21035692 / 21297911 (LE)",
  aplicacao="FH / FM 2009 2010 2011 2012 2013 2014", info="Importado", **_VV)
T(428, 10, "LENTE FAROL AUXILIAR VOLVO FH/FM 13 VIDRO", {"7000482": "LENTE FAROL AUXILIAR VOLVO FH/FM 13 VIDRO LD",
                                                        "7008550": "LENTE FAROL AUXILIAR VOLVO FH/FM 13 VIDRO LE"},
  variacoes="", cod_ref="21120482 e PL60050102", aplicacao="Volvo", info="Importado | Conversão: 21120482 e PL60050102", **_VV)
NOTAS.append("Pág. 428: 7000482 e 7008550 (lente farol auxiliar FH/FM13 LD e LE) trazem a mesma conversão (21120482 e PL60050102); "
             "o similar 21297917 do 7007035 é o mesmo número original do farol auxiliar 5117917.")
# 429 (pág. impressa 428): lentes e lanternas Volvo
T(429, 1, "LENTE FAROL PRINC FH/FM 2009 A 2014", {"7002119": "LENTE FAROL PRINC FH/FM 2009 A 2014 LE",
                                                 "7002120": "LENTE FAROL PRINC FH/FM 2009 A 2014 LD"},
  variacoes="", info="Dimensões: alt 43cm x larg 24cm", **_VV)
T(429, 2, "LENTE FAROL PRINC FH/FM 2009 A 2014", {"7002120": "LENTE FAROL PRINC FH/FM 2009 A 2014 LE",
                                                 "7002122": "LENTE FAROL PRINC FH/FM 2009 A 2014 LD"},
  variacoes="", info="Dimensões: alt 60cm x larg 30cm", **_VV)
T(429, 3, "", {"7040021": "PDR- LANTERNA DIRECIONAL VOLVO AMARELO PL0740.00.21"}, variacoes="PL0740.00.21", cod_ref="2134 1202",
  aplicacao="VL VM220, VM2707 e VM330", info="", montadora="Volvo")
T(429, 4, "", {"7040031": "PDR- LANTERNA DIRECIONAL VOLVO CRISTAL PL0740.00.22"}, variacoes="PL0740.00.22", cod_ref="2134 1202",
  aplicacao="VL VM220, VM2707 e VM330", info="", montadora="Volvo")
T(429, 5, "PDR- LANTERNA DIRECIONAL VOLVO VL/VM", {"7040718": "PDR- LANTERNA DIRECIONAL VOLVO VL/VM L/D",
                                                  "7040728": "PDR- LANTERNA DIRECIONAL VOLVO VL/VM L/E"},
  variacoes="PL0708.21.22 (LD) / PL0708.22.22 (LE)", cod_ref="2053 7295 (LD) / 2053 7294 (LE)", aplicacao="VL / VM", info="",
  montadora="Volvo")
T(429, 6, "LANT VOLVO SET FH/FM 2004 A 2009", {"5116211": "LANT VOLVO SET FH/FM 2004 A 2009 LE 20826213",
                                              "5116213": "LANT VOLVO SET FH/FM 2004 A 2009 LD 20826213"},
  variacoes="", cod_ref="20826211 / 20826213", info="", **_VV)
T(429, 7, "PDR- LANT VL TRAS LED 24V BIC", {"7040147": "PDR- LANT VL TRAS LED 24V LD BIC", "7040247": "PDR- LANT VL TRAS LED 24V LE BIC"},
  variacoes="PL1550.01.47 - LD / PL1550.02.47 - LE", aplicacao="VL VM", info="Lanterna traseira LED 24V - sem vigia",
  montadora="Volvo")
T(429, 8, "PDR- LANT FH TRAS LED BIVOLT CONECT TRI", {"7042149": "PDR- LANT FH TRAS LED BIVOLT CONECT LD TRI - SEM VIGIA",
                                                     "7042249": "PDR- LANT FH TRAS LED BIVOLT CONECT LE VIGIA - COM VIGIA"},
  variacoes="PL0728.21.49 - LD / PL0728.22.49 - LE", aplicacao="VL FH", info="Lanterna traseira LED 24V", montadora="Volvo")
T(429, 9, "", {"7042150": "PDR- LENT LANT FH TRAS LED BIVOLT CONECT LD/LE"}, variacoes="PL07290009", info="", montadora="Volvo")
T(429, 10, "LANTERNA TRAS LED VOLVO FH VM", {"7003074": "LANTERNA TRAS LED LE VOLVO FH VM", "7009923": "LANTERNA TRAS LED LD VOLVO FH VM"},
  variacoes="", cod_ref="82483074 (LE) / 82849923 (LD)", info="Importada", **_VV)
NOTAS.append("Pág. 429: o código 7002120 aparece como 'LD' no card 1 e como 'LE' no card 2 (também na pág. 428 como LD); "
             "7040021 e 7040031 trazem a mesma referência (2134 1202); no card 6, 5116211 e 5116213 citam 20826213 na descrição.")
# 430 (pág. impressa 429): faróis e lentes Scania
_SC = dict(montadora="Scania", marca="")
_SIM5 = "Similares Scania: 1760597 / 2241845 / 2416143"
T(430, 1, "FAROL SC PRINCIPAL ELETRICO SERIES S 2019", {"5119893": "FAROL SC PRINCIPAL ELETRICO LD SERIES S 2019",
                                                       "5110889": "FAROL SC PRINCIPAL ELETRICO LE SERIES S 2019"},
  variacoes="", cod_ref="2379893 (LD) / 2379889 (LE)", info="Importado", **_SC)
T(430, 2, "FAROL SCANIA SERIE 5", {"5110597": "FAROL SCANIA SERIE 5 LD", "5110596": "FAROL SCANIA SERIE 5 LE"},
  variacoes=_SIM5, cod_ref="1760597 (LD) / 1760596 (LE)", info="Importado", **_SC)
T(430, 3, "FAROL AUXILIAR INT SCANIA P G R124 INT", {"5116354": "FAROL AUXILIAR INT SCANIA P G R124 INT LD",
                                                    "5116353": "FAROL AUXILIAR INT SCANIA P G R124 INT LE"},
  variacoes="", cod_ref="1446354 (LD) / 1446353 (LE)", aplicacao="Farol auxiliar Scania P G R124 P310 interno longo alcance",
  info="Importado | Interno, longo alcance | Aplicação 'lado direito F204' impressa nos dois", **_SC)
T(430, 4, "LENTE FAROL PRINCIPAL SC S5", {"7007419": "LENTE FAROL PRINCIPAL SC S5 LD", "7007406": "LENTE FAROL PRINCIPAL SC S5 LE"},
  variacoes="Similares Scania: 1549815 / 1521566 (LD); 1549814 / 1521565 (LE)", info="Importado", **_SC)
T(430, 5, "LENTE FAROL PRINCIPAL SC S4", {"7007446": "LENTE FAROL PRINCIPAL SC S4 LD", "7007447": "LENTE FAROL PRINCIPAL SC S4 LE"},
  variacoes="Similares Scania: 1349781 / 1446581 / 1446583 (LD); 1446584 / 1349782 (LE)",
  aplicacao="Série 4 2010 a 2016 - tipo Hella", info="Importado", **_SC)
T(430, 6, "LENTE FAROL SCANIA SERIE 5", {"7000540": "LENTE FAROL SCANIA SERIE 5 LE", "7000549": "LENTE FAROL SCANIA SERIE 5 LD"},
  variacoes="", cod_ref="Conversão: 106986, 1549815, 1730958, 1760554 e 2399977", aplicacao="Scania série 5/P/G/R", info="", **_SC)
T(430, 7, "PDR- LENT LANT SC TRAS AC", {"7041443": "PDR- LENT LANT SC TRAS LD AC PL14430167",
                                       "7042443": "PDR- LENT LANT SC TRAS LE AC PL14430267"},
  variacoes="PL14430167 - LD / PL14430267 - LE", info="LED traseira", montadora="Scania")
T(430, 8, "LENTE FAROL PRINCIPAL SCANIA S4 RAIADA", {"7007948": "LENTE FAROL PRINCIPAL SCANIA S4 RAIADA LE",
                                                    "7007949": "LENTE FAROL PRINCIPAL SCANIA S4 RAIADA LD"},
  variacoes="", cod_ref="Conversão: Scania 1349782, Scania 1407949, Scania 1446584", aplicacao="Série 4 P/R/T", info="", **_SC)
T(430, 9, "LANTERNA SCANIA TS LED STREMLINE", {"7005066": "LANTERNA SCANIA TS LED LE STREMLINE 1905044",
                                              "7005067": "LANTERNA SCANIA TS LED LD STREMLINE 1905043"},
  variacoes="", cod_ref="1905044 (LE) / 1905043 (LD)", info="Importado", **_SC)
T(430, 10, "", {"7060842": "LANTERNA SCANIA TRAS LED LE SERIE 5 / SC124"},
  variacoes="Códigos compatíveis: 85122023 / 8512203 / LT1223E / GD1223 / 1756761", aplicacao="Scania 124, Scania série 5, Scania P, "
  "Scania G, Scania R", info="", **_SC)
T(430, 11, "PDR- LENT LANT PL1616 VERMELHO CRISTAL", {"7040107": "PDR- LENT LANT PL1616 VERMELHO CRISTAL LD",
                                                     "7040207": "PDR- LENT LANT PL1616 VERMELHO CRISTAL LE"},
  variacoes="PL1670107 - LD / PL16170207 - LE", info="", montadora="Scania")
NOTAS.append("Pág. 430: os números vermelhos miúdos dos cards 4 e 5 são similares Scania (não códigos internos); "
             "7000540 e 7000549 trazem a mesma conversão.")
# 431 (pág. impressa 430): DAF, Facchini e MAN
T(431, 1, "PDR- FAROL DAF PRINCIPAL 2010 A 2019", LDLE("PDR- FAROL DAF PRINCIPAL 2010 A 2019", "7046001", "7046002"),
  variacoes="PL60520102 - LD / PL60520202 - LE", info="PL6052 – farol duplo com lanterna direcional", aplicacao="DAF XF 2010 a 2019",
  montadora="DAF")
T(431, 2, "PDR- LANT DAF TRAS S/VIGIA BICOLOR AC", {"7044127": "PDR- LANT DAF TRAS S/VIGIA BICOLOR AC LD",
                                                   "7044227": "PDR- LANT DAF TRAS S/VIGIA BICOLOR AC LE"},
  variacoes="PL16204127 - LD / PL16204227 - LE", info="Lanterna traseira com conector bicolor acríl. DAF XF sem vigia", montadora="DAF")
T(431, 3, "FAROL DAF PRINCIPAL XF", {"5119301": "FAROL DAF PRINCIPAL XF LD 1699301", "5119300": "FAROL DAF PRINCIPAL XF LD 1699300"},
  variacoes="", cod_ref="1699301 / 1699300", info="Importado", marca="", montadora="DAF")
T(431, 4, "PDR- LENT LANT DAF TRAS S/VIGIA BICOLOR AC", {"7040127": "PDR- LENT LANT DAF TRAS S/VIGIA BICOLOR AC LD",
                                                        "7040227": "PDR- LENT LANT DAF TRAS S/VIGIA BICOLOR AC LE"},
  variacoes="PL16210127 - LD / PL16210227 - LE", info="", montadora="DAF")
T(431, 5, "", {"7001156": "LANT LED TRAS F70 FACCHINI HN-01-160"}, variacoes="HN-01-160", info="", marca="", montadora="Facchini")
T(431, 8, "PDR- LENTE LANT MAN LED TRASEIRA VM AZ", {"7040111": "PDR- LENTE LANT MAN LED TRASEIRA LD VM AZ",
                                                    "7040211": "PDR- LENTE LANT MAN LED TRASEIRA LE VM AZ"},
  variacoes="PL16190111 - LD / PL16190211 - LE", info="", montadora="MAN")
T(431, 7, "PDR- FAROL MAN AUXILIAR NEBLINA P/ TGX CR", {"7046026": "PDR- FAROL MAN AUXILIAR NEBLINA P/ TGX LD CR",
                                                       "7046126": "PDR- FAROL MAN AUXILIAR NEBLINA P/ TGX LE CR"},
  variacoes="PL60260102 - LD / PL60260202 - LE", info="", montadora="MAN")
T(431, 9, "PDR- LANT MAN LED TRASEIRA VM AZ", {"7042151": "PDR- LANT MAN LED TRASEIRA LD VM AZ",
                                              "7042251": "PDR- LANT MAN LED TRASEIRA LE VM AZ"},
  variacoes="PL16182151 - LD / PL16182251 - LE", info="", montadora="MAN")
NOTAS.append("Pág. 431: no card 3 (farol DAF principal XF) os dois códigos estão impressos como 'LD' (1699301 e 1699300); "
             "7001156 também aparece como nº de cor no chicote 7 vias lanterna da pág. 406.")
# 432 (pág. impressa 431): lanternas redondas, suporte Noma e chicotes
T(432, 1, "", {"7040782": "PDR- LANT 10 LEDS 96MM BIVOLT AM AC"}, variacoes="PL07820061", info="Lanterna traseira lado direito / esquerdo",
  montadora="Noma")
T(432, 2, "", {"7042467": "PDR- LANT 10 LEDS 3 POLOS 155MM 24V VMCR AC"}, variacoes="PL07882467", info="Lado direito / esquerdo",
  montadora="Noma")
T(432, 3, "", {"7040762": "PDR- LANT FACCHINNI TRAS 10 LEDS 2 PINO 1POLO"}, variacoes="", cod_ref="PL08200067", info="",
  montadora="Facchini")
T(432, 4, "PDR- SUP NOMA TRAS TRIANG BIVOLT TRICOLOR", {"7047569": "PDR- SUP NOMA TRAS TRIANG BIVOLT TRICOLOR LD",
                                                       "7047669": "PDR- SUP NOMA TRAS TRIANG BIVOLT TRICOLOR LE"},
  variacoes="PL21047569 - LD / PL21047669 - LE", info="Universal", montadora="Noma")
T(432, 5, "", {"7040820": "PDR- LANT TRAS 19 LEDS UNIVERSAL 3 FUNÇÕES"}, variacoes="", cod_ref="PL08200067", info="", montadora="")
T(432, 6, "", {"7040824": "PDR- LANT TRAS 19 LEDS UNIVERSAL 4 FUNÇÕES"}, variacoes="PL08200069",
  info="Lanterna 19 LEDs, traseira universal - freio de ré - bivolt", montadora="Mercedes-Benz")
T(432, 7, "", {"7040041": "PDR- LANT LATERAL 2 LEDS BV CABOS HASTE 85MM"}, variacoes="PL0688.00.41",
  info="PL0688 – lanterna lateral com 2 LEDs e haste acoplada | LED bivolt", montadora="")
T(432, 8, "", {"7040056": "PDR- LANT 2 LEDS LUZ PLACA"}, variacoes="PL04800056", info="", montadora="")
T(432, 9, "", {"7043900": "PDR- CHICOTE UNIVERSAL C/CONECTOR 5 VIAS"}, variacoes="PL99533900",
  info="Chicote c/ conector ultra seal 5 vias | Lente para lanterna PL1616 - lado esquerdo - poliestireno PL1670107", montadora="")
T(432, 10, "", {"7049947": "PDR- CHICOTE 7V FEMEA 20CM LANT TRASEIRA"}, variacoes="5518425 (mesmo)", info="", montadora="Scania")
NOTAS.append("Pág. 432: 7040762 e 7040820 trazem a mesma referência original (PL08200067); o card 9 traz também o texto "
             "'Lente para lanterna Pl1616 - lado esquerdo' e o 10 indica '5518425 mesmo'.")
# 433 (pág. impressa 432): lanternas LED ASX / Multilight / Outliers (não Pradolux)
_X = dict(marca="ASX", info="Bivolt")
T(433, 1, "LED GUERRA LANTERNA BIVOLT DIAMOND", {"5515319": "LED GUERRA LANTERNA BIVOLT DIAMOND LE",
                                                "5515309": "LED GUERRA LANTERNA BIVOLT DIAMOND LD"},
  variacoes="ASX5319 (LE) / ASX5309 (LD)", montadora="Guerra", **_X)
T(433, 2, "LANTERNA LED GUERRA 12/24V BIVOLT A", {"5515315": "LANTERNA LED GUERRA 12/24V ESQ BIVOLT A LE",
                                                 "5515305": "LANTERNA LED GUERRA 12/24V DIR BIVOLT A LD"},
  variacoes="", montadora="Guerra", **_X)
T(433, 3, "", {"5515300": "SUPORTE PARA LANTERNA TRASEIRA GUERRA"}, variacoes="", marca="ASX", montadora="Guerra",
  info="Características: chapa de aço | Serve para Guerra 2018, Guerra Diamond 2018, Argos e outras | Pintura eletrostática")
T(433, 4, "LANTERNA LED GUERRA 24V MULT", {"7008220": "LANTERNA LED GUERRA 24V ESQ MULT LE",
                                          "7000822": "LANTERNA LED GUERRA 24V DIR MULT LD"},
  variacoes="", marca="Multilight", montadora="Guerra", info="")
T(433, 5, "LANTERNA TRASEIRA LED MB NEW ACTROS", {"5515322": "LANTERNA TRASEIRA LED MB NEW ACTROS DIREITA",
                                                 "5515332": "LANTERNA TRASEIRA LED MB NEW ACTROS ESQUERDA"},
  variacoes="Cód. 5322 (direita) / 5332 (esquerda)", montadora="Mercedes-Benz", **_X)
T(433, 6, "LANTERNA TRASEIR LED NEW R", {"5515333": "LANTERNA TRASEIR LED NEW R ESQUERDA", "5515323": "LANTERNA TRASEIR LED NEW R DIREITA"},
  variacoes="Cód. 5333 (esquerda) / 5323 (direita)", montadora="Scania", **_X)
T(433, 7, "LED LANTERNA RANDON NEW TRAS", {"5515336": "LED LANTERNA RANDON NEW TRAS LE", "5515326": "LED LANTERNA RANDON NEW TRAS LD"},
  variacoes="ASX5336 (esquerda) / ASX5326 (direita)", montadora="Randon", **_X)
T(433, 8, "LANT.LED TRAS SEQUENCIAL OLOGO", {"7005050": "LANT.LED TRAS SEQUENCIAL OLOGO L/DIREITO",
                                            "7005051": "LANT.LED TRAS SEQUENCIAL OLOGO L/ESQUERDO"},
  variacoes="Outliers @5051", marca="Outliers", montadora="",
  info="Características: 1 - RE | 2 - seta progressiva | 3 - lanterna | 4 - freio | 5 - negativo (GND)")
T(433, 9, "LANTERNA TRASEIRA LED IVECO", {"5515338": "LANTERNA TRASEIRA LED IVECO ESQUERDA", "5515328": "LANTERNA TRASEIRA LED IVECO DIREITA"},
  variacoes="ASX5338 (esquerda) / ASX5328 (direita)", montadora="Iveco", **_X)
T(433, 10, "LANT LED TRASEIRA BOTINHA BIVOLT", {"5515331": "LANT LED TRASEIRA BOTINHA BIVOLT ESQUERDA",
                                               "5515321": "LANT LED TRASEIRA BOTINHA BIVOLT DIREITA"},
  variacoes="ASX5331 (esquerda) / ASX5321 (direita)", montadora="", **_X)
for _c, _cod, _d, _v, _m in [(11, "5515304", "LED RANDON REFIL LANTERNA 2013 BIVOLT A", "ASX5304", "Randon"),
                             (12, "5515316", "LANTERNA TRASEIRA LED MASTER UNIVERSAL", "ASX5316", ""),
                             (13, "5515327", "LANTERNA TRASEIRA LED SCANIA NTG DR", "ASX5327", "Scania"),
                             (14, "5515302", "LED UNIVERSAL LANTERNA TRAS BIVOLT A", "ASX5302", ""),
                             (15, "5511642", "LED LIBRELATO LANTERNA BIVOLT LD/ LE", "LLB", "Librelato"),
                             (19, "5515303", "LANT MARMITAO VW BIVOLT A", "", "Volkswagen"),
                             (20, "5515317", "LANTERNA TRASEIRA LED MARMITÃO LINHA NEW", "ASX5317", "")]:
    T(433, _c, "", {_cod: _d}, variacoes=_v, montadora=_m, **_X)
F(433, "5515327", info="Direita")
T(433, 16, "", {"5515308": "LANTERNA TRASEIRA LED SOFT MULTIFUNÇÕES UNIVERSAL"}, variacoes="ASX5308", marca="ASX", info="12V",
  montadora="")
T(433, 17, "", {"7001890": "LANTE TRAS MB 1114/1614/1618/1620"}, variacoes="", marca="", info="", montadora="Mercedes-Benz")
T(433, 18, "", {"7007369": "LENTE LANTERNA TRICOLOR UNIVERSAL"}, variacoes="", marca="", info="", montadora="Volkswagen, Ford")
T(433, 21, "", {"7065306": "LANTERNA TRASEIRA MB BIVOLT"}, variacoes="", marca="Multilight", info="", montadora="Mercedes-Benz")
NOTAS.append("Pág. 433 (lanternas ASX / Multilight / Outliers): o card 2 traz 5515315 'ESQ ... LE' e 5515305 'DIR ... LD'.")
