# Capítulo 23 - Balanças, Suportes e Pinos (págs. 315-341)
import re

from cards_grade import ler

TIPOS = [(r"COXIM", "COXIM"), (r"BATENTE", "BATENTE"), (r"BALAN[ÇC]A", "BALANÇA"), (r"BUCHA", "BUCHA"),
         (r"DESLIZANTE", "DESLIZANTE DE SUSPENSÃO"), (r"SAPATA", "SAPATA"), (r"SUP(ORTE)?\b|SUP\.", "SUPORTE"),
         (r"PINO", "PINO"), (r"TENSOR|TIRANTE", "TENSOR / TIRANTE"), (r"ARRUELA|CALCO|CALÇO", "ARRUELA / CALÇO"),
         (r"MANCAL", "MANCAL"), (r"GRAXEIRO|PINO GRAX", "GRAXEIRO"), (r"PORCA", "PORCA"), (r"\bPF\b|PARAFUSO", "PARAFUSO"),
         (r"ROTULA|RÓTULA", "RÓTULA"), (r"FLANGE", "FLANGE"), (r"ALGEMA", "ALGEMA")]
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(315, 342))
for _p in range(315, 342):
    ADD.extend(ler(_p))


def F(p, c, **kw):
    regs = [r for r in ADD if r["pagina"] == p and r["codigo"] == c]
    assert regs, f"{c} não está na pág. {p}"
    for r in regs:
        r.update(kw)


def T(p, c, **kw):
    base = dict(cod_ref="", variacoes="", aplicacao="", info="", montadora="")
    base.update(kw)
    F(p, c, **base)


def N(p, c, descricao, rect, **kw):
    ADD.append(dict(dict(pagina=p, card=90 + len(ADD), codigo=c, descricao=descricao, marca="", cod_ref="", variacoes="",
                         aplicacao="", info="", montadora="", _nao_agrupar=True, foto_spec={"rect": rect}), **kw))


def X(p, c):
    ADD[:] = [r for r in ADD if not (r["pagina"] == p and r["codigo"] == c)]


def MP(p, montadora, exceto=()):
    for r in ADD:
        if r["pagina"] == p and r["codigo"] not in exceto:
            r["montadora"] = montadora


MB, VW, FD, SC, VO = "Mercedes-Benz", "Volkswagen", "Ford", "Scania", "Volvo"
TH = "Thor"
_OBS = "OBS: ao substituir os coxins verificar o Nº original da peça; em caso de dúvida, verificar o Nº do chassi e consultar concessionária"
# 315
T(315, "50613081", descricao="COXIM DIANT SUSP MERCEDES BASE 28MM", marca=TH, montadora=MB, cod_ref="941.241.8713",
  variacoes="REF REI: R-3317 / MESMO R-3214", aplicacao="Axor: 2035S - 2036S - 2040S - 2044S - 2533 - 2535 - 2540S 6X2 - 2640 6X2 - "
  "2640 6X4 rodoviário/canavieiro - 2644S 6X2 - 3340S - 3344 - 3344K - 3344S - 4140 - 4140K - 4144 / Actros: 2631B - 2648B - 3231B - "
  "3248B - 3331B - 3348B - 4140B - 4141B - 4148B - 4844", info="Largura do coxim 122 mm | Espessura da base de fixação do coxim no "
  "chassi 28 mm | Rosca M 18 x 1,5 e rosca M 14 x 1,5 | " + _OBS)
T(315, "50613082", descricao="COXIM SUSP MOTOR CAMBIO MERCEDES - BASE 20,5MM", marca=TH, montadora=MB, cod_ref="934.241.0613",
  variacoes="REF REI: R-3504", aplicacao="Actros: 2546 6X2 - 2546 6X4 - 2651 6X4 - 2655 6X4 - 4160 8X8 - 4844K 8X4",
  info="Largura do coxim 117 mm | Espessura da base de fixação do coxim no chassi 20 mm | Rosca M18 x 1,5 e rosca M14 x 1,5 | " + _OBS)
T(315, "50913066", descricao="BATENTE DE MOLA VOLVO", marca=TH, montadora=VO, cod_ref="1629553 / 3090971 / 1089501 / 20390836",
  variacoes="MESMA IABV 3070", aplicacao="Volvo: N 10/NL 10 6X2-6X4/NL10S/N 12/NL12 6X2-6X4/NL 12S/FM12 380 6X4/NH 12 420 6X4/F 7/F 10/"
  "F 12/F16/FH12/FH 16/FL 7/FL 10/traçados", info="Material: tubo SAE 1020 e borracha 70 shore A | Dimensões: comprimentos 200mm x "
  "210mm x altura 151mm x larguras 150mm x 135mm")
T(315, "50613086", descricao="COXIM DIANTEIRO DA SUSP MOTOR DC-OC13 - SCANIA L/P/G/R/S", marca=TH, montadora=SC,
  cod_ref="2611114 / 2222211")
# 316 (Randon / Facchini - Thor)
RD, FC = "Randon", "Facchini"
X(316, "3740001"); X(339, "3740001")
T(316, "50913034", descricao="BUCHA SUSPENSAO PNEUMATICA RANDON 40MM INT", marca=TH, montadora=RD, cod_ref="2102009133 / 212009133",
  variacoes="MESMA IABV 3392 (4983392)", aplicacao="Carretas Randon Nova", foto_spec={"rect": [20, 85, 293, 262]},
  info="Material: tubo SAE 1020 e borracha 70 shore A | Dimensões: Ext. 152mm x Int. 40mm x Comprimento 132mm")
