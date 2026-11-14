# Capítulo 13 - Válvulas (págs. 158-170) — grades definidas na revisão visual (molduras sobrepostas)
TIPOS = [(r"REPARO|REP\b|JOGO DE REPARO|QA-", "REPARO VÁLVULA"), (r"REGULADOR", "REGULADOR DE PRESSÃO"),
         (r"PUXADOR", "PUXADOR VÁLVULA"), (r"TESTE", "VÁLVULA DE TESTE"), (r"V[AÁ]LV|VALV", "VÁLVULA")]
GRADES = {
    158: {"rows": [88, 259, 445, 628, 805], "fonte": 12},
    159: {"cells": [[25, 88, 298, 267], [298, 88, 570, 267], [25, 267, 298, 446], [298, 267, 570, 446],
                    [25, 446, 298, 626], [298, 446, 570, 626], [25, 626, 208, 805], [208, 626, 394, 805], [394, 626, 570, 805],
                    ], "fonte": 9},
    160: {"rows": [88, 214, 351, 469, 580, 690, 805], "cols": [25, 298, 570], "fonte": 9},
}
MB = "Mercedes-Benz"
_INS = dict(pagina=159, tipo="REPARO VÁLVULA")
ADD = [
    dict(_INS, card=20, codigo="4001072", descricao="QA-1072 JOGO DE REPARO VÁLVULA RELÊ", marca="Quinelato",
         info="Reparo das válvulas relê 7773137, 7773116 e 7770000", foto_spec={"rect": [165, 150, 210, 216]}),
    dict(_INS, card=21, codigo="4001280", descricao="QA-1280C JOGO DE REPARO COMPLETO REGULADOR DE PRESSÃO", marca="Quinelato",
         info="Reparo do regulador de pressão 7770038", foto_spec={"rect": [167, 522, 230, 588]}),
    dict(pagina=159, card=22, codigo="8001397", descricao="TESTE VALVULA PRESSAO 16MM 1.5", tipo="VÁLVULA DE TESTE",
         info="Indicada nos reguladores de pressão 7770038 e 7770039", foto_spec={"rect": [120, 464, 184, 506]}),
]
AJ = {
    "cod:8790004": dict(descricao="VALVULA RELE DISTRIBUIDORA FREIO CARRETA RE01", info="16MM X 22MM"),
    "cod:8792741": dict(descricao="VALVULA RELE DISTRIBUIDORA FREIO CARRETA RE02", info="Antiga | 1/4 X 1/4 X 1/2 NPT"),
    "cod:8790316": dict(descricao="VALVULA MESTRA Re04 3 16MM X 122 MM", info="3 saídas | M16 X 1,5 mm"),
    "cod:8791149": dict(descricao="VALVULA MESTRA Re04 4-16MM X 1-22 MM", info="LANÇAMENTO | 4 saídas | M16 X 1,5 mm"),
    "cod:7773137": {"-info": r"- QA-1072 \| JOGO DE REPARO \| VÁLVULA RELÊ", "+info": "Jogo de reparo: 4001072 (QA-1072)",
                    "montadora": "Volkswagen, Ford, Scania, Mercedes-Benz"},
    "cod:7773116": {"-info": r"- QA-1072 \| JOGO DE REPARO \| VÁLVULA RELÊ", "+info": "Jogo de reparo: 4001072 (QA-1072)", "montadora": MB},
    "cod:7770000": {"-info": r"- QA-1072 \| JOGO DE REPARO \| VÁLVULA RELÊ", "+info": "Jogo de reparo: 4001072 (QA-1072)", "montadora": MB},
    "cod:7773138": {"montadora": MB},
    "cod:7770038": {"info": "Jogo de reparo: 4001280 (QA-1280C) | Teste válvula pressão: 8001397"},
    "cod:7770039": {"-variacoes": r" / REF SIMILAR: WABCO\( 975.300.110.0\) / REF LNG: 43-450",
                    "-info": r"TESTE VALVULA PRESSAO \| 16MM 1.5", "+info": "Teste válvula pressão: 8001397", "montadora": MB},
    "cod:5113280": dict(info="", variacoes="Wabco 4750103280 / Similares: 4750103280 / 2T2607262",
                        aplicacao="Válvula limitadora pressão VW ônibus / MAN TGX / MB / Scania série 3/4",
                        montadora="Volkswagen, MAN, Mercedes-Benz, Scania"),
    "cod:5113197": dict(info="16MM / 16MM"),
    "cod:4000925": dict(descricao="REP VALV 2 VIAS KNORR", cod_ref="", variacoes="", marca="Knorr", foto_spec={"rect": [488, 220, 560, 288]}),
    "cod:5110553": dict(descricao="VALVULA DUPLA RETENCAO M16 X 1,5", montadora="Mercedes-Benz, Agrale, Iveco",
                        foto_spec={"rect": [250, 218, 420, 300]}),
    "cod:5110302": dict(descricao="ST302 IMP VALVULA NIVE.CABINE MB AXOR/ACTROS", cod_ref="4640070110 / A0003284530",
                        info="LANÇAMENTO 03/2025", aplicacao="Válvula niveladora cabine / Compatível: MB Actros / Axor"),
    "cod:7771118": dict(descricao="VALVULA NIVELAMENTO CABINE SCANIA 113/143", tipo="VÁLVULA", info="", montadora="Scania"),
    "cod:5110170": dict(descricao="ST170 IMP VALVULA NIVE.CABINE CONSTE 2006", tipo="VÁLVULA", cod_ref="2T0616149",
                        info="LANÇAMENTO 03/2025", montadora="Volkswagen",
                        aplicacao="Válvula niveladora / Volkswagen Constellation 2006 em diante / Worker 2000 a 2019 suspensão pneumática do eixo / rosca M12 X 1,5"),
    "cod:7774018": {"montadora": "Mercedes-Benz, Volkswagen, Scania"},
    "cod:7774410": {"montadora": MB},
}
NOTAS = []
AJ["cod:8001397"] = dict(descricao="TESTE VALVULA PRESSAO 16MM 1.5", tipo="VÁLVULA DE TESTE", cod_ref="", variacoes="", aplicacao="",
                         info="Indicada nos reguladores de pressão 7770038 e 7770039", foto_spec={"rect": [120, 464, 184, 506]})
