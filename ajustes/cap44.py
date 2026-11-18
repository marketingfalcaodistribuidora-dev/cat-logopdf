# Capítulo 44 - Conexões Pneumáticas (págs. 484-497)
# Listas por caixa: cada caixa (seção) = 1 produto com os códigos como itens; código+descrição via tabela_livre.ler_pagina,
# seções dadas à mão (retângulos pelas bordas das molduras); foto = maior imagem da seção.
import re

from tabela_livre import _spans, ler_pagina

TIPOS = [(r"COTOVELO", "COTOVELO"), (r"^TEE|EMENDA EM T", "TEE"), (r"CONECTOR", "CONECTOR"), (r"UNIAO|UNIÃO", "UNIÃO"),
         (r"PARAFUSO OCO", "PARAFUSO OCO"), (r"OLHAL", "OLHAL"), (r"ANILHA", "ANILHA"), (r"INSERT", "INSERT"), (r"PORCA", "PORCA"),
         (r"NIPLE", "NIPLE"), (r"BUJ[AÃ]O|TAMP[AÃ]O", "BUJÃO / TAMPÃO"), (r"REDU", "REDUÇÃO"), (r"ENGATE|PINO", "ENGATE"),
         (r"DRENO", "DRENO"), (r"BICO", "BICO PARA MANGUEIRA"), (r"RABO TATU", "RABO DE TATU"), (r"REGISTRO|TORNEIRA", "REGISTRO"),
         (r"ADAPTADOR|ADAPTACAO", "ADAPTADOR")]
AJ = {}
ADD = []
NOTAS = ["Págs. 484-497 (conexões pneumáticas): cada caixa da página virou 1 produto com os códigos da lista como itens."]
MANUAIS = set(range(484, 498))
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


# 484 (pág. impressa 483)
S(484, [("UNIAO RAPIDA PLASTICA MILIMETRO", [25, 88, 294, 274]), ("UNIAO RAPIDA PLASTICA POLEGADA", [294, 88, 570, 274]),
        ("UNIAO RAPIDA PLASTICA REDUÇÃO", [25, 274, 294, 440]), ("COTOVELO PLASTICO", [294, 274, 570, 440]),
        ("COTOVELO R GIR OD.TB", [25, 440, 570, 567]), ("CONECTOR R", [25, 567, 570, 805])],
  {"8010604": "UNIAO PLASTICA 06 X 04", "7710608": "UNIAO PLASTICA 08 X 06", "8011008": "UNIAO PLASTICA 10 X 08"})
for _r in [r for r in ADD if r["pagina"] == 484 and r["codigo"] == "8011210"]:
    _r["descricao"] = "UNIAO PLASTICA 12 X 10 / 08 X 12"
NOTAS.append("Pág. 484: 8011210 está impresso duas vezes na lista de reduções (12 X 10 e 08 X 12); lançado uma vez com as duas medidas. "
             "Os cotovelos 801.1204 e 801.1214 do desenho são os mesmos 8011204/8011214 do cap. Buzinas.")
# 485 (pág. impressa 484)
S(485, [("CONECTOR Y PLASTICO", [25, 87, 322, 189]), ("UNIAO PLASTICA Y", [25, 189, 322, 267]),
        ("TEE PLASTICO", [322, 87, 570, 267]), ("TEE EMENDA RAPIDA", [25, 267, 570, 384]),
        ("TEE PLASTICO CENTRAL", [25, 384, 225, 508]), ("TEE PLASTICA 6 X 6 X 8", [225, 384, 387, 508]),
        ("TEE PLASTICA 8 X 8 X 6", [387, 384, 570, 508]), ("TEE LATAO UNIAO EMENDA", [25, 508, 315, 598]),
        ("TEE UNIAO EMENDA NYLON", [315, 508, 570, 679]), ("TEE MACHO CENTRAL TUBO", [25, 598, 315, 679]),
        ("EMENDA EM T LATAO", [25, 679, 315, 805]), ("TEE RAPIDA LATAO", [315, 679, 570, 805])],
  {"7710668": "TEE PLASTICA 6 X 6 X 8", "7710886": "TEE PLASTICA 8 X 8 X 6", "8011000": "TEE PLASTICO UNIAO 10MM",
   "7711771": "EMENDA EM T A LATAO 06MM 1/4"})
