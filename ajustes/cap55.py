# Capítulo 55 - Ferramentas Manuais e Abrasivos (págs. 569-582)
# Listas por caixa: cada caixa (seção) = 1 produto com os códigos como itens; código+descrição via tabela_livre.ler_pagina,
# seções dadas à mão (retângulos pelas bordas das molduras); foto = maior imagem da seção.
import re

from tabela_livre import _spans, ler_pagina

TIPOS = []
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(569, 583))
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


TIPOS += [(r"^CH PHILLIPS|^CH FENDA|CHAVES? FENDA", "CHAVE DE FENDA / PHILLIPS"), (r"ESTILETE", "ESTILETE"), (r"TRENA", "TRENA"), (r"SOQUETE|SOQ ", "JOGO DE SOQUETES"), (r"DISCO|REBOLO", "DISCO ABRASIVO"),
          (r"LANTERNA", "LANTERNA"), (r"SOPRADOR", "SOPRADOR TÉRMICO"), (r"LIXA", "LIXA"), (r"REBITE", "REBITE"), (r"REBITADOR", "REBITADOR"), (r"ALICATE", "ALICATE"), (r"MULTIMETRO|MULTÍMETRO", "MULTÍMETRO"),
          (r"FITA", "FITA"), (r"FURADEIRA", "FURADEIRA"), (r"COMPRESSOR", "COMPRESSOR"), (r"CAIXA", "CAIXA DE FERRAMENTAS"), (r"MANIPULO", "MANÍPULO"), (r"SERRA COPO", "SERRA COPO"), (r"LAMINA", "LÂMINA DE SERRA"),
          (r"ARCO", "ARCO DE SERRA"), (r"PAQUIMETRO", "PAQUÍMETRO"), (r"BROCA", "BROCA"), (r"DESINGRIPANTE", "DESENGRIPANTE"), (r"CHAVE", "CHAVE")]
