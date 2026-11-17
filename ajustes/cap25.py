# Capítulo 25 - Molas (págs. 348-367)
# Pág. 348 = índice (código + descrição). Demais = tabelas de feixe por modelo: cada linha com código Falcão (vermelho)
# é um produto; colunas (Nº Marchetti / R.Fama / Ref. Mobrasma, Bitola, Medida, Comp., Peso, Características) e o
# cabeçalho do modelo (MODELO, APLICAÇÃO, ANO, Nº ORIGINAL, ARQUEAÇÃO, ESPIGÃO) vão para referência/aplicação/informações.
import re

from tabela_livre import _spans

TIPOS = [(r"FEIXE", "FEIXE DE MOLA"), (r"SOB MEDIDA", "MOLA SOB MEDIDA"), (r"PARAB", "MOLA PARABÓLICA"), (r".", "MOLA (LÂMINA)")]
AJ = {}
ADD = []
NOTAS = ["Págs. 350-367: em cada tabela de feixe só as lâminas com código Falcão (em vermelho) viraram produto; as demais linhas "
         "(referências Marchetti/R.Fama sem código) não têm código interno no catálogo."]
MANUAIS = set(range(348, 368))
_COD = re.compile(r"^4\d{6,9}$|^5\d{6,9}$")
_MONT = [(r"\bMBB?\b|MERCEDES|ATEGO|ACCELO|AXOR|ACTROS|SPRINTER|\bL[SKP]?-? ?1\d{3}|\bLK|\bO-?\d{3}\b|\bOF|\bOH", "Mercedes-Benz"),
         (r"\bVW\b|VOLKS|CONSTELLATION|DELIVERY|WORKER|TITAN", "Volkswagen"), (r"\bFORD\b|CARGO|F-?4000|F-?350|F-?\d{4,5}\b", "Ford"),
         (r"SCANIA|\bSC\b", "Scania"), (r"VOLVO|\bFH\b|\bFM\b|\bVM\b|\bNH\b", "Volvo"), (r"IVECO|DAILY|TECTOR", "Iveco"),
         (r"AGRALE", "Agrale"), (r"\bGM\b|CHEVROLET|S-?10|D-?20", "GM-Chevrolet"), (r"FIAT|DUCATO", "Fiat"),
         (r"HILUX|TOYOTA", "Toyota"), (r"RANDON|\bRD\b", "Randon"), (r"GUERRA", "Guerra"), (r"FACCHINI", "Facchini"),
         (r"NOMA", "Noma"), (r"SUSPENSYS", "Suspensys"), (r"VOLARE", "Volare"), (r"INTERNATIONAL", "International")]


def _ok(s):
    t = s["t"].replace(" ", "")
    return (s["red"] and _COD.match(t)) or bool(re.fullmatch(r"49\d{7}", t))  # alguns códigos estão em verde/preto


# índice da pág. 348
IDX = {}
_sp = _spans(348)[0]
for _s in _sp:
    if _ok(_s):
        _v = sorted([x for x in _sp if abs(x["y"] - _s["y"]) < 2 and 0 <= x["x"] - _s["x1"] < 25 and not x["red"]],
                    key=lambda x: x["x"])
        if _v:
            IDX[_s["t"]] = _v[0]["t"].strip()

_LABELS = [("marchetti", r"MARCHETTI"), ("rfama", r"R\.?\s*FAMA|PRE[ÇC]O"), ("mobrasma", r"MOBRASMA|REF\b"),
           ("carac", r"CARACTER"), ("bitola", r"BITOLA"), ("medida", r"MEDIDA"), ("comp", r"COMP"), ("peso", r"PESO"),
           ("cod", r"C[OÓ]DIGO")]


def _cab(sp, s):
    """Linha de cabeçalho da tabela acima do código (rótulos e posições x)."""
    lab_sp = [x for x in sp if 0 < s["y"] - x["y"] < 260 and s["x"] - 25 <= x["x"] <= s["x"] + 560 and not x["red"]
              and any(re.search(rx, x["t"], re.I) for k, rx in _LABELS[:-1]) and len(x["t"].strip()) < 22]
    if not lab_sp:
        return []
    yh = max(x["y"] for x in lab_sp)
    labs = []
    for x in lab_sp:
        if abs(x["y"] - yh) < 3:
            for k, rx in _LABELS:
                if re.search(rx, x["t"], re.I):
                    labs.append((k, (x["x"] + x["x1"]) / 2))
                    break
    return labs


