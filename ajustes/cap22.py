# Capítulo 22 - Itens IABV (págs. 290-314)
import json
import os
import re

from capitulos import WORK
from tabela_livre import _spans

TIPOS = [(r"COXIM", "COXIM"), (r"BATENTE", "BATENTE"), (r"HASTE|REP(ARO)? (CENTRAL|PONTAS?|HASTE|BRA[ÇC]O)", "REPARO DE HASTE / BRAÇO"),
         (r"BUCHA", "BUCHA"), (r"BORRACHA", "BORRACHA"), (r"PROTETOR", "PROTETOR"), (r"KIT", "KIT"), (r"ANEL", "ANEL"),
         (r"SUPORTE", "SUPORTE"), (r"PINO", "PINO"), (r"ARRUELA", "ARRUELA"), (r"CASTANHA", "CASTANHA"),
         (r"SEPARADOR", "SEPARADOR"), (r"TIRANTE|TENSOR", "TIRANTE / TENSOR"), (r"MANCAL", "MANCAL"), (r"PORCA", "PORCA"),
         (r"PF|PARAFUSO", "PARAFUSO")]
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(290, 315))
IA = "IABV"

# ---- pág. 290: lista IABV (código + "- nnnn DESCRIÇÃO", em preto)
_IDX = {}
_sp290 = _spans(290)[0]
for _s in _sp290:
    _m = re.match(r"^(\d{7,9})\s*(-.*)?$", _s["t"].strip())
    if not _m:
        continue
    if _m.group(2):
        _IDX[_m.group(1)] = _m.group(2).strip()
        continue
    _viz = sorted([x for x in _sp290 if abs(x["y"] - _s["y"]) < 2 and 0 <= x["x"] - _s["x1"] < 15
                   and x["t"].strip().startswith("-")], key=lambda x: x["x"])
    if _viz:
        _IDX[_m.group(1)] = _viz[0]["t"].strip()

_MONT = [(r"\bMBB?\b|MERCEDES|SPRINTER|ATEGO|ACTROS|AXOR|ACCELO|\bL ?\d{3,4}D?\b", "Mercedes-Benz"),
         (r"\bVW\b|VOLKS|CONSTELLATION|DELIVERY", "Volkswagen"), (r"\bFORD\b|CARGO", "Ford"), (r"SCANIA|\bSC\b", "Scania"),
         (r"VOLVO|\bFH\b|\bFM\b|\bVM\b|\bNH\b", "Volvo"), (r"IVECO|DAILY|STRALIS", "Iveco"), (r"\bDAF\b", "DAF"),
         (r"\bMAN\b", "MAN"), (r"FIAT", "Fiat"), (r"TOYOTA|HILUX", "Toyota"), (r"MITSUBISH|L-?200", "Mitsubishi"),
         (r"KIA|BESTA", "Kia"), (r"AGRALE", "Agrale"), (r"RANDON", "Randon"), (r"NOMA", "Noma"), (r"GUERRA", "Guerra"),
         (r"FACCHINI", "Facchini"), (r"LIBRELATO", "Librelato"), (r"SUSPENSYS", "Suspensys"), (r"KLL", "KLL"),
         (r"VOLARE", "Volare")]
_LAB = re.compile(r"(Subst\.?\s*(?:o\s*)?c[óo]d\.?\s*original\s*:?|Substitui\s*(?:o\s*)?(?:N[ºo°]\.?\s*)?Orig(?:inal)?\.?\s*:?|"
                  r"REF\.?\s*ORIG(?:INAL)?\s*:?|Material\s*:|Dimens[õo]es?\s*:|DIMENS[ÃA]O\s*:|Aplica[çc](?:[ãa]o|[õo]es)\s*:|"
                  r"Compat[ií]vel(?:\s*com\s*o\s*ve[ií]culo)?\s*:?|Produtos\s*relacionados\s*:|Embalagem\s*:|C[ÓO]D\s*:|"
                  r"MESMA\s+TH\s*-?|SUPORTE\s+REI\b)", re.I)


def _linhas(ss, tol=2.4):
    out = []
    for s in sorted(ss, key=lambda s: (s["y"], s["x"])):
        if out and abs(out[-1][0] - s["y"]) < tol:
            out[-1][1].append(s)
        else:
            out.append([s["y"], [s]])
    return [" ".join(x["t"].strip() for x in sorted(l[1], key=lambda s: s["x"])) for l in out]


