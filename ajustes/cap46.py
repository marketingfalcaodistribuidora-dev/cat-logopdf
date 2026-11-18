# Capítulo 46 - Pinos, Prisioneiros, Parafusos, Tuchos e Machos (págs. 507-512)
# Listas por caixa: cada caixa (seção) = 1 produto com os códigos como itens; código+descrição via tabela_livre.ler_pagina,
# seções dadas à mão (retângulos pelas bordas das molduras); foto = maior imagem da seção.
import re

from tabela_livre import _spans, ler_pagina

TIPOS = [(r"PINO ELASTICO", "PINO ELÁSTICO"), (r"CONTRA PINO", "CONTRA PINO"), (r"PRIS", "PRISIONEIRO"),
         (r"TUCHO", "TUCHO"), (r"MACHO|VIRA MACHO|COSSINETE", "MACHO / COSSINETE"), (r"PORCA", "PORCA"),
         (r"ARRUELA", "ARRUELA"), (r"PF|PARAFUSO", "PARAFUSO")]
AJ = {}
ADD = []
NOTAS = ["Págs. 507-512: cada caixa/lista da página virou 1 produto com os códigos como itens."]
MANUAIS = set(range(507, 513))
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


# 507 (pág. impressa 506)
S(507, [("PINO ELASTICO (GRUPO 475)", [25, 87, 570, 448]), ("CONTRA PINO", [25, 448, 570, 805])], LN(507, [25, 87, 300, 340]))
for _r in ADD:
    if _r["pagina"] == 507 and _r["codigo"] == "4750887":
        _r["montadora"] = "Volvo"
NOTAS.append("Pág. 507: 4750660 e 4750890 estão impressos com a mesma medida (pino elástico 06 x 60); 47005100, 47008100 e "
             "47010100 (contra pino) têm 8 dígitos.")
# 508 (pág. impressa 507)
S(508, [("PRISIONEIRO", [25, 87, 286, 457]), ("PRIS. SM 08X10 SOB MEDIDA", [25, 457, 286, 690]),
        ("PORCA PRISIONEIRO CUBO 1113", [286, 87, 570, 164]), ("CONE PRISIONEIRO", [286, 164, 570, 243]),
        ("PRISIONEIRO CAPA SECA / COMP / COROA", [286, 243, 570, 376]), ("PRIS. COMP UNC X UNF", [286, 376, 570, 493]),
        ("PRIS.COM PORCA FLUTUANTE 1113", [286, 493, 570, 589]), ("PRIS. SIMPLES", [286, 589, 570, 690]),
        ("BARRA ROSCADA ZB 1MT", [25, 690, 570, 805])], LN(508, [286, 376, 570, 805]))
for _r in ADD:
    if _r["pagina"] == 508 and _r["_titulo"] in ("PRISIONEIRO", "PRIS. SM 08X10 SOB MEDIDA"):
        _r["foto_spec"] = {"rect": [303, 246, 560, 303]}
        _r["info"] = "Foto ilustrativa (a lista não tem foto própria)"
NOTAS.append("Pág. 508: vários prisioneiros 'sob medida' têm código de 7, 8 ou 9 dígitos (ex.: 250081031, 2506269, 10027930); as "
             "listas da coluna esquerda não têm foto própria (usada a foto de prisioneiro da página).")