def _modelo(sp, s):
    ms = [x for x in sp if x["t"].upper().startswith("MODELO") and 0 < s["y"] - x["y"] < 330 and abs(x["x"] - s["x"]) < 120]
    if not ms:
        return {}
    m = max(ms, key=lambda x: x["y"])
    bloco = [x for x in sp if 0 <= x["y"] - m["y"] < 70 and m["x"] - 3 <= x["x"] < m["x"] + 330 and not x["red"] and x["size"] >= 6.8]
    linhas = []
    for x in sorted(bloco, key=lambda x: (round(x["y"]), x["x"])):
        if linhas and abs(linhas[-1][0] - x["y"]) < 2.5:
            linhas[-1][1].append(x["t"].strip())
        else:
            linhas.append([x["y"], [x["t"].strip()]])
    out, ult = {}, None
    for _, ts in linhas:
        t = " ".join(ts)
        mm = re.match(r"^(MODELO|APLICA[ÇC][ÃA]O|ANO|N[ºO°]\s*ORIGINAL|ARQUEA[ÇC][ÃA]O|ESPIG[ÃA]O|BUCHAS)\s*:?\s*(.*)$", t, re.I)
        if mm:
            k = re.sub(r"\s", "", mm.group(1).upper())[:4]
            if k in out:
                break
            out[k] = mm.group(2).strip()
            ult = k
        elif ult == "MODE" and t.startswith("/"):
            out["MODE"] += " " + t
        else:
            ult = None
    return out


def ler(p):
    sp, imgs = _spans(p)
    regs = []
    for s in sorted([x for x in sp if _ok(x)], key=lambda x: (x["y"], x["x"])):
        cod = s["t"].replace(" ", "")
        linha = sorted([x for x in sp if x is not s and abs((x["y"] + x["size"] / 2) - (s["y"] + s["size"] / 2)) < 4
                        and x["x"] > s["x1"] - 1 and x["x"] - s["x1"] < 520], key=lambda x: x["x"])
        # corta na próxima coluna de código (tabelas lado a lado)
        out = []
        for x in linha:
            if _ok(x):
                break
            out.append(x)
        labs = _cab(sp, s)
        col = {}
        for x in out:
            cx = (x["x"] + x["x1"]) / 2
            if labs:
                k = min(labs, key=lambda l: abs(l[1] - cx))[0]
            else:
                k = "carac"
            col.setdefault(k, []).append(x["t"].strip())
        col = {k: " ".join(v) for k, v in col.items()}
        mod = _modelo(sp, s)
        acima = [b for b in imgs if b[3] <= s["y"] + 6 and s["y"] - b[3] < 330 and s["x"] - 30 <= (b[0] + b[2]) / 2 <= s["x"] + 560
                 and (b[2] - b[0]) > 60 and (b[3] - b[1]) > 25]
        foto = max(acima, key=lambda b: b[3]) if acima else None
        regs.append(dict(pagina=p, codigo=cod, col=col, mod=mod, y=s["y"], x=s["x"], foto=foto))
    return regs


LINHAS = []
for _p in range(349, 368):
    LINHAS.extend(ler(_p))


def _desc(r):
    if r["codigo"] in IDX:
        return IDX[r["codigo"]]
    c, m = r["col"], r["mod"]
    car = c.get("carac", "")
    if re.match(r"^MOLA", car, re.I):
        return car.upper()
    partes = ["MOLA"]
    if m.get("MODE"):
        partes.append(m["MODE"])
    if m.get("APLI"):
        partes.append(m["APLI"])
    if car:
        partes.append(car)
    if c.get("medida"):
        partes.append(c["medida"])
    return re.sub(r"\s+", " ", " ".join(partes)).upper()


