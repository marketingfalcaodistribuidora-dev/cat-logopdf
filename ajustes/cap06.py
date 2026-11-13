# Capítulo 6 - Anel Elástico, Rolete e Trava (págs. 43-47)
# Págs. 43 e 45: textos em imagem e molduras sobrepostas -> lidas visualmente e registradas manualmente (ADD).
MANUAIS = {43, 45}


def M(pag, card, codigo, descricao, tipo, rect, cod_ref="", montadora="", info="", aplicacao="", marca="", variacoes=""):
    return dict(pagina=pag, card=card, codigo=codigo, descricao=descricao, tipo=tipo, foto_spec={"rect": rect},
                cod_ref=cod_ref, montadora=montadora, info=info, aplicacao=aplicacao, marca=marca, variacoes=variacoes)


def R(*recs, **comuns):
    out = []
    for r in recs:
        d = dict(comuns)
        d.update(r)
        out.append(d)
    return {"records": out}


def r(codigo, descricao, tipo, **kw):
    d = dict(codigo=codigo, descricao=descricao, tipo=tipo)
    d.update(kw)
    return d


# ---------------- pág. 43 ----------------
_EXT = [("4381121", "08"), ("4381122", "09"), ("4381123", "10"), ("4381124", "11"), ("4381125", "12"), ("4381126", "13"),
        ("4381127", "14"), ("4381128", "15"), ("4381129", "16"), ("4381130", "17"), ("4381132", "18"), ("4381133", "19"),
        ("4381134", "20"), ("4381137", "21"), ("4380867", "22"), ("4380023", "23"), ("4381139", "24"), ("4381140", "25"),
        ("4381131", "28"), ("4384329", "29"), ("4380868", "30"), ("4380869", "32"), ("4380870", "34"), ("4381141", "36"),
        ("4381142", "38"), ("4384338", "37"), ("4380058", "58"), ("4380063", "63")]
_INT = ["08", "09", "10", "11", "12", "14", "16", "18", "20", "22", "24", "26", "28", "30", "32", "34", "36", "37", "38", "40", "65"]
_RET = [("4900255", "1,2"), ("4900256", "1,5"), ("4900257", "1,9"), ("4900002", "2,3"), ("4900003", "3,2"), ("4900004", "4,0"),
        ("4900005", "5,0"), ("4900006", "6,0"), ("4900007", "7,0"), ("4900008", "8,0"), ("4900009", "9,0"), ("4900010", "10,0"),
        ("4900012", "12,0"), ("4900015", "15,0"), ("4900019", "19,0")]
ADD = []
ADD += [M(43, 1, c, f"ANEL ELASTICO EXTERNO {m}MM", "ANEL ELÁSTICO EXTERNO", [50, 92, 112, 150], info="Linha G 438")
        for c, m in _EXT]
ADD += [M(43, 2, "43900" + m if len(m) == 2 else c, f"ANEL ELASTICO INTERNO {m}", "ANEL ELÁSTICO INTERNO", [305, 108, 368, 166],
          info="Linha G 439") for c, m in [(None, x) for x in _INT]]
ADD += [M(43, 3, "4381131", "TRAVA EIXO S 25,5MM", "TRAVA EIXO S", [50, 380, 95, 424], info="25,5MM"),
        M(43, 3, "4380868", "TRAVA EIXO S 27,5MM", "TRAVA EIXO S", [140, 380, 182, 426],
          info="27,5MM | Código impresso no card como 438.0868"),
        M(43, 3, "4380869", "TRAVA EIXO S 29MM", "TRAVA EIXO S", [190, 380, 270, 424],
          info="29MM | Código impresso no card como 438.0869 (só na imagem)"),
        M(43, 3, "4380870", "TRAVA EIXO S 31MM", "TRAVA EIXO S", [38, 462, 95, 516], info="31MM"),
        M(43, 3, "4381141", "TRAVA EIXO S 33MM", "TRAVA EIXO S", [132, 462, 190, 516], info="33MM"),
        M(43, 3, "4381142", "TRAVA EIXO S 35MM", "TRAVA EIXO S", [214, 452, 274, 519], info="35MM"),
        M(43, 3, "5064202", "TRAVA S AMARELA MODERNA TUBELESS", "TRAVA EIXO S", [54, 538, 108, 604], info="Selo de lançamento"),
        M(43, 3, "4682224", "P 37,47X5,33 ANEL ORING EIXO S", "ANEL O-RING EIXO S", [178, 558, 232, 611], info="S sist. tubeless")]
