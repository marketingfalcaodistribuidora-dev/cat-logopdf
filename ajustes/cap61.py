# Capítulo 61 - Bombas, Carrinhos e Ferramentas Especiais (págs. 634-641)
# Listas por caixa: cada caixa (seção) = 1 produto com os códigos como itens; código+descrição via tabela_livre.ler_pagina,
# seções dadas à mão (retângulos pelas bordas das molduras); foto = maior imagem da seção.
import re

from tabela_livre import _spans, ler_pagina

TIPOS = []
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(634, 642))
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


TIPOS += [(r"MOTOBOMBA", "MOTOBOMBA"), (r"BOMBA", "BOMBA"), (r"CARRINHO", "CARRINHO DE FERRAMENTAS"), (r"ESTEIRA", "ESTEIRA PARA MECÂNICO"), (r"MACACO", "MACACO HIDRÁULICO"), (r"RODA RU", "RODA DE CARRINHO"),
          (r"TORQUIMETRO", "TORQUÍMETRO"), (r"FERRAMENTA|EXTRATOR", "EXTRATOR DE TERMINAL"), (r"CHAVE|^CH ", "CHAVE ESPECIAL DE CUBO"), (r"FACA", "FACA DE MÁQUINA"), (r"CRIMPAGEM", "MÁQUINA DE CRIMPAGEM"), (r"MAQUINA", "MÁQUINA RETIRAR LONA")]
