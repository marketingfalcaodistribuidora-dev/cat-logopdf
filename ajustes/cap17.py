# Capítulo 17 - Parafusos e Porcas (págs. 203-240)
import json
import os
import re

from capitulos import WORK

TIPOS = [(r"^PRIS|PRISIONEIRO", "PRISIONEIRO"), (r"CRAVO", "CRAVO"), (r"CASTANHA", "CASTANHA DE RODA"),
         (r"VER PORCA", "INDICADOR DE PORCA SOLTA"), (r"PORCA", "PORCA"), (r"ARRUELA|ARR\b", "ARRUELA"),
         (r"PF RD|PARAFUSO RODA", "PARAFUSO DE RODA"), (r"TRANSMISS", "PARAFUSO DE TRANSMISSÃO"),
         (r"BARRA ROSCADA", "BARRA ROSCADA"), (r"PF|PARAFUSO", "PARAFUSO")]
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set()

_CODE = re.compile(r"^\d{5,12}$")
_MARCAS = [(r"\bMBB?\b|MERCEDES", "Mercedes-Benz"), (r"\bFORD\b|\bCARGO", "Ford"), (r"\bVW\b|DELIVERY|VOLKSWAGEN", "Volkswagen"),
           (r"SCANIA", "Scania"), (r"VOLVO", "Volvo"), (r"IVECO", "Iveco"), (r"\bDAF\b", "DAF"), (r"VOLARE", "Volare"),
           (r"RANDON|RANDOM", "Randon"), (r"GUERRA", "Guerra"), (r"\bNOMA\b", "Noma"), (r"RECRUSUL", "Recrusul"),
           (r"FACCHINI", "Facchini"), (r"\bGM\b|CHEVROLET", "GM-Chevrolet")]


def _raw(p):
    return json.load(open(os.path.join(WORK, "raw", f"p{p:03d}.json"), encoding="utf-8"))


def _linhas(spans, tol=2.5):
    out = []
    for s in sorted(spans, key=lambda s: (s["y"], s["x"])):
        if out and abs(out[-1][0] - s["y"]) < tol:
            out[-1][1].append(s)
        else:
            out.append([s["y"], [s]])
    return [" ".join(x["t"].strip() for x in sorted(l[1], key=lambda s: s["x"])).strip() for l in out]


def marcas(txt):
    return [m for rx, m in _MARCAS if re.search(rx, txt, re.I)]


def card_roda(p, card, app_max=6.5):
    """Card de parafuso/porca de roda: código vermelho, descrição, similares ZM/FEY e aplicação em letra miúda."""
    spans = [s for ln in card["lines"] for s in ln if s["t"].strip()]
    cods = [s["t"].replace(" ", "") for s in spans if s["red"] and _CODE.match(s["t"].replace(" ", ""))]
    if len(cods) != 1:
        return None
    sim, ref, info, desc, app = [], [], [], [], []
    for s in spans:
        t = s["t"].strip()
        if s["red"] and _CODE.match(t.replace(" ", "")):
            continue
        m = re.match(r"^(?:REF\s*)?(ZM|FEY)\s*:?\s*(.*)$", t, re.I)
        if m:
            if m.group(2).strip():
                sim.append(f"{m.group(1).upper()} {m.group(2).strip()}")
            continue
        if re.match(r"^REG\.? ORIG", t, re.I):
            ref.append(re.sub(r"^REG\.? ORIG\.?\s*", "", t, flags=re.I))
            continue
        if re.fullmatch(r"(CAMPE[ÃA]O DE )?VENDAS|CAMPE[ÃA]O DE", t, re.I):
            continue
        if re.match(r"^LAN[ÇC]AMENTO", t, re.I):
            info.append("LANÇAMENTO")
            continue
        (app if s["size"] < app_max else desc).append(s)
    d = re.sub(r"\s+", " ", " ".join(_linhas(desc))).strip()
    # aplicação pode vir em 2 colunas (ex.: "INTERNATIONAL TODOS/ALL" à esquerda): junta cada coluna separadamente
    x0, x1 = card["rect"][0], card["rect"][2]
    meio = x0 + 0.42 * (x1 - x0)
    dir_ = [s for s in app if s["x"] >= meio]
    esq = [s for s in app if s["x"] < meio]
    a = " / ".join(_linhas(dir_) + _linhas(esq)) if dir_ else " / ".join(_linhas(esq))
    return dict(codigo=cods[0], descricao=d, variacoes=" / ".join(sim), cod_ref=" / ".join(ref), aplicacao=a,
                info=" | ".join(info), montadora=", ".join(marcas(d + " " + a)))


def aplicar_roda(paginas, **kw):
    for p in paginas:
        for c in _raw(p)["cards"]:
            if c["id"] == 0:
                continue
            r = card_roda(p, c, **kw)
            if r:
                AJ[f"{p}.{c['id']}"] = {"records": [r]}


# ---- págs. 203-210: parafusos, porcas e prisioneiros de roda (similares ZM / FEY)
aplicar_roda(range(203, 211))
# logos de montadora (vetoriais, lidas na página) que o texto não traz
_LOGO = {
    "563272": "Mercedes-Benz", "581153": "Mercedes-Benz, Randon", "581154": "Mercedes-Benz, Randon", "582211": "Mercedes-Benz, Randon",
    "592082": "Ford", "520714": "Ford", "520715": "Ford", "525824": "Ford", "525821": "Ford", "521872": "Ford", "521881": "Ford",
    "520728": "Ford", "520727": "Ford",
    "511806": "Ford, Volkswagen", "511890": "Ford, Volkswagen", "511943": "Mercedes-Benz, Ford, Volkswagen",
    "582080": "Guerra, Scania", "591885": "Scania", "750814": "Iveco", "75716112": "Volvo",
    "751190": "Mercedes-Benz", "751232": "Mercedes-Benz",
}
for _c in ("522080", "522090", "522092", "524002060", "522010", "522151", "520968", "522263", "522216", "523002021"):
    _LOGO[_c] = "Ford, Volkswagen"