_ST, _TR, _GE, _GR, _MI = dict(marca="Stanley"), dict(marca="Tramontina"), dict(marca="Gedore"), dict(marca="Gedore Red"), dict(marca="Minipa")
_SR, _MX, _CO, _SA = dict(marca="Starrett"), dict(marca="MTX"), dict(marca="Corneta"), dict(marca="Mayle")
NOTAS.append("Pág. 569: divisória de ferramentas.")
# 570 (pág. impressa 569)
LS(570, 1, "CHAVE PHILLIPS EMBORRACHADA", [25, 88, 570, 343], [50, 140, 244, 308], **_ST)
LS(570, 2, "CHAVE FENDA EMBORRACHADA", [25, 343, 570, 659], [72, 391, 190, 637], **_ST)
A(570, "6013072", "JOGO CHAVES FENDA PHILLIPS 6PÇ", [28, 660, 178, 803], info="Fenda: SL 4x100mm, SL 5x100mm, SL 6x150mm | Phillips: PH 0x80mm, PH 1x100mm, PH 2x150mm")
# 571 (pág. impressa 570)
A(571, "6019540", "ESTILETE 18MM EMBORRACHADO", [29, 120, 275, 190])
A(571, "6019541", "ESTILETE 18MM PLASTICO C/PONTA DE METAL", [51, 195, 275, 257])
A(571, "6018018", "LAMINA ESTILETE 18MM TUBETE C/10", [374, 190, 514, 263])
A(571, "6013891", "TRENA 5MTS EMBORRACHADO", [29, 322, 223, 454])
A(571, "6260632", "JG SOQUETE 1/2 22 PECAS 06MM A 32MM ESTRIADO", [425, 330, 566, 478], info='18 soquetes estriados com encaixe de 1/2": 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 24, 27, 30, 32mm | 01 cabo T de 10" | 01 extensão de 5" | 01 extensão de 10" | Catraca 10"', **_ST)
A(571, "6260516", "DISCO CORTE FINO METAL INOX DE 12 X 3.0MMX5/8", [34, 482, 144, 586], info="Grãos abrasivos selecionados, cortes rápidos e pouca perda de material | Duas telas de fibra de vidro", **_ST)
A(571, "6017085", "LANTERNA RECAR 9 LEDS BIVOLT LRV225 VD", [291, 640, 570, 811], info="Modelo LRV 225 | 100 V~ a 240 V~ automático | Plástico ABS | Lente 57,5 mm | Comprimento 220 mm | 54 lm | Carga 12 horas | Autonomia 5 leds: 12h, 9 leds: 8h | Alcance 70 metros | Preta")
A(571, "6020220", "SOPRADOR TERMICO 2000W 220V", [164, 660, 299, 789], info="Acompanha bocal plano, de desvio, de ponta e de deflexão | 3 estágios: 80 W 50 ºC 500 L/min; 1.000 W 350 °C 300 L/min; 2.000 W 550 °C 500 L/min | 60 Hz | ABNT NBR IEC 60335-1 e IEC 60335-2-45")
NOTAS.append("Pág. 571: o soprador 6020220 é anunciado como 220V e a especificação do card diz 'Tensão: 110V'.")
# 572 (pág. impressa 571)
LS(572, 1, "LIXA D'AGUA NORTON", [25, 88, 570, 323], [28, 94, 210, 281], marca="Norton")
LS(572, 2, "LIXA FERRO NORTON", [25, 323, 570, 532], [35, 332, 216, 519], marca="Norton")
_FL = "Flap de fibra cônico 4.1/2\" | Utilizados em lixadeiras e esmerilhadeiras angulares para desbastes de soldas, rebarbação"
A(572, "9734000", "DISCO DE LIXA FLAP DESBAST NORTON P40", [34, 554, 193, 706], cod_ref="R801 115 X 22,23 P040", info=_FL, marca="Norton")
A(572, "9736000", "DISCO DE LIXA FLAP DESBAST NORTON P60", [316, 560, 472, 708], cod_ref="R801 115 X 22,23 P060", info=_FL, marca="Norton")
# 573 (pág. impressa 572)
LS(573, 1, "REBITE POP DE ALUMINIO", [25, 88, 570, 456], [43, 145, 227, 450])
A(573, "62669800", "REBITADOR MANUAL", [79, 465, 435, 633], **_ST)
A(573, "6010045", "REBITADOR TIPO ALAVANCA MANUAL", [59, 642, 536, 770], info="Lançamento")
# 574 (pág. impressa 573)
A(574, "9931001", "ALICATE PRESSAO 10'' GEDORE RED", [32, 96, 211, 165], **_GR)
A(574, "6219839", "ALICATE UNIVERSAL 8\" MTX CABO DUPLA INJECAO", [308, 94, 542, 183], **_MX)
A(574, "6028622", "JG CHAVE FIXA 06 A 22MM 08 PCS", [35, 220, 175, 333], info="1 chave 6x7, 8x9, 10x11, 12x13, 14x15, 16x17, 18x19 e 20x22", **_MX)
A(574, "6090712", "JG SOQ TORX 1/2 7PÇ", [332, 253, 537, 340], info="Aço cromo vanádio | Medidas: T20, T25, T30, T40, T45, T50, T55", **_CO)
A(574, "6011972", "JOGO CHAVE TORX T10 A T50 LONGA", [39, 393, 157, 543], **_CO)
A(574, "6011510", "JOGO CHAVE ALLEN 1,5 MM A 10 MM LONGA", [300, 425, 437, 539], **_CO)
A(574, "6213055", "ALICATE RETO MTX PARA ANEIS INTERNO 6\" 150MM", [69, 585, 234, 641], **_MX)
A(574, "6018887", "JOGO ALICATES ANÉIS INTERNOS E EXTERNOS DE 7 POL. COM 4 PEÇAS", [387, 578, 557, 750], info="Alicate para anéis interno e externo bico reto de 7\"; interno e externo bico curvo de 7\"")
A(574, "9941580", "REBITADOR PNEUMATICO 1/4 INDUSTRIAL", [143, 647, 291, 793], marca="Corneta", info="Rebitadeira 27 x 16 x 7,8cm | 4 bicos | 2 chaves | 1 niple | Pressão 90 Psi | Consumo 4 Pcm | Entrada 1/4\" NPT | Mangueira 3/8\" | Rebites de 1/8\" a 1/4\"")
# 575 (pág. impressa 574)
A(575, "9963144", "MULTIMETRO DIGITAL ET.1002", [181, 131, 287, 273], info="CAT I 600 V | 3 1/2 dígitos | Tensão AC/DC até 600 V | Corrente DC 10 A | Resistência 2000 kΩ | Teste de diodo, continuidade e transistor | Alimentação 1 x 9 V | 0,130 kg", **_MI)
A(575, "9961611", "MULTIMETRO DIGITAL ET-1110B", [304, 97, 389, 242], info="Corrente AC/DC, tensões AC/DC, resistência, temperatura, diodo, continuidade e hFE | Desligamento automático, data HOLD e NCV | IEC61010 CAT II 600V | 140 x 72 x 37 mm | Aprox. 195 g", **_MI)
A(575, "9963880", "MULTÍMETRO DIGITAL ET-1000, MINIPA", [33, 280, 167, 410], info="CAT I 600V | 3 1/2 dígitos | Tensão AC/DC até 600 V | Corrente DC 10 A | Resistência 2000 kΩ | Alimentação 1 x 9 V | 0,150 kg", **_MI)
A(575, "9920294", "GED ALICATE UNIVERSAL", [39, 426, 243, 493], **_GE)
A(575, "9821920", "FITA ISOLANTE 20MTS 3M SCHOTCH 33+", [299, 431, 416, 545], marca="3M")
A(575, "9931032", "GED RED JG SOQUETE ESTRIADO 1/2 08 A 32", [37, 557, 244, 797], info="18 soquetes estriados de 8 a 32 mm | 2 extensões 125 mm e 250 mm | 1 cabo T e 1 catraca reversível | Maleta plástica | Aço cromo-vanádio", **_GR)
# 576 (pág. impressa 575)
_J22 = '22 peças | Aço cromo vanádio | Encaixe de 1/2" | 1 extensão 5", 1 extensão 10", 1 catraca reversível, 1 cabo T 10", 18 soquetes '
P(576, "10019122", "JOGO SOQUETE 1/2 22 PEÇAS ESTRIADO", [387, 90, 554, 255], info=_J22 + "estriados: 8 a 32 mm", marca="Tramontina Pro")
A(576, "10019204", "JOGO SOQUETE 1/2 22 PEÇAS SEXTAVADO", [375, 275, 566, 458], info=_J22 + "sextavados: 8 a 32 mm", marca="Tramontina Pro")
A(576, "10022390", 'MALETA SOQUETES E ACESS. 1/2" 22P PRO', [32, 467, 189, 637], info="18 soquetes estriados de 8 a 32mm, 2 extensões, cabo T, catraca reversível e maleta plástica | 7,5 x 23,5 x 30,5 cm", marca="Tramontina Master")
A(576, "6010004", 'ALICATE CORTE DIAGONAL 6"', [397, 477, 539, 719])
# 577 (pág. impressa 576)
LS(577, 1, "CHAVE FIXA TRAMONTINA MASTER", [25, 88, 298, 440], [37, 142, 295, 207], **_TR)
LS(577, 2, "CHAVE BIELA TRAMONTINA MASTER", [298, 88, 570, 440], [322, 145, 536, 230], desc={"10017848": "CHAVE BIELA 12MM 42805/112"}, **_TR)
LS(577, 3, "CHAVE COMBINADA TRAMONTINA MASTER", [25, 440, 298, 805], [37, 488, 293, 540], **_TR)
LS(577, 4, "CHAVE ESTRELA TRAMONTINA MASTER", [298, 440, 570, 805], [300, 505, 556, 554], **_TR)
NOTAS.append("Pág. 577: 10017848 está impresso como '100.17848'.")
# 578 (pág. impressa 577)
_FI = "Com sistema de reversão de rotação"
A(578, "101440961", "CHAVE P/FILTRO 3 GARRA 63-120 TRAMONTINA PRO", [86, 96, 193, 215], **_TR)
A(578, "10142630", 'FURADEIRA IMPACTO TRAMONTINA 3/8" 500W127V', [229, 92, 380, 225], info=_FI, **_TR)
A(578, "10142362", 'FURADEIRA IMPACTO TRAMONTINA 1/2" 220V - 500W C/SUP', [410, 87, 565, 235], info=_FI, **_TR)
A(578, "10144110", "JG CHAVE FENDA 05 PECAS TRAMONTINA PRO", [100, 272, 197, 411], info="Fenda: 5x100mm, 3x75mm, 6x125mm | Phillips: 5x100mm, 6x125mm", **_TR)
A(578, "10142361", 'FURADEIRA IMPACTO TRAMONTINA 3/8" 500W 220V', [230, 273, 381, 406], info=_FI, **_TR)
A(578, "10142363", 'FURADEIRA IMPACTO TRAMONTINA 1/2" 127V - 500W C/SUP', [422, 272, 567, 406], info=_FI, **_TR)
A(578, "10142331", "COMPRESSOR PORTATIL TRAMONTINA 300PSI 50W 12V", [32, 457, 198, 582], info="50 W | 12 V | 300 Psi | Vazão 8 l/min | Mangueira de 45 cm | Ponteiras adaptadoras para bolas e boias", **_TR)
A(578, "10144950", "CAIXA FERRAMENTAS 5 COMPARTI. TRAMONTINA PRO", [333, 457, 556, 644], info="Caixa com 5 gavetas, alças dobráveis, alça e rodas | 60 peças: alicates, cabo T, catraca, chaves combinadas, de fenda, hexagonais, extensões, martelo e 18 soquetes estriados 1/2\" | 580 x 220 x 320 mm", **_TR)
LS(578, 9, "CHAVE MEIA LUA", [25, 716, 297, 805], [37, 712, 138, 780], **_TR)
A(578, "101447420", "MANIPULO CH RODA 19 X 600 TRAMONTINA", [305, 732, 565, 756], **_TR)
# 579 (pág. impressa 578)
A(579, "6200300", "DESINGRIPANTE STARRETT MULTIUSO 300ML", [36, 92, 207, 217], **_SR)
A(579, "6201218", "LAMINA SERRA STARRET 12 X 18", [227, 90, 362, 220], **_SR)
A(579, "6200058", 'SERRA COPO STARRETT CORTE RAP 5/8" - (15,8MM)', [409, 159, 560, 201], **_SR)
A(579, "6200100", 'SERRA COPO STARRETT CORTE RAPIDO 1" - (25MM)', [35, 262, 90, 370], **_SR)
A(579, "6200134", 'SERRA COPO STARRETT CORTE RAP 1.3/4" - (44MM)', [160, 289, 208, 346], **_SR)
A(579, "6200114", 'SERRA COPO STARRETT CORTE RAP 1.1/4" - (32MM)', [300, 289, 345, 346], **_SR)
A(579, "6201916", "SERRA COPO 40MM (1.6/16) STARRET CORTE RAPIDO", [435, 289, 497, 378], **_SR)
GP(579, 4, "BROCA STARRETT", [("6200500", 'BROCA STARRETT P/CONCRETO 5,00MM-3/16"'), ("6200650", 'BROCA STARRETT P/CONCRETO 6,50MM-1/4"'), ("6200120", "BROCA STARRETT ACO RAPIDO 12,00MM"), ("6200012", 'BROCA STARRETT ACO RAPIDO 1/2"')],
   [35, 382, 293, 544], **_SR)
