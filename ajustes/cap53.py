# Capítulo 53 - Óleos, Graxas e Fluidos (págs. 552-557)
# Listas por caixa: cada caixa (seção) = 1 produto com os códigos como itens; código+descrição via tabela_livre.ler_pagina,
# seções dadas à mão (retângulos pelas bordas das molduras); foto = maior imagem da seção.
import re

from tabela_livre import _spans, ler_pagina

TIPOS = []
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(552, 558))
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


TIPOS += [(r"AGUA", "ÁGUA DESMINERALIZADA"), (r"GRAXA", "GRAXA"), (r"ADITIVO", "ADITIVO"), (r"DOT", "FLUIDO DE FREIO"), (r"PASTA", "PASTA DE MONTAGEM"),
          (r"OLEO|ÓLEO", "ÓLEO"), (r"ADESIVO", "ADESIVO"), (r"VEDA|ELIMINA", "VEDANTE"), (r"APLICADOR", "APLICADOR DE SILICONE")]
_K, _R, _H = dict(marca="Karter"), dict(marca="Radnaq"), dict(marca="Hitech")
_AR = "Aplicação: a cada 01 litro de aditivo utiliza-se 08 litros de água"
_GC = ("Recomendada para situações que exigem boa adesividade, resistência à ação da água e temperaturas não superior a 80 ºC | Aplicado em pinos graxeiros de veículos e máquinas "
       "industriais, buchas, feixes de molas, montagem de bicicletas e afins")