for _r in LINHAS:
    c, m = _r["col"], _r["mod"]
    refs = [x for x in (c.get("marchetti") and f"Marchetti {c['marchetti']}", c.get("rfama") and f"R.Fama {c['rfama']}",
                        c.get("mobrasma") and f"Mobrasma {c['mobrasma']}") if x]
    info = [f"{k}: {c[kk]}" for k, kk in (("Bitola", "bitola"), ("Medida", "medida"), ("Comprimento", "comp"), ("Peso", "peso"))
            if c.get(kk)]
    if c.get("carac") and not _desc(_r).endswith(c["carac"].upper()):
        info.insert(0, c["carac"])
    for k, nome in (("ARQU", "Arqueação"), ("ESPI", "Espigão"), ("ANO", "Ano"), ("BUCH", "Buchas")):
        if m.get(k):
            info.append(f"{nome}: {m[k]}")
    apl = " / ".join(x for x in (m.get("MODE") and f"Modelo {m['MODE']}", m.get("APLI")) if x)
    ADD.append(dict(pagina=_r["pagina"], card=int(_r["y"]), codigo=_r["codigo"], descricao=_desc(_r),
                    cod_ref=m.get("NºOR", "") or m.get("N°OR", "") or m.get("NOOR", ""),
                    variacoes=" / ".join(refs), aplicacao=apl, info=" | ".join(info), marca="", _nao_agrupar=True,
                    foto_spec={"rect": _r["foto"]} if _r["foto"] else None))
# índice: códigos que só aparecem lá
_TEM = {r["codigo"] for r in ADD}
for _c, _d in IDX.items():
    if _c not in _TEM:
        ADD.append(dict(pagina=348, card=1, codigo=_c, descricao=_d, cod_ref="", variacoes="", aplicacao="", info="",
                        marca="", _nao_agrupar=True, foto_spec=None))


def POS_PROC(r):
    if not r.get("_mont_fix"):
        t = r["descricao"] + " " + r.get("aplicacao", "")
        r["montadora"] = ", ".join(dict.fromkeys(m for rx, m in _MONT if re.search(rx, t, re.I)))


def F(p, c, **kw):
    regs = [r for r in ADD if str(r["pagina"]) == str(p) and r["codigo"] == c]
    assert regs, f"{c} não está na pág. {p}"
    for r in regs:
        r.update(kw)
        if "montadora" in kw:
            r["_mont_fix"] = True


# 349 (feixes completos)
F(349, "491410911", descricao="MOLA F CAR FOR CENTRO EIXO FXE 10LAM MB252FOR", tipo="FEIXE DE MOLA", montadora="Mercedes-Benz",
  cod_ref="695.320.7302", variacoes="Ref. MB252FOR (feixe reforçado MB252FRF)", aplicacao="L 1620 - 1418 / 1214K / LS 1632 / "
  "LK 1218 - 1418 - 1620 - 1623 | Dianteiro 1997/19..", info="Feixe original c/10 folhas | Espigão 12X7 | Peso 71,19 | "
  "Lâminas MB25201 a MB25210 e MB252RF (bitola 70X14) listadas no card", foto_spec={"rect": [150, 85, 575, 180]})
F(349, "491915613", descricao="MOLA F CAR FOR FXE. 11 LÂMINAS ORIG RN867FOR", tipo="FEIXE DE MOLA", montadora="Randon",
  cod_ref="2080.06871 / 78.000.098", variacoes="RA 91560 FOR / Ref. RN776FOR (feixe reforçado RN776FRF)",
  aplicacao="Carreta 13 ton. | Diant./tras. | 3 eixos", info="Feixe original c/11 folhas | Espigão 9/16X7 | Peso 66,00 | "
  "Lâminas RN77601 a RN77611 e RN776RF (bitola 90X10/90X12) listadas no card", foto_spec={"rect": [150, 360, 575, 450]})
F(349, "491917009", descricao="MOLA F CAR FOR CENTRO EIXO FXE 11LAM RD1050FX", tipo="FEIXE DE MOLA", montadora="Randon",
  cod_ref="2080.06574 / 78.000.103", variacoes="Ref. RN885FOR (feixe reforçado RN885FRF)",
  aplicacao="Carreta 2000 / 2008 11 ton. | Central | 3 eixos", info="Feixe original c/11 folhas | Espigão 9/16X6 | Peso 56,72 | "
  "Lâminas RN88501 a RN88511 (bitola 90X10/90X11) listadas no card", foto_spec={"rect": [150, 610, 575, 700]})
