# Capítulo 34 - Elétrica - Lâmpadas, LEDs e Lanternas (págs. 410-417)
# Páginas de layout livre (cards mesclados): registros montados à mão a partir da imagem; foto = imagem mais próxima do código.
import re

from tabela_livre import _spans

TIPOS = [(r"^LED LUMENS|^LED ", "LÂMPADA LED"), (r"^LAMPADA LED", "LÂMPADA LED"), (r"^LAMPADA", "LÂMPADA"), (r"^LANT", "LANTERNA"), (r"^FAROL", "FAROL"), (r"^SUPORTE", "SUPORTE"), (r"^GIRO", "GIROFLEX"), (r"^TERMINAL", "TERMINAL"), (r"^CAPA", "CAPA DE TERMINAL"), (r"^FITA", "FITA ISOLANTE"), (r"^SOQ", "SOQUETE"),
         (r"^CHICOTE", "CHICOTE"), (r"^CON\.", "CONECTOR"), (r"^RELE", "RELÉ"), (r"^BOT[ÃA]O", "BOTÃO"), (r"^CHAVE", "CHAVE"),
         (r"^PORTA FUSIVEL", "PORTA FUSÍVEL"), (r"^FUSIVEL|^PORTA (MINI|LAMINA|MAX|VIDRO)", "FUSÍVEL"), (r"^CABO", "CABO"),
         (r"^GARRA", "GARRA DE BATERIA"), (r"^FIO", "FIO"), (r"^SIRENE|^ALARME", "SIRENE"), (r"^MB SOQUETE", "SOQUETE")]
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(410, 418))
_CACHE = {}
_NCOL = {}  # colunas de cards por página (padrão 3)


def _pag(p):
    if p not in _CACHE:
        _CACHE[p] = _spans(p)
    return _CACHE[p]