AJ["205.4"] = {"records": [dict(codigo="520714", descricao="PORCA RODA DIANT/TRAS 5/8\" CH 1.1/16\" ESQUERD",
                                variacoes="ZM 29.508.02 / FEY 13730", aplicacao="D400/F350 / F400/F4000", montadora="Ford")]}
AJ["205.5"] = {"records": [dict(codigo="520715", descricao="PORCA RODA F4000 5/8 ROSCA DIR 5/8", variacoes="ZM 29.508.01 / FEY 13709",
                                aplicacao="CHRYSLER-DODGE / D400/F350 / F400/F4000 / FREIO A DISCO / DISC BRAKE 1990 1990 / F4000 1976",
                                montadora="Ford, Chrysler-Dodge")]}


def POS_PROC(r):
    _completa(r)
    if int(str(r["pagina"]).split(",")[0]) >= 213:
        # a partir da pág. 213 "MA"/"MB" = rosca métrica grossa/fina (não Mercedes-Benz): só vale montadora escrita por extenso
        # item de grupo: só a montadora do título do grupo (a de um item isolado aparece na coluna de variações)
        txt = r["_titulo"] if r.get("_titulo") else " ".join(str(r.get(k, "")) for k in ("descricao", "aplicacao"))
        ms = [m for rx, m in [(r"VOLVO", "Volvo"), (r"SCANIA", "Scania"), (r"FIAT", "Fiat"), (r"CHEVETTE", "GM-Chevrolet"),
                              (r"MERCEDES|\bMBB\b", "Mercedes-Benz"), (r"\bVW\b|VOLKSWAGEN", "Volkswagen")] if re.search(rx, txt)]
        r["montadora"] = ", ".join(ms)
    extra = _LOGO.get(r["codigo"])
    if extra:
        ms = [m.strip() for m in (r.get("montadora", "") + ", " + extra).split(",") if m.strip()]
        r["montadora"] = ", ".join(dict.fromkeys(ms))

# ---- correções 206-210
AJ["206.1"]["records"][0].update(descricao="PF RD FORD 20X90/97 D/T SIMPLES",
                                 aplicacao="Cargo 1113 / Cargo 1114 / Cargo 1117 / 12.140 H / 16.210 / 16.220")
AJ["206.11"]["records"][0].update(descricao="PF RD SCANIA 7/8X11", info="O card não traz descrição impressa (só código, similares e aplicação)")
AJ["206.22"]["records"][0]["descricao"] = "PF RD DAF OSC 22X100 REC Ch32 TRASEIRO"
AJ["206.23"]["records"][0]["descricao"] = "PF RD DAF OSC 22X104 REC Ch32 TRASEIRO"
AJ["207.21"]["records"][0]["aplicacao"] = "Cursor 450E37 / Cursor 8190E31 / E37 / HM 200 / HM 450E37"
AJ["208.17"]["records"][0]["variacoes"] = "ZM 33.030.58"
AJ["208.18"]["records"][0].update(descricao="VER PORCA RODA Ch32 LARANJA", variacoes="ZM 33.032.54")
AJ["209.13"] = {"records": [
    dict(codigo="3662015", descricao="PORCA RODA PF RANDON MARTELO R FINA Ch27", montadora="Randon", tipo="PORCA",
         info="Texto presente no PDF, mas coberto pelo card da Facchini (não aparece na página impressa)"),
    dict(codigo="36878272", descricao="PORCA PINO EXCENTRICO FACCHINI 1\" UNC", montadora="Facchini", tipo="PORCA")]}
AJ["209.13"]["_nao_agrupar"] = True
AJ["210.6"] = {"records": [dict(codigo=c, descricao=d, _titulo="PRISIONEIRO COMPLETO UNC / UNF", tipo="PRISIONEIRO") for c, d in [
    ("2503434", "PRIS. COMP 3/4-10UNC X 3/4-10UNC X 3"), ("2505858", "PRIS. COMP 5/8-11UNC X 5/8-18UNF X 3,13/32"),
    ("25012916", "PRIS. COMP 1/2-20UNF X 9/16-12UNC X 2.1/2"), ("25058583", "PRIS. COMP 5/8-11UNC X 5/8-18UNF X 3"),
    ("250581158", "PRIS. COMP 5/8-11UNC X 5/8-18UNF X 2.1/5"), ("250121312", "PRIS. COMP 1/2-13UNC X 1/2-20UNF X 2"),
    ("250916916", "PRIS. COMP 9/16-12UNC X 9/16-18UNF X 63,5")]]}
AJ["210.9"]["records"][0].update(aplicacao="MB 1111/1113 / 1513/2013", info="12 X 57")
AJ["210.15"] = {"info": ""}
AJ["210.16"] = {"info": "", "_titulo": "PF TRANSMISSAO"}
NOTAS.append("Pág. 209: o código 3662015 (PORCA RODA PF RANDON MARTELO R FINA Ch27) está no texto do PDF, mas coberto pelo card "
             "da Facchini (36878272); foi registrado mesmo assim.")
NOTAS.append("Pág. 210: a lista de PF TRANSMISSAO repete códigos que também têm card próprio (750814, 75716112, 751190, 751232).")
NOTAS.append("Págs. 203-210: a coluna 'Outras referências / similares' traz os códigos equivalentes ZM e FEY impressos em cada card.")
AJ["cod:3662015"] = {"foto_spec": None}  # a foto do card é da porca Facchini

# ---- pág. 211
AJ["cod:2741675"] = dict(cod_ref="4220320271", info="", aplicacao=(
    "Parafuso volante motor OM 447/449 M16X75x1,5 MB 4220320271 - METALAC PA800786102R / Mercedes caminhão L1625 "
    "(motor OM442 OM447 OM449LA) / Mercedes ônibus O400RSL O400UP O400UPA O400PL OH1628 O371R O371UP Oh1635 Ol1635 O371R O500 "
    "(motor OM442 OM447 OM449LA)"))