# 552 (pág. impressa 551)
P(552, "9780339", "AGUA DESMINERALIZADA 1LT", [32, 108, 80, 220], info="Bateria, radiadores, motores estacionários e reservatórios", **_R)
P(552, "9780340", "AGUA DESMINERALIZADA 5LT", [165, 114, 236, 226], **_R)
P(552, "9801700", "GRAXA CHASSIS 170KG", [303, 116, 366, 227], info="Lançamento | " + _GC, **_K)
P(552, "9805050", "ADITIVO RADIADOR HITECH SUPER CONCENTRADO 1L", [450, 121, 559, 202], info=_AR, **_H)
P(552, "9780003", "DOT 3", [29, 253, 78, 373], info="Fluido para freios | NBR-9292 Tipo 3, SAE-J 1703 e FM/SS n° 116 DOT3 | Ponto de ebulição acima de 205 °C | Trocar a cada 12 meses", **_R)
P(552, "9780004", "DOT 4", [163, 250, 216, 372], info="Fluido para freios | NBR-9292 Tipo 4, SAE-J 1703 e FM/SS n° 116 DOT4 | Ponto de ebulição acima de 230 °C | Trocar a cada 12 meses", **_R)
P(552, "9851096", "ADITIVO DIESEL VERDE DNK 1LT ORGÂNICO L LIFE", [344, 242, 382, 345], marca="DNK", info="Lançamento | Truck concentrado - fluido para radiadores")
P(552, "9805054", "ADITIVO RADIADOR HITECH SUPER CONCENTRADO 5L", [438, 271, 500, 369], info=_AR, **_H)
P(552, "9806000", "DOT 3 500ML HITECH", [28, 394, 87, 514], info="Fluido para freio | Trocar conforme o manual do fabricante; na ausência, a cada 12 meses ou 10.000 km", **_H)
P(552, "9806010", "DOT 4 500ML HITECH", [163, 403, 227, 519], info="Fluido para freio | NBR 9292-Tipo 4, SAE J 1704, FMVSS n°116 DOT-4 | Ponto de ebulição acima dos 230 °C", **_H)
P(552, "9806050", "DOT 5 500ML HITECH", [307, 403, 362, 513], info="AP: BR9292-Tipo 5.1, SAE J 1703 e FMVSS N°116, DOT 5.1", variacoes="HT-6050", **_H)
P(552, "9802070", "ADITIVO SUPER DIESEL S10 500ML", [478, 382, 532, 476], **_H)
P(552, "6021313", "PASTA P/ MONTAGEM PNEU 3,2 LTS", [26, 529, 127, 629], marca="Lubrissis")
# 553 (pág. impressa 552)
P(553, "9801541", "OLEO MOTOR TURBO 15W40 BB 01LTS", [162, 93, 200, 168], **_K)
P(553, "9801540", "ÓLEO MOTOR TURBO 15W40 BB 20LTS", [30, 89, 110, 181], info="Troca varia geralmente entre 5.000 km e 10.000 km (ou 6 meses), conforme a formulação e o fabricante do veículo", **_K)
P(553, "9800012", "OLEO TRANSMISSAO K250 BD 20LTS SAE250/API-GL4", [212, 93, 312, 214], **_K)
P(553, "9800055", "OLEO TRANSMISSAO 85W140 BD 20LTS", [408, 90, 504, 207], **_K)
P(553, "9806820", "OLEO HIDRAULICO K-68 HL 20 LTS", [29, 282, 118, 378], info="Grau ISO VG 68 | Cor ASTM 3 | Viscosidade a 40 ºC: 66,8 cSt | Índice de viscosidade 104 | Ponto de fluidez -3 ºC | Ponto de fulgor 221 ºC | Galão balde 20 litros", **_K)
P(553, "9801010", "ÓLEO HIDRAULICO ATF 01LT", [333, 309, 375, 387], info="ATF (TASA)", **_K)
P(553, "9800120", "ÓLEO HIDRAULICO ATF 20LT", [212, 274, 310, 394], info="ATF (TASA)", **_K)
GP(553, 6, "GRAXA AZUL BLUTER MP-2", [("9801000", "GRAXA AZUL 01 KG BALDE"), ("9801011", "GRAXA AZUL 10 KG BALDE"), ("9801020", "GRAXA AZUL 20 KG BALDE")], [397, 278, 514, 399], **_K)
P(553, "9801420", "OLEO DIFERENCIAL SK-140", [41, 453, 178, 581], info="20 litros", **_K)
P(553, "9809020", "OLEO DIFERENCIAL SK-90 20 LTS", [239, 453, 345, 587], **_K)
_T30 = "Grau SAE 10W30 | Densidade a 20/4° 0,8871 | Cor ASTM D1500 4,5 | Viscosidade a 40 °C 81,46 cSt | a 100 °C 10,04 cSt | Índice de viscosidade 103 | Ponto de fluidez -39 °C | Ponto de fulgor 239 °C"
P(553, "9801030", "OLEO TRANSMISSAO 10W30 AGRICOLA BD 20LTS", [393, 454, 484, 575], info=_T30, **_K)
P(553, "9801031", "OLEO TRANSMISSAO 10W30 AGRICOLA BD 5LTS", [44, 649, 104, 743], info=_T30, **_K)
P(553, "9802050", "OLEO MOTOR PESADO 20W50 BD 20LTS", [214, 645, 289, 731], info="Grau SAE 20W50 | Densidade a 20/4° 0,8 a 0,9 | Cor ASTM D1500 máx. 4 | Viscosidade a 100 °C 16,3 / 21,8 cSt | Ponto de fluidez -18 °C", **_K)
_T80 = "Grau SAE 80W90 | Densidade a 20/4° 0,8 a 0,9 | Cor ASTM D1500 máx. 3,0 | Viscosidade a 100 °C 15,20–20,58 cSt | Ponto de fluidez -30 °C"
P(553, "9808091", "OLEO TRANSMISSAO 80W90 BD 20LT", [399, 643, 469, 731], info=_T80, **_K)
# 554 (pág. impressa 553)
P(554, "9801820", "GRAXA PARA CHASSIS 18KG", [32, 92, 130, 219], info="Retrak Chassis CA-2 castanha | " + _GC + " | Sabão de cálcio | NLGI 2 | Ponto de gota mínimo 95 ºC", **_K)
P(554, "9800267", "GRAXA VERDE 01,5 KG P/CB RODA, BISNAGA EP-K2", [223, 119, 373, 198], aplicacao="Lubrificação de várias peças em todos os modelos de carretas, trucks e cavalos", **_K)
P(554, "9809001", "OLEO DIFERENCIAL K-090 01 LT", [446, 94, 516, 221], **_K)
P(554, "9808001", "OLEO DIFERENCIAL K-080 01 LT", [82, 270, 146, 404], **_K)
P(554, "9801401", "OLEO DIFERENCIAL SK-140 01 LT", [264, 270, 332, 404], **_K)
GP(554, 6, "GRAXA VERDE P/CB RODA, 5A RODA EP-K2", [("9800211", "GRAXA VERDE 10,0 KG P/CB RODA, 5A RODA EP-K2"), ("9800257", "GRAXA VERDE 20,0 KG P/CB RODA, 5A RODA EP-K2")], [429, 273, 533, 409], **_K)
P(554, "9808090", "OLEO TRANSMISSAO 80W90 BD 01LT", [28, 473, 94, 620], info=_T80, **_K)
P(554, "9732020", "ADESIVO TEK ACRILICO SELA MADEIRA BRANCO 425G", [214, 461, 257, 593], marca="Tekbond")
P(554, "9732210", "VEDA P/ESCAPAMENTO 100G", [399, 466, 446, 618], marca="Tekbond")
P(554, "9731500", "ELIMINA JUNTA 0190 ROXO 15G", [30, 693, 105, 799], marca="Tekbond")
P(554, "9730050", "VEDA PARABRISA PRETO PU 55 405G OU 310ML", [212, 649, 251, 779], marca="Tekbond")
P(554, "6013919", "APLICADOR SILICONE AMARELO 300 GRS", [392, 666, 562, 764])
# 555-557 (págs. impressas 554-556): repetições das págs. 552-554
for _p, _c, _d, _kw in [(555, "9801540", "ÓLEO MOTOR TURBO 15W40 BB 20LTS", _K), (555, "9806820", "OLEO HIDRAULICO K-68 HL 20 LTS", _K), (555, "9801010", "ÓLEO HIDRAULICO ATF 01LT", _K),
                        (555, "9801000", "GRAXA AZUL 01 KG BALDE", _K), (555, "9801020", "GRAXA AZUL 20 KG BALDE", _K), (555, "9801820", "GRAXA PARA CHASSIS 18KG", _K),
                        (555, "9809020", "OLEO DIFERENCIAL SK-90 20 LTS", _K), (555, "6021313", "PASTA P/ MONTAGEM PNEU 3,2 LTS", dict(marca="Lubrissis")), (555, "9780003", "DOT 3", _R),
                        (555, "9780004", "DOT 4", _R), (555, "9780339", "AGUA DESMINERALIZADA 1LT", _R), (556, "9801700", "GRAXA CHASSIS 170KG", _K),
                        (557, "9851096", "ADITIVO DIESEL VERDE DNK 1LT ORGÂNICO L LIFE", dict(marca="DNK"))]:
    P(_p, _c, _d, **_kw)
NOTAS.append("Pág. 555: repete produtos das págs. 552-554; 9801000 está como 'graxa para rolamento 1 kg Bluter MP-2' e 9801868 (estopa polimento) já está no cap. 49 (pág. 526). "
             "Págs. 556-557: páginas de lançamento de 9801700 e 9851096.")
P(555, "9801868", "ESTOPA POLIMENTO", [426, 451, 543, 560])