T(316, "50913063", descricao="BUCHA SUSPENSAO PNEUMATICA CAR RANDON FS250", marca=TH, montadora=RD, cod_ref="100000133571",
  variacoes="Referências 3392-01 / 3559 / 70000035 / 212009133 / 100000133571", aplicacao="Carretas Randon Nova 2014 em diante",
  foto_spec={"rect": [293, 85, 570, 262]}, info="Arruela IABV 4982293 | Material: tubo SAE 1020 e borracha 70 shore A | Dimensões: "
  "Ext. 152,0mm x Int. 40,3mm x Comprimento total 132,5mm")
T(316, "49843551", descricao="PINO DA BUCHA SUSP PNEU 22MM", marca="IABV", montadora=RD, variacoes="Cód. 4355-A1", tipo="PINO",
  aplicacao="Bucha IABV 3392 (4983392) / Bucha suspensão pneumática S250", foto_spec={"rect": [20, 262, 293, 589]},
  info="Dimensões: comprimento total 266mm x comprimento do corpo 250mm x M22 x 1,5 | Produtos relacionados: 4682, 3146, 3392, "
       "3392-01, 3392-02, 4355-A1 e 4347")
T(316, "50904092", descricao="PINO EXCENTRICO SUSP PNEU FACCHINI TH", marca=TH, montadora=FC, cod_ref="368146601", tipo="PINO",
  variacoes="MESMA IABV 4984507", aplicacao="Carreta Facchini com suspensão a ar", foto_spec={"rect": [293, 262, 570, 415]},
  info="Não acompanha porca (porca TR UNC I 1\" 3740001) | Dimensões: corpo de 31,5mm, compr. total 283mm, cabeça 80mm, rosca 1\" 8 FPP")
T(316, "50913035", descricao="BUCHA SUSPENSAO PNEUMATICA RANDON LONGA", marca=TH, montadora=RD, foto_spec={"rect": [293, 415, 570, 546]},
  info="152mm comprimento x 145mm altura")
for _p in (316, 339):
    T(_p, "50613038", descricao="BUCHA SUSPENSAO PNEUMATICA CAR FACCHINI", marca=TH, montadora=FC, cod_ref="0308190702",
      aplicacao="Carretas Facchini", info="Material: tubo SAE 1020 e borracha 70 shore A | Dimensões: Ext. 63,5 mm x Int. 37 mm x "
      "Comp. 72,5 mm")
F(316, "50613038", foto_spec={"rect": [20, 589, 293, 805]})
T(316, "50913062", descricao="CASTANHA SUSP PNEU RANDON TH", marca=TH, montadora=RD, cod_ref="70000035", variacoes="MESMA IABV 4984559",
  aplicacao="Bucha suspensão pneumática S250 | Compatível: Randon FS250 Nova", foto_spec={"rect": [293, 655, 570, 805]},
  info="Dimensões: Ext. da aba 76 mm x Ext. do meio 39,6mm x Int. 30,3 mm x Comprimento total 36,8mm | Produtos relacionados: "
       "IABV 4559 - Thor 13062")
NOTAS.append("Págs. 316/339: a porca 3740001 aparece só como acessório do pino excêntrico (está no capítulo Parafusos e Porcas).")
# 317 (balanças - grade 3 x 4)
GU = "Guerra"
_xs, _ys = [25, 208, 391, 570], [85, 268, 448, 627, 805]


def cel(i, j):
    return {"rect": [_xs[j], _ys[i], _xs[j + 1], _ys[i + 1]]}


for _c, _i, _j, _d, _m, _inf in [
        ("50648070", 0, 0, "BALANCA CARRETA RANDON 480 X 70 PINO 50MM", RD, "Asa delta | Chapa 5/16 | Medidas 480mm x 94mm x 70mm"),
        ("50900007", 0, 1, "BALANCA CAR RANDON ASA DELTA 60 MM", RD, ""),
        ("50900024", 0, 2, "BALANCA CAR RANDON LUB FREE MOD 2011 C/BUCHA", RD, ""),
        ("50900142", 1, 0, "BALANCA CAR RANDON SUSP C/BRACO EQUAL LUBFREE", RD, ""),
        ("50900017", 1, 1, "BALANCA TR RODOVIARIA Ø50", RD, ""),
        ("50900023", 1, 2, "BALANCA A CAR LUB FREE RANDON 2007 C/BUCHA", RD, "Mola: 90mm | Comprimento: 520mm | Ø pino: 30mm"),
        ("50900103", 2, 0, "BALANCA TR SUSPENSYS Ø50 MB 1620", "Suspensys, Mercedes-Benz", ""),
        ("5700717", 2, 1, "BALANCA FACCHINI DISTANCIADA LUBFREE 2019 LD", FC, "Medidas: 344 x 344 x 308 x 168,5 x Ø18,8 x Ø52,7"),
        ("5700718", 2, 1, "BALANCA FACCHINI DISTANCIADA LUBFREE 2019 LE", FC, "Medidas: 344 x 344 x 308 x 168,5 x Ø18,8 x Ø52,7"),
        ("5095051", 2, 2, "BALANCA CAR RANDON P/SUSP DISTAN SOLD CH 5/16", RD, "1708MM x 94MM"),
        ("50652064", 3, 0, "BALANCA CARR GUERRA 520 X 64 PINO 50MM", GU, "Balança carreta asa delta pino 50 mm - 5/16 | Molas 92 | "
         "Bucha 50 x 118 mm | 500 x 155 mm"),
        ("50648080", 3, 1, "BALANCA ATEGO FENIX 480 X 80 PINO 50MM", MB, "Mola: 80mm | Comprimento: 480mm | Ø pino: 50mm"),
        ("50900111", 3, 2, "BALANCA TR ATEGO 050 MOD. ORIGINAL", MB, "")]:
    T(317, _c, descricao=_d, montadora=_m, info=_inf, tipo="BALANÇA", foto_spec=cel(_i, _j))
