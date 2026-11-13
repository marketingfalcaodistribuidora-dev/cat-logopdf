# Capítulo 7 - Anel Pista, Buchas e Eixos (págs. 48-56) — leitura visual card a card
MANUAIS = {48}


def r(codigo, descricao, tipo, **kw):
    d = dict(codigo=codigo, descricao=descricao, tipo=tipo)
    d.update(kw)
    return d


def R(*recs, **comuns):
    out = []
    for x in recs:
        d = dict(comuns)
        d.update(x)
        out.append(d)
    return {"records": out}


# ---------------- pág. 48 (molduras sobrepostas: grade lida visualmente) ----------------
_C = [(20, 205), (205, 388), (388, 575)]
_L = [(85, 190), (190, 293), (293, 396), (396, 537), (537, 677), (677, 805)]


def M(lin, col, card, codigo, descricao, tipo, **kw):
    (x0, x1), (y0, y1) = _C[col], _L[lin]
    d = dict(pagina=48, card=card, codigo=codigo, descricao=descricao, tipo=tipo,
             foto_spec={"rect": [x0 + 2, y0 + 2, x1 - 2, y1 - 2]})
    d.update(kw)
    return d


ADD = [
    M(0, 0, 1, "5060782", "ANEL PISTA RANDON RODOVIARIA 127X95X21,5", "ANEL PISTA", montadora="Randon", info="Moderna"),
    M(0, 1, 2, "5063082", "ANEL PISTA RANDON MASTER 127X95X22", "ANEL PISTA", montadora="Randon"),
    M(0, 2, 3, "5064015", "ANEL PISTA NOMA EIXO EXT 127 - INT 94,5 ALT 22", "ANEL PISTA", montadora="Noma"),
    M(1, 0, 4, "5064136", "ANEL PISTA / GUERRA", "ANEL PISTA", montadora="Guerra"),
    M(1, 1, 5, "5060325", "ANEL PISTA GUERRA MODERNA 97MM", "ANEL PISTA", montadora="Guerra", info="127 x 97 x 25"),
    M(1, 2, 6, "5064135", "ANEL PISTA NOMA/KRONE/IDERO EIXO EXT 127 - INT 94,5 - ALT 26", "ANEL PISTA", montadora="Noma, Krone, Iderol"),
    M(2, 0, 7, "5064020", "PORCA CARRETA KRONE EXT 120 - ALT. 15 x 90 MM", "PORCA CARRETA", montadora="Krone"),
    M(3, 0, 8, "5068080", "PORCA CUBO MOD ORIG C TRAVA RANDON 80MM", "PORCA CUBO", montadora="Randon", info="Modelo original | 80MM"),
    M(3, 1, 9, "5068081", "PORCA CUBO MOD ORIG C TRAVA RANDON 80M FIO 2,0", "PORCA CUBO", montadora="Randon", info="Modelo original | 80MM fio 2,0"),
    M(3, 2, 10, "5069190", "PORCA CUBO MOD ORIG C TRAVA GUERRA 90MM", "PORCA CUBO", montadora="Guerra", info="Modelo original | 90MM"),
    M(4, 0, 11, "5064017", "PORCA CARRETA RANDON MENOR ALT. 25,4 x 78 MM", "PORCA CARRETA", montadora="Randon", info="Moderna"),
    M(4, 1, 12, "5064014", "PORCA CARRETA RANDON ALT. 25,4 x 90 MM ROSCA GROSA", "PORCA CARRETA", montadora="Randon",
      info="Antiga | No card: \"PORCA CARRRET RANDON\""),
    M(4, 2, 13, "5019068", "PORCA CARC VW 52,50MM X 16 FIOS CHAVE 65", "PORCA CARCAÇA", cod_ref="2RD501471",
      montadora="Volkswagen, Ford", aplicacao="8.150E / 9.150E (difer. Meritor)"),
    M(5, 0, 14, "5060324", "PORCA GUERRA M80 MODERNA APOS 2000", "PORCA CARRETA", montadora="Guerra"),
    M(5, 1, 15, "5061855", "PORCA EIXO CARRETA GUERRA 90MM", "PORCA CARRETA", montadora="Guerra", aplicacao="Noma, Facchini, Krone"),
    M(5, 2, 16, "5019067", "PORCA CARC VW 3/4 TOOS LEVE", "PORCA CARCAÇA", cod_ref="02989067", montadora="Volkswagen, Ford",
      aplicacao="VW 6.80 / 6.90 / 7.90 / 7.110 Eaton", info="51,50MM X 16 fios (chave 65MM)"),
]

