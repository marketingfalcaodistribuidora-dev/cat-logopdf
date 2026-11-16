# Capítulo 16 - Mangueiras e Conexões (págs. 191-202)
TIPOS = [(r"CHICOTE", "CHICOTE ELÉTRICO"), (r"TOMADA", "TOMADA ELÉTRICA"), (r"ESPIRAL|MANGUEIRA ESP", "MANGUEIRA ESPIRAL"),
         (r"ENGATE|PINO ENGATE", "ENGATE RÁPIDO"), (r"JUNTA UNIVERSAL", "JUNTA UNIVERSAL"), (r"MANGUEIRA|MANG", "MANGUEIRA"),
         (r"CONEX|CONECTOR|NIPLE|UNI[AÃ]O|COTOVELO|ESPIG", "CONEXÃO"), (r"TUBO", "TUBO")]
GRADES = {193: {"cells": [[25, 88, 570, 350], [25, 350, 570, 600], [25, 600, 286, 805], [286, 600, 570, 805]], "fonte": 9}}
AJ = {
    "cod:7720009": {"descricao": "CHICOTE ELETRICO 7 VIAS 5,5MT", "info": ""},
    "cod:7726500": {"descricao": "CHICOTE ELETRICO 7 FIOS 6,5MT", "info": ""},
    "cod:7722600": {"info": "Chicote elétrico para geladeira de caminhão | Fabricado com tubo de poliamida (PA6) e 2 fios revestidos nas bitolas de 4 ou 6 mm²"},
    "cod:5591312": {"descricao": "TOMADA ELETRICA MACHO", "marca": "DNI"},
    "cod:7711561": {"descricao": "TOMADA ELETRICA PLASTICA CONJUNTO", "marca": "DNI"},
    "cod:5591313": {"descricao": "TOMADA ELETRICA FEMEA", "marca": "DNI"},
    "cod:5590588": {"info": "Quantidade de pinos 7p | À prova d'água: sim | Material de contato: cobre | Material: alumínio | Tensão 24 V"},
    "cod:5590589": {"info": "Quantidade de pinos 7p | À prova d'água: sim | Material de contato: cobre | Material: alumínio | Tensão 24 V"},
    "cod:7727100": {"info": "Chicote 7 vias para ligação elétrica do freio ABS | Tamanho 5,5 metros"},
    "cod:7721265": {"info": "15 vias / 7 vias"},
    "192.1": {"_titulo": "MANGUEIRA ESPIRAL UNIVERSAL COM ADAPTADOR"},
    "cod:7720206": {"montadora": "Scania"}, "cod:7700001": {"montadora": "Iveco", "info": "Foto ilustrativa"},
    "cod:7700003": {"montadora": "Volvo", "info": "Foto ilustrativa"}, "cod:7700002": {"montadora": "Scania", "info": "Foto ilustrativa"},
    "cod:5500816": {"marca": "Stahl", "montadora": "Mercedes-Benz, Volvo"}, "cod:5500807": {"marca": "Stahl", "montadora": "Volkswagen"},
}
_BI1 = "MANGUEIRA ESPIRAL BITREM 6,5 MTS ROSCA 16M X PORCA 16M"
_BI2 = "MANGUEIRA ESPIRAL BITREM 6,5 MTS ROSCA 16M X ROSCA 16M"
for _c in ("7701632", "7701633", "7701634", "7701635"):
    AJ["cod:" + _c] = {"_titulo": _BI1, "_nao_agrupar": False, "montadora": "Randon, Guerra"}
for _c in ("7701636", "7701637", "7701638", "7701639"):
    AJ["cod:" + _c] = {"_titulo": _BI2, "_nao_agrupar": False, "montadora": "Randon, Guerra"}
AJ["cod:7706500"] = {"descricao": "MANGUEIRA ESP M16 X M16 6,5 MTS FINA MODERNA PRETA", "info": ""}
AJ["cod:7720205"] = {"descricao": "MANGUEIRA ESPIRAL 5,5 TITAN VW", "montadora": "Volkswagen", "info": ""}
ADD = []
NOTAS = []

