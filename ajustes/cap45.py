# Capítulo 45 - Abraçadeiras (págs. 498-506)
# Listas por caixa: cada caixa (seção) = 1 produto com os códigos como itens; código+descrição via tabela_livre.ler_pagina,
# seções dadas à mão (retângulos pelas bordas das molduras); foto = maior imagem da seção.
import re

from tabela_livre import _spans, ler_pagina

TIPOS = [(r"NYLON|PLASTICA", "ABRAÇADEIRA NYLON"), (r"INJE", "ABRAÇADEIRA INJEÇÃO"), (r"TURB|INTERC", "ABRAÇADEIRA TURBINA"),
         (r"MANGOTE", "ABRAÇADEIRA MANGOTE"), (r"ESCAP", "ABRAÇADEIRA ESCAPAMENTO"), (r"CARDAN|CRUZ", "ABRAÇADEIRA CARDAN"),
         (r"ABRA", "ABRAÇADEIRA")]
AJ = {}
ADD = []
NOTAS = ["Págs. 498-506 (abraçadeiras): cada caixa da página virou 1 produto com os códigos da lista como itens."]
MANUAIS = set(range(498, 507))
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


# 498 (pág. impressa 497)
S(498, [("ABRAÇADEIRA PLASTICA NYLON", [25, 87, 570, 414]), ("ABRAÇ. NY PTA ESP LIN VW FHC", [25, 414, 570, 496]),
        ("ABR NYLON PLASTICA 4,6 X 110 PRET TIP T", [25, 496, 570, 646]), ("ABRAÇADEIRA PLASTICA NYLON BRANCA", [25, 646, 570, 805])],
  {"8882143": "ABRAÇ. NY PTA ESP LIN VW FHC", "88846110": "ABR NYLON PLASTICA 4,6 X 110 PRET TIP T P/ACABAMENTO"})
for _r in ADD:
    if _r["pagina"] == 498 and _r["codigo"] == "8882143":
        _r["montadora"] = "Volkswagen, Ford"
    if _r["pagina"] == 498 and _r["codigo"] == "88846110":
        _r["info"] = "Cabeça em T | Trava com eficácia | Acabamento antideslizante"
    if _r["pagina"] == 498 and _r["codigo"] == "88876750":
        _r["descricao"] = "ABR NYLON PLASTICA 7,8 X 230 / 7,6 X 750 PRETA"
NOTAS.append("Pág. 498: 88876750 está impresso duas vezes (7,8 x 230 preta e 7,6 x 750 preta); lançado uma vez com as duas medidas.")
# 499 (pág. impressa 498): códigos impressos em preto junto da descrição
for _c, _d in [("5390812", "ABRAC 09MM 08 X 12 C/APERTO"), ("5391220", "ABRAC 09MM 12 X 20 C/APERTO"),
               ("53914222", "ABRAC 09MM 14 X 22 C/APERTO"), ("53919277", "ABRAC 09MM 19 X 27 C/APERTO")]:
    ADD.append(dict(pagina=499, card=1, codigo=_c, descricao=_d, cod_ref="", variacoes="", aplicacao="", info="", marca="",
                    montadora="", _titulo="ABRAC 09MM C/APERTO", foto_spec={"rect": [91, 235, 514, 676]}))
NOTAS.append("Pág. 499: códigos impressos em preto (não vermelho); 53914222 e 53919277 têm 8 dígitos.")
# 500 (pág. impressa 499)
S(500, [("ABRACADEIRA FITA 9MM", [25, 87, 570, 680]), ("ABRACADEIRA INJEÇÃO", [25, 680, 570, 805])])
NOTAS.append("Pág. 500: há medidas repetidas com códigos diferentes (44x57: 5390982/5394457; 51x64: 5390174/5395164; 57x70: "
             "5390983/5395770; 57x76: 5390984/5395776; 102x121: 5391585/539102121) e 07x08 p/gasolina em 5390708/5391653; "
             "539102121 e 539114133 têm 9 dígitos, 53983102 tem 8.")
# 501 (pág. impressa 500): abraçadeira 14mm Suprens
S(501, [("ABRAÇADEIRA 14MM", [25, 87, 570, 805])], LN(501, [25, 400, 570, 805]))
for _r in ADD:
    if _r["pagina"] == 501:
        _r.update(marca="Suprens", foto_spec={"rect": [61, 201, 304, 358]})
# 502 (pág. impressa 501): grupos Suprens 545 / 542 / 541
S(502, [("ABRAÇADEIRA MANGOTE 19MM (GRUPO 545)", [25, 87, 570, 280]), ("ABRAÇADEIRA MANGOTE 32MM (GRUPO 545)", [25, 280, 570, 442]),
        ("ABRAÇADEIRA COM BORRACHA (GRUPO 542)", [25, 442, 570, 616])], LN(502, [25, 87, 570, 616]))