_RV, _RS, _BV, _HD = dict(marca="Raven"), dict(marca="Riosul"), dict(marca="Bovenau"), dict(marca="Hidraumon")
_MB = "Mercedes-Benz"
# 634 (pág. impressa 633)
A(634, "6212019", "MOTOBOMBA GASOLINA P/AGUA PX50, 7 CV, 2, 600", [29, 99, 216, 267], marca="Denzel", info="7 cv | 212 cm³ | Quatro tempos | Altura manométrica 30 m | 1000 L/min | Entrada e saída 80 mm | Tanque 3 L | 510 x 385 x 445 mm | Para água limpa")
A(634, "6020020", "BOMBA PROPULSORA GRAXA PNEUMÁTICA 20KG", [32, 274, 208, 440], info="Alumínio e aço | Trabalho 87 a 116 PSI | Saída 4350 a 5800 PSI | Rateio 50:1 | 14,47 Kg")
A(634, "6018032", "BOMBA OLEO MANUAL 20L BOZZA", [68, 456, 177, 620], marca="Bozza", info="Reservatório 20L | 0,250 L/ciclo | 5,400 kg | 370 x 600 mm | 4 ciclos por litro")
A(634, "6008007", "BOMBA MANUAL TRANSF P/OLEO 20 LT OFICINA", [45, 645, 198, 791], info="Lançamento | 20 litros | 120 ml/acionamento | 50 psi | Reservatório 320 x 620 mm | Mangueira 1/4 pol. com 1,7 m")
# 635 (pág. impressa 634)
A(635, "6011343", "CARRINHO DE FERRAMENTAS ABERTO DOSMONTAVÉL BOVENAU R050006", [30, 95, 189, 276], cod_ref="R050006", **_BV)
A(635, "6010175", "CARRINHO P/FERRAM C/ 01 GAV", [304, 108, 480, 301], **_RS)
A(635, "6002000", "MACACO JACAREZINHO MALETA 2T", [102, 415, 288, 535], info="2 toneladas | 380 x 185 x 145 mm | Altura 140 a 290 mm | Curso 150 mm", **_RS)
P(635, "6018032", "BOMBA OLEO MANUAL 20L BOZZA", [305, 387, 443, 588], marca="Bozza")
A(635, "6010191", "ESTEIRA DOBRAVEL P/ MECANICO", [43, 639, 210, 759], info="Altura 9 cm | Comprimento 92 cm | Largura 42 cm", **_RS)
A(635, "6020534", "ESTEIRA P/MECANICO COM ENCOSTO", [305, 705, 464, 794], marca="Rotta", info="Polímero | Porta ferramentas | Rodas articuladas | Encosto para cabeça | 110kg | 3,440 Kg")
# 636 (pág. impressa 635)
A(636, "5980001", "MACACO HID RET. CX CAMBIO 1T P/OFICINA", [37, 139, 194, 280], info="1 tonelada | 1250 x 800mm | Altura 180 a 780mm | Óleo 32W | 103kg", **_HD)
A(636, "5980494", "RODA RU 312 CARRINHO DE CAMBIO", [405, 152, 530, 273], info="75MM x 12MM")
A(636, "6000001", "MACACO HID RETIRAR CX BOVENAU 1T", [37, 296, 211, 446], info="1000 kg | Altura 155 a 730 mm | 630 x 925 mm | Bandeja 375 mm | 72 kg", **_BV)
A(636, "102600", "MACACO HIDRÁULICO COMPACTO MANUAL P/ CAIXA DE TRANSMISSÃO", [46, 474, 225, 628], info="Carga máx. 800 kgs | Bandeja giratória 410 x 410mm | Inclinação até 15º | Altura máx. 882mm | 1011 x 418 x 272 mm | Código impresso com 6 dígitos", **_RV)
A(636, "991102700", "MACACO HIDRÁULICO P/ CAIXA DE TRANSMISSÃO 102700", [31, 636, 218, 800], cod_ref="102700", info="Carga máx. 1.000 kgs | Bandeja giratória 500 x 500mm | Inclinação até 15º | Trava automática | Altura máx. 845mm | 1184 x 645 x 307 mm | Substitui o antigo modelo 102400", **_RV)
NOTAS.append("Pág. 636: 102600 está impresso com 6 dígitos (igual à referência Raven) e 991102700 com 9 dígitos.")
# 637 (pág. impressa 636)
_A1 = "Mercedes-Benz 1117 a 2225, 2314 a 2423, O-355, O-362, O-364, O-365, O-371R/U/UL/UP, OF/OH-1313 a 1721 e 1525"
A(637, "10023854", 'CHAVE DE GARRAS 714007 ENCAIXE 3/4" P/ PORCA RANHURADA 95MM', [160, 152, 375, 228], cod_ref="714007", aplicacao=_A1, montadora=_MB, info='Porca ranhurada de 95mm do cubo traseiro | Eixos HD 4/21DG, HL 4/25D, HL 4/26D, HL 4/27D, HD 4/22D, HH 4/12D, HL 4/60, HL 5/Z, HL 5/2DZ, HL 5/12, HL 5/061, HO 4 e HO 4/23D | 41,5MM x 87MM', **_RV)
A(637, "10023876", 'CHAVE DE GARRAS 714150 ENCAIXE 1" P/ PORCA RANHURADA 100MM', [127, 280, 360, 364], cod_ref="714150", aplicacao="1622, 1728, 1728(6X2), 1728S, O-400R, O-400RS/RSD/RSL, O-400UP/UPA, O-500", montadora=_MB, info="Eixos HL 4/061, HL 4/062, HL 4/62, HL 5/61 e HO 4/09 | 54MM x 82MM", **_RV)
A(637, "10023862", 'CHAVE DE GARRAS 714015 ENCAIXE 1" P/ PORCA RANHURADA 108MM', [177, 456, 429, 540], cod_ref="714015", aplicacao="1215, 1218, 1718A, 1720(4X4), O-370RS/RSD, O-371U/UL/UP, O-400R/RS/RSD/RSL/UP/UPA, O-500, OH-1420/1421/1520, OH/OF-1618 a 1635, 1721 e 1525", montadora=_MB, info="Eixos HL4/01D, HD4/02DG, HD4/03D, HO4/01DL, HL4/060, HH4/05 e HH4/0 | 54MM x 100MM", **_RV)
A(637, "10023929", 'CHAVE OITAVADA 724560 100MM ENCAIXE 1" SCANIA', [100, 679, 316, 778], cod_ref="724560", aplicacao="Scania 94, 111-S, 112, 113, 114, 124, 142 e 143", montadora="Scania", info="Porca do cubo traseiro sem redução | 54MM x 100MM", **_RV)
NOTAS.append("Pág. 637: 10023862 (714015) é anunciado para porca de 108mm, mas o desenho da ferramenta indica 100MM.")
# 638 (pág. impressa 637)
for _c, _d, _ref, _a, _m, _f, _i in [
        ("10023953", "733811 FERRAMENTA P/SOLTAR TERM DIRECAO VOLVO", "733811", "FH-12 e NH-12", "Volvo", [110, 94, 195, 222], ""),
        ("10023918", "723001 EXTRATOR DO TERMINAL DE DIREÇÃO SCANIA", "723001", "112, 113, 114 e 124", "Scania", [262, 96, 347, 223], ""),
        ("10023837", "713019 FERRAMENTA P/DESTACAR TERM DIREC", "713019", "1924, 1929, 1932, 1933, 1934, 1935, 1938, 1941, 1945, 2629, 2635, 2638, 608D/E, 610, 708, LO-608, LO-708, O-370, O-371, O-400, O-500", _MB, [469, 90, 552, 233], ""),
        ("10023247", "713070 CHAVE QUADR P/PORCA EX DIAT AXOR", "713070", "Pontas de eixo dianteiras dos caminhões Mercedes-Benz Axor", _MB, [34, 286, 193, 380], 'Encaixe de 3/4" para porca retangular (60 x 76 mm)'),
        ("10023854", "713070 CHAVE QUADR P/PORCA EX DIAT AXOR Ø95 MM", "713070", "Aplica-se para todos Mercedes", _MB, [217, 313, 370, 390], "Ø95 mm"),
        ("10023869", "714122 CHAVE GARRA P/EIXO TRAS C/112MM", "714122", "Aplica-se para todos Mercedes", _MB, [413, 300, 543, 370], "112 mm"),
        ("10023876", 'CHAVE DE GARRAS 714150 ENCAIXE 1" P/ PORCA RANHURADA 100MM', "714150", "1622, 1728, 1728(6X2), 1728S, O-400R, O-400RS/RSD/RSL, O-400UP/UPA, O-500", _MB, [39, 473, 180, 547], "100 mm"),
        ("9910002", "734800 CH CUBO VOLVO RAVEN", "734800", "Caminhões Volvo (exceto séries FH, NH e FM) e ônibus B10M e B12", "Volvo", [221, 477, 352, 557], 'Chave sextavada de 106 mm, encaixe 1", porca do cubo traseiro sem redução ("canela seca")'),
        ("9914008", "754008 CH SEXTAVADA 95MM P/PORCA CUBO TRASEIR", "754008", "Caminhões Delivery, Express e micro-ônibus", "Volkswagen", [403, 464, 561, 569], ""),
        ("10023929", 'CHAVE OITAVADA 724560 100MM ENCAIXE 1" SCANIA', "724560", "111-S, 112 e 113", "Scania", [38, 661, 176, 743], "100 mm"),
        ("9913135", "723135 CH OITAVADA 101MM P/CUB RD DIAN SCANIA", "723135", "Caminhões Scania P / G / R série 5 (08>)", "Scania", [258, 641, 336, 720], ""),
        ("9912923", "722923 CHAVE 70MM PORCA 2 SCAN", "722923", "114 e 124", "Scania", [441, 656, 530, 735], "70 mm")]:
    A(638, _c, _d, _f, cod_ref=_ref, aplicacao=_a, montadora=_m, info=_i, **_RV)