A(579, "6200140", 'ARCO STARRETT SERRA C/LAMINA 12"', [322, 382, 539, 478], **_SR)
A(579, "6206150", "PAQUIMETRO STARRETT MANUAL INOX 150 X 0,05MM", [323, 529, 534, 592], cod_ref="125MEB-6/150", **_SR)
A(579, "6201230", "PAQUIMETRO STARRETT MANUAL INOX 300 X 0,05MM", [54, 654, 559, 800], cod_ref="125MEB-12/300", **_SR)
# 580 (pág. impressa 579)
LS(580, 1, "BROCA ACO RAPIDO GOLD", [25, 130, 375, 391], [32, 146, 58, 370], desc={"6260916": "BROCA GOLD ACO BLACK E DECKER G 9/16"}, marca="Dewalt")
A(580, "6260650", "BROCA GOLD ACO BLACK E DECKER 06,50MM", [401, 111, 548, 282], **_ST)
GP(580, 2, "BROCA STARRETT", [("6200500", 'BROCA STARRETT P/CONCRETO 5,00MM-3/16"'), ("6200650", 'BROCA STARRETT P/CONCRETO 6,50MM-1/4"'), ("620120", "BROCA STARRETT ACO RAPIDO 12,00MM"),
                           ("6200120", "BROCA STARRETT ACO RAPIDO 12,00MM"), ("6200012", 'BROCA STARRETT ACO RAPIDO 1/2"')], [30, 401, 87, 592], **_SR)