for _r in ADD:
    if _r["pagina"] == 502:
        _r["marca"] = "Suprens"
        if "19MM" in _r["_titulo"]:
            _r["foto_spec"] = {"rect": [96, 132, 174, 233]}
        elif "32MM" in _r["_titulo"]:
            _r["foto_spec"] = {"rect": [81, 239, 195, 352]}
for _c, _d in [("5416877", "ABRACADEIRA 068 X 77 TURB"), ("5418089", "ABRACADEIRA 080 X 89 TURB"), ("5419210", "ABRACADEIRA 092 X 101 SC."),
               ("5419510", "ABRACADEIRA 095 X 104 MB"), ("5411011", "ABRACADEIRA 101 X 110 IN"),
               ("5411131", "ABRACADEIRA 113 X 126 INTERC."), ("541104116", "ABRAC TURB 104 X 116 INTERC"),
               ("541128140", "ABRAC TURB 128 X 140 INTERC")]:
    ADD.append(dict(pagina=502, card=4, codigo=_c, descricao=_d, cod_ref="", variacoes="", aplicacao="", info="", marca="Suprens",
                    montadora="", _titulo="ABRAÇADEIRA TURBINA (GRUPO 541)", foto_spec={"rect": [94, 638, 204, 743]}))
NOTAS.append("Pág. 502: os códigos da abraçadeira turbina (grupo 541) estão impressos em preto; vários códigos de mangote têm 8 ou 9 "
             "dígitos (ex.: 545394732, 545616932) e 542137149 / 542143155 começam com 542 (os demais da lista com 545).")
# 503 (pág. impressa 502)
for _c, _d in [("5428086", "ABRAC INOX TUCHO 80 X 86"), ("5428695", "ABRAC INOX TUCHO 86 X 95"), ("54292101", "ABRAC INOX TUCHO 92 X 101"),
               ("542101110", "ABRAC INOX TUCHO 101 X 110")]:
    ADD.append(dict(pagina=503, card=1, codigo=_c, descricao=_d, cod_ref="", variacoes="", aplicacao="", info="", marca="",
                    montadora="", _titulo="ABRAÇADEIRA INOX TUCHO", foto_spec={"rect": [394, 117, 524, 212]}))
S(503, [("ABRAÇADEIRA INOX TURB", [25, 211, 570, 355]), ("ABRAÇADEIRA INOX COM PARAFUSO", [25, 355, 570, 593]),
        ("ABRAC TURB REF C/PARAFUSO", [25, 593, 570, 805])], LN(503, [25, 211, 570, 805]))
for _r in ADD:
    if _r["pagina"] == 503 and _r["codigo"] == "5414043":
        _r["descricao"] = "ABRAC TURB 032 X 035 / 040 X 043 REF C/PARAFUSO"
NOTAS.append("Pág. 503: 5414043 está impresso duas vezes (032x035 e 040x043); lançado uma vez com as duas medidas. 541108130 "
             "(abrac inox 108x130 c/parafuso) tem 9 dígitos.")
# 504 (pág. impressa 503)
S(504, [("ABRAÇADEIRA TURBINA REFORÇADA C/PARAFUSO", [25, 87, 570, 230]), ("ABRAC TURB 112 X 124 REF C/PARAFUSO", [25, 230, 570, 334]),
        ("ABRAÇADEIRA TURBINA", [25, 334, 570, 496]), ("ABRAÇADEIRA TURBINA INTERC", [25, 496, 570, 616]),
        ("ABRAÇADEIRA INOX TUCHO INTERC. (GRUPO 541)", [25, 616, 570, 805])],
  dict(LN(504, [25, 230, 570, 805]), **{"541112124": "ABRAC TURB 112 X 124 REF C/PARAFUSO"}))
for _c, _d, _card, _t, _f in [
        ("5412430", "ABRACADEIRA 024 X 030 REFORÇADA C/PARAFUSO", 1, "ABRAÇADEIRA TURBINA REFORÇADA C/PARAFUSO", [27, 102, 166, 210]),
        ("5412834", "ABRACADEIRA 028 X 034 REFORÇADA C/PARAFUSO", 1, "ABRAÇADEIRA TURBINA REFORÇADA C/PARAFUSO", [27, 102, 166, 210]),
        ("5413238", "ABRACADEIRA 032 X 038 REFORÇADA C/PARAFUSO", 1, "ABRAÇADEIRA TURBINA REFORÇADA C/PARAFUSO", [27, 102, 166, 210]),
        ("541128140", "ABRACADEIRA 128 X 140 INTERC", 4, "ABRAÇADEIRA TURBINA INTERC", [49, 500, 166, 616])]:
    ADD.append(dict(pagina=504, card=_card, codigo=_c, descricao=_d, cod_ref="", variacoes="", aplicacao="", info="", marca="",
                    montadora="", _titulo=_t, foto_spec={"rect": _f}))
