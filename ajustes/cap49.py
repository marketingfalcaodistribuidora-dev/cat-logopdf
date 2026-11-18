# Capítulo 49 - Ferragens, Fitas e Parafusos para Móveis (págs. 524-530)
# Listas por caixa: cada caixa (seção) = 1 produto com os códigos como itens; código+descrição via tabela_livre.ler_pagina,
# seções dadas à mão (retângulos pelas bordas das molduras); foto = maior imagem da seção.
import re

from tabela_livre import _spans, ler_pagina

TIPOS = []
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(524, 531))
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


TIPOS += [(r"DOBRADICA", "DOBRADIÇA"), (r"^SUPORTE", "SUPORTE"), (r"PONTEIRA", "PONTEIRA"), (r"PASSA CABO", "PASSA CABO"), (r"ESQUADRETA", "ESQUADRETA"),
          (r"TRILHO", "TRILHO"), (r"PUXADOR", "PUXADOR"), (r"RODIZIO", "RODÍZIO"), (r"PISTAO", "PISTÃO A GÁS"), (r"CORREDICA", "CORREDIÇA"),
          (r"FECHADURA", "FECHADURA"), (r"TAPA FURO", "TAPA FURO"), (r"ADESIVO|SUPER BOND|COLA", "ADESIVO"), (r"ESTOPA", "ESTOPA"),
          (r"DESENGRIPANTE|VASELINA", "SPRAY"), (r"^FITA", "FITA"), (r"^ABR ", "ABRAÇADEIRA NYLON"), (r"FURADEIRA", "FURADEIRA"), (r"ESTILETE", "ESTILETE"),
          (r"TRENA", "TRENA"), (r"ALICATE", "ALICATE"), (r"^CH ", "CHAVE DE FENDA / PHILLIPS"), (r"CHIP BOARD", "PARAFUSO CHIP BOARD"),
          (r"AUTO BROCANTE|TORX", "PARAFUSO AUTOBROCANTE"), (r"^PF", "PARAFUSO")]
_XS = [25, 208, 392, 575]
_YS = [88, 268, 449, 629, 806]


def _ft(p, col, lin):
    """Maior imagem dentro da célula (coluna, linha) da grade 3 x 4."""
    _, imgs = _spans(p)
    r = [_XS[col], _YS[lin], _XS[col + 1], _YS[lin + 1]]
    f = [b for b in imgs if _dentro(r, (b[0] + b[2]) / 2, (b[1] + b[3]) / 2) and (b[2] - b[0]) * (b[3] - b[1]) > 500]
    return [round(v, 1) for v in max(f, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))]


def C(p, col, lin, cod, desc, **kw):
    X(p, cod, desc, _ft(p, col, lin), **kw)


def GR(p, col, lin, tit, itens, **kw):
    f = _ft(p, col, lin)
    for c, d in itens:
        r = dict(pagina=p, card=10 * lin + col + 1, codigo=c, descricao=d, cod_ref="", variacoes="", aplicacao="", info="", marca="", montadora="",
                 _titulo=tit, foto_spec={"rect": f})
        r.update(kw)
        ADD.append(r)


# 524 (pág. impressa 523)
GR(524, 0, 0, "DOBRADICA CALCO FIX C/PISTAO", [("1194415", "DOBRADICA CALCO FIX C/PISTAO CURVA"), ("1194416", "DOBRADICA CALCO FIX C/PISTAO SUPER CURVA"),
                                               ("1194419", "DOBRADICA CALCO FIX C/PISTAO SUPER CURVA INOX"), ("1194418", "DOBRADICA CALCO FIX C/PISTAO CURVA INOX")])
C(524, 1, 0, "1194417", "DOBRADICA CALCO FIX C/PISTAO RETA INOX")
C(524, 2, 0, "1192315", "DOBRADICA CALCO FIX C/PISTAO CURVA")
GR(524, 0, 1, "SUPORTE CADEIRINHA 2 FUROS - PESADA", [("1200002", "SUPORTE CADEIRINHA 14 X 14 2 FUROS - PESADA"), ("1200008", "SUPORTE CADEIRINHA 17 X 17 2 FUROS - PESADA")])
for _a in [(1, 1, "1200085", "SUPORTE PRATELEIRA TUBINHO BRANCO 10 X 15"), (2, 1, "1200004", "SUPORTE CABIDEIRO OBLONGO"), (0, 2, "1200005", "SUPORTE CABIDEIRO REDONDO"),
           (1, 2, "1200035", "SUPORTE AEREO REFORCADO COM CAPA"), (2, 2, "1200188", "PONTEIRA GALAXY 15MM PAR - FACETATO"), (0, 3, "1200069", "PASSA CABO PLASTICO BRANCO 60MM"),
           (1, 3, "1200039", "JG ESQUADRETA 8 PARAFUSOS C/4 PECAS 41MM")]:
    C(524, *_a)