# 509 (pág. impressa 508): tabelas motocicleta (marca/modelo impressos como imagem, transcritos)
TIPOS.insert(0, (r"^PORCA FLANGEADA", "PORCA FLANGEADA"))
_HCT = "Honda CG / Titan / Strada / Cargo"
_HB = "Honda Bros 125/150 - 2003/.. / CRF 110/150R/230/250R - 2008.. / Tornado 250 - 2002/2008"
for _c, _bit, _passo, _mm, _apl, _ch, _alt, _fl, _emb, _f, _ref in [
        ("3610062", "M6", "1,00", "Honda", "Diversas", "10", "6,10", "13", "20", [491, 192, 542, 236], "2808 6"),
        ("3610061", "M7", "1,00", "Honda CG / Titan / Strada Cargo", "Fixação mesa superior do guidão", "10", "7,10", "16,3", "10",
         [491, 192, 542, 236], "54788"),
        ("3610060", "M8", "1,25", "Honda", "Diversas", "12", "7,70", "17", "10", [491, 192, 542, 236], "30 621"),
        ("3610064", "M10", "1,25", "Honda CG / ML / Turuna / Titan / Titan Fan / XL 125 / XLS 125 / Strada / Cargo",
         "Prisioneiro da coroa", "14", "9,10", "19,40", "10", [491, 192, 542, 236], "33912"),
        ("3610063", "M12", "1,25", "Honda CG / Titan / ML / Turuna", "Volante", "17", "11,10", "24", "2", [491, 192, 542, 236], "36340"),
        ("3610008", "M8", "1,25", _HB, "Prisioneiro da coroa", "13", "11,10", "17,90", "10", [490, 274, 544, 334], "5007 0"),
        ("3610012", "M12", "1,25", _HCT + " / Biz", "Eixo dianteiro", "19", "13,00", "24,20", "2", [490, 274, 544, 334], "65517"),
        ("3610014", "M14", "1,50", _HCT + " / Biz", "Eixo traseiro", "22", "15,50", "26,50", "1", [490, 274, 544, 334], "65524")]:
    ADD.append(dict(pagina=509, card=90 + len(ADD), codigo=_c, descricao=f"PORCA FLANGEADA P/ MOTOCICLETA {_bit} X {_passo}",
                    cod_ref="", variacoes="Cód. fornecedor: " + _ref, aplicacao=f"{_mm} | {_apl}", marca="", montadora="Honda",
                    info=f"Bitola: {_bit} | Passo: {_passo} | Chave: {_ch} | Altura: {_alt} | Ø da flange máx.: {_fl} | Emb.CT(s): {_emb}",
                    _nao_agrupar=True, foto_spec={"rect": _f}))
for _c, _d, _mm, _apl, _f, _ref, _m in [
        ("2740176", "P SX FLG M8 X 1,25 (MA) X 20 RI8.8 CH12 ZB", "Honda Biz / Titan / Pop todos os modelos", "Parafuso do estribo",
         [481, 422, 557, 454], "819295", "Honda"),
        ("2780829", "PRIPFCAB ESCSX INT M8 x 1,25 (MA) x 29 8.8", _HB, "Prisioneiro da coroa", [483, 459, 557, 493], "816911", "Honda"),
        ("2788290", "CJPRI M8 X 1,25 (MA) x 29 RP8.8 + PO SX NYF C.8", _HB, "Prisioneiro da coroa", [483, 495, 557, 532], "6020 71", "Honda"),
        ("2787447", "PRISIONEIRO M10 x 1,25 x 36,5 mm",
         "Honda CG / ML / Turuna Titan / Titan Fan / XL 125 XLS 125 / Strada / Cargo", "Fixação da coroa ao cubo",
         [482, 535, 557, 567], "800 095", "Honda"),
        ("2787448", "CONJ.PRISIONEIRO M10 x 1,25 x 36,5 mm + POSX FLGM10 x 1,25",
         "Honda CG / ML / Turuna Titan / Titan Fan / XL 125 XLS 125 / Strada / Cargo", "Fixação da coroa ao cubo",
         [487, 573, 557, 606], "600 305", "Honda"),
        ("5080051", "PF SX M8 X 1,25 (MA) X 35 mm MA RP Ch.17H. 4", "Yamaha YBR", "Fixação da coroa ao cubo", [478, 608, 557, 645],
         "815242", "Yamaha"),
        ("2780089", "PF SX M10 X 1.25 (MA) X 38 mm PSCØ12 mm", "Honda / Yamaha / Suzuki", "Cavalete lateral", [480, 647, 556, 682],
         "81412 2", "Honda, Yamaha, Suzuki"),
        ("2780088", "CJ PF SX M10 X 1.25 (MA) X 38 mm PSCØ12 mm + POSX NYB M10 x 1,25", "Honda / Yamaha / Suzuki", "Cavalete lateral",
         [482, 686, 556, 720], "6020 33", "Honda, Yamaha, Suzuki"),
        ("2781215", "PF SX FLG M12X1,50X15", "CG / BIS / YBR / TWISTER", "Bujão do óleo", [503, 742, 557, 781], "817765",
         "Honda, Yamaha"),
        ("2781315", "PF SX FLG M13X 1,50 X 15", "CG / BIS / YBR / TWISTER", "Bujão do óleo", [503, 742, 557, 781], "820130",
         "Honda, Yamaha")]:
    ADD.append(dict(pagina=509, card=90 + len(ADD), codigo=_c, descricao=_d, cod_ref="", variacoes="Cód. fornecedor: " + _ref,
                    aplicacao=f"{_mm} | {_apl}", marca="", montadora=_m, info="", _nao_agrupar=True, foto_spec={"rect": _f}))