NOTAS.append("Pág. 638: 10023854 está como '713070 chave quadr. Ø95 mm', mas na pág. 637 o mesmo código é a chave de garras 714007; 10023247 e 10023854 trazem a mesma referência 713070 impressa. "
             "O produto 734800 tem código 9910002 aqui e 9914800 na pág. 639.")
# 639 (pág. impressa 638)
A(639, "9914800", 'CHAVE SEXTAVADA 734800 106MM ENCAIXE 1" VOLVO', [200, 101, 416, 210], cod_ref="734800", montadora="Volvo", aplicacao="Caminhões Volvo (exceto séries FH, NH e FM) e ônibus B10M e B12", info='Porca do cubo traseiro sem redução ("canela seca") | 54MM x 106MM', **_RV)
A(639, "9914801", 'CHAVE SEXTAVADA 734801 95MM ENCAIXE 1" VOLVO', [162, 258, 396, 384], cod_ref="734801", montadora="Volvo", aplicacao="Volvo B-10M, B-58, FH, FM-12, N-10, N-12, NH, NL-10, NL-12", info="Porca do cubo traseiro com redução (cubo NR3, eixos EV71 e EV72; FM12 cubo NR4) | 41,5MM x 95MM", **_RV)
A(639, "10023966", "CHAVE CUBO ROCKWELL 744146 ENCAIXE 100MM", [251, 484, 528, 590], cod_ref="744146", montadora="Volkswagen, Ford, Iveco",
  aplicacao="Volkswagen 12-140T a 40-300; Ford C1417 a C4031, F12000, F14000, F16000; Eurocargo 170 E-21, 170 E-22 e 230 E-22", info='Lançamento | Chave sextavada de 100mm e encaixe de 1" para porca do cubo traseiro grande (08 parafusos), com rolamento blindado', **_RV)
A(639, "9914107", "100550 TORQUIMETRO 3/4 35KG", [25, 695, 331, 805], cod_ref="100550", info="Torquímetro de estalo ajustável | Margem +/- 4% | Certificado ISO 6789 | 7 a 35 kgf.m | 70 a 330 Nm | 50 a 250 lb.ft | 825 mm | Encaixe 3/4 pol. | Acompanha manual de torques", **_RV)
# 640 (pág. impressa 639)
A(640, "6020274", "MAQUINA PARA RETIRAR LONA DE FREIO", [54, 156, 218, 368], cod_ref="300274", info="50w | AC220V | 8-10 kg/cm² | 950 x 46 x 1020")
A(640, "60240606", "MAQUINA CRIMPAGEM DE MANGUEIRA", [396, 380, 561, 600], info='Crimpagem de 1/8" a 2" | Força 500t | 220v monofásica | 11 conjuntos de moldes | Precisão 0,01 mm | 31,5 MPa | 200 peças por hora | 300kg | 800 x 640 x 1300 mm')
A(640, "6020275", "FACA MAQUINA TIRAR LONA FREIO", [34, 652, 240, 799], cod_ref="3000275")
NOTAS.append("Pág. 641: contracapa institucional, sem produtos.")