AJ["cod:5110553"]["tipo"] = "VÁLVULA"

# pág. 162-163
_BX = dict(marca="Brex")
_PAINEL = "Válvula de aplicação em painel"
AJ.update({
    "cod:5113213": {"info": "MB 1519/2219", "montadora": MB},
    "cod:5112899": {"cod_ref": "8152899"},
    "cod:5130011": dict(descricao="PAINEL MOVIMENTA PUSH/PULL MULT 03 VALVULAS", tipo="PAINEL DE VÁLVULAS", cod_ref="PA030011",
        variacoes="Reparos: RP040010 / RP250005 / RP010010 / RP020010",
        aplicacao="Randon / Noma / Guerra / Facchini e outros", montadora="Randon, Noma, Guerra, Facchini",
        info="3 válvulas | Roscas M16 x 1,5mm | Funções: válvula dupla retenção, proteção spring brake, filtro de linha com by pass, "
             "válvula de desfrenagem, válvula de estacionamento, acionamento do suspensor pneumático (opcional)"),
    "cod:513090012": dict(_BX, descricao="VALVULA BREX ACION M16 X 1,5 PT C/REG C/SAIDA", aplicacao=_PAINEL,
        info="Obs.: válvula de aplicação em painel (compõe o painel 2G, 3G e 4G) | Rosca M16 x 1,5mm (pórticos) | M12 x 1,5mm (montagem com outras válvulas do painel)"),
    "cod:513050014": dict(_BX, descricao="VALVULA BREX ACION M16 X 1,5 PT C/REG S/SAIDA", aplicacao=_PAINEL,
        info="M16 x 1,5mm (pórtico de saída) | M12 x 1,5mm (pórtico de entrada)"),
    "cod:51103012": dict(_BX, descricao="VALVULA BREX ACION M16 X 1,5 PT S/REG S/SAIDA", aplicacao=_PAINEL,
        info="Compõe o painel 2G, 3G e 4G | M16 x 1,5mm (pórticos) | M12 x 1,5mm (montagem com outras válvulas do painel)"),
    "cod:513280005": dict(_BX, descricao="VALVULA BREX ACION M16 X 1,5 PT SUSPENSOR", aplicacao=_PAINEL, info="M16 x 1,5mm", tipo="VÁLVULA"),
    "cod:513250005": dict(_BX, descricao="VALVULA BREX EXAUSTAO M16 X 1,5 PROT SPRING", aplicacao="", info="M16 x 1,5mm", tipo="VÁLVULA"),
    "cod:513260005": dict(_BX, descricao="VALVULA BREX NIVELADORA 12MM SEM FIM", aplicacao="", info="M12 x 1,5mm", tipo="VÁLVULA"),
    "cod:513060016": dict(_BX, descricao="VALVULA BREX REGULADORA PRESSAO 1/8", info="1/8\" BSP | Válvula reguladora de pressão com manômetro com glicerina", tipo="REGULADOR DE PRESSÃO"),
    "cod:513060022": dict(_BX, descricao="VALVULA BREX REGULADORA PRESSAO 1/4", info="1/4\" BSP | Válvula reguladora de pressão com manômetro com glicerina", tipo="REGULADOR DE PRESSÃO"),
    "cod:513320005": dict(_BX, descricao="VALVULA BREX PUSH PULL 16 X 1,5 AZUL", info="M16 x 1,5mm"),
    "cod:513370005": dict(_BX, descricao="VALVULA BREX PUSH PULL 16 X 1,5 VERM", info="M16 x 1,5mm"),
    "cod:5111183": dict(descricao="VALVULA IMPORTADA REGULADORA PRESSAO 1/4", tipo="REGULADOR DE PRESSÃO", cod_ref="384.421.5369",
        info="Rosca 1/4\" BSP | Válvula reguladora de pressão com manômetro com glicerina | Faixa de pressão 0 a 12 bar",
        aplicacao="Noma / Guerra / Librelato / Facchini", montadora="Noma, Guerra, Librelato, Facchini"),
    "cod:8005500": {"descricao": "VALVULA ACION PUSH PULL 16 X 1,5 AZUL"},
    "cod:8005600": {"descricao": "VALVULA ACION PUSH PULL 16 X 1,5 VERMELHA"},
    "cod:8005900": {"descricao": "VALVULA ACION PUSH PULL 16 X 1,5 AMARELO"},
    "cod:800401045": {"descricao": "VALVULA ACION PUSH PULL 16 X 1,5 PRETA"},
    "cod:5110031": {"montadora": "Scania, Mercedes-Benz", "info": "Scania todos / antigo"},
})
GRADES[164] = {"cells": [[25, 88, 240, 220], [240, 88, 570, 220], [25, 220, 240, 345], [240, 220, 570, 345],
                         [25, 345, 240, 455], [240, 345, 570, 455], [25, 455, 190, 625], [190, 455, 380, 625], [380, 455, 570, 625],
                         [25, 625, 298, 805], [298, 625, 570, 805]], "fonte": 9}
