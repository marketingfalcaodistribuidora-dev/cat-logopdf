# Capítulo 48 - Bujões de Cárter e Câmbio (págs. 517-523)
# Listas por caixa: cada caixa (seção) = 1 produto com os códigos como itens; código+descrição via tabela_livre.ler_pagina,
# seções dadas à mão (retângulos pelas bordas das molduras); foto = maior imagem da seção.
import re

from tabela_livre import _spans, ler_pagina

TIPOS = []
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(517, 524))
_CACHE = {}


def _itens(p):
    if p not in _CACHE:
        _CACHE[p] = ler_pagina(p)
    return _CACHE[p]


def _dentro(r, x, y):
    return r[0] - 1 <= x <= r[2] + 1 and r[1] - 1 <= y <= r[3] + 1


def S(p, secs, desc=None):
    """secs = [(título, [x0,y0,x1,y1])]; desc = {código: descrição} para corrigir/completar."""
    desc = desc or {}
    sp, imgs = _spans(p)
    # posição de cada item = posição do seu código (spans com o mesmo texto, na ordem)
    pos, usados = {}, set()
    for i in _itens(p):
        cands = [s for s in sp if s["t"].replace(" ", "") == i["codigo"] and id(s) not in usados]
        if cands:
            s = min(cands, key=lambda s: (s["y"], s["x"]))
            usados.add(id(s))
            pos[id(i)] = ((s["x"] + s["x1"]) / 2, s["y"] + 2)
        else:
            pos[id(i)] = (i["_bbox"][0] + 1, i["_bbox"][1] + 1)
    vistos = set()
    for n, (tit, r) in enumerate(secs, 1):
        its = [i for i in _itens(p) if _dentro(r, *pos[id(i)])]
        fotos = [b for b in imgs if _dentro(r, (b[0] + b[2]) / 2, (b[1] + b[3]) / 2) and (b[2] - b[0]) * (b[3] - b[1]) > 400]
        foto = {"rect": [round(v, 1) for v in max(fotos, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))]} if fotos else None
        for i in its:
            k = (i["codigo"], id(i))
            if k in vistos:
                continue
            vistos.add(k)
            d = desc.get(i["codigo"], i["descricao"])
            ADD.append(dict(pagina=p, card=n, codigo=i["codigo"], descricao=re.sub(r"^\+|^-\s*", "", d).strip(), cod_ref="",
                            variacoes="", aplicacao="", info="", marca="", montadora="", _titulo=tit if len(its) > 1 else "",
                            _nao_agrupar=len(its) == 1, foto_spec=foto))
    soltos = [i["codigo"] for i in _itens(p) if not any((i["codigo"], id(i)) == v for v in vistos)]
    assert not soltos, (p, soltos)


def LN(p, area, tol=2.5):
    """{código: texto da mesma linha} para códigos dentro da área (descrição longe do código)."""
    sp, _ = _spans(p)
    x0, y0, x1, y1 = area
    ss = [s for s in sp if x0 <= s["x"] <= x1 and y0 <= s["y"] <= y1]
    out = {}
    for c in ss:
        t = c["t"].replace(" ", "")
        if c["red"] and re.fullmatch(r"\d{6,9}", t):
            lin = sorted([s for s in ss if s is not c and abs(s["y"] - c["y"]) < tol and s["x"] > c["x"] and not s["red"]],
                         key=lambda s: s["x"])
            out[t] = re.sub(r"\s+", " ", " ".join(s["t"] for s in lin)).strip(" -")
    return out


def X(p, cod, d, foto, **kw):
    """Item fora das listas (código solto com foto própria)."""
    r = dict(pagina=p, card=90 + len(ADD), codigo=cod, descricao=d, cod_ref="", variacoes="", aplicacao="", info="", marca="",
             montadora="", _nao_agrupar=True, foto_spec={"rect": foto})
    r.update(kw)
    ADD.append(r)


TIPOS += [(r"^ANEL", "ANEL ORING"), (r"^ARRUELA", "ARRUELA DE ALUMÍNIO"), (r"^PORCA", "PORCA"), (r"^PARAFUSO", "PARAFUSO"), (r"^BUJ", "BUJÃO")]
NOTAS.append("Págs. 517-523 (bujões): textos dos cards impressos como imagem (transcritos); 'ORG.' do card está em referência original. "
             "A pág. 517 é divisória.")