NOTAS.append("Pág. 524: o código 1194416 está impresso em dois cards (dobradiça c/pistão super curva e dobradiça S/pistão curva); o card 3 também repete "
             "a descrição 'c/pistão curva' do 1194415 no código 1192315.")
# 525 (pág. impressa 524)
for _a in [(0, 0, "1212353", "TRILHO SUPERIOR P/PORTA DE CORRER - 3MTS"), (1, 0, "1212383", "TRILHO INFERIOR P/PORTA DE CORRER - 3MTS"),
           (2, 0, "12130713", "PUXADOR GOLA 15MM X 3,5 CM INOX FOSCO - 3MTS"), (0, 1, "1213973", "PUXADOR GOLA 18MM X 3,5 CM FOSCO - 3MTS"),
           (1, 1, "1213073", "PUXADOR GOLA 15MM X 3,5 CM FOSCO - 3MTS"), (2, 1, "1212203", "PUXADOR GALAXY 15MM JATEADO FOSCO - 3MTS"),
           (0, 2, "1220351", "RODIZIO TEN RG35 INCOLOR C/FREIO"), (1, 2, "1227501", "RODIZIO TEN RG75 INCOLOR C/FREIO"), (2, 2, "1227500", "RODIZIO TEN RG75 INCOLOR S/FREIO")]:
    C(525, *_a)
# 526 (pág. impressa 525)
GR(526, 0, 0, "PISTAO TEN A GAS FORCA INVERSA", [("1226000", "PISTAO TEN A GAS 060N FORCA INVERSA"), ("1228000", "PISTAO TEN A GAS 080N FORCA INVERSA"),
                                                 ("1221000", "PISTAO TEN A GAS 100N FORCA INVERSA")])
GR(526, 1, 0, "PISTAO TEN A GAS", [("1220080", "PISTAO TEN A GAS 080N"), ("1220100", "PISTAO TEN A GAS 100N"), ("1220120", "PISTAO TEN A GAS 120N"), ("1220140", "PISTAO TEN A GAS 140N")])
GR(526, 2, 0, "CORREDICA LIGHT MINI", [("1220030", "CORREDICA LIGHT MINI 300MM"), ("1220035", "CORREDICA LIGHT MINI 350MM"), ("1220040", "CORREDICA LIGHT MINI 400MM"),
                                       ("1220045", "CORREDICA LIGHT MINI 450MM")])
GR(526, 0, 1, "CORREDICA H45 LARGA", [("1222500", "CORREDICA H45 LARGA 250MM"), ("1223000", "CORREDICA H45 LARGA 300MM"), ("1223500", "CORREDICA H45 LARGA 350MM"),
                                      ("1224000", "CORREDICA H45 LARGA 400MM"), ("1224500", "CORREDICA H45 LARGA 450MM")])
for _a in [(1, 1, "1220300", "FECHADURA PARA GAVETA CANO LONGO"), (2, 1, "1220022", "FECHADURA PARA GAVETA CANO CURTO"), (0, 2, "1191250", "TAPA FURO BRANCO 12MM CARTELA C/50 UNID"),
           (2, 2, "9801516", "ADESIVO INSTANTÂNIO 20G"), (0, 3, "9811446", "SUPER BOND THEREE BOND 2G"), (1, 3, "9801868", "ESTOPA POLIMENTO"),
           (2, 3, "9800116", "DESENGRIPANTE WHITE LUB 300 ML")]:
    C(526, *_a)