GRADES[165] = {"cells": [[25, 88, 298, 255], [298, 88, 570, 255], [25, 255, 298, 440], [298, 255, 570, 440],
                         [25, 440, 298, 625], [298, 440, 570, 625], [25, 625, 298, 805], [298, 625, 570, 805]], "fonte": 9}
V = "Volvo"
SC = "Scania"
AJ.update({
    "cod:7772863": dict(descricao="VALVULA RELE EMERGENGIA VOLVO TODOS", cod_ref="286370", variacoes="REF LNG: 43-119", info="", montadora=V),
    "cod:7771069": dict(descricao="VALVULA INIBIDORA CAIXA CAMBIO VOLVO FH12/ NH12", cod_ref="1069841", variacoes="REF LNG: 43-365", info="", montadora=V),
    "cod:7771669": dict(descricao="VALVULA CAIXA CAMBIO PONTO NEUTRO VOLVO FH12/ NH12", cod_ref="1669297", variacoes="REF LNG: 43-153",
                        info="Também em card da p.164: Valvula Volvo caixa cambio ponto neutro (ref. original 1669297)", montadora=V, tipo="VÁLVULA"),
    "cod:7777206": dict(descricao="VALVULA 2 VIAS CAMBIO", cod_ref="000.431.7206", variacoes="REF LNG: 43-258",
                        aplicacao="1519/1520/2219/2220 (1982/1985)", info="", montadora=MB),
    "cod:7772995": dict(descricao="VALVULA FILTRO LINHA TODOS 0370/0371", cod_ref="000.429.2995", variacoes="REF LNG: 43-194",
                        info="Rosca 22 X 1,5", montadora=MB),
    "cod:7778344": dict(descricao="VALVULA FLUX COM RETORNO TOTAL", cod_ref="000.249.8344", variacoes="REF LNG: 43-187",
                        aplicacao="608/364/365/OH1313/1316/1517", info="", montadora=MB),
    "cod:5115168": dict(descricao="VALVULA VOLVO CAIXA CAMBIO FH12 20775168", cod_ref="20775168", info="LANÇAMENTO 03/2025", montadora=V),
    "cod:5112627": dict(descricao="VALVULA VOLVO PONTO NEUTRO FH/NH/FM 8172627", tipo="VÁLVULA", cod_ref="8172627 / 1669324", variacoes="",
                        info="", montadora=V),
    "cod:5111363": dict(descricao="VALVULA NIVEL BANCO PNEUMA VOLVO FH 20443641", cod_ref="20443641 / 20586535 / 20748450",
                        aplicacao="Válvula de nível do banco a ar (banco pneumático)", info="LANÇAMENTO 03/2025", montadora=V),
    "cod:5111413": dict(descricao="VALVULA SOLENOIDE TRANSF CAIXA CAMBIO 2 PINOS", cod_ref="BH1X7595AA / 21266510 / 503356201",
                        aplicacao="Válvula solenóide caixa câmbio / Compatível: Iveco EuroCargo / Ford / Volvo", info="LANÇAMENTO 03/2025",
                        montadora="Volvo, Iveco, Ford"),
    "cod:5111140": dict(descricao="VALVULA SOLENOIDE MOLDURA 24V ABS 4721950180", cod_ref="4721950180", aplicacao="Iveco / Scania / Volvo",
                        marca="Wabco", montadora="Iveco, Scania, Volvo"),
    "cod:4721950180": {"skip": True},
    "cod:5111327": dict(descricao="VALVULA SOLENOIDE SISTEMA TRAVA DIFERENCIAL", aplicacao="Garrafinha transferência / Compatível: Scania T112/R112/T113/R113/T132/R142/T143/R143",
                        montadora=SC),
    "cod:5119557": dict(descricao="VALVULA SCANIA PONTO NEUTRO 1319557", cod_ref="1319557", montadora=SC),
    "cod:5111354": dict(descricao="VALVULA NIVELADORA SC L94/ K94/ K112/ K124", aplicacao="", montadora=SC),
    "cod:5111335": dict(descricao="VALVULA APU FILTRO SECADOR SCANIA 4324102262", cod_ref="4324102262",
                        aplicacao="Filtro secador | Rosca grossa / Compatível: VW / Scania", montadora="Scania, Volkswagen"),
    "cod:5118083": dict(descricao="VALVULA SCANIA SOLENOIDE CAMBIO 113 1488083", cod_ref="1488083", montadora=SC),
    "cod:5111120": dict(descricao="VALVULA ACIONACURTA FREIO MOTOR 4630131120", cod_ref="463.013.012-0 / 4630131120",
                        variacoes="Código 43-140 (816.3009) / LNG RDA-0314 (num. novo LNG 43-826)", marca="Wabco",
                        info="Válvula acionamento freio motor (Wabco) (haste curta)", aplicacao="MBB / Volvo / VW / Fiat",
                        montadora="Mercedes-Benz, Volvo, Volkswagen, Ford, Fiat"),
    "cod:7771384": dict(descricao="VALVULA FLUXO COM RETORNO LIMITADO SCANIA", cod_ref="1384864", variacoes="REF LNG: 43-169",
                        aplicacao="T114/ R114/ T124/ R124/ P124/ P94/ K94/ K124", info="", montadora=SC),
})
_VW16 = "Volkswagen 16.180 CO 1993 / 1994 / 1995 / 1996"
MANUAIS = {166}
ADD += [
    dict(pagina=166, card=1, codigo="51160015", descricao="VALVULA 3/2 VIAS CORPO DUPLO", tipo="VÁLVULA", marca="Brex",
         info="Válvula desbloqueio do truck 3/2 vias-NA corpo duplo VALV77", foto_spec={"rect": [28, 92, 150, 215]}),
    dict(pagina=166, card=2, codigo="8791622", descricao="VALVULA DE BLOQUEIO SEGURANÇA MODERNA", tipo="VÁLVULA", cod_ref="0308750470",
         aplicacao="Carreta moderna todas", montadora="Mercedes-Benz", foto_spec={"rect": [245, 95, 425, 220]}),
    dict(pagina=166, card=3, codigo="5117600", descricao="VALVULA ACION FREIO MOTOR 12V VOLKS", tipo="VÁLVULA", cod_ref="7600-076RTH",
         aplicacao="Acionamento do freio motor, reduzida e trava do diferencial / " + _VW16, info="Tipo 3/2 vias NF | Tensão 12 VCC",
         montadora="Volkswagen", foto_spec={"rect": [28, 260, 210, 330]}),
    dict(pagina=166, card=4, codigo="5117624", descricao="VALVULA ACION FREIO MOTOR 24V FORD", tipo="VÁLVULA",
         cod_ref="2RP901015A / 7600-076RTH", variacoes="SKU 136866 / A.Parts AP6004773-3000",
         aplicacao="Volkswagen, Ford e Mercedes-Benz / " + _VW16, info="Tipo 3/2 vias NF | Tensão 14 VCC",
         montadora="Volkswagen, Ford, Mercedes-Benz", foto_spec={"rect": [380, 250, 470, 320]}),
    dict(pagina=166, card=5, codigo="7773760", descricao="CABECOTE FILTRO RACOR ROSCA DO FILTRO 1\" X 12UNF", tipo="CABEÇOTE FILTRO",
         cod_ref="323519 / 376.092.7208", variacoes="REF LNG: 09-237", montadora="Mercedes-Benz",
         aplicacao="2423B / 2423K / 2423 / Atego 1725 / 1315 / 1418 / 1518 / Axor 1933 / 2533 / 2628K / 2628B / 2831K / 2831B / 2035 / 2040 / 2044 / 2535 / 2540 / 2644 / Actros 3340 / 3340S / 3340K / 4140 / Accelo 715 / 915 / 915C / O500",
         info="Furo lateral 16MM", foto_spec={"rect": [30, 365, 140, 480]}),
    dict(pagina=166, card=6, codigo="7773761", descricao="CABECOTE FILTRO RACOR ROSCA FILTRO 1\" X14UNF", tipo="CABEÇOTE FILTRO",
         cod_ref="2R0.201.581B", variacoes="REF Rochester 032.434-5 / REF BR 508604", aplicacao="Uso geral linha diesel",
         info="Rosca 1\"X14UNS-2B | Rosca de entrada e saída 16mm", foto_spec={"rect": [245, 365, 410, 525]}),
    dict(pagina=166, card=7, codigo="5110834", descricao="VALVULA DE PROTEÇÃO 4 CIRCUITOS - 6 VIAS", tipo="VÁLVULA",
         cod_ref="A0044310406", variacoes="SKU K014440/S", montadora="Mercedes-Benz",
         info="LANÇAMENTO | Código interno impresso em preto | Roscas: pórtico 1 NG 12 (M22 x 1,5); pórticos 21-26 NG 12 (M22 x 1,5); "
              "pórticos 27 e 28 M12 x 1,5 | Pressão de alimentação 10 bar | Abertura: pórticos 21 e 22 9 -0,3 bar; 23 a 26 7,5 -0,3 bar | "
              "Fechamento: pórticos 21 e 22 >7 bar; 23 a 26 >5,5 bar", foto_spec={"rect": [28, 535, 105, 660]}),
    dict(pagina=166, card=8, codigo="5113229", descricao="VALVULA PROTECAO 6 CIRCUITOS O500 RSD", tipo="VÁLVULA",
         cod_ref="0034316806", variacoes="Códigos similares: II37680", montadora="Mercedes-Benz",
         foto_spec={"rect": [245, 535, 400, 660]}),
]
AJ.update({"cod:5112675": {"montadora": "Mercedes-Benz, Volare"}, "cod:5114113": {"montadora": MB, "marca": "Knorr", "cod_ref": "AM514113"},
           "cod:5119326": {"montadora": SC}, "cod:5118864": {"montadora": SC}, "cod:51194004": {"montadora": "Mercedes-Benz, Volkswagen"}})
