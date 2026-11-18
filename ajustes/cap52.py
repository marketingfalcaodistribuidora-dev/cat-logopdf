# Capítulo 52 - Adesivos, Silicones e Tintas Tekbond (págs. 546-551)
# Listas por caixa: cada caixa (seção) = 1 produto com os códigos como itens; código+descrição via tabela_livre.ler_pagina,
# seções dadas à mão (retângulos pelas bordas das molduras); foto = maior imagem da seção.
import re

from tabela_livre import _spans, ler_pagina

TIPOS = []
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(546, 552))
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


TIPOS += [(r"TINTA SPRAY", "TINTA SPRAY"), (r"SILICONE|SELANTE", "SILICONE"), (r"FITA", "FITA"), (r"ESPUMA", "ESPUMA EXPANSIVA"), (r"ARALDITE|ADESIVO|COLA|TRAVA|AUTO LOCK", "ADESIVO"),
          (r"VEDA|ELIMINA JUNTA", "VEDANTE"), (r"LIMPA CONTATO|GRAFITE|DESENGRIPANTE|TEK LUB", "SPRAY")]
_T = dict(marca="Tekbond")
_S4 = "Temperatura de trabalho e dureza conforme tabela da página"
# 546 (pág. impressa 545): relação; os produtos com foto estão nas páginas seguintes
for _c, _d in [("9738207", "TEK ADESIVO ARALDITE HOBBY 16G"), ("9738900", "TEK ADESIVO ARALDITE MASSA ALTA PERFORM 50G"), ("9738098", "TEK ADESIVO SILICONE 8098 BLACK 85G"),
               ("9738099", "TEK ADESIVO SILICONE 8099 GREY 85G"), ("9733001", "TEK COLA DE CONTATO 200G"), ("9738105", "TEK DESENGRIPANTE 300ML"),
               ("9731061", "TEK ESPUMA EXPANSIVA PU 500ML"), ("9731185", "TEK FITA CREPE 18MM X 50M"), ("9731710", "TEK FITA EMPACOTAMENTO 48MM X 40M"),
               ("9735459", "TEK LIMPA CONTATO TEKSPRAY 300ML"), ("9731412", "TEK SILICONE ACETICO 50G ALTA TEMP CINZA"), ("9733412", "TEK SILICONE ACETICO 50G ALTA TEMP INCOLOR"),
               ("9732412", "TEK SILICONE ACETICO 50G ALTA TEMP PRETO"), ("9734412", "TEK SILICONE ACETICO 50G ALTA TEMP VERMELHO"), ("9735615", "TEK SPRAY GRAFITE LUBRIFICANTE SECO 200ML")]:
    P(546, _c, _d, **_T)
NOTAS.append("Pág. 546: 9738105 (desengripante) e 9731185 (fita crepe) aparecem só na relação, sem foto no catálogo; a fita crepe com foto da pág. 551 tem o código 9731850. "
             "Na relação 9733412 é 'alta temp incolor', mas na pág. 547 ele está como acético uso geral.")
# 547 (pág. impressa 546)
_AT = "Silicone acético alta temperatura: formador de juntas para vedar e selar aplicações automotivas; aguenta até 316 °C dependendo da cor"
for _c, _d, _f, _i in [("9731412", "TEK SILICONE ACETICO 50G ALTA TEMP CINZA", [244, 122, 314, 243], _AT), ("9732412", "TEK SILICONE ACETICO 50G ALTA TEMP PRETO", [356, 125, 427, 242], _AT),
                       ("9734412", "TEK SILICONE ACETICO 50G ALTA TEMP VERMELHO", [459, 127, 527, 242], _AT),
                       ("9733412", "TEK SILICONE ACETICO 50G ALTA TEMP INCOLOR", [452, 367, 540, 517], "Acético uso geral: multiúso para aderir, vedar e selar"),
                       ("9738099", "TEK ADESIVO SILICONE 8099 GREY 85G", [315, 585, 394, 712], "Silicone neutro high performance | Grey 85 g / 290 g | -54 a 232 contínua e 260 intermitente"),
                       ("9738098", "TEK ADESIVO SILICONE 8098 BLACK 85G", [421, 585, 500, 710], "Silicone neutro high performance | Black 85 g / 290 g | -54 a 204 contínua e 260 intermitente")]:
    P(547, _c, _d, _f, info=_i, **_T)
# 548 (pág. impressa 547)
GP(548, 1, "TEK TINTA SPRAY SUPER COLOR USO GERAL 350ML", [("9730169", "TEK TINTA SPRAY USO GERAL 350ML PRETO FOSCO"), ("9731169", "TEK TINTA SPRAY USO GERAL 350ML PRETO BRILH"),
                                                         ("9732169", "TEK TINTA SPRAY USO GERAL 350ML BRANCO BRIL"), ("9733169", "TEK TINTA SPRAY USO GERAL 350ML ALUMINIO"),
                                                         ("9734169", "TEK TINTA SPRAY USO GERAL 350ML VERMELHO"), ("9736169", "TEK TINTA SPRAY USO GERAL 350ML AMARELO"),
                                                         ("9738169", "TEK TINTA SPRAY USO GERAL 350ML AZUL"), ("9731069", "TEK TINTA SPRAY USO GERAL 350ML BRANCO FOSC")],
   [74, 222, 563, 337], info="Embalagem 350 ml / 250 g", **_T)
GP(548, 2, "TEK TINTA SPRAY SUPER COLOR ALTA TEMPERATURA 350ML", [("9735169", "TEK TINTA SPRAY ALTA TEMPE 350ML PRETO BRIL"), ("9737169", "TEK TINTA SPRAY ALTA TEMPE 350ML PRETO FOSC"),
                                                                 ("9732669", "TEK TINTA SPRAY ALTA TEMPE 350ML ALUMINIO")],
   [447, 222, 563, 334], info="Embalagem 350 ml / 250 g", **_T)