NOTAS.append("Pág. 509 (motocicleta): o número em preto sob o código vermelho (ex.: 2808 6, 819295) é o código do fornecedor (em "
             "similares); a última linha (PF SX FLG M14X1,50X15, bujão do óleo, nº 822516i) não tem código vermelho e não foi lançada.")
# 510 (pág. impressa 509)
S(510, [("PF.FLANGE CH 08", [25, 140, 330, 565]), ("PF.FLANGE CH 10 / CH 12", [330, 140, 570, 385]),
        ("PF.FLANGE CH 12 08 X 20", [330, 385, 455, 565]), ("PF.FLANGE CH 12 08 X 25", [455, 385, 570, 565]),
        ("PORCA FLANGE", [25, 565, 570, 805])],
  {"2740020": "PF.FLANGE CH 12 08 X 25", "2740176": "PF.FLANGE CH 12 08 X 20"})
NOTAS.append("Pág. 510: 2740176 e 2740020 aparecem na lista e em card próprio; as porcas flange 3610062/61/60/64/63/08/12/14 "
             "também estão na tabela de motocicleta da pág. 509; 36112175 tem 8 dígitos.")
# 511 (pág. impressa 510): tuchos (um produto por card)
for _c, _d, _f in [
        ("6630418", "05 X 08 X 15 IN 1,0 X EX 1,25", [81, 128, 141, 163]), ("6630419", "05 X 10 X 15 IN 1,0 EX 1,5", [258, 120, 322, 164]),
        ("6630031", "06 X 08 X 15 IN1,00 EX 1,25", [496, 118, 561, 162]), ("6630032", "06 X 10 X 15 INT 1,0 EXT 1,5", [88, 197, 149, 232]),
        ("6630373", "07 X 10 X 15 IN 1,00 EX 1,50", [261, 196, 330, 242]), ("6630030", "08 X 10 X 16 IN 1,25 EX 1,25", [457, 201, 513, 232]),
        ("6635005", "08 X 10 X 16 IN1,00 EX1,25 FIRE", [31, 292, 90, 325]),
        ("6635006", "08 X 10 X 16 INTERNO 1,25 EXTERNO 1,00", [127, 252, 193, 289]),
        ("6630810", "08 X 10 X 20 IN 1,25 EX 1,25", [249, 274, 339, 328]), ("6630372", "08 X 12 X 16 IN1,25 EX 1,50", [447, 277, 517, 321]),
        ("6630375", "08 X 12 X 20 IN1,25 EX 1,50", [68, 363, 161, 420]), ("6630090", "08 X 12 X 26 IN 1,25 EX 1,5", [238, 360, 347, 422]),
        ("6630284", "08 X 14 X 26 IN 1,25 EX 1,5", [424, 363, 516, 421]),
        ("6630816", "08 X 16 X 26 IN 1,25 EX 1,5 PASSANTE S/M P/GOL", [42, 462, 137, 538]),
        ("6631012", "10 X 12 X 20 IN 1,0 EX 1,25 VELA BIZ", [185, 460, 292, 525]), ("6630912", "09 X 12 X 26 IN 1,25 EX 1,5", [319, 463, 420, 522]),
        ("6631226", "10 X 12 X 21 IN1,25 EX1,25", [463, 463, 556, 516]), ("6631142", "10 X 14 X 15 VELA BIZ IN 1,0 X EX 1,50", [63, 570, 126, 628]),
        ("6631410", "10 X 14 X 21 IN1,0 EX1,5", [192, 562, 270, 626]), ("6630285", "10 X 14 X 26 IN1,25 EX1,5", [316, 565, 418, 627]),
        ("6631014", "10 X 14 X 26 IN1,5 EX1,5", [452, 553, 555, 636]), ("6630374", "10 X 16 X 26 IN1,5 EX1,5", [75, 657, 157, 710]),
        ("6630276", "12 X 16 X 20 IN1,5 EX 1,5 BUJAO OLEO", [318, 654, 385, 712]), ("6630175", "12 X 16 X 26 IN1,75 EX1,50", [430, 655, 510, 708]),
        ("6630106", "12 X 16 X 21 IN1,25 X EX 1,5", [42, 744, 114, 803]), ("6632148", "14 X 18 X 16 IN 1,25X1,50", [199, 741, 266, 801]),
        ("6631418", "14 X 18 X 21 IN 1,25 EXT 1,50", [333, 741, 395, 801]), ("6631420", "14 X 20 X 16 IN1,25 EXT 1,5", [472, 741, 541, 800])]:
    X(511, _c, "TUCHO " + _d, _f, info="Campeão de venda" if _c == "6630031" else "")
