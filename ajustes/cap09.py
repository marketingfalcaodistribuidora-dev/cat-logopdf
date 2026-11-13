# Capítulo 9 - Retentores e Diafragmas (págs. 74-83) — leitura visual card a card


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


def mont(t):
    m = {"MB": "Mercedes-Benz", "SC": "Scania", "VW": "Volkswagen", "FORD": "Ford", "IVECO": "Iveco", "AGRALE": "Agrale",
         "GM": "GM", "FIAT": "Fiat", "FIAT ALLIS": "Fiat Allis", "FNM": "FNM", "VOLVO": "Volvo"}
    return ", ".join(m.get(x.strip(), x.strip().title()) for x in t.split(","))


# pág. 74 — tabela Sabo (fotos genéricas + 2 fotos identificadas pela ref.) e tabela Arca
_F_SABO = {"rect": [476, 125, 557, 186]}
_SABO = [
    ("5060310", "RETENTOR SABO CARRETA 00310B", "00310B", ""),
    ("5062753", "RETENTOR SABO DIANT MB 812/912 02753BGRG", "02753BGRG", ""),
    ("5061149", "RETENTOR SABO EIXO PILOTO GM 01149BR", "01149BR", ""),
    ("5062395", "RETENTOR SABO FORD F1000 02395BAGG", "02395BAGG", ""),
    ("5061549", "RETENTOR SABO MB DIANT 1620 01549BRA", "01549BRA", "8801549"),
    ("5062049", "RETENTOR SABO MB DIANTEIRO 1620 02049BG", "02049BG", "8802049"),
    ("5061884", "RETENTOR SABO MB TRAZ 01884BRAG", "01884BRAG", "8801884"),
    ("5061735", "RETENTOR SABO MB TRAZ F OLEO1313/15 01735BG", "01735BG", "8801735"),
    ("5060516", "RETENTOR SABO MB TRAZ 0516BG", "0516BG", "8800516"),
    ("5067338", "RETENTOR SABO RODA TRAS 07338BAYF", "07338BAYF", ""),
    ("5067375", "RETENTOR SABO RODA TRAS VW 6.80 07375BY", "07375BY", ""),
    ("5060188", "RETENTOR SABO VW 3/4 00188-BA", "00188-BA", "8800188"),
    ("5062713", "RETENTOR SABO VW/FOR/1620 GROSSO 02713BR", "02713BR", ""),
    ("5062484", "RETENTOR SABO VW/FORD DIANT MOD 02484BGE", "02484BGE", "8802484"),
    ("5062483", "RETENTOR SABO WOLKS/FORD DIANT 02483BGE", "02483BGE", "8802483"),
    ("5062485", "RETENTOR SABO WOLKS/FORD TRAS FINO 02485BY", "02485BY", "8802485"),
    ("5067888", "RETENTOR SABO CAIXA MUDANCA 07888GR", "07888GR", ""),
]
_FOTO_SABO = {"5062713": {"rect": [481, 217, 551, 324]}, "5067888": {"rect": [486, 352, 546, 425]}}
_ARCA = [
    ("8800188", "RETENTOR (00188-BA) / ARCA 5118 VW 3/4", "00188-BA / Arca 5118", "5060188"),
    ("8801549", "RETENTOR (01549-BR) / ARCA 5178 DIANT OF1620 100 X 128 X 13", "01549-BR / Arca 5178", "5061549"),
    ("8801923", "RETENTOR (01923-BG) / ARCA 5122 RODA TRAS VW 6.90/7.90S/7.11", "01923-BG / Arca 5122", ""),
    ("8802049", "RETENTOR (002049-BG) / ARCA 5057 DIANTEIRO FREIO AR", "002049-BG / Arca 5057", "5062049"),
    ("8802483", "RETENTOR (02483-BGE) / ARCA 5399 VW/FORD DIANT", "02483-BGE / Arca 5399", "5062483"),
    ("8802484", "RETENTOR (02484-BGE) / ARCA 5177 VW/FORD DIANT VW 14.150 A 35.3", "02484-BGE / Arca 5177", "5062484"),
    ("8802485", "RETENTOR (02485-BY) / ARCA 5400 VW/FORD DIANT VW 14.150 A 35.3", "02485-BY / Arca 5400", "5062485"),
    ("8800500", "RETENTOR (00500-BAG) / ARCA 5418 MB PINHAO MERCEDES", "00500-BAG / Arca 5418", ""),
    ("8807790", "RETENTOR (07790-BY) / ARCA 5839 SCANIA TRAS INT SERIE04", "07790-BY / Arca 5839", ""),
    ("8808316", "RETENTOR (08316-BRY) / ARCA 5840 SCANIA TAMPA ARRASTO", "08316-BRY / Arca 5840", ""),
    ("8802093", "RETENTOR (02093-BRG) / ARCA 5116 SC RODA TRAS", "02093-BRG / Arca 5116", ""),
    ("8800269", "RETENTOR (00269-BR) / ARCA 5299 SC RODA TRAS", "00269-BR / Arca 5299", ""),
    ("8802753", "RETENTOR (02753BRG) / ARCA 5164 DIANT MB 709/914", "02753BRG / Arca 5164", ""),
    ("8801735", "RETENTOR (01735BG) / ARCA 5036 MB RODA TRAS", "01735BG / Arca 5036", "5061735"),
    ("8801884", "RETENTOR (01884BRAG) / ARCA 5054 MB RODA TRAS", "01884BRAG / Arca 5054", "5061884"),
    ("8800516", "RETENTOR (00516BG) / ARCA 5344 MB RODA TRAS", "00516BG / Arca 5344", "5060516"),
    ("88012020", "RETENTOR (12020-BRY) / ARCA 12020 SC TAMP ARRASTO VERDE", "12020-BRY / Arca 12020", ""),
]