ADD += [M(43, 4, c, f"ANEL RETENCAO {m}", "ANEL RETENÇÃO", [309, 482, 385, 552], info="Linha G 490") for c, m in _RET]
ADD += [M(43, 5, "7774202", "TRAVA S PRETA MODERNA TUBELESS", "TRAVA EIXO S", [34, 659, 120, 748]),
        M(43, 5, "7713106", "+ANEL ELAST EXTERNO 31", "ANEL ELÁSTICO EXTERNO", [132, 659, 225, 774]),
        M(43, 5, "7713328", "+ANEL ELAST EXTERNO 32", "ANEL ELÁSTICO EXTERNO", [244, 659, 336, 774]),
        M(43, 5, "7713509", "+ANEL ELAST EXTERNO 35", "ANEL ELÁSTICO EXTERNO", [352, 639, 447, 774]),
        M(43, 5, "7713926", "+ANEL ELAST EXTERNO 39", "ANEL ELÁSTICO EXTERNO", [469, 639, 559, 774])]

# ---------------- pág. 45 (grade lida visualmente) ----------------
_C3 = [(20, 205), (205, 388), (388, 575)]
_L = [(85, 190), (190, 293), (293, 396), (396, 499), (499, 602)]


def g(lin, col):
    (x0, x1), (y0, y1) = _C3[col], _L[lin]
    return [x0 + 2, y0 + 2, x1 - 2, y1 - 2]


