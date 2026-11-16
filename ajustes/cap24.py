# Capítulo 24 - Lançamentos - Suportes de Mola (págs. 342-347)
# Cards: código (vermelho, fonte grande) + descrição, "Aplicação:", "Código Silc:", "Cod. Original:" / "REF ORIG" / "Nº ORIG"
import json
import os
import re

from capitulos import WORK
from tabela_livre import _spans

TIPOS = [(r"^BRA[CÇ]O", "BRAÇO"), (r"^CAPA", "CAPA"), (r"^ASSENTO", "ASSENTO DO MOLEJO"), (r"MANCAL", "MANCAL"), (r"CAL[CÇ]O", "CALÇO"), (r"GUIA", "GUIA DO GRAMPO"), (r"BALAN[CÇ]A", "BALANÇA"),
         (r"ALGEMA|JUMELO", "ALGEMA / JUMELO"), (r"BRA[CÇ]ADEIRA|ABRA[CÇ]ADEIRA", "ABRAÇADEIRA"), (r"BATENTE", "BATENTE"),
         (r"PINO", "PINO"), (r"TRAVESSA", "TRAVESSA"), (r"CAVALETE", "CAVALETE"), (r"SUPORTE|SUP\b|SUP\.", "SUPORTE")]
AJ = {}
ADD = []
NOTAS = ["Págs. 342-347 (lançamentos): suportes de mola e peças de suspensão; o 'Código Silc' (fabricante) está na coluna de "
         "similares e o código original da montadora em referência."]
MANUAIS = set(range(342, 348))
SILC = "Silc"
_MONT = [(r"\bMBB?\b|MERCEDES|ATEGO|ACCELO|AXOR|ACTROS|\bL ?1[0-9]{3}\b|\bLS? ?\d{4}", "Mercedes-Benz"),
         (r"\bVW\b|VOLKS|CONSTELLATION|DELIVERY|WORKER", "Volkswagen"), (r"\bFORD\b|CARGO|F-?4000|F-?350", "Ford"),
         (r"SCANIA", "Scania"), (r"VOLVO|\bFH\b|\bFM\b|\bVM\b|\bNH\b", "Volvo"), (r"IVECO|DAILY|TECTOR|STRALIS", "Iveco"),
         (r"VOLARE", "Volare"), (r"AGRALE", "Agrale"), (r"\bMAN\b", "MAN"), (r"\bDAF\b", "DAF"), (r"RANDON", "Randon"),
         (r"GUERRA", "Guerra"), (r"FACCHINI", "Facchini"), (r"NOMA", "Noma"), (r"SUSPENSYS", "Suspensys")]
_RO = re.compile(r"(?:C[óo]digo\s*Original\s*:?|Cod\.?\s*Original\s*:?|C[óo]d\.?\s*Original\s*:?|REF\.?\s*ORIG\.?\s*:?|N[ºo°]\s*ORIG\.?\s*:?)", re.I)


def _linhas(ss, tol=2.4):
    out = []
    for s in sorted(ss, key=lambda s: (s["y"], s["x"])):
        if out and abs(out[-1][0] - s["y"]) < tol:
            out[-1][1].append(s)
        else:
            out.append([s["y"], [s]])
    return [" ".join(x["t"].strip() for x in sorted(l[1], key=lambda s: s["x"])) for l in out]


