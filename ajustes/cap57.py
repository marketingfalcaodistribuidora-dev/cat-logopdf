# Capítulo 57 - Soquetes de Impacto, Saca Filtros e Organização (págs. 594-603)
# Listas por caixa: cada caixa (seção) = 1 produto com os códigos como itens; código+descrição via tabela_livre.ler_pagina,
# seções dadas à mão (retângulos pelas bordas das molduras); foto = maior imagem da seção.
import re

from tabela_livre import _spans, ler_pagina

TIPOS = []
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(594, 604))
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




def P(p, cod, desc, foto=None, **kw):
    """Produto único; foto=None = repetição de produto com foto em outra página (ou sem foto no catálogo)."""
    r = dict(pagina=p, card=500 + len(ADD), codigo=cod, descricao=desc, cod_ref="", variacoes="", aplicacao="", info="", marca="", montadora="",
             _nao_agrupar=True, foto_spec={"rect": foto} if foto else None)
    r.update(kw)
    ADD.append(r)


def GP(p, card, titulo, itens, foto=None, **kw):
    """Card com lista de códigos = 1 produto; itens = [(código, descrição)]."""
    for c, d in itens:
        r = dict(pagina=p, card=card, codigo=c, descricao=d, cod_ref="", variacoes="", aplicacao="", info="", marca="", montadora="",
                 _titulo=titulo, foto_spec={"rect": foto} if foto else None)
        r.update(kw)
        ADD.append(r)



import json as _json  # noqa: E402
import os as _os  # noqa: E402

from capitulos import WORK as _WORK  # noqa: E402


def _cards(p):
    return [c for c in _json.load(open(_os.path.join(_WORK, "raw", f"p{p:03d}.json"), encoding="utf-8"))["cards"] if c["id"]]


def FA(p, cod):
    """Foto automática: imagem da menor moldura que contém o código, a mais próxima e maior."""
    sp, imgs = _spans(p)
    ss = [s for s in sp if re.sub(r"[^0-9]", "", s["t"]) == cod]
    if not ss:
        return None
    s = ss[0]
    cx, cy = (s["x"] + s["x1"]) / 2, s["y"] + 3
    cs = [c["rect"] for c in _cards(p) if _dentro(c["rect"], cx, cy)]
    r = min(cs, key=lambda r: (r[2] - r[0]) * (r[3] - r[1])) if cs else [0, 0, 600, 850]
    f = [b for b in imgs if _dentro(r, (b[0] + b[2]) / 2, (b[1] + b[3]) / 2) and 700 < (b[2] - b[0]) * (b[3] - b[1]) < 250000] or \
        [b for b in imgs if 700 < (b[2] - b[0]) * (b[3] - b[1]) < 250000]
    if not f:
        return None
    b = min(f, key=lambda b: abs((b[0] + b[2]) / 2 - cx) + abs((b[1] + b[3]) / 2 - cy) - ((b[2] - b[0]) * (b[3] - b[1])) ** 0.5)
    return [round(v, 1) for v in b]


def A(p, cod, desc, foto=None, **kw):
    P(p, cod, desc, foto or FA(p, cod), **kw)


def LS(p, card, titulo, area, foto=None, desc=None, **kw):
    """Lista 'código descrição' dentro da área = 1 produto com itens."""
    d = LN(p, area)
    d.update(desc or {})
    _, imgs = _spans(p)
    if not foto:
        f = [b for b in imgs if _dentro(area, (b[0] + b[2]) / 2, (b[1] + b[3]) / 2) and 700 < (b[2] - b[0]) * (b[3] - b[1]) < 250000]
        foto = [round(v, 1) for v in max(f, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))] if f else None
    GP(p, card, titulo, [(c, re.sub(r"^[-–\\s]+", "", t)) for c, t in d.items()], foto, **kw)


TIPOS += [(r"SOQUETE|^SOQ |KINGT SOQ", "SOQUETE DE IMPACTO"), (r"ALICATE", "ALICATE"), (r"^ADAP", "ADAPTADOR DE SOQUETE"), (r"GRIFO|INGLESA", "CHAVE AJUSTÁVEL"), (r"EXTENSAO", "EXTENSÃO DE IMPACTO"), (r"CABO DE FORCA", "CABO DE FORÇA"),
          (r"CHAVE RODA|CH RODA", "CHAVE DE RODA"), (r"SACA FILTRO", "SACA FILTRO"), (r"ALMOTOLIA", "ALMOTOLIA"), (r"CINTA P/", "CINTA PARA ANÉIS DE PISTÃO"), (r"PINO CONECTOR", "PINO CONECTOR"), (r"VALVULA ESFERA", "VÁLVULA DE ESFERA"),
          (r"ESPIGAO", "ESPIGÃO"), (r"CAIXINHA", "CAIXINHA ORGANIZADORA"), (r"ESTANTE", "ESTANTE DE CAIXAS"), (r"CAIXA FERRAMENTAS", "CAIXA DE FERRAMENTAS"), (r"CADEADO", "CADEADO"), (r"TORQUEADOR", "TORQUEADOR"),
          (r"BOMBA", "BOMBA DE GRAXA"), (r"ACOPLADOR", "ACOPLADOR DE GRAXA")]
