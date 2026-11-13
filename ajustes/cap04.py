# Capítulo 4 - Sapata e Lona Freio (págs. 33-39) — ajustes da revisão visual
# As tabelas de conversão e muitas aplicações das lonas são IMAGENS no PDF: foram transcritas da leitura visual.
# Prefixos observados: 875xxx = Cobreq (logo na maioria), 872xxx = Thermoid, 873xxx = Frum; sapatas 878xxxx = Momag.


def conv(duroline, frasle, lonaflex, thermoid, cobreq):
    partes = [("Duroline", duroline), ("Fras-le", frasle), ("Lonaflex", lonaflex), ("Thermoid", thermoid), ("Cobreq", cobreq)]
    return "Conversão: " + " | ".join(f"{m} {v}" for m, v in partes if v)


def LONA(codigo, ref, cv, aplicacao="", montadora="", marca="", info=""):
    return {"records": [dict(codigo=codigo, descricao=f"LONA FREIO {ref}", tipo="LONA FREIO", cod_ref=ref, variacoes=cv,
                             aplicacao=aplicacao, montadora=montadora, marca=marca, info=info)]}


def SAP(codigo, descricao, cod_ref="", variacoes="", aplicacao="", montadora="", info="", marca="Momag"):
    return {"records": [dict(codigo=codigo, descricao=descricao, tipo="SAPATA FREIO", cod_ref=cod_ref, variacoes=variacoes,
                             aplicacao=aplicacao, montadora=montadora, marca=marca, info=info)]}


C636 = conv("DC/333", "CA/33", "L-636", "TH-204", "4533T")
A636 = "Daf, Fachini, Gotti, Iderol, Ford, Guerra, Iveco, Randon, Volvo"
M636 = "DAF, Volvo, Facchini, Guerra, Randon, Ford"
C637 = conv("DC/381", "FD/81", "L-637", "TH-187", "0183T-140")
C638 = conv("DC/332", "CA/32", "L-638", "TH-4516", "4644T")
A638 = ("Antonini, Biselli, Contin, Engesa-FNV (Fruehauf), Fachini, Golive, Iderol, Iveco, Krone, Mafersa, Maringá, "
        "Massari, Matalpi, Noma, Pastre, Randon, Recrusul, Schiffer, Rosseti, Guerra")
M638 = "Iderol, Facchini, Noma, Iveco, Krone, Randon, Guerra, Recrusul"
C219 = conv("DFW/977", "FD/77", "L-219", "TH-202", "0811T")
C733 = conv("DV/903", "VV/303", "L-733", "TH-206", "0725T")
C734 = conv("DV/904", "VV/304", "L-734", "TH-207", "0726T")
C223 = conv("DFW/987", "FD/87", "L-223", "TH-165", "0814T")
C224 = conv("DFW/988", "FD/88", "L-224", "TH-166", "0815T")
C227 = conv("DM/588", "MB/188", "L-227", "TH-164", "0137T")
C559 = conv("DFW/959", "FD/59", "L-559", "TH-259", "0821T-140")
A559 = "Agrale, Iveco, Marcopolo, Mercedes-Benz, Volkswagen / Agrale MA 92 eixo traseiro e cardan, Agrale MA 85 eixo traseiro e cardan, Agrale 9200 eixo traseiro e cardan"
C1059 = conv("", "FD/165", "L1059", "TH-257", "0830T-142")
A1059 = "Std Agrale Ônibus W9 / M / Agrale MA 10.0 14, Agrale MA 10000 14, Agrale MA 10000WL 14"
C640 = conv("DFW/910", "4710", "L-640", "TH-191", "4710T")
C309 = conv("DS/730", "SV/230", "L-309", "TH-179", "0713")
C310 = conv("DS/731", "SV/231", "L-310", "TH-181", "0714")
C551 = conv("DM/585", "MB/185", "L-551", "TH-132", "0135T")
C552 = conv("DM/584", "MB/184", "L-552", "TH-133", "0134T")
C562 = conv("DFW/958", "FD/58", "L-562", "TH-258", "0822T")
C410 = conv("DFW/410", "MP/410", "L-410", "TH-410", "0546T-141")
C411 = conv("DFW/411", "MP411", "L-411", "TH411", "0549T-141")
AVW17 = "Volkswagen Caminhões 17.230 OD 4.6 L 16V DOHC L4 (2012 - 2026) / 17.260 OD (2014)"