def _grade(big):
    linhas = []
    for s in sorted(big, key=lambda s: s["y"]):
        if linhas and s["y"] - linhas[-1][-1]["y"] < 15:
            linhas[-1].append(s)
        else:
            linhas.append([s])
    ncol = max(len(l) for l in linhas)
    larg = 545 / ncol
    tops = [min(s["y"] for s in l) - 12 for l in linhas] + [806]
    out = {}
    for i, l in enumerate(linhas):
        for s in l:
            k = min(int(((s["x"] + s["x1"]) / 2 - 25) // larg), ncol - 1)
            out[id(s)] = [25 + k * larg, tops[i], 25 + (k + 1) * larg, tops[i + 1]]
    return out


def cards_iabv(p, grade=None, tam_cod=6):
    """grade: None = molduras do PDF (com fallback), True = grade inferida pelos códigos."""
    raw = json.load(open(os.path.join(WORK, "raw", f"p{p:03d}.json"), encoding="utf-8"))
    sp, imgs = _spans(p)
    big = [s for s in sp if s["red"] and re.fullmatch(r"\d{7,9}", s["t"]) and s["size"] >= tam_cod]
    # códigos secundários (MESMA TH / SUPORTE REI / IABV) não são âncora
    sec = [s for s in sp if re.search(r"MESMA\s*TH|SUPORTE\s*REI|IABV\s*$|^IABV|REF\.?\s*ORIG|REFER[ÊE]NCIA|Subst", s["t"], re.I)]
    big = [s for s in big if not any(abs(x["y"] - s["y"]) < 14 and abs(x["x"] - s["x"]) < 140 and x["y"] <= s["y"] + 7
                                     and re.search(r"SUPORTE\s*REI|MESMA", x["t"], re.I) and x["x"] <= s["x"] + 40
                                     for x in sec)
           and not any(re.search(r"REF|Subst|REFER", x["t"], re.I) and (abs(x["y"] - s["y"]) < 4 and x["x"] < s["x"] and s["x"] - x["x1"] < 30
                                                                       or 0 < s["y"] - x["y"] < 13 and abs(x["x"] - s["x"]) < 12 and s["size"] < 10)
                       for x in sec)]
    cards = [c for c in raw["cards"] if c["id"] != 0]

    def dentro(r, s):
        return r[0] - 1 <= (s["x"] + s["x1"]) / 2 <= r[2] + 1 and r[1] - 1 <= s["y"] + 3 <= r[3] + 1
    rect_de = {}
    if not grade:
        # grade pelas bordas de todas as molduras (as molduras do PDF se sobrepõem)
        def _clus(vs):
            out = []
            for v in sorted(vs):
                if out and v - out[-1][-1] < 6:
                    out[-1].append(v)
                else:
                    out.append([v])
            return [sum(c) / len(c) for c in out]
        xs = _clus([c["rect"][0] for c in cards] + [c["rect"][2] for c in cards])
        ys = _clus([c["rect"][1] for c in cards] + [c["rect"][3] for c in cards])
        for s in big:
            cx, cy = (s["x"] + s["x1"]) / 2, s["y"] + 3
            xa = [x for x in xs if x <= cx]
            xb = [x for x in xs if x > cx]
            ya = [y for y in ys if y <= cy]
            yb = [y for y in ys if y > cy]
            if xa and xb and ya and yb:
                rect_de[id(s)] = [max(xa), max(ya), min(xb), min(yb)]
    g = _grade(big) if big else {}
    regs = []
    for n, s in enumerate(sorted(big, key=lambda s: (round(s["y"] / 20), s["x"]))):
        x0, y0, x1, y1 = rect_de.get(id(s)) or g[id(s)]
        cs = [t for t in sp if t is not s and x0 - 1 <= (t["x"] + t["x1"]) / 2 <= x1 + 1 and y0 - 1 <= t["y"] + t["size"] / 2 <= y1 + 1]
        codigo = s["t"]
        tit_tam = sorted({round(t["size"]) for t in cs if not t["red"] and t["y"] > s["y"] - 4}, reverse=True)
        titulo = [t for t in cs if not t["red"] and t["size"] >= 9.5 and t["y"] >= s["y"] - 30
                  and not _LAB.search(t["t"]) and t["y"] <= s["y"] + 45]
        resto = [t for t in cs if t not in titulo]
        tit = re.sub(r"\s+", " ", " ".join(_linhas(titulo))).strip()
        txt = re.sub(r"\s+", " ", " ".join(_linhas(resto))).strip()
        partes = _LAB.split(txt)
        campos = {"_": [partes[0].strip()]}
        for k in range(1, len(partes) - 1, 2):
            lab = re.sub(r"[^a-z]", "", partes[k].lower())[:5]
            campos.setdefault(lab, []).append(partes[k + 1].strip(" -/:"))
        ref = campos.get("subst", []) + campos.get("refor", []) + campos.get("subst", [])[:0]
        ref = [x for x in dict.fromkeys(ref) if x]
        sim = [f"MESMA TH {x.split()[0]}" for x in campos.get("mesma", []) if x]
        sim += [f"Suporte Rei {x.split()[0]}" for x in campos.get("supor", []) if x]
        sim += [f"Cód. {x.split()[0]}" for x in campos.get("cd", []) if x]
        apl = campos.get("aplic", [])
        info = []
        for lab, nome in (("mater", "Material"), ("dimen", "Dimensões"), ("compa", "Compatível"), ("produ", "Produtos relacionados"),
                          ("embal", "Embalagem")):
            info += [f"{nome}: {x}" for x in campos.get(lab, []) if x]
        info = [x for x in campos["_"] if x] + info
        # sobras após o 1º token de MESMA/SUPORTE REI/CÓD
        for lab in ("mesma", "supor", "cd"):
            for x in campos.get(lab, []):
                sobra = " ".join(x.split()[1:])
                if sobra:
                    info.append(sobra)
        fotos = [b for b in imgs if x0 - 2 <= (b[0] + b[2]) / 2 <= x1 + 2 and y0 - 2 <= (b[1] + b[3]) / 2 <= y1 + 2]
        foto = max(fotos, key=lambda b: (b[2] - b[0]) * (b[3] - b[1])) if fotos else None
        desc = (re.sub(r"^-\s*\d{3,5}(-\d+)?\s+", "", _IDX[codigo]).strip(" .'") if codigo in _IDX
                else re.sub(r"^-\s*\d{3,5}(-\d+)?\s+", "", tit).strip(" .'"))
        regs.append(dict(pagina=p, card=n + 1, codigo=codigo, descricao=desc, marca=IA if codigo.startswith("498") else "",
                         cod_ref=" / ".join(ref), variacoes=" / ".join(dict.fromkeys(sim)), aplicacao=" / ".join(apl),
                         info=" | ".join(x for x in info if x), _nao_agrupar=True, foto_spec={"rect": foto} if foto else None,
                         _texto=tit + " " + txt))
    ADD.extend(regs)
    return regs


for _p in range(291, 315):
    cards_iabv(_p)


def POS_PROC(r):
    if not r.get("montadora"):
        t = (r.get("descricao", "") + " " + r.get("aplicacao", "") + " " + r.get("info", ""))
        r["montadora"] = ", ".join(dict.fromkeys(m for rx, m in _MONT if re.search(rx, t, re.I)))


def F(p, c, **kw):
    regs = [r for r in ADD if r["pagina"] == p and r["codigo"] == c]
    assert regs, f"{c} não está na pág. {p}"
    for r in regs:
        r.update(kw)


def T(p, c, **kw):
    """Substitui o registro inteiro (campos não informados ficam vazios)."""
    base = dict(cod_ref="", variacoes="", aplicacao="", info="", montadora="")
    base.update(kw)
    F(p, c, **base)


SUSP5 = "Volkswagen, Ford, Volvo, Scania, Mercedes-Benz"
# 291
F(291, "5063116", descricao="SUSPENSYS BUCHA TIR RANDON 2000", marca="Suspensys", montadora="Randon, Librelato")
F(291, "5066997", descricao="SUSPENSYS BUCHA TIRANTE C/PINO", marca="Suspensys", montadora=SUSP5)
F(291, "5066998", descricao="SUSPENSYS BUCHA TIRANTE S/PINO", marca="Suspensys", montadora=SUSP5)
F(291, "4983396", montadora=SUSP5, aplicacao="Tirante suspensão",
  info="Material: SAE 1020 e borracha 70 Shore | Dimensões: Ext. 63mm x entre furos 101,5 x furo 20x17mm (furo oblongo) | "
       "Compatível: Suspensys - Truck (Ford/VW/Volvo/Scania/Mercedes Benz)")
F(291, "4983445", montadora=SUSP5)
F(291, "4983116", montadora="Randon")
F(291, "4983132", descricao="BUCHA SUSPENSÃO AR CARR KLL", montadora="KLL",
  info="Material: Tubo SAE 1020 e borracha 70 shore | Dimensões: Ext. 68,2mm x Int. 30,2mm x Comprimento 104mm | "
       "Compatível: Carretas KLL com suspensão a ar | Produtos relacionados: 4145 | Embalagem: 08")
T(291, "4983811", descricao="BUCHA DO ESTABILIZADOR SEM PINO", marca=IA, cod_ref="A 942.326.0050", montadora="Mercedes-Benz",
  aplicacao="Barra estabilizadora do eixo traseiro - Suspensão pneumática",
  info="Dimensões: Ext. 88,50 mm x Comprimento 60 mm | Compatível Actros: 1823L / 1823LS / 1831 / 1831L / 1831LS / 1832L / "
       "1833L / 1833LS / 1835L / 1835LS / 1843L / 1843LS / 1844L / 1846LS / 1848L / 1848LS / 1857LS / 1860L / 1865LS / "
       "1923L / 1929L / 2223L / 2229L / 2432LS / 2436LS / 2443LS / 2455LS / 2528L / 2529L / 2531L / 2531LS / 2532L / "
       "2533L / 2535L / 2535LS / 2536L / 2543L / 2548L / 2553L / 2553LS e ônibus (lista completa no card)")
F(291, "4983592", cod_ref="A 000.326.44.81")

# limpeza geral: o título "- nnnn DESCRIÇÃO" que caiu em informações vira descrição (se faltar) e sai das informações
_TIT = re.compile(r"^-?\s*\d{3,4}(-\d+)?\s+[A-ZÀ-Ú]")
for _r in ADD:
    segs = [x.strip() for x in _r.get("info", "").split(" | ") if x.strip()]
    tit = [x for x in segs if _TIT.match(x)]
    if tit and not _r["descricao"]:
        _r["descricao"] = re.sub(r"^-?\s*\d{3,4}(-\d+)?\s+", "", tit[0]).strip(" .'")
    _r["info"] = " | ".join(x for x in segs if not _TIT.match(x))
    if _r["cod_ref"] in ("**", "*"):
        _r["cod_ref"] = ""
# 292
F(292, "4987002", cod_ref="Bucha A0003230685 / Tubo A0003236950 / Espaçador A0003232253", montadora="Mercedes-Benz")
F(292, "50913004", descricao="BUCHA TH TIRANTE RODOVIARIA SEM ABA TH", marca="Thor", montadora="Guerra, Randon",
  info="Medidas: diâmetro externo 60,50mm | diâmetro interno 36,00mm | comprimento 50,00mm",
  aplicacao="Carretas Guerra/Randon/Iderol/Schiffer/Rodoviária")
F(292, "50913003", descricao="BUCHA TH TIRANTE RODOVIARIA COM ABA TH", marca="Thor", montadora="Guerra, Randon",
  info="Medidas: diâmetro externo maior 68,70mm | externo menor 60,70mm | interno 36,00mm | comprimento 50,00mm",
  aplicacao="Carreta Rodoviária/Randon/Guerra/Hélio/Iderol/Maringá/Miral/Schiffer")
F(292, "4982003", montadora="")
F(292, "4982002", montadora="")
F(292, "4983007", montadora="Randon, Noma")
F(292, "4983011", descricao="BUCHA CONICA COMPATIVEL FNV", montadora="FNV")
F(292, "4983010", descricao="BUCHA CÔNICA COMPATÍVEL FNV / KRONE", montadora="FNV, Krone")
for _c in ("4982293", "4982225", "4983392"):
    F(292, _c, montadora="Randon")


def N(p, c, descricao, rect, **kw):
    ADD.append(dict(dict(pagina=p, card=90 + len(ADD), codigo=c, descricao=descricao, marca=IA if c.startswith("498") else "",
                         cod_ref="", variacoes="", aplicacao="", info="", _nao_agrupar=True, foto_spec={"rect": rect}), **kw))


# 293
F(293, "4983003", montadora="Guerra")
F(293, "50913005", descricao="BUCHA GUERRA TH", marca="Thor", montadora="Guerra")
F(293, "4983197", descricao="BUCHA SCHIFFER C/PINO", montadora="Schiffer")
N(293, "4983527", "BUCHA ARTICULACAO DO EIXO TANDEN", [26, 270, 205, 405], cod_ref="A 000.325.0485 / A 000.325.0985 / A 947.325.0050",
  montadora="Mercedes-Benz")
F(293, "4983784", descricao="BUCHA BRACO EQUALIZADOR", aplicacao="Suspensão Lubfree distanciada com braço equalizador",
  info="Dimensões: 68,3 x 24,5 x 75mm")
F(293, "4983299", cod_ref="212008921 / 3453200181 / 71700086", info="Dimensões: Int. 30,2mm x Ext. 84,7mm x Comprimento 119mm",
  montadora="Randon")
F(293, "4982137", descricao="BUCHA ISOLADORA TRAVESSA DA CARRETA", info="Dimensões: 33 x 25 x 16mm")
F(293, "4982263", descricao="ARRUELA ENCOSTO BUCHA SUSP PNEUMATICA", tipo="ARRUELA")
F(293, "4983002", descricao="BUCHA TIRANTE SUSPENSAO GUERRA IABV", cod_ref="3893207181")
F(293, "4984559", montadora="Randon")
F(293, "4983790", descricao="BUCHA MOLA DIANTEIRA ACCELO 710/715", cod_ref="A9793200644 / A9793200044", montadora="Mercedes-Benz")
F(293, "4983375", descricao="ACTROS BARRA ESTAB 000.323.7585", cod_ref="A000.323.7985 / 000.323.7585", montadora="Mercedes-Benz",
  tipo="BUCHA")


def MP(p, montadora, exceto=()):
    for r in ADD:
        if r["pagina"] == p and r["codigo"] not in exceto:
            r["montadora"] = montadora


def X(p, c):
    ADD[:] = [r for r in ADD if not (r["pagina"] == p and r["codigo"] == c)]


# 294 (Mercedes-Benz)
X(294, "5000496")
T(294, "4982062", descricao="BUCHA BARRA ESTABIL DIANT MB L608D", marca=IA, cod_ref="A 688.323.7085 / A 308.323.7085",
  variacoes="Suporte Rei 5000496 / Cód. 2062", aplicacao="Barra estabilizadora dianteira",
  info="Embalagem: 20 | Material: borracha 70 shore | Dimensões: Int. 30mm x Comprimento 49,5mm | Compatível: caminhões MB "
       "LO608D/LO608D/L608E/LO708D/LO708E/L708E / Ônibus LFU608D", foto_spec={"rect": [396, 135, 545, 233]})
F(294, "4982060", cod_ref="A 667.324.0253 / A 667.324.0053", variacoes="Suporte Rei 5003251 / Cód. 2060")
F(294, "4982061", cod_ref="A 667.324.0353 / A 667.322.0050 / 979.324.0053")
F(294, "4983024", descricao="BUCHA ALGEMA MOLA TRASEIRA", cod_ref="670.320.0444")
MP(294, "Mercedes-Benz")
# 295 (grade irregular: 4 colunas na 1ª linha)
MB = "Mercedes-Benz"
T(295, "4983073", descricao="PU3073 BUCHA BARRA ESTABILIZADORA MB 708", marca=IA, cod_ref="A 688.320.7073", montadora=MB,
  aplicacao="Ponta da barra estabilizadora", foto_spec={"rect": [25, 90, 160, 225]},
  info="Dimensões: Ext. maior 38mm x Ext. menor 30,5mm x Int. 12,2mm x Comp. 32mm | Compatível: caminhões MB 712E/710/914/"
       "914C/915E/712C/1114/709/710/L710/L710D/712/L608D/L608E / Ônibus LO712")
T(295, "4983076", descricao="BUCHA BARRA ESTABILIZADORA ÔNIBUS", marca=IA, variacoes="Cód. 3076", montadora=MB,
  aplicacao="Olhal ponta barra estabilizadora dianteira e traseira", foto_spec={"rect": [160, 90, 300, 225]},
  info="Material: Tubo SAE 1010 e borracha 70 shore | Dimensões: Ext. 54mm x Int. 14,2mm x Comprimento 42mm | Compatível: "
       "ônibus O500M/1725/1726/O364/O365/O362/O355/O370/O371-ST/O371-U/O370-ST/O371-ST/O400RSE/O400RSD/O400RS/O371RSL "
       "(lista completa no card)")
N(295, "4983160", "BUCHA BARRA ESTAB DIANT/TRAS MB", [300, 90, 430, 225], variacoes="Cód. 3160", montadora=MB,
  aplicacao="Mancal da barra estabilizadora diant. / tras",
  info="Material: Tubo SAE 1020 e borracha 70 shore | Compatível: caminhões MB L1218/L1318/L1319 e ônibus (lista no card)")
F(295, "4982130", foto_spec={"rect": [430, 90, 570, 225]}, montadora=MB)
F(295, "4982068", montadora=MB, info="Dimensões: Ext. 68mm x Int. 28mm x Comprimento 51mm | Compatível: Trucks e Carretas Ito")
F(295, "4982142", montadora=MB, info="Dimensões: Altura 84,5mm x Largura aba 59,2mm | Compatível: caminhões L1218/L1318/L1319/"
  "L1418/L1622/L1624/L1620/L1625 / Ônibus OH1318/OH1418/OF1318/OF1320/OF1618/OF1317/OF1115/OF1315/OF1318E")
F(295, "5063081", info="", montadora="")
F(295, "4982044", info="", montadora="")
F(295, "4982070", montadora="Volvo", info="Embalagem: 20 | Material: borracha 70 shore | Dimensões: Ext. 48mm x Int. 25,4mm x "
  "Comprimento 25mm | Compatível: Volvo F6/FS/F7/F10/F12/F16/FL/NL10/NL12, ônibus B57/B58E/B58 (lista completa no card)")
F(295, "4985113", montadora=MB)
F(295, "4984245", descricao="PINO JUMELO SUSP DIANT ATEGO 18X140", montadora=MB)
T(295, "27418142", descricao="18 X 140 PF FLANGE ACO 10.9 JUMELO DT-P/TRAS", montadora=MB, tipo="PARAFUSO",
  aplicacao="Jumelo mola suspensão do eixo dianteiro",
  info="Compatível: caminhão MB 1726S 4X2-36/ Atego 1718 4X2-36/1719 4X2-36/1725 4X2-36/1726 4X2-36/1723 6X2/1729/2425/2428/"
       "2429/2425 6X2/1725A 4X4/1315/1418/1518/ Atron 2423")
MP(296, MB)
# 297 (Mercedes-Benz)
N(297, "4983366", "BATENTE SUSPENSAO MOLA TRASEIRA", [394, 451, 570, 625], cod_ref="A 000.325.0796 / A 000.325.0596 / A 000.325.0184",
  aplicacao="Actros 3340/2631/2648/2655/3331/3360/3355/3331A/3348A/3241/",
  info="Dimensões: Comprimento maior 230mm x Comprimento menor 208mm x Altura 150mm")
F(297, "4983539", variacoes="Suporte Rei 5003437 / MESMA TH 50913068")
F(297, "4983403", descricao="BUCHA EST ACT 51,5MM X 38,5MM X 55,5MM")
F(297, "49804234", descricao="BUCHA PINO MOLA DIANT TRAS MB ATEGO")
MP(297, MB)
X(293, "71700086")
# 298
F(298, "4983816", cod_ref="A9603261781 / A0003265581", montadora=MB)
F(298, "4984682", descricao="KIT CASTANHA COMPATIVEL KLL")
F(298, "5065134", montadora=MB)
F(298, "498332401", info="Dimensões: Rosca M16 x 1,5 e M18 x 1,5 | Material: alumínio e borracha | Produtos relacionados: 3792, 4174, "
  "3793, 2292, 3776", aplicacao="Fixação traseira do motor | Compatível: caminhões MB Actros", montadora=MB)
F(298, "4984691", aplicacao="Accelo 715C/719C", info="Entre furos 110 mm x Espessura da chapa 8 mm x Comprimento 170 mm x Largura 60 mm | "
  "Produtos relacionados: 4692", montadora=MB)
F(298, "4984692", aplicacao="Accelo 715C/719C", info="Entre furos 110 mm x Espessura da chapa 16 mm x Comprimento 170 mm x Largura 60 mm | "
  "Produtos relacionados: 4691", montadora=MB)
F(298, "4983810", variacoes="Referência Suspensys 100000178327", montadora="Suspensys")
for _c in ("4984698", "4984697", "4984699"):
    F(298, _c, montadora="Suspensys")
F(298, "4984698", cod_ref="70000027")
F(298, "4984697", cod_ref="70000026")
F(298, "4984699", cod_ref="")
F(298, "4983471", montadora=MB)
# 299
_r291 = [r for r in ADD if r["pagina"] == 291 and r["codigo"] == "4983811"][0]
for _p in (298, 299):
    F(_p, "4983811", **{k: _r291[k] for k in ("descricao", "cod_ref", "variacoes", "aplicacao", "info", "montadora", "marca")})
_r292 = [r for r in ADD if r["pagina"] == 292 and r["codigo"] == "4987002"][0]
F(299, "4987002", **{k: _r292[k] for k in ("descricao", "cod_ref", "variacoes", "aplicacao", "info", "montadora", "marca")})
F(299, "4987003", cod_ref="Bucha A0003230685 / Tubo A0003236850")
F(299, "4987004", cod_ref="")
F(299, "4987005", cod_ref="Bucha A000463075 / Tubo A0003236850")
F(299, "4987006", cod_ref="Bucha A000463075 / Tubo A0003236950")
F(299, "4987007", cod_ref="A0083230285 / Tubo A0083230150")
MP(299, MB, exceto=("50913018", "50913019"))
F(299, "50913018", descricao="BUCHA TIRANTE TH SUSPENSYS C/PINO", marca="Thor", variacoes="MESMA IABV 4983396", montadora=SUSP5,
  info="LANÇAMENTO | Material: SAE 1020 e borracha 70 shore | Dimensões: Ext. 63mm x entre furos 101,5 x furo 20x17mm (furo oblongo)")
F(299, "50913019", descricao="BUCHA TIRANTE TH SUSPENSYS S/PINO", marca="Thor", variacoes="MESMA IABV 4983445", montadora=SUSP5,
  info="LANÇAMENTO | Material: Tubo SAE 1020 e borracha 70 shore | Dimensões: Comp. 63,0mm x Int. 24,3mm x Ext. 63,5")
# 300 (Mercedes-Benz; reparos ZL Brasil)
MP(300, MB)
ZL = "ZL Brasil"
F(300, "4983427", aplicacao="Barra de torção traseira Actros 2631/2648/2655/3331/3360/3355/3331A/3348A/3241/3248 (lista completa no card)",
  info="Dimensões: Ext. 85mm x Comprimento entre furos 152mm x Furo 21mm | Material: aço forjado e borracha 70 shore")
F(300, "4983589", aplicacao="Axor 2628K/B/2825/2826KB/2831K/B / Actros 2631LK/2658LK/2631B/2648B/3231",
  info="Dimensões: Ext. 85 mm x Entre furos 152 mm x Furo 25 mm")
T(300, "4970361", descricao="REP ZL CENTRAL AXOR 4140 ZL", marca=ZL, montadora=MB, cod_ref="A 000.350.3605 / A 000.350.4905",
  aplicacao="Actros 3331S/3355S/3331AS/3355AS/3331K/3351K/3348K / Axor 3340/4140/2825/2831/2628K/B/2825/2826KB/2831K/B/6X4",
  info="LANÇAMENTO 04/25 | Ext. 107,7mm | Entre furos 152mm | Furo 25mm | Produtos relacionados: 3388 e 3563",
  tipo="REPARO DE HASTE / BRAÇO")
T(300, "4973391", descricao="ZL REP PONTAS HASTE AXOR 4140 ZL", marca=ZL, montadora=MB, cod_ref="010.697 / 010697",
  aplicacao="Actros 3331S / 3355S / 3331AS / 3355AS / 3331K / 3351K", tipo="REPARO DE HASTE / BRAÇO",
  info="Ext. 85mm | Entre furos 130mm | Furo 23 mm | Comp. total 165 mm | Produtos relacionados: 3388 e 3563")
for _p in (300, 302):
    T(_p, "4983196", descricao="PINO ZL TENSOR HASTE CARGO MEDIO ZL", marca=ZL, montadora=MB, cod_ref="A0003302011",
      aplicacao="Caminhões Atego 2425 (1997 – 2015) / ônibus O500 (1997 – 2015)", tipo="PINO",
      info="Ext. 75mm x Pino 43mm | Comprimento pino 170mm | Entre furos 130mm | Furo 19 mm")
# 301 (hastes de reação em V)
TIPOS.insert(0, (r"HASTE|BARRA REA", "HASTE DE REAÇÃO"))
F(301, "4983388", montadora=MB)
T(301, "4973388", descricao="ZL HASTE REAÇÃO \"V\" ACTROS 3331S/3355S", marca=ZL, montadora=MB, cod_ref="01.32.157 / 013.379-00A",
  aplicacao="Actros, Axor 3331S/3355S/3331AS/3355AS", tipo="HASTE DE REAÇÃO")
T(301, "4973588", descricao="ZL HASTE DE REACAO EM \"V\" - AXOR", marca=ZL, montadora=MB, tipo="HASTE DE REAÇÃO",
  aplicacao="Actros 1831L/1848L/1855L/1860L/1832L/1844L", info="Produtos relacionados: 3589, 3590, 5104 e 5102")
F(301, "4983443", montadora="Volvo", tipo="HASTE DE REAÇÃO")
T(301, "49734431", descricao="HASTE ZL EM V VM310 TRAÇADO/FH ZL", marca=ZL, montadora="Volvo", tipo="HASTE DE REAÇÃO",
  cod_ref="20367004 / 20567262 / 20741695 / 20741703", info="Número de conversão / cód. original 20367004 | Ref. original adicional 20741703")
F(301, "49803198", descricao="HASTE REAÇÃO EM \"V\" VOLKSWAGEN 24.220", montadora="Volkswagen, Ford", tipo="HASTE DE REAÇÃO",
  cod_ref="2T0.511.441 / 2RR.512.391-A / 208.005.204-7 / 2U0.511.441")
F(301, "4973198", marca=ZL, montadora="Volkswagen, Ford", tipo="HASTE DE REAÇÃO",
  cod_ref="2T0.511.441 / 2RR.512.391-A / 208.005.204-7 / 2U0.511.441")
T(301, "4973212", descricao="ZL HASTE EM V VOLVO", marca=ZL, montadora="Volvo", cod_ref="21295227", tipo="HASTE DE REAÇÃO",
  aplicacao="Volvo / F10 / FH / FH12 / FL10 / FM10 / FM12 / NH12 Globetrotter",
  info="Código do fabricante: ZL7083 | Código de barras: 7899152923175")
T(301, "49844921", descricao="PARAFUSO DO REPARO CENTRO \"V\" VM M14 X 1,5", marca=IA, montadora="Volvo", tipo="PARAFUSO",
  aplicacao="VM310 traçado/FH16: 470/520 haste de reação - suspensão traseira | Braço V (4983443) / reparo central (4983138)",
  info="Medida: M14 x 1,5 | Produtos relacionados: 3443, 3198")
T(301, "4974051", descricao="BARRA REAÇÃO SCANIA ZL4051 616MM", marca=ZL, montadora="Scania", variacoes="Cód. ref: 1722750",
  aplicacao="Scania P94 / P114 / P124 / R124 / R164 / T124", tipo="HASTE DE REAÇÃO")
# 302
for _p in (300, 302):
    F(_p, "4983196", cod_ref="A0003302011 / TMJ.512.393", montadora="Mercedes-Benz, Volkswagen",
      info="Ext. 75mm x Pino 43mm | Comprimento pino 170mm | Entre furos 130mm | Furo 19 mm | Também apresentado na pág. 302 como "
           "'3196 PINO TENSOR HASTE CARGO MEDIO/PESADO' (IABV, VW Cargo médio/pesado 1995 a 2022)")
NOTAS.append("Págs. 300/302: o código 4983196 aparece como pino tensor ZL (Atego/O500) e como pino tensor IABV (VW Cargo médio/pesado).")
T(302, "4974450", descricao="ZL REP BRAÇO TENSOR SUSP PNEU SC SÉRIE 3", marca=ZL, montadora="Scania", tipo="REPARO DE HASTE / BRAÇO",
  variacoes="MESMA IABV 3074 / Similar 3668501, N6521", cod_ref="Scania 1953249, 550709, 550806 / Volvo 20912536, 22445562, 85104221 / "
  "MAN 81432206244", aplicacao="Suspensão pneumática - traseira",
  info="Ext. 75mm x Pino 41mm | Comp. pino 148mm | Entre furos 115mm | Furo 17mm")
F(302, "4983074", montadora="Scania"); F(302, "4983225", montadora="Scania", tipo="REPARO DE HASTE / BRAÇO")
F(302, "4983499", descricao="VOLVO REPARO BARRO REACAO", montadora="Volvo", tipo="REPARO DE HASTE / BRAÇO")
F(302, "4983565", montadora="Volvo", tipo="REPARO DE HASTE / BRAÇO")
T(302, "4977241", descricao="REP ZL BARRA DE REACAO 95MM VOLVO FH", marca=ZL, montadora="Volvo", cod_ref="20702095",
  tipo="REPARO DE HASTE / BRAÇO", info="Ext. 95 mm | Entre furos 130 mm | Comprimento pino 168 mm | Furo 21 mm",
  aplicacao="FH12/FM9/12/FH400 - 610 séries/FM300 - 500 séries/F10/F12/F16/FH/FH12/FH16/FM/FM9/FM12/12H/FL7/FL10/10H/FL12/12H/"
            "N10/N12/NH12/NL10/NL12/VM")
F(302, "4983449", montadora="Volvo", tipo="REPARO DE HASTE / BRAÇO")
F(302, "4983138", montadora="Volkswagen", tipo="REPARO DE HASTE / BRAÇO")
F(302, "4983139", montadora="Volkswagen", tipo="PINO")
for _p in (302, 307):
    T(_p, "4983684", descricao="REPARO PONTA \"V\" MAN TGX", marca=IA, montadora="MAN", cod_ref="2V5598081G",
      aplicacao="Suspensão traseira | Compatível: MAN TGX 28440/ 29440/ 33440", tipo="REPARO DE HASTE / BRAÇO",
      info="Dimensões: Ext. 85mm x Comp. pino 170mm x Entre furos 130mm x Furo 25mm | Produtos relacionados: 3682 e 3683")
# 303 (Scania)
X(303, "5005057"); X(303, "5005075")
MP(303, "Scania")
F(303, "4983233", aplicacao="Parte dianteira da suspensão a ar 4 pontos | Caminhões Série 4 (1994-2008)/Séries P,G,R,T (2003)/114C 4X2/"
  "6X4/114G 6X2/114L 4X2/6X2/4", info="Ext. 61mm x Int. 16,0mm x Comprimento 80mm | Material: SAE 1020, alumínio e borracha 70 shore")
F(303, "4983108", cod_ref="1353959", aplicacao="Parte dianteira da suspensão do capô | Caminhões Série 4 (1994-2008)/Séries P,G,R,T (2003)",
  info="LANÇAMENTO 04/25 | Dimensões: Ext. 55,2mm x Int. 10,5mm x Comprimento 70mm")
for _p in (303, 304):
    F(_p, "4983365", cod_ref="1892896", variacoes="Suporte Rei R-5057 | 5005057")
F(303, "4983791", variacoes="Suporte Rei R-5075 | 5005075", info="")
F(303, "4983271", info="Usa-se o parafuso 30 X 225 | " + [r for r in ADD if r["codigo"] == "4983271"][0]["info"].replace("USA-SE O PARAFUSO 30 X 225 | ", ""))
F(303, "4982022", descricao="ANEL VEDAÇÃO PINO SUP DIANT SC SERIE 3")
# 304 (Scania; 498207401 Randon)
MP(304, "Scania", exceto=("498207401",))
F(304, "4987000", descricao="KIT PINO MOLA SCANIA DIANTEIRA COM LUBRIFICACAO")
F(304, "4987009", cod_ref="1377562 / 2157762 / 2V5899541 / 1385170 / 1381893 / 2V5.804.889 / 2V5.804.889-A", montadora="Scania, MAN")
F(304, "4982197", cod_ref="1385170 / 1381893 / 2V5.804.889 / 2V5.804.889-A", variacoes="Suporte Rei 5000877 R-877",
  montadora="Scania, MAN", info="Dimensões: Rosca M16 x 1,5 e M18 x 1,5 | Produtos relacionados: 3233",
  aplicacao="Bucha da suspensão dianteira da cabine | Scania 114C 4X2/6X4/114G 6X2/6X4/114L 4X2/6X2/6X4/P114/P124/P94/R114/R124/T114/T124/"
            "Série 4 (1994-2008)/Série P,G,R,T (2003) / MAN TGX 28.440/TGX 29.440/TGX 33.440")
F(304, "4982080", cod_ref="213604", aplicacao="Barra estabilizadora dianteira",
  info="Dimensões: Int. 37mm x Comprimento 118mm | Compatível: caminhão Série 3 4X4/6X4/8X4 (1987-1996) / Série 4 (1994-2008) / "
       "Séries P,G,R,T (2003) / T112/T113/T142/T143/R112/R113/R142/R143 / Ônibus K112/K113/F112/F113/L113 (lista no card)")
F(304, "498207401", descricao="BORRACHA PARA ENGATE AUTOMÁTICO", cod_ref="2440110012", aplicacao="Engate automático", montadora="Randon",
  info="Dimensões: Int. 62mm x Altura 57mm x Largura 116mm x Comprimento maior 163,5mm x Comprimento menor 143,5mm")
F(304, "4982211", info="Dimensão: Altura 95mm x Int. 63mm x Comprimento 104mm")
# 305 (Volvo)
MP(305, "Volvo")
for _p in (305, 311):
    F(_p, "4983250", descricao="BUCHA MOLA DIAT SUSP VOLVO VM PF 20M")
F(305, "4982344", cod_ref="82074379 / 20500859")
T(305, "50913055", descricao="BUCHA MOLA VOLVO FURO 16,2MM", marca="Thor", montadora="Volvo", variacoes="MESMA IABV 49803250",
  cod_ref="20553083", aplicacao="Volvo: VM 240/260 ano 200", tipo="BUCHA",
  info="Material: tubo SAE 1020 e borracha 70 shore A | Dimensões: Ext. maior 61,5mm x Ext. 54,5mm x Int. 16,2mm x Comp. 95mm")
F(305, "50913056", marca="Thor", variacoes="MESMA IABV 4983250", aplicacao="Volvo: VM traçados VW240/260 2004/2005",
  info="Material: tubo SAE 1020 e borracha 70 shore A | Dimensões: Ext. maior 61,5mm x Ext. 54,5mm x Int. 20,2mm x Comp. 95mm")
N(305, "4983070", "BATENTE MOLA PINO VOLVO", [209, 625, 391, 805], variacoes="MESMA TH 50913066", montadora="Volvo",
  cod_ref="1629553 / 3090971 / 1089501 / 20390836", aplicacao="Mola traseira da suspensão",
  info="Dimensões: Comprimentos 200mm x 210mm x Altura 151mm x Larguras 150mm x 135mm | Compatível: Volvo FH16/FH12/FM/VM/NH/NL/F10/"
       "F12/F16/FL (lista completa no card)")
F(305, "49841721", descricao="PINO MOLA TRASEIRA FH/NH", cod_ref="3173819", variacoes="Cód. 4172-A1",
  aplicacao="Mola traseira da suspensão | Compatível: Volvo FH/NH/FM",
  info="Dimensões: Corpo 26mm x Comprimento 207,5mm x Rosca M24 x 3 x Comp. total 224,5mm")
T(305, "27420155", descricao="20 X 155 PF FLANGE ACO 10.9 MA 2,5 CH30", montadora="Volvo", tipo="PARAFUSO", cod_ref="20883938",
  variacoes="4273-01 PINO JUMELO 152MM DIANT/TRAS VOLVO", aplicacao="Jumelo dianteiro e traseiro - traseiras | Volvo FM/FH",
  info="Material: SAE 1045 temperado e revenido | Dimensões: Externo 20mm x Comprimento 152mm x Rosca M20 x 2,5 | Embalagem: 04")
NOTAS.append("Pág. 305: o card do pino jumelo 4273-01 traz o código 27420155 (parafuso flange 20 x 155, também no capítulo "
             "Parafusos e Porcas).")
# 306 (Volvo)
X(306, "21622369")
MP(306, "Volvo")
F(306, "4984247", cod_ref="22221048 / 21226775 / 21622369")
F(306, "4984694", cod_ref="22221048", tipo="JUMELO")
F(306, "4984695", aplicacao="Volvo VM 240/260/ VM traçado", info="Espessura da chapa 9,5 mm (3/8\") x Entre furos 100 mm x Furo 20 mm x "
  "Comprimento 149,50 mm x Largura 59,50mm")
F(306, "4984693", aplicacao="Volvo VM310/240/260/ VM traçado", info="Espessura da chapa 9,5 mm (3/8\") x Entre furos 100 mm x Furo 16,50 mm "
  "x Comprimento 149,50 mm x Largura 59,50 mm")
F(306, "4984690", cod_ref="", info="Comprimento 152,5mm x Largura 50mm x Espessura 25,20mm x Rosca M24x3 x Entre furos 105 mm | "
  "Produto relacionado: 4689")
F(306, "4982292", tipo="COIFA")
F(306, "4983793", tipo="REPARO DE HASTE / BRAÇO")
# 307 (grade 3 x 4)
_G307 = {"4983213": [25, 88, 203, 268], "4983249": [203, 88, 386, 268], "4983202": [386, 88, 570, 268],
         "4983423": [25, 268, 203, 448], "4983575": [203, 268, 386, 448], "4982008": [386, 268, 570, 448]}
for _c, _r in _G307.items():
    F(307, _c, foto_spec={"rect": _r})
F(307, "4983213", cod_ref="1624486", info="Dimensões: Ext. 55,8mm x Int. 26,2mm x Comprimento 112mm | Produtos relacionados: 3491",
  montadora="Volvo")
F(307, "4983249", info="Ext. 51,5mm x Altura 51mm | Material: SAE 1020 e borracha 70 shore",
  aplicacao="Cabine FH12/FM/FH12J/FH16/FH16J", montadora="Volvo")
F(307, "4983202", descricao="BATENTE MOLA DIANTEIRA", montadora="Volvo", tipo="BATENTE",
  aplicacao="FH12/FH16/FM10/FM12/NH12/FH/FM/FMX/VM210/VM230/VM240/VM260/VM270/VM310/VM330/VM3130",
  info="Dimensão: Ext. 96mm x Altura 96mm x Rosca M14 x 2")
F(307, "4983423", montadora="Iveco", cod_ref="93800933", aplicacao="Mola dianteira parte traseira | Iveco Daily (cabine simples, "
  "cabine dupla e furgão - lista completa no card)", info="Material: SAE 1020 e borracha 70 shore | Dimensões: Ext. maior 54mm x "
  "Ext. menor 48,2mm x Int. 14,7 x Comprimento 35,2mm | Embalagem: 20")
F(307, "4983575", montadora="Iveco", cod_ref="500107653", aplicacao="Feixe da mola dianteira | Compatível: Iveco Tector (caminhões 4X2, "
  "6X2, 6X4, cavalo mecânico e Eurocargo - lista completa no card)", info="Material: tubo SAE 1020 e borracha 70 shore | Dimensões: "
  "Ext. 60mm x Int. 20,2mm x Comprimento 84mm | Embalagem: 08")
F(307, "4982008", descricao="BUCHA DO TIRANTE DA SUSPENSAO NOMA", montadora="Noma", aplicacao="Carretas Noma",
  info="Dimensões: 68,5 x 37 x 50mm", tipo="BUCHA")
F(307, "4984636", montadora="MAN, Volkswagen", info="Dimensões: Ext. 64,5mm x Int. 24,4mm x Comprimento total 95mm")
F(307, "4983678", montadora="MAN", cod_ref="2S0.411.346A")
F(307, "4983679", montadora="MAN")
F(307, "4983323", cod_ref="2V5511150 / 81962100554 / 81962100547", montadora="MAN", descricao="BATENTE MOLA MAN (LADO DIREITO)")
F(307, "4983322", descricao="BATENTE MOLA MAN (LADO ESQUERDO)", montadora="MAN", cod_ref="2V5511149 / 81962100555 / 81962100548",
  aplicacao="Molas da suspensão traseira | Compatível: MAN TGX", info="Dimensões: Altura 142 mm x Comprimento 269,5 mm x Largura 147 mm "
  "x Rosca M20x2 | Produtos relacionados: 3323")
# 308 (Facchini / Librelato)
FC = "Facchini"
F(308, "4984507", cod_ref="0368146601", montadora=FC, info="Não acompanha porca (usar 36878272 porca pino excêntrico Facchini 1\" UNC e "
  "3740001 porca TR UNC 1\") | Material: SAE 1020 | Dimensões: corpo de 31,5mm x compr. total 283mm x cabeça 60mm x rosca 1\" 8 FPP | "
  "Compatível: carreta Fachini com suspensão a ar e suspensão KLL | Embalagem: 01")
F(308, "4983244", cod_ref="", montadora=FC, tipo="ARRUELA")
F(308, "49832441", descricao="PU3244 ARR FACCHINI ENCOSTO BUCHA SUSPENSAO", montadora=FC, tipo="ARRUELA")
T(308, "36878272", descricao="PORCA PINO EXCENTRICO FACCHINI 1\" UNC", montadora=FC, tipo="PORCA",
  foto_spec={"rect": [25, 560, 278, 825]})
X(308, "3740001")
NOTAS.append("Pág. 308: a porca TR UNC 1\" 3740001 aparece só como acessório no card do pino excêntrico 4984507 (ela está no capítulo "
             "Parafusos e Porcas); 36878272 também está naquele capítulo (pág. 209).")
F(308, "4983146", descricao="BUCHA DA SUSPENSAO PNEUMATICA FACCHINI", montadora="Facchini, KLL", tipo="BUCHA",
  aplicacao="Carretas Facchini com suspensão a ar e suspensão KLL", info="Dimensões: 152 x 32,5 x 172,4mm",
  foto_spec={"rect": [25, 278, 203, 548]})
F(308, "4983700", descricao="BUCHA SUSPENSAO PNEUMATICA MACIÇA", montadora="Facchini, KLL", tipo="BUCHA",
  aplicacao="Carretas Facchini com suspensão a ar e suspensão KLL", info="Dimensões: 154 x 32,5 x 171mm",
  foto_spec={"rect": [203, 278, 386, 548]})
N(308, "50913059", "PU3244 ARR FACCHINI ENCOSTO BUCHA SUSP TH", [386, 278, 570, 548], marca="Thor", montadora=FC, tipo="ARRUELA",
  aplicacao="Bucha suspensão a ar | Compatível: carreta Facchini com suspensão a ar",
  info="Dimensões: Ext. 179mm x Int. 58mm x Esp. 8,5mm | Produtos relacionados: orig. A 688.320.7073 - Thor 13059 - IABV PU3244")
F(308, "4983216", descricao="BUCHA ISOLADORA TRAVESSA DA CARRETA", montadora="Librelato, Krone", tipo="BUCHA",
  info="Dimensões: 151 x 29 x 171mm")
T(308, "6328250", descricao="28 X 250 ACO 10.9 MA ROSC 1.1/8 CH30 COMPLETO", marca=IA, montadora="Krone, Librelato", tipo="PARAFUSO",
  aplicacao="Carretas Krone/Librelato/Watson & Chalin", info="Dimensões: 248mm x 28mm x 264mm x rosca 1 1/8 x 12 FPP")
NOTAS.append("Pág. 308: o card 4983216 traz o texto '- 2137 BUCHA ISOLADORA TRAVESSA DA CARRETA' (o 2137 é o 4982137 da pág. 293).")
# 309 (VW / Ford / Volvo)
MP(309, "Volkswagen")
F(309, "4983587", montadora="Volvo")
F(309, "4982051", montadora="Ford")
F(309, "4982224", montadora="Volkswagen, Ford")
F(309, "4983020", montadora="Ford", cod_ref="31772", aplicacao="Ford Willys", info="LANÇAMENTO 03/25 | Dimensões: Ext. 29mm x "
  "Int. 14,5mm x Compr. 62mm")
F(309, "4983021", cod_ref="T11.511.181 / T11.411.171A", aplicacao="Volkswagen 11.130/11.140/11.160/12.140/13.130/14.140/14.210",
  info="Dimensões: Ext. maior Ø56,5mm x Ext. 53,0mm x Int. 19,2mm x Compr. 105mm")
F(309, "4982041", montadora="Volkswagen, Ford")
# 310 (VW em cima; DAF embaixo, grade de 4 colunas)
MP(310, "Volkswagen")
F(310, "4983794", cod_ref="23B511213D"); F(310, "4983774", cod_ref="2W0505179 / 2Z0.511.423-A")
F(310, "4983799", montadora="Volkswagen, MAN"); F(310, "4984253", cod_ref="23B511415A")
F(310, "4987008", cod_ref="Bucha 2080007867 / Arruela 2T0511347")
_X4 = [25, 172, 318, 450, 570]
_YA, _YB, _YC = (451, 626), (626, 805), (626, 805)
for _c, _rect, _d, _ref, _apl, _inf in [
        ("4983779", [_X4[0], 451, _X4[1], 626], "COXIM DAF FX TRASEIRO MOTOR", "1806720 / 1378588", "Fixação traseira do motor | "
         "Compatível: caminhões DAF XF 95/105 (até 2020) / DAF CF 75/85 (até 2020)", "Dimensões: Roscas M16 x 2, M12 x 1,75 e 8 x 1,25 | "
         "Produtos relacionados: 3762"),
        ("4983462", [_X4[1], 451, _X4[2], 626], "COXIM DAF CF/XF DIANTEIRO MOTOR", "2307423", "Fixação dianteira do motor | "
         "Compatível: caminhões DAF CF/XF Euro 6", "Dimensões: Rosca M12 | Produtos relacionados: 3761"),
        ("4983772", [_X4[2], 451, _X4[3], 626], "REPARO DAF HASTE EM V", "2141265", "Haste de reação da suspensão traseira | "
         "Compatível: caminhões DAF CF/XF Euro 6", "Dimensões: Ext. 71 mm x Entre furos 152 mm x Furo 23 mm x Comp. 188 mm | "
         "Produtos relacionados: 3822, 3770"),
        ("4983822", [_X4[3], 451, _X4[4], 626], "BUCHA DAF XF REPARO HASTE EM V", "", "Reparo da ponta da haste em \"V\" | "
         "Compatível: caminhões DAF XF 106 480/530 - Euro 6", "Dimensões: Ext. 70 mm x Int. 39,70 x Comp. 59,20 mm | Produtos "
         "relacionados: 3772, 3770 | Card repetido na linha de baixo da página"),
        ("4983770", [_X4[1], 626, _X4[2], 805], "REPARO CENTRAL DA HASTE EM V", "1676776", "Caminhões DAF XF 106 - Euro 6",
         "Dimensões: Ext. 108 mm x Alt. 67,8 mm x Rosca M24x1,5"),
        ("4983750", [_X4[2], 626, _X4[3], 805], "BUCHA MOLA DIANT DAF 105.440/105.460/105.510", "1368283 / 1357764",
         "Compatível com o veículo DAF XF 105.440/105.460/105.510", "Dimensões: Ext. maior 62,8mm x Int. 24,35mm x Compr. 86,3 mm"),
        ("4983761", [_X4[3], 626, _X4[4], 805], "COXIM DAF TRASEIRO MOTOR", "2136893 / 2136889 / 1897781 / 1897780 / 1851471",
         "Fixação traseira do motor | Compatível: caminhões DAF CF Euro 6", "Embalagem: 20 | Material: tubo SAE 1020 e borracha "
         "70 shore | Dimensões: Rosca M16 x 2, entre furos da fixação do motor 66mm x 32,22 mm, entre furos da fixação no chassi "
         "60 mm x 160 mm x 44,5mm")]:
    T(310, _c, descricao=_d, marca=IA, cod_ref=_ref, aplicacao=_apl, info=_inf, montadora="DAF", foto_spec={"rect": _rect},
      tipo="COXIM" if "COXIM" in _d else "BUCHA" if _d.startswith("BUCHA") else "REPARO DE HASTE / BRAÇO")
# 311 (VW / Ford)
MP(311, "Volkswagen", exceto=("4983250",))
F(311, "4983091", montadora="Volkswagen, Ford")
F(311, "4983448", descricao="KIT DE FIXACAO TRASEIRO DA CABINE", montadora="Ford, Volkswagen", cod_ref="TJG.899.369 / TJG.899.397 / "
  "TAM.899.397 / TJG.899.349", aplicacao="Parte traseira da cabine | Veículos Ford: 814/815/1113/1114/1117/1215/1217/1218/1313/1314/"
  "1317/1415/1418/1617/1618/1621/1622/1722/1731/2217/2218/2631/3224/3530/4030/4031 | Veículos Volkswagen: L80/7.100/7.120/8.120/"
  "8.140/8.150/12.140/12.170/13.150/13.170/13.180/14.150/14.170/14.200/14.210/15.170/15.180/16.170/16.200/16.210/16.300 (lista no card)",
  info="Material: tubo SAE 1020 e borracha 70 shore | Dimensões: Corp. pino 151,5mm x Furo coxim 16,2mm")
F(311, "4983071", montadora="Volkswagen, Ford", cod_ref="T2D.411.171")
F(311, "4983122", descricao="COXIM CABINE PARTE DIANT VW", cod_ref="TJG.899.607 / 2R0.899.413-A", aplicacao="Parte dianteira da "
  "articulação cabine | Caminhões VW 16220 (leito)/35300/12140T/14150/14220/16170/16220/24220/35300/16300/12170BT/14170BT/16200/"
  "40300/12180/14180/Worker 24220/24250/Constellation 24250", info="Material: tubo SAE 1020 e borracha 70 shore | Dimensões: "
  "Ext. 75,6mm x Int. 16,2mm x Comprimento 80mm")
F(311, "4983717", descricao="BUCHA MOLA VW 18310/19370", cod_ref="2T0511173", aplicacao="Suspensão da mola pneumática - traseira | "
  "Caminhão VW 18310 / Constellation 19320 / 19370", info="Material: SAE 1020 forjado | Dimensões: Comprimento 104mm x Interno 30,10mm")
F(311, "4984148", descricao="PINO MOLA SUSPENS AO TRAS VW 30MM X 210MM")
T(311, "4983251", descricao="BUCHA MOLA VW", marca=IA, montadora="Volkswagen", cod_ref="2080007867 / 2T0511173", tipo="BUCHA",
  aplicacao="Olhal da mola da suspensão traseira VW 18.310 traçado/Constellation (2006 em diante): 19320E/25320E/19370E/25370E/"
            "26370E/Constellation Euro 5 19330T/25330T/26330T/1936", info="Dimensões: Ext. 69,2mm x Int. 30,2mm x Comprimento total "
  "104mm | Produtos relacionados: 4687, 7008")
F(311, "4983250", montadora="Volkswagen, Volvo")
F(311, "4983001", descricao="BUCHA MOLA SUSP DIANT/TRAS", montadora="Volkswagen, Ford", info="",
  aplicacao="VW 6.90/7.90 / VW 6.90/7.90/7.110/11.130/14.210")
F(311, "4983144", montadora="Ford")
# 312 (VW / Ford)
MP(312, "Volkswagen")
F(312, "4983198", descricao="PU3198 CALCO FEIXE MOLA L80/690", tipo="CALÇO")
F(312, "4983231", montadora="Volkswagen, Ford")
F(312, "4984261", descricao="BASE V DESL. VW CONSTELLATION", tipo="BASE DE HASTE")
F(312, "4984262", descricao="BASE V DES. VW MENOR CONSTELLAT.", tipo="BASE DE HASTE")
F(312, "4982174", descricao="BUCHA AMORTECEDOR", cod_ref="2Z0.516.337-1", aplicacao="Parte superior e inferior do amortecedor traseiro",
  info="Dimensões: Ext. maior 59,5mm x Ext. 57mm x Int. 24,5mm x Comprimento 41mm")
F(312, "4983301", cod_ref="2R2.899.545-B / 2T2.899.545", aplicacao="Suporte da barra basculante da cabine | Compatível com "
  "Constellation / Worker 17250E / 24250E / 13180E / 15180E / 26260 / 31260 17250E", info="Dimensões: Ext. 55mm x Int. 20,5mm x "
  "Comprimento 47mm (medidas do conjunto montado)")
F(312, "4983042", montadora="Ford", aplicacao="Mola da suspensão | Compatível com o veículo Ford Jeep")
F(312, "4983739", montadora="Ford", aplicacao="Mola traseira parte dianteira e parte traseira | Compatível com Ford Cargo 1119 (2013 em "
  "diante)/1519 4X2")
F(312, "4983543", montadora="Volkswagen, Ford")
F(312, "4983782", cod_ref="23B411719C / 23B411719E")
# 313 (Chevrolet / Sprinter / Mitsubishi / Volare / Ford)
for _c, _m in (("4983090", "GM-Chevrolet"), ("4983015", "GM-Chevrolet"), ("4983029", "GM-Chevrolet, Volkswagen"),
               ("4983276", "GM-Chevrolet"), ("4983227", MB), ("4982151", MB), ("4982123", MB), ("4982170", "Mitsubishi"),
               ("4984630", "Mitsubishi"), ("4982135", "Mitsubishi"), ("4982231", "Volare"), ("4982232", "Volare"),
               ("4983112", "Ford"), ("4983113", "Ford"), ("4983175", "Ford"), ("4983176", "Ford")):
    F(313, _c, montadora=_m)
F(313, "4983090", cod_ref="468481")
F(313, "4983015", cod_ref="7317426 / BC8C.5781.A", info="Dimensões: Ext. 29mm x Int. 14,5mm x Comprimento 70mm | Compatível: "
  "Chevrolet C-10/D-10/D-20/F-1000", descricao="BUCHA MOLA TRAS SUSP CHEVROLET C10/D20")
F(313, "4983029", cod_ref="T11.511.181 / T11.411.171A", info="Dimensões: Ext. maior Ø56,5mm x Ext. 53,0mm x Int. 19,2mm x Compr. 105mm",
  aplicacao="Compatível com Volkswagen 11.130/11.140/11.160/12.140/13.130/14.140/14.210")
F(313, "4983276", descricao="BATENTE MOLA DA SUSPENSÃO CHEVROLET", tipo="BATENTE", aplicacao="Mola da suspensão",
  info="Altura 78mm x Furo 10,5mm x Entre furos 132mm x Base 65mm x 159mm | Descrição conforme foto (card só traz código e aplicação)")
F(313, "4983227", descricao="ASSENTO MOLA INF DIANT SPRINTER 308CDI", cod_ref="A 9013221119", tipo="ASSENTO DE MOLA")
N(313, "4983228", "ASSENTO MOLA SUP DIANT SPRINTER 308CDI", [386, 88, 570, 266], cod_ref="A 9013220019", tipo="ASSENTO DE MOLA",
  variacoes="Suporte Rei 5003237", montadora=MB, aplicacao="Parte superior da mola dianteira | Compatível: Sprinter 308CDI/311CDI/"
  "313CDI/316CDI/408CDI/411CDI/413CDI/416CDI/314/414", info="Dimensões: Altura 33mm x Comprimento 94,5mm x Largura maior 61,5mm x "
  "Largura menor 32,5mm")
N(313, "4983042", "BUCHA MOLA SUSP FORD JEEP", [203, 625, 386, 805], montadora="Ford")
F(313, "4982231", cod_ref="6008014018003")
F(313, "4983112", cod_ref="BF8T5781A", info="", aplicacao="Mola traseira parte dianteira da suspensão | Compatível: F-250 S. Duty/"
  "F-250 simples/F-250 C. Dupla/F-250 simples (1999) / F-4000 (1999)")
F(313, "4983175", cod_ref="65A5781BA"); F(313, "4983176", cod_ref="F4TA5781DA")
NOTAS.append("Pág. 313: o card 4984630 (bucha feixe mola L-200) aparece duas vezes na página; 4983042 também está na pág. 312.")
# 314 (Fiat / Toyota / Agrale / Kia)
for _c in ("4983494", "4983425", "4983380", "4983376", "4983379", "4983433"):
    F(314, _c, montadora="Fiat")
F(314, "4983494", descricao="BUCHA DA MOLA FIAT DUCATO", info=" | ".join(x for x in
  [r for r in ADD if r["codigo"] == "4983494"][0]["info"].split(" | ") if x != "Mola Traseira Parte Dianteira"))
F(314, "4983425", descricao="BUCHA SUSPENSAO DO FIAT DUCATO TRAS")
F(314, "4983380", aplicacao="Suspensão traseira", info="LANÇAMENTO 03/25 | Dimensões: Ext. 37mm x Int. 18mm x Comprimento 21mm | "
  "Compatível: Fiat Strada")
F(314, "4983783", montadora="Fiat")
NOTAS.append("Pág. 314: o card 4983783 'BUCHA DA MOLA TRASEIRA SPRINTER' tem logo Fiat (mantida a montadora do logo).")
F(314, "4982100", cod_ref="90.385.18.007 / 9.038.518.046", montadora="Toyota", aplicacao="Hilux",
  info="LANÇAMENTO 03/25 | Ext. maior 35,5mm | Ext. menor 29,5mm | Int. 17,5mm | Comprimento 54,5 mm")
F(314, "4982036", variacoes="Suporte Rei 5000210", info="Dimensões: Ext. 29mm x Int. 15,5mm x Comprimento 18,5mm | Compatível: "
  "Toyota Bandeirante", montadora="Toyota")
F(314, "4983136", cod_ref="9038914004", aplicacao="Toyota: Hillux/L200 Triton", montadora="Toyota, Mitsubishi",
  info="Dimensões: Ext. 40,1mm x Int. 14,5mm x Comprimento 70mm")
F(314, "4982058", montadora="Agrale", cod_ref="6007.014.011.00.0 / T06.411.041")
F(314, "4983169", montadora="Kia", aplicacao="Jumelo traseiro da suspensão | Compatível: Kia Besta",
  info="Embalagem: 01 | Material: SAE 1020 e borracha 70 shore | Dimensões: diversas")
F(314, "4982093", montadora="Kia")
for _r in ADD:
    if _r.get("tipo") == "ARR" or _r["descricao"].startswith("ARR "):
        _r["tipo"] = "ARRUELA"
    if _r.get("tipo") == "REPARO":
        _r["tipo"] = "REPARO DE HASTE / BRAÇO"
    # subtítulos genéricos do card ("BUCHA BARRA ESTABILIZADORA") saem das informações
    _segs = [x for x in _r.get("info", "").split(" | ") if x]
    _r["info"] = " | ".join(x for x in _segs if not (re.fullmatch(r"[A-ZÀ-Ú ./()-]+", x) and not re.search(r"LAN[ÇC]AMENTO|NOVO", x)
                                                     and len(x) < 60))
NOTAS.append("Pág. 290: lista de códigos IABV (usada para a descrição curta dos cards das págs. 291-314). Os campos 'MESMA TH' "
             "(Thor), 'Suporte Rei' e 'Cód.' de cada card estão na coluna de similares.")
for _c in ("4983456", "4983792", "498427301"):
    ADD.append(dict(pagina=290, card=1, codigo=_c, descricao=re.sub(r"^-\s*\d{3,5}(-\d+)?\s+", "", _IDX[_c]).strip(" .'"), marca=IA,
                    cod_ref="", variacoes="", aplicacao="", info="Consta só na lista IABV da pág. 290, sem card com foto",
                    _nao_agrupar=True, foto_spec=None))
NOTAS.append("Pág. 290: 4982072, 4982087, 4982159 e 4982300 da lista IABV estão no capítulo Quinta Roda e Coxim; 4983456, 4983792 e "
             "498427301 só constam na lista (sem card).")