AJ["cod:5524200"] = dict(descricao="PARAFUSO DO SUPORTE DE MOLAS SCANIA", info="Classe 10.9",
                         aplicacao="Parafuso do Suporte Dianteiro de Molas SCANIA NTG Série L / P / G / R / S")
AJ["cod:36116150"] = dict(descricao="PORCA FLANGE 16 MB 1,5 TORQUE MACHO P/SOQ E16", info="Classe 10",
                          aplicacao="Porca da Longarina Caminhões Mercedes-Benz")
AJ["cod:3610160"] = dict(descricao="PORCA FLANGE 16 MB 1,5 TORQUE SPRINTER DIANT", info="Classe 10",
                         aplicacao="Porca do Amortecedor Dianteiro Sprinter Modelos da Série 906 (2006 a 2018)")
AJ["cod:3611825"] = dict(aplicacao="Porca do Tirante Dianteiro Volkswagen Constellation")
AJ["cod:3612025"] = dict(aplicacao="Porca do Parafuso do Jumelo Dianteiro/Traseiro Volvo FH/FM a partir de 2006", montadora="Volvo")

# ---- pág. 212 (página sem moldura: 2 grupos de parafusos de suspensão Mercedes-Benz)
MANUAIS.add(212)
_F212 = {"rect": [385, 85, 575, 290]}
_INF212 = "Classe 10.9 | Revestimento organometálico | Embalagem: 15 unidades"
for _cs, _tit, _ref, _apl in [
        (("27422150", "27422170", "27422180"), "PARAFUSO SUSPENSÃO MERCEDES-BENZ 22 X 1,5 - BRAÇO SUSP. PNEUMÁTICA",
         "A0049902103 / A0049902203 / A0019906203", "Braço Susp. Pneumática Arocs, New Actros (A Partir De 2024) E Axor"),
        (("27422200", "27422230", "27422240"), "PARAFUSO SUSPENSÃO MERCEDES-BENZ 22 X 1,5 - FIXAÇÃO FEIXES DIANTEIROS",
         "A0049900303 / A0019906303 / A0019908303", "Fixação Feixes Dianteiros Arocs, New Actros (A Partir De 2024) E Axor")]:
    for _c in _cs:
        ADD.append(dict(pagina=212, card=1 if _cs[0] == "27422150" else 2, codigo=_c, _titulo=_tit, tipo="PARAFUSO",
                        descricao=f"22 X {_c[-3:]} PF FLANGE ACO 10.9 MB 1,5 TORQ MACHO", cod_ref=_ref, aplicacao=_apl,
                        info=_INF212, montadora="Mercedes-Benz", foto_spec=_F212))
NOTAS.append("Pág. 212: as tabelas do alto da página (dimensão x código x código Mercedes) não batem com as listas de códigos "
             "em vermelho (ex.: tabela do braço pneumático cita 27422240, a lista traz 27422180). Foram usadas as listas; "
             "os códigos originais de cada grupo estão na coluna de referência.")

# ---- págs. 213+ em "tabela livre" (listas por diâmetro + caixinhas de arruelas/porcas): scripts/tabela_livre.py
from tabela_livre import ler_pagina  # noqa: E402

TL_OPCOES = {}


def tabela(p, **kw):
    MANUAIS.add(p)
    regs = ler_pagina(p, **dict(TL_OPCOES.get(p, {}), **kw))
    for r in regs:
        r.pop("_bbox", None)
    ADD.extend(regs)
    return regs


def _sem_desc_lookup():
    """Caixinhas que só trazem o código: usa a descrição do mesmo código em outra página do capítulo."""
    d = {}
    for r in ADD:
        if r.get("descricao") and r["codigo"] not in d:
            d[r["codigo"]] = (r["descricao"], r["pagina"])
    return d


_LOOKUP = {}


def _completa(r):
    if r.get("descricao") or " / " in r["codigo"]:
        return
    if not _LOOKUP:
        _LOOKUP.update(_sem_desc_lookup())
        _LOOKUP.update(DESC_EXTRA)
    if r["codigo"] in _LOOKUP:
        d, p = _LOOKUP[r["codigo"]]
        r["descricao"] = d
        r["info"] = " | ".join(x for x in (r.get("info", ""), f"Na pág. {r['pagina']} só aparece o código; "
                                                              f"descrição conforme pág. {p}") if x)


DESC_EXTRA = {}  # código -> (descrição, página PDF de onde veio)


def fix(p, codigo, **campos):
    achou = [r for r in ADD if r["pagina"] == p and r["codigo"] == codigo]
    assert achou, f"fix: {codigo} não está na pág. {p}"
    for r in achou:
        r.update(campos)


def novo(p, codigo, descricao, rect=None, **kw):
    n = max([r.get("card", 0) for r in ADD if r["pagina"] == p] + [0]) + 1
    ADD.append(dict(pagina=p, card=n, codigo=codigo, descricao=descricao, _nao_agrupar=True,
                    foto_spec={"rect": rect} if rect else None, **kw))


for _p in range(213, 229):
    if _p != 224:
        tabela(_p)

# 213
NOTAS.append("Pág. 213: na seção 08MM a caixinha 4411212 traz 'ARR.PRESSÃO PESADA 14MM' (na seção 12MM o mesmo código é "
             "'ARR.PRESSÃO PESADA 12MM'); registrado uma vez só.")