# ---- pág. 194
AJ["cod:7720206"] = {"descricao": "MANGUEIRA ESPIRAL 5,5 SCANIA S4", "tipo": "MANGUEIRA ESPIRAL", "montadora": "Scania"}
AJ["cod:7720205"]["tipo"] = "MANGUEIRA ESPIRAL"

# ---- pág. 195 (grade de molduras; códigos 7720001/03/04/05/07/08 impressos em cor, não em vermelho)
MANUAIS = {195}
_R195 = [85, 189, 301, 417, 523, 619, 805]
def _cel(lin, col):
    xs = [(20, 298), (298, 575)][col] if col is not None else (20, 575)
    return [xs[0], _R195[lin], xs[1], _R195[lin + 1]]
_NOTA_COR = "No card consta só o código e a cor; descrição complementada pela foto (mangueira espiral com bico de limpeza)"
for _i, (_c, _d, _l, _col, _inf) in enumerate([
        ("7720002", "MANGUEIRA ESPIRAL COM BICO VERMELHA", 0, 0, _NOTA_COR),
        ("7720003", "MANGUEIRA ESPIRAL COM BICO AZUL", 0, 1, _NOTA_COR),
        ("7720004", "MANGUEIRA ESPIRAL COM BICO CINZA", 1, 0, _NOTA_COR),
        ("7720001", "MANGUEIRA ESPIRAL COM BICO PRETA", 1, 1, _NOTA_COR),
        ("7720006", "MANG LIMPEZA CABINE VERMELHA SIMPL", 2, 0, ""),
        ("7720005", "MANG LIMPEZA CABINE AZUL SIMPL", 2, 1, ""),
        ("7720008", "MANG LIMPEZA CABINE CINZA SIMPL", 3, 0, ""),
        ("7720007", "MANG LIMPEZA CABINE PRETA SIMPL", 3, 1, ""),
        ("7729026", "BICO MANGUEIRA LIMPEZA CABINE", 4, 0, ""),
        ("7001005", "ABRACADEIRA PARA MANGUEIRA RODO AR", 4, 1, "")]):
    _t = "BICO DE LIMPEZA" if _c == "7729026" else "ABRAÇADEIRA" if _c == "7001005" else "MANGUEIRA ESPIRAL"
    ADD.append(dict(pagina=195, card=_i + 1, codigo=_c, descricao=_d, tipo=_t, faixa=_cel(_l, _col)))
    AJ["cod:" + _c] = {"info": _inf}
for _c, _m in (("7725550", "05"), ("7725670", "07"), ("7725710", "10"), ("7725815", "15")):
    ADD.append(dict(pagina=195, card=11, codigo=_c, descricao=f"MANG ESP PINTURA {_m} METROS 10 X 07", tipo="MANGUEIRA ESPIRAL",
                    _titulo="MANGUEIRA ESPIRAL PARA PINTURA 10 X 07", faixa=_cel(5, None)))
    AJ["cod:" + _c] = {"info": "LANÇAMENTO"}

# ---- págs. 196-197: mesmas tabelas de mangueira nas duas páginas (registradas nas duas -> mescladas "196, 197").
# Descrições da Mangueira Lonada, 7749787 e Emenda T (8001771-74) estão dentro da imagem.
MANUAIS |= {196, 197}
_INJ = ("MANGUEIRA INJEÇÃO ELETRONICA", [("7741415", "MANGUEIRA INJ ELETRONICA 7X14"), ("7741280", "MANGUEIRA INJ ELETRONICA 8X15")])
_BOR = ("MANGUEIRA BOR. P/AR COMP. 300PSI", [
    ("7741152", "MANG.BOR.P/AR A 500PSI 1/4"), ("7741492", "MANG.BOR.P/AR B 500PSI 5/16"), ("7740466", "MANG.BOR.P/AR C 500PSI 3/8"),
    ("7741151", "MANG.BOR.P/AR D 500PSI 1/2"), ("7740058", "MANG.BOR.P/AR E 300PSI 5/8"), ("7740465", "MANG.BOR.P/AR F 300PSI 3/4"),
    ("7740078", "MANG.BOR.P/AR F 350PSI 7/8"), ("7744034", "MANG.BOR.P/AR G 300PSI 1\""), ("7740114", "MANG.BOR.P/AR I 300PSI 1.1/4"),
    ("7740112", "MANG.BOR.P/AR J 150PSI 1.1/2")])