# 350 (molas reforçadas universal)
_UNIV = "Volvo, Ford, Volkswagen, Guerra, Facchini, Mercedes-Benz, Scania"
for _c, _d, _ref, _bit, _med, _peso in [
        ("491032901", "MOLA REFORÇADA UNIVERSAL OLHETE ORIGINAL 30 / 30", "Mb32901", "80X14", "860X860", "17,54"),
        ("491032902", "MOLA REFORÇADA UNIVERSAL VIRADA / DESPONTE PARALELO", "MB32902", "80X14", "860X860", "16,90"),
        ("491033001", "MOLA F MB 1A CENTRO TODOS EIXO", "Mb33001", "80X15", "950X950", "20,68"),
        ("491033002", "MOLA F MB 2A CENTRO TODOS EIXO", "MB33002", "80X15", "950X950", "20,21"),
        ("491033003", "MOLA F MB 3A CENTRO TODOS EIXO", "Mb33003", "80X16", "950X950", "19,29"),
        ("491033004", "MOLA F MB 4A CENTRO TODOS EIXO", "Mb33004", "80X16", "780X780", "15,67"),
        ("491033005", "MOLA F MB 2A CENTRO TODOS EIXO 710X710", "Mb33005", "80X16", "710X710", "14,27"),
        ("491084801", "MOLA REFORÇADA UNIVERSAL QUEDA CHANFRADA", "FA84801", "90X13", "560X560", "10,29"),
        ("491007147", "MOLA 1. CARRETA REFORCADA", "Si7147", "90X13", "725 X 565", "10,29")]:
    F(350, _c, descricao=_d, variacoes="Ref. Mobrasma " + _ref, aplicacao="Molas reforçadas universal",
      info=f"Bitola: {_bit} | Medida: {_med} | Peso: {_peso}", montadora=_UNIV, foto_spec={"rect": [25, 85, 570, 560]})
NOTAS.append("Pág. 350: o código 491033005 está descrito como 'MOLA F MB 2A CENTRO TODOS EIXO' (mesma descrição do 491033002), "
             "com bitola 80X16 e medida 710X710.")
# 353 (texto em curvas, transcrito da imagem)
_AXOR = "Axor 2826 / 2831 / 3131 / 3340 / 3341 / 3344 / 4140 / 4144 | Dianteiro (subs. parabólica) 2005/...."
_REF353 = "958.320.0502 / 958.320.1002 / 958.320.0802 / 958.320.1102 / 644.320.0302 / 958.320.0902 / (FRF) 958.320.1902"
for _c, _d, _ref, _med, _peso in [("491445481", "OLHETE ORIGINAL 60 / 60", "MB43801", "900X900", "29,05"),
                                   ("491445482", "VIRADA / DESPONTE PARALELO", "MB43802", "900X900", "25,70"),
                                   ("491445483", "LAMINADA C/ FURO / LAMINADA", "MB43803", "580X580", "14,34"),
                                   ("491445484", "LAMINADA / LAMINADA C/ FURO", "MB43804", "480X480", "11,87")]:
    F(353, _c, descricao=f"MOLA MB AXOR DIANTEIRA {_d} {_med}", cod_ref=_REF353, variacoes="Ref. " + _ref, aplicacao=_AXOR,
      info=f"Bitola: 90X17,5 | Medida: {_med} | Peso: {_peso} | Espigão 9/16 X 6 | Feixe original c/7 folhas (MB438FOR) | "
           "Texto impresso como imagem no card", montadora="Mercedes-Benz", foto_spec={"rect": [25, 85, 200, 160]})
# 367 (Toyota Hilux SRV importados)
for _c, _d, _ref, _med, _peso in [("491073801", "MOLA F HILUX 1A CENTRO TR 700MM X 700MM", "IP73801", "700X700", "6,41"),
                                   ("491073802", "MOLA F HILUX 2A CENTRO TR 700MM X 700MM", "IP73802", "700X700", "5,46"),
                                   ("491073803", "MOLA F HILUX 3A CENTRO TR 580MM X 580MM", "IP73803", "580X580", "4,37"),
                                   ("491073804", "MOLA F HILUX 4A CENTRO TR 480MM X 480MM", "IP73804", "480X480", "6,78")]:
    F(367, _c, descricao=_d, cod_ref="482100K720", variacoes="Ref. " + _ref, marca="Importados", montadora="Toyota",
      aplicacao="Toyota Hilux SRV traseiro 2017/...", info=f"Bitola: {'60X15' if _c.endswith('4') else '60X8'} | Medida: {_med} | "
      f"Peso: {_peso} | Espigão 3/8 X 3 | Feixe original c/5 folhas (IP738FOR) | Texto impresso como imagem no card",
      foto_spec={"rect": [25, 85, 570, 420]})