F(317, "5700717", cod_ref="Facchini 03.68.0928.05"); F(317, "5700718", cod_ref="Facchini 03.68.0928.06")
# 318
NO = "Noma"
for _c, _i, _j, _d, _m, _inf in [
        ("5093646", 0, 0, "BALANCA A CAR LUB FREE FACCHINI", FC, ""),
        ("5060708", 0, 1, "BALANCA A CAR FACCHINI CARREGA TUDO LUB FREE", FC, "Balança carrega tudo HD Facchini Lubfree 2019 PF 30MM"),
        ("50900057", 0, 2, "BALANCA A CAR FACCHINI MOD 2012", FC, "Mola: 90mm | Comprimento: 545mm | Ø pino: 51mm"),
        ("50900124", 1, 0, "BALANCA NOMA ELEVACAO EIXO 61,5MM", NO, "Mola: 90mm | Comprimento: 590mm | Ø pino: 61,5mm"),
        ("50650094", 1, 1, "BALANCA ASA DELTA CARRETA NOMA PINO 61MM (500X200MM)", NO, ""),
        ("50653094", 1, 2, "BALANCA CAR NOMA FENIX PINO 61MM MOLA DE 90MM (200X530) DOBRADA", NO, ""),
        ("50602006", 2, 0, "PEITO POMBO BALANCA TRUK", "", "80 X 203 1/2"),
        ("50690170", 2, 0, "PEITO POMBO BALANCA CARRETA", "", "90 X 170 1/2"),
        ("50923025", 3, 1, "ARRUELA REFORCO BALANCA 97 X 142,5 X 6,35", "Randon, Guerra", ""),
        ("50903003", 3, 2, "ARRUELA REFORÇO", MB, "Dimensões: 150 x 150 x 9,50")]:
    T(318, _c, descricao=_d, montadora=_m, info=_inf, foto_spec=cel(_i, _j))
for _c in ("50602006", "50690170"):
    F(318, _c, tipo="PEITO DE POMBO")
F(318, "4983299", descricao="BUCHA BALANCA LUB FREE SUSP 11T RANDON", marca="IABV", montadora=RD, foto_spec=cel(2, 1),
  cod_ref="212008921 / 3453200181", info="Dimensões: Int. 30,2mm x Ext. 84,7mm x Comprimento 119mm")
T(318, "6330210", descricao="30 X 210 ACO 10.9 PF RP 2,0 R FINA CH46", montadora=RD + ", " + FC, tipo="PARAFUSO",
  aplicacao="Lub Free Randon e Facchini", info="Não acompanha a porca (porca travante MB 30 x 2,0 - 3683020)", foto_spec=cel(2, 2))
N(318, "631862", "18 X 60 ACO 10.9 SUP BALANCO 1,5 RF Ch27", cel(3, 0)["rect"], tipo="PARAFUSO",
  montadora="Noma, Ford, Mercedes-Benz, Scania, Volkswagen, Volvo, Guerra, Randon", aplicacao="SC/Volvo/Ford/VW | Para fixar "
  "suporte de balança do terceiro eixo para 242")
# 319 (pinos da balança 50MM / 60MM)
_M50 = "Randon, Guerra, Ford, Volkswagen, Mercedes-Benz, Volvo, Scania"
_F319 = [20, 85, 455, 655]
for _c, _d, _m, _inf in [
        ("7950173", "PINO BALANCA 50 X 173", _M50, "173MM x 50MM"), ("7950180", "PINO BALANCA 50 X 180", _M50, "180MM x 50MM"),
        ("7950190", "PINO BALANCA TRUCK VW SUSPENSYS 50 X 190", "Volkswagen, Suspensys", "190MM x 50MM"),
        ("7950203", "PINO BALANCA CARRETA RANDON SL 49,7 X 203", RD, "203MM x 49,7MM"),
        ("7950215", "PINO BALANCA CARRETA FACCHINI MOD 50 X 215", FC, "215MM x 50MM"),
        ("7950225", "PINO BALANCA 50 X 225", _M50, "225MM x 50MM"),
        ("7950216", "PINO BALANCA 50 X 215", GU, "LANÇAMENTO | 215MM x 50MM"),
        ("7950230", "PINO BALANCA 50 X 230", GU, "LANÇAMENTO | 230MM x 50MM"),
        ("7951215", "PINO BALANCA 51 X 215 FACCHINI", FC, ""),
        ("7960215", "PINO BALANCA 60 X 215", _M50, "215MM x 60MM"), ("7960225", "PINO BALANCA 60 X 225", _M50, "225MM x 60MM"),
        ("7960230", "PINO BALANCA 60 X 230", _M50, "230MM x 60MM")]:
    T(319, _c, descricao=_d, montadora=_m, info=_inf, tipo="PINO DA BALANÇA", foto_spec={"rect": _F319 if _c.startswith("795")
                                                                                          else [20, 655, 400, 805]})
T(319, "3330916", descricao="PORCA UNF E 9/16 PF CE CARRETA", tipo="PORCA", foto_spec={"rect": [400, 312, 570, 392]})
T(319, "0790916", descricao="PINO TRAVA PINO BALANCA TRUCK (ROSCA 9/16\") MENOR 90MM", tipo="PINO", info="Comprimento 90 mm x 3/4",
  foto_spec={"rect": [400, 392, 570, 515]})
N(319, "079916", "PINO TRAVA PINO BALANCA TRUCK (ROSCA 9/16\") MAIOR 105MM", [400, 515, 570, 600], tipo="PINO",
  info="Comprimento 105 mm x 3/4 | Código impresso com 6 dígitos")