def B(p, cod, desc, org="", mont="", apl="", med=""):
    """Card de bujão: foto = maior imagem sobre o código, cortada acima do código (o texto do card faz parte da imagem)."""
    sp, imgs = _spans(p)
    c = [s for s in sp if s["t"].strip() == cod][0]
    cx, cy = (c["x"] + c["x1"]) / 2, c["y"]
    cand = [b for b in imgs if b[0] - 12 <= cx <= b[2] + 12 and b[1] < cy and cy - b[1] < 190 and (b[2] - b[0]) * (b[3] - b[1]) > 700]
    b = max(cand, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
    X(p, cod, desc, [round(b[0], 1), round(b[1], 1), round(b[2], 1), round(min(b[3], cy - 2), 1)], cod_ref=org, montadora=mont, aplicacao=apl,
      info=("Medida: " + med) if med else "")


_MB, _VW, _FD, _GM = "Mercedes-Benz", "Volkswagen", "Ford", "GM-Chevrolet"
for _p, _lin in [
    (518, [("00250028", "BUJÃO ESCOAMENTO FILTRO OLEO", "3469970130", _MB, "OM-314 / OM-352", "M18X1.5X13"),
           ("00250012", "BUJÃO CÂMBIO/DIFERENCIAL S/ IMÃ", "1869970032", _MB, "MB todos", "M24X1.5X12"),
           ("00250013", "BUJÃO ESCOAMENTO FILTRO OLEO", "3469970130", _MB, "OM-314 / OM-352", "M18X1.5X13"),
           ("00250008", "BUJÃO CARTER C/IMÃ MB MODERNO", "3450100081", _MB, "", "M26X1.5X16 CH 19"),
           ("00250253", "BUJÃO CÂMBIO / DIFERENCIAL C/ IMÃ", "2109970032", _MB,
            "Mercedes G 210-16/G 230-16/G 231/G 240/G 241-16/G 260/280-16/G 281/330-12/GO 110-6/6.1, Sprinter CDI 311/313/316/318, TDS câmbio G 100-12/G 221-9",
            "M26X1.5X14"),
           ("00250108", "BUJÃO ESCOAMENTO FILTRO ÓLEO MOTOR", "469970130", _MB, "MB-180", "M18X1.5X9"),
           ("00250107", "BUJÃO CARTER COMUNITARIO S/IMÃ", "4039970230", _MB, "MB TDS", "M26X1.5X16"),
           ("00250248", "BUJÃO CARTER", "1159970032", _MB, "OM 457/904/906/924/926LA", "M20X1.5X14"),
           ("00250155", "BUJÃO CARTER S/ IMÃ", "1159970032", _MB, "MB todos", "M24X1.5X14 ALLEN 14"),
           ("00260005", "BUJÃO CARTER", "70650008", "GM-Chevrolet, Mercedes-Benz", "D-10/20 Silverado todos c/ motor Perkins/Maxxion", "3/4 X19"),
           ("00250065", "BUJÃO CARTER C/ IMÃ", "A0029972130", _MB, "MB Sprinter", "M18X1.5X14")]),
    (519, [("00210113", "BUJÃO CAVALETE D'AGUA", "T11121589", _VW, "Volks 12.140/150/180/200 TDS MWM", "3/8 -18 NPT"),
           ("00210177", "BUJÃO RESERVATÓRIO AR", "2RD607383", _VW, "Volks TDS", "1/2 NPT"),
           ("00210030", "BUJÃO CARTER", "N141552", _VW, "Passat/Gol/Voyage motor AP", "M14X1.5X9 CHAVE 19"),
           ("00210181", "BUJÃO CARTER C/ ARRUELA FIXA ALLEN 8MM", "", _VW, "Gol/Voyage/Saveiro geração 5", "M14X1.5X18"),
           ("00210223", "BUJÃO CARTER C/ ARRUELA FIXA", "", _VW, "Amarok/Jetta/Golf/Tiguan/Touareg", "M14X1.5X22"),
           ("00210256", "BUJAO CARTER C/ARR FIXA", "", _VW, "Up/Novo Polo/Virtus/Golf 1.4/Tiguan/TSI TDS", "14X1,5X16"),
           ("00210032", "BUJAO CARTER PF ALLEN 06MM", "016271", _VW, "Fusca/Brasília 1200/1300/1500/1600", "M14X1,5X12"),
           ("00210046", "BUJÃO CARTER", "9008401", _VW, "Gol/Parati/Saveiro geração 3", "M14X1.5X15 ALLEN 8MM"),
           ("00210033", "BUJÃO ALLEN CÂMBIO C/IMÃ CHAVE 17", "111301141", _VW, "Volks TDS", "M24X1.5X17"),
           ("00210028", "BUJÃO CARTER", "113115193", _VW, "Fusca/Brasília 1200/1300/1500/1600", "M14X1.5X11 CHAVE 21"),
           ("00210056", "BUJÃO CARTER INFERIOR", "3924147", "Ford, Volkswagen", "Cargo/caminhões VW F250/350/4000 98/... motor Cummins série B 5.9/C 8.3", "M18X1.5X13"),
           ("00210252", "BUJÃO DRENAGEM DIFERENCIAL S/ IMÃ", "2RG525389", "Volkswagen, Ford", "VW todos/Ford Cargo todos L/LK 1620 eixo Rockwell", "M26X1.75X16")]),
    (520, [("00220088", "BUJÃO CARTER ÓLEO MOTOR CUMMINS 3.9", "BG5X.6730.FA", _FD, "Ford 1517/1317/815/2628, Cargo 2005/... 2422/1722/1717 Cummins 3.9 eletrônico, F250 2006/...", "M22X1.5X14"),
           ("00210055", 'BUJÃO CARTER "SUPERIOR"', "2RL103113", "Ford, Volkswagen", "F250/350/4000 98/..., Cargo/caminhões VW motor Cummins série B 5.9/C 8.3", "M22X1.5X14"),
           ("00220040", "BUJÃO SEXT. PONTA DE EIXO M32", "NF991AB", _FD, "F2000/4000 até 98", "M32"),
           ("00220067", "BUJÃO CARTER C/ ANEL 'O' RING", "F6TZ6730BA", _FD, "Ka/Fiesta/Courrier/Focus motor Zetec Rocan", "M14X1.5X22"),
           ("00220014", "BUJÃO CAMBIO C/ IMÃ", "72MU77010A", _FD, "Corcel/Belina/Del Rey/Pampa 69/...", "3/8 BSPT"),
           ("00220041", "BUJÃO SEXT. PONTA DE EIXO M32", "NF991AB", _FD, "F2000/4000 até 98", "M32"),
           ("00220044", "BUJÃO CARTER", "", "MWM, Ford", "MWM / F1000 / F22000", "1/2 BSP"),
           ("00220010", "BUJÃO CARTER", "", _FD, "Corcel II/Belina/Del Rey/Pampa motor CHT", "14X1,5X17"),
           ("00220083", "BUJÃO CARTER C/IMÃ", "", _FD, "Ranger 2005/2011 motor Maxxion eletrônico 3.0", "M14X1.25X16"),
           ("00220089", "BUJÃO CARTER ÓLEO MOTOR DIESEL", "", _FD, "Ranger 3.2 2013/...", "14X1.25X14"),
           ("00220046", "BUJÃO CARTER C/IMÃ", "E6HN6730AA", _FD, "Ford Cargo TDS", "3/4 X 13 NF"),
           ("00220047", "PARAFUSO SEXT. DO PARA-LAMA C/ ARRUELA PRATO", "57041S36B", _FD, "F-2000/F-4000", "5/16X1.1/8")]),
    (521, [("00220068", "ANEL ORING P/BUJÃO CARTER", "", _FD, "Ford Ka / Fiesta / Courrier", ""),
           ("00280001", "BUJÃO CARTER C/ IMÃ", "524416", "Scania", "Scania TDS", "M24X2.0X19 SEXT. 19"),
           ("00290002", "BUJÃO CARTER C/IMÃ", "949175", "Volvo", "Volvo moderno após 84", "M24X1.5X16"),
           ("00240030", "BUJÃO CARTER C/ ANEL 'O' RING", "55224611", "Fiat, Jeep", "Fiat motor E-Torq/Toro/Renegade 1.8 flex", "14X1.5X21"),
           ("00240033", "BUJÃO CARTER", "55196505", "Fiat, Jeep", "Toro/Renegade/Compass motor diesel", "M18X1.5X18 CHAVE 13MM"),
           ("00240021", "BUJÃO CARTER", "16993411", "Fiat", "Ducato", "M22X1.5X10 ALLEN 12"),
           ("002100001", "BUJÃO CARTER", "RE002045", "Renault", "Renault Sandero/Logan/Clio/Symbol/Kangoo/Megane/Scenic/Duster/Trafic motor 1.0 a 1.6 TDS", "M16X1.5X19 CHAVE 8"),
           ("00240037", "BUJÃO CARTER ÓLEO MOTOR EVO (FIAT)", "", "Fiat", "Uno 1.4/Novo Palio 1.4/Grand Siena 1.4/Palio Fire 1.3/Fiorino 1.3", "M16X1,5X14"),
           ("00240003", "BUJÃO CARTER MOTOR FIRE TDS", "14325301", "Fiat", "", "M22X1.5X14 ALLEN 12"),
           ("00230086", "PARAFUSO M12 X 52", "", _GM, "Cruze/11/Onix 12/Prisma/Tracker 13/S-10/12 tras", ""),
           ("00230088", "PORCA MANGA DE EIXO", "7.326.750", _GM, "A/C/D-10/20 85/92, S10", "3/4 20 FIOS")]),
    (522, [("00230030", "BUJÃO CÂMBIO C/ IMÃ", "3449250", _GM, "Monza 82/96 / Corsa 94/... / Kadett 89/98", "M18X1.5X10"),
           ("00230031", "BUJÃO QUADR/INT CÂMBIO", "103868A", _GM, "Opala / Chevette", "1/2 NPTF"),
           ("00230084", "BUJÃO CAMBIO S/ IMÃ", "93209070", _GM, "D-20/D-40", "3/4 NPT"),
           ("00230032", "BUJÃO QUADR/INT CÂMBIO", "7316926", _GM, "Opala / Chevette", "1/2 NPTF/MAGN"),
           ("00230023", "BUJÃO CAMBIO C/IMÃ", "93209069", _GM, "D-20 / D-40", "3/4 NPT"),
           ("00230073", "BUJÃO CARTER C/ ANEL 'O' RING", "", "Chrysler", "Chrysler / Gran Caravan 2.4", "M14X1.5X17"),
           ("00230021", "BUJÃO CARTER", "70650008", "GM-Chevrolet, Ford", "D20/D40/F1000 gas/F4000/F250/Ranger diesel/Silverado/S10 96-00", ""),
           ("00230072", "BUJÃO CARTER C/ ANEL 'O' RING MAGN.", "24100042", _GM, "S-10 / Blazer / Blazer 6 cil", "M12X1.75X25.5"),
           ("00230019", "BUJÃO CARTER", "3456849", _GM, "Chevette/Corsa/Celta/Monza", "M14X1.5X14"),
           ("00220012", "BUJÃO CARTER", "66555", "GM-Chevrolet", "Corcel / Belina 69/77", "18X1.5X15 CHAVE 27"),
           ("00230091", "BUJAO CARTER C/ANEL ORING", "", _GM, "S10 2012... diesel", "M12X1,75X25 CH 16"),
           ("00230017", "BUJÃO CARTER", "3921988", _GM, "Opala/A/C-10/20 85/96/Silverado 97/9", "1/2X7/8")]),
    (523, [("00270052", "BUJÃO CARTER", "", "Toyota", "Corolla 02/... / Hilux até 2004 / Hilux Pitbul 2005/... / Hilux SW4 TDS", "M12X1.25X16"),
           ("00270037", "BUJÃO CARTER", "9034112026", "Toyota", "Corolla 92/97 / Toyota Band.", "M12X1.25X16"),
           ("002110018", "BUJÃO P/ CARTER", "900009PH1000", "Honda, Mitsubishi, Asia", "Honda Civic/City/Accord/Fit, Mitsubishi L200/300/Outlander/Pajero, Topic/Besta motor 1.4 a 2.2 TDS", "M14X1.5X12"),
           ("002110025", "BUJÃO CÂMBIO DIFERENCIAL C/IMÃ", "", "Hyundai, Asia", "Topic/Besta/H100", "M18X1.5X13"),
           ("002130160", "BUJÃO CARTER ESPANADO 15MM", "", "", "", ""),
           ("002130159", "BUJÃO CARTER ESPANADO 13MM", "", "", "", ""),
           ("002120001", "BUJÃO CARTER", "", "Honda", "Honda CG 125", "M12X1.5X14 CHAVE 17"),
           ("002120006", "BUJÃO CARTER", "", "Honda", "Honda CG 150", "12X1.5X16 CHAVE 12")])]:
    for _a in _lin:
        B(_p, *_a)
# 00230032 aparece na pág. 521 (bujão câmbio Monza) e na 522 (bujão quadr/int Opala)
B(521, "00230032", "BUJÃO CÂMBIO C/ IMÃ", "3449250", _GM, "Monza 82/96 / Corsa 94/... / Kadett 89/98", "M18X1.5X10")
for _c, _d in (("7710610", "ARRUELA ALUMINIO 06 X 10"), ("7710812", "ARRUELA ALUMINIO 08 X 12"), ("7711014", "ARRUELA ALUMINIO 10 X 14"),
               ("7711216", "ARRUELA ALUMINIO 12 X 16"), ("7711420", "ARRUELA ALUMINIO 14 X 20"), ("7711622", "ARRUELA ALUMINIO 16 X 22")):
    ADD.append(dict(pagina=523, card=7, codigo=_c, descricao=_d, cod_ref="", variacoes="", aplicacao="", info="", marca="", montadora="",
                    _titulo="ARRUELA DE ALUMINIO", foto_spec={"rect": [30, 663, 205, 797]}))
NOTAS.append("Pág. 521/522: o código 00230032 está impresso em dois produtos diferentes (bujão câmbio c/ imã Monza, ORG 3449250, igual ao 00230030; "
             "e bujão quadr/int câmbio Opala, ORG 7316926). Pág. 522: 00220012 (Corcel/Belina) está com logo Chevrolet. Pág. 518: 00250248 e 00250155 "
             "trazem o mesmo ORG 1159970032.")
for _r in ADD:
    if _r["codigo"] == "002100001":
        _r["foto_spec"] = {"rect": [405, 512, 563, 585]}