GRADES[168] = {"cells": [[20, 85, 298, 245], [298, 85, 570, 245], [20, 245, 298, 410], [298, 245, 570, 410],
                         [20, 410, 298, 575], [298, 410, 570, 575], [20, 575, 210, 805], [210, 575, 390, 805], [390, 575, 570, 805]],
               "fonte": 8.5}
GRADES[169] = {"rows": [85, 250, 450, 615, 805], "fonte": 12}
_VW_MAN = ("Volkswagen 15.180 EOD 2004-2006 / 16.180 CO 1993-1999 / 17.210 OD 2003 e demais versões listadas no card (todas as versões)")
AJ.update({
    "cod:5110181": dict(descricao="VALVULA MANETIN 3 SAIDAS 16MM", cod_ref="9584300181", variacoes="REF LNG: 43-435",
                        aplicacao="Mercedes: Atego 1315/ 1418/ 1518/ 1718/ 1725/ Axor 1933S/ 2425/ 2533", montadora=MB),
    "cod:5111700": dict(descricao="VALVULA MANETIN 3 SAIDA 2 SAIDAS 14MM 3504307009", cod_ref="3504307009 / Wabco 961.722.170.0",
                        variacoes="REF LNG: 43-863", info="", montadora=MB,
                        aplicacao="Mercedes-Benz LS 1929 (OM 355/6 LA) 1983-1998 / L 1314 (OM 352) 1987-1997 / L 1318 (OM 352 A) 1987-1997 / L 1514 (OM 352) 1987-1997"),
    "cod:5119290": dict(descricao="VALVULA MANETIN 2 SAIDAS 14MM", cod_ref="2RP 607 403 A", variacoes="REF LNG: 43-519", info="",
                        aplicacao=_VW_MAN, montadora="Volkswagen"),
    "cod:7770041": dict(descricao="VALVULA MANETIN 2 SAIDAS 14MM", cod_ref="2TA 607 403", variacoes="Wabco 98400195 / Cód. similar: 961.722.151.0 / II31325",
                        info="", montadora="Iveco, Volkswagen",
                        aplicacao="Iveco: Eurocargo 120E15/ 150E18/ 160E21/ 170E21/ 170E22/ 230E22/ 260E25/ 450E32/ 450E37/ Eurotrakker 380E38/ 450E37 | Volkswagen: 7.100/ 8.140/ 12.140/ 14.150/ 14.220/ 16.170/ 16.220/ 16.300/ 24.220"),
    "cod:7770042": dict(descricao="VALVULA MANETIN 2 SAIDAS 16MM SCANIA", aplicacao="F113HL/ F94/ K112/ K113/ K124", info="16MM / 16MM"),
    "cod:51143865": dict(descricao="MANETIN 2 SAIDAS 14MM", tipo="VÁLVULA", cod_ref="Volkswagen 2TA607403 / Ford 1C452A622AA / EC452A622AA",
                         variacoes="REF LNG: 43-865 / Código similar: Wabco (Volkswagen) 98400195", montadora="Volkswagen, Ford",
                         info="Válvula manete (freio de mão) 2 saídas 14mm",
                         aplicacao="Volkswagen 7100 / 8140 / 12140 / 14150 / 14220 / 16170 / 16220 / 16300 / 24220 / Ford Cargo 712 / 814 / 815 / 915 / 1215 / 1415 / 1422 / 1617 / 1622 / 1317E / 1517E / 1722E / 2422E / 2428E / 2628E / 2632E / 2932E"),
    "cod:51143798": dict(aplicacao="Iveco / Mercedes-Benz / Volkswagen / Scania / Volvo - todos com caçamba", info="",
                         montadora="Iveco, Mercedes-Benz, Volkswagen, Scania, Volvo"),
    "cod:5111710": dict(descricao="VALVULA MANETIN 2 SAIDAS VW 961 722 1710", cod_ref="961 722 1710", info="14x1,5mm / 14x1,5mm"),
    "cod:511423951": dict(info="Roscas 1/4", montadora="Volvo, Scania, Volkswagen, Mercedes-Benz, Iveco",
                          aplicacao="Caminhões, cavalo mecânico, ônibus, semirreboque (tabela de aplicação do card)"),
    "cod:511405095": dict(info="Mesma ST 056 (Suspentech)", aplicacao="Conjunto completo de válvula niveladora - todos",
                          montadora="Mercedes-Benz, Scania, Volvo, Volkswagen, Iveco"),
    "cod:4990056": dict(marca="Suspentech", info="Válvula - conjunto completo de válvula niveladora carretas | Rosca 1/4 NPT", montadora=MB),
})
GRADES[170] = {"rows": [85, 236, 390, 512, 645, 805], "cols": [20, 298, 570], "fonte": 9}
TIPOS.insert(0, (r"SECADOR|SECADORA|APU", "SECADOR DE AR / APU"))
AJ.update({
    "cod:5110040": dict(cod_ref="9324000070 / 0004301515 / 0004304515 / 6934208371 / 81630130 / 9324000030 / 9325000120", marca="Wabco",
        aplicacao="Mercedes-Benz 1214K / 1215C / 1218R / 1418 / 1418EL / 1720 / 1720K / 1723 / 1723S / 2423B / 2423K / L1418R / L1620 / L1620R / L1622 / LK1418 / LK1620 / LS1632 / OF1620 / OF1721 / OH1421 / OH1621 / 1935 / 1938 / 2635 / 2638 / 3340 / 3344",
        info="", montadora=MB),
    "cod:5119515": dict(cod_ref="29409515 / Volvo 8137622 / 20409513 / 20409515",
        variacoes="Knorr-Bremse II19483 / K001392 / K005022 / LNG 43-192",
        aplicacao="Caminhão Volvo FH12 (1993-2012) / FH16 (1993-2012) e demais Volvo listados no card", info="Secador de ar | Foto ilustrativa", montadora=V),
    "cod:5119513": dict(descricao="VALVULA VOLVO SECADOR AR APU 20409513", cod_ref="20409513",
        aplicacao="Volvo FH/FM/NH - FH12/FH16 - FM7/FM10/FM12 - NH12/BR até 2005", info=""),
    "cod:5111364": dict(cod_ref="20884103", aplicacao="Volvo FH / FM / NH", info=""),
    "cod:5117373": dict(aplicacao="Volkswagen 5.140EOD / 8120OD / 8150EOD / 9150EOD / 26260E / 31260E / 31320E / Constellation", info="Válvula APU"),
    "cod:5111144": dict(cod_ref="50054085"),
    "cod:7772262": dict(descricao="FILTRO SECADOR AR APU UNIVERSAL", cod_ref="432 410 020 2 / 4324100202 / 076.954-10A",
        aplicacao="Compatível: Volvo | Volkswagen | Mercedes-Benz | Iveco | Ford", montadora="Volvo, Volkswagen, Mercedes-Benz, Iveco, Ford",
        info="IMPORTADO | Altura 164mm | Diâmetro interno 100mm | Diâmetro externo 136mm / 110mm | Conexão / rosca M39 x 1,5"),
    "cod:5113357": dict(descricao="FILTRO AR SECADOR APU COMPLETA SCANIA S5 WABCO", tipo="SECADOR DE AR / APU", marca="Wabco", montadora=SC,
        cod_ref="Scania 1796161 / 1941953 / 2063357 / 2148069 / 2308777", variacoes="Wabco 9325100090 / 9325100040R / 000229251785 / 0370444 / 000229251787 / EAN 7895851081338",
        info="Válvula E-APU Scania série 5 Wabco"),
    "cod:7771600": dict(descricao="FILTRO SECADOR AR SCANIA"),
})
NOTAS += ["p171: página institucional (Falcão / Quinelato Freios), sem produtos.",
          "p165: 4721950180 é a ref. original impressa em vermelho no card 5111140 (não é código interno).",
          "p166: código 5110834 impresso em preto (não vermelho) — registrado.",
          "p159: 4001072 (QA-1072) e 4001280 (QA-1280C) são jogos de reparo mostrados dentro dos cards das válvulas; registrados como produtos e citados nas válvulas."]
AJ["cod:8005502"] = {"descricao": "REP VALVULA PUSH PULL 16 X 1,5 PT", "info": ""}
AJ["cod:7773641"] = {"tipo": "CABEÇOTE FILTRO", "info": "Aplicação: todos Scania", "aplicacao": "Todos Scania"}
NOTAS += ["Conferência automática: na p168 os códigos 51143798, 5111710 e 5111143 estão colados na mesma linha de texto do PDF; os três estão registrados."]