for _r in ADD:
    if _r["pagina"] == 504 and _r["card"] == 1:
        _r["info"] = "20MM"
NOTAS.append("Pág. 504: 541104116 e 541128140 também estão na pág. 502 (grupo 541).")
# 505-506 (págs. impressas 504-505): cardan e escapamento (um produto por card)
TIPOS.insert(0, (r"^PF CRUZETA", "PARAFUSO CRUZETA"))
_APL4 = "Volkswagen, Ford, Agrale, Gen. Motors, Mercedes"
for _p, _c, _d, _f, _kw in [
        (505, "9025152", "PF CRUZETA VW FORD 3/8 X 20MM", [50, 108, 142, 151],
         dict(aplicacao="14.200/16.200/16.220/17.220", montadora="Volkswagen, Ford")),
        (505, "10007545", "MB ABRAÇADEIRA CRUZETA CARDAN C/ APOIO LATERAL 5-263X/5-275", [33, 187, 221, 267],
         dict(aplicacao="709/12/809/12/912/14 (F10,0-C/C55M)", montadora="Mercedes-Benz")),
        (505, "5067010", "MB ABRAC CRUZETA 1620 ORIGIN C/ APOIO LATERAL (F10,5-C/C60M)", [39, 284, 244, 361],
         dict(cod_ref="695.995.7010", aplicacao="L1218/1620 p/cruzeta SPL90.1X", montadora="Mercedes-Benz")),
        (505, "5017059", "MB ABRAC CRUZ CARDAN CRUZET 5-273X", [29, 379, 163, 457],
         dict(aplicacao="Volkswagen, Ford, Agrale, Gen. Motors, Mercedes | Cruzeta 5-121X/5-153X/5-310X/5-273X/CZ-202/CZ-119/CZ-253",
              info="15MM / 47MM / PF 10MM", montadora="Volkswagen, Ford, Agrale, GM, Mercedes-Benz")),
        (505, "5063407", "MB ABRAC CRUZ CARDAN", [199, 383, 364, 480],
         dict(aplicacao=_APL4 + " | Aplic. cruzeta 5-438X/CZ-264", info="20MM / 57MM / PF 3/8",
              montadora="Volkswagen, Ford, Agrale, GM, Mercedes-Benz")),
        (505, "5017089", "MB ABRAC CRUZ CARDAN", [382, 386, 537, 488],
         dict(aplicacao="Cruzeta SPL250-1X/CZ-232; Volvo aplicação cruzeta SPL250-1X/CZ-232; para Iveco aplicação cruzeta SPL250-1X/CZ-232",
              info="29MM / 90MM / PF 12MM", montadora="Volvo, Iveco")),
        (505, "5069499", "ABRACADEIRA ESCAPE VOLVO FH,NH,EDC,FM", [49, 646, 238, 760], dict(montadora="Volvo")),
        (505, "5065499", "ABRA ESCAP. COMP VOLVO N10/12", [325, 651, 482, 760],
         dict(aplicacao="N10/N12/NL/B58", cod_ref="475499", montadora="Volvo")),
        (506, "5069499", "ABRACADEIRA ESCAPE VOLVO FH,NH,EDC,FM", [46, 105, 234, 219], dict(montadora="Volvo")),
        (506, "5065499", "ABRA ESCAP. COMP VOLVO N10/12", [323, 107, 480, 216],
         dict(aplicacao="N10/N12/NL/B58", cod_ref="475499", montadora="Volvo")),
        (506, "5067100", "ABRAÇADEIRA ESCAPAMENTO 5\" 127MM UNIVERSAL.", [83, 290, 245, 398], {})]:
    X(_p, _c, _d, _f, **_kw)
NOTAS.append("Págs. 505-506: 5069499 e 5065499 aparecem nas duas páginas (e no cap. Peças Volvo, pág. 398); a descrição do 10007545 "
             "estava impressa como imagem (transcrita).")
for _r in ADD:
    if _r["pagina"] == 504 and _r["codigo"] in ("541104116", "541128140"):
        _r.update(_nao_agrupar=False, card=4, _titulo="ABRAÇADEIRA TURBINA INTERC", foto_spec={"rect": [49, 500, 166, 616]})
    if _r["pagina"] == 503 and _r["_titulo"] == "ABRAÇADEIRA INOX TUCHO":
        _r["card"] = 90