def ler(p):
    raw = json.load(open(os.path.join(WORK, "raw", f"p{p:03d}.json"), encoding="utf-8"))
    sp, imgs = _spans(p)
    regs = []
    for c in raw["cards"]:
        if c["id"] == 0:
            continue
        x0, y0, x1, y1 = c["rect"]
        cs = [s for s in sp if x0 - 1 <= (s["x"] + s["x1"]) / 2 <= x1 + 1 and y0 - 1 <= s["y"] + s["size"] / 2 <= y1 + 1]
        cods = [s for s in cs if s["red"] and re.fullmatch(r"\d{7,9}", s["t"].replace(" ", "")) and s["size"] >= 11]
        if not cods:
            continue
        txt = re.sub(r"\s+", " ", " ".join(_linhas([s for s in cs if s not in cods]))).strip()
        # fatia por rótulos
        partes = re.split(r"(Aplica[çc][ãa]o\s*:|APLI\s*:|C[óo]digo\s*Silc\s*:|" + _RO.pattern + r")", txt, flags=re.I)
        desc, apl, silc, ref = partes[0], [], [], []
        k = 1
        while k < len(partes) - 1:
            lab, val = partes[k].lower(), partes[k + 1].strip(" .")
            if lab.startswith("aplica") or lab.startswith("apli"):
                apl.append(val)
            elif "silc" in lab:
                silc.append(val)
            else:
                ref.append(val)
            k += 2
        for cod in cods:
            fotos = [b for b in imgs if x0 - 2 <= (b[0] + b[2]) / 2 <= x1 + 2 and y0 - 2 <= (b[1] + b[3]) / 2 <= y1 + 2]
            foto = max(fotos, key=lambda b: (b[2] - b[0]) * (b[3] - b[1])) if fotos else None
            regs.append(dict(pagina=p, card=c["id"], codigo=cod["t"].replace(" ", ""), descricao=desc.strip(" .-").upper(),
                             cod_ref=" / ".join(x for x in ref if x), variacoes=" / ".join(f"Silc {x}" for x in silc if x),
                             aplicacao=" / ".join(apl), info="", marca="", _nao_agrupar=True,
                             foto_spec={"rect": foto} if foto else None))
    return regs


for _p in range(342, 348):
    ADD.extend(ler(_p))


def F(p, c, **kw):
    regs = [r for r in ADD if r["pagina"] == p and r["codigo"] == c]
    assert regs, f"{c} não está na pág. {p}"
    for r in regs:
        r.update(kw)


def POS_PROC(r):
    if not r.get("montadora"):
        t = r["descricao"] + " " + r.get("aplicacao", "")
        r["montadora"] = ", ".join(dict.fromkeys(m for rx, m in _MONT if re.search(rx, t, re.I)))
# 342
F(342, "48001232", descricao="MANCAL BARRA ESTAB DIANT ATEGO", info="Título impresso como imagem no card")
F(342, "48001233", descricao="MANCAL CAPA BARRA ESTAB DIANT ATEGO", info="Conta peça 48001132 | Título impresso como imagem no card")
F(342, "48000045", variacoes="", aplicacao="MB Atego", marca="Suspensys")
# 343
F(343, "48012320", descricao="MANCAL BARRA ESTAB DIANT ACCELO", info="Título impresso como imagem no card")
F(343, "48001262", aplicacao="Mercedes Benz Accelo")


def MP(p, montadora, exceto=()):
    for r in ADD:
        if r["pagina"] == p and r["codigo"] not in exceto:
            r["montadora"] = montadora


_PRIM = [(r"^(SUPORTE|SUP\b|SUP\.)", "SUPORTE"), (r"^SAPATA", "SAPATA"), (r"^ALGEMA", "ALGEMA / JUMELO"), (r"^GUIA", "GUIA DO GRAMPO"),
         (r"^CAL[CÇ]O", "CALÇO"), (r"^MANCAL", "MANCAL"), (r"^BRA[CÇ]O", "BRAÇO"), (r"^ASSENTO", "ASSENTO DO MOLEJO"),
         (r"^CAPA", "CAPA"), (r"^PINO", "PINO"), (r"^BALAN", "BALANÇA"), (r"^MB SUPORTE", "SUPORTE")]
_POS_OLD = POS_PROC


def POS_PROC(r):  # noqa: F811
    _POS_OLD(r)
    for rx, t in _PRIM:
        if re.search(rx, r["descricao"]):
            r["tipo"] = t
            break


