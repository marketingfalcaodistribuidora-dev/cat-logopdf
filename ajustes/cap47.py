# Capítulo 47 - Terminais, Fusíveis e Anéis O-Ring (págs. 513-516)
# Listas por caixa: cada caixa (seção) = 1 produto com os códigos como itens; código+descrição via tabela_livre.ler_pagina,
# seções dadas à mão (retângulos pelas bordas das molduras); foto = maior imagem da seção.
import re

from tabela_livre import _spans, ler_pagina

TIPOS = []
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(513, 517))
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


TIPOS += [(r"^TERMINAL", "TERMINAL"), (r"^CAPA", "CAPA DE TERMINAL"), (r"SOQUETE", "SOQUETE"), (r"^CONECTOR", "CONECTOR"), (r"^FITA", "FITA ISOLANTE"),
          (r"^PORTA FUSIVEL", "PORTA FUSÍVEL"), (r"^PORTA|^FUSIVEL", "FUSÍVEL"), (r"^CABO", "CABO"), (r"^CHICOTE", "CHICOTE"), (r"^GARRA", "GARRA DE BATERIA"),
          (r"^KIT", "KIT ANEL ORING"), (r"ORING|ORIG", "ANEL ORING"), (r"GAXETA", "GAXETA")]
# 513 (pág. impressa 512): repete a pág. 402, com alguns itens novos
for _c, _d, _f, _kw in [
        ("5580105", "TERMINAL ENCAIXE C/TRAVA UNIVERSAL", [47, 101, 146, 191], dict(variacoes="7020 C")),
        ("5581800", "CAPA DE TERMINAL ENCAIXE MACHO 6,3MM", [235, 101, 280, 131], {}),
        ("5581802", "CAPA DE TERMINAL ENCAIXE FEMEA 6,3MM", [420, 101, 466, 131], {}),
        ("5587009", "TERMINAL OLHAL FURO 3/6 FIO 2,5 MM", [33, 211, 113, 260], dict(variacoes="7009")),
        ("5587022", "TERMINAL OLHAL FURO 5/32 F 1,5", [214, 213, 305, 255], dict(variacoes="7022 A")),
        ("5580253", "TERMINAL OLHAL FURO 1/4 F 2,50", [396, 217, 472, 256], dict(variacoes="7023 A")),
        ("5587028", "TERMINAL ELETRICO MACHO MENOR", [35, 307, 153, 350], dict(variacoes="7028")),
        ("5580036", "TERMINAL ENCAIXE MOSQUITINHO", [222, 301, 343, 347], dict(variacoes="7030")),
        ("5581896", "TERMINAL OLHAL FURO 3/8 GRANDE", [399, 296, 501, 347], dict(variacoes="7031")),
        ("5580120", "TERMINAL ELETRICO MACHO REFORC", [39, 391, 182, 433], dict(variacoes="7033")),
        ("5581991", "TERMINAL TUBO MACHO PARA MOTO", [214, 389, 332, 439], dict(variacoes="7038")),
        ("5587821", "TERMINAL OLHAL FURO 8,0 F GROS", [395, 389, 516, 436], dict(variacoes="7821")),
        ("5587907", "TERMINAL OLHAL FURO 8,0 F 2,5", [27, 486, 162, 532], dict(variacoes="7907")),
        ("5587061", "MB SOQUETE LAMPADA PAINEL ISOL", [216, 484, 316, 532], dict(montadora="Mercedes-Benz")),
        ("5100200", "TERMINAL PONTEIRA PEQUENO P/CABO 10 A 25MM²", [469, 463, 538, 521], dict(info="Linha leve | 9,0MM")),
        ("5100201", "TERMINAL PONTEIRA 13MM AUTOMOV 14MM A 95MM²", [88, 550, 165, 615], dict(info="Médio | 13,0MM / 12,5MM")),
        ("5101201", "TERMINAL PONTEIRA GRANDE P/CABO 35 A 95MM²", [278, 554, 349, 613], dict(info="15,0MM / 11,5MM")),
        ("5101202", "TERMINAL PONTEIRA 13MM AUTOMOV 35MM A 50MM²", [460, 546, 537, 611], dict(info="10,0MM / 9,0MM")),
        ("5101899", "TERMINAL BATERIA SAPINHO P/CABO 10MM A 50MM", [97, 640, 199, 712], dict(info="17,0 MM")),
        ("5100104", "TERMINAL BATERIA 16MM SAPAO", [285, 641, 383, 715], dict(info="17,0 MM")),
        ("5593551", "CONECTOR 02 VIAS C/TERMINAIS", [395, 637, 501, 711], dict(info="Lançamento 04/25")),
        ("5593511", "CONECTOR 04 VIAS C/TERMINAIS", [82, 724, 200, 804], dict(info="Lançamento 04/25"))]:
    X(513, _c, _d, _f, **_kw)