_KT, _RV, _TR = dict(marca="King Tony"), dict(marca="Raven"), dict(marca="Tramontina")
# 594 (pág. impressa 593)
LS(594, 1, 'SOQUETE IMPAC COMP 88MM 1"', [25, 88, 570, 256], [39, 91, 204, 251])
LS(594, 2, 'KINGT SOQ IMPACTO SEXT 1"', [25, 256, 570, 398], [39, 289, 214, 380], **_KT)
LS(594, 3, "KINGT SOQ IMPACTO SEXT 3/4", [25, 398, 570, 551], [31, 429, 217, 526], **_KT)
A(594, "9970915", "9AA15 - ALICATE PARA ABRAÇADEIRA ELÁSTICA DO RADIADOR", [46, 631, 176, 733], **_KT)
A(594, "9970917", "9AA17 ALICATE PARA REMOVER OU INSTALAR ABRAÇADEIRA DA LINHA DE COMBUSTÍVEL", [229, 586, 356, 719], **_KT)
A(594, "9970911", "9BK11 ALICATE PARA BALANCEAMENTO DE RODAS", [405, 592, 541, 711], **_KT)
# 595 (pág. impressa 594)
_H = sorted(s["y"] for s in _spans(595)[0] if s["t"].strip().startswith("SOQUETE IMPACTO"))
LS(595, 1, 'SOQUETE IMPACTO 1" CURTO', [25, _H[0] + 4, 570, _H[1] - 2], [439, 119, 563, 266])
LS(595, 2, 'SOQUETE IMPACTO 1" LONGO', [25, _H[1] + 4, 570, _H[2] - 2], [441, 301, 563, 515])
LS(595, 3, "SOQUETE IMPACTO 3/4 LONGO", [25, _H[2] + 4, 570, 805], [441, 580, 567, 794])
# 596 (pág. impressa 595)
A(596, "6021209", 'KIT SOQUETE IMPAC LONGO 1/2" 17/19/21 PROTECÇÃO NYLON', [103, 157, 222, 304])
A(596, "6021215", "KIT SOQUETE IMPAC 1/2 10 A 27MM 15 PECAS", [360, 155, 518, 246], info="1 maleta | 15 soquetes: 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24 e 27 mm")
A(596, "6023408", "KIT SOQUETE IMPAC 3/4 - 19 A 38 08 PECAS", [43, 403, 258, 534])
A(596, "6023451", "JG SOQUETE IMPACTO 3/4 - 21 PCS (19MM-50MM)", [352, 361, 507, 480], info="1 maleta | 16 soquetes: 17, 18, 19, 20, 21, 22, 24, 27, 29, 30, 32, 33, 36, 38, 41 e 46 mm | Extensões 3/4 de 200 e 100 mm | 1 cabo de força | 1 chave catraca reversível")
A(596, "6022441", 'KIT SOQUETE IMPAC 1" 24/27/30/32/33/36/38/41 - 08 PECAS', [31, 593, 207, 755])
NOTAS.append("Pág. 596: 6023451 é anunciado como '19MM-50MM', mas a composição do card lista soquetes de 17 a 46 mm.")
# 597 (pág. impressa 596)
LS(597, 1, "ADAP SOQUETE", [25, 88, 570, 273], [31, 94, 207, 212])
LS(597, 2, "CHAVE GRIFO PC", [25, 273, 570, 429], [28, 275, 370, 376])
LS(597, 3, "CHAVE INGLESA AJUSTAVEL", [25, 429, 570, 608], [117, 427, 476, 526])
LS(597, 4, "EXTENSAO IMPAC P/SOQUETE", [25, 608, 570, 700], [31, 614, 221, 697])
LS(597, 5, "CABO DE FORCA T", [25, 700, 570, 805], [33, 706, 245, 799])
# 598 (pág. impressa 597)
LS(598, 1, "CHAVE RODA", [25, 170, 570, 291], [29, 117, 563, 167])
A(598, "6011501", "CH RODA CRUZ 17,19,21,23", [32, 300, 219, 486])
A(598, "6020300", "SACA FILTRO 3 GARRA TIPO ARANHA", [57, 496, 185, 626], info="Abertura 75MM a 110MM")
A(598, "6021003", "SACA FILTRO UNIVERSAL 3 GARRA", [211, 502, 369, 621])
A(598, "6020500", "ALMOTOLIA BICO FIXO 500ML", [408, 493, 559, 597])
A(598, "6010170", 'CINTA P/ ANEIS DE PISTAO 3"', [228, 650, 345, 760])
A(598, "6010171", 'CINTA P/ ANEIS DE PISTAO 4"', [422, 645, 546, 762])
# 599 (pág. impressa 598)
LS(599, 1, "SACA FILTRO CINTA", [25, 295, 298, 382], [37, 136, 293, 293])
A(599, "60250130", "SACA FILTRO CORRENTE 50 X 130 MM", [302, 95, 566, 253], info="Fabricado em aço | Uso universal | Punho ergonômico de 123 mm | Comprimento da corrente: 420 mm")
A(599, "6021326", "PINO CONECTOR NITTO 3/8 X 3/8", [37, 387, 275, 470])
LS(599, 4, "SACA FILTRO", [298, 480, 570, 553], [329, 382, 529, 478])
LS(599, 5, "VALVULA ESFERA MINI", [25, 553, 298, 805], [53, 567, 262, 708])
LS(599, 6, "ESPIGAO FIXO", [298, 553, 570, 805], [380, 649, 482, 737])
for _r in ADD:
    _r["descricao"] = _r["descricao"].lstrip("#").strip()