# 344 (Mercedes-Benz)
MP(344, "Mercedes-Benz")
F(344, "48001035", descricao="SUPORTE DA MOLA TRASEIRA, PARTE TRASEIRA (PINO FINO 30MM)")
F(344, "48001052", descricao="SAPATA GRAMPO MOLA TRAS 1214, 1215, 1218, 131", info="Com furos para sup. do amortecedor")
# 345 (logo Mercedes-Benz em todos os cards)
MP(345, "Mercedes-Benz")
_PRIM.insert(0, (r"^CUNHA", "CUNHA"))
F(345, "48000058", variacoes="Silc SC- (013.000058)")
F(345, "48003023", descricao="CALCO LEVANTAR MOLEJO TRUCKS 40 X 80 X 185MM")
F(345, "48000084", variacoes="Silc SC-013.000084"); F(345, "48003024", cod_ref="")
F(345, "480010008", variacoes="Silc SC-01.008-AS ESPECIAL", cod_ref="S/N")
F(345, "48001007", variacoes="Silc SC-01.007S", info="Furo: 12,8 mm")
F(345, "48001008", variacoes="Silc SC-01.008", info="Furo: 13,5 mm", aplicacao="1113, 1313 (13x78x164 mm)")
F(345, "48000026", descricao="CUNHA MOLA TRAS 12 X 78 X 150 MM", aplicacao="MB 1113, 1313", variacoes="Ref LTK (013.000026)")
F(345, "48001011", variacoes="Silc SC-01.011S"); F(345, "48001017", variacoes="Silc SC-01.017S", aplicacao="Lpo, 1111, 1113 a 2013")
F(345, "48001003", descricao="GUIA GRAMPO MB TRAS 1111 A 2013 (GRAMPO REDONDO)", variacoes="Silc SC-01.003S")
F(345, "48002012", aplicacao="Carreta Krone")
NOTAS.append("Pág. 345: 48002012 (guia grampo mola carreta truck 90MM, aplicação carreta Krone) tem logo Mercedes-Benz.")
# 346 (Ford; suportes Suspensys também VW)
MP(346, "Ford")
F(346, "48003158", variacoes="Silc SC-03.158 / Similares: FU1111LE, 013100006, 675702", cod_ref="70100183", marca="Suspensys",
  montadora="Ford, Volkswagen")
F(346, "48003159", variacoes="Silc SC-03.159 / Similares: FU1111LD, 013100005, 675703", cod_ref="70100185 / 81000307R",
  marca="Suspensys", montadora="Ford, Volkswagen")
for _c, _s in (("48003181", "SC-03.181"), ("48003182", "SC-03.182")):
    F(346, _c, variacoes="Silc " + _s, marca="Suspensys", montadora="Ford, Volkswagen")
F(346, "48004059", cod_ref="F81Z.5700.AA / F81Z5700AA", montadora="Ford, Volkswagen")
_r = [r for r in ADD if r["pagina"] == 346][0]
for _c, _d, _ref, _silc, _apl, _rect in [
        ("48004012", "ASSENTO FEIXE MOLA TRAS FORD CARGO TODOS", "B7HU5789", "SC-04.012", "Ford Cargo todos", [393, 595, 575, 676]),
        ("48004017", "ALGEMA MOLA DIANT FORD CARGO, ÔNIBUS", "B7HU5789", "SC-04.17", "Ford cargo ônibus", [393, 680, 575, 760])]:
    ADD.append(dict(pagina=346, card=90, codigo=_c, descricao=_d, cod_ref=_ref, variacoes="Silc " + _silc, aplicacao=_apl, info="",
                    marca="", montadora="Ford", _nao_agrupar=True, foto_spec={"rect": _rect}))
NOTAS.append("Pág. 346: 48004012 e 48004017 têm o mesmo código original impresso (B7HU5789).")
# 347
F(347, "48004069", montadora="Ford")
F(347, "48003169", montadora="Ford, Volkswagen, Volvo", marca="Suspensys", aplicacao="Ford, Volks, Volvo, a partir de 2008")
F(347, "48006085", info="O código 48006085 aparece em dois cards da página (suporte da mola traseira parte traseira; Silc SC-006.085 "
  "e SC-06.085)", montadora="Volkswagen")
F(347, "48006039", montadora="Volkswagen")
F(347, "48004294", variacoes="Silc SC-0 (incompleto)")
F(347, "48008001", variacoes="Silc SC-08.001 / Códigos similares: 116801, SC-08.001, 6007002251006")
NOTAS.append("Págs. 342-347: a 3ª coluna de algumas páginas traz só logos (Atego, Axor, Accelo, Actros, Ford, VW, Volare, Volvo).")
NOTAS.append("48003158, 48003159 e 48003169 também estão no capítulo Balanças, Suportes e Pinos (pág. 333).")