ADD += [
    M(45, 1, "5060765", "TRAVA ARANHA RANDON 132 X 81,3", "TRAVA ARANHA", g(0, 0), montadora="Randon", info="Menor | Master"),
    M(45, 2, "5060766", "TRAVA ARANHA RANDON ANTIGA 139,6 X 81,3", "TRAVA ARANHA", g(0, 1), montadora="Randon", info="Maior"),
    M(45, 3, "5060249", "TRAVA ARANHA IDEROL 90 X 132MM", "TRAVA ARANHA", g(0, 2), montadora="Iderol", info="Int. 90,5 mm / Ext. 132 mm"),
    M(45, 4, "5060769", "TRAVA ARANHA RECROSUL 139,5 X 90,5", "TRAVA ARANHA", g(1, 0), montadora="Recrusul",
      info="Int. 90,5 mm / Ext. 139,5 mm | No card: \"RECROSUL 139,5 X 90,5\""),
    M(45, 5, "50600768", "TRAVA ARANHA GUERRA ATE 2000 138 X 80,5", "TRAVA ARANHA", g(1, 1), montadora="Guerra",
      info="Moderna | Código impresso com 8 dígitos (50600768)"),
    M(45, 6, "5060767", "TRAVA ARANHA GUERRA ATE 2000 139,5 X 90,5", "TRAVA ARANHA", g(1, 2), montadora="Guerra", info="Antiga"),
    M(45, 7, "5060771", "ARRUELA LISA RANDON 81,3 X 120MM", "ARRUELA LISA", g(2, 0), montadora="Randon"),
    M(45, 8, "5060773", "ARRUELA LISA GUERRA MOD MENOR 80 X 125 MM", "ARRUELA LISA", g(2, 1), montadora="Guerra", info="Moderna"),
    M(45, 9, "5060772", "ARRUELA LISA GUERRA MAIOR 90X135X10MM", "ARRUELA LISA", g(2, 2), montadora="Guerra", info="Antiga"),
    M(45, 10, "5060775", "ARRUELA LISA ENCOSTO SEM DENTE CARRETAS TODOS 90.5x121mm", "ARRUELA LISA ENCOSTO", g(3, 0)),
    M(45, 11, "5060774", "ARRUELA LISA ENCOSTO COM DENTE GUERRA/IDEROL/KRONE TODOS 90,5 X 120MM", "ARRUELA LISA ENCOSTO", g(3, 1),
      montadora="Guerra, Iderol, Krone"),
    M(45, 12, "5069015", "ARRUELA LISA ENCOSTO KRONORTE 90 X 155", "ARRUELA LISA ENCOSTO", g(3, 2), info="Ext. 155MM | Int. 90MM"),
    M(45, 13, "5067650", "TRAVA ARANHA RANDON PEQ 81.3 X 132 ORIGINAL", "TRAVA ARANHA", g(4, 0), montadora="Randon", marca="Suspensys"),
    M(45, 14, "5064762", "TRAVA ARANHA 2 DENTES RANDON MODERNA 2017/...", "TRAVA ARANHA", g(4, 1), montadora="Randon, Facchini"),
    M(45, 15, "5064701", "TRAVA ARANHA 6 DENTES CARRETA FACCHINI MODERNA", "TRAVA ARANHA", g(4, 2), montadora="Facchini, Randon",
      info="90 X 145 X 118MM"),
    M(45, 16, "5060770", "TRAVA ARANHA NOMA/IDEROL/KRONE 126M X 90M", "TRAVA ARANHA", [22, 604, 166, 702],
      montadora="Iderol, Noma, Krone", info="90 x 126 x 10mm"),
    M(45, 17, "5061944", "MB TRAVA ARANHA 1620/WOLKS RED", "TRAVA ARANHA", [169, 604, 296, 702], cod_ref="386.356.7073",
      montadora="Mercedes-Benz, Ford, Volkswagen", info="83,5X117,5"),
    M(45, 18, "5011473", "TRAVA ARANHA VW 14.210 INT: 74MM X EXT: 102MM", "TRAVA ARANHA", [300, 604, 437, 702],
      cod_ref="TE3501473A", montadora="Volkswagen", info="Medida: interna 74MM / externa 102MM"),
    M(45, 19, "5061723", "TRAVA CUB TRAS 814 CARGO 11DEN", "TRAVA CUBO", [441, 604, 573, 702], montadora="Volkswagen, Ford",
      aplicacao="VW 6.80 / 6.90 / 7.90 / 7.110 / Tras 814/815 Cargo", info="Int: 51,50 X Ext: 77,00mm"),
    M(45, 20, "5012514", "TRAVA ARANHA TRAZ FORD 11130/11140/12140/13130/14140", "TRAVA ARANHA", [22, 705, 166, 804],
      cod_ref="01925818", montadora="Ford, Volkswagen", info="Externo 107MM | Interno 67MM"),
    M(45, 21, "5061724", "TRAVA CUB TRAS F.4000 ANT 5DEN FO F350/F2000", "TRAVA CUBO", [169, 705, 294, 804], montadora="Ford",
      info="Int: 51MM X Ext: 75MM"),
    M(45, 22, "5061722", "TRAVA CUB TRAS VOLARE 11DEN 54MM", "TRAVA CUBO", [297, 705, 437, 804], cod_ref="6010.009.012.009",
      montadora="Volkswagen", info="54MM | Logo ônibus Volare"),
]