for _r in ADD:
    if _r["pagina"] == 485 and _r["codigo"] == "7710668":
        _r["info"] = "Buzina 6MM / buzina 6MM / 8MM rodo ar"
    if _r["pagina"] == 485 and _r["codigo"] == "7710886":
        _r["info"] = "8MM / 8MM / 6MM"
NOTAS.append("Pág. 485: 7710668 e 7710886 (tees plásticos 6x6x8 e 8x8x6) — no cap. Nicolini os mesmos tees aparecem com os códigos "
             "8016608 e 8016606.")
# 486 (pág. impressa 485)
S(486, [("PARAFUSO BANJO", [25, 290, 570, 330]), ("PARAFUSO OCO", [25, 87, 570, 290]), ("OLHAL MANGUEIRA", [25, 330, 570, 560]),
        ("MB TERMINAL", [25, 560, 298, 688]), ("TERMINAL ACELERADOR", [298, 560, 570, 688]),
        ("TERMINAL ACELERADOR", [25, 688, 298, 805]), ("TERMINAL ACELERADOR", [298, 688, 570, 805])],
  {"5170612": "PARAFUSO BANJO CHANFRADO 06X1X12MM", "5060426": "MB TERMINAL 5MM", "7716090": "TERMINAL ACELERADOR 06 X 06",
   "7710222": "TERMINAL ACELERADOR 08 X 06", "7715146": "TERMINAL ACELERADOR 08 X 08"})
for _r in ADD:
    if _r["pagina"] == 486 and _r["codigo"] in ("9980006", "9980008", "7710100", "7711215", "7711415", "7711615", "7711815",
                                                 "7711110", "7711112", "9981445", "7711616"):
        _r["_titulo"] = "PARAFUSO OCO (SIMPLES / LONGO / DUPLO)"
NOTAS.append("Pág. 486: o '+' antes das descrições foi retirado; os terminais 5060426, 7716090, 7710222 e 7715146 também estão no "
             "cap. Peças Mercedes-Benz (pág. 384).")
# 487 (pág. impressa 486)
S(487, [("UNIAO COMPLETA LATÃO MILIMETRO", [25, 87, 570, 302]), ("PORCA CONICA / PORCA LATAO UNIAO", [25, 302, 570, 403]),
        ("UNIAO COMPLETA LATÃO POLEGADA (CONICA)", [25, 403, 570, 520]), ("ANILHA", [25, 520, 322, 805]),
        ("INSERT", [322, 520, 570, 805])],
  {"8003316": "UNIAO A COMPLETA CONICA 3/16"})
NOTAS.append("Pág. 487: 7710606, 8000682 e 8000684 aparecem duas vezes na caixa da união completa latão (união completa latão e "
             "união comp tubo porca QD); 8000688 e 8000430 estão como 'CB' (1/2 e 7/16). Insert 7711200 e união 7710606 repetem códigos "
             "de outros capítulos.")