# 215
fix(215, "632250", descricao="22 X 50 PF MB ACO RI 8.8")
fix(215, "3682215", descricao="")
fix(215, "632480", descricao="24 X 80 PF SX ACO 2,0 R FINA CH36 RP")
fix(215, "3611615", foto_spec={"rect": [487, 556, 525, 593]})
novo(215, "3160010", "PORCA DUPLA MB 10X1,00", [27, 266, 86, 314], info="Código impresso dentro da imagem ('316 0010')")
novo(215, "751190", "PF TRANSMISSAO 10 X 30 1113", [89, 266, 157, 314], info="Código impresso dentro da imagem ('075 1190')")
novo(215, "751232", "PF TRANSMISSAO 12 X 32 1313/15", [359, 266, 427, 314], info="Código impresso dentro da imagem ('075 1232')")
# 216
fix(216, "2741435", descricao="14 X 35 PF FLANGE PINO REI ACO")
fix(216, "2741645", descricao="16 X 45 PF FLANGE PINO REI ACO")
# 218
fix(218, "3160010", descricao="PORCA DUPLA MB 10X1,00")
fix(218, "4070020", descricao="ARR.LISA Z ZB 20MM")
fix(218, "4110034", descricao="ARR.LISA Z ZB 3/4", info="Texto parcialmente coberto na página ('RR.LISA Z ZB 3/4')")
fix(218, "4110038", descricao="ARR.LISA H ZB 3/8", info="Texto parcialmente coberto na página")
# 219
fix(219, "4070078", descricao="ARR.LISA O ZB 7/8 (22MM)")
fix(219, "6324101", info="LANÇAMENTO")
fix(219, "6324141", info="LANÇAMENTO")
# 220
fix(220, "4070020", descricao="ARR.LISA Z ZB 20MM")
NOTAS.append("Pág. 220: a caixinha 4070020 traz a descrição 'ARR.LISA Z ZB 24MM X 43MM' (nas demais páginas 4070020 é "
             "ARR.LISA Z ZB 20MM e a de 24MM X 43MM é 4072400); mantida a descrição de 20MM.")
# 221
fix(221, "4070018", descricao="ARR.LISA Z 18MM", info="O card não traz descrição impressa (só código e foto)")
# 226-228: arruelas com código dentro da imagem
novo(226, "4110014", "ARR.LISA D ZB 1/4", [413, 94, 449, 122], info="Código impresso dentro da imagem")
novo(226, "4110516", "ARR.LISA F ZB 5/16", [414, 208, 456, 238], info="Código impresso dentro da imagem")
novo(226, "4110038", "ARR.LISA H ZB 3/8", [417, 373, 465, 406], info="Código impresso dentro da imagem")
novo(226, "4110716", "ARR.LISA I ZB 7/16 1,7EXP", [410, 524, 449, 553], info="Código impresso dentro da imagem")
fix(226, "3740078", descricao="PORCA TRAVANTE C UNC 7/16")
NOTAS.append("Pág. 226: a porca travante 7/16 está com o código 3740078, o mesmo da PORCA TRAVANTE UNC 7/8 das págs. 223 e 228.")
fix(227, "3740012", descricao="PORCA TRAVANTE D UNC 1/2")
novo(227, "4110012", "ARR.LISA J ZB 1/2 3MM EXP", [419, 112, 469, 150], info="Código impresso dentro da imagem")
novo(227, "4110058", "ARR.LISA M ZB 5/8 3MM EXP", [412, 386, 461, 419], info="Código impresso dentro da imagem")
novo(227, "4110034", "ARR.LISA N ZB 3/4", [417, 535, 459, 565], info="Código impresso dentro da imagem")
novo(228, "411784617", "ARR.LISA 7/8 23,5MM X 46MM X 1,7 MM ZB", [462, 92, 506, 122], info="Código impresso dentro da imagem")

# 224: parafuso e porca rosca 1,25 Fiat (descrição longe do código)
MANUAIS.add(224)
for _c, _d in (("631062", "10 X 60 FIAT PF SX ACO 1,25 R FINA CH17"), ("631072", "10 X 70 FIAT PF SX ACO 1,25 R FINA CH17"),
               ("631092", "10 X 90 FIAT PF SX ACO 1,25 R FINA CH17")):
    ADD.append(dict(pagina=224, card=1, codigo=_c, descricao=_d, _titulo="PARAFUSO ROSCA 1,25 FIAT PF SX ACO R FINA CH17 - 10MM",
                    montadora="Fiat", foto_spec={"rect": [436, 164, 564, 464]}))
for _c, _d in (("631236", "12 X 35 FIAT PF SX ACO 1,25 R FINA CH19"), ("631242", "12 X 40 FIAT PF SX ACO 1,25 R FINA CH19"),
               ("631252", "12 X 50 FIAT PF SX ACO 1,25 R FINA CH19"), ("631272", "12 X 70 FIAT PF SX ACO 1,25 R FINA CH19"),
               ("631292", "12 X 90 FIAT PF SX ACO 1,25 R FINA CH19")):
    ADD.append(dict(pagina=224, card=2, codigo=_c, descricao=_d, _titulo="PARAFUSO ROSCA 1,25 FIAT PF SX ACO R FINA CH19 - 12MM",
                    montadora="Fiat", foto_spec={"rect": [436, 164, 564, 464]}))
ADD.append(dict(pagina=224, card=3, codigo="31710125", descricao="PORCA SEXT 10MM FIAT MB G R 1,25 CH17", montadora="Fiat",
                _nao_agrupar=True, foto_spec={"rect": [34, 634, 170, 764]}))
ADD.append(dict(pagina=224, card=4, codigo="31712125", descricao="PORCA SEXT 12MM FIAT MB G R 1,25 CH17", montadora="Fiat",
                _nao_agrupar=True, foto_spec={"rect": [34, 634, 170, 764]}))
# 214: os códigos 3681820 e 3171800 vêm grudados num só trecho de texto ("36818203171800")
novo(214, "3681820", "", [32, 389, 73, 424])
novo(214, "3171800", "", [83, 390, 128, 424])


def foto_grupo(p, codigos, rect, **campos):
    for c in codigos:
        fix(p, c, foto_spec={"rect": rect}, **campos)


