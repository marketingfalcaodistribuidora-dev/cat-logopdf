# Capítulo 56 - Ferramentas Gedore, MTX e Máquinas de Bancada (págs. 583-593)
# Listas por caixa: cada caixa (seção) = 1 produto com os códigos como itens; código+descrição via tabela_livre.ler_pagina,
# seções dadas à mão (retângulos pelas bordas das molduras); foto = maior imagem da seção.
import re

from tabela_livre import _spans, ler_pagina

TIPOS = []
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(583, 594))
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


TIPOS += [(r"^CH FIXA|CHAVE FIXA", "CHAVE FIXA"), (r"^CH ESTRELA", "CHAVE ESTRELA"), (r"^CH COMB", "CHAVE COMBINADA"), (r"SOQUETE|^SOQ ", "SOQUETE"), (r"^JG CH", "JOGO DE CHAVES"), (r"^CH L |BIELA", "CHAVE BIELA"),
          (r"ALICATE", "ALICATE"), (r"AJUSTAVEL|GRIFO|CHAVE ING", "CHAVE AJUSTÁVEL"), (r"^ADAP", "ADAPTADOR"), (r"JUNTA UNIVERSAL", "JUNTA UNIVERSAL"), (r"CATRACA", "CATRACA"), (r"CABO T", "CABO T"), (r"EXTENSAO", "EXTENSÃO"),
          (r"CHAVE RODA", "CHAVE DE RODA"), (r"TORQUIMETRO", "TORQUÍMETRO"), (r"MANIPULO", "MANÍPULO"), (r"ESPATULA|ESPÁTULA", "ESPÁTULA"), (r"BROCA", "BROCA"), (r"FURADEIRA", "FURADEIRA DE COLUNA"),
          (r"ESMERIL", "MOTO ESMERIL"), (r"TORNO", "TORNO DE BANCADA"), (r"ESCOVA", "ESCOVA DE AÇO"), (r"ENGATE", "CONECTORES DE ENGATE"), (r"CABO T HEX", "CHAVE CABO T"), (r"CORREIA", "CHAVE DE CORREIA"),
          (r"ALLEN|TORX", "JOGO DE CHAVES"), (r"VIRA MACHO", "VIRA MACHO"), (r"JG MACHO", "JOGO DE MACHOS"), (r"ALARGADOR", "ALARGADOR")]