def _foto(p, cod, min_area=500, acima_primeiro=False):
    sp, imgs = _pag(p)
    ss = [s for s in sp if s["t"].replace(" ", "").strip() == cod] or [s for s in sp if cod in s["t"].replace(" ", "")]
    if not ss:
        return None
    s = ss[0]
    cx, cy = (s["x"] + s["x1"]) / 2, s["y"]
    w = 545 / _NCOL.get(p, 3)
    col = int((cx - 25) // w)
    cand = [b for b in imgs if (b[2] - b[0]) * (b[3] - b[1]) >= min_area and int(((b[0] + b[2]) / 2 - 25) // w) == col]
    if not cand:
        return None
    # imagens entre este código e o próximo código vermelho da mesma coluna (foto abaixo); senão, acima
    outros = [t["y"] for t in sp if t["red"] and re.fullmatch(r"\d{7,9}", t["t"].replace(" ", "")) and t is not s
              and int(((t["x"] + t["x1"]) / 2 - 25) // w) == col]
    prox = min([y for y in outros if y > cy + 5], default=900)
    ant = max([y for y in outros if y < cy - 5], default=0)
    abaixo = [b for b in cand if cy - 15 <= (b[1] + b[3]) / 2 < prox]
    acima = [b for b in cand if ant < (b[1] + b[3]) / 2 < cy]
    cand = (acima or abaixo or cand) if acima_primeiro else (abaixo or acima or cand)
    b = min(cand, key=lambda b: abs((b[0] + b[2]) / 2 - cx) + abs((b[1] + b[3]) / 2 - cy))
    return {"rect": [round(v, 1) for v in b]}


def R(p, cod, desc, card=None, foto=None, acima=False, **kw):
    r = dict(pagina=p, card=card or (len(ADD) + 1), codigo=cod, descricao=desc, cod_ref="", variacoes="", aplicacao="", info="",
             marca="", montadora="", _nao_agrupar=card is None)
    r.update(kw)
    r["foto_spec"] = {"rect": foto} if foto else _foto(p, cod, acima_primeiro=acima)
    ADD.append(r)
    return r


def G(p, card, titulo, itens, foto=None, **kw):
    """Card com vários códigos = 1 produto (itens = [(código, descrição)])."""
    for c, d in itens:
        R(p, c, d, card=card, foto=foto, _titulo=titulo, **kw)


# 410 (pág. impressa 409): kits LED (um card por linha; códigos por tipo de base)
G(410, 1, "LED LUMENS 11.000 SLIM 50W 12/24", [("7331124", "LED LUMENS 11.000 H11 SLIM 50W 12/24"),
                                              ("7330324", "LED LUMENS 11.000 H3 SLIM 50W 12/24"),
                                              ("7330424", "LED LUMENS 11.000 H4 SLIM 50W 12/24"),
                                              ("7330724", "LED LUMENS 11.000 H7 SLIM 50W 12/24")],
  foto=[394, 95, 547, 211], info="Tonalidade: 6.000K | Eficiência: 11.000 lúmens | Potência: 50W par | Resistência: IP67 | "
                                 "Voltagem: 12/24V | Duplo CSP | Chip de cobre | Com canceller | Obs: par")
G(410, 2, "LED LUMENS 8.400 SMALL 45W 12/24V", [("7330124", "LED LUMENS 8.400 H1 SMALL 45W 12/24V"),
                                               ("7332411", "LED LUMENS 8.400 H11 SMALL 45W 12/24V"),
                                               ("7332403", "LED LUMENS 8.400 H3 SMALL 45W 12/24"),
                                               ("7332404", "LED LUMENS 8.400 H4 SMALL 45W 12/24V"),
                                               ("7332407", "LED LUMENS 8.400 H7 SMALL 45W 12/24V")],
  foto=[382, 442, 560, 567], info="Tonalidade: 6.000K | Eficiência: 8.400 lúmens | Potência: 45W par | Resistência: IP67 | "
                                  "Voltagem: 12/24V | CSP | Chip de cobre | Obs: par")
NOTAS.append("Pág. 410: o card LED Small mostra também a base H8, sem código próprio.")
# 411 (pág. impressa 410): lâmpadas Teslla (foto = card inteiro: lâmpada + caixa)
_C3 = [(27, 206), (209, 388), (391, 568)]
_R6 = [(90, 208), (210, 334), (336, 453), (455, 572), (574, 689), (691, 806)]
for _k, _it in enumerate([
        ("7340067", "LAMPADA 12V 67 5W"), ("7340001", "LAMPADA 12V 1034 21/5V"), ("7340003", "LAMPADA 12V 1141 21W"),
        ("7341176", "LAMPADA 12V 1176 5W"), ("7340011", "LAMPADA 12V H1 55W"), ("7340005", "LAMPADA 12V H3 55W"),
        ("7340016", "LAMPADA 12V H4 60/55W"), ("7340019", "LAMPADA 12V H7 55W"), None,
        ("7340021", "LAMPADA 12V TORPEDO PEQ 36MM"), ("7340023", "LAMPADA 12V TORPEDO GRD 41MM"), ("7340028", "LAMPADA 24V 67 05W"),
        ("7340029", "LAMPADA 24V 69 04W"), ("7340025", "LAMPADA 24V 1034 21/5V"), ("7340033", "LAMPADA 24V H1 70W"),
        ("7340120", "LAMPADA 24V 1141"), ("7340027", "LAMPADA 24V 1176 21W"), ("7340038", "LAMPADA 14V TORPEDO GRD 44MM")]):
    _x, _y = _C3[_k % 3], _R6[_k // 3]
    if _it is None:
        G(411, 90, "LAMPADA ESMAGADA GRD 03W", [("7340009", "LAMPADA 12V ESMAGADA GRD 03W"), ("7340010", "LAMPADA 24V ESMAGADA GRD 03W")],
          foto=[_x[0], _y[0], _x[1], _y[1]], marca="Teslla")
        continue
    R(411, _it[0], _it[1], foto=[_x[0], _y[0], _x[1], _y[1]], marca="Teslla")
NOTAS.append("Pág. 411: 7340038 está no card 'TORPEDO GRA 24V' mas a descrição diz 'LAMPADA 14V TORPEDO GRD 44MM'.")
# 412 (pág. impressa 411): lâmpadas Teslla / ASX / Philips (foto = card inteiro)
for _c, _d, _rect, _kw in [
        ("7340014", "LAMPADA 24V H3 70W", [27, 90, 206, 190], dict(marca="Teslla")),
        ("7340039", "LAMPADA 24V H4 75/70W", [209, 90, 388, 190], dict(marca="Teslla")),
        ("7340036", "LAMPADA 24V H7 100W", [391, 90, 568, 190], dict(marca="Teslla")),
        ("7340036", "LAMPADA 24V H7 70W IMP TESLLA", [27, 192, 292, 299], dict(marca="Teslla")),
        ("7341141", "LAMPADA 24V 1141 21W AMBAR", [294, 192, 568, 299], dict(marca="Teslla")),
        ("7346724", "LAMPADA LED 67 / 1034 24V 2 POLOS 8 LED", [27, 301, 289, 438],
         dict(marca="ASX", info="2 polos | Obs: pino desencontrado")),
        ("7346725", "LAMPADA LED 67 / 1141 24V 1 POLO", [291, 301, 568, 438], dict(marca="ASX", info="Obs: pino encontrado")),
        ("7363342", "LAMPADA LED 24V 69 4 LEDS", [27, 440, 148, 555],
         dict(marca="ASX", info="24V 4 LED SMD | Aplicação: farolete, placa ou interior")),
        ("5515201", "LANT.LED PLACA BIVOLT 6 LEDS", [150, 440, 292, 555], dict(marca="ASX")),
        ("5511034", "LAMPADA 24V 1034 P21/5V ASX2634", [294, 440, 441, 555], dict(marca="ASX", variacoes="ASX2634", info="2 polos")),
        ("7342304", "LAMPADA 12V H4 SUPER BRANCA 60/55W ASX2304", [443, 440, 568, 555], dict(marca="ASX", variacoes="ASX2304")),
        ("7370699", "LAMPADA 24V 67 5W PHILIPS", [27, 557, 289, 673], dict(marca="Philips", variacoes="Ref. 13821", info="Original")),
        ("7342411", "LAMPADA 24V H11 70W ACTROS", [291, 557, 568, 673],
         dict(aplicacao="Aplicada para caminhões, Cibie MB Actros", montadora="Mercedes-Benz")),
        ("7373972", "LAMPADA 24V H7 PHILLIPS", [27, 675, 289, 804], dict(marca="Philips", variacoes="Ref. 13972", info="Original")),
        ("7371477", "LAMPADA 12V H4 FAROL BIODO 35/35 MOTO", [291, 675, 568, 804], dict(marca="Philips"))]:
    R(412, _c, _d, foto=_rect, **_kw)
NOTAS.append("Pág. 412: o código 7340036 aparece em dois cards (lâmpada 24V H7 100W e lâmpada 24V H7 70W imp. Teslla).")
# 413 (pág. impressa 412): lâmpadas LED ASX (aplicação: farolete, placa ou interior)
_R4 = [(90, 262), (265, 447), (450, 626), (629, 804)]
_FPI = "Farolete, placa ou interior"
for _k, (_c, _d, _inf, _apl) in enumerate([
        ("7363005", "LAMPADA LED 12V ESMAGADA 5 LEDS BRANCA", "Esmagada ou pingo d'água | T10 12V 5 LEDs", _FPI),
        ("7363020", "LAMPADA LED 12V ESMAGADA 20 LEDS BRANCA", "Esmagada ou pingo d'água | T10 12V 20 LEDs", _FPI),
        ("7363014", "LAMPADA LED 24V ESMAGADA 4 LEDS BRANCA", "Esmagada ou pingo d'água | T10 24V 4 LEDs", _FPI),
        ("7363015", "LAMPADA LED ESMAGADA 24V 5 LEDS BRANCA", "Esmagada ou pingo d'água | T10 24V 5 LEDs", _FPI),
        ("7363222", "LAMPADA LED 67 / 1034 12V 2 POLOS VERMELHA", "Obs: pino desencontrado", _FPI),
        ("7363202", "LAMPADA LED 67 / 1034 12V 2 POLOS BRANCA", "Obs: pino desencontrado", _FPI),
        ("7363212", "LAMPADA LED 67 / 1034 24V 2 POLOS BRANCA", "Obs: pino desencontrado", _FPI),
        ("7363201", "LAMPADA LED 67 / 1141 12V 1 POLOS BRANCA", "Obs: pino encontrado", "Farolete, placa ou lâmpada de ré"),
        ("7363231", "LAMPADA LED 1141 / 67 12V 8 LEDS 1 POLOS BRAN", "Obs: pino encontrado", _FPI),
        ("7363341", "LAMPADA LED 69 12V 4 LEDS", "Obs: 1 polo", _FPI),
        ("7363351", "LAMPADA LED 69 12V 5 LEDS", "Obs: 1 polo", _FPI),
        ("7363352", "LAMPADA LED 69 24V 5 LEDS", "Obs: 1 polo", _FPI)]):
    _x, _y = _C3[_k % 3], _R4[_k // 3]
    R(413, _c, _d, foto=[_x[0], _y[0], _x[1], _y[1]], marca="ASX", info=_inf, aplicacao=_apl)
# 414 (pág. impressa 413): faróis, barras e luminárias LED ASX (grade 4 x 5; foto = card inteiro)
_C4 = [(27, 161), (164, 298), (301, 436), (439, 571)]
_R5 = [(88, 229), (232, 378), (381, 522), (525, 666), (669, 804)]
for _k, _it in enumerate([
        ("5514407", 'FAROL REDONDO 7" H4 ANGEL EYE', dict(variacoes="ASX4407")),
        ("5514405", 'FAROL REDONDO 5,75" H4 ANGEL EYE', dict(variacoes="ASX4405")),
        ("5514407", 'LED FAROL REDONDO 7" H4 ANGEL', dict(variacoes="ASX4407",
         info='Farol redondo 7" - H4 angel eye - bivolt | 45W/90W / 12-60V | Alt: 19cm | Larg: 19cm | Prof: 7cm')),
        ("5514406", 'ARO FAROL REDONDO 7"', dict(info="Foto ilustrativa")),
        ("5514408", 'SUPORTE VW CONSTELLATION - FAROL REDONDO 7" H4 ANGEL EYE', dict(variacoes="ASX4408", montadora="Volkswagen")),
        ("5514009", "LED FAROL MINI 27W 9 LEDS", dict(variacoes="ASX4009", info="Cor branca | Bivolt | 27W | 6.000K | A: 9 cm | L: 9 cm")),
        ("5514042", "FAROL LED 42W 14 LEDS BIVOLT A", {}),
        ("5514019", "FAROL LED MILHA OFF ROAD 42W 14 LEDS BIVOLT A", dict(info="Mini")),
        ("5516104", "BLUE SPOT", dict(variacoes="ASX6104", info="Cor azul | Bivolt | Alt: 6,2cm | Comp: 9,5")),
        ("5514204", "LED FAROL 8 LEDS OVAL BIVOLT", dict(variacoes="ASX4204", info="Cor branca | Bivolt | 24W | 6.000K | A: 9,5 cm | L: 15 cm")),
        ("5514148", "LED UNIVERSAL LANTERNA TRAS BIVOLT A", dict(variacoes="ASX4148", info="Cor branca | Bivolt | 48W | 6.000K")),
        ("7002124", "FAROL LED TRATOR 24W 8 LEDS", dict(info="8 LEDs x 3W | Luz branca | 10-80V | Foco de lente tipo copo | 55 x 90 x 63MM | "
                                                          "Profundidade: 5,5 cm | Altura: 6,3 cm | Largura: 9,0 cm")),
        ("5516105", "LED RED LINE", dict(variacoes="ASX6105", info="Cor vermelha | Bivolt | Alt: 15,5cm | Comp: 3,7cm | Prof: 4,5cm")),
        ("5514340", "BARRA 40 LED 120W - BIVOLT", dict(variacoes="ASX4340", info="Worklight barra 40 LED - 120W - bivolt | 120W 10-80V | "
                                                                             "Altura: 10cm | Largura: 55cm | Impresso como 'BARRA BARRA 40 LED'")),
        ("5515015", "LUMINARIA 48 LED 8 W BIVOLT A", dict(info="8W bivolt | 800 lúmens | Alt: 7,5cm | Larg: 15cm")),
        ("5515030", "LUMINARIA 72 LED 12W BIVOLT A", dict(info="12W bivolt | 6000 lúmens")),
        ("5515050", "BARRA ALUMINIO 33 LED 50 CM BIVOLT A", dict(info="Bivolt | Larg: 1,7cm | Comp: 50cm | Prof: 1,3cm")),
        ("5515040", "RÉGUA 6 LED - 40 CM", dict(variacoes="ASX5040", info="Cor branca | Bivolt | Alt: 3cm | Comp: 40cm")),
        ("5515060", "RÉGUA 12 LED - 60 CM", dict(variacoes="ASX5060", info="Cor branca | Bivolt | Alt: 3cm | Comp: 60cm")),
        ("5515013", "PENDENTE LED 6W 48V", {})]):
    _x, _y = _C4[_k % 4], _R5[_k // 4]
    R(414, _it[0], _it[1], foto=[_x[0], _y[0], _x[1], _y[1]], marca="ASX", **_it[2])
NOTAS.append('Pág. 414: o código 5514407 aparece em dois cards (farol redondo 7" H4 angel eye e LED farol redondo 7" H4 angel).')
# 415 (pág. impressa 414): lanternas, suportes, giroleds e acessórios ASX (grade 4 x 6; foto = card inteiro)
_R6b = [(88, 232), (235, 353), (356, 465), (468, 579), (582, 693), (696, 804)]


def _cel(c, l):
    return [_C4[c][0], _R6b[l][0], _C4[c][1], _R6b[l][1]]


_SMD = "LED SMD | Aplicação: farolete, luz de ré e seta | Emb.: pacote com 10 unidades | Cor branca | 24V | 6.000K"
_G1 = "Alt: 10cm | Comp: 12,5cm | Prof: 12,5cm | Bivolt"
_G2 = "Alt: 16cm | Comp: 12,8cm | Prof: 13,2cm | Bivolt"
G(415, 1, "KIT MINI STROBE MULTIFUNÇÕES", [("5516081", "KIT MINI STROBE MULTIFUNÇÕES BRANCA ASX6081"),
                                          ("5516083", "KIT MINI STROBE MULTIFUNÇÕES AZUL ASX6083"),
                                          ("5516082", "KIT MINI STROBE MULTIFUNÇÕES ÂMBAR ASX6082"),
                                          ("5516084", "KIT MINI STROBE MULTIFUNÇÕES VERMELHA ASX6084")],
  foto=_cel(0, 0), marca="ASX", info="Alt: 9,5cm | Comp: 2,5cm | Bivolt")
G(415, 2, "LANTERNA LATERAL OVAL UNIVERSAL FC", [("5515251", "LANTERNA LATERAL OVAL UNIVERSAL FC ÂMBAR ASX5251"),
                                                ("5515252", "LANTERNA LATERAL OVAL UNIVERSAL FC BRANCA ASX5252"),
                                                ("5515253", "LANTERNA LATERAL OVAL UNIVERSAL FC VERMELHA ASX5253")],
  foto=_cel(2, 1), marca="ASX", info="Bivolt")
G(415, 3, "LANTERNA DELIMITADORA LED UNIVERSAL", [("5515271", "LANTERNA DELIMITADORA LED UNIVERSAL ÂMBAR ASX5271"),
                                                 ("5515272", "LANTERNA DELIMITADORA LED UNIVERSAL BRANCA ASX5272"),
                                                 ("5515273", "LANTERNA DELIMITADORA LED UNIVERSAL VERMELHA ASX5273")],
  foto=_cel(3, 1), marca="ASX", info="Bivolt")
for _c, _d, _cel_, _kw in [
        ("5513272", "LÂMPADA 1034 3 LED BULBO - 2 POLOS", (1, 0), dict(variacoes="ASX3272", info=_SMD)),
        ("5513271", "LÂMPADA 1141/67 BULBO - 1 POLO", (2, 0), dict(variacoes="ASX3271", info=_SMD)),
        ("5515307", "LANTERNA TRASEIRA REDONDA 29 LED UNIVERSAL", (3, 0), dict(variacoes="ASX5307", info="Bivolt")),
        ("5515390", "SUPORTE PARA LANT DE CAMINHÃO", (0, 1), dict(variacoes="ASX5390", info="A: 11 cm | L: 46 cm")),
        ("5515250", "SUPORTE LANTERNA LATERAL OVAL", (1, 1), dict(variacoes="ASX5250")),
        ("5515280", "SUPORTE LANTERNA TRASEIRA 3 LED 85MM", (0, 2), dict(variacoes="ASX5280")),
        ("5515102", "BOMBINHA DE ÁGUA 12V", (1, 2), dict(variacoes="ASX5102", info="Alt: 3,5cm | Comp: 9cm")),
        ("5515103", "BOMBINHA DE ÁGUA 24V", (2, 2), dict(variacoes="ASX5103", info="Alt: 3,5cm | Comp: 9cm")),
        ("5515313", "LANTERNA CARRETINHA CRISTAL STANDARD 12V", (3, 2), dict(variacoes="ASX5313",
         info="Lanterna carretinha 12V universal com farolete, freio, seta e ré. Lente cristal resistente à água e vibração, "
              "longa vida útil e instalação simples")),
        ("5515283", "LANT LED 85MM VERMELHA C/SUPORTE", (0, 3), dict(variacoes="LTLVER85", info="Cor vermelho | Bivolt")),
        ("7002008", "LANT LED 65MM CRISTAL S/SUPORTE", (1, 3), dict(variacoes="ASX5262", info="Cor cristal | Bivolt")),
        ("7002485", "LANT LED 85MM CRISTAL S/SUPORTE", (2, 3), dict(variacoes="ASX5282", info="Cor cristal | Bivolt")),
        ("5516052", "GIROLED BIVOLT VERMELHO", (0, 4), dict(variacoes="ASX6052", info=_G1)),
        ("5516053", "GIROLED BIVOLT AZUL", (1, 4), dict(variacoes="ASX6053", info=_G1)),
        ("5516054", "GIROLED BIVOLT VERDE", (2, 4), dict(variacoes="ASX6054", info=_G1)),
        ("5516051", "GIROLED 12 LED BIVOLT AMARELO", (3, 4), {}),
        ("5516056", "GIROLED PREMIUM 60 LED ÂMBAR", (0, 5), dict(variacoes="ASX6056", info=_G2)),
        ("5516057", "GIROLED PREMIUM 60 LED VERMELHO", (1, 5), dict(variacoes="ASX6057", info=_G2)),
        ("5516058", "GIROLED PREMIUM 60 LED AZUL", (2, 5), dict(variacoes="ASX6058", info=_G2)),
        ("5515101", "MICROFONE PTT 4 PINOS BIVOLT A", (3, 5), dict(info="4 pinos | Frequência: 500-600hz"))]:
    R(415, _c, _d, foto=_cel(*_cel_), marca="ASX", **_kw)
NOTAS.append("Pág. 415: nos giroleds premium a cor está só na linha 'COR ...' do card (âmbar, vermelho, azul) e foi acrescentada à descrição.")
# 416 (pág. impressa 415): lanternas LED laterais 65MM / 85MM e suportes
for _c, _d in [("7060165", "LANT LED 65MM A AMBAR S/SUPORTE"), ("7060465", "LANT LED 65MM B AMBAR C/SUPORTE"),
               ("7060265", "PDR-LANT LED 65MM A VERMELHA S/SUPORTE"), ("7060565", "LANT LED 65MM B VERMELHA C/SUPORTE"),
               ("7060365", "PDR-LANT LED 65MM A CRISTAL S/SUPORTE"), ("7060665", "LANT LED 65MM B CRISTAL C/SUPORTE"),
               ("7068501", "LANT LED 85MM C AMBAR S/SUPORTE DW"), ("7068505", "LANT LED 85MM D AMBAR C/SUPORTE DW"),
               ("7068502", "LANT LED 85MM C CRISTAL S/SUPORTE DW"), ("7068504", "LANT LED 85MM D CRISTAL C/SUPORTE DW"),
               ("7068506", "LANT LED 85MM D VERMELHA C/SUPORTE DW"), ("7068503", "LANT LED 85MM C VERMELHA S/SUPORTE DW"),
               ("7061056", "SUP. LANTERNA 03 MARIA"), ("7061053", "SUP. LANTERNA 03 MARIA"), ("7061052", "SUP. LANTERNA 07 MARIA"),
               ("7061269", "LANT LED CONJ 85MM 3 MARIAS DW")]:
    R(416, _c, _d)
R(416, "7002024", "SUPORTE LUZ DE POSIÇÃO 65MM", info="65MM menor")
R(416, "7002285", "SUPORTE LANTERNA 85MM", info="85MM maior")
R(416, "7068508", "LANT COMUM 85MM C AMBAR C/SUP S/LAMP GLR", marca="GLR")
NOTAS.append("Pág. 416: 7061056 e 7061053 têm a mesma descrição impressa (SUP. LANTERNA 03 MARIA), com suportes de formato diferente na foto.")
# 417 (pág. impressa 416): lanternas delimitadoras / laterais LED (grade 2 x 6; foto = card inteiro)
_C2 = [(27, 297), (302, 571)]
_R6c = [(83, 191), (194, 310), (313, 430), (433, 551), (554, 671), (674, 791)]
for _k, (_c, _d, _inf) in enumerate([
        ("7067145", "LANT.LED DELIMITADORA A AMBAR OVAL", "12V/24V"), ("7067146", "LANT.LED DELIMITADORA A VERMELHA OVAL", "12V/24V"),
        ("7067147", "LANT.LED DELIMITADORA A CRISTAL OVAL", "12V/24V"), ("7067148", "LANT.LED DELIMITADORA A VERDE OVAL", "12V/24V"),
        ("7061225", "PDR-LANT LED FACCHINI LATERAL LED C/SUPORTE", ""), ("7007254", "LANT.LED LATERAL EXCLUSIVE CAMINHÃO C/VIGIA", ""),
        ("7066507", "LANT LED 65MM C FRONTAL S/SUP AMBAR DW", ""), ("7061232", "LANT LED LATERAL DIAMANTE AMBAR C/SUPORTE", ""),
        ("7066509", "LANT LED 65MM C FRONTAL S/SUP CRISTAL DW", ""), ("7061234", "LANT LED LATERAL DIAMANTE CRISTAL C/SUPORTE", ""),
        ("7062012", "LANT.LED DELIMITADORA AMARELA OVAL", ""), ("7061250", "LANT LED 125 MM TRAS RUBI CARRETA DW", "")]):
    _x, _y = _C2[_k % 2], _R6c[_k // 2]
    R(417, _c, _d, foto=[_x[0], _y[0], _x[1], _y[1]], info=_inf)
for _r in ADD:
    if _r["codigo"] == "7061225":
        _r["montadora"] = "Facchini"
# 416: fotos pelo retângulo do card (a busca automática pegava a foto do verso)
_E, _D = (27, 297), (302, 571)
for _c, _x, _y in [("7060165", _E, (109, 170)), ("7060465", _D, (109, 170)), ("7060265", _E, (172, 235)), ("7060565", _D, (172, 235)),
                   ("7060365", _E, (237, 304)), ("7060665", _D, (237, 304)), ("7002024", _E, (306, 373)), ("7002285", _D, (306, 373)),
                   ("7068501", _E, (420, 486)), ("7068502", _E, (488, 551)), ("7068503", _E, (553, 621)),
                   ("7068505", _D, (420, 468)), ("7068504", _D, (470, 520)), ("7068506", _D, (522, 570)), ("7068508", _D, (572, 621)),
                   ("7061056", _E, (637, 718)), ("7061053", _D, (637, 718)), ("7061052", _E, (720, 804)), ("7061269", _D, (720, 804))]:
    for _r in ADD:
        if _r["pagina"] == 416 and _r["codigo"] == _c:
            _r["foto_spec"] = {"rect": [_x[0], _y[0], _x[1], _y[1]]}