TL_OPCOES[229] = {"gap_primeiro": 80}
for _p in (229, 230, 231):
    tabela(_p)
# 230
foto_grupo(230, ["22234212", "22234214", "22234234", "22234318", "22258212", "22258214", "2225803"], [36, 402, 114, 566])
fix(230, "2220058", descricao="PORCA PF ARADO 5/8 UNC", foto_spec={"rect": [34, 595, 77, 677]})
fix(230, "2220034", descricao="PORCA PF ARADO 3/4 UNC", foto_spec={"rect": [34, 595, 77, 677]})
fix(230, "5070001", descricao="PF FACA FORRAGEIRA GRAU 5", foto_spec={"rect": [45, 695, 209, 786]})
# 231
foto_grupo(231, ["1296325", "1291212", "1291234", "1291278"], [43, 95, 136, 236])
fix(231, "1290351", descricao="PF PARALAMA DO CHEVETTE 6,3X19MM", montadora="GM-Chevrolet")
foto_grupo(231, ["1294219", "1294225", "1294232", "1294238"], [32, 364, 177, 455], info="Parafuso Brocante Flangeado Phillips")
foto_grupo(231, ["1294220", "1294226"], [25, 489, 173, 536])
fix(231, "1101525", descricao="PF.TORX 4,2 X 25 ASSOALHO AUTOBROCANTE", foto_spec={"rect": [43, 555, 180, 611]},
    info="Parafuso Atarrachante Assoalho Ponta Broca Redonda Torx Zincado")
fix(231, "1141547", descricao="PF PHILIPS SOBERBA 4,8X38 PRE", foto_spec={"rect": [59, 695, 132, 759]})

# 232
tabela(232)
for _r in ADD:
    if _r["pagina"] == 232 and _r["codigo"].startswith("27"):
        _r["foto_spec"] = {"rect": [25, 509, 236, 773]}
# 233: página com a grade vazia (sem produtos)
NOTAS.append("Pág. 233: página só com a grade de cards, sem produtos.")
# 234: grade de caixinhas (descrição em fonte grande)
MANUAIS.add(234)
_L1, _L2, _L3, _L4, _L5 = (126, 260), (261, 429), (430, 545), (545, 674), (675, 805)
_G234 = [
    ("2740001", "PF 06 X 12 CH 8", (26, 116), _L1), ("2740075", "PF 06 X 15 CH 8 - F075-PF. CH8 PLACA", (116, 200), _L1),
    ("2740074", "PF 06 X 20 CH 8 - F074-PF. CH8 6X20", (200, 285), _L1), ("2740073", "PF 06 X 25 CH 8 - F073-PF. CH8 6X25", (285, 383), _L1),
    ("2740365", "PF 06 X 28 CH 8 - F365-PF. TAMPA DE VÁLVULA CH8", (383, 481), _L1), ("2740006", "PF 06 X 30 CH8", (481, 569), _L1),
    ("2740071", "PF 06 X 35 CH 8 - F071-PF. TAMPA 6X35 LATERAL MOTOR CH8", (26, 144), _L2),
    ("2740364", "PF 06 X 40 CH 8 - F364-PF. TAMPA 6X40 LATERAL MOTOR CH8", (144, 257), _L2),
    ("2740390", "PF 06 X 45 CH 8", (257, 341), _L2), ("2740070", "PF 06 X 50 CH 8 - F070-PF. CENTRAL 6X50 MOTOR CH8", (341, 467), _L2),
    ("2740103", "PF 06 X 60 CH 8 - F103-PF.MOTOR 6X60 CH8", (467, 569), _L2),
    ("2740612", "PF 06 X 12 CH 10", (26, 116), _L3), ("2740177", "PF 06 X 16 CH 10", (116, 200), _L3),
    ("2740620", "PF 06 X 20 CH 10", (200, 285), _L3), ("2740625", "PF 06 X 25 CH 10", (285, 369), _L3),
    ("2740367", "PF 06 X 28 CH 10 TAMPA VALVULA ORIGINAL", (369, 467), _L3), ("2740092", "PF 06 X 30 CH 10", (467, 569), _L3),
    ("2740176", "PF.FLANGE CH 12 08 X 20", (26, 158), _L4), ("2740020", "PF.FLANGE CH 12 08 X 25", (158, 299), _L4),
    ("3610062", "PORCA FLANGE 06 MM CH 10", (299, 425), _L4), ("3610060", "PORCA FLANGE 08MM TAMPA LATERAL", (425, 569), _L4),
    ("3610064", "PORCA FLANGE 10MM PRIS COROA CG", (26, 158), _L5), ("3610063", "PORCA CG MAGNETO 12X1,25 FLG", (158, 299), _L5),
    ("3611212", "PORCA CG EIXO DIANT CG 12X1,25", (299, 425), _L5), ("3611413", "PORCA FLANGE 14 MB 1,5", (425, 569), _L5)]
for _i, (_c, _d, (_x0, _x1), (_y0, _y1)) in enumerate(_G234):
    ADD.append(dict(pagina=234, card=_i + 1, codigo=_c, descricao=_d, faixa=[_x0, _y0, _x1, _y1], fonte_titulo=1,
                    _nao_agrupar=True, tipo="PORCA" if _d.startswith("PORCA") else "PARAFUSO"))


_CT = {}


def _card_titulo(p, titulo):
    if (p, titulo) not in _CT:
        _CT[(p, titulo)] = 60 + sum(1 for k in _CT if k[0] == p)
    return _CT[(p, titulo)]


def grupo(p, codigos, titulo, rect=None, **campos):
    """Define título (=> agrupamento) e foto de um conjunto de códigos da página."""
    for c in codigos:
        extra = dict(campos, _titulo=titulo, _nao_agrupar=False, card=_card_titulo(p, titulo))
        if rect:
            extra["foto_spec"] = {"rect": rect}
        fix(p, c, **extra)