NOTAS.append("Pág. 319: o pino trava maior 105MM está com o código 079916 (6 dígitos), e o menor 90MM com 0790916.")
# 320 (graxeiros e pinos tensor)
_GX = [("7710206", "GRAXEIRO RETO 06MM", "R"), ("7710208", "GRAXEIRO RETO 08MM", "R"), ("7710210", "GRAXEIRO RETO 10MM", "R"),
       ("7710214", "GRAXEIRO RETO 1/4", "R"), ("9860220", "GRAXEIRO RETO C 3/8", "R"),
       ("7710645", "GRAXEIRO CURVO 06 X 45°", "45"), ("7710845", "GRAXEIRO CURVO 08 X 45°", "45"),
       ("7711045", "GRAXEIRO CURVO 10 X 45°", "45"), ("9861245", "GRAXEIRO CURVO 1/2 X 45°", "45"),
       ("7711445", "GRAXEIRO CURVO 1/4 X 45°", "45"), ("7713845", "GRAXEIRO CURVO 3/8 X 45°", "45"),
       ("7710690", "GRAXEIRO CURVO 06 X 90°", "90"), ("7710890", "GRAXEIRO CURVO 08 X 90°", "90"),
       ("7711090", "GRAXEIRO CURVO 10 X 90°", "90"), ("7711490", "GRAXEIRO CURVO 1/4 X 90°", "90"),
       ("7715169", "GRAXEIRO CURVO 5/16 X 90°", "90"), ("7713890", "GRAXEIRO CURVO 3/8 X 90°", "90")]
_TGX = {"R": ("GRAXEIRO RETO", [30, 90, 110, 140]), "45": ("GRAXEIRO 45º", [300, 95, 395, 140]),
        "90": ("GRAXEIRO 90º", [30, 205, 110, 260])}
for _c, _d, _k in _GX:
    T(320, _c, descricao=_d, tipo="GRAXEIRO", _titulo=_TGX[_k][0], _nao_agrupar=False, card=100 + list(_TGX).index(_k),
      foto_spec={"rect": _TGX[_k][1]})
T(320, "9861620", descricao="GRAXEIRO EM Y CRUZETA 1620", tipo="GRAXEIRO", foto_spec={"rect": [20, 255, 300, 330]})
for _c, _d, _r in (("986380024", "GX UNF RETO 3/8 24FIOS", [300, 140, 435, 330]), ("986384524", "GX UNF 3/8 X 45 24FIOS", [435, 140, 535, 330]),
                   ("986389024", "GX UNF 3/8 X 90 24FIOS", [535, 140, 575, 330])):
    T(320, _c, descricao=_d, tipo="GRAXEIRO", info="UNF 24 fios", foto_spec={"rect": _r})
F(320, "986389024", foto_spec={"rect": [490, 140, 575, 330]}); F(320, "986384524", foto_spec={"rect": [395, 140, 490, 330]})
F(320, "986380024", foto_spec={"rect": [300, 140, 395, 330]})
T(320, "0790754", descricao="PINO TENSOR RANDON SUPER LEVE (PORCA 1\" POLEGADA)", montadora=RD, tipo="PINO",
  info="160mm x 30mm | Rosca 1\" | Porca 1\" polegada", foto_spec={"rect": [20, 330, 298, 457]})
T(320, "0790756", descricao="PINO TENSOR RANDON SUPER LEVE (PORCA 24MM)", montadora=RD, tipo="PINO",
  info="160mm x 30mm | Rosca 24MM | Porca 24MM", foto_spec={"rect": [298, 330, 575, 457]})
T(320, "0790755", descricao="PINO TENSOR RODOVIARIO LONGO", montadora=RD, tipo="PINO",
  info="150mm x 37mm x 24mm x 60mm | Porca 1\" polegada", foto_spec={"rect": [20, 457, 298, 630]})
T(320, "0792030", descricao="PINO TENSOR RANDON ANTIGA", montadora=RD, tipo="PINO",
  info="150mm x 37mm x 24mm x 70mm | Porca 1\" polegada", foto_spec={"rect": [298, 457, 575, 630]})
T(320, "5063007", descricao="BUCHA CARRETA RANDON CONICA", montadora=RD, variacoes="MESMA TH 50913005 / IABV 3007", tipo="BUCHA",
  foto_spec={"rect": [20, 630, 205, 805]})
T(320, "3471794", descricao="PO CASTELO 1\" PINO TIRANTE 14", montadora=GU, tipo="PORCA", foto_spec={"rect": [205, 630, 390, 805]})
for _p in (320, 336):
    T(_p, "50923023", descricao="ARRUELA PINO TENSOR RANDON LEVE 26 X 62 X 6,35", montadora=RD, tipo="ARRUELA / CALÇO",
      info="Para pino 790756 / 790754")
F(320, "50923023", foto_spec={"rect": [390, 630, 575, 805]})
# 321 (Noma)
T(321, "7961228", descricao="PINO BALANCA NOMA SUSP 2012 FENIX 61 X 228", montadora=NO, tipo="PINO DA BALANÇA",
  aplicacao="Pino de balança carreta Noma 2012 - Fenix", foto_spec={"rect": [20, 85, 545, 448]},
  info="Medidas: 61 x 228mm | Produzido em aço 1020, trefilado e retificado | Contém 01 pino de balança da carreta Noma 2012 em diante "
       "- 61x132mm com rosca 36x3 | Diâmetro 61,00mm | Comprimento do corpo 132,00mm | Comprimento total 224,50mm | Espessura da "
       "cabeça 15,00mm | Diâmetro da cabeça 83,00mm | Rosca M36x3")
T(321, "3683630", descricao="PORCA TRAVANTE MA 36 X 3,0", tipo="PORCA", foto_spec={"rect": [545, 305, 575, 448]})
F(321, "3683630", foto_spec={"rect": [400, 305, 575, 448]})
F(321, "7961228", foto_spec={"rect": [20, 85, 400, 448]})
T(321, "7961210", descricao="PINO BALANCA NOMA SUSP 2012 FENIX 61 X 210", montadora=NO, tipo="PINO DA BALANÇA",
  aplicacao="Pino balança carreta Noma Fenix (61x132 214 rosca M36x3)", foto_spec={"rect": [20, 448, 400, 805]})