# ---------------- págs. 44, 46, 47 (cards automáticos + correções) ----------------
AJ = {
    "44.1": R(r("5060756", "ROLETE BENDIX 28MM CARRETA", "ROLETE", info="Pino patim")),
    "44.2": R(r("5060757", "ROLETE PATIM MASTER 58X31,8X25", "ROLETE", info="Pino patim Randon moderna", montadora="Randon")),
    "44.3": R(r("5060057", "ROLETE GUERRA MODERNA", "ROLETE", montadora="Guerra")),
    "44.4": R(*[r(c, f"ROLETE {m} MM", "ROLETE") for c, m in
                [("5060754", "32"), ("5060038", "35"), ("5060755", "38"), ("5062103", "41"), ("5062104", "44")]]),
    "44.5": R(r("5061874", "MB REP PATIM FREIO AR 1518/1618/...", "REPARO PATIM", cod_ref="307.421.1874", montadora="Mercedes-Benz")),
    "44.6": R(r("10004216", "MB REP ADAPT PATIM FREIO AR TODOS CONJ 30 X 90MM", "REPARO PATIM", cod_ref="346.421.1174",
                montadora="Mercedes-Benz")),
    "44.7": R(r("5063997", "ROLETE PATIM VOLKS/MAN 60 X 35 X 35", "ROLETE", montadora="Volkswagen, MAN",
                info="LANÇAMENTO 25/03 | Desmontada / Montada")),
    "44.8": R(r("5069106", "MB PINO ROLETE PATIM 20 X 73MM", "PINO ROLETE", montadora="Mercedes-Benz",
                aplicacao="MBB OF 1313 1318 HPN LS 1632", variacoes="Similares: LP006 / T5002 / 05002 / 120136 / 3074210074 / 5002",
                info="73mm x 20mm")),
    "44.9": R(r("5060202", "BUCHA ROLETE FLANGE BENDIX MENOR", "BUCHA ROLETE")),
    "44.10": R(r("5060777", "CONJ. TRAVA DO ROLETE", "TRAVA ROLETE")),
    "44.11": R(r("5060776", "TRAVA DO ROLETE MODERNO MASTER", "TRAVA ROLETE")),
    "44.12": R(r("5060125", "BUCHA ROLETE FLANGE MASTER MAIOR", "BUCHA ROLETE")),
    "44.13": R(r("4702018", "CONTRA PINO TRAVA ROLETE", "CONTRA PINO")),
    "44.14": R(r("9133801", "REBITE LISO 3/8 X 1", "REBITE MACIÇO LISO", info="Rebite maciço liso cabeça redonda"),
               r("9131201", "REBITE LISO 1/2 X 1", "REBITE MACIÇO LISO", info="Rebite maciço liso cabeça redonda")),
    "44.15": R(r("5062300", "PINO SAPATA FREIO RODA TRASEIRA 12MM X 88MM", "PINO SAPATA", cod_ref="682.421.0074",
                 montadora="Mercedes-Benz", aplicacao="Mercedes-Benz Atego 1725, Atego 2425, Atego 2426")),
    "44.16": R(r("4730142", "QUEBRA DEDO 1/4' X 2'", "QUEBRA DEDO"), r("4735162", "QUEBRA DEDO 5/16' X 2'", "QUEBRA DEDO"),
               r("4730382", "QUEBRA DEDO 3/8' X 2'", "QUEBRA DEDO"), r("4737162", "QUEBRA DEDO 7/16'X 2'", "QUEBRA DEDO"),
               r("4731400", "QUEBRA DEDO 1/4\" X 1 1/2\" C/ CORRENTE", "QUEBRA DEDO", info="No card: 1/4\" X 1 1/2\" C/ CORRENTE"),
               r("4731600", "QUEBRA DEDO 5/16\" X 40MM C/ CORRENTE", "QUEBRA DEDO", info="No card: 5/16\" X 40MM C/ CORRENTE")),
    "44.17": R(r("4730614", "PINO TRAVA CORRENTE 1/4", "PINO TRAVA CORRENTE"), r("4730516", "PINO TRAVA CORRENTE 5/16", "PINO TRAVA CORRENTE")),
    "44.18": R(*[r(c, d, "TRAVA R IMPLEMENTOS") for c, d in [
        ("4730485", "TRAVA R IMPLEMENTOS 4,0X28X90"), ("4730595", "TRAVA R IMPLEMENTOS 5,0X95"),
        ("4732550", "TRAVA R IMPLEMENTOS 2,5X18X50"), ("4733059", "TRAVA R IMPLEMENTOS 3 X 18 X 59"),
        ("4734100", "TRAVA R IMPLEMENTOS 4,8X29X100"), ("4734140", "TRAVA R TOMBADOR CARRETA 4X140"),
        ("4734511", "TRAVA R IMPLEMENTOS 4X29X120"), ("4734724", "TRAVA R PARAFUSO CARRETA")]]),
    # pág. 46 (todos com logo Mercedes-Benz, exceto Volvo/Scania)
    "46.1": R(r("5061177", "MB TRAVA CUBO 1313 FREIO AR", "TRAVA CUBO", info="(75,00 X 99,00 mm)")),
    "46.2": R(r("5061939", "MB TRAVA ARANHA CUBO 1620 MOD", "TRAVA ARANHA", info="(85,00 X 112,00 mm)")),
    "46.3": R(r("9010320", "MB TRAVA ARANHA CARCACA", "TRAVA ARANHA", info="(80,00 X 105,00 mm) | L1620/2423... (HL4/050-HL5/61)")),
    "46.4": R(r("5015272", "TRAVA ARANHA 608/708 TRAS", "TRAVA ARANHA", cod_ref="070952.052101", aplicacao="608D 708E 709 912",
                info="(52,00 X 72,00 MM)")),
    "46.5": R(r("5061929", "MB TRAVA ARANHA 1938 TRAS D PQ", "TRAVA ARANHA", info="(88,00 X 106,00 mm)")),
    "46.6": R(r("5061480", "MB TRAVA PORCA CUBO TRAS. ARANHA L 1113/LPO", "TRAVA PORCA CUBO", cod_ref="321 356 01 73")),
    "46.7": R(r("5060004", "MB TRAVA CUBO 1313 OLEO", "TRAVA CUBO", info="(larga) (65 X 94mm)")),
    "46.8": R(r("5061480", "MB TRAVA CUBO 1113", "TRAVA CUBO", info="(63,00 X 88,00 mm)")),
    "46.9": R(r("5060004", "MB TRAVA PORCA CUBO TRAS. ARANHA L 2213/13130362 PC FREIO A ÓLEO", "TRAVA PORCA CUBO",
                cod_ref="345.356.0073", info="(65 X 94mm)")),
    "46.10": R(r("5061935", "MB TRAVA ARANHA DENTE GDE 1935", "TRAVA ARANHA", info="(88,00 X 123,00 mm)")),
    "46.11": R(r("5060273", "MB TRAVA M FREIO AR", "TRAVA ARANHA", cod_ref="355 332 02 73")),
    "46.13": R(r("5061179", "TRAVA ARANHA CUBO TRAS VOLVO", "TRAVA ARANHA", montadora="Volvo")),
    "46.14": R(r("5065525", "TRAVA ARANHA CUBO DIANT GRAXA VOLVO", "TRAVA ARANHA", montadora="Volvo")),
    "46.16": R(r("5065176", "TRAVA ARANHA SCANIA INT 36 x 57", "TRAVA ARANHA", montadora="Scania",
                 info="Descrição impressa dentro da imagem do card")),
    "46.19": R(r("5060349", "MB TRAVA PINO PATIM FREIO 0370/371/LS 1632/1113 FREIO", "TRAVA PINO PATIM", cod_ref="381 994 00 49")),
    "46.20": R(r("5060009", "MB TRAVA PINO PATIM FREIO AR ORIGINAL", "TRAVA PINO PATIM", cod_ref="381.994.0009", info="3,75mm")),
    "46.21": R(r("5069009", "MB TRAVA PATIM FREIO AR 4,00MM", "TRAVA PINO PATIM", info="4,00mm")),
    "46.22": R(r("5060582", "MB TRAVA PINO PATIM MODERNO 364-1313/2213", "TRAVA PINO PATIM", cod_ref="364 994 70 09")),
    "46.23": R(r("5060576", "MB TRAVA PINO PATIM 30MM ANT. L 1313/1513/2013/OF", "TRAVA PINO PATIM", cod_ref="302 994 02 09")),
    # pág. 47
    "47.1": R(r("5061175", "MB ARRUELA ENCOSTO 1313 FINA", "ARRUELA ENCOSTO")),
    "47.2": R(r("5061176", "MB ARRUELA ENCOSTO 1313 LARGA", "ARRUELA ENCOSTO", info="(65x98mm) | Código impresso no card como 061176")),
    "47.3": R(r("5060971", "MB ARRUELA ENCOSTO P CAPA 1113", "ARRUELA ENCOSTO", info="(62x85mm)")),
    "47.4": R(r("5061841", "MB ARRUELA ENCOSTO FREIO AR", "ARRUELA ENCOSTO", info="(75x95mm)")),
    "47.6": R(r("5063462", "MB ARRUELA TRAVA MANGA 608D 55 X 24MM", "ARRUELA TRAVA MANGA", cod_ref="324.334.0062",
                aplicacao="608D 708E 709 912")),
    "47.7": R(r("5061029", "MB ARRUELA TRAVA MANGA 608D 55 X 24MM", "ARRUELA TRAVA MANGA", cod_ref="355.332.0062",
                aplicacao="Freio a ar todos")),
    "47.8": R(r("5060362", "MB ARRUELA TRAVA MANGA EIXO INT 60,0 X EXT 115,6 X ESP 5,0 MM", "ARRUELA TRAVA MANGA",
                aplicacao="Axor todos (VL5/1)", info="60MM / 115,6 | Logo Axor")),
    "47.13": R(r("9010872", "ARRUELA TRAVA CUBO DIANTEIRO MANGA EIXO", "ARRUELA TRAVA CUBO", montadora="Volkswagen",
                 aplicacao="8150OD / 9150OD / 8/9150EOD", info="Int 22MM X Ext 60MM")),
    "47.14": R(r("9010170", "ARRUELA TRAVA CUBO DIANTEIRO MANGA EIXO", "ARRUELA TRAVA CUBO", montadora="Volkswagen",
                 aplicacao="8.150 EOD / 9.150 EOD", info="Int 25MM / Ext 70MM")),
    "47.15": R(r("9010906", "ARRUELA TRAVA CUBO DIANTEIRO MANG EIXO", "ARRUELA TRAVA CUBO", montadora="Volkswagen",
                 aplicacao="13/15180E / 17250E / 24250E / 19320E")),
    "47.19": R(r("5060972", "ARRUELA SCANIA DIANT SC 112/113/94/114/124", "ARRUELA", cod_ref="301.519", montadora="Scania",
                 info="(40 X 71,5 X 85 mm)")),
}
for _k in [k for k in AJ if k.startswith("46.") or k.startswith("47.")]:
    for _rec in AJ[_k]["records"]:
        _rec.setdefault("montadora", "Mercedes-Benz")

NOTAS = [
    "p43: o código 4381131 aparece como ANEL ELÁSTICO EXTERNO 28MM e também como TRAVA EIXO S 25,5MM; 4380868 como anel 30MM e trava 27,5MM; 4380869 como anel 32MM e trava 29MM; 4380870/4381141/4381142 também se repetem — registrados conforme cada card.",
    "p45: código 50600768 (TRAVA ARANHA GUERRA MODERNA) está impresso com 8 dígitos no catálogo.",
    "p46: 5061480 e 5060004 aparecem em dois cards cada (descrições diferentes) — ambos registrados.",
    "p47 card 2: código impresso '061176'; o texto do PDF traz 5061176 (usado na planilha).",
]