_LON = ("MANGUEIRA LONADA", [
    ("7740967", "MANGUEIRA LONADA 03,0 X 7,0 1/8"), ("7741140", "MANGUEIRA LONADA 04,0 X 8,0 5/32"),
    ("7740966", "MANGUEIRA LONADA 05,0 X 9,5 3/16"), ("7740463", "MANGUEIRA LONADA 06,0 X 11,0 1/4"),
    ("7740849", "MANGUEIRA LONADA 08,0 X 13,0 5/16"), ("7740464", "MANGUEIRA LONADA 09,0 X 15,0 3/8"),
    ("7740850", "MANGUEIRA LONADA 12,0 X 18,0 1/2")])
_CRI = ("MANG CRISTAL TRANCADA", [("7741463", "MANG CRISTAL TRANCADA 1/2"), ("7741493", "MANG CRISTAL TRANCADA 1/4"),
                                  ("7741308", "MANG CRISTAL TRANCADA 3/8"), ("7741307", "MANG CRISTAL TRANCADA 5/16"),
                                  ("7741458", "MANG CRISTAL TRANCADA 5/8")])
_TRA = ("MANGUEIRA TRANSPARENTE (ENCAPAR MOLA / COMBUSTÍVEL)", [
    ("7741012", "MANG ENCAPAR MOLA 1/2 TRANSP"), ("7741014", "MANG COMBUSTIVEL 1/4 X 2 TRANSP"),
    ("7741839", "MANG COMBUSTIVEL 5 X 2,5 TRANSP")])
_GAS1 = ("", [("7740466", "MANG.BOR.P/AR C 500PSI 3/8 GAS")])
_GAS2 = ("", [("7749787", "MANG.CRISTAL TRANCADA 3/8 GAS")])
def _grupo(pag, card, faixa, grupo, tipo="MANGUEIRA"):
    tit, itens = grupo
    for c, d in itens:
        r = dict(pagina=pag, card=card, codigo=c, descricao=d, tipo=tipo, faixa=faixa, fonte_titulo=1)
        if tit:
            r["_titulo"] = tit
        else:
            r["_nao_agrupar"] = True
        ADD.append(r)
_X = (25, 570)
for _card, (_y0, _y1), _g in [(1, (85, 186), _INJ), (2, (186, 337), _BOR), (3, (337, 474), _LON), (4, (474, 589), _CRI),
                              (5, (589, 679), _TRA), (6, (679, 733), _GAS1), (7, (733, 805), _GAS2)]:
    _grupo(196, _card, [_X[0], _y0, _X[1], _y1], _g)
for _card, (_y0, _y1), _g in [(1, (85, 232), _BOR), (2, (232, 358), _LON), (3, (358, 428), _INJ), (4, (428, 472), _GAS2),
                              (5, (472, 586), _TRA), (6, (472, 586), _CRI)]:
    _grupo(197, _card, [_X[0], _y0, _X[1], _y1], _g)
# 7740466 aparece 2x: na tabela Mangueira Bor. e num card próprio "GAS" -> o card avulso vira registro com sufixo na nota
for _i, (_c, _m, _x0, _x1) in enumerate([("8001771", "1/4", 20, 160), ("8001772", "5/16", 160, 295),
                                         ("8001773", "3/8", 295, 431), ("8001774", "1/2", 431, 571)]):
    ADD.append(dict(pagina=197, card=7 + _i, codigo=_c, descricao=f"EMENDA T LATAO {_m}", tipo="CONEXÃO",
                    faixa=[_x0, 682, _x1, 805], fonte_titulo=1))
NOTAS.append("Págs. 196-197: as tabelas de mangueira (Injeção Eletrônica, Bor. P/AR Comp., Lonada, Cristal Trançada, Transparente) "
             "aparecem nas duas páginas e foram mescladas; 7741458 (Cristal Trançada 5/8) só aparece na pág. 197.")
