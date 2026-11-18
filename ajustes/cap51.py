# Capítulo 51 - Reparos de Freio e Acessórios de Pneu (págs. 543-545)
# Listas por caixa: cada caixa (seção) = 1 produto com os códigos como itens; código+descrição via tabela_livre.ler_pagina,
# seções dadas à mão (retângulos pelas bordas das molduras); foto = maior imagem da seção.
import re

from tabela_livre import _spans, ler_pagina

TIPOS = []
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(543, 546))
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


TIPOS += [(r"^KIT", "KIT DE FREIO"), (r"ACIONADOR", "ACIONADOR DE FREIO AUTOMÁTICO"), (r"REGULADOR", "REGULADOR DE FREIO AUTOMÁTICO"), (r"^REPARO", "REPARO DE FREIO"),
          (r"CONTRA PESO", "CONTRA PESO"), (r"TAMPA", "TAMPA BICO PNEU"), (r"PITO|BICO PNEU", "BICO DE PNEU"), (r"RETIFICA", "RETÍFICA PNEUMÁTICA"), (r"SOQUETES", "JOGO DE SOQUETES"),
          (r"JOGO DE CHAVES", "JOGO DE CHAVES"), (r"CHAVE RODA", "CHAVE DE RODA"), (r"CABO", "CABO"), (r"FILTRO REG|LUBRIFIL", "FILTRO REGULADOR DE AR")]