# 235 - porcas
tabela(235, separar_diam=False)
grupo(235, ["333516", "33338", "333716", "3337160", "33312", "3330916", "3330058", "3330078", "3330001", "3330118", "3330034"],
      "PORCA UNF", [392, 133, 532, 253])
grupo(235, ["3172122", "3170004", "3170005", "3170006", "3170007", "3170008", "3178000", "3170010", "3171015", "31712", "3171215",
            "31714", "3171415", "31716", "3170016", "3171800", "3171815", "3172020", "3172015", "31722", "3172215", "3170944"],
      "PORCA SEXTAVADA MÉTRICA", [48, 253, 232, 455])
grupo(235, ["3320018", "332316", "332532", "33214", "332516", "33238", "332716", "33212", "332916", "3320058", "3320034",
            "33278", "3327800", "3321045", "3320112", "332114"], "PORCA UNC", [180, 528, 258, 678])
grupo(235, ["3170100", "3170120", "3170140"], "PORCA SEXTAVADA TORQUE ZB", [48, 705, 148, 795])
fix(235, "3171615", info="O código 3171615 aparece duas vezes na página: 'PORCA SEXT 16MM TORX MB FINA' e "
                         "'PORCA SEXT 16MM TORQUE MB CH24 ZB'")
fix(235, "3178000", info="Também listada como 'PORCA SEXT 08MM TORQUE MA CH13 ZB'")
fix(235, "3173061", descricao="PORCA REBITE LI PLA 3,0 M6", foto_spec={"rect": [380, 547, 505, 610]})
fix(235, "3173008", descricao="PORCA REBITE LI PLA 3,0 M8", foto_spec={"rect": [382, 640, 525, 705]})
NOTAS.append("Pág. 235: o código 3171615 aparece com duas descrições (PORCA SEXT 16MM TORX MB FINA e PORCA SEXT 16MM TORQUE "
             "MB CH24 ZB); o 3178000 também aparece duas vezes (com e sem 'CH13').")

# 236 - porca travante
tabela(236, separar_diam=False, gap_primeiro=80)
grupo(236, ["3680006", "3680008", "3681000", "36812175", "3681420", "3681620", "3681820", "3682020", "3680022", "3682430",
            "3683021", "3681215", "3681415", "3681615", "3681815", "3682015", "3682215", "3682415", "3680863", "3683020"],
      "PORCA TRAVANTE MÉTRICA", [296, 158, 525, 345])
grupo(236, ["3740014", "3740516", "3740038", "3740012", "3741212", "3740058", "3740034", "3740078", "3740001", "3741283"],
      "PORCA TRAVANTE UNC", [45, 462, 216, 547])
grupo(236, ["3730038", "3730012", "3730916", "3730058", "3730034", "3730078", "3730001"], "PORCA TRAVANTE UNF",
      [296, 158, 525, 345])
NOTAS.append("Pág. 236: a lista de porcas travantes UNC termina com 3741283 'PORCA TRAVANTE D UNC 1/2' (já existe 3740012 "
             "'PORCA TR UNC E 1/2'). Na pág. 226 a porca travante 7/16 usa o código 3740078, o mesmo da UNC H 7/8 desta página.")
# 237 - porca dupla, castelo e flange
tabela(237, separar_diam=False)
grupo(237, ["3160008", "3160010", "3161215", "3161415", "3161615", "3160018", "3162015", "3162025", "3162215", "3162225",
            "3162400", "3162403", "3160027", "3160300", "3163000"], "PORCA DUPLA MÉTRICA", [302, 222, 543, 344])
grupo(237, ["3160012", "3160916", "3160058", "3160034", "3160078", "3160118"], "PORCA DUPLA POLEGADA", [54, 415, 245, 494])
grupo(237, ["3470034", "3471794"], "PORCA CASTELO", [476, 515, 552, 584])
grupo(237, ["3618000", "3611000", "3610062", "3610061", "3610060", "3610064", "3610063", "36112175", "3611420", "3611815"],
      "PORCA FLANGE", [409, 624, 553, 690])
grupo(237, ["3610008", "3610012", "3610014", "3611615"], "PORCA FLANGE TRAVANTE", [440, 737, 500, 795])

# 238 - arruelas: só os códigos da arruela pressão são texto; o resto da página está em curvas (transcrito da imagem)
MANUAIS.add(238)
_F_LISA, _F_PRES, _F_ALUM = [50, 153, 214, 264], [77, 437, 189, 564], [43, 634, 228, 776]
_PRES = [("4410006", "ARR.PRESSAO PESADA 06MM"), ("4410008", "ARR.PRESSAO PESADA 08MM 5/16"), ("4410010", "ARR.PRESSAO PESADA 10MM"),
         ("4411212", "ARR.PRESSAO PESADA 12MM."), ("4410014", "ARR.PRESSAO PESADA 14MM"), ("4410016", "ARR.PRESSAO PESADA 16MM"),
         ("44238", "ARR.PRESSAO PS A 3/8"), ("4420716", "ARR.PRESSAO PS B 7/16"), ("442212", "ARR.PRESSAO PS C 1/2"),
         ("442916", "ARR.PRESSAO PS D 9/16"), ("44258", "ARR.PRESSAO PS E 5/8"), ("44234", "ARR.PRESSAO PS F 3/4"),
         ("44278", "ARR.PRESSAO PS G 7/8"), ("4420001", "ARR.PRESSAO PS H 1\"")]
_FUN = [("4111200", "ARR.FUNILEIRO LISA 1/2"), ("4111400", "ARR.FUNILEIRO LISA 1/4"), ("4113800", "ARR.FUNILEIRO LISA 3/8"),
        ("4111118", "ARR.FUNILEIRO LISA 5/16")]