# 354 (Randon)
F(354, "516915401", cod_ref="2080.04392.7", variacoes="Cód. ref RN86201", montadora="Randon",
  aplicacao="Carreta - todos eixos (parabólica plana) 3 eixos", info="Bitola: 90X11 | Medida: 540X540 | Espigão 9/16X6")
F(354, "516915601", cod_ref="2080.06573 / 78.000.102", variacoes="Cód. ref RN86701", montadora="Randon",
  aplicacao="Carreta 2000 / 2008 11 ton. - diant. / tras. - 3 eixos", info="Bitola: 90X10 | Medida: 725X565 | Peso: 9,11 | Espigão 9/16X6")
# 355-356
F(355, "491916901", info="Quadrada / chanfrada rebaixada | MESMA 491915601 | Bitola: 90X10 | Medida: 725X565 | Comprimento: 1290 | "
  "Arqueação: 120 S/P | Espigão: 9/16\" X 5.1/2\" CB | Ano: 1999/...")
F(356, "491445451", foto_spec={"rect": [330, 410, 570, 447]})
for r in ADD:
    if r["pagina"] == 356 and r["codigo"].startswith(("4910000", "49180", "49170")):
        r["aplicacao"] = "Carretas diversas - dianteiro/traseiro (molas sob medida)"
        r["info"] = "Ano: 1998/..."
        r["tipo"] = "MOLA SOB MEDIDA"
        r["foto_spec"] = {"rect": [210, 690, 570, 730]}
F(356, "491801216", descricao="MOLA F BARRA LISA CARRETA 80 X 12 X 1600", variacoes="R.Fama SI 222160")
NOTAS.append("Págs. 355-356: 491915601 aparece como lâmina SR-553.1 (Randon 11 ton.) e como SR-566.3 'MESMA 491915601' na tabela "
             "Randon/Suspensys 13 ton.")
# 357-358
F(358, "491640702", foto_spec={"rect": [316, 98, 572, 135]}, montadora="Volkswagen, Ford")
F(358, "491910401", montadora="Volkswagen, Ford")
F(358, "49144906", info="Código impresso com 8 dígitos | " + [r for r in ADD if r["codigo"] == "49144906"][0]["info"])
NOTAS.append("Pág. 358: o código 49144906 (lâmina FO-792.6 do Cargo 712/814/815/816) está impresso com 8 dígitos.")
# 359
for _c, _m, _mob, _fam, _med, _comp, _car in [("49144101", "FO-787", "VW44102", "VW 63070 02", "950X950", "1900", "QUADRADAS"),
                                              ("49144102", "FO-787.2", "VW44103", "VW 63070 03", "890X890", "1780", "VIRADAS P/BAIXO")]:
    F(359, _c, descricao=f"MOLA VW/FORD CARGO 1215 TRASEIRA {_car} {_med}", variacoes=f"Marchetti {_m} / Mobrasma {_mob} / Fama {_fam}",
      aplicacao="Cargo 1215 - serve VW 12140H / 12140T / 12170BT / 12180 / 13150 / 13170 / 13180 | Traseiro",
      info=f"Bitola: 3X9/16 | Medida: {_med} | Comprimento: {_comp} | Arqueação: 195 S/P | Espigão: 1/2\" X 6\" CB | Ano: 1995/... | "
           "Código impresso com 8 dígitos", montadora="Volkswagen, Ford")
for _c in ("491933901", "491933902", "491933903"):
    F(359, _c, montadora="Volkswagen, Ford")
NOTAS.append("Págs. 359/361: os códigos 49144101, 49144102 e 49143702 estão impressos com 8 dígitos.")
# 360
F(360, "491080011", montadora="Volkswagen, Mercedes-Benz")
# 361
for r in ADD:
    if r["pagina"] == 361:
        r["_mont_fix"] = True
        r["montadora"] = "Volkswagen" if r["codigo"] in ("49143702", "491944502") else "Agrale, Volare"
# 362
F(362, "491078631", montadora="Volkswagen", tipo="MOLA PARABÓLICA")
for _c in ("491080012", "491080013", "491080051", "491080057"):
    F(362, _c, tipo="MOLA PARABÓLICA")