# 527 (pág. impressa 526)
for _a, _kw in [((0, 0, "9821468", "FITA DUPLA FACE VHB 12MM X 20MTS"), dict(marca="3M")), ((1, 0, "9821469", "FITA DUPLA FACE VHB 19MM X 20MTS"), dict(marca="3M")),
                ((2, 0, "9821496", "FITA DUPLA FACE 3M 12MM X 20MTS"), dict(marca="3M")), ((0, 1, "9820110", "FITA DUPLA FACE 12MM X 1MT"), dict(marca="3M")),
                ((1, 1, "9792059", "VASELINA SPRAY 300ML"), {}), ((2, 1, "9731850", "FITA CREPE TEK 18MM X 50M"), dict(marca="Tekbond")),
                ((0, 2, "9733001", "COLA TEK DE CONTATO 200G"), dict(marca="Tekbond")), ((1, 2, "9731710", "FITA EMPACOTAMENTO TRANSPARENTE"), dict(marca="Tekbond")),
                ((2, 2, "9732020", "ADESIVO TEK ACRILICO SELA MADEIRA BRANCO 425G"),
                 dict(marca="Tekbond", info="Tempo de formação de película: 30 minutos | Tempo de cura total: 24 a 96 horas | Profundidade de cura em 24 horas: 3 mm | "
                                            "Densidade a 25 °C: 1,50±1,60g/mL | Temperatura ideal de aplicação: +5 a 35 °C | Temperatura de trabalho: -20 a 80 °C | "
                                            "Taxa de encolhimento: 17% | Tempo de armazenamento 5 a 25 °C: 36 meses")),
                ((1, 3, "5592020", "FITA ISOLANTE TECIDO 20MTS S/COLA"), {})]:
    C(527, *_a, **_kw)
GR(527, 0, 3, "FITA ISOLANTE", [("5590005", "FITA ISOLANTE 05MTS"), ("5590010", "FITA ISOLANTE 10MTS"), ("5590020", "FITA ISOLANTE 20MTS")])
C(527, 2, 3, "9731710", "FITA EMBALAGEM TEK 48MM X 40M", marca="Tekbond")
NOTAS.append("Pág. 527: o código 9731710 está em dois cards (fita empacotamento transparente e fita embalagem Tek 48mm x 40m).")
# 528 (pág. impressa 527)
for _a, _kw in [((0, 0, "7713515", "ABR NYLON PLASTICA 3,5 X 150"), {}),
                ((1, 0, "10142362", 'FURADEIRA IMPACTO TRAMONTINA 1/2" 220V - 500W C/SUP'), dict(marca="Tramontina", info="Com sistema de reversão de rotação")),
                ((2, 0, "10142363", 'FURADEIRA IMPACTO TRAMONTINA 1/2" 127V - 500W C/SUP'), dict(marca="Tramontina", info="Com sistema de reversão de rotação")),
                ((0, 1, "6019541", "ESTILETE 18MM PLASTICO C/PONTA DE METAL"), {}), ((1, 1, "6013891", "TRENA 5MTS EMBORRACHADO"), {}),
                ((2, 1, "9920294", "ALICATE UNIVERSAL"), dict(marca="Gedore Red"))]:
    C(528, *_a, **_kw)
for _i in ler_pagina(528):
    if _i["descricao"].startswith("CH PHILLIPS"):
        _t, _f, _n = "CHAVE PHILLIPS EMBORRACHADA", [32, 473, 283, 584], 7
    elif _i["descricao"].startswith("CH FENDA"):
        _t, _f, _n = "CHAVE FENDA EMBORRACHADA", [314, 482, 561, 588], 8
    else:
        continue
    ADD.append(dict(pagina=528, card=_n, codigo=_i["codigo"], descricao=_i["descricao"], cod_ref="", variacoes="", aplicacao="", info="", marca="Stanley", montadora="",
                    _titulo=_t, foto_spec={"rect": _f}))
# 529-530 (págs. impressas 528-529)
S(529, [("PARAFUSO CHIP BOARD", [25, 87, 575, 440]), ("PARAFUSOS PF.PN RS ZB", [25, 440, 575, 806])])
S(530, [("PARAFUSO AUTO BROCANTE", [9, 87, 575, 236]), ("PARAFUSO AUTO BROCANTE FLANGEADO", [9, 236, 575, 375]),
        ("PARAFUSO AUTO BROCANTE FLANGEADO CABECA CHATA", [9, 375, 575, 522]), ("PF.TORX 4,2 X 25 ASSOALHO AUTOBROCANTE", [9, 522, 575, 806])],
  {"1101525": "PF.TORX 4,2 X 25 ASSOALHO AUTOBROCANTE"})
for _r in ADD:
    if _r["codigo"] == "1101525":
        _r["info"] = "Parafuso atarrachante assoalho | Ponta broca redonda Torx zincado"