# 600 (pág. impressa 599)
for _c, _d, _a, _f in [("9911021", "SACA FILTRO DE ÓLEO TIPO CINTA 62 A 68MM", "Linha Fiat Fire e Fire EVO, Honda Civic, New Civic, City, Fit e New Fit, Toyota Corolla, Mitsubishi Pajero TR4", [41, 127, 222, 203]),
                       ("9911022", "SACA FILTRO DE ÓLEO TIPO CINTA 70 A 76MM", "Motores VW AP, AT, EA111, EA113, EA211, Ford 1.0 12V (3 cils.), Zetec Rocam 8V, Zetec, Duratec e Sigma 16V, GM 1.0 a 2.4 (8 e 16V, exceto Ecotec), 4.1, 4.3 V6, Fiat 1.6 e 1.8 (8 e 16V), entre outros", [29, 266, 222, 347]),
                       ("9911025", "SACA FILTRO DE ÓLEO TIPO CINTA 82 A 93MM", "Motor 1.6 VW AE/Ford CHT (com filtro de 93mm), Maxion HS 2.5 e 2.8, MWM 229 e Sprint", [39, 424, 212, 496]),
                       ("9911024", "SACA FILTRO DE ÓLEO TIPO CINTA 100 A 102MM", "Renault Master 2.5 16V (motor G9U) e Mitsubishi L200 2.5 8V (motor 4D56)", [31, 567, 240, 654]),
                       ("9910130", "SACA FILTRO DE ÓLEO TIPO CINTA 134 A 137MM", "Motores Mercedes-Benz", [36, 705, 256, 797])]:
    A(600, _c, _d, _f, aplicacao=_a, **_RV)
# 601 (pág. impressa 600)
GP(601, 1, "CAIXINHA PRETA", [("9613000", "CAIXINHA PRETA N 03"), ("9610228", "CAIXINHA PRETA N 05"), ("9611482", "CAIXINHA PRETA N 07")], [404, 95, 549, 192])
GP(601, 2, "CAIXINHA AZUL", [("9611967", "CAIXINHA AZUL N 03"), ("9611968", "CAIXINHA AZUL N 05"), ("9611969", "CAIXINHA AZUL N 07")], [412, 201, 548, 307])
GP(601, 3, "ESTANTE DE CAIXA", [("9621333", "ESTANTE DE CAIXA N3 C/60"), ("9621332", "ESTANTE DE CAIXA N5 P/54")], [38, 309, 152, 482], info="Obs: preço só da armação")
A(601, "6016117", "CAIXA FERRAMENTAS 7 COMPARTIMENTO", [41, 574, 249, 756], info="Dimensões: 500 x 200 x 250 (impresso em cm)", **_TR)
A(601, "6011339", "CAIXA FERRAMENTAS 5 COMPARTIMENTO", [366, 569, 558, 747], info="Dimensões: 500 x 200 x 300mm", **_TR)
# 602-603 (págs. impressas 601-602)
LS(602, 1, "CADEADO PAPAIZ", [25, 88, 570, 805], [32, 186, 418, 543], marca="Papaiz")
A(603, "6010903", "TORQUEADOR DESFORCIMETRO REFORÇADO", [287, 162, 561, 371], info="Acompanha: 1 desforcímetro/torqueador, maleta, barra de extensão, manivela e 2 soquetes 32 e 33mm em aço cromo vanádio | 100 x 395 x 235 mm")
A(603, "6011757", "BOMBA DE GRAXA 07 KG", [45, 422, 226, 606])
A(603, "8001027", "ACOPLADOR BICO GRAXA COM TRAVA", [65, 646, 225, 768])
A(603, "6011856", "ACOPLADOR BICO GRAXA", [350, 716, 491, 790])