def P75(codigo, desc, subst, dim, apl, compat, rel, info=""):
    return R(r(codigo, desc, "RETENTOR", cod_ref=subst, aplicacao=apl, montadora=mont(compat), marca="Arca",
               variacoes="Produtos relacionados: " + rel, info=" | ".join(x for x in ("Dimensões: " + dim, info) if x)))


def D(codigo, tipo_n, pol, oem, apl, med, bins, info=""):
    return R(D1(codigo, tipo_n, pol, oem, apl, med, bins, None, info))


def D1(codigo, tipo_n, pol, oem, apl, med, bins, rect, info=""):
    d = r(codigo, f"DIAFRAGMA BINS TIPO {tipo_n} ({pol})", "DIAFRAGMA", cod_ref=oem, aplicacao=apl, marca="BINS",
          variacoes="Código BINS " + bins, info=" | ".join(x for x in ("Medidas " + med, info) if x))
    if rect:
        d["foto_spec"] = {"rect": rect}
    return d


AJ = {
    "74.1": R(*[r(c, d, "RETENTOR", cod_ref=ref, marca="Sabo", variacoes=(f"Equivalente Arca: {arca}" if arca else ""),
                  foto_spec=_FOTO_SABO.get(c, _F_SABO)) for c, d, ref, arca in _SABO]),
    "74.2": R(*[r(c, d, "RETENTOR", cod_ref=ref, marca="Arca", variacoes=(f"Equivalente Sabo: {sabo}" if sabo else ""))
                for c, d, ref, sabo in _ARCA]),
    # ---------------- pág. 75 (cards individuais Arca) ----------------
    "75.1": P75("8801549", "RETENTOR (01549-BR) / ARCA 5178 DIANT OF 1620", "006.997.9346", "100 x 125 x 13",
                "Cubo de roda dianteira", "MB", "01549-BR / 5061549"),
    "75.2": P75("8800500", "RETENTOR (00500-BAG) / ARCA 5418 MB PINHAO MB", "008.997.0747 / 345.997.7646", "68 x 90 x 13",
                "Pinhão (saída) (2 para 3 eixo)", "MB", "00500-BAG"),
    "75.3": P75("8802049", "RETENTOR (01923-BG) / ARCA 5122 RODA TRAS VW", "010.997.8147 / 345.997.8446 / 007.997.3646",
                "99,9 x 119,95 x 13", "Cubo de roda dianteira", "MB", "002049-BG / 5062049",
                "Título do card repete o texto do 8801923; dimensões e relacionados são do 02049-BG"),
    "75.4": P75("8800516", "RETENTOR (00516BG) / ARCA 5344 MB RODA TRAS", "000.997.7446 / 344.997.7346 / 017.997.1147 / 300.278",
                "110 x 139,95 x 13", "Cubo de roda traseira (freio hidráulico)", "MB, SC", "00516-BG / 5060516"),
    "75.5": P75("8802753", "RETENTOR (02753BRG) / ARCA 5164 DNT MB 709/91", "688.997.7147 / 017.997.3047 / 4002.010.098.00.4",
                "75 x 95 x 13", "Cubo de roda dianteira", "MB, AGRALE", "02753-BRG"),
    "75.6": P75("8801735", "RETENTOR (01735BG) / ARCA 5036 MB RODA TRAS",
                "016.997.7747 / 345.997.8046 / 345.997.7046 / 016.997.7747 / 015.997.5647", "125 x 149,95 x 15",
                "Cubo de roda (eixo traseiro HL4 com reforço / R390)", "MB", "01735-BG / 5061735"),
    "75.7": P75("8801884", "RETENTOR (01884BRAG) / ARCA 5054 MB RODA TRAS",
                "010.997.8147 / 345.997.8346 / 345.997.8346 / 308.997.7346 / 015.997.2647", "120 x 145 x 15",
                "Cubo de roda traseira (freio a ar)", "MB", "01884-BRAG / 5061884"),
    "75.8": P75("8802484", "RETENTOR (02484-BGE) / ARCA 5177 VW/FORD DT", "T16407641 / E5HT1190EA / 81866390",
                "88,9 x 122,95 x 18,7 / 21,7", "Cubo de roda dianteira", "VW, FORD, FIAT ALLIS", "02484-BGE / 5062484"),
    "75.9": P75("8802483", "RETENTOR (02483-BGE) / ARCA 5399 VW/FORD DNT", "77TU.1175C / E5HT.1190.BA / 500054292 / T11.407.641 A",
                "88,9 x 115,4 x 16 / 19", "Cubo de roda dianteira", "VW, FORD, IVECO", "02483-BGE / 5062483"),
    "75.10": P75("8802485", "RETENTOR (02485-BY) / ARCA 5400 VW/FORD DIANT", "T12.501.317 / E5HT.1175.AA / 500054220 / 71494.89",
                 "98,4 x 144,5 x 16", "Cubo de roda traseira", "VW, FORD, IVECO", "02485-BY / 5062485"),
    "75.11": P75("8801923", "RETENTOR (01923-BG) / ARCA 5122 RODA TRAS VW", "T06.501.317 B / 83TU1175A / 50216.6",
                 "82,5 x 114,3 x 12,7", "Cubo de roda traseira", "VW, FORD, FIAT, FNM, IVECO", "01923-BG"),
    "75.12": P75("8800188", "RETENTOR (00188-BA) / ARCA 5118 VW 3/4",
                 "2RD 407 641 / B7T.1190.A / 500054287 / XC45/1190 A2/A / 4002.010.059.00.6", "57,3 x 84 x 8",
                 "Cubo de roda dianteira", "AGRALE, FORD, IVECO, VW", "00188-BA / 5060188"),
    # ---------------- pág. 76 (Arca / Scania) ----------------
    "76.1": P75("8808316", "RETENTOR (08316-BRY) / ARCA 5840 SC TAMP ARR", "140.989.0 / 205.758.6", "75 x 100 x 14",
                "Cubo de roda traseira (cúpula)", "SC", "08316-BRY"),
    "76.2": P75("8807790", "RETENTOR (07790-BY) / ARCA 5839 SC TRAS S4", "140.988.0 / 140.988.9", "142 x 170 x 15,5 / 17,5",
                "Cubo de roda traseira", "SC", "07790-BY / 03750-BRAY"),
    "76.3": P75("8802093", "RETENTOR (02093-BRG) / ARCA 5116 SC RODA TRAS", "179.360", "150,8 x 177,8 x 12,5",
                "Cubo de roda traseira (raiada interno)", "SC", "02093-BRG"),
    "76.4": P75("8800269", "RETENTOR (00269-BR) / ARCA 5299 SC RODA TRAS", "033.352", "75 x 100 x 12",
                "Cubo de roda traseira (externo)", "SC", "00269-BR"),
    # ---------------- pág. 77 ----------------
    "77.1": R(r("8760714", "PASTILHA FREIO DIAT/TRAS MB 1938-S/ACTROS19", "PASTILHA FREIO", montadora="Mercedes-Benz",
                marca="SYL", info="LANÇAMENTO | Seção Freio")),
    "77.2": R(r("5063100", "RETENTOR CARRETA", "RETENTOR", marca="Falcão Distribuidora", info="Embalagem Falcão Distribuidora")),
    "77.3": R(r("4948434", "CORTECO 8434N RET DIANT AXOR ACTROS", "RETENTOR", cod_ref="0139977346", variacoes="Mesmo Sabo: 03682BAGE",
                marca="Corteco", montadora="Mercedes-Benz",
                aplicacao="Retentor cubo dianteiro Mercedes-Benz Axor Actros 8434N Corteco 0139977346 / Mercedes-Benz LS 1929 OM 355/6 LA 1983 a 1998, LS 1932 OM 355/6 LA 1984 a 1987, LS 1933 OM 355/6 LA 1987 a 1988, LS 1935 OM 447 LA 1990 a 2000, LS 1941 OM 447 LA 1990 a 2000, O 370R OM 355/5 1986 a 1987, O 370R/RS/RSD OM 355/6 1984 a 1987, O 370RS OM 355/6 LA 1985 a 1987, O 370RSD OM 355/5 1985 a 1987, O 370RSD OM 355/6 LA 1985 a 1995, O 371 OM 366 1987 a 1997, O 371R OM 355/5 1986 a 1997, O 371R BR-400 OM 355/5 1992 a 1995, O 371RS OM 355/6 1987 a 1993, O 371RS BR-400 OM 355/6 1992 a 1995, O 371RSD OM 447 LA 1987 a 1993, O 371RSD BR 400 OM 355/6 1992 a 1993, O 371RSE OM 355/6 1993, O 371UL OM 366 1993 a 2003, O 371UP OM 355/5 1987 a 1997, O 400 OM 447 LA 1994, O 400R OM 449 A 1993 a 2003, O 400RS OM 447 LA 1992 a 2002, O 400RSD OM 457 LA 1992 a 2002, O 400RSE OM 457 LA 1992 a 2002, O 400RSL OM 447 LA 1992 a 2002, O 500UDA OM 457 LA BlueTec 5 2012 a 2016, O 500UDA 3736 OM 457 LA BlueTec 5 2012 a 2022",
                foto_spec={"rect": [100, 545, 230, 640]}),
              r("4948390", "KIT RETENTOR RODA MB LS1935 O371 O400 O500 TRASEIRO CORTECO 56005K PRO", "KIT RETENTOR", cod_ref="56005KPRO",
                marca="Corteco", montadora="Mercedes-Benz",
                info="Conteúdo da embalagem: 2 retentores, 1 junta, 1 anel O-ring | Tipo de veículo: caminhões / ônibus | Posição: traseiro | Obs: kit de roda sem rolamento",
                foto_spec={"rect": [160, 630, 270, 800]})),
    # ---------------- pág. 78 ----------------
    "78.1": R(*[r(c, d, "RETENTOR") for c, d in [
        ("8800188", "RETENTOR 00188-BA VW 3/4"), ("8801549", "RETENTOR 01549 DIANT OF1620 100 X 128 X 13"),
        ("8807327", "RETENTOR 01735BG MB TR 1313"), ("8806731", "RETENTOR 01884 BRAG MB TRAS F AR"),
        ("8801923", "RETENTOR 01923 RODA TRAS VW 6.90/7.90S/7.11"), ("8802049", "RETENTOR 02049 DIANTEIRO FREIO AR"),
        ("8802483", "RETENTOR 02483BR VW/FORD DIANT"), ("8802713", "RETENTOR 2317 VW/FOR/1620 GROSSO"),
        ("8800500", "RETENTOR 0500 MB PINHAO MERCEDES")]]),
    "78.2": R(r("8802484", "RETENTOR 02484 VW/FORD DIANT VW 14.150 A 35.3", "RETENTOR", montadora="Volkswagen, Ford",
                aplicacao="Retentor do cubo de roda dianteiro - roda dianteira / Ford - 814 / 914 / 1215 / 1415 / 1419 / 1422 / 1617 / 1622 / 2422 / 2425 / 3224 / 3530 / 4030 / 4600 / 6600 / F1000 / F11000 / F12000 / F13000 / F14000 / F2000 / F21000 / F22000 / F4000 / F7000 / F8000 / F8500 / Fairlane")),
    "78.3": R(r("88012020", "RETENTOR (12020-BRY) / ARCA 12020 TR VERDE GROSSO", "RETENTOR", cod_ref="12020-BRY / Arca 12020",
                montadora="Volkswagen, Mercedes-Benz", marca="Arca",
                aplicacao="Volkswagen 24-220 / 24-250 / 35-350 acima de 16 ton. / Mercedes-Benz 1725 / 2638 - todos com eixos Mercedes e Braseixos - Rockwell / O500 - rodoviários e urbanos",
                info="02713 | Alta temperatura")),
    "78.4": R(r("8807790", "RETENTOR 07790BY SCANIA TRAS INT SERIE04", "RETENTOR", cod_ref="1409890 / 2057586 / 1313719",
                montadora="Scania", aplicacao="Retentor do cubo de roda traseiro Scania série 4 P/G/R/T", info="Menor")),
    "78.5": R(r("8808316", "RETENTOR 08316 BRY SCANIA TRAS T124/T142", "RETENTOR", cod_ref="409889 / 1740992", montadora="Scania",
                aplicacao="Retentor do cubo de roda traseiro grande - Scania - R 780 - série 4")),
    # ---------------- pág. 79: capa da seção DIAFRAGMAS (sem produto) ----------------
    "79.1": {"skip": True},
    # ---------------- págs. 80-81: diafragmas BINS ----------------
    "80.1": D("40110201", "12", "5 1/2\"", "897.120.505.4", "Wabco Tristop 12x16 / Normal", "137,5 x 36,2 mm", "4011.0201"),
    "80.2": D("40110620", "12", "5 1/2\"", "2B 56.620", "Knorr Simples 12 / Combinado 12x16", "139,0 x 32,0 mm", "4011.0620"),
    "80.3": D("40110205", "14", "6\"", "897.121.610.4", "Wabco Tristop 14x24", "148,0 x 34,0 mm", "4011.0205"),
    "80.4": D("40110871", "14 FUNDO", "6\"", "2B 54.871", "Knorr 14x24", "149,0 x 48,0 mm", "4011.0871"),
    "80.5": D("40110032", "16", "6\"", "234189", "Bendix", "155,0 x 34,0 mm", "4011.0032"),
    "80.6": D("40110202", "16", "6\"", "897.120.510.4", "Wabco Membrana 16 / Tristop 16/24 Tipo F", "156,4 x 35,0 mm", "4011.0202"),
    "80.7": D("40110363", "16", "6\"", "3B 49.363/2", "Knorr 16x24", "156,0 x 36,0 mm", "4011.0363"),
    "80.8": D("4010217", "27", "7 1/2\"", "897.121.925.4", "Wabco Tristop 27 x 30", "192,0 x 46,0 mm", "4011.0217",
              "Código interno impresso com 7 dígitos (4010217)"),
    "81.1": {"records": [
        D1("40110203", "20", "6 1/2\"", "897.120.520.4", "Wabco Tristop 20x30 / Normal", "168,0 x 34,0 mm", "4011.0203", [150, 122, 268, 201]),
        D1("40110465", "20", "6 1/2\"", "3B 42.465/5", "Knorr 20x24", "168,0 x 34,4 mm", "4011.0465", [434, 117, 556, 200]),
        D1("40110238", "30 FURADO", "8\"", "8017438", "Master Emerg. 24x30 HO", "199,6 x 50,6 mm", "4011.0238", [168, 658, 273, 737]),
        D1("40110240", "30 C/ ANEL", "8\"", "21.14.00240.3", "Master 30x30 / 24x30", "200,0 x 37,0 mm", "4011.0240", [448, 666, 564, 744])]},
    "81.2": {"records": [
        D1("40110100", "24", "7\"", "234100", "Bendix 24x30 / 24 Normal", "178,0 x 34,8 mm", "4011.0100", [137, 292, 271, 387]),
        D1("40110210", "24 C/ ANEL", "7\"", "21.14.FM02", "Master 24x24 / 16x24 / 14x24", "178,0 x 35,0 mm", "4011.0210", [439, 299, 555, 374]),
        D1("40110208", "24 FUNDO", "7\"", "897.120.536.4", "Wabco Tristop 24x24 / 30x30", "177,0 x 44,5 mm", "4011.0208", [137, 484, 262, 631]),
        D1("40110101", "30", "8\"", "234101", "Bendix 30x30 / 24x30 / 30 Normal", "200,0 x 37,0 mm", "4011.0101", [402, 474, 548, 572])]},
    # ---------------- pág. 82: tabelas de diafragmas (BINS e Ditech) ----------------
    "82.2": R(*[r(c, d, "DIAFRAGMA", marca="BINS") for c, d in [
        ("40110620", "BINS DIAF TIPO 12 (5 1/2) KNORR SIMPLES"), ("40110201", "BINS DIAF TIPO 12 (5 1/2) WABCO TRISTOP"),
        ("40110205", "BINS DIAF TIPO 14 (6) WABCO TRISTOP 14X24"), ("40110871", "BINS DIAF TIPO 14 FUNDO (6) KNORR"),
        ("40110032", "BINS DIAF TIPO 16 (6) BENDIX"), ("40110363", "BINS DIAF TIPO 16 (6) KNORR 16X24"),
        ("40110202", "BINS DIAF TIPO 16 (6) WABCO / TRISTOP 16/24"), ("40110465", "BINS DIAF TIPO 20 (6 1/2) KNORR 20X24"),
        ("40110203", "BINS DIAF TIPO 20 (6 1/2) WABCO TRISTOP 20X30"), ("40110100", "BINS DIAF TIPO 24 (7) BENDIX 24X30 / 24 NORMA"),
        ("40110210", "BINS DIAF TIPO 24 C/ ANEL (7) MASTER 24X24"), ("40110101", "BINS DIAF TIPO 30 8 SEM ANEL"),
        ("40110240", "BINS DIAF TIPO 30 C/ ANEL (8) MASTER 30X30")]]),
    "82.1": R(*([r(c, d, "DIAFRAGMA", marca="Ditech") for c, d in [
        ("8902252", "DIAF. 5.1/2\" D 2252 133MM 12\" (WABCO) DT."), ("8902543", "DIAF. 6\" D 2543 158MM 20 (KNORR).."),
        ("8902253", "DIAF. 6.1/2\" D 2253 158MM 16\" (WABCO).."), ("8902535", "DIAF. 6.1/2\" D 2535 167MM 20 (WABCO) DT."),
        ("8902212", "DIAF. 7\" D 2212 RASO 178MM 24 DT."), ("8902250", "DIAF. 7\" D 2250 178MM 24C/ANEL (MASTER) DT."),
        ("8902213", "DIAF. 8\" D 2213 S/ANEL 30 (MASTER) DT."), ("89002213", "DIAF. 8\" D 2213A C/ANEL 30 (MASTER) DT."),
        ("8902251", "DIAF. 8\" D 2251 VW C/FURO 30 (MASTER) DT."), ("8902214", "DIAF. 9\" D 2214 (MASTER) DT.")]] +
        [r("89450518", "DIAF. 5.1/2\" MA 138MM 16\" (KNORR).", "DIAFRAGMA", cod_ref="50518", marca="Ditech"),
         r("89450521", "DIAF. 6.1/2 105MM 20\" FUNDO (WABCO) DT", "DIAFRAGMA", cod_ref="50521", marca="Ditech")])),
}
NOTAS = [
    "p79 e p83: páginas de capa (DIAFRAGMAS / AMORTECEDORES DE CABINE), sem produtos.",
    "p80 card 8: código interno impresso com 7 dígitos (4010217) — mantido como no catálogo.",
    "p74: Sabo e Arca têm códigos internos diferentes para o mesmo retentor; cada código é uma linha, com a equivalência da outra marca em Variações.",
    "p74 tabela Sabo: as fotos do card são genéricas, exceto 02713BRY (5062713) e 07888GR (5067888), que têm foto identificada.",
    "p75 card 3: o código 8802049 aparece com o título 'RETENTOR (01923-BG) / ARCA 5122 RODA TRAS VW' (texto repetido do 8801923).",
]
ADD = []