_GE, _GR, _MX, _ST, _SC = dict(marca="Gedore"), dict(marca="Gedore Red"), dict(marca="MTX"), dict(marca="Stels"), dict(marca="Schulz")
# 583 (pág. impressa 582)
LS(583, 1, "CHAVE FIXA BOCA GEDORE", [25, 88, 298, 418], [229, 113, 293, 349], **_GE)
LS(583, 2, "CHAVE ESTRELA OMEGA GEDORE", [298, 88, 570, 418], [526, 100, 563, 338], **_GE)
LS(583, 3, "CHAVE COMBINADA GEDORE", [25, 418, 298, 805], [243, 478, 295, 735], **_GE)
LS(583, 4, "SOQUETE SEXTAVADO 1/2 GEDORE", [298, 418, 570, 805], [513, 568, 560, 640], **_GE)
NOTAS.append("Pág. 583: na lista de soquetes, 9925012 (17) e 9921225 (25) fogem da sequência dos demais códigos.")
# 584 (pág. impressa 583)
LS(584, 1, "CH COMB GEDORE RED", [25, 200, 570, 443], [57, 101, 495, 197], **_GR)
A(584, "9934519", "CH FIXA 30 X 32 GEDORE RED", [31, 512, 195, 552], **_GR)
A(584, "9931012", 'EXTENSAO 1/2 -10" GEDORE RED', [220, 513, 384, 530], **_GR)
LS(584, 4, "SOQUETE SEXT 1/2 GEDORE RED", [392, 449, 570, 624], [398, 478, 564, 560], **_GR)
A(584, "99311222", "SOQ ESTRIADO ENC 1/2 22MM GEDORE RED", [32, 667, 190, 748], **_GR)
# 585 (pág. impressa 584)
A(585, "9924603", "JG CH FIXA 06 X 22MM GEDORE", [32, 131, 159, 229], info="6 x 7, 8 x 9, 10 x 11, 12 x 13, 14 x 15, 16 x 17, 18 x 19, 20 x 22, 21 x 23, 24 x 26, 25 x 28, 27 x 32 mm", **_GE)
A(585, "9920028", "JG CH ESTRELA 06 X 32 GEDORE", [167, 120, 282, 192], info="6 x 7, 8 x 9, 10 x 11, 12 x 13, 14 x 15, 16 x 17, 18 x 19, 20 x 22, 21 x 23, 24 x 26, 25 x 28, 27 x 32 mm", **_GE)
A(585, "9922603", "JG CH COMB 6 A 32 GEDORE", [298, 125, 399, 225], info="6 a 28, 30 e 32 mm", **_GE)
A(585, "9931256", "JG CH COMB 06MM A 32MM 24PC GEDORE RED", [425, 123, 561, 228], info="6 a 24, 26, 27, 28, 30 e 32 mm", **_GR)
A(585, "9939644", "GED RED JG CHAVE BIELA L", [38, 305, 197, 391], info="Encaixes sextavados | 12 peças: 8 a 19mm", **_GR)
LS(585, 6, "CHAVE BIELA (L) GEDORE", [208, 265, 395, 415], [220, 294, 264, 405], **_GE)
A(585, "9932104", 'GED RED JOGO ALICATE ANÉIS INT E EXT DE 7"', [415, 295, 552, 408], **_GR)
A(585, "9921244", 'ALICATE C DIAGONAL 6" GEDORE', [33, 475, 204, 541], **_GE)
A(585, "9921246", 'ALICATE PRESSAO 10" GEDORE', [227, 456, 385, 547], **_GE)
A(585, "9920294", "ALICATE UNIVERSAL", [401, 465, 566, 519], **_GE)
A(585, "9925501", "JG SOQUETE 08 A 32MM 1/2", [27, 584, 174, 752], variacoes="060.230 Robust", info="Jogo de soquetes estriados, 22 peças | 18 soquetes de 8 a 32 mm | 2 extensões 125 mm e 250 mm | 1 cabo T e 1 catraca reversível", **_GE)
A(585, "9938305", 'CH AJUSTAVEL GRIFO 15" GEDORE', [406, 585, 561, 624], **_GE)
A(585, "9931018", 'CH AJUSTAVEL/INGLESA 18" GEDORE RED', [396, 719, 566, 767], info="Sem foto própria no card (foto da chave inglesa ao lado)", **_GR)
A(585, "9922442", 'CH AJUSTAVEL INGLESA 24" GEDORE', [396, 719, 566, 767], **_GE)
# 586 (pág. impressa 585)
for _c, _d, _f in [("9921239", 'ADAP MACHO 3/8" X 1/2 FEMEA GEDORE', [52, 128, 141, 183]), ("9927100", 'ADAP MACHO 1/2" X 3/4 FEMEA 3219 GEDORE', [194, 125, 276, 177]),
                   ("9929340", 'ADAP FEMEA 3/4" X 1 MACHO 3221 GEDORE', [328, 126, 400, 196]), ("9920002", "ADAP FEMEA 1 X 3/4 MACHO 2132 GEDORE", [452, 132, 533, 187]),
                   ("9921234", "ADAP FEMEA 1/2 X 3/4 MACHO 1932 GEDORE", [62, 225, 151, 292]), ("9921120", 'JUNTA UNIVERSAL ENCAIXE DE 1/2"', [180, 227, 275, 274]),
                   ("9925230", 'CABO T 1/2 1987 12" GEDORE', [32, 326, 195, 357]), ("9921012", 'EXTENSAO 1/2 -10" GEDORE', [220, 328, 369, 355]),
                   ("9920006", 'CABO T 3/4 20" 3287 GEDORE', [381, 326, 555, 357]), ("9921717", "CHAVE RODA 17 C/ESPATULA", [350, 432, 532, 479]),
                   ("9921330", "MANIPULO P/ CH RODA 13 X 300 MM GEDORE", [321, 527, 555, 555]), ("9921950", "MANIPULO P/ CH RODA 19 X 500 MM GEDORE", [340, 609, 551, 632]),
                   ("9922460", 'ESPATULA CURVA 24" 600MM ESPECIAL GEDORE', [36, 607, 261, 640]), ("9921845", 'ESPATULA CHATA 450MM 18" GEDORE', [35, 687, 254, 717]),
                   ("9921250", 'ESPATULA CORPO REDONDO 18" 450MM GEDORE', [331, 690, 559, 729]), ("9922051", 'ESPATULA CHATA 500MM 20" GEDORE', [40, 766, 250, 792]),
                   ("9922300", 'ESPÁTULA REDONDA DESMONTAR PNEUS 23" 575MM', [360, 770, 541, 805])]:
    A(586, _c, _d, _f, **_GE)