T(321, "50925000", descricao="PORCA PINO BALANCA NOMA 2 1/16X10FPP", montadora=NO, tipo="PORCA", info="Rosca 2 1/6\" 10Fpp",
  foto_spec={"rect": [400, 448, 575, 805]})
# 322 (buchas da balança; códigos de 6 dígitos não são lidos automaticamente)
X(322, "7950120"); X(322, "7960120")
for _c, _d, _m, _inf, _y0, _y1 in [
        ("795063", "BUCHA BALANCA RANDON 50,2 X 60 X 53", RD, "50,2MM interno x 60MM externo x comprimento 53MM", 85, 229),
        ("7950120", "BUCHA BALANCA GUERRA/RANDON 50,2 X 60 X 120", "Guerra, Randon", "50,2MM interno x 60MM externo x comprimento "
         "120MM", 229, 366),
        ("796055", "BUCHA BALANCA GUERRA 60,2 X 75 X 55", RD, "60,2MM interno x 70MM externo x comprimento 53MM (como impresso)", 366, 517),
        ("7960120", "BUCHA BALANCA GUERRA 60,2 X 75 X 120", GU, "60MM interno x 75MM externo x comprimento 120MM", 517, 654),
        ("795053", "BUCHA BALANCA RANDON 50,2 X 60 X 53 FINA", RD, "Parede fina | 49,7MM interno x 59MM externo x comprimento 45MM",
         654, 805)]:
    N(322, _c, _d, [20, _y0, 330, _y1], montadora=_m, info=_inf, tipo="BUCHA")
NOTAS.append("Pág. 322: 796055 'BUCHA BALANCA GUERRA' tem logo Randon; as medidas no desenho (70MM externo, comprimento 53MM) "
             "diferem do título (75 x 55). Os códigos 795063, 796055 e 795053 têm 6 dígitos.")
# 323 (suportes Randon/Suspensys)
F(323, "50905022", info="Randon leve")
F(323, "50908003", montadora="Suspensys, Mercedes-Benz", aplicacao="MB 1620", info="")
_MONT23 = [(r"RANDON|RANDOM", "Randon"), (r"GUERRA", "Guerra"), (r"NOMA", "Noma"), (r"FACCHINI|FACHINI", "Facchini"),
           (r"SUSPENSYS", "Suspensys"), (r"\bMBB?\b|MERCEDES|ATEGO|ACCELO|AXOR|ACTROS|\b1620\b", "Mercedes-Benz"),
           (r"\bVW\b|VOLKS|CONSTELLATION", "Volkswagen"), (r"\bFORD\b|CARGO", "Ford"), (r"SCANIA", "Scania"),
           (r"VOLVO", "Volvo"), (r"LIBRELATO", "Librelato"), (r"KRONE", "Krone"), (r"RODOVIARIA", "Rodoviária"),
           (r"PASTRE", "Pastre"), (r"IDEROL", "Iderol"), (r"SCHIFFER", "Schiffer")]


def POS_PROC(r):
    segs = [x.strip() for x in r.get("info", "").split(" | ") if x.strip()]
    if not r.get("descricao") and segs and segs[0] == segs[0].upper():
        r["descricao"] = segs.pop(0)
        r["info"] = " | ".join(segs)
    if not r.get("montadora"):
        t = r["descricao"] + " " + r.get("aplicacao", "")
        r["montadora"] = ", ".join(dict.fromkeys(m for rx, m in _MONT23 if re.search(rx, t)))
    if not r.get("tipo"):
        for rx, t in TIPOS:
            if re.search(rx, r["descricao"]):
                r["tipo"] = t
                break
F(323, "50905193", montadora=RD); F(323, "50905194", montadora=RD)


def G(p, linhas, codigos, cols=(25, 208, 391, 570)):
    """Fotos em grade: codigos = lista por linha (None = célula vazia)."""
    for i, lin in enumerate(codigos):
        for j, c in enumerate(lin):
            if c:
                F(p, c, foto_spec={"rect": [cols[j], linhas[i], cols[j + 1], linhas[i + 1]]})


# 324
G(324, [85, 268, 455, 641, 805], [["50908002", "50907019", "50907018"], ["50907002", "48003206", "50901000"],
                                  ["50901001", "50913065", "50909135"], ["50909080", "50913100", "50909017"]])
F(324, "50908002", montadora="Suspensys, Mercedes-Benz")
F(324, "50907002", info="Sapata da mola carreta Randon linha leve eixo quadrado 112mm com suporte tirante 1500 8890", tipo="SAPATA")
for _c in ("50907019", "50907018"):
    F(324, _c, tipo="SAPATA")
F(324, "50907018", aplicacao="1620")
F(324, "50901000", info="Int: 50mm | Ext: 60mm | Comprimento 50mm")
F(324, "50901001", info="Int: 60mm (60,4mm) | Ext: 75mm | Comprimento 55mm")
F(324, "50913065", descricao="OLHAL VIGA SUSPENSAO AR CARRETA RANDON (COPO)", info="Int: 139,5mm | Ext: 159mm | Larg: 126mm", tipo="OLHAL")
F(324, "50909135", descricao="BUCHA PONT TENSOR CAR RANDON 2000 58MM X 76,2MM X 58MM", info="Int 58mm | Ext 76,2mm")
F(324, "50909080", descricao="BUCHA PONTEIRA TENSOR TR/CAR GUERRA/RANDON", info="Int: 71mm | Ext: 87mm | Larg: 80mm")
F(324, "50909017", descricao="BUCHA PONT TENSOR TR/CAR RANDON/GUERRA 71X80", info="Int 71mm | Ext 87mm | Larg: 80mm")
for _p in (324, 339):
    F(_p, "50913100", descricao="OLHAL VIGA SUSP PNEUMÁTICA FACCHINI (COPO)", info="Int: 139,5mm | Ext: 159mm | Larg: 152mm", tipo="OLHAL")