MB = "Mercedes-Benz"
AJ = {
    # ---------------- pág. 49 (marca MIC nas porcas de carcaça) ----------------
    "49.1": {"skip": True},
    "49.2": R(r("5140001", "PORCA CARCACA ACO M65 X 1.5MM 1313 / 1314", "PORCA CARCAÇA", cod_ref="3453560026",
                variacoes="506.0508", info="65X1.5X90mm", montadora=MB, marca="MIC")),
    "49.3": R(r("5140002", "PORCA CARCACA ACO M62 X 1.5MM 1113 / HL-4", "PORCA CARCAÇA", cod_ref="3213560026",
                variacoes="506.0506", info="62X1.5", montadora=MB, marca="MIC")),
    "49.4": R(r("5140003", "PORCA CARCACA ACO -75X1,5MM (FREIO AR) 1313/1513/1519/DIVERSOS", "PORCA CARCAÇA",
                cod_ref="070852075000", info="75X1,5MM", montadora=MB, marca="MIC")),
    "49.5": R(r("5140004", "PORCA CARCACA ACO M52 X 1.5MM 608-D / HL-2", "PORCA CARCAÇA", cod_ref="070852052000",
                aplicacao="Porca carcaça MB 608/708/709/912", info="52 X 1.5MM", montadora=MB, marca="MIC")),
    "49.6": R(r("5140005", "PORCA CARCACA ACO M85 X 1.5MM 370/ 371 / 1721", "PORCA CARCAÇA", cod_ref="070852085000",
                variacoes="506.6515", aplicacao="1524 1525 2325 2425 OF1618 OF1721 1625 O370", info="85X1,5X107,5MM",
                montadora=MB, marca="MIC")),
    "49.7": R(r("5140150", "PORCA CARCACA ACO 49,21 X 12 UN- 16 FIOS 65MM", "PORCA CARCAÇA", cod_ref="BC5Y4252A",
                aplicacao="F350 / F2000 / F4000 / 6.80 / 6.90 / 7.90 / 7.100 / 7.110", montadora=MB + ", Ford, Volkswagen",
                marca="MIC")),
    "49.8": R(r("5061708", "MB PORCA P. CAPA FREIO AR 75X95 1519 2219", "PORCA CAPA", cod_ref="070.852.075.000",
                info="75 X 95", montadora=MB)),
    "49.9": R(r("5060507", "MB PORCA PONTA CAPA ACO 1313 1316 1317 65X83", "PORCA CAPA", cod_ref="322.356.0126", montadora=MB)),
    "49.10": R(r("5140074", "PORCA MANGA DE EIXO DIANT 40MM FREIO A AR", "PORCA MANGA EIXO", cod_ref="3603320272",
                 aplicacao="1318 / 1516 / 1618 / 1620 - todos freio a ar", info="40MM", montadora=MB, marca="MIC")),
    "49.11": R(r("5140224", "ARRUELA ENCOSTO EIXO DIANT 371/1618/OF 1620/1621", "ARRUELA ENCOSTO", cod_ref="3863320062",
                 info="Código impresso como 514.0224", montadora=MB, marca="MIC")),
    "49.12": {"skip": True},  # card só com o logo MIC
    "49.13": R(r("9015144", "PORCA INTERNA CUBO VW TRAS 64.6X89X11.5", "PORCA CUBO", cod_ref="01925824",
                 montadora="Volkswagen, Ford")),
    "49.14": R(r("5141434", "PORCA CARCACA ACO 52,5 X 16 FIOS SEXT 65MM", "PORCA CARCAÇA", cod_ref="BF8T4A063B",
                 aplicacao="F4000 - moderna", montadora="Ford", marca="MIC")),
    "49.15": R(r("5140168", "PORCA CARCACA ACO 3.1/4\" 12 EIXO TRAS 98MM", "PORCA CARCAÇA", cod_ref="T16501475A",
                 aplicacao="Ford - eixo MS145 - MS230 / 235 - Ford Cargo / VW - 16210 / 16170 / 24220 / 24250 / TJG",
                 montadora="Volkswagen, Ford, Volvo, MAN, Iveco, DAF", marca="MIC")),
    "49.16": R(r("5140086", "PORCA CARCACA ACO S/RETENTOR TINKAO F600", "PORCA CARCAÇA", cod_ref="BD2T4252A",
                 aplicacao="Ford - F600 / F750 / GM - D60 / D70 / Tinkão interna VW 13130", montadora="Volkswagen, Ford, GM")),
    # ---------------- pág. 50 ----------------
    "50.1": R(r("5064000", "MB PORCA MANGA EIXO FUNDIDA 40X1,5MM", "PORCA MANGA EIXO", cod_ref="3893320072",
                aplicacao="Mercedes-Benz - 1929 / 1933 / Ônibus 370 / 371 OF1620", montadora=MB)),
    "50.2": R(r("5061473", "MB PORCA MANGA EIXO ACO 24,0 X 43,5 X 73,0MM", "PORCA MANGA EIXO", cod_ref="6563300088",
                aplicacao="Mercedes-Benz - Axor 2640 / 2644", montadora=MB)),
    "50.3": R(r("10015848", "PORCA PONTEIRA CARDAN L/LS 1938/2638", "PORCA PONTEIRA CARDAN", cod_ref="001.990.5550",
                aplicacao="Volvo: VM17 210 / VM23 240 | Mercedes: 1938 / 2423 / 2638 (cód. original 001.990.5550) | Iveco: Cursor 450E37 / 8190E31 / 8450E31 / Eurotech 200E37 / HM450E37 | Volkswagen: Constellation 31.320",
                info="Volvo / MBB / Iveco / Mitsubishi", montadora="Mercedes-Benz, Volkswagen, Volvo, Iveco")),
    "50.4": R(r("5030204", "TAMPA DA MANGA DE EIXO VW 11.130", "TAMPA MANGA EIXO", cod_ref="204.TPE", info="Dimensão da rosca: 48MM",
                montadora="Volkswagen")),
    "50.5": R(r("5030202", "TAMPA INF/SUPE DA MANGA DE EIXO VW 8.150", "TAMPA MANGA EIXO", cod_ref="202.TPE",
                info="Dimensão da rosca: 39MM", montadora="Volkswagen")),
    "50.6": R(r("10015941", "PORCA PINHAO DIFERENCIAL (ROCKWELL) RS 240 (2 VELOC.)", "PORCA PINHÃO DIFERENCIAL",
                cod_ref="TE3.525.215", aplicacao="Diferencial Rockwell RS240 RS245 RS155 MD145 / Volkswagen 14200 / 12140H / 14150 / VW todos",
                info="Rosca 1\"1/2 X 1,50", montadora="Volkswagen")),
    "50.7": R(r("5030205", "TAMPA INF/SUPE DA MANGA DE EIXO VW 14.210", "TAMPA MANGA EIXO", cod_ref="205.TPE",
                info="Dimensão da rosca: 47MM", montadora="Volkswagen")),
    "50.8": R(r("5030203", "TAMPA INF/SUPE DA MANGA DE EIXO VW 9.150", "TAMPA MANGA EIXO", cod_ref="203.TPE",
                info="Dimensão da rosca: 39MM", montadora="Volkswagen")),
    "50.9": R(r("5030207", "TAMPA INF/SUPE DA MANGA DE EIXO VW 5.140", "TAMPA MANGA EIXO", cod_ref="207.TPE",
                info="Dimensão da rosca: 39MM", montadora="Volkswagen")),
    # ---------------- pág. 51 ----------------
    "51.1": R(r("5069800", "BUCHA S TECNYL CONICA 38MM", "BUCHA EIXO S", info="38MM interno", montadora="Randon, Guerra")),
    "51.2": R(r("5067061", "BUCHA S TECNYL RANDON 38MM", "BUCHA EIXO S", info="Int 38MM | Alt 39MM", montadora="Guerra")),
    "51.3": R(r("5067058", "BUCHA S TECNYL RANDON 41MM", "BUCHA EIXO S", info="Int 41MM | Alt 42MM", montadora="Randon")),
    "51.4": {"skip": True},  # rótulo "38MM INTERNO" sobre a foto do card 51.1
    "51.5": R(r("5060614", "BUCHA EIXO S CONICA TECNYL 38MM PRETA", "BUCHA EIXO S")),
    "51.6": R(r("5063840", "BUCHA S INTEIRICA C/ANEL 38MM NYLON", "BUCHA EIXO S", info="Int 38MM | Alt 40MM", montadora="Guerra")),
    "51.7": R(r("5064180", "BUCHA S INTEIRICA C/ANEL 41MM NYLON", "BUCHA EIXO S", info="Int 41MM | Alt 40MM")),
    "51.8": R(r("5060099", "REP EIXO S TECNYL GUERRA MENOR", "REPARO EIXO S", info="Int 38MM | Alt 39MM | 38MM interno", montadora="Guerra")),
    "51.9": R(r("5060098", "REP EIXO S TECNYL RANDON MAIOR", "REPARO EIXO S", info="Int 41MM | Alt 44MM | 38MM interno", montadora="Randon")),
    "51.10": R(r("5060946", "REP EIXO S TUBELESS CARRETA MODERNA NYLON", "REPARO EIXO S", info="38MM / 41MM", montadora="Randon")),
    "51.11": R(r("5063899", "REP EIXO S TECNYL MENOR GUERRA PRETO 38MM", "REPARO EIXO S", info="38MM / 38MM", montadora="Guerra")),
    "51.12": R(r("5063898", "REP EIXO S TECNYL MENOR GUERRA BUCHA LISA 38MM", "REPARO EIXO S", info="Bucha lisa | 38MM / 38MM",
                 montadora="Guerra")),
    # ---------------- pág. 52 ----------------
    "52.1": R(r("5060942", "REP EIXO S TUBELESS BUCHA FERRO", "REPARO EIXO S", info="42MM", montadora="Randon")),
    "52.2": R(r("5060941", "REP EIXO S TUBELESS COMPLETO C RET", "REPARO EIXO S", info="41MM / 38MM", montadora="Randon")),
    "52.3": R(r("5060019", "REP EIXO S NOMA C BUCHA FERRO", "REPARO EIXO S", info="38MM interno | 34MM", montadora="Noma")),
    "52.4": R(r("5060961", "REP EIXO S TECNYL TUB RANDON", "REPARO EIXO S", info="38MM interno / 41MM interno | 42MM", montadora="Randon")),
    "52.5": R(r("5060097", "REP EIXO S GUERRA BUCHA FERRO", "REPARO EIXO S", info="38MM interno / 38MM interno | 40MM", montadora="Guerra")),
    "52.6": R(r("5065863", "BUCHA S FERRO GUERRA TUBLLES C ANEL", "BUCHA EIXO S", info="Int 38MM | Alt 40MM", montadora="Guerra")),
    "52.7": R(r("5060945", "REP EIXO S GUERRA FERRO MODER", "REPARO EIXO S", info="38MM interno | 34MM", montadora="Guerra")),
    "52.8": R(r("5064098", "BUCHA AÇO DO S RANDON NOVA", "BUCHA EIXO S", info="Int 41MM | Alt 25MM", montadora="Randon")),
    "52.9": R(r("5067059", "BUCHA EIXO S TUBILES FERRO", "BUCHA EIXO S", info="Int 41MM | Alt 42MM", montadora="Randon")),
    "52.10": R(r("5063841", "REP EIXO S GUERRA 38MM (TECNIL PRETO + BUCHA FERRO)", "REPARO EIXO S", info="38MM interno | 40MM",
                 montadora="Guerra")),
    "52.11": R(r("5060963", "REP EIXO S TECNYL TUB RANDON BUCHA PRETA41MM", "REPARO EIXO S", info="38MM interno | 41MM / 40MM",
                 montadora="Randon")),
    "52.12": R(r("5061538", "REP EIXO S F GUERRA EXPANSAO BUCHA PLAST 38MM", "REPARO EIXO S", info="LANÇAMENTO 03/2025 | 38MM / 35MM",
                 montadora="Guerra")),
    # ---------------- pág. 53 (descrições impressas dentro das imagens) ----------------
    "53.1": R(r("5060940", "BUCHA S NYLON FLANGE", "BUCHA EIXO S", info="42 MM", montadora="Randon")),
    "53.2": R(r("5060939", "BUCHA S NYLON MANCAL 38 M", "BUCHA EIXO S", info="Cônica | Tubeless", montadora="Guerra, Randon")),
    "53.3": R(r("5060679", "BUCHA NYLON DO S SISTEMA BENDIX (MENOR)", "BUCHA EIXO S", info="Antiga | INT38 EX48 ALT30", montadora="Randon")),
    "53.4": R(r("5060680", "BUCHA NYLON DO S SISTEMA MASTER (MAIOR)", "BUCHA EIXO S", info="Antiga | INT38 EX48 ALT34", montadora="Randon")),
    "53.5": R(r("5060706", "BUCHA S NYLON RANDON ANTIGA FINA 42 MM INT", "BUCHA EIXO S", info="Antiga", montadora="Randon")),
    "53.6": R(r("5060598", "BUCHA S ACO LISA ANTIGA", "BUCHA EIXO S", info="41,5INT X 48EXT X 30A")),
    "53.7": R(r("5060393", "BUCHA S FERRO MAIOR", "BUCHA EIXO S", info="Antiga | INT38M EXT48M ALT30", montadora="Randon")),
    "53.8": R(r("5061359", "MB REP EIXO S FREIO DIANT C BUCHA LATAO", "REPARO EIXO S", cod_ref="3454200041",
                variacoes="Similar: Boechat 4620 / Master EX206 / Master 2210FM350",
                aplicacao="MB Mercedes-Benz freio a ar", info="Dianteiro | Completo | Peso 1.735 kg | Altura 1.5 cm | Largura 1.5 cm | Profundidade 1.5 cm",
                montadora=MB)),
    "53.9": R(r("5060341", "MB REP EIXO S C/ROTULA C/DEF T", "REPARO EIXO S", cod_ref="3454200341",
                aplicacao="MB Mercedes-Benz freio a ar", info="Traseiro | Peso 1.735 kg | Altura 1.5 cm | Largura 1.5 cm | Profundidade 1.5 cm",
                montadora=MB)),
    "53.10": R(r("5060778", "ARRUELA S PEQUENA 48 EXT x 32 INT", "ARRUELA EIXO S"),
               r("5060779", "ARRUELA S MEDIA 62 EXT x 38 INT", "ARRUELA EIXO S"),
               r("5060780", "ARRUELA S GRANDE 62 EXT x 42 INT", "ARRUELA EIXO S")),
    "53.11": R(r("5065295", "ARRUELA S RETÂNGULAR 38 MM", "ARRUELA EIXO S"), r("5065318", "ARRUELA S RETÂNGULAR 41,5 MM", "ARRUELA EIXO S")),
    "53.12": R(r("50923016", "ARRUELA ENCOSTO EIXO S C/ABA", "ARRUELA EIXO S", info="Int 41MM", montadora="Randon")),
    # ---------------- pág. 54 ----------------
    "54.1": R(r("5064132", "BUCHA S NY LISA INT32,4 EXT41,2 AL30 VW TDS", "BUCHA EIXO S", cod_ref="2RD607025",
                aplicacao="VW todos com freio \"S\"", info="Int: eixo 32MM | 41,2 X 32,4 X 30 | Bucha eixo S plást.", montadora="Volkswagen")),
    "54.2": R(r("5017064", "ANEL ORING VEDACAO VOLKS MANCAL", "ANEL VEDAÇÃO MANCAL", cod_ref="2RD607064 / 10112194",
                aplicacao="Volkswagen: 5140E / 8150E / 815E plus / 9150E / 5150 / 8/9/10 / 8160 ano 2005 a 2019 / Micro-ônibus: 8150EOD / 9150EOD ano 2004 a 2016",
                info="Anel vedação mancal freio sistema tubeless (duplo) | Int: eixo 30MM / eixo 32MM", montadora="Volkswagen")),
    "54.3": R(r("8777060", "SUPORTE S KIT TUBELESS VW 8150/9150 FORD815", "SUPORTE EIXO S", cod_ref="2RD607060 / BF5X1233AA",
                aplicacao="Volkswagen: 7100 8100 8120 8140 8150 / Ford Cargo 712 - 21/05/2007 a 30/01/2012 / 815 - após 2005 / 816 1119 - após 2012",
                info="Int: eixo 30MM / eixo 32MM | Anel", montadora="Volkswagen, Ford")),
    "54.4": R(r("5068150", "REP EIXO S VW 8150/9150 FORD 815/816", "REPARO EIXO S",
                aplicacao="Reparo eixo S buchas de poliacetal Master 325 HD / eixos 32 mm / VWC - 8150/9150 / Volare W8/W9 / Ford 815/816 / MB-710 Plus",
                info="Int: eixo 32MM / 30MM | Anel | Retentor", montadora="Volkswagen, Ford, Agrale")),
    "54.5": R(r("5065645", "REP EIXO S TRAS VW 7100/8140 / FORD 814/816", "REPARO EIXO S", cod_ref="2RD607025",
                variacoes="QA5645", aplicacao="Rep eixo S VW 7100/8140 / Ford 814/816", info="Eixo 32MM / 30MM",
                montadora="Volkswagen, Ford")),
    "54.6": R(r("5065646", "REP EIXO S DIANT VW 7100/8140 / FORD 814/816", "REPARO EIXO S", cod_ref="2TA.604.464",
                variacoes="QA-5646", aplicacao="Reparo eixo S dianteiro bucha de poliacetal Master 325HD / eixo 32MM / VWC - 7100-8140 / Ford - 814/816",
                info="Eixo 32MM / 30MM", montadora="Volkswagen, Ford")),
    "54.7": R(r("5065080", "REP EIXO S VW DIANT/TRAS 10 EST QA-5080", "REPARO EIXO S", cod_ref="TE3698719", variacoes="QA-5080",
                aplicacao="Volkswagen caminhões c/ freios Master (c/ eixo 10 dentes) / Ford caminhões c/ freios Master (c/ eixo 10 dentes)",
                info="Eixos 41MM / 32MM / 30MM / 28MM", montadora="Volkswagen, Ford")),
    "54.8": R(r("5060944", "BUCHA S NYLON GUERRA MODERNA", "BUCHA EIXO S", info="39MM | 38MM interno | Também para linha Volkswagen",
                montadora="Volkswagen, Guerra")),
    "54.9": R(r("5060943", "BUCHA S ACO GUERRA MODERNA", "BUCHA EIXO S", info="39MM | 38MM interno | Também para linha Volkswagen",
                montadora="Volkswagen, Guerra")),
    "54.10": R(r("5013280", "BUCHA S NY VOLKS MENOR 2RD607066", "BUCHA EIXO S", cod_ref="2RD607066",
                 aplicacao="VW 5140E / 7100 / 8140 / 8150 / 9150", info="Int 32 MM X Ext 53MM X Alt 26 MM", montadora="Volkswagen, Ford")),
    "54.12": R(r("5060783", "RETENTOR S 40,00 X 50,90 X 08,00 MM", "RETENTOR EIXO S"),
               r("5060785", "RETENTOR S 38,00 X 52,00 X 10,00MM", "RETENTOR EIXO S"),
               r("5065132", "RETENTOR EIXO S GUERRA FERRO F 38X47,6X6,5", "RETENTOR EIXO S", montadora="Guerra"),
               r("5065141", "RETENTOR EIXO S TUBLES FERRO 41,1X50,8X6", "RETENTOR EIXO S")),
    # ---------------- pág. 55 ----------------
    "55.1": R(r("5060975", "EIXO S RANDON EXPANSOR LE", "EIXO S", cod_ref="2210FM254",
                aplicacao="Carreta: carretas em geral 3º eixo Scania / Volvo e Zurlo (\"S\" extra longo)",
                info="609MM | 41MM | 59MM | 51MM | 28 estrias", montadora="Randon, Scania, Volvo")),
    "55.2": R(r("5060974", "EIXO S RANDON EXPANSOR LD", "EIXO S", cod_ref="2210FM254",
                aplicacao="Carreta: carretas em geral 3º eixo Scania / Volvo e Zurlo (\"S\" extra longo)",
                info="609MM | 41MM | 59MM | 51MM | 28 estrias", montadora="Randon, Scania, Volvo")),
    "55.3": R(r("8770005", "SUPORTE S RET TUBELESS", "SUPORTE EIXO S")),
    "55.4": R(r("8770006", "SUPORTE S RET TUBELESS GRAXEIR", "SUPORTE EIXO S")),
    "55.5": R(r("8770012", "SUPORTE S KIT", "SUPORTE EIXO S")),
    "55.6": R(r("8770241", "SUPORTE S KIT TUBELESS CARR 16,5X8 COMPLE", "SUPORTE EIXO S", info="Tipo Master carretas todos | 38MM")),
    "55.7": R(r("8770441", "SUPORTE S COMPLETO 38MM TODOS", "SUPORTE EIXO S", info="Int 38MM | Montado")),
    "55.8": R(r("5061531", "ALOJAMENTO MODERNO CARRETA", "ALOJAMENTO EIXO S", montadora="Randon")),
    "55.9": R(r("0751190", "PF TRANSMISSAO 10 X 30 1113", "PARAFUSO TRANSMISSÃO", montadora=MB)),
    "55.10": R(r("751020", "PF TRANSMISSAO 10 X 20MM CRUZETA VW", "PARAFUSO TRANSMISSÃO", montadora="Volkswagen")),
    "55.11": R(r("5061530", "ALOJAMENTO SOLDAVEL BUCHA EIXO S FLANGE CARRETA 2012", "ALOJAMENTO EIXO S", montadora="Guerra")),
    "55.12": R(r("9025152", "PF TRANSMISSAO 3/8 X 20MM CRUZETA WV", "PARAFUSO TRANSMISSÃO", montadora="Volkswagen")),
    "55.13": R(r("0751232", "PF TRANSMISSAO 12 X 32 1313/15", "PARAFUSO TRANSMISSÃO", montadora=MB)),
    "55.14": R(r("750814", "PF TRANSMISSAO 08 X 14 P/CRUZETA", "PARAFUSO TRANSMISSÃO", montadora="Iveco")),
    # ---------------- pág. 56 ----------------
    "56.1": R(r("5150070", "REP EIXO S KIT BI PARTIDO SPIDER SOLDADO/MANC", "REPARO EIXO S BI PARTIDO",
                info="Kit troca rápida: cônica bi partida nylon, mancal bi partido aço, 4 parafusos com porca, bucha bi partida com aba Tecnyl, unha da flange soldado | Montado / desmontado",
                montadora="Randon, Facchini")),
    "56.2": R(r("5150080", "REP EIXO S KIT BI PARTIDO PARCIAL FLANGE SOLD", "REPARO EIXO S BI PARTIDO",
                info="Para alojamento parafusado | Kit troca rápida: cônica bi partida nylon, mancal bi partido nylon, 4 parafusos com porca, mancal bucha bi partida com aba Tecnyl, unha da flange parafusado | 41MM / 38MM | Montado / desmontado",
                montadora="Randon, Facchini")),
    "56.3": R(r("5150060", "REP EIXO S KIT BI PARTIDO P/FLANGE SOLDADA", "REPARO EIXO S BI PARTIDO",
                info="Para alojamento soldado | Kit troca rápida: cônica bi partida nylon, mancal bi partido nylon, 4 parafusos com porca, mancal bucha bi partida com aba Tecnyl, unha da flange parafusado | 41MM / 38MM | Montado / desmontado",
                montadora="Randon, Facchini")),
}

NOTAS = [
    "p49 card 11: código impresso '514.0224' (com ponto) registrado como 5140224.",
    "p49 card 12 e p54 card 11: cards sem produto (logo MIC / card vazio).",
    "p48: '5064014 - PORCA CARRRET RANDON' — grafia do catálogo corrigida para PORCA CARRETA na descrição.",
]