NOTAS.append("Pág. 196: o código 7740466 aparece na tabela de Mangueira Bor. P/AR (500PSI 3/8) e num card próprio como "
             "'MANG.BOR.P/AR C 500PSI 3/8 GAS'.")

# ---- págs. 198-199 (molduras sobrepostas; descrições do tubo sem trama estão na imagem)
MANUAIS |= {198, 199}
_grupo(198, 1, [25, 85, 570, 358], ("TUBO NYLON / MANGUEIRAS COM TRAMA", [
    ("7720710", "TUBO L NYLON C/TRAMA 107"), ("7720711", "TUBO M NYLON C/TRAMA 12X9"), ("7720712", "TUBO N NYLON C/TRAMA 3/8"),
    ("7720713", "TUBO O NYLON C/TRAMA 1/2"), ("7721200", "TUBO P NYLON C/TRAMA 5/8")]), tipo="TUBO NYLON")
_grupo(198, 2, [20, 358, 300, 610], ("", [("7720703", "MANGUEIRA RODO AR PRETA")]))
_grupo(198, 3, [300, 358, 575, 610], ("", [("7720313", "MANGUEIRA RODO AR AZUL PU 8X16")]))
_grupo(198, 4, [20, 610, 575, 805], ("", [("7741260", "MANG.BOR. PNEUMATICA AZUL REFORCADA 1/2")]))
_grupo(198, 5, [26, 228, 150, 340], ("", [("9010", "CORTADOR TUBO NYLON")]), tipo="FERRAMENTA")
_grupo(199, 1, [25, 85, 570, 463], ("TUBO NYLON / MANGUEIRAS SEM TRAMA", [
    ("7721203", "TUBO NYLON S/TRAMA 1/8X1"), ("7721202", "TUBO A NYLON S/TRAMA 3/16"), ("7720706", "TUBO B NYLON S/TRAMA 1/4"),
    ("7720707", "TUBO C NYLON S/TRAMA 5/16"), ("7720708", "TUBO D NYLON S/TRAMA 3/8"), ("7720709", "TUBO E NYLON S/TRAMA 1/2"),
    ("7721201", "TUBO F NYLON S/TRAMA 4 X 2"), ("7720702", "TUBO G NYLON S/TRAMA 6 X 4"), ("7720704", "TUBO I NYLON S/TRAMA 10 X 8"),
    ("7721204", "TUBO I NYLON S/TRAMA 11 OU 7/16"), ("7720705", "TUBO J NYLON S/TRAMA 12 X 9"), ("7721300", "TUBO NYLON S/TRAMA 13 X 10"),
    ("7721400", "TUBO L NYLON S/TRAMA 14 X 11"), ("7720015", "TUBO NYLON S/TRAMA 15 X 11"), ("7721600", "TUBO L NYLON S/TRAMA 16 X 12"),
    ("7721814", "TUBO NYLON S/TRAMA 18 X 14")]), tipo="TUBO NYLON")
_grupo(199, 2, [35, 320, 176, 447], ("", [("9010", "CORTADOR TUBO NYLON")]), tipo="FERRAMENTA")
_grupo(199, 3, [25, 463, 570, 542], ("", [("8010618", "CONECTOR MACHO BOLSA AR 06X1/8")]), tipo="CONEXÃO")
_grupo(199, 4, [25, 542, 570, 668], ("MANGUEIRA PARA BUZINA", [
    ("7720014", "TUBO B NYLON SILICONADA AZUL 1/4"), ("7726000", "TUBO G NYLON SILICONADA AZUL 6 X 4")]), tipo="TUBO NYLON")
_grupo(199, 5, [25, 668, 570, 805], ("TUBO NYLON / MANGUEIRAS SILICONADO AZUL", [
    ("7720430", "TUBO N.SIL.PAINEL R.AR 4,30M"), ("7721000", "TUBO NYLON SILICO AZUL 10X7MM"),
    ("7720012", "TUBO NYLON SILICO AZUL 12X8MM"), ("7720953", "TUBO NYLON SILICO AZUL 3/8"),
    ("7721270", "TUBO NYLON SILICO AZUL 1/2")]), tipo="TUBO NYLON")