# 325 (mancais e flanges)
TIPOS.insert(0, (r"^MANCAL", "MANCAL"))
TIPOS.insert(0, (r"^FLANGE", "FLANGE"))
for r in ADD:
    if r["pagina"] == 325 and r["descricao"].startswith("MANCAL"):
        r["tipo"] = "MANCAL"
    if r["pagina"] in (325, 339, 341) and r["descricao"].startswith("FLANGE"):
        r["tipo"] = "FLANGE"
MP(325, RD, exceto=("50906072",))
F(325, "50906072", montadora=MB)
F(325, "50906019", descricao="MANCAL INT PINO BAL TR/CAR RODOVIARIA 050", info="Comprimento do parafuso: 80 mm | Diâmetro do parafuso: 30 mm")
F(325, "50906021", descricao="MANCAL EXT PINO BAL TR/CAR RODOVIARIA 050")
F(325, "50906009", descricao="MANCAL EXT PINO TENSOR RANDON 070", info="LANÇAMENTO 03/25 | 100MM x 125MM x 70MM")
F(325, "50906014", descricao="MANCAL PINO VAL TR/CAR RANDON 50MM", marca="Thor")
F(325, "50924011", marca="Thor")
for _p in (325, 339, 341):
    for r in ADD:
        if r["pagina"] == _p and r["codigo"] == "50924012":
            r.update(descricao="FLANGE FREIO EIXO QUADRADO RANDON/FACCHINI 148MM", info="Para eixo quadrado Ø148", montadora=RD + ", " + FC)
        if r["pagina"] == _p and r["codigo"] == "50924011":
            r.update(descricao="FLANGE FREIO SPIDER RANDON MASTER REDONDO 130MM", info="Dimensões: Ø130 | Produtos relacionados: 24011",
                     aplicacao="Randon", montadora=RD)
F(325, "50924044", info="140MM")
F(325, "50923016", info="42MM", descricao="ARRUELA ENCOSTO EIXO S C/ABA 42MM")
F(325, "50903002", descricao="ARRUELA REFORCO 150 X 150 X 6,35")
# 326 (tensores)
G(326, [85, 268, 448, 627, 805], [["50913070", None, "509803003"], ["50909035", "50909036", "50901930"],
                                  ["50909082", "50909067", "50909025"], [None, "48003051", "50913001"]])
F(326, "50909012", foto_spec={"rect": [208, 85, 391, 180]}); F(326, "50909028", foto_spec={"rect": [208, 180, 391, 268]})
for _p in (326, 339):
    for r in ADD:
        if r["pagina"] == _p and r["codigo"] == "50913070":
            r.update(descricao="BUCHA LARANJA SUSPENSÃO PNEUMÁTICA CAR FACCHINI", montadora=RD + ", " + FC, info="172MM x 148,5MM | Furo 32MM")
        if r["pagina"] == _p and r["codigo"] == "50909028":
            r.update(descricao="VARAO TENSOR REGULAVEL CAR RANDON 2000/FACCHINI MODERNA 390MM", montadora=RD + ", " + FC, info="")
F(326, "50909012", descricao="PONTEIRA TENSOR TR/CAR RANDON GUERRA 600MM RD", montadora=RD + ", " + GU)
F(326, "509803003", descricao="TENSOR REGULAVEL CAR RANDON 480MM", info="58MM")
F(326, "50901930", descricao="TENSOR REGULAVEL CAR RANDON 530MM", info="530MM")
F(326, "50909067", descricao="TENSOR REGULAVEL TR/CAR RODOVIARIA 640MM", info="61MM", montadora=RD)
N(326, "50909038", "TENSOR FIXO TR/CAR RODOVIARIA/NOMA 640MM", [25, 627, 208, 805], montadora=RD + ", " + NO, tipo="TENSOR / TIRANTE",
  info="61MM | Código impresso como '509.09038'")
F(326, "48003051", descricao="BRACO TENSOR FUNDIDO 58 X 535 MM RANDON", variacoes="SC-03.051")
F(326, "50913001", descricao="BUCHA CARRETA RANDON 2000", marca="Thor", cod_ref="208.006.277", variacoes="MESMA 4983116 IABV / "
  "MESMA 5063116 Suspensys", aplicacao="Carretas Randon 2000", info="Material: tubo SAE 1020 e borracha 70 shore A", montadora=RD)
# 327-328 (Mercedes Atego)
MP(327, MB)
T(327, "50913047", descricao="BUCHA OLHAL MOLA MB TRAS PARTE TRAS ALGEMA", marca="Thor", montadora=MB, cod_ref="6703200444",
  variacoes="MESMA IABV 4983024", tipo="BUCHA", aplicacao="Mercedes Benz: MB709/710/712/913/914/1114/L 710/L 710D/L913D / Ônibus: "
  "LO809/LO 812/LO 813D/LO814/OF 809/OF 812", info="Material: tubo SAE 1020 e borracha 70 shore A | Dimensões: Ext. 56,5mm x Int. "
  "30,4mm x Comprimento 87mm")
T(327, "50913068", descricao="BUCHA SUPORTE MB ATEGO", marca="Thor", montadora=MB, cod_ref="A 958.320.0344 / A 970.320.0144",
  variacoes="MESMA IABV 4983539", tipo="BUCHA", aplicacao="Mercedes Atego", info="Material: tubo SAE 1020 e borracha 70 shore A | "
  "Dimensões: Ext. da aba 58,5 x furo 18,5 x comprimento total 95,8mm")
