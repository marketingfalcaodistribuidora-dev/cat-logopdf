# Capítulo 58 - Ferramentas Elétricas e Pneumáticas (págs. 604-613)
# Listas por caixa: cada caixa (seção) = 1 produto com os códigos como itens; código+descrição via tabela_livre.ler_pagina,
# seções dadas à mão (retângulos pelas bordas das molduras); foto = maior imagem da seção.
import re

from tabela_livre import _spans, ler_pagina

TIPOS = []
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(604, 614))
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


TIPOS += [(r"PARAFUSADEIRA", "PARAFUSADEIRA"), (r"FURADEIRA", "FURADEIRA"), (r"CARREGADOR", "CARREGADOR"), (r"BATERIA", "BATERIA"), (r"CHAVE IMPACTO|CHAVE DE IMPACTO|CHAVE PNEUM", "CHAVE DE IMPACTO"),
          (r"POLICORTE", "POLICORTE"), (r"BROCA", "BROCA ANULAR"), (r"LIXADEIRA|ESMERILHADEIRA", "ESMERILHADEIRA"), (r"MAQUINA", "MÁQUINA SOLTA GRAMPO"), (r"DESTALONADOR", "DESTALONADOR"),
          (r"DESMONTADORA|DESMONTAGEM", "DESMONTAGEM DE PNEU"), (r"MARRETA|MARTELO", "MARRETA / MARTELO")]