A(586, "9938305", "CATRACA SIMPLES 1/2 GEDORE", [331, 239, 498, 285], **_GE)
GP(586, 90, "CHAVE RODA GEDORE", [("9920265", "CHAVE RODA 24 X 27MM GEDORE"), ("9922732", "CHAVE RODA 27 X 32 MM GEDORE"), ("9926165", "CHAVE RODA 30X32 MM GEDORE")], [30, 423, 276, 457], **_GE)
A(586, "9927180", "TORQUIMETRO ESTALO 1/2 2,0 KGF.M - 10,0 KGF.", [36, 501, 277, 531], info='Comprimento 395,0 mm | Escala 10 lbf.pé / 0,50 N.m | Encaixe 1/2" | 2,0 a 10,0 kgf.m | 15 a 75 lbf.pé / 20 a 100 N.m | DIN EN ISO 6789', **_GE)
NOTAS.append("Págs. 585-586: o código 9938305 está impresso em dois produtos diferentes (chave ajustável grifo 15\" e catraca simples 1/2); lançado com as duas descrições.")
# 587 (pág. impressa 586)
A(587, "9931464", "ESPATULA CURVA PERFIL ESPECIAL GEDORE RED", [24, 657, 154, 801], **_GR)
A(587, "9935005", "ESPATULA GED CHATA 500MM GEDORE RED", [166, 636, 273, 799], **_GR)
A(587, "6012004", 'ESPATULA CHATA 24" 600MM RIOSUL', [304, 638, 411, 801], marca="Riosul")
A(587, "9935000", "ESPATULA REDONDA. 500MM GEDORE RED", [434, 642, 562, 801], **_GR)
NOTAS.append("Pág. 587: as três molduras superiores da página estão vazias.")
# 588 (pág. impressa 587): repete a pág. 580
LS(588, 1, "BROCA ACO RAPIDO GOLD", [25, 130, 375, 391], [52, 160, 110, 380], desc={"6260916": "BROCA GOLD ACO BLACK E DECKER G 9/16"}, marca="Dewalt")
A(588, "6260650", "BROCA GOLD ACO BLACK E DECKER 06,50MM", [401, 111, 548, 282], marca="Stanley")
GP(588, 2, "BROCA STARRETT", [("6200500", 'BROCA STARRETT P/CONCRETO 5,00MM-3/16"'), ("6200650", 'BROCA STARRETT P/CONCRETO 6,50MM-1/4"'), ("620120", "BROCA STARRETT ACO RAPIDO 12,00MM"),
                           ("6200120", "BROCA STARRETT ACO RAPIDO 12,00MM"), ("6200012", 'BROCA STARRETT ACO RAPIDO 1/2"')], [30, 401, 87, 592], marca="Starrett")