for _c in ("7720430", "7721000", "7720012", "7720953", "7721270"):
    AJ["cod:" + _c] = {"info": "NOVO"}
NOTAS.append("Págs. 198-199: o cortador de tubo nylon tem código de 4 dígitos (9010) e aparece nas duas páginas (mesclado).")

# ---- págs. 200-202 (mangueira HD, terminais e emendas hidráulicas)
TIPOS[:0] = [(r"TERMINAL", "TERMINAL HIDRÁULICO"), (r"EMENDA", "EMENDA PARA MANGUEIRA"), (r"COTOVELO", "CONEXÃO"),
             (r"CAPA", "CAPA DE MANGUEIRA")]
AJ["200.1"] = {"_titulo": "MANGUEIRA HD TRAMA AÇO 1 TRAMA E 2 TRAMAS", "info": "", "tipo": "MANGUEIRA HIDRÁULICA"}
AJ["cod:7755016"] = {"descricao": "ENGATE RAPIDO HIDRAULICO COMPLETO ROSCA FEMEA 1.1/4", "tipo": "ENGATE RÁPIDO",
                     "info": "Rosca 1.1/4 ou 31,75MM | Fotos do engate montado e desmontado"}
AJ["200.3"] = {"_nao_agrupar": True}
AJ["cod:7751004"] = {"descricao": "MANGUEIRA HIDROLAVADORA 1/4\"", "tipo": "MANGUEIRA",
                     "info": "STRONG MAX | 2400PSI/165BAR | MAX +60ºC(140ºF)"}