for _c, _ref, _bit, _med, _peso in [("491645501", "VW34701", "90X15", "800X800", "16,96"), ("491645502", "VW34702", "90X15", "800X800", "16,96"),
                                    ("491645503", "VW34703", "90X17,5", "650X650", "16,07"),
                                    ("491645504", "VW34704", "90X17,5", "610X610", "15,08")]:
    F(362, _c, descricao=f"MOLA VW 22.220/24.220 TRASEIRA QUADRADA {_med}", cod_ref="2080.05254", variacoes="Ref. Mobrasma " + _ref,
      aplicacao="VW 22.220 / 22.250 (6 X 4) - 24.220 / 24250 | Traseiro 1995/...",
      info=f"Quadrada | Bitola: {_bit} | Medida: {_med} | Peso: {_peso} | Espigão 1/2X10 | Feixe original c/13 folhas (VW347FOR)",
      montadora="Volkswagen", foto_spec={"rect": [20, 600, 330, 640]})
NOTAS.append("Pág. 362: os códigos 49100901, 49100902 e 49100903 (S-10) estão impressos com 8 dígitos; 491078631 e os códigos da "
             "Titan estão em verde (não vermelho).")
# 363-364 (Mercedes-Benz)
for r in ADD:
    if r["pagina"] in (363, 364):
        r["_mont_fix"] = True
        r["montadora"] = "Mercedes-Benz"
        for k in ("descricao", "aplicacao"):
            r[k] = r[k].replace("A TEGO", "ATEGO").replace("A CCELO", "ACCELO")
for _c in ("491406001", "491406002"):
    F(364, _c, aplicacao="Modelo ACCELO 715 | 7 ton. | Dianteiro",
      descricao=[r for r in ADD if r["codigo"] == _c][0]["descricao"].replace(" MB-2437.9 80X18 340X340", ""))
# 364: blocos com o cabeçalho do modelo fora do alinhamento padrão (lidos da imagem)
_ATG = dict(cod_ref="9583200302", aplicacao="Atego 1718 / 1725 | Caminhão de bebidas e lixo | Traseiro 2005/...")
F(364, "491059321", variacoes="Marchetti MBP-2437.1 / R.Fama MB 05932 01 / Mobrasma MB-9.205.01",
  info="Olhetes engordados 60mm | Bitola: 80X20(12) | Medida: 597X597 | Comprimento: 1194 | Arqueação: 92 S/P | Buchas: 3303", **_ATG)
F(364, "491059322", variacoes="Marchetti MB-2437.2 / R.Fama MB 05932 02 / Mobrasma MB-9.205.01",
  info="Virada / rec. paralelo | Bitola: 80X12 | Medida: 600X615 | Comprimento: 1215 | Arqueação: 92 S/P | Buchas: 3303", **_ATG)
_A715 = dict(cod_ref="9793200002", aplicacao="Accelo 715 | 7 ton. | Dianteiro 2003/...")
F(364, "491406001", variacoes="Marchetti MBP-2416.1 / R.Fama MB 05876 01 / Mobrasma MB-9.492.01",
  info="Olhetes 54mm | Bitola: 70X18,5 | Medida: 798X798 | Comprimento: 1596 | Arqueação: 127 S/P | Buchas: 3591", **_A715)
F(364, "491406002", variacoes="Marchetti MBP-2416.2 / R.Fama MB 05876 02 / Mobrasma MB-9.492.02",
  info="Virada / rec. angular c/furo p/brac. / + anti-ruído | Bitola: 70X18,5 | Medida: 798X808 | Comprimento: 1606 | "
       "Arqueação: 127 S/P | Buchas: 3591", **_A715)
for _c in ("491058780", "491058782"):
    F(364, _c, cod_ref="9793200102", aplicacao="Accelo 815 - ano 2011/... | 915 - ano 2003/2008 | Dianteiro",
      variacoes=[r for r in ADD if r["codigo"] == _c][0]["variacoes"].replace(" / / ", " / "))
_A915 = "Accelo 915 - ano 2008/... | Accelo 1016 - ano 2012/... | Euro 5 | Micro-ônibus LO-815 | LO-916 | Dianteiro"
for _c in ("491058821", "491058822"):
    F(364, _c, cod_ref="9793200202", aplicacao=_A915)