P(548, "9736788", "ADESIVO TITANIO TEK 25G", [75, 605, 172, 800], info="Cola tudo | Super Epóxi Titânio: adesivo epóxi de duas partes para colagem e reparação de superfícies metálicas diversas", **_T)
NOTAS.append("Pág. 548: na tabela, a linha 'Alumínio alta temperatura' está sem código visível; o código 9732669 vem da relação da pág. 546.")
# 549 (pág. impressa 548)
P(549, "9730116", "TEK LUB MULTIUSO", [496, 105, 562, 350], info="Proteção contra umidade e corrosão, lubrifica e desengripa, eliminando ruídos e evitando o engripamento de peças e roscas metálicas", **_T)
P(549, "9735459", "TEK LIMPA CONTATO TEKSPRAY 300ML", [486, 366, 572, 584], info="Recuperar a condutividade, remover oxidação, oleosidade e umidade | Incolor | 300 ml / 200 g | -15 a +50 °C", **_T)
P(549, "9735615", "TEK SPRAY GRAFITE LUBRIFICANTE SECO 200ML", [488, 597, 568, 798], info="Diminuir atrito e formar película deslizante seca | Cinza-escuro | 200 ml / 100 g | -40 a +150 °C", **_T)
# 550 (pág. impressa 549)
P(550, "9732210", "VEDA P/ESCAPAMENTO 100G", [59, 152, 104, 304], info="Lançamento | Excelente adesão em aço, alumínio, latão e outras ligas metálicas | Não é inflamável | Resistente a vibrações | "
                                                                       "Resistente a altas temperaturas (até 600 ºC) | Secagem rápida | Pode ser lixado e pintado | Livre de amianto/asbestos", **_T)
P(550, "9731500", "ELIMINA JUNTA 0190 ROXO 15G", [230, 197, 301, 303], info="Lançamento | Vedação eficaz | Alta resistência à pressão | Média resistência à desmontagem | Alta viscosidade | "
                                                                           "Vedação em flanges, substitui juntas em bombas, termostatos, compressores, caixas de engrenagens", **_T)
P(550, "9730050", "VEDA PARABRISA PRETO PU 55 405G OU 310ML", [404, 153, 440, 283],
  info="Lançamento | Pasta tixotrópica preta com baixo odor | Película: 30 a 70 min | Cura em 24 h: ≥ 3 mm | Densidade a 25 ºC: 1,37 ± 0,02 g/mL | Aplicação: +5 a 45 °C | Trabalho: 40 a 80 °C | "
       "Armazenamento 5 a 25 °C: 12 meses | Materiais: acrílico, alumínio, borracha, ferro, metal, plástico e vidro", **_T)
P(550, "9731061", "TEK ESPUMA EXPANSIVA PU 500ML", [471, 335, 555, 514], info="Preenchimento de espaços vazios; instalação de portas e janelas | 500 ml / 480 g | Rendimento até 18 L", **_T)
P(550, "9738207", "TEK ADESIVO ARALDITE HOBBY 16G", [406, 611, 490, 694], info="Embalagem 16G | Secagem inicial 10 minutos | Cura total 8 horas", marca="Araldite")
P(550, "9738900", "TEK ADESIVO ARALDITE MASSA ALTA PERFORM 50G", [402, 717, 510, 806], info="Massa epóxi Araldite | Embalagem 50 G | Secagem inicial 2 horas | Cura total 72 horas", marca="Araldite")
# 551 (pág. impressa 550)
P(551, "9734256", "SILICONE ACETICO 256G PRETO TEK BOND", [27, 109, 70, 266], info="Pasta com odor característico | Densidade 0,93 a 1,05 g/mL | Película: 5 a 15 min | Aplicação: +5 a 35 °C | "
                                                                                 "Trabalho: -50 a 150 °C | Alongamento à ruptura 200% | Dureza Shore A: 20 | Cura após 24 h: ≥ 2 mm", **_T)
P(551, "9731710", "TEK FITA EMPACOTAMENTO 48MM X 40M", [473, 140, 537, 274], info="Fita empacotamento transparente 48mm x 40 metros | Pacote com 4 unidades", **_T)
P(551, "9731850", "FITA CREPE TEK 18MM X 50M", [353, 324, 534, 420], info="Fita de papel crepado de fácil remoção em até 24 horas | Branca | Uso interno/externo", **_T)
P(551, "9800316", "TRAVA PARAFUSOS TEK E ROSCAS 10G TEKBOND ANT0879", [30, 430, 101, 581], info="Viscosidade 6.000 a 8.000 cP | Trabalho -60 a 150 ºC | Folgas 0,25 mm | Resistência total em 24 horas | Torque de quebra 25 a 45 N.m", **_T)
P(551, "9800317", "AUTO LOCK TRAVA ROLAMENTO 10G", [273, 437, 344, 578], info="Viscosidade 100 a 200 cP | Trabalho -60 a 150 ºC | Folgas 0,10 mm | Resistência total em 24 horas | Cisalhamento ≥ 20", **_T)
GP(551, 90, "SELANTE ALTA TEMPERATURA", [("9800330", "SELANTE ALTA TEMPERATURA CINZA / PRETO"), ("9800115", "SELANTE ALTA TEMPERATURA VERMELHO"), ("9800329", "SELANTE ALTA TEMPERATURA INCOLOR")],
   [142, 604, 417, 797], **_T)
NOTAS.append("Pág. 551: o código 9800330 está impresso para duas cores do selante (cinza e preto); lançado uma vez com as duas cores.")