# 488 (pág. impressa 487)
S(488, [("UNIAO ENGATE RAPIDA", [25, 87, 298, 240]), ("UNIAO REDUTURA COMPLETA", [298, 87, 570, 240]),
        ("CONECTOR RAPIDO", [25, 240, 298, 382]), ("UNIAO EMENDA NYLON", [298, 240, 570, 382]),
        ("TEE UNIAO EMENDA NYLON", [25, 382, 298, 582]), ("CONECTOR M RAPIDO 08MM", [298, 382, 438, 480]),
        ("UNIAO ENGATE RAPIDA CONICA", [438, 382, 570, 480]), ("CONECTOR M RAPIDO 10MM", [298, 480, 438, 582]),
        ("CONECTOR M RAPIDO 12MM", [438, 480, 570, 582]), ("PORCA C/ANILHA PLASTICA", [25, 582, 298, 805]),
        ("CONECTOR FEMEA", [298, 582, 570, 805])],
  {"8006503": "CONECTOR M RAPIDO OD 08MM X 16MM 1,5 CONICA", "8006500": "UNIAO ENGATE RAPIDA 06MM CONICA",
   "8006501": "CONECTOR M RAPIDO OD 10MM X 16MM 1,5 CONICA", "8006502": "CONECTOR M RAPIDO OD 12MM X 16MM 1,5 CONICA",
   "8000504": "CONECTOR FEMEA TUBO 1/4 X 1/8 NPT"})
NOTAS.append("Pág. 488: o tee união emenda nylon (8000513/8001618/8000512/8000511) repete a pág. 485.")
# 489 (pág. impressa 488)
S(489, [("CONECTOR MACHO (MÉTRICO)", [25, 87, 570, 368]), ("CONECTOR MACHO OD NPT", [25, 368, 570, 512]),
        ("CONECTOR MACHO X M16 / M22", [25, 512, 570, 628]), ("CONECTOR MACHO OD POLEGADA NPT", [25, 628, 570, 805])],
  LN(489, [25, 87, 570, 368]))
