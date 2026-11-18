# Capítulo 60 - Macacos, Prensas e Equipamentos de Oficina (págs. 624-633)
# Listas por caixa: cada caixa (seção) = 1 produto com os códigos como itens; código+descrição via tabela_livre.ler_pagina,
# seções dadas à mão (retângulos pelas bordas das molduras); foto = maior imagem da seção.
import re

from tabela_livre import _spans, ler_pagina

TIPOS = []
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(624, 634))
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


TIPOS += [(r"CARRINHO", "CARRINHO"), (r"MACACO", "MACACO HIDRÁULICO"), (r"MARTELETE", "MARTELETE PNEUMÁTICO"), (r"CHAVE IMPACTO", "CHAVE DE IMPACTO"), (r"BOMBA", "BOMBA"), (r"REPARO", "REPARO DE MACACO"), (r"EXPANSOR", "EXPANSOR HIDRÁULICO"),
          (r"PRENSA", "PRENSA HIDRÁULICA"), (r"GIRAFA", "GIRAFA"), (r"CAVALETE", "CAVALETE"), (r"ARQUEAR", "MÁQUINA DE ARQUEAR MOLAS"), (r"REBITADEIRA", "REBITADEIRA"), (r"PUNCAO", "PUNÇÃO"),
          (r"SACA|SACADOR|VARAO", "SACADOR HIDRÁULICO")]
_PT, _RN, _BV, _HD, _RS = dict(marca="Potente"), dict(marca="Rino"), dict(marca="Bovenau"), dict(marca="Hidraumon"), dict(marca="Riosul")
# 624 (pág. impressa 623)
A(624, "9961805", "CARRINHO P PNEUMATICA 1''", [292, 172, 561, 430], cod_ref="CAR-10", marca="Sigma",
  info='Carrinho ergonômico para chave de impacto 1" | Aço | Suporta até 25kg | Elo regulador de tensão da mola | Peso 20kg | Embalagem 19 x 55 x 65 cm | Chave de impacto não inclusa, foto ilustrativa')