_DW = dict(marca="Dewalt")
_RT, _SH = dict(marca="Rota"), dict(marca="Shallper")
_B = "Tensão 20V - 5,0Ah | Duração prolongada | Alimenta toda linha de ferramentas Dewalt"
_CG = "Carregador DCB1104 | Indicador LED de carga | Compatível com baterias íon de lítio 12V MAX, 20V MAX e Flexvolt | Montagem em parede"
# 604 (pág. impressa 603)
A(604, "6265052", 'FURADEIRA IMPACTO DEWALT 1/2" 580W 2 VEL', [84, 149, 283, 301], variacoes="DEWALT-DWD520", info='Lançamento 04/25 | 220 V | 1100 W | 0-1.200 / 0-3.500 | Mandril 1/2" (13 mm) | Acompanha empunhadura auxiliar, chave para mandril e limitador de profundidade', **_DW)
A(604, "6262552", "PARAFUSADEIRA BLACK E DECKER DRY WALL 2 20V", [360, 152, 551, 286], variacoes="DEWALT-DW255", info="Lançamento 04/25 | 220 Volts | 540 Watts | 0-5.300 rpm | Torque 6.8 Nm | Parafuso máx. 6 mm | Velocidade variável e reversível", **_DW)
A(604, "6268924", 'KIT CHAVE IMPACTO DEWALT 1/2" 13MM 20V MAX', [399, 347, 551, 548], **_DW)
A(604, "6268923", 'CHAVE IMPACTO DEWALT 1/2" 13MM 20V MAX S/BATE', [399, 347, 551, 548], **_DW)
A(604, "6261104", "CARREGADOR DEWALT BIVOLT LI-IO 4AH / 5AH 12V-20V", [246, 361, 352, 430], info=_CG, **_DW)
A(604, "6262043", "BATERIA DEWALT CHAVE IMPACTO LI-ION 5AH 20V", [278, 432, 370, 490], info=_B, **_DW)
A(604, "6268794", 'KIT CHAVE IMPACTO DEWALT 3/4" 19MM 20V MAX', [366, 579, 566, 770], **_DW)
A(604, "6068793", 'CHAVE IMPACTO DEWALT 3/4" 19MM 20V MAX S/BATE', [366, 579, 566, 770], info='Encaixe 3/4" (19mm) | Luz LED | 0-400 / 0-1.200 / 0-1.900 RPM | 0-2.400 IPM | Torque 950 Nm | Carregadores DCB115 e DCB118', **_DW)
NOTAS.append("Pág. 604: 6261104 está impresso como carregador 4AH e 5AH; a parafusadeira 6262552 diz 'Black e Decker' mas a marca do card é Dewalt; 6068793 foge do padrão 626xxxx dos demais.")
# 605-607 (págs. impressas 604-606)
A(605, "6268730", 'POLICORTE DEWALT 14" 220V SERRA RAPIDO', [250, 168, 536, 472], cod_ref="D28730-B2", info="220V - 2300W | Eixo 25,4mm | 4.000 RPM | Disco 14 pol. (355mm) | Esquadria 0-45° | Corte a 90°: tubo quadrado 115 x 115mm", **_DW)
A(605, "6260142", 'FURADEIRA DEWALT 3/8" VVR 220V', [178, 576, 350, 804], info='600 watts | Mandril 3/8" (10mm) | 0 a 2.800 RPM | Perfuração: madeira 25 mm, aço 10 mm | 220 V', **_DW)
A(606, "6261622", 'FURADEIRA CHASSI DEWALT C/BASE MAGN 5/8" 220V', [31, 169, 252, 425], cod_ref="DWE1622K-B2", info='1200W | 300 a 450 rpm | Encaixe Weldon | Mandril 5/8" (16mm) | 2 velocidades | Profundidade 50mm | Fixação eletromagnética 17.000 N | Base 90 x 170 mm | 220V', **_DW)
A(606, "6261430", "BROCA ANULAR CHASSIS 14 X 30 / 16 X 30 BLACK E DECKER", [148, 452, 306, 518], marca="Black e Decker", info="Corte 14,00mm e 16,00mm | Fixação Weldon | Haste 19,00mm | HSS | Comprimento total 30mm | Corte 25mm | Também conhecida como broca copo para metal")
A(606, "6267220", 'LIXADEIRA ANGULAR 7" 2200W 220V', [22, 580, 376, 750], cod_ref="DWE493PW-B2", info="5500 RPM | 2200W | Discos de até 9\" (230mm) | Acompanha flange, disco de borracha e empunhadura lateral", **_DW)
A(607, "6261220", "FURADEIRA PARAFUSADEIRA IMPAC 1/2 20V", [271, 112, 567, 417], info='12 posições de torque | Torque máx. 45 Nm | 0-400 / 0-1550 RPM | Mandril 1/2" sem chave | Luz LED | Bateria 20V MAX | Acompanha 1 bateria 2,0Ah, carregador e maleta', **_DW)
A(607, "6264120", 'ESMERILHADEIRA ANG 4.1/2" 920W 220V G720X', [231, 533, 572, 723], cod_ref="G720XB2", info='220V | 920W | Disco 4-1/2" (115 mm) | 11.000 RPM | Acompanha empunhadura lateral, chave de aperto e guarda de proteção', **_DW)
NOTAS.append("Pág. 606: o código 6261430 está impresso para as duas brocas anulares (14 x 30 e 16 x 30); lançado uma vez com as duas medidas.")
# 608 (pág. impressa 607)
A(608, "6064150", "MAQUINA ELET. LONGA SOLTAR PORCA GRAMPO 7,5CV 161 CM", [108, 148, 504, 268], info="Cabeça com giro 360° | 5,5 Kw / 7,5 Cv | Torque máx. 5.000 Nm / 510 Kgf.m | 17 Rpm | 380 Volts (pode ser alterado para 220V por profissional) | 214,5 x 40 x 42,5 cm | Encaixe 1\" | 86 kg")
A(608, "6067530", 'CHAVE IMPACTO SIGMA 1" 1.500NM 2BAT 24V-6AH', [121, 483, 574, 697], marca="Sigma", info='Torque máx. 1.500 Nm (4 velocidades: 800, 1000, 1300, 1500) | 0-105 r/min | Bateria 24V | Encaixe 1" | 2 baterias de lítio')
# 609 (pág. impressa 608)
A(609, "6060539", 'CHAVE IMPACTO 200 KGF 1/2" SUPER TORK', [58, 91, 226, 256], marca="Super Tork", info="Carcaça em composite | Regulagem de torque em 3 níveis | Twin Hammer")
A(609, "9961804", 'CHAVE PNEUM 1" CURTA SIGMA', [404, 279, 529, 428], marca="Sigma", info='Carcaça em alumínio | 3 níveis de torque | Twin Hammer | 3.900 rpm | Encaixe 1" | Torque máx. 2024 ft.lbs / 279 kgf.m | 8,600 kg')
A(609, "6021266", "CHAVE PNEUM 1/2 IMP C/ 10 PÇS ROTA 66KGF", [386, 466, 519, 605], info="Entrada de ar 1/4\" | Encaixe 1/2\" | 7.000 Rpm | Torque 66 Kgf | 90 a 115 PSI | Soquetes 9, 10, 11, 13, 14, 17, 19, 22, 24, 27mm | Twin Hammer", **_RT)
A(609, "6021276", "CHAVE PNEUM 1/2 IMP ROTA 76KGF", [381, 648, 518, 787], info="Entrada de ar 1/4\" | Encaixe 1/2\" | 8.000 Rpm | Torque 76 Kgf | 90 a 115 PSI | Twin Hammer", **_RT)
# 610 (pág. impressa 609)
A(610, "6020012", "CHAVE PNEUM 1/2 IMP ROTA 80KGF", [114, 88, 245, 215], info="Entrada de ar 1/4\" | Encaixe 1/2\" | 8.000 Rpm | Torque 80 Kgf | 90 a 115 PSI | Twin Hammer", **_RT)
A(610, "9950012", "CHAVE PNEUM 1/2", [302, 88, 426, 206])
A(610, "9960655", "CHAVE PNEUM 3/4 REFORÇADA", [33, 225, 174, 355], marca="Schulz")
A(610, "6023400", "CHAVE PNEUM 3/4 RPM 4.300 200KGF", [302, 218, 414, 361], info="Entrada de ar 3/8\" | Encaixe 3/4\" | 4.300 Rpm | Torque 200 Kgf | 90 a 115 PSI | Twin Hammer", **_RT)
A(610, "9967000", 'CHAVE DE IMPACTO 3/4" TORQUE: 1.600 NM / 1.180 FT-LBS', [33, 390, 148, 516], info="Acompanha 4 soquetes longos CH 24, 27, 32 e 33mm | Para aperto de grampo de mola | 12 cfm | Entrada 3/8\" | 90 psi | 6,9 kg", **_SH)
A(610, "6031279", 'CHAVE IMPACTO POTENTE 1/2" PNEUMATICA 79,6KG', [408, 512, 563, 650], marca="Potente", cod_ref="PN120178 / 01.41.PN120178", info="8000 RPM | Torque 780 N.M (79,6 KgFM) | 85 a 113 PSI | Entrada 1/4 | 550 L/min | 2,69 Kg | Garantia de 6 meses")
A(610, "100463003", "CHAVE PNEUM 1/2 - 59 KGF TRAMONTINA PRO", [403, 658, 567, 802], marca="Tramontina Pro", info='Encaixe 1/2" | Entrada 1/4" NPT | 8000 rpm | Torque 570 N.m - 59 kg.f | Parafuso 5/8" | 90 psi | 142,5 l/min')
# 611 (pág. impressa 610)
A(611, "9961806", 'CHAVE DE IMPACTO 1"', [34, 129, 430, 310], info='Torque máx. 4.200Nm / 3.090 ft-lbs | 12 cfm | 90 psi | Entrada 1/2"', **_SH)
A(611, "60213200", 'CHAVE PNEUM 1" IMP ROTA 3200 RPM 320GF', [179, 329, 561, 491], info='Entrada de ar 1/2" | Encaixe 1" | 3200 Rpm | Mangueira 13mm | Torque 320 Kgf.M | 8-10 Kg/cm² | Vista explodida com 50 itens na página', **_RT)
A(611, "60214300", 'CHAVE PNEUM 1" CURTA ROTA 3400 RPM 200GF', [47, 620, 188, 798], info='Entrada de ar 3/8" | Encaixe 1" | 4.200 Rpm | Mangueira 11mm | Torque 200 Kgf | 90 a 115 PSI | Twin Hammer', **_RT)
NOTAS.append("Pág. 611: 60214300 é anunciado com 3400 RPM e a ficha técnica diz 4.200 Rpm.")
# 612-613 (págs. impressas 611-612)
A(612, "6025206", "DESTALONADOR DE PNEU PNEUM PORTATIL CAMINHAO", [275, 141, 566, 337], variacoes="5206", info="Aros 17,5 e 22,5 | Funciona com ar comprimido | Não recomendado para rodas com anel de proteção")
A(612, "6020273", "DESMONTADORA PNEUS MOVEL 220V", [269, 360, 548, 526], info="220V / 60 Hz | Motor 4 KW / 5.3 HP | Rodas de 10\" a 24\" | Largura máx. 330 mm | Diâmetro máx. 1000 mm | 6 RPM | Torque 3200 NM | 109 KG | Pneus 11R22.5 / 12R22.5 / 13R22.5")
A(613, "6021232", "DESMONTAGEM PNEU KIT ESPATULAS 2 PECAS", [78, 410, 359, 494])
GP(613, 5, "MARRETA COM CABO", [("6011503", "MARRETA 02KG COM CABO"), ("6018553", "MARRETA 05KG COM CABO")], [54, 512, 258, 706])
P(613, "@449", "MARTELO DE MADEIRA BORRACHARIA", [291, 672, 556, 781], info="Código impresso como '@449'")