def _item(p, card, c, d, tit, foto):
    ADD.append(dict(pagina=p, card=card, codigo=c, descricao=d, cod_ref="", variacoes="", aplicacao="", info="", marca="", montadora="",
                    _titulo=tit, foto_spec={"rect": foto}))


for _c, _d in (("5590005", "FITA ISOLANTE 05MTS"), ("5590010", "FITA ISOLANTE 10MTS"), ("5590020", "FITA ISOLANTE 20MTS")):
    _item(513, 23, _c, _d, "FITA ISOLANTE", [210, 742, 278, 792])
for _c, _d in (("5592020", "FITA ISOLANTE TECIDO 20MTS S/COLA"), ("5591020", "FITA ISOLANTE TECIDO 10MTS S/COLA")):
    _item(513, 24, _c, _d, "FITA ISOLANTE TECIDO S/COLA", [397, 725, 459, 803])
NOTAS.append("Pág. 513: repete os terminais da pág. 402 (cap. Terminais, Chicotes e Fios); 5591020 aparece só aqui.")
# 514 (pág. impressa 513): repete a pág. 404 (389202 é referência original, não código)
_CACHE[514] = ler_pagina(514, ignorar=("389202",))
S(514, [("FUSIVEL MINI G732", [25, 87, 207, 268]), ("FUSIVEL LAMINA G731", [207, 87, 388, 268]), ("FUSIVEL MAX G731", [388, 87, 570, 268]),
        ("FUSIVEL DE VIDRO", [25, 268, 207, 446]), ("FUSIVEL PORCELANA", [207, 268, 388, 446]), ("PORTA FUSIVEL", [388, 268, 570, 446]),
        ("CABO DE TRANSMISSÃO DE CARGA", [25, 446, 388, 627]), ("CHICOTE SENSOR PRESSAO OLEO", [388, 446, 570, 627]),
        ("CABO CHUPETA", [25, 627, 370, 805]), ("GARRA BATERIA", [370, 627, 570, 805])],
  {"6013500": "CABO DE TRANSMISSÃO DE CARGA TIPO CHUPETA 300A", "5589202": "CHICOTE SENSOR PRESSAO OLEO",
   "7000600": "CABO CHUPETA 600A 5MTS REFORCADO", "5590053": "GARRA BATERIA 600 AMP (2 PECAS)",
   "7301500": "FUSIVEL PORCELANA 15AMP MARON", "7303000": "FUSIVEL PORCELANA 30AMP PRETO"})
for _r in ADD:
    if _r["pagina"] != 514:
        continue
    if _r["codigo"] == "6013500":
        _r.update(marca="Riosul", foto_spec={"rect": [35, 492, 297, 616]})
    if _r["codigo"] == "5589202":
        _r.update(cod_ref="389202", aplicacao="SC 94/114/124/164/F112/113", montadora="Scania", foto_spec={"rect": [410, 472, 551, 572]})
    if _r["codigo"] == "7000600":
        _r.update(info="Especificações: 600 amperes | 5 metros de comprimento | Bitola de 10mm | Revestimento cobreado | Garras tipo jacaré",
                  foto_spec={"rect": [113, 679, 364, 786]})
    if _r["codigo"] == "5590053":
        _r["foto_spec"] = {"rect": [378, 632, 558, 734]}
NOTAS.append("Pág. 514: repete os fusíveis e cabos da pág. 404.")
# 515-516 (págs. impressas 514-515): kits de anel oring e relação completa (coluna direita)
for _p, _kit, _dk, _fk, _ind, _lista in [
        (515, "7712168", "KIT ANEL ORING MILIMETRO", [32, 110, 157, 217], "ANEL ORING INDIVIDUAL MILIMETRO", [395, 395, 570, 805]),
        (516, "7712167", "KIT ANEL ORING POLEGADA", [41, 95, 187, 236], "ANEL ORING INDIVIDUAL POLEGADA", [355, 365, 570, 805])]:
    X(_p, _kit, _dk, _fk, info="Estojo com 30 medidas (tabela com nº, código, Int, W e quantidade impressa na página)")
    for _c, _d in LN(_p, _lista).items():
        if _c != "4686530":
            _item(_p, 2, _c, _d, _ind, _fk)
X(515, "4686530", "GAXETA 10 X 16 X 4.00", [95, 614, 294, 745])
NOTAS.append("Págs. 515-516: a foto dos anéis individuais é a do kit (a tabela da página é imagem); 4682216 e 4682217 estão impressos como 'ANEL ORIG'.")