# 625 (pág. impressa 624)
A(625, "6033200", "MACACO GARRAFA POTENTE 32 TON", [312, 116, 546, 356], **_PT)
A(625, "6031279", 'CHAVE IMPACTO POTENTE 1/2" PNEUMATICA 79,6KG', [319, 403, 493, 558], cod_ref="PN120178 / 01.41.PN120178", info="8000 RPM | Torque 780 N.M (79,6 KgFM) | 85 a 113 PSI | Entrada 1/4 | 550 L/min | 2,69 Kg | Garantia de 6 meses", **_PT)
A(625, "6030150", "MARTELETE PNEUMATICO 150MM", [224, 616, 565, 800], info="Cortar, perfurar, lascar ou raspar superfícies metálicas | Reparação automotiva", **_PT)
# 626 (pág. impressa 625)
LS(626, 1, "MACACO GARRAFA OFICINA RINO", [21, 96, 574, 352], [373, 106, 569, 343], **_RN)
A(626, "6011500", "MACACO JACAREZINHO 2T RINO", [272, 412, 561, 590], **_RN)
A(626, "6011724", "BOMBA GRAXA 400 GR", [27, 621, 343, 797])
# 627 (pág. impressa 626)
A(627, "5983250", "MACACO MOLEIRO 32 TON 500MM HIDROP P/OFICINA", [38, 105, 121, 249], cod_ref="MMP32500", info="Hidropneumático (manual e ar) para postos de molas | 32 toneladas | Consumo 10 PCM | Óleo 32W | Compressor indicado 10 pés/175 lbs | Garantia 1 ano | Modelos: MMP32400, MMP32500, MMP32600, MMP32700", **_HD)
A(627, "5986900", "JG REPARO MACACO (5980695/5983250)", [395, 281, 558, 402], **_HD)
A(627, "5980695", "MACACO MOLEIRO 32 TON 500MM P/OFICINA", [51, 290, 134, 435], info="32 toneladas | Injeção manual c/ 2 injetores | Base de aço A36 | Altura 536mm | Curso 370mm | 32kg", **_HD)
A(627, "5985051", "MACACO MOLEIRO 50 TON 500MM HIDROP P/OFICINA", [43, 441, 279, 794], **_HD)
A(627, "5985050", "MACACO MOLEIRO 50 TON 500MM P/OFICINA", [338, 447, 560, 799], **_HD)
# 628 (pág. impressa 627)
A(628, "5980129", "EXPANSOR DUPLA ACAO 30 TONELADAS", [223, 124, 565, 356], info="Expansor e encolhedor 30 ton de expansão e 15 ton de tração | Bomba manual 700 bar | Pistão 500mm | Curso 250mm | Altura total 740mm | Mangueiras 2m | Óleo 32W | 45kg", **_HD)
NOTAS.append("Pág. 628: o expansor 5980129 é anunciado com 30 ton de expansão e 15 de tração, mas o descritivo técnico diz 20 toneladas de avanço e 10 de retorno.")
A(628, "5980032", "MACACO GAR HDM REFORCADO 32T P/OFICINA", [27, 464, 262, 610], info="32 toneladas | Altura fechado 250mm | Curso 140mm | Fuso 80mm | Altura total 470mm | 18kg | Garantia 1 ano", **_HD)
A(628, "5980462", "JG REPARO MACACO (5980032/5980696)", [400, 636, 566, 765], **_HD)
A(628, "5980696", "MACACO HIDROPNEUMATICO HDM REFO 32T P/OFICINA", [31, 631, 136, 804], info="32 toneladas | Altura fechado 250mm | Curso 140mm | Fuso 80mm | Altura total 470mm | Consumo 10 PCM | 21kg | Garantia 1 ano", **_HD)
# 629 (pág. impressa 628)
LS(629, 1, "MACACO GARRAFA R P/OFICINA", [25, 88, 360, 240], [49, 244, 341, 367])
A(629, "6023200", "MACACO HIDROPNEUMATICO R 32 TON P/OFICINA", [393, 231, 531, 369])
A(629, "6080060", "PRENSA 60TON MARCON", [149, 459, 321, 677], cod_ref="MPH-60", marca="Marcon", info="60 toneladas | 396 Kg | 1295 x 750 x 1646 mm | Distância mesa/pistão 81 a 641 mm | Curso do pistão 140 mm | Com manômetro")
A(629, "5980302", "PRENSA 30TON HIDRAU. MANUAL HIDRAUMON", [461, 487, 561, 723], cod_ref="Hidraumon 00302", info="Modelo P30 | Amarelo | Força 30 t | Área de trabalho 18 x 65 cm | Altura total 140 cm", **_HD)
# 630 (pág. impressa 629)
A(630, "6003043", "MACACO HIDRAUL BAIXO BOVENAU 30 TON P/OFICINA", [26, 94, 148, 238], info="30 ton | Altura fechado 165mm | Curso 70mm | Fuso 40mm | Aberto 275mm | Base 170x185mm | Alavanca 600mm | 12KG", **_BV)
A(630, "6013910", "MACACO GARRAFA 50 TONELADAS", [419, 91, 568, 236], cod_ref="R070032", info="50 toneladas | Altura 285mm | Base 180x220mm | Curso 180mm | Altura total 465mm", **_RS)
A(630, "6003110", "MACACO MOLEIRO BOVENAU MTM-30T", [33, 238, 98, 370], cod_ref="MTM-30T", info="30 ton | Altura fechado 800mm | Curso 500mm | Fuso 40mm | Base 170x185mm | Alavanca 600mm", **_BV)
A(630, "6013915", "BOMBA DE GRAXA 16 KG MANUAL", [300, 240, 408, 364], info="16 L | Pressão máx. 3.000 psi | Inclui mangueira | Portátil", **_RS)
A(630, "6001001", "PRENSA HIDRÁULICA DE 10 TON C/ MANÔMETRO", [140, 373, 297, 561], cod_ref="P10000", info="Pistão com retorno automático | Válvula de sobrecarga | Altura 702 mm | 33 Kg | 35 x 53 x 70,2 cm", **_BV)
A(630, "6001501", "PRENSA 15 TON", [430, 376, 568, 564], **_BV)
A(630, "6000003", "PRENSA 30TON BOVENAU", [173, 608, 294, 798], info="30 ton | Altura 1570mm | Hidráulico/mesa 115 a 830mm | Entre colunas 585mm | 815 x 540mm | Curso 125mm | Fuso 85mm | 137kg", **_BV)
A(630, "6000060", "PRENSA 60TON BOVENAU", [387, 618, 569, 804], **_BV)
NOTAS.append("Pág. 630: 6003110 tem altura total aberto impressa como 275mm, menor que a altura fechado (800mm).")
# 631 (pág. impressa 630)
A(631, "6001002", "GIRAFA COM REGULAGEM 1 TON", [31, 151, 295, 395], info="Braço recuado 1544 mm, aberto 2144 mm | Altura 1754 mm | Comprimento 2100 mm | Entre rodas 829 mm", **_BV)
A(631, "6002003", "GIRAFA BOVENAU 2 T REFORCADA", [306, 157, 547, 380], **_BV)
A(631, "6002100", "MACACO HID. JACARE 2 GRD J2", [32, 427, 238, 617], info="2 toneladas | 1200 x 414mm | Puxador 1060mm | Altura 124 a 550mm | Trava de segurança e rodas de ferro", **_BV)
A(631, "6002002", "CAVALETE 2T PAR REFORCADO CT20", [175, 623, 291, 798], **_BV)
A(631, "6003003", "GIRAFA BOVENAU 3 T REFORCADA", [306, 492, 546, 795], info="3000kg | Roda de ferro | 2165 x 1780mm | Braço 1682/2282mm | Entre pernas 855mm | Solo 1082 a 3042mm | 230KG", **_BV)
# 632 (pág. impressa 631)
A(632, "5985020", "MAQUINA ARQUEAR MOLAS UNIVERSAL 50 TONELADAS", [25, 118, 396, 423], info="Universal 2 em 1 | 2 pedais | 2 jogos de sapatas | Motor trifásico 220V/380V | 50 toneladas | 1200 x 500 x 500mm | Curso 160mm | Haste 4\" | Óleo 68w / 20 litros | 330kg | Garantia 1 ano", **_HD)
A(632, "5980690", "REBITADEIRA PNEUMATICA LONA FREIO", [436, 437, 564, 695], info="Rebitar e sacar todos os tipos de lonas de freio | Hidropneumático | 8 BAR | 1450 x 330 x 550mm | Curso 32mm | 110 kg | Garantia 1 ano", **_HD)
A(632, "5981009", "JG PUNCAO P/REBITADEIRA DE LONA FREIO 3 PCS", [33, 703, 288, 802], info="116MM", **_HD)
# 633 (pág. impressa 632)
A(633, "5983030", "SACADOR DE BUCHA PARA SUSPENSÃO 35 TON", [198, 142, 523, 372], info="Sacar e posicionar buchas de suspensões hidropneumáticas de caminhões e ônibus | 35 ton | 30 KG", **_HD)
A(633, "5983031", "VARAO ROSCA SACA BUCHA (5983030) SUSP 35TON", [40, 410, 556, 437], **_HD)
A(633, "5981021", "SACA TERMINAL PNEUMATICO", [317, 448, 558, 566], **_HD)
A(633, "5980199", "SACA PINOS MANGA DE EIXO HIDROPNEUMÁTICA 50 TON", [24, 577, 269, 802], info="Sacar pinos manga de eixo diretamente no veículo | 50 toneladas | Altura 700mm | Entre colunas 290mm | Curso 130mm | Hidropneumático/manual | 65 kg", **_HD)
