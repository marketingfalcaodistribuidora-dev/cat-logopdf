# Capítulo 50 - Parafusos e Porcas de Roda (págs. 531-542)
# Listas por caixa: cada caixa (seção) = 1 produto com os códigos como itens; código+descrição via tabela_livre.ler_pagina,
# seções dadas à mão (retângulos pelas bordas das molduras); foto = maior imagem da seção.
import re

from tabela_livre import _spans, ler_pagina

TIPOS = []
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(531, 543))
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


TIPOS += [(r"^PORCA", "PORCA DE RODA"), (r"^PF RODA", "PARAFUSO DE RODA")]
NOTAS.append("Págs. 531-542: a referência ZM do card está em similares; porcas repetidas em várias páginas foram lançadas uma vez, com todas as páginas.")
_GM, _FD, _VW, _FT = "GM-Chevrolet", "Ford", "Volkswagen", "Fiat"
_P31 = ("0682901231", "PORCA DE RODA M12-1,5 X CH/SW 19 H31", "ZM 29.012.31")
_P34 = ("0682901234", "PORCA DE RODA M12-1,5 X CH/SW 19 H35", "ZM 29.012.34")
_APL_FIAT = "Fiat 147, Brava, Elba, Fiorino, Idea, Marea, Palio, Palio Weekend, Prêmio, Siena, Strada, Uno"
for _p, _c, _d, _z, _a, _m, _f in [
        (531, "0684071662", 'PF RODA DIA/TRA 7/16"-20UNF X 38,1 / 44,5 CH/SW 3/4" H36', "ZM 40.716.62", "A10, C10, D10", _GM + ", Ford", [307, 90, 474, 156]),
        (531, "683071602", 'PF RODA D/T 7/16"-20UNF X 38,1 / 44,5 A10/C10', "ZM 30.716.02", "A10, C10, D10", _GM, [292, 201, 452, 258]),
        (531, "0684001235", "PF RODA TRA M12-1,5 X 42 / 49 CH/SW 19 H31", "ZM 40.012.35", "Blazer, D20, S10", _GM, [288, 318, 458, 372]),
        (531, "683001231", "PF RODA TRA M12-1,5 X 42 / 47 BLAZER/D20/S10", "", "Blazer, D20, S10", _GM, [29, 436, 184, 496]),
        (531, _P31[0], _P31[1], _P31[2],
         "Ford: Courier, EcoSport, Escort, Fiesta, Focus, Ka, Mondeo, Verona; GM: Blazer, Caravan, Chevette, Chevy, D20, Marajó, Opala, S10, Silverado; VW: Logus, Pointer",
         "Ford, GM-Chevrolet, Volkswagen", [443, 495, 476, 544]),
        (531, "0683001262", "PF RODA DIA/TRA M12-1,5 X 52 / 56,5", "ZM 300.12.62", "Cobalt 2011/2019, Onix 2012, Prisma 2013/2019, Spin 2012, Tracker 2013/2018", _GM, [226, 591, 386, 636]),
        (531, _P34[0], _P34[1], _P34[2], "Aveo, Captiva 2008, Cobalt 2012, Cruze 2012, Malibu 2010/2012, Onix 2012, Prisma 2013, S10 2012, Sonic 2012/2015, Spin 2013, Tracker 2013, Trailblazer 2013",
         _GM, [428, 743, 465, 795]),
        (532, "0684001241", "PF RODA DIA/TRA M12-1,5 X 51 / 55,5 CH/SW 19 H35", "ZM 40.012.41",
         "Captiva 2008, Cobalt 2011, Cruze (diant.) 2011, Onix (diant.) 2012, Prisma (diant.) 2013, S10 (tras.) 2012, Sonic (diant.) 2012, Spin 2012, Tracker (diant.) 2013", _GM, [188, 105, 384, 169]),
        (532, "0684001232", "PF RODA DIA/TRA M12-1,5 X 36 / 41 CH/SW 19 H14", "ZM 40.012.32", "Blazer (diant.), Caravan 1980, Chevette, D20 (diant.), Opala 1980, S10 (diant.)", _GM, [220, 346, 362, 419]),
        (532, "683001230", "PF RODA DIA M12-1,5 X 36 / 41 BLAZER/D20/S10", "", "Blazer, D20, S10", _GM, [35, 597, 183, 675]),
        (532, "0682901230", "PORCA DE RODA M12-1,5 X CH/SW 19 H31", "ZM 29.012.31", "", "", [202, 710, 252, 785]),
        (532, "682901221", "PORCA RODA M12-1,5 X CH/SW 19 H14 FIESTA",
         "", "Ford: Courier, Fiesta Street, Fiesta 1993, Focus, Ka; GM: Caravan 1980, Chevette, Opala 1980; Toyota: Bandeirante", "Ford, GM-Chevrolet, Toyota", [45, 707, 95, 761]),
        (533, "684071601", 'PF RODA D/T 7/16"-20UNF X 32,5 / 39 CH 3/4 D10', "", "A10, C10, D10", _GM, [34, 93, 212, 175]),
        (533, "682971601", 'PORCA RODA 7/16"-20UNF X CH/SW 3/4" H14,5', "", "A10, C10, D10, Opala 1978, Veraneio 1989", _GM, [397, 182, 462, 239]),
        (533, "683001233", "PF RODA D/T M12-1,5 X 22 / 47,5 CH 17 CELTA", "",
         "GM: Agile 2009/2014, Astra, Celta, Corsa, Kadett 1993, Meriva, Montana, Monza 1993, Omega, Prisma 2006/2012, Tigra, Vectra, Zafira; Renault: Clio, Logan", "GM-Chevrolet, Renault", [30, 294, 220, 385]),
        (533, "683001232", "PF RODA TRA M12-1,5 X 46 / 52 SILVERADO/D20", "", "Silverado, D20 1993", _GM, [30, 520, 189, 581]),
        (533, "683001238", "PF RODA D/T M12-1,5 X 51 / 55,5 ONIX/PRISM.", "",
         "Aveo (diant.), Captiva 2008, Cobalt 2011, Cruze (diant.) 2011, Onix (diant.) 2012, Prisma (diant.) 2013, S10 (tras.) 2012, Sonic (diant.) 2012, Spin 2012, Tracker (diant.) 2013", _GM, [27, 655, 221, 707]),
        (534, "683001265", "PF RODA TRA M12-1,5 X 36,5 / 41 FIESTA", "", "Ford: EcoSport, Fiesta Street, Fiesta 2003, Focus, Ka; VW: Logus, Pointer", "Ford, Volkswagen", [36, 90, 181, 150]),
        (534, "683001266", "PF RODA DIA M12-1,5 X 40,5 / 45 FIESTA STREET", "Porca ZM 29.012.30",
         "Ford: Courier, EcoSport, Escort 1993, Fiesta Street, Fiesta 2003, Focus, Ka, Mondeo 1995/2006, Verona 1993; VW: Logus, Pointer", "Ford, Volkswagen", [40, 269, 185, 329]),
        (534, "0683010203", 'PF RODA D/T DIA/TRA 1/2"-20UNF X 54 / 58,5 F1000', "Porca ZM 29.102.01", "F1000", _FD, [32, 515, 224, 580]),
        (534, "682910201", 'PORCA RODA 1/2"-20UNF X CH/SW 13/16" F-1000', "", "F100 1967/1987, F1000 1980/1993", _FD, [422, 589, 474, 638]),
        (534, "683010201", 'PF RODA D/T 1/2"-20UNF X 44,5 / 49 F1000', "Porca ZM 29.102.01", "F100 1967/1987, F1000 1980/1993", _FD, [30, 660, 225, 735]),
        (535, "0683001200", "PF RODA DIA/TRA M12-1,5 X 24 / 45 CH/SW 17", "ZM 30.012.00", "Gol, Lupo, Parati, Passat, Santana, Voyage", _VW, [209, 103, 329, 163]),
        (535, "0683001400", "PF RODA DIA/TRA M14-1,5 X 19 / 38 CH/SW 19", "ZM 30.014.00", "Brasília, Fusca, Kombi", _VW, [210, 202, 330, 268]),
        (535, "683001402", "PF RODA D/T M14-1,5 X 27 / 48 CH/SW 17 VOLKS", "",
         "Audi: A3 1997, A4 1995, A6 2011, TT 1998; Seat: Cordoba 1995/2002, Ibiza 1995/2002; VW: Bora 2001/2012, CrossFox 2005, Eos 2009/2010, Fox 2003, Golf 1994, Golf 2015, Jetta 2006, "
         "Jetta Variant 2008/2013, New Beetle 2000/2011, Passat 1994, Polo 2002/2014, SpaceCross 2012/2017, SpaceFox 2006, Suran, T-Cross 2019, Tiguan 2009, Vento", "Audi, Seat, Volkswagen", [29, 351, 120, 474]),
        (536, "0684001291", "PF RODA DIA M12-1,5 X 41 / 46 CH/SW 21 H36", "ZM 40.012.91", "L 300 (dianteiro)", "Mitsubishi", [179, 101, 339, 169]),
        (536, "0684001293", "PF RODA TRA M12-1,5 X 36 / 41 CH/SW 21 H36", "ZM 40.012.93", "L 300 (traseiro)", "Mitsubishi", [184, 206, 336, 274]),
        (536, "0684001215", "PF RODA TRA M12-1,5 X 44,5 / 49,5 CH/SW 21 H47", "ZM 40.012.15", "Fortuner, Hilux 2005, Hilux SW4 2005", "Toyota", [188, 311, 340, 371]),
        (536, "0684001229", "PF RODA TRA M12-1,5 X 36 / 41 CH/SW 21 H47", "ZM 40.012.29", "Corolla 2008", "Toyota", [176, 401, 343, 477]),
        (536, "683001224", "PF RODA TRA M12-1,5 X 44,5 CH/SW 21 SIMPLES", "ZM 30.012.24", "Pick-up 4x4, SW4", "Toyota", [174, 502, 345, 580]),
        (536, "682901213", "PORCA AC SX CALOTA M12 X 1,50 X CL8 PRETA", "", "Corolla, Tacoma, SW4", "Toyota", [261, 612, 311, 655]),
        (536, "682901223", "PORCA AC SX CALOTA M12 X 1,50 X CL8 CRO", "", "Corolla (08/...), Fortuner, Hilux (05/...), Hilux SW4 (05/...), RAV4 / Tacoma (08/14)", "Toyota", [242, 662, 308, 700]),
        (536, "0683001480", "PF RODA DIA/TRA M14-1,5 X 30 / 60 CH/SW 19", "ZM 30.014.80", "Master", "Renault", [210, 721, 357, 797]),
        (538, "0683001244", "PF RODA D/T M12-1,25 X 22 CH/SW 19 PALIO WEEK", "", _APL_FIAT, _FT, [43, 90, 182, 164]),
        (538, "5052148", "PF RODA FIAT 12 X 1,25 X 26,5 CH 19 PALIO WEEKEND", "ZM 30.012.40", _APL_FIAT, _FT, [42, 289, 209, 356]),
        (538, "683001268", "PF RODA D/T M12-1,25 X 22 / 48,5 CH/SW 19", "", "Argo 2017, Bravo 2010, Cronos 2018, Fiorino 2013, Grand Siena 2012, Palio 2010, Stilo 2002/2010, Uno 2010", _FT, [204, 476, 372, 552]),
        (538, "0683001242", "PF RODA DIA/TRA M12-1,25 X 37 / 62 CH/SW 19", "ZM 30.012.42", _APL_FIAT, _FT, [206, 625, 371, 679]),
        (539, "684001286", "PF RODA D/T L/D M12-1,5 X 40 / 45 CH/SW 21 KIA", "", "Asia: Topic, Towner; Kia: Besta, Sportage", "Asia, Kia", [181, 128, 326, 201]),
        (539, "684001287", "PF RODA D/T L/D M12-1,5 X40 CH/SW 21 KIA", "", "Asia: Topic, Towner; Kia: Besta, Sportage", "Asia, Kia", [184, 252, 319, 320]),
        (539, "684001288", "PF RODA D/T L/E M12-1,5 X 40 / 45 CH/SW 21 KIA", "", "Asia: Topic, Towner; Kia: Besta", "Asia, Kia", [196, 374, 361, 457]),
        (539, "684001289", "PF RODA D/T L/E M12-1,5 X40 CH/SW 21 H20", "", "Asia: Topic, Towner; Kia: Besta", "Asia, Kia", [185, 531, 343, 608]),
        (539, "684001488", "PF RODA D/T M14-1,5 X 45,5 / 51,5 CH/SW 22 H1", "", "Kia Bongo K2400, Bongo K2700", "Asia, Kia", [154, 708, 334, 797]),
        (540, "6864004", "PF RODA FIAT ORIG M12 X 1,25 X 22 CH19 16 PÇS", "", "", _FT, [56, 160, 162, 202]),
        (540, "6864003", "PF RODA FIAT M12 X 1,25 X 27 CH19 16 PECAS", "", "", _FT, [250, 174, 356, 216]),
        (540, "6864006", "PF RODA PALIO M12 X 1,25 X 29 16PÇS", "", "", _FT, [441, 161, 547, 203]),
        (540, "6864005", "PF RODA FIAT LONGO M12 X 1,25 X 36 CH19 16PÇS", "", "", _FT, [60, 330, 166, 372]),
        (540, "6864001", "PF RODA MULT LONGO M12 X 1,5 X 36 CH19 16PÇ", "", "", "", [243, 330, 349, 372]),
        (540, "6864000", "PF RODA MULT CONICO M12 X 1,5 X 26 CH19 16PÇ", "", "", "", [421, 331, 527, 373]),
        (540, "6850031", "PF RODA MULT CONICO VW PG 16PÇS", "", "", _VW, [63, 519, 173, 562]),
        (540, "6870051", "PORCA RODA FORD KA/FIESTA 16 PÇS", "", "Ka, Fiesta", _FD, [401, 500, 558, 587]),
        (540, "6864032", "PORCA RODA M12 X 1,5 X 30 HB20 CH21 16PÇS", "", "HB20", "Hyundai", [53, 705, 189, 793]),
        (540, "6892476", "PORCA RODA MITSUBISHI", "", "", "Mitsubishi", [247, 686, 356, 787]),
        (540, "6890977", "PORCA RODA M12-1,5 X 37 L-200 TRITON", "", "L-200 Triton", "Mitsubishi", [410, 684, 548, 776]),
        (542, "0682901489", "PORCA DE RODA M14-1,5 X CH/SW 22 H19", "ZM 290.1489", "Bongo K2400, Bongo K2700", "Kia", [183, 117, 282, 212]),
        (542, "0682910261", 'PORCA DE RODA 1/2"-20UNF X CH/SW 13/16" H36', "ZM 291.02.61",
         "Chrysler-Dodge: Dakota 1998/2002; Dodge: 1800 1972/1976, Polara 1976/1981; Ford: F100 1957/1985, F1000 1983/1998, F75 1967/1982, Galaxie 1967/1983, Maverick 1973/1979, Rural", "Chrysler, Dodge, Ford", [281, 246, 390, 323]),
        (542, "682910260", 'PORCA RODA 1/2"-20UNF X CH/SW 3/4" H36 RANGE', "", "Ford: Edge 2008, Explorer 1993/2006, Ranger 1994/2012; Jeep: Cherokee", "Ford, Jeep", [258, 670, 367, 737])]:
    X(_p, _c, _d, _f, variacoes=_z, aplicacao=_a, montadora=_m)
_MESMOS = {"0682901231": (532, 533, 541), "0682901234": (532, 533, 541), "0682901230": (541,), "682901221": (534, 541), "682971601": (541,),
           "682901223": (537,), "683001224": (537,), "682910201": (542,)}
_B = {r["codigo"]: r for r in ADD}
for _c, _ps in _MESMOS.items():
    for _p in _ps:
        ADD.append(dict(_B[_c], pagina=_p, card=900 + len(ADD)))
NOTAS.append("Pág. 531: 0682901231 está impresso como '068.2901231'; 0682901230 e 0682901231 trazem a mesma ref. ZM 29.012.31. Págs. 536/537: 683001224 e 682901223 "
             "aparecem nas duas páginas. Pág. 533: 683001233 e pág. 538: 5052148 têm selo 'campeão de vendas'.")