for _p in (363, 364):
    F(_p, "491058823", cod_ref="9793200202", aplicacao=_A915, variacoes="Marchetti MBP-2434.3 / R.Fama MB 05882 03",
      info="Chanfradas c/furo p/brac. / + anti-ruído | Bitola: 70X18 | Medida: 810X810 | Comprimento: 1620 | Arqueação: 120 S/P | "
           "Espigão: 3/8\" X 3\" CB | Buchas: 3591")
# 365 (Volvo)
_FM12 = dict(cod_ref="257904", aplicacao="FM-12 | FH-12 (400/420) | NH-12 (6X4) | Dianteiro 2006/...", montadora="Volvo",
             tipo="MOLA PARABÓLICA", foto_spec={"rect": [300, 375, 575, 415]})
F(365, "491083851", descricao="MOLA VOLVO FM12/FH12/NH12 DIANT PARABOLICA OLHETES 51MM C/CANALETA 990X900",
  variacoes="Marchetti VLP-2927.1 / Ref. Fama VL 0835 01",
  info="Olhetes 51mm c/canaleta | Bitola: 100X30 | Medida: 990X900 | Comprimento: 1890 | Arqueação: 140 S/P | Espigão: 1/2\" X 4\" CB | "
       "Buchas: 3253 | Código impresso em verde", **_FM12)
F(365, "491083852", descricao="MOLA VOLVO FM12/FH12/NH12 DIANT PARABOLICA VIRADA / REC. PARALELO 990X930",
  variacoes="Marchetti VLP-2927.2 / Ref. Mobrasma VL-9.410.02",
  info="Virada / rec. paralelo / c/can. e vinco + anti-ruído | Bitola: 100X30 | Medida: 990X930 | Comprimento: 1920 | "
       "Arqueação: 140 S/P | Espigão: 1/2\" X 4\" CB | Buchas: 3253", **_FM12)
for r in ADD:
    if r["pagina"] == 365:
        r["variacoes"] = r["variacoes"].replace("Mobrasma VL", "Ref. Fama VL").replace("Mobrasma Vl", "Ref. Fama Vl")
NOTAS.append("Pág. 365: a metade de cima da página está vazia.")
# 366 (Fiat)
for r in ADD:
    if r["pagina"] == 366:
        r["_mont_fix"] = True
        r["montadora"] = "Fiat, Peugeot, Citroën" if r["codigo"] == "491920901" else "Fiat"
F(366, "4910181", tipo="FEIXE DE MOLA", info="Feixe original c/3 folhas | Arqueação: 165 S/P | Ano: 1984/... | Código impresso com 7 dígitos")
F(366, "49118101", info="Laminadas | Bitola: 75X6 | Comprimento: 700 | Arqueação: 165 S/P | Ano: 1984/... | Código impresso com 8 dígitos")
NOTAS.append("Pág. 366: 4910181 (feixe Uno/Prêmio, 7 dígitos), 49118101 (8 dígitos) e 4919110 (7 dígitos, lâmina Strada FIP-2101.2A) "
             "estão impressos com menos dígitos que o padrão.")
# págs. de cabeçalho "PARABÓLICA"
for r in ADD:
    if r["pagina"] in (360, 362, 363, 364, 365) and r.get("tipo", "") in ("", "MOLA (LÂMINA)") and not r["codigo"].startswith("4916455"):
        r["tipo"] = "MOLA PARABÓLICA"
F(356, "491445453", foto_spec={"rect": [330, 410, 570, 447]})
NOTAS.append("Tipo: lâminas das páginas com cabeçalho 'PARABÓLICA' (360, 362-365) estão como MOLA PARABÓLICA; as demais como "
             "MOLA (LÂMINA) (convencional).")
# fotos corrigidas (recortes da ilustração da mola, sem logo/tabela)
for _p, _cs, _rect in [(349, ["491410911"], [149, 117, 318, 177]), (349, ["491915613"], [157, 338, 398, 403]),
                       (349, ["491917009"], [125, 564, 366, 644]), (351, ["491660301"], [318, 306, 567, 334]),
                       (353, ["491445481", "491445482", "491445483", "491445484"], [20, 152, 181, 190])]:
    for _c in _cs:
        F(_p, _c, foto_spec={"rect": _rect})
for r in ADD:
    if r["pagina"] == 350:
        r["foto_spec"] = {"rect": [149, 198, 567, 294]}
    if r["pagina"] == 356 and r.get("tipo") == "MOLA SOB MEDIDA":
        r["foto_spec"] = {"rect": [225, 588, 559, 628]}