_F, _G, _T, _M, _R, _H = "Ford", "GM-Chevrolet", "Toyota", "Mitsubishi", "Renault", "Hyundai"
for _p, _c, _d, _no, _a, _m, _f in [
        (543, "5668280", "REPARO DE FREIO A DISCO 2 RDS", "BE5E2B486A", "F-100 / F-1000 79/... F-2000 80/85", _F, [30, 107, 122, 149]),
        (543, "5660121", "REPARO DE FREIO A DISCO 2 RDS", "", "F4000 85/.. S.Vargas", _F, [211, 111, 295, 149]),
        (543, "5660131", "REPARO FREIO A DISCO 1 RODA BENDIX", "", "F1000 out/94/...", _F, [396, 108, 465, 141]),
        (543, "5660109", "REPARO SAPATA DE FREIO (PINO 52MM)", "", "Ranger 95/... 10 pol.", _F, [30, 172, 90, 225]),
        (543, "5660144", "REPARO SAPATA DE FREIO (PINO 57MM)", "", "Ranger 98/... 11 pol.", _F, [211, 177, 291, 214]),
        (543, "5660137", "REPARO SAPATA DE FREIO (PINO 52MM)", "BF2CK035B", "F100 / F1000 79/...", _F, [391, 175, 448, 208]),
        (543, "5660149", "REPARO SAPATA DE FREIO (PINO 52MM)", "BF2C2K035D", "F1000", _F, [29, 242, 93, 298]),
        (543, "5661867", "REPARO SAPATA DE FREIO (PINO 70MM)", "BF2Y2K035", "F4000", _F, [214, 245, 286, 297]),
        (543, "5660200", "REPARO SAPATA DE FREIO (PINO 52MM)", "BC7A2A094B", "F350/400/4000", _F, [403, 256, 455, 294]),
        (543, "5663000", "ACIONADOR DE FREIO AUTOMÁTICO LD", "C6TZ2A1776-A", "F250 / F350", _F, [39, 326, 116, 361]),
        (543, "5663001", "ACIONADOR DE FREIO AUTOMÁTICO LE", "C6TZ2A1776-A", "F250 / F350", _F, [211, 325, 292, 362]),
        (543, "5663002", "ACIONADOR DE FREIO AUTOMÁTICO LD", "225.4988-D", "F100 68/87 / F1000 79/...", _F, [394, 329, 476, 365]),
        (543, "5663005", "ACIONADOR DE FREIO AUTOMÁTICO LE", "225.4988-E", "F100 68/87 / F1000 79/...", _F, [34, 396, 106, 438]),
        (543, "5663003", "ACIONADOR DE FREIO AUTOMÁTICO LD", "225.4989-D", "F400 / F200 / F4000 85/...", _F, [216, 392, 288, 443]),
        (543, "5663004", "ACIONADOR DE FREIO AUTOMÁTICO LE", "225.4989-E", "F400 / F200 / F4000 85/...", _F, [395, 393, 463, 431]),
        (543, "5663006", 'ACIONADOR DE FREIO AUT. (10" X 2¼) LD', "F57Z2A278", "Ranger 95/...", _F, [32, 469, 94, 500]),
        (543, "5663106", 'ACIONADOR DE FREIO AUT. (10" X 2¼) LE', "F57Z2A278", "Ranger 95/...", _F, [210, 473, 284, 510]),
        (543, "5663007", 'ACIONADOR DE FREIO AUT. (11" X 2¼) LD', "F67Z2A178", "Ranger 98/...", _F, [394, 465, 467, 502]),
        (543, "5663107", 'ACIONADOR DE FREIO AUT. (11" X 2¼) LE', "F67Z2A178", "Ranger 98/...", _F, [37, 537, 107, 572]),
        (543, "5668005", "REGULADOR FREIO AUTOMÁTICO DUCATO", "", "Ducato 94/02, Boxer 98/..., Jumper 96/...", "Fiat", [211, 535, 297, 583]),
        (543, "5668105", "REGULADOR FREIO AUTOMÁTICO DUCATO", "", "Ducato 94/02, Boxer 98/..., Jumper 96/...", "Fiat", [394, 541, 474, 574]),
        (543, "5665007", "REPARO SAPATA DE FREIO (PINO 40MM)", "9949473", "Ducato 2003/...", "Fiat", [29, 607, 104, 655]),
        (543, "5665011", "REPARO DA SAPATA DE FREIO COMPLETO", "", "Ducato 94/2002", "Fiat", [212, 605, 282, 655]),
        (543, "5665013", "REPARO DA SAPATA DE FREIO DOBRO TDS", "", "Doblò tds", "Fiat", [395, 617, 469, 652]),
        (543, "5662102", "REPARO SAPATA DE FREIO (PINO 52MM)", "50832631030A", "Besta / Topic tds", "Kia", [28, 680, 90, 729]),
        (543, "5662073", "REPARO SAPATA DE FREIO (PINO 40MM)", "", "Frontier 4 X 4 2003/...", "Nissan", [215, 684, 290, 727]),
        (543, "5662070", "REPARO DA SAPATA DE FREIO", "", "L200 Sport / Out-door RT 2003", _M, [395, 684, 472, 727]),
        (543, "5662032", "REPARO SAPATA DE FREIO (PINO 52MM) LE", "", "Mitsubishi L200 / L300", _M, [32, 753, 99, 802]),
        (543, "5662031", "REPARO SAPATA DE FREIO (PINO 52MM) LD", "", "Mitsubishi L200 / L300", _M, [213, 750, 281, 803]),
        (543, "5662071", "REPARO DO PATIM DE FREIO", "", "L200 Triton", _M, [393, 752, 470, 802]),
        (544, "5660714", "REPARO DE FREIO A DISCO", "900690K071JG", "Toyota Hylux", _T, [30, 104, 99, 153]),
        (544, "5662055", "REGULADOR DE FREIO AUTOMÁTICO", "", "Toyota Hilux 05/...", _T, [213, 115, 294, 154]),
        (544, "5662155", "REGULADOR DE FREIO AUTOMÁTICO", "", "Toyota Hilux 05/...", _T, [393, 116, 478, 155]),
        (544, "5662072", "REPARO SAPATA DE FREIO (PINO 40MM)", "", "Toyota Hilux 05/...", _T, [39, 182, 97, 218]),
        (544, "5662030", "REPARO SAPATA DE FREIO (PINO 40MM)", "9050626014", "Toyota Hilux tds", _T, [218, 186, 298, 219]),
        (544, "5660703", "REPARO SAPATA DE FREIO (PINO 56MM)", "47.447.98001", "Toyota Bandeirantes", _T, [396, 181, 470, 224]),
        (544, "5662120", "KIT DE FREIO A DISCO COMPLETO", "", "Renault Trafic S.Bendix", _R, [34, 254, 105, 296]),
        (544, "5662056", "KIT DO PATIM DE FREIO", "", "Renault Trafic 93/... S.Vargas", _R, [212, 256, 290, 300]),
        (544, "5662021", "REPARO DA SAPATA DE FREIO", "", "Renault Trafic S.Bendix", _R, [394, 254, 473, 296]),
        (544, "5660008", "REPARO FREIO A DISCO", "94.855.914", "A / C / D-10 / 20 78/... Bonanza / Veraneio", _G, [34, 324, 107, 368]),
        (544, "5661066", "REPARO DE FREIO A DISCO BENDIX", "", "A/C/D-20 93/... Silverado 97/...", _G, [211, 326, 283, 360]),
        (544, "5661080", "REPARO SAPATA FREIO PINO 52MM", "7.363.271-225.4931", "A/C/D-10/20/C-14 / Veraneio / Bonanza", _G, [397, 320, 467, 372]),
        (544, "5661095", "REPARO SAPATA DE FREIO (PINO 52MM)", "90.193.013", "S-10 / Blazer tds", _G, [30, 393, 104, 429]),
        (544, "5661099", "REPARO DA SAPATA DE FREIO LD", "93215584 / 93215597", "A/C/D-20 93/... / Silverado", _G, [214, 406, 296, 438]),
        (544, "5661199", "REPARO DA SAPATA DE FREIO LE", "93215584 / 93215597", "A/C/D-20 93/... / Silverado", _G, [395, 404, 473, 436]),
        (544, "5661108", "ACIONADOR DE FREIO AUTOMÁTICO", "93.215.596D", "A / C / D-20 93/... Silverado tds", _G, [29, 467, 99, 512]),
        (544, "5661109", "ACIONADOR DE FREIO AUTOMÁTICO", "93.215.596E", "A / C / D-20 93/... Silverado tds", _G, [209, 468, 292, 508]),
        (544, "5661110", "ACIONADOR DE FREIO AUTOMÁTICO", "2254988-D", "C/D-10/20 / Veraneio 78/... Blazer / S10", _G, [393, 466, 465, 512]),
        (544, "5661113", "ACIONADOR DE FREIO AUTOMÁTICO", "2254988-E", "C/D-10/20 / Veraneio 78/... Blazer / S10", _G, [28, 534, 109, 568]),
        (544, "5661111", "ACIONADOR DE FREIO AUTOMÁTICO LD", "2254989-D", "A / C / D-40 85/...", _G, [209, 534, 294, 582]),
        (544, "5661112", "ACIONADOR DE FREIO AUTOMÁTICO LD", "2254989-E", "A / C / D-40 85/...", _G, [394, 534, 476, 581]),
        (544, "5662077", "REPARO DA SAPATA DE FREIO LE", "", "Hyunday HR", _H, [30, 608, 106, 644]),
        (544, "5662076", "REPARO DA SAPATA DE FREIO LD", "", "Hyunday HR", _H, [212, 612, 281, 646]),
        (544, "5660516", "REPARO DA SAPATA DE FREIO", "A9019930410005", "Sprinter CDI", "Mercedes-Benz", [399, 611, 461, 648]),
        (544, "5660527", "REPARO DO PATIM DE FREIO (PINO 52MM)", "000.423.6012", "Sprinter 310D / 312D / 314D", "Mercedes-Benz", [32, 678, 100, 718]),
        (544, "5665000", "REPARO SAPATA DE FREIO", "42535860", "Iveco Daily / 3510 / 4012 / 4912", "Iveco", [213, 680, 292, 728]),
        (544, "5665001", "REPARO DA SAPATA DE FREIO", "42535859", "Iveco 5912", "Iveco", [396, 688, 484, 726])]:
    X(_p, _c, _d, _f, cod_ref=_no, aplicacao=_a, montadora=_m)