LS(580, 3, "BROCA ACO RAPIDO IRWIN", [25, 603, 395, 805], [34, 658, 353, 684], desc={"6274019": "BROCA ACO RAPIDO 18MM IRWIN / 10MM IRWIN COBERTURA TITANIO"}, marca="Irwin")
A(580, "6274049", "BROCA ACO RAPIDO 05MM IRWIN COBERTURA TITANIO", [375, 542, 567, 739], marca="Irwin")
NOTAS.append("Pág. 580: 620120 (6 dígitos) e 6200120 são a mesma broca Starrett 12,00mm impressa nas duas listas; 6274019 está impresso como broca 18MM Irwin e como broca 10MM Irwin cobertura titânio.")
# 581 (pág. impressa 580)
for _c, _d, _i in [("6201151", "DISCO DE CORTE AÇO", '4-1/12x3/64x7/8" | 115x1,0x22,2mm'), ("6268061", "DISCO DE CORTE INÓX", '4-1/2x1/25x7/8" | 115x1,0x22mm'), ("6260413", "DISCO DESBASTE ABRASIVO METAL", '4-1/2x1/4x7/8" | 115x22,23mm'),
                   ("9734000", "DISCO DE LIXA FLAP DESBASTE NORTON P040", '4x1/2x7/8" | 115x22,23mm'), ("9736000", "DISCO DE LIXA FLAP DESBASTE NORTON P060", '4x1/2x7/8" | 115x22,23mm'),
                   ("9736662", "DISCO CORTE DE AÇO NORTON", '4.1/2x3/64x7/8" | 115x1,0x22,23mm'), ("6201842", "DISCO DE CORTE AÇO", '7x1/16x7/8" | 178x1,6x22,2mm'), ("6260414", "DISCO DE DESBASTE ABRASIVO METAL", '7x1/4x7/8" | 180x6x22mm'),
                   ("6268067", "DISCO DE CORTE INÓX", '7x1/16x7/8" | 180x1,6x22mm'), ("9736673", "DISCO CORTE DE AÇO NORTON", '7x1/16x7/8" | 180x1,6x22,2mm'), ("6260516", "DISCO DE CORTE INÓX", '12x1/8x5" | 300x3,0x15,9mm'),
                   ("6203035", "DISCO DE CORTE AÇO", '12x1/8x1" | 300x3,2x40mm'), ("9734655", "REBOLO DESBAST A60 ACO", '6x3/4x1 1/4" | 152,4 x 19 x 31,75mm'), ("6268308", "DISCO DE LIXA FLAP DESBAST RETO DW8308 P060", '4" x1/2" x 7/8" | 115 x 22mm')]:
    A(581, _c, _d, info=_i)
A(581, "6201842", "DISCO STARRETT CORTE", [192, 541, 266, 616], info='7" x1/16" x 7/8" | 178 x 1,6 x 22,23mm', **_SR)
NOTAS.append("Pág. 581: 6201842 está em dois cards (disco de corte aço e disco Starrett corte, mesma medida); 6260516 também aparece na pág. 571 com medida 12 x 3.0mm x 5/8.")
# 582 (pág. impressa 581)
A(582, "9939644", "GED RED JG CHAVE BIELA L", [28, 93, 293, 236], info="Encaixes sextavados | 12 peças: 8 a 19mm", **_GR)
A(582, "9932104", 'GED RED JOGO ALICATE ANÉIS INT E EXT DE 7"', [334, 92, 538, 259], **_GR)
A(582, "6011415", "JG CHAVE FIXA 6 A 32MM", [36, 321, 286, 510], **_SA)
A(582, "6020622", "JG CHAVE COMB 06 A 22MM 12PCS", [326, 321, 548, 526], **_SA)
A(582, "6020632", "JG CHAVE COMB 06 X 32MM.", [60, 596, 263, 750], **_SA)
A(582, "6011577", "JG CHAVE ESTRELA 6 A 32", [312, 588, 563, 733], **_SA)