# pág. 33 — tabela "SAPATA FREIO" (marca Momag no topo da página); duas linhas aparecem repetidas no catálogo
_P33 = [
    ("8780410", "S-640", "SAPATA L-410"), ("8780411", "S-641", "SAPATA L-411"), ("8780236", "S-236A", "SAPATA L-157A"),
    ("8780237", "S-237A", "SAPATA L-224"), ("8780213", "S213", "SAPATA L-227"), ("8780219", "S244", "SAPATA L-219"),
    ("8780240", "S-240", "SAPATA L-551"), ("8780623", "S-623", "SAPATA L-559"), ("8780223", "S-223A", "SAPATA L-636"),
    ("8780281", "S-281A", "SAPATA L-637"), ("8780217", "S-217A", "SAPATA L-638"),
    ("8780291", "S-291", "SAPATA S-291 SCANIA TRAS SV-231"), ("8780299", "S-299", "SAPATA S-299 SCANIA DIANT SV-230"),
    ("8780273", "S-273A", "SAPATA VV-303 VOLVO PRIMARIA DIANTEIRA"), ("8782730", "S-273B", "SAPATA VV-303 VOLVO SECUNDARIA DIANTEIRA"),
    ("8780274", "S-274A", "SAPATA VV-304 VOLVO PRIMARIA TRASEIRA"), ("8782740", "S-274B", "SAPATA VV-304 VOLVO SECUNDÁRIA TRASEIRA"),
    ("8780299", "S-299", "SAPATA S-299 SCANIA DIANT SV-230"), ("8780291", "S-291", "SAPATA S-291 SCANIA TRAS SV-231"),
]
AJ = {
    "33.1": {"marca": "Momag", "records": [dict(codigo=c, descricao=d, tipo="SAPATA FREIO", cod_ref=r,
                                                 info=("Linha repetida na tabela do catálogo" if i >= 17 else ""))
                                            for i, (c, r, d) in enumerate(_P33)]},
    # ---------------- pág. 34 ----------------
    "34.1": LONA("875636", "L636", C636, A636, M636, "Cobreq"),
    "34.2": LONA("872636", "L636", C636, A636, M636, "Thermoid"),
    "34.3": LONA("873636", "L636", C636, A636, M636, "Frum"),
    "34.4": SAP("8780223", "SAPATA L636", "S-223A", "Ca33 / CA/33 - AF-600 / 251100370",
                "Carreta - freio Q. Plus Guerra 95... / Randon 99...", "Guerra, Randon", "Sapata do freio 8\" s/rolete L-636"),
    "34.5": LONA("875637", "L637", C637, "Charger, Guerra", "Guerra", "Cobreq", "Posição: traseira | Guerra moderno roda alumínio"),
    "34.6": LONA("872637", "L637", C637, "Charger, Guerra", "Guerra", "Thermoid", "Posição: traseira | Guerra moderno roda alumínio"),
    "34.8": SAP("8780281", "SAPATA L637", "S-281A", "FD/81 (Fras-le FD-81)", "Sapata carreta Guerra 98/... s/rolete", "Guerra"),
    "34.9": LONA("875638", "L638", C638, A638, M638, ""),
    "34.10": LONA("872638", "L638", C638, A638, M638, "Thermoid"),
    "34.11": LONA("873638", "L638", C638, A638, M638, "Frum"),
    "34.12": SAP("8780217", "SAPATA L638", "S-217A", "Ca32 / Fras-le CA-32 / 251.100.0105 / T\" A-3222 / K-1831",
                 "Master carreta (89...) / Caminhão Iveco Eurotech e Stralis", "Iveco", "Sapata do freio 8\" s/rolete L-638"),
    "34.13": LONA("875219", "L219", C219, "Agrale, Ford, Marcopolo, Mercedes-Benz, Volkswagen",
                  "Volkswagen, Mercedes-Benz, Agrale", "", "Posição: dianteira / traseira"),
    "34.14": LONA("872219", "L-219", C219, "7000 STD Caminhão LT 4.3 8V MWM 4.10 Série 10 TCA Diesel (1993 - 2002)",
                  "Volkswagen, Mercedes-Benz, Agrale", "Thermoid"),
    "34.16": SAP("8780219", "SAPATA L-219", "S-244 / VW 2RD.607455", "Compatível com a lona L219 (Lonaflex)",
                 "VW dianteira/traseira 7.100 até 8.140 / Agrale caminhões e ônibus 7-8 ton / Mercedes-Benz ônibus MBB LO 712/812 MO, caminhão MBB 710 Plus / Ford caminhões 8 ton",
                 "Volkswagen, Mercedes-Benz, Agrale"),
    # ---------------- pág. 35 ----------------
    "35.1": LONA("875733", "L733", C733, "Volvo", "Volvo", "Cobreq", "Posição: dianteira"),
    "35.2": LONA("872733", "L-733", C733, "Volvo FH 460 ano inicial 2003, ano final 2023", "Volvo", "Thermoid",
                 "Medidas: comprimento da lona por pedaço 175mm | largura por pedaço 182mm | espessura por peça 18mm / 12,4mm"),
    "35.3": {"marca": "Momag", "montadora": "Volvo", "records": [
        dict(codigo="8780273", descricao="SAPATAS 733 VV303 VOLVO PRIMARIA DIANTEIRA", tipo="SAPATA FREIO", cod_ref="VV303",
             aplicacao="Volvo NH 12 (99/...) / FH 12 Globetrotter (98/...) / FM 12"),
        dict(codigo="8782730", descricao="SAPATA L733 VV303 SECUNDARIA DIANTEIRA", tipo="SAPATA FREIO", cod_ref="VV303",
             aplicacao="Volvo NH 12 (99/...) / FH 12 Globetrotter (98/...) / FM 12")]},
    "35.4": LONA("875734", "L734", C734, "Volvo", "Volvo", "Cobreq", "Posição: traseira"),
    "35.6": {"marca": "Momag", "montadora": "Volvo", "records": [
        dict(codigo="8780274", descricao="SAPATA -734 VV304 VOLVO PRIMARIA TRASEIRA", tipo="SAPATA FREIO", cod_ref="VV304",
             aplicacao="Volvo NH 12 (99/...) / FH 12 Globetrotter (98/...) / FM 12"),
        dict(codigo="8782740", descricao="SAPATA -734 VV304 VOLVO SECUNDÁRIA TRASEIRA", tipo="SAPATA FREIO", cod_ref="VV304",
             aplicacao="Volvo NH 12 (99/...) / FH 12 Globetrotter (98/...) / FM 12")]},
    "35.7": LONA("875223", "L223", C223, "Agrale, Ford, Iveco, Volkswagen, Volvo", "Agrale, Ford, Iveco, Volkswagen, Volvo", "Cobreq",
                 "Posição: dianteira / traseira"),
    "35.8": LONA("872223", "L223", C223, "Agrale, Ford, Iveco, Volkswagen, Volvo", "Agrale, Ford, Iveco, Volkswagen, Volvo", "Thermoid",
                 "Posição: dianteira / traseira"),
    "35.9": SAP("8780614", "SAPATA L-223", "S-614A", "Sistema Master FD/87",
                "Ford - Ford Cargo (98...) F12.000 / C1215 / 1615 / 1618 / 1630 / C1722 2422 / 4030 / 3224 1680 / Volks (...90) freios a ar 11.140 / 12.140 / Ônibus - dianteiro / 180C",
                "Ford, Volkswagen", "Sapata de freio traseiro a ar 6\" MA (15\" x 6\") s/rolete", ""),
    "35.10": LONA("875224", "L224", C224, "Agrale, Ford, Guerra, Iveco, Randon, Volkswagen", "Agrale, Ford, Iveco, Volkswagen, Volvo",
                  "Cobreq", "Posição: dianteira / traseira"),
    "35.11": LONA("872224", "L224", C224, "Agrale, Ford, Guerra, Iveco, Randon, Volkswagen", "Agrale, Ford, Iveco, Volkswagen, Volvo",
                  "Thermoid", "Posição: dianteira / traseira"),
    "35.12": SAP("8780237", "SAPATA L-224", "S-237A", "FD - 88",
                 "VW Cam. 14.150 / 14.170-BT / 220 / 24.250 35.300 / 35.300 CL (T) / Ônib. 16.180 CO (T) - 16.210 CD (D) / Ford Cam. F-14.000 C-1415 / C-1422 (T) C-1416 (T/3) C-1617 / C-1618 / C-1622 / C-1722",
                 "Volkswagen, Ford", "Sapata freio traseiro a ar 7\" s/rolete", ""),
    # ---------------- pág. 36 ----------------
    "36.1": LONA("875227", "L227", C227, "MAN, Mercedes-Benz", "MAN, Mercedes-Benz", "", "Posição: traseira"),
    "36.2": LONA("872227", "L227", C227, "MAN, Mercedes-Benz", "MAN, Mercedes-Benz", "Thermoid", "Posição: traseira"),
    "36.3": SAP("8780213", "SAPATA L227", "S-213 / 620.420.0519", "Fras-le MB 188",
                "2038 97/98 importado - 2240 97/98 importado - OF-1618 92 - OH-1635 L 9 (93...)", "Mercedes-Benz",
                "Sapata do freio traseiro c/rolete 220mm", ""),
    "36.4": LONA("875559", "L559", C559, A559, "Agrale", "", "Posição: dianteira / traseira"),
    "36.5": LONA("872559", "L559", C559, A559, "Agrale", "Thermoid", "Posição: dianteira / traseira"),
    "36.6": SAP("8780623", "SAPATA L-559", "S-623 / FM113 3222FM109", "Lona Fras-le FD/59 / Lona Flex L-559 / MB-193",
                "MB 912/914 (98...) 0909 / VW 11.140 91/93, 12.140 90/91, 12.140 91/96, 12.140 H 91, 12.170 BT 97",
                "Mercedes-Benz, Volkswagen", "Sapata de freio a ar traseira", ""),
    "36.7": LONA("8751059", "L1059", C1059, A1059, "Agrale", "", "Posição: dianteira / traseira"),
    "36.8": LONA("8721059", "L1059", C1059, A1059, "Agrale", "Thermoid", "Posição: dianteira / traseira"),
    "36.10": LONA("875640", "L-640", C640, "Volkswagen", "Guerra, Iveco, Ford, Volkswagen", "", "REF ORIG: 2T0698075"),
    "36.11": LONA("872640", "L-640", C640, "Volkswagen", "Guerra, Iveco, Ford, Volkswagen", "Thermoid", "REF ORIG: 2T0698075"),
    "36.12": LONA("873640", "L640", conv("DFW/910", "4710", "L-640", "TH191", "4710T-140C"), "Volkswagen",
                  "Guerra, Iveco, Ford, Volkswagen", "Frum"),
    # ---------------- pág. 37 ----------------
    "37.1": LONA("875309", "L309", C309, "Scania", "Scania", "Cobreq", "Posição: dianteira / traseira"),
    "37.2": LONA("872309", "L309", C309, "Scania", "Scania", "Thermoid", "Posição: dianteira / traseira"),
    "37.3": SAP("8780299", "SAPATA S-299 SCANIA DIANT SV-230", "1.300.204", "", "L-94 IB - L-94 UB (00...) / P-93 (95...) / P-94 4x2 - P-94 6x2",
                "Scania", "", ""),
    "37.5": LONA("875310", "L310", C310, "Scania", "Scania", "Cobreq", "Posição: traseira"),
    "37.6": SAP("8780291", "SAPATA S-291 SCANIA TRAS SV-231", "1.300.205 (novo) / 1.104.545 (antigo)", "",
                "L-94 IB - L-94 UB (00...)", "Scania", "", ""),
    "37.7": LONA("875551", "L551", C551, "MAN, Mercedes-Benz", "", "Cobreq", "Posição: dianteira / traseira"),
    "37.9": SAP("8780240", "SAPATA L-551", "S-240", "", "OF 1318 (p/ eixo 743099) / Chassi argentino LS", "Mercedes-Benz",
                "Sap. freio ar Ts. 3º eixo (180mm)"),
    "37.10": LONA("875552", "L552", C552, "Mercedes-Benz", "Mercedes-Benz", "Cobreq", "Posição: dianteira / traseira"),
    "37.11": LONA("872552", "L552", C552, "Mercedes-Benz", "Mercedes-Benz", "Thermoid", "Posição: dianteira / traseira"),
    "37.12": SAP("8780214", "SAPATA L-552", "S-214", "", "Dianteira L/LS 1924 - 1924A - 1929 - 2624 LS 1930 - 1932", "Mercedes-Benz",
                 "Sapata do freio MB c/rolete"),
    # ---------------- pág. 38 ----------------
    "38.1": LONA("875258", "L562", C562, "Ford / Volkswagen", "Volkswagen, Ford", ""),
    "38.2": LONA("872258", "L562", C562, "Ford / Volkswagen / Lona de freio Ford Cargo C-815E / VW 7110 / 8120 / 8150 - dianteira / traseira - TH 258",
                 "Volkswagen, Ford", "Thermoid"),
    "38.4": LONA("875157", "L157", conv("4515-C", "4515-C", "L-157-A", "TH-4515", "4515T"),
                 "Contin, Cummins, Engesa-FNV (Fruehauf), Fiat, FNM (Alfa Romeo), Golive, Guerra, Iderol, Metalpi, Pastre, Recrusul, Schiffer",
                 "", "", "Posição: traseira"),
    "38.6": SAP("8780236", "SAPATA L-157A", "S-236A / 251100015.6", "Fras-le 4515-C / 4515-G",
                "Truck e carreta - freio Master (89...)", "", "Sapata freio traseiro a ar 7\" s/rolete"),
    "38.7": LONA("8751570", "L1570", conv("4515-G", "4515-G", "L-157-0", "TH-151", "4515FC"), "Ford, Golive, Guerra, Krone",
                 "", "", "Posição: traseira"),
    "38.10": LONA("875111", "L111", conv("", "MB200", "L-111", "TH135", "9466T-140"),
                  "Lona STD freio traseiro MB Novo Actros (2020...)", "Mercedes-Benz", "", "Logo Actros"),
    # ---------------- pág. 39 ----------------
    "39.1": LONA("8752410", "L410", C410, AVW17, "Volkswagen", ""),
    "39.4": LONA("875411", "L411", C411, AVW17, "Volkswagen", ""),
}

NOTAS = [
    "p35 card 5: card só com logos Thermoid e Volvo (lona L734 Thermoid), sem código interno impresso.",
    "p36 card 13: Sapata de freio S-625A (Nº original 2TJ607525, aplicação VW 11.140 91/93, 12.140 90/91, 12.140 91/96, 12.140 H 91, 12.170 BT 97, s/rolete, lona Fras-le 4710) — sem código interno impresso.",
    "p37 cards 4 e 8: cards só com o logo Thermoid (posição das lonas L309/L551 Thermoid), sem código interno.",
    "p38 card 3: Sapata de freio S-611 (Nº original FM110 3222FM108, aplicação caminhão VW 7-110 / 8-120 / 8-150 / 9-150 (2003...), lona Fras-le FD/58, Lona Flex L-562) — sem código interno impresso.",
    "p38 cards 5, 8 e 11: cards só com o logo Thermoid, sem código interno.",
    "p34 cards 9 e 13, p36 cards 1, 4, 7, 10, p38 cards 1, 4, 7, 10, p39: lonas 875xxx sem logo de marca visível (as demais 875xxx exibem Cobreq).",
]
ADD = []