_LISA_POL = [("4111107", "ARR.LISA A ZB"), ("4110018", "ARR.LISA A ZB 1/8"), ("4110532", "ARR.LISA B ZB 5/32"),
             ("4110316", "ARR.LISA C ZB 3/16"), ("4110014", "ARR.LISA D ZB 1/4"), ("4110516", "ARR.LISA F ZB 5/16"),
             ("4110038", "ARR.LISA H ZB 3/8"), ("4110716", "ARR.LISA I ZB 7/16 1,7EXP"), ("4110012", "ARR.LISA J ZB 1/2 3MM EXP"),
             ("4110916", "ARR.LISA L ZB 9/16"), ("4110058", "ARR.LISA M ZB 5/8 3MM EXP"), ("4110034", "ARR.LISA N ZB 3/4"),
             ("4111000", "ARR.LISA P ZB 1\" 3MM EXP"), ("4110112", "ARR.LISA P ZB 1\"1/2"), ("4110114", "ARR.LISA P ZB 1\"1/4")]
_LISA_17 = [("41111417", "ARR.LISA 1\" 1 1/4 33,5MM X 70MM X 1,7 MM ZB"), ("41115217", "ARR.LISA 1\" 27MM X 52MM X 1,7 MM ZB"),
            ("411123017", "ARR.LISA 1/2 13MM X 30MM X 1,7 MM ZB"), ("411344017", "ARR.LISA 3/4 20,5MM X 40MM X 1,7 MM ZB"),
            ("411583317", "ARR.LISA 5/8 17MM X 33,5MM X 1,7 MM ZB"), ("411784617", "ARR.LISA 7/8 23,5MM X 46MM X 1,7 MM ZB"),
            ("41191617", "ARR.LISA 9/16 15MM X 31MM X 1,7 MM ZB")]
_LISA_Z = [("4070003", "ARR LISA Z ZB 03 MM"), ("4070004", "ARR.LISA Z ZB 04 MM"), ("4070005", "ARR.LISA Z ZB 05 MM"),
           ("4070006", "ARR.LISA Z ZB 06 MM"), ("4070008", "ARR.LISA Z ZB 08 MM"), ("4070010", "ARR.LISA Z ZB 10 MM"),
           ("4070012", "ARR.LISA Z ZB 12 MM"), ("4070014", "ARR.LISA Z ZB 14 MM"), ("4070016", "ARR.LISA Z ZB 16MM"),
           ("4071800", "ARR.LISA Z ZB 18MM"), ("4070020", "ARR.LISA Z ZB 20MM"), ("4072400", "ARR.LISA Z ZB 24MM X 43MM ESP 4,00")]
_ALUM = [("4630610", "ARR ALUM 06 X 10"), ("4630812", "ARR ALUM 08 X 12"), ("4631014", "ARR ALUM 10 X 14"),
         ("4631016", "ARR ALUM 10 X 16"), ("4631218", "ARR ALUM 12MM X 18MM"), ("4631170", "ARR ALUM 12X23X1 COM FURO"),
         ("4631320", "ARR ALUM 13 X 20"), ("4630305", "ARR ALUM 14 X 20"), ("4631824", "ARR ALUM 18 X 24"),
         ("4631826", "ARR ALUM 18 X 26 BUJAO DA TORO"), ("4631924", "ARR ALUM 19 X 24"), ("4632026", "ARR ALUM 20 X 26"),
         ("4632126", "ARR ALUM 21,5 X 26"), ("4632230", "ARR ALUM 22 X 30"), ("4632430", "ARR ALUM 24 X 30"),
         ("4632632", "ARR ALUM 26 X 32"), ("4633036", "ARR ALUM 30,2 X 36 FREIO HIDRAULICO"), ("4630546", "SCARR ALUM 08 X 12"),
         ("4631874", "SCARR ALUM 13 X 20"), ("4631420", "SCARR ALUM 14 X 20"), ("4631878", "SCARR ALUM 24 X 30"),
         ("4631620", "VER CODIGO (7711622)")]
_INF238 = "Lista impressa como imagem (sem texto no PDF); transcrita da página"
for _n, (_tit, _itens, _f, _inf) in enumerate([
        ("ARRUELA PRESSÃO PESADA (GRUPO 441)", _PRES[:6], _F_PRES, ""),
        ("ARRUELA PRESSÃO PS (GRUPO 442)", _PRES[6:], _F_PRES, ""),
        ("ARRUELA FUNILEIRO LISA", _FUN, _F_LISA, _INF238),
        ("ARRUELA LISA ZB POLEGADA (GRUPO 411)", _LISA_POL, _F_LISA, _INF238),
        ("ARRUELA LISA ZB 1,7 MM (GRUPO 411)", _LISA_17, _F_LISA, _INF238),
        ("ARRUELA LISA Z ZB MILÍMETRO (GRUPO 407)", _LISA_Z, _F_LISA, _INF238),
        ("ARRUELA DE ALUMÍNIO", _ALUM, _F_ALUM, _INF238)]):
    for _c, _d in _itens:
        ADD.append(dict(pagina=238, card=_n + 1, codigo=_c, descricao=_d, _titulo=_tit, tipo="ARRUELA",
                        info=_inf, foto_spec={"rect": _f}))
AJ["cod:4631620"] = {"info": "Na lista consta 'VER CODIGO (7711622)' | " + _INF238}
NOTAS.append("Pág. 238: as listas de arruela lisa, funileiro e alumínio estão impressas como imagem (sem texto pesquisável) e "
             "foram transcritas da página. O item 4631620 da lista de alumínio só diz 'VER CODIGO (7711622)'.")