T(327, "50913051", descricao="BUCHA MOLA DIANTEIRA MB", marca="Thor", montadora=MB, cod_ref="9743200644", tipo="BUCHA",
  aplicacao="MB Atego", info="Material: tubo SAE 1020 e borracha 70 shore A | Dimensões: Ext. 62,5mm x Int. 18,3mm x Comprimento 96mm")
T(327, "50913069", descricao="BUCHA MOLA MB ATEGO DIANT/TRAS", marca="Thor", montadora=MB, cod_ref="A 958.320.0204", tipo="BUCHA",
  variacoes="MESMA IABV 4983303", aplicacao="Mercedes Atego", info="Material: tubo SAE 1020 e borracha 70 shore A e nylon | "
  "Dimensões: Ext. da aba 73,5mm x Int. 22,0mm x Comprimento 96mm")
F(328, "50908019", info="92MM x 183MM x 201,6MM", montadora="Usicamp")
F(328, "48001240", descricao="SUPORTE CENTRAL TRUCK MB ATEGO")
NOTAS.append("Pág. 328: só 3 produtos; demais molduras vazias.")
# 329 (Suspensys)
for r in ADD:
    if r["pagina"] == 329:
        r["montadora"] = ", ".join(dict.fromkeys(["Suspensys"] + [m for rx, m in _MONT23[:6] if re.search(rx, r["descricao"])]))
# 330 (Guerra) / 331
for r in ADD:
    if r["pagina"] == 330 and r["descricao"].startswith("SAP "):
        r["tipo"] = "SAPATA"
MP(331, GU)
for _c, _comp in (("50909000", "550"), ("50909004", "450"), ("50909093", "550"), ("50909097", "450")):
    _d = [r for r in ADD if r["pagina"] == 331 and r["codigo"] == _c][0]["descricao"]
    F(331, _c, descricao=_d.split(" MEDIDAS")[0], tipo="TENSOR / TIRANTE", montadora=GU + ", " + RD,
      info=f"Comprimento do corpo sem as buchas: {_comp},00mm | Diâmetro interno das pontas sem as buchas: 71,00mm | "
           "Diâmetro do corpo do tensor: 38,1mm | Diâmetro externo das pontas: 87,00mm")
F(331, "50909001", montadora=GU + ", " + RD)
F(331, "50907039", descricao="SAPATA INFERIOR TRAS CARRETA GUERRA P/EIXO", cod_ref="07039", info="Dimensão: 60,3 x 30,5mm",
  tipo="SAPATA")
# 332 (Volvo/Scania) / 333 (Ford/VW)
for _c in ("50905040", "50905041", "50905043", "50905044"):
    F(332, _c, montadora="Suspensys, Volvo, Scania")
F(332, "50906083", tipo="ARRUELA / CALÇO", montadora="Volvo, Ford, Volkswagen")
F(332, "50913080", cod_ref="274.1225 / 361.12175 / 063.1666 / 082.1625", info="")
for _c in ("50905035", "50905036", "50905037", "50905038", "50905039"):
    F(333, _c, montadora="Suspensys, Ford, Volkswagen")
F(333, "48003158", descricao="SUPORTE TRUCK CENTRAL SUSPENSYS FORD VOLKS LE", variacoes="SC-03.158 (SILC)")
F(333, "48003159", descricao="SUPORTE TRUCK CENTRAL SUSPENSYS FORD VOLKS LD", variacoes="SC-03.159 (SILC)")
F(333, "48003169", cod_ref="70.100.100", variacoes="SC-03.169", aplicacao="Ford, Volks, Volvo, a partir de 2008", info="",
  montadora="Suspensys, Ford, Volkswagen, Volvo")
T(333, "50913045", descricao="BUCHA MOLA TRAS SUSP VOLKS", marca="Thor", montadora=VW, cod_ref="TAP.511.181", tipo="BUCHA",
  variacoes="MESMA IABV 4983045", aplicacao="Volkswagen", info="Material: tubo SAE 1020 e borracha 70 shore A | Dimensões: "
  "Ext. 58,0mm x Int. 30,2mm x Comp. 90mm")
# 334-335
_VVF = "Volvo, Ford, Volkswagen"
F(334, "50909114", descricao="BUCHA PONT TENSOR FIXO TR VW/VO/FORD 62,7MM X 76MM X 58MM", info="Int 62,7mm | Ext 76mm", montadora=_VVF)
for _c in ("509803002", "50909112"):
    F(334, _c, montadora=_VVF)
for _p in (332, 334):
    F(_p, "50907068", montadora="Volvo, Scania")
T(334, "50913075", descricao="BUCHA OLHAL SUSP TRAS SCANIA TH", marca="Thor", montadora=SC, cod_ref="1362710 / 255669 / 445589",
  variacoes="MESMA IABV 4983271", tipo="BUCHA", info="LANÇAMENTO 03/25 | Ext. 65,5mm x Int. 30,2mm x Comprimento 121mm")
F(334, "50911013", descricao="BUCHA PINO MOLA DIANT SCANIA")
for _c in ("50907046", "50907047"):
    F(335, _c, tipo="SAPATA")
NOTAS.append("Pág. 335: a última moldura traz só o logo Noma.")
# 336-337
for r in ADD:
    if r["pagina"] == 336 and r["descricao"].startswith("ARRUELA"):
        r["tipo"] = "ARRUELA / CALÇO"
F(336, "50923033", descricao="ARRUELA ENCOSTO PINO BALANCA 2012 CAR NOMA", info="Ø 80 x 40 x 12 mm", montadora=NO, tipo="ARRUELA / CALÇO")
for _c in ("50909137", "50909140"):
    F(337, _c, tipo="TENSOR / TIRANTE")
for r in ADD:
    if r["codigo"] == "50909038":
        r["montadora"] = RD + ", " + NO