LS(588, 3, "BROCA ACO RAPIDO IRWIN", [25, 603, 395, 805], [34, 651, 353, 677], desc={"6274019": "BROCA ACO RAPIDO 10MM IRWIN / 18MM IRWIN"}, marca="Irwin")
A(588, "6274049", "BROCA ACO RAPIDO 05MM IRWIN COBERTURA TITANIO", [375, 542, 567, 739], marca="Irwin")
A(588, "6274055", "BROCA ACO RAPIDO 10MM IRWIN COBERTURA TITANIO", [375, 542, 567, 739], marca="Irwin")
NOTAS.append("Pág. 588: repete as brocas da pág. 580; aqui a broca 10MM cobertura titânio tem o código 6274055 (na pág. 580 está 6274019), e 6274019 está impresso para as brocas 10MM e 18MM Irwin.")
# 589 (pág. impressa 588)
A(589, "9900406", "FURADEIRA COLUNA FSC329 MONOF 4P 750W 220V", [485, 95, 564, 259], info='Furação de até 32MM | Eixo 1 1/4", cone morse 3 | Mesa móvel e inclinável | Protetor de cavaco e interruptor magnético conforme NR-12')
A(589, "6043002", "FURADEIRA COLUNA FC-16 - 3/4 CV - 220V", [472, 272, 555, 443], info="Motor 3/4 cv (550W) | 1700 rpm | 220 V | Mandril 3/4 pol. (19mm) | 12 velocidades de 250 a 3100 rpm | Altura total 1600 mm | Mesa 300 mm | Base 440 x 410 mm")
A(589, "6043003", 'FURADEIRA COLUNA PROF FCI-19 - 1.1.2" CV 220V', [487, 449, 561, 622], info="Motor 1.5 cv (1100W) | 1700 rpm | 220 / 380 V | Mesa inclinável até 45 graus | 12 velocidades de 140 a 3560 rpm | Mesa 470 x 420 mm | Base 420 x 560 mm")
A(589, "9909121", 'MOTO ESMERIL SCHULZ 6", 300 WATTS - 110 VOLTS', [44, 631, 255, 785], info="Ferro fundido | 3,0A (110V), 1,5 A (220V) | 3450 rpm | 2 rebolos: desbaste (A-36) e afiação (A-60) | 27,5 x 21 x 39 cm | 8,2 Kg", **_SC)
NOTAS.append("Pág. 589: a FC-16 é anunciada com '12 velocidades 280 até 3000 rpm', mas os dados técnicos listam de 250 a 3100 rpm.")
# 590 (pág. impressa 589)
A(590, "6011368", "TORNO DE BANCADA FERRO N 8", [46, 166, 302, 330], cod_ref="Schulz-10010094", info="Torno de bancada N°08 com mordentes metálicos", **_SC)
A(590, "6011369", "TORNO DE BANCADA FERRO N10", [37, 415, 269, 563], cod_ref="Schulz-10010095", info="Torno de bancada N°10 com mordentes metálicos", **_SC)
A(590, "6017025", "ESCOVA CIRCULAR P/MOTO ESMERIL", [412, 426, 538, 546])
_ME = "Ideal para afiar ferramentas, desbastar superfícies, dar acabamento e rebarbar peças | Rebolo 6×1/2×5/8 | 60 Hz"
A(590, "6040008", 'MOTO ESMERIL BIVOLT 6" 360W', [32, 588, 165, 684], marca="Ferrari", info=_ME + " | 360 W | 3580 rpm | 127/220 V | Bivolt com chave seletora")
A(590, "60160127", "MOTOESMERIL 360W MONO 127V VONDER", [229, 585, 380, 684], marca="Vonder", info=_ME + " | 360 W | 3450 rpm | 127 V")
A(590, "60160220", "MOTOESMERIL 360W MONO 220V VONDER", [408, 585, 559, 684], marca="Vonder", info=_ME + " | 360 W | 3450 rpm | 220 V")
# 591 (pág. impressa 590)
A(591, "6215369", "MTX - JG SOQUETE ESTRIADO 20 PCS 3/4 POL", [34, 91, 221, 231], info='16 soquetes estriados de 19 a 50 mm | 2 extensões de 4" e 8" | 1 chave T de 450mm | 1 catraca 3/4" de 490mm', **_MX)
A(591, "6216155", "MTX - JG SOQUETE IMP 10 A 22MM 1O PÇS ENC 1/2", [28, 263, 204, 402], info="10 soquetes: 10, 11, 12, 13, 14, 15, 17, 18, 19 e 22 mm | Estojo metálico", **_ST)
A(591, "6026012", "CATRACA REVERS 1/2 EMBOR", [403, 296, 563, 392], **_ST)
GP(591, 3, "MTX - CHAVE ING CABO EMBORRACHADO", [("6215039", "MTX - CHAVE ING CABO EMBORRACHADO 200M 8 POL"), ("6215079", "MTX - CHAVE ING CABO EMBORRACHADO 300M 12 POL")], [30, 400, 397, 510], **_MX)
GP(591, 4, "MTX - CHAVE GRIFO AMERICANA", [("6210455", "MTX - CHAVE GRIFO AMERICANA 350MM 14 POL"), ("6212400", "MTX - CHAVE GRIFO AMERICANA 600MM 24 POL"), ("6213600", "MTX - CHAVE GRIFO AMERICANA 900MM 36 POL")], [31, 511, 359, 589], **_MX)
A(591, "6216655", "MTX - ESCOVA ACO CARBONO 4 FILEIRAS CABO PAST", [50, 668, 270, 728], **_MX)
A(591, "6011824", "ESCOVA MANUAL DE AÇO C CABO", [49, 748, 279, 801])
A(591, "6211655", "MTX - JG CONEC C/ ENGATE RAPIDO 4 PCS 1/4 NPT", [388, 688, 561, 790], **_ST)
# 592 (pág. impressa 591)
GP(592, 1, "CHAVE CABO T HEXAGONAL", [("9900025", "CHAVE CABO T HEXAGONAL 2,5X112"), ("9900030", "CHAVE CABO T HEXAGONAL 3,0X126"), ("9900004", "CHAVE CABO T HEXAGONAL 4,0X142"), ("9900005", "CHAVE CABO T HEXAGONAL 5,0X160")], [47, 175, 275, 272])
GP(592, 2, "CHAVE DE CORREIA", [("6010168", 'CHAVE DE CORREIA 4"-100MM'), ("6012515", "CHAVE DE CORREIA 25 - 150MM")], [358, 89, 516, 170])
GP(592, 3, "CHAVE RODA", [("9922730", "CHAVE RODA 27 X 30 MM"), ("6010522", "CHAVE RODA ROBUST 27X33MM"), ("6010525", "CHAVE RODA ROBUST 32X33MM")], [309, 200, 565, 236])
A(592, "6011510", "JOGO CHAVE ALLEN 1,5 MM A 10 MM LONGA", [47, 276, 288, 365], marca="Corneta")
A(592, "6011972", "JOGO CHAVE TORX T10 A T50 LONGA", [310, 278, 564, 357], marca="Corneta")
A(592, "6210512", "MTX - VIRA MACHO M5 A M12", [30, 418, 121, 509], **_MX)
A(592, "6010213", 'VIRA MACHOS "T" 150MM', [402, 431, 538, 514], info='Vira macho tipo T de 1/4" a 1/2", 150 mm')
A(592, "6011810", 'VIRA MACHOS "T" 250MM - 10MM -18MM', [90, 519, 284, 637], info="Lançamento")
A(592, "6212055", "MTX - VIRA MACHO M6 A M20", [311, 519, 562, 603], **_MX)
LS(592, 6, "JG MACHO ACO RAPIDO", [25, 638, 570, 805], [389, 649, 527, 722])
# 593 (pág. impressa 592)
GP(593, 1, "ALARGADOR EXPANSIVO COM GUIA", [("9070017", "ALARGADOR EXPANSIVO COM GUIA MODELO I 27,00 A 30,00MM"), ("9070018", "ALARGADOR EXPANSIVO COM GUIA MODELO J 30,00 A 34,00MM"),
                                           ("9070019", "ALARGADOR EXPANSIVO COM GUIA MODELO K 34,00 A 38,75MM"), ("9070020", "ALARGADOR EXPANSIVO COM GUIA MODELO L 38,75 A 46,00MM"),
                                           ("9070021", "ALARGADOR EXPANSIVO COM GUIA MODELO M 46,00 A 56,00MM")], [37, 173, 559, 471], info="Venda sob consulta")
NOTAS.append("Pág. 593: impresso 'VENDA SOBE CONSULTA'.")