# 239 - parafuso de centro
tabela(239)
_F_PFC = [288, 98, 316, 312]
for _cs, _t in [(["790104", "791005", "790106", "791008"], "PF CENTRO CABEÇA BAIXA - 10MM"),
                (["790124", "791205", "790720", "790137", "790725", "791209", "790721", "790719", "791214"], "PF CENTRO CABEÇA BAIXA - 12MM"),
                (["791406", "7914312"], "PF CENTRO CABEÇA BAIXA - 14MM"),
                (["791808", "791810", "791812"], "PF CENTRO CABEÇA BAIXA - 18MM"),
                (["79125", "79126", "791206", "79128", "791208", "791210", "791212"], "PF CENTRO CABEÇA BAIXA POLEGADA - 1/2"),
                (["790382", "79383", "790384", "790385", "790386", "790388", "790175", "790182", "793812"],
                 "PF CENTRO CABEÇA BAIXA POLEGADA - 3/8"),
                (["795163", "795164"], "PF CENTRO CABEÇA BAIXA POLEGADA - 5/16"),
                (["795806", "795808", "795809", "795810", "795812", "795814"], "PF CENTRO CABEÇA BAIXA POLEGADA - 5/8 ACO UNF"),
                (["797164", "797166", "797168"], "PF CENTRO CABEÇA BAIXA POLEGADA - 7/16")]:
    grupo(239, _cs, _t, _F_PFC)
novo(239, "791204", "PF CENTRO CA 12 X 04 12 X 100",
     info="Código impresso como '79.1204' (com ponto); registrado sem o ponto")
grupo(239, ["791204", "790126", "791207", "790128", "790121", "790122"], "PF CENTRO CABEÇA ALTA - 12MM", [290, 334, 309, 428])
grupo(239, ["3170010", "3171215", "3171415", "33516", "33338", "3330716", "33312", "3330916", "3171815"],
      "PORCA PARA PARAFUSO DE CENTRO", [430, 470, 490, 520])
for _c, _d in [("790724", "PF CENTRO CARRETA 9/16 X 06"), ("799166", "PF CENTRO CARRETA 9/16 X 06."),
               ("799167", "PF CENTRO CARRETA 9/16 X 07"), ("799169", "PF CENTRO CARRETA 9/16 X 09"),
               ("7991610", "PF CENTRO CARRETA 9/16 X 10."), ("799162", "PF CENTRO CARRETA 9/16 X 12"),
               ("7991614", "PF CENTRO CARRETA 9/16 X 14.")]:
    fix(239, _c, descricao=_d)
grupo(239, ["790724", "799166", "799167", "799168", "799169", "7991610", "799162", "7991614"], "PF CENTRO CARRETA - 9/16",
      [113, 561, 131, 667])
grupo(239, ["0791407", "0791480"], "PF CENTRO CABEÇA BAIXA FRESADO - 14MM", [393, 700, 563, 722], info="LANÇAMENTO")
fix(239, "5060101", descricao="MB TRAVA PINO MOLA TODOS MBB", info="OBS: USA PORCA 3170209", montadora="Mercedes-Benz")
NOTAS.append("Pág. 239: os códigos 790724 e 799166 têm a mesma descrição (PF CENTRO CARRETA 9/16 X 06); na lista de porcas para "
             "parafuso de centro aparecem 33516 'PORCA UNF A 5/16' e 3330716 'PORCA UNF C 7/16' (na pág. 235 os códigos são "
             "333516 e 333716).")
fix(239, "791204", info="")
fix(239, "5060101", tipo="TRAVA PINO MOLA", foto_spec={"rect": [73, 762, 295, 802]})
NOTAS.append("Pág. 239: o código 791204 (PF CENTRO CA 12 X 04 12 X 100) está impresso como '79.1204'.")

# 240
tabela(240)
grupo(240, ["791240", "791250", "7901206", "7901207", "7901208", "7901210", "7901212"], "PF CENTRO CEA - 12MM", [29, 99, 309, 244])
fix(240, "7901404", foto_spec={"rect": [29, 99, 309, 244]})
grupo(240, ["7916269", "7916300"], "PF CENTRO CDA 16MM ESP 10.9", [45, 283, 250, 422])
NOTAS.append("Pág. 240: a parte de baixo da página tem molduras vazias (sem produtos).")

# ---- fechamento: caixinha de acessório (arruela/porca) cujo código também está numa lista agrupada -> vira só referência
#      de página dessa lista (sem foto própria), para não repetir o produto na planilha
_EM_GRUPO = {}
for _r in ADD:
    if _r.get("_titulo"):
        _EM_GRUPO.setdefault((_r["pagina"], _r["_titulo"]), []).append(_r["codigo"])
_EM_GRUPO = {c for v in _EM_GRUPO.values() if len(v) > 1 for c in v}
for _r in ADD:
    if _r.get("_nao_agrupar") and not _r.get("_titulo") and _r["codigo"] in _EM_GRUPO:
        _r["foto_spec"] = None

# duplicatas e fotos finais
fix(215, "3682215", _nao_agrupar=True, foto_spec=None)
_C219 = {r["codigo"] for r in ADD if r["pagina"] == 219}
_REP220 = [r["codigo"] for r in ADD if r["pagina"] == 220 and r["codigo"] in _C219 and r["codigo"].startswith("632")]
ADD[:] = [r for r in ADD if not (r["pagina"] == 220 and r["codigo"] in _REP220)]
NOTAS.append("Pág. 220: a lista de parafusos 10.9 rosca fina 24MM (" + ", ".join(_REP220) + ") repete a da pág. 219; "
             "registrada uma vez (pág. 219).")
NOTAS.append("Págs. 207/210/215: 75716112, 750814, 751190 e 751232 têm card próprio e também aparecem na lista 'PF TRANSMISSAO' "
             "da pág. 210. Pág. 239: a lista 'porca para parafuso de centro' repete porcas já listadas na pág. 235.")
fix(216, "2741435", foto_spec={"rect": [443, 700, 552, 793]})
fix(216, "2741645", foto_spec={"rect": [443, 700, 552, 793]})
fix(229, "0828250", foto_spec={"rect": [45, 427, 186, 482]})
fix(231, "1290351", foto_spec={"rect": [42, 249, 189, 350]})
NOTAS.append("Pág. 206: o card ao lado dos parafusos Volare é só uma ilustração do ônibus Volare (sem produto).")