AJ["cod:7751104"] = {"descricao": "CAPA P/MANGUEIRA HIDROLAVADORA 1/4\"", "tipo": "CAPA DE MANGUEIRA", "info": ""}
AJ["200.4"] = {"_titulo": "MANGUEIRA TEFLON SAE 100-R14", "tipo": "MANGUEIRA HIDRÁULICA"}
AJ["200.5"] = {"_titulo": "CAPA MANGUEIRA HD TRAMA AÇO", "tipo": "CAPA DE MANGUEIRA"}
for _c, _d, _i in [
        ("7751221", "HD TERMINAL RETO TUBO 15MM X MACHO 22MM FIXO", "Bico 13MM | Rosca macho 22MM"),
        ("7755826", "HD TERMINAL RETO TUBO 18MM X MACHO 26MM FIXO", "Bico 16,2MM | Rosca macho 26MM"),
        ("77511516", "HD TERMINAL RETO TUBO B 1\" X MACHO 1.5 X 16\"", "Bico 1\" ou 25,4 MM | Rosca macho 34 MM | G1\""),
        ("7751214", "HD TERMINAL RETO TUBO 06MM X FEMEA 12MM GIRA", "Bico 6,5MM | Rosca fêmea 12MM"),
        ("7751414", "HD TERMINAL RETO TUBO 06MM X FEMEA 14MM GIRA", "Bico 6,5MM | Rosca fêmea 14MM"),
        ("7753818", "HD TERMINAL RETO TUBO 12MM X FEMEA 18MM GIRA", "Bico 6,5MM (como impresso) | Rosca fêmea 18MM"),
        ("7751222", "HD TERMINAL RETO TUBO 15MM X FEMEA 22MM GIRA", "Bico 13MM | Rosca fêmea 22MM"),
        ("7751412", "HD TERMINAL CURVO TUBO 06MM X FEMEA 12MM GIRA", "Bico 6,5MM | 22MM macho fêmea (como impresso)"),
        ("7751218", "HD TERMINAL CURVO TUBO 12MM X FEMEA 18MM GIRA", "Bico 10MM | 18MM macho fêmea"),
        ("7751522", "HD TERMINAL CURVO TUBO 15MM X FEMEA 22MM GIRA", "Bico 13MM | 22MM macho fêmea"),
        ("7751826", "HD TERMINAL CURVO TUBO 18MM X FEMEA 26MM GIRA", "Bico 16,5MM | 26MM macho fêmea"),
        ("7751401", "HD EMENDA P/MANGUEIRA TRAMA ACO A 1/4", "1/4"),
        ("7755161", "HD EMENDA P/MANGUEIRA TRAMA ACO B 5/16", "5/16"),
        ("7753801", "HD EMENDA P/MANGUEIRA TRAMA ACO C 3/8", "3/8"),
        ("7751201", "HD EMENDA P/MANGUEIRA TRAMA ACO D 1/2", "1/2"),
        ("7755801", "HD EMENDA P/MANGUEIRA TRAMA ACO E 5/8", "5/8"),
        ("7753401", "HD EMENDA P/MANGUEIRA TRAMA ACO F 3/4", "3/4"),
        ("7750101", "HD EMENDA P/MANGUEIRA TRAMA ACO G 1\"", "1\" ou 25,4 MM"),
        ("7753413", "HD TERMINAL RETO TUBO A 1/2 X FEMEA 3/4 GIRA", "Tubo 1/2 | Rosca fêmea 3/4"),
        ("7757858", "HD TERMINAL RETO TUBO B 5/8 X FEMEA 7/8 GIRA", "Tubo 5/8 | Rosca fêmea 7/8"),
        ("7757812", "HD TERMINAL RETO TUBO A 1/2 X FEMEA 7/8 GIRA", "Tubo 1/2 | Rosca fêmea 7/8"),
        ("7757834", "HD TERMINAL RETO TUBO C 3/4 X FEMEA 7/8 GIRA", "Tubo 3/4 | Rosca fêmea 7/8"),
        ("77511616", "HD TERMINAL RETO TUBO B 1\" X FEMEA 1.5 X 16\"", "Tubo 1.5/16 | Rosca fêmea 1\" (como impresso)"),
        ("7757835", "HD TERMINAL CURVO A TUBO 3/4 X FEMEA 7/8 GIRA", "Tubo 3/4 | Fêmea 7/8"),
        ("7753412", "HD TERMINAL CURVO A TUBO 1/2 X FEMEA 3/4 GIRA", "Tubo 1/2 | Fêmea 3/4"),
        ("7757854", "HD TERMINAL CURVO A TUBO 5/8 X FEMEA 7/8 GIRA", "Tubo 5/8 | Fêmea 7/8"),
        ("7751278", "HD TERMINAL CURVO A TUBO 1/2 X FEMEA 7/8 GIRA", "Tubo 1/2 | Fêmea 7/8"),
        ("7751516", "HD TERMINAL CURVO A TUBO 1\" X FEMEA 1.5 X 16\"", "Tubo 1\" | Fêmea 1.5/16"),
        ("775716916", "HD COTOVELO P/MANGUEIRA 7/16 X 9/16", "7/16 ou 11,11 rosca macho | 9/16 ou 14,28 rosca macho")]:
    _t = ("TERMINAL HIDRÁULICO" if "TERMINAL" in _d else "EMENDA PARA MANGUEIRA" if "EMENDA" in _d else "CONEXÃO")
    AJ["cod:" + _c] = {"descricao": _d, "info": _i, "tipo": _t}
NOTAS.append("Págs. 200-202: alguns códigos internos têm 8-9 dígitos como impressos (77511516, 77511616, 775716916).")

# ---- pág. 192: tipo/informação do card e pontos soltos antes de duas descrições
AJ["192.1"].update({"tipo": "MANGUEIRA ESPIRAL", "info": ""})
AJ["cod:7701604"] = {"descricao": "MANGUEIRA ESPIRAL 5,5 PRETO"}
AJ["cod:7705503"] = {"descricao": "MANGUEIRA ESPIRAL 5,5 VERMELHA"}

# ---- fotos recortadas à mão
AJ["cod:7751004"]["foto_spec"] = {"rect": [262, 290, 446, 440]}
AJ["cod:7751104"]["foto_spec"] = {"rect": [448, 296, 568, 382]}
for _c in ("7720014", "7726000"):  # mangueira (e não a buzina)
    AJ["cod:" + _c] = {"foto_spec": {"rect": [38, 578, 168, 658]}}