NOTAS.append("Pág. 489: 801086 (conector macho OD 10MM x 1/4 NPT) está impresso com 6 dígitos.")
# 490 (pág. impressa 489): conexões engate rápido (texto impresso como imagem, transcrito); grade 3 x 4
_C3 = [(27, 208), (208, 389), (389, 568)]
_R4 = [(87, 267), (267, 447), (447, 625), (625, 805)]
_VA = "Veículos a ar mod. TDS"
for _k, (_c, _d, _ref, _apl) in enumerate([
        ("7718071", "CONEXAO ENGATE RAPIDO 90@ NG12 (TUBO 08X1,0MM)", "001.990.8071", _VA),
        ("7715871", "CONEXAO ENGATE RAPIDO 90@ NG12 (TUBO 12X1,5MM)", "002.990.5871", _VA),
        ("7712971", "CONEXAO ENGATE RAPIDO 90@ NG12 (TUBO 16X2,0MM)", "002.990.2971", _VA),
        ("771678", "CONEXAO ENGATE RAPIDO RETA NG8 (TUBO 08X1,0MM)", "000.990.6678", _VA),
        ("7716778", "CONEXAO ENGATE RAPIDO RETA NG12 (TUBO 08X1,0MM)", "000.990.6778", _VA),
        ("7711178", "CONEXAO ENGATE RAPIDO RETA NG8 (TUBO 12X1,5MM)", "001.990.1178", _VA),
        ("7716878", "CONEXAO ENGATE RAPIDO RETA NG12 (TUBO 12X1,5MM)", "000.990.6878", _VA),
        ("7711278", "CONEXAO ENGATE RAPIDO RETA NG12 (TUBO 16X2,0MM)", "001.990.1278", _VA),
        ("7710834", "NIPLE ENGATE RAPIDO PNEUMAT (16X1,5MM) (PORCA UBL NG8)", "000.997.0834", _VA),
        ("7710934", "NIPLE ENGATE RAPIDO PNEUMAT (22X1,5MM) (PORCA UBL NG12)", "000.997.0934", _VA),
        ("7710045", "REP CONEXAO ENC NG08 ENCANAM. AR COMPRIM.16MM", "", ""),
        ("7710145", "REP CONEXAO ENC NG12 ENCANAM. AR COMPRIM.22MM", "", "")]):
    _x, _y = _C3[_k % 3], _R4[_k // 3]
    X(490, _c, _d, [_x[0], _y[0], _x[1], _y[1] - 45], cod_ref=_ref, aplicacao=_apl, montadora="Mercedes-Benz" if _ref else "",
      info="Descrição impressa como imagem (transcrita)" if _ref else "")
NOTAS.append("Pág. 490: 771678 (conexão engate rápido reta NG8 tubo 08) está impresso com 6 dígitos; as referências 000.990.xxxx "
             "são números originais Mercedes-Benz.")
# 491 (pág. impressa 490)
S(491, [("CONECTOR M RAPIDO OD", [25, 100, 570, 306]), ("BUJAO C ENCOSTO ORING / TAMPAO MACHO NPT", [25, 306, 570, 440]),
        ("NIPLE ENGATE RAPIDO NG 22", [25, 440, 217, 596]), ("NIPLE ENGATE RAPIDO NG16", [217, 440, 396, 596]),
        ("CONTRA PORCA C/ORING 16MM", [396, 440, 571, 596]), ("CONEXAO FREIO AR C/PONTA PLASTICA", [25, 596, 217, 817]),
        ("UNIAO FEMEA", [217, 596, 571, 674]), ("REDUCAO (REDUTORA MXF)", [217, 674, 571, 817])],
  {"8001251": "CONTRA PORCA C/ORING 16MM", "8001609": "CONEXAO FREIO AR C/PONTA PLASTICA 16 X 1,5MM"})
for _r in ADD:
    if _r["pagina"] == 491 and _r["codigo"] == "8001609":
        _r.update(montadora="Mercedes-Benz", aplicacao="Axor 1315/1418/1518/2031",
                  cod_ref="0009973634, 0009974734, 0009974934, 0009975034, 0009975334, 0009975334 e 495232001800")
NOTAS.append("Pág. 491: 768000613, 767712212 e 768007007 estão impressos com 9 dígitos (descrição 'IMP 3,25').")
# 492 (pág. impressa 491)
S(492, [("COTOVELO M. ENGATE RAPIDO OD", [25, 87, 570, 257]), ("COTOVELO MACHO OD 16M X MACHO 16M C/PORCA", [25, 257, 150, 405]),
        ("COTOVELO MACHO OD 16 X FEMEA 16MM", [25, 405, 235, 540]), ("COTOVELO MACHO OD (MÉTRICO / NPT)", [235, 257, 570, 540]),
        ("COTOVELO GIRATORIO TUBO 06MM X 1/4 NPT", [25, 540, 150, 685]), ("COTOVELO MACHO OD 1/2 X MACHO 1/2", [25, 685, 150, 805]),
        ("COTOVELO MACHO COMP (POLEGADA)", [150, 540, 570, 752]), ("CONECTOR MACHO OD 12MM X 3/8 NPT", [150, 752, 570, 768]),
        ("COTOVELO MACHO FEMEA 1/8 NPT", [150, 768, 570, 805])],
  {"8001430": "COTOVELO MACHO OD 16M X MACHO 16M C/PORCA", "8001601": "COTOVELO MACHO OD 16 X FEMEA 16MM",
   "8006142": "COTOVELO GIRATORIO TUBO 06MM X 1/4 NPT", "8001680": "COTOVELO MACHO 08MM X 16 1,5MM"})
for _r in ADD:
    if _r["pagina"] == 492 and _r["codigo"] == "8000764":
        _r["info"] = "Lançamento"
NOTAS.append("Pág. 492: 8000618 impresso como 'COTOVELO MACHA'.")
# 493 (pág. impressa 492)
S(493, [("PINO ENGATE AR COMPR RABO TATU", [25, 87, 570, 327]), ("ENGATE FEMEA AR COMPR 1/4", [25, 327, 570, 522]),
        ("COTOVELO RABO TATU OD", [25, 522, 570, 805])])
# 494 (pág. impressa 493)
S(494, [("UNIAO ANTEPARO PNEUMATICA", [25, 87, 570, 184]), ("UNIAO ANTEPARO RAPIDO", [25, 184, 570, 270]),
        ("UNIAO ANTEPARO 16MM TB", [25, 452, 570, 508]), ("UNIAO ANTEPARO", [25, 270, 570, 452]),
        ("UNIAO ANTEPARO LONGA COM ANILHA", [25, 508, 570, 575]), ("UNIAO ANTEPARO M X F", [25, 575, 570, 652]),
        ("DRENO BALAO AR 1/2 VW / FORD", [25, 652, 298, 805]), ("DRENO BALÃO DE AR M22", [298, 652, 570, 805])],
  {"8002128": "UNIAO ANTEPARO M X F M16-1,5", "8002129": "UNIAO ANTEPARO M X F M16-1,5 X M22-1,5",
   "7770522": "DRENO BALAO AR 1/2 VW / FORD", "7770689": "DRENO BALÃO DE AR M22", "7710003": "UNIAO ANTEPARO 16MM TB 08MM",
   "7710004": "UNIAO ANTEPARO 16MM TB 10MM"})
for _r in ADD:
    if _r["pagina"] == 494 and _r["codigo"] == "7770522":
        _r["montadora"] = "Volkswagen, Ford"
# 495 (pág. impressa 494)
S(495, [("NIPLE / NIPLE REDUCAO / NIPLE RETO", [25, 87, 570, 538]), ("NIPLE COM ORING", [25, 538, 570, 630]),
        ("BICO PARA MANGUEIRA", [25, 630, 570, 713]), ("RABO TATU EMENDA LATAO", [25, 713, 570, 805])],
  {"8001385": "NIPLE COM ORING M12 X 1,5", "8000616": "NIPLE COM ORING M16 X 1,5", "8001393": "NIPLE RED M22 X 1,5 X M16 X 1,5"})
NOTAS.append("Pág. 495: 8001385, 8000616 e 8001393 aparecem na lista de niples e de novo na caixa 'niple com oring' (descrições "
             "diferentes); 9022291 (niple relógio temperatura) está na lista de niples.")
# 496 (pág. impressa 495)
S(496, [("TEE LATAO UNIAO EMENDA", [25, 87, 570, 234]), ("TEE MACHO CENTRAL TUBO", [25, 234, 570, 346]),
        ("TEE MACHO LATERAL 1/8 NPT", [25, 346, 184, 447]), ("TEE MACHO LATERAL 1/4 NPT", [184, 346, 319, 447]),
        ("TEE ADAPTACAO VOLVO M16 X 1,5", [319, 346, 440, 447]), ("TESTE VALVULA PRESSAO 16MM 1.5", [440, 346, 570, 447]),
        ("EMENDA EM T LATAO", [25, 447, 570, 566]), ("UNIAO RAPIDA LATAO (MM / POLEGADA)", [25, 566, 256, 679]),
        ("TEE RAPIDA LATAO", [256, 566, 570, 679]), ("UNIAO RAPIDA LATAO", [25, 679, 570, 805])],
  dict(LN(496, [25, 87, 570, 234]), **{"7711771": "EMENDA EM T A LATAO 06MM 1/4"}))
for _r in ADD:
    if _r["pagina"] == 496 and _r["codigo"] == "8001395":
        _r["montadora"] = "Volvo"
NOTAS.append("Pág. 496: tee latão, tee macho central, emenda em T e tee rápida repetem a pág. 485.")
# 497 (pág. impressa 496): grade 3 colunas, um produto por card
_C = [(27, 208), (208, 391), (391, 568)]
_R = [(87, 184), (184, 252), (252, 333), (333, 418), (418, 512), (512, 652), (652, 805)]
for (_l, _k), _c, _d, _inf in [
        ((0, 0), "8006012", "NIPLE REDUCAO 1/2 NPT X M16MM", ""), ((0, 1), "8001101", "CONECTOR M 16 X FEMEA 1/4 NPT", ""),
        ((0, 2), "8001102", "CONECTOR M 16 X FEMEA 3/8 NPT", ""), ((1, 0), "8001109", "CONECTOR M16 X FEMEA 22MM ALUMINIO", ""),
        ((1, 1), "8001178", "PORCA CONICA 3/8", ""), ((1, 2), "8001838", "CONECTOR M 1/8NPT X FEMEA 3/8", ""),
        ((2, 0), "8001104", "CONECTOR M 16 X FEMEA M 22", ""), ((2, 1), "8001103", "CONECTOR M 16 X FEMEA 1/2 NPT", ""),
        ((2, 2), "8000302", "MACHO 16X18 - PONTEIRA CONICA", "Impresso 'CUNICA'"),
        ((3, 0), "8000301", "MACHO 3/4 X 3/8 - PONTEIRA CONICA", "Impresso 'CUNICA'"),
        ((3, 1), "8000300", "MACHO 3/4 X 1/4 - PONTEIRA CONICA", "Impresso 'CUNICA'"),
        ((3, 2), "8000303", "MACHO 16 X 3/4 - PONTEIRA CONICA", "Impresso 'CUNICA'"),
        ((4, 0), "8000307", "ADAPTADOR MACHO 3/8 X FEMEA 16", ""), ((4, 1), "8001397", "TESTE VALVULA PRESSAO 16MM 1.5", ""),
        ((4, 2), "8004118", "CONEXAO REL.TEMP MACHO/FEM.14X1.5X27 ALT.", ""),
        ((5, 0), "8001992", "REGISTRO TORNEIRA BALAO AR MACHO 1/4 X 1/4 FEMEA TODOS", "Polegada x milímetro: 1/4 = 12,6"),
        ((5, 1), "8001993", "REGISTRO TORNEIRA BALAO AR M 1/4 X F 1/4 NPT BORBOLETA", "Polegada x milímetro: 1/4 = 12,6"),
        ((5, 2), "8001995", "REGISTRO AR CARRETAS 1/4 X 1/4 NPT", "Polegada x milímetro: 1/4 = 12,6"),
        ((6, 0), "8001996", "REGISTRO AR CARRETAS 3/8 X 3/8 NPT", "Polegada x milímetro: 3/8 = 16,44"),
        ((6, 1), "8001997", "REGISTRO AR CARRETAS 1/2 X 1/2 NPT", "Polegada x milímetro: 1/2 = 20,07MM"),
        ((6, 2), "8001994", "TORNEIRA TANQUE KIT ADAP VW", "")]:
    _x, _y = _C[_k], _R[_l]
    X(497, _c, _d, [_x[0], _y[0], _x[1], _y[1]], info=_inf, montadora="Volkswagen" if _c == "8001994" else "")
NOTAS.append("Pág. 497: 8006012 (niple redução) e 8001397 (teste válvula pressão) repetem as págs. 495/496.")
# 492: fotos (a foto da lista métrica fica à esquerda da caixa; as 2 últimas linhas usam a foto da lista COMP)
for _r in ADD:
    if _r["pagina"] == 492 and _r["_titulo"] == "COTOVELO MACHO OD (MÉTRICO / NPT)":
        _r["foto_spec"] = {"rect": [151, 274, 269, 400]}
    if _r["pagina"] == 492 and _r["codigo"] in ("8003813", "8000406"):
        _r["foto_spec"] = {"rect": [153, 628, 211, 702]}
        _r["info"] = "Sem foto própria no card (foto da lista de cotovelos macho comp)"
# 490/497: foto = maior imagem dentro do card
for _p in (490, 497):
    _, _imgs = _spans(_p)
    for _r in ADD:
        if _r["pagina"] == _p and _r.get("foto_spec"):
            _c = _r["foto_spec"]["rect"]
            _f = [b for b in _imgs if _dentro(_c, (b[0] + b[2]) / 2, (b[1] + b[3]) / 2) and (b[2] - b[0]) * (b[3] - b[1]) > 400]
            if _f:
                _r["foto_spec"] = {"rect": [round(v, 1) for v in max(_f, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))]}