NOTAS.append("Págs. 326/337: o tensor 50909038 aparece nas duas páginas (na 326 com o código impresso '509.09038').")
# 338-339 (Facchini)
for _c in ("50905127", "50905129", "50905131"):
    F(338, _c, tipo="SUPORTE")
T(338, "50904095", descricao="PINO VARAO SUSP DISTANCIADA CAR 50,8 X 114", montadora=FC, tipo="PINO",
  aplicacao="Carretas Facchini suspensão distanciada", info="Não acompanha porca (porca trav MB 24 x 2,0 pino tensor 3680863)",
  foto_spec={"rect": [391, 448, 570, 627]})
X(338, "3680863")
for _c, _lado in (("50900062", "LE"), ("50900061", "LD")):
    T(338, _c, descricao=f"BALANCA FACCHINI DISTANCIADA 050 {_lado}", montadora=FC, tipo="BALANÇA",
      aplicacao="Carretas Facchini eixo distanciado; outros modelos de carretas Vanderléia com pino 50mm",
      info="Dimensões: diâmetro pino 5cm (50mm) | comprimento 31,5cm (315mm) | largura da mola 9cm (90mm) | peso 15 kg")
F(338, "50908016", info="211MM x 94MM")
F(338, "50905200", info="Dimensões: 390x172 | Ø 25,7x80,3")
X(339, "4984507")
N(339, "50909036", "LUVA TENSOR CAR RANDON MOD2000/FACCHINI MODERNA LD", [25, 85, 208, 268], montadora=FC, tipo="TENSOR / TIRANTE",
  info="Código impresso como '509 09036'")
X(326, "50909036")
F(339, "50906053", info="Ø106 x Ø26 x 17,5 x 9,5 x 8"); F(339, "50906054", info="Ø106 x Ø80,7 x 9,5")
NOTAS.append("Págs. 338-339: 3680863 (porca) e 4984507 (pino excêntrico IABV) aparecem só como acessório/repetição (estão nos "
             "capítulos Parafusos e Porcas e Itens IABV). A luva 50909036 está impressa como '509 09036' na pág. 339.")
# 340-341
F(340, "50907083", tipo="SAPATA")
T(340, "50913049", descricao="BUCHA MOLA DIANT 1938S 1944S - TH", marca="Thor", montadora=MB, cod_ref="A 000.322.3285", tipo="BUCHA",
  variacoes="IABV 3148", aplicacao="Mola dianteira da suspensão | Caminhões MB 1938/1944S/1938S Actros 4140B/4148B/4141B/4140K/4151K/"
  "4148K/2631LS/2660LS/2648LS Axor 1933 4X2-36/45/1933LS 4X2-36/2533 6X2/2533 6X2-48/2035S/2040S",
  info="Dimensões: Ext. 62,5mm x Int. 24,2mm x Comprimento 96mm | Produtos relacionados: 4248, 5043, 4251 e 3692")
for _c in ("50905105", "50905106"):
    F(340, _c, tipo="SUPORTE")
NOTAS.append("Pág. 340: duas molduras vazias.")
MP(341, MB, exceto=("48003501", "50924011", "50924012"))
T(341, "4804206", descricao="MB SUPORTE FREIO A AR DIANTEIRO", montadora=MB, cod_ref="346.421.4206", tipo="SUPORTE",
  aplicacao="1316/1516/1518/1618/2216 c/freio a ar")
T(341, "5061359", descricao="MB REP EIXO S FREIO DIANT C BUCHA LATAO", montadora=MB, cod_ref="3454200041", tipo="REPARO DO EIXO S",
  variacoes="Similar Boechat 4620 / Master EX206 / Master 2210FM350 completo", aplicacao="MB Mercedes Benz freio a ar - dianteiro",
  info="Peso: 1.735 kg | Altura: 1.5 cm | Largura: 1.5 cm | Profundidade: 1.5 cm")
T(341, "48001503", descricao="MB SUPORTE FREIO A AR TRASEIRO", montadora=MB, cod_ref="386.423.0006", tipo="SUPORTE",
  aplicacao="C/freio a ar")
T(341, "5060341", descricao="MB REP EIXO S C/ROTULA C/DEF T (TRASEIRO)", montadora=MB, cod_ref="3454200341", tipo="REPARO DO EIXO S",
  aplicacao="MB Mercedes Benz freio a ar - traseiro", info="Peso: 1.735 kg | Altura: 1.5 cm | Largura: 1.5 cm | Profundidade: 1.5 cm")
F(341, "5061551", montadora="")
T(341, "48003501", descricao="SUP PATIM COMP FREIO TUBELESS MASTER LD-LE", tipo="SUPORTE", variacoes="REF SILC: SC-03.501 / (Boechat) 2503",
  aplicacao="Truck e carretas", foto_spec={"rect": [20, 565, 345, 805]})
F(338, "50905200", descricao="SUP SUSP PNEUMATICA CAR FACCHINI - LE", montadora=FC, tipo="SUPORTE")
F(339, "50906053", descricao="MANCAL EXT SUSP PNEUMATICA FACCHINI 080", montadora=FC, tipo="MANCAL")
F(339, "50906054", descricao="MANCAL INT SUSP PNEUMATICA FACCHINI 026", montadora=FC, tipo="MANCAL")
F(325, "50924044", descricao="FLANGE FREIO SPIDER RANDON MASTER REDON 0140", tipo="FLANGE", info="140MM")
for _c, _d in (("50909000", "TENSOR FIXO TR/CAR RANDON/GUERRA 550MM"), ("50909004", "TENSOR FIXO TR/CAR RANDON/GUERRA 450MM"),
               ("50909093", "TENSOR REG TR/CAR RANDON/GUERRA 550MM"), ("50909097", "TENSOR REG TR/CAR RANDON/GUERRA 450MM")):
    F(331, _c, descricao=_d)