NOTAS.append("Págs. 543-544: textos impressos como imagem (transcritos). 5661112 está impresso como 'LD', com NO terminado em -E (lado esquerdo). "
             "5668005 e 5668105 têm a mesma descrição; 5662055 e 5662155 também.")
# 545 (pág. impressa 544)
for _c, _g, _e in (("8101549", "10G", 100), ("8101550", "15G", 100), ("8101551", "20G", 100), ("8101552", "25G", 100), ("8101553", "30G", 100), ("8101554", "35G", 100),
                   ("8101555", "40G", 50), ("8101556", "45G", 50), ("8101557", "50G", 50), ("8101559", "60G", 50)):
    ADD.append(dict(pagina=545, card=1, codigo=_c, descricao=f"CONTRA PESO GARRA BAIXA {_g}", cod_ref="", variacoes="", aplicacao="", montadora="", marca="",
                    info=f"Embalagem {_e:03d} unidades | Contrapeso para balanceamento de roda comum | Material de ferro zincado", _titulo="CONTRA PESO GARRA BAIXA",
                    foto_spec={"rect": [31, 96, 202, 224]}))
for _c, _d, _f, _kw in [
        ("8101579", "CONTRA PESO ADESIVO 10/5", [34, 224, 153, 325], dict(info="Embalagem 100 unidades | Contrapeso para balanceamento de roda em liga leve | Material de ferro zincado | Fita colante dupla face")),
        ("8100003", "TAMPA PLASTICA BICO PNEU", [33, 335, 92, 407], {}), ("8101976", "PITO P PNEU ARO 13 S CAMARA", [234, 336, 340, 383], {}),
        ("8101722", "PITO P PNEU ARO 14 S CAMARA", [412, 336, 518, 383], {}), ("8106180", "BICO PNEU AGRICOLA BASE FERRO TR-618A", [53, 414, 150, 451], {}),
        ("9963145", "RETIFICA PNEUMATICA 1/4 2400 RPM", [247, 414, 341, 500], {}),
        ("10019122", 'JOGO SOQUETES 1/2" 22 PECAS ESTRIADO', [392, 411, 494, 507],
         dict(info='Maleta que proporciona organização | Aço cromo vanádio | Encaixe de 1/2" | 22 peças: 1 extensão 5", 1 extensão 10", 1 catraca reversível de 1/2", 1 cabo T 10", '
                   "18 soquetes estriados 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 24, 27, 30, 32 mm")),
        ("6010819", "JOGO DE CHAVES BIELA 12 PÇS (8 - 19 MM)", [32, 539, 160, 619], dict(marca="Riosul")),
        ("9934855", "CHAVE RODA CRUZ 17X19 X 13/16 23MM /20 | 17X19 X 21X23 350MM", [216, 542, 303, 616], {}),
        ("6013500", "CABO DE TRANSMISSÃO DE CARGA TIPO CHUPETA 300A", [388, 539, 486, 632], dict(marca="Riosul", info="Promoção")),
        ("6010022", "FILTRO REGULADOR AR 1/2 PROFISSIONAL", [215, 673, 270, 802], dict(marca="Sigma")),
        ("9941345", 'CONJUNTO LUBRIFIL 1/2" PROFISSIONAL', [398, 675, 472, 759], dict(marca="Sigma", info="Conjuntos Lubrifil servem para filtragem, regulagem de pressão do ar comprimido e lubrificação de toda linha pneumática"))]:
    X(545, _c, _d, _f, **_kw)
NOTAS.append("Pág. 545: o código 9934855 está impresso em duas chaves de roda cruz com medidas diferentes; lançado uma vez com as duas medidas.")