# 512 (pág. impressa 511)
S(512, [("MTX - VIRA MACHO M6 A M20", [25, 87, 570, 190]), ("JG MACHOS MANUAIS COSSINETE", [25, 190, 570, 415]),
        ("JG MACHO ACO RAPIDO MILIMETRO", [25, 415, 395, 690]), ("JG MACHO ACO RAPIDO POLEGADA", [25, 690, 395, 805])],
  {"6217731": "JG MACHOS MANUAIS COSSINETE M3-M12 / 020 PCS"})
for _r in ADD:
    if _r["pagina"] != 512:
        continue
    if _r["codigo"] == "6212055":
        _r.update(marca="MTX", foto_spec={"rect": [70, 114, 555, 185]})
    elif _r["codigo"] == "6217731":
        _r.update(foto_spec={"rect": [315, 198, 554, 403]},
                  info="Composição: cossinetes M3 x 0,5 mm, M4 x 0,7 mm, M5 x 0,8 mm, M6 x 1 mm, M7 x 1 mm, M8 x 1,25 mm, M10 x 1,5 mm, "
                       "M12 x 1,75 mm, 1/8 NPT27 | Machos M3 x 0,5 mm, M4 x 0,7 mm, M5 x 0,8 mm, M6 x 1 mm, M7 x 1 mm, M8 x 1,25 mm, "
                       "M10 x 1,5 mm, M12 x 1,75 mm, 1/8 NPT27 | Porta cossinete: M3-M12 | Porta vira macho: M3-M12 | Estojo plástico")
    else:
        _r["foto_spec"] = {"rect": [395, 488, 552, 760]}
# 510: 2740176 e 2740020 ficam só nos cards próprios; a lista CH 10 usa a foto do parafuso flange da página
ADD[:] = [r for r in ADD if not (r["pagina"] == 510 and r["card"] == 2 and r["codigo"] in ("2740176", "2740020"))]
for _r in ADD:
    if _r["pagina"] == 510 and _r["card"] == 2:
        _r["foto_spec"] = {"rect": [43, 132, 286, 248]}
