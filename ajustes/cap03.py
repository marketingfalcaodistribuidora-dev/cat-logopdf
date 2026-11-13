# Capítulo 3 - Reparo Freio (págs. 20-32) — ajustes da revisão visual
VB = "B7, B7M, B7R, B9R, B10, B12, B12M, B12R"
MER = "Ref. Meritor ELSA195 / ELSA225"

TIPOS = [
    (r"PIST[AÃ]O", "PISTÃO"), (r"EIXO\s+(VOLVO\s+)?TRANSV", "EIXO"), (r"\bALAV", "ALAVANCA"),
    (r"\bUND\.?|UNIDADE DE AJUSTE", "UNIDADE DE AJUSTE"),
    (r"CONTRA ?PINO", "CONTRA PINO"), (r"INDICADOR", "INDICADOR DE DESGASTE"), (r"RETENTOR", "RETENTOR"),
    (r"COROA", "COROA"), (r"CREMALHEIRA", "CREMALHEIRA"), (r"SUPORTE", "SUPORTE"),
    (r"GUAR?DA.?P[OÓ]|TAMPA BORRACHA|COIFA", "GUARDA-PÓ / TAMPA BORRACHA"), (r"PARAFUSO|\bPF\b", "PARAFUSO"),
    (r"BUCHA|MANCAL", "BUCHA / MANCAL"), (r"KIT REP|REP PARCIAL|REPARO", "KIT REPARO"), (r"PINH[AÃ]O", "PINHÃO"),
    (r"REGULADOR", "REGULADOR / PINO REGULADOR"), (r"ENGRENAGEM", "ENGRENAGEM DE AJUSTE"), (r"MECANISMO", "MECANISMO DE AJUSTE"),
    (r"TAMPA", "TAMPA"), (r"JUNTA|GUIA", "GUIA / JUNTA"), (r"EIXO", "EIXO"), (r"ROLAMENTO", "ROLAMENTO"),
    (r"PIST[AÃ]O", "PISTÃO"), (r"SAPATA", "SAPATA PINÇA"), (r"ALAVANCA", "ALAVANCA"), (r"CORRENTE", "CORRENTE"),
    (r"CORPO", "CORPO DE ACIONAMENTO"), (r"CAVALETE", "CAVALETE"), (r"MOLA", "MOLA"), (r"ADAPTADOR", "ADAPTADOR"),
    (r"TRAVA", "TRAVA"), (r"\bPINO\b", "PINO"),
]

AJ = {
    # ---------------- pág. 20 (todos com logo Volvo) ----------------
    "20.1": {"montadora": "Volvo", "info": "Lado: L/D"},
    "20.2": {"montadora": "Volvo", "info": "Lado: L/E"},
    "20.3": {"montadora": "Volvo"}, "20.4": {"montadora": "Volvo"}, "20.5": {"montadora": "Volvo"},
    "20.6": {"montadora": "Volvo"}, "20.7": {"montadora": "Volvo"}, "20.8": {"montadora": "Volvo"},
    "20.9": {"montadora": "Volvo", "aplicacao": f"Volvo {VB} / {MER}"},
    "20.10": {"montadora": "Volvo", "aplicacao": f"Volvo {VB} / {MER}, pinça 20706903"},
    "20.11": {"montadora": "Volvo", "aplicacao": f"{MER} / pinça 20706903"},
    "20.12": {"montadora": "Volvo", "aplicacao": f"Volvo {VB} / {MER}"},
    # ---------------- pág. 21 ----------------
    "21.1": {"montadora": "Volkswagen, Volvo",
             "aplicacao": "VW 33460 8x4 (3º e 4º eixo, lado esquerdo), VW 32380 6x4 (2º eixo, lado esquerdo), Volvo FH, NH, FM12, B12",
             "info": "Substitui o código original"},
    "21.2": {"montadora": "Volkswagen, Volvo",
             "aplicacao": "VW 33460 8x4 (3º e 4º eixo, lado direito), VW 32380 6x4 (2º eixo, lado direito), Volvo FH, NH, FM12, B12",
             "info": "Substitui o código original"},
    "21.3": {"montadora": "Volvo", "aplicacao": "Volvo / Compatível: B12, FH, FH12, NH"},
    "21.4": {"montadora": "Volvo", "marca": "Eckisil", "cod_ref": "8550978, 272909, 68162565"},
    "21.5": {"montadora": "Volvo", "marca": "Eckisil", "cod_ref": "8550978, 272909, 68162565"},
    "21.6": {"montadora": "Volvo", "cod_ref": "1696450", "aplicacao": "FH / NH / FM12 / B12"},
    "21.7": {"montadora": "Volvo", "cod_ref": "Tampa 1696449 / Junta 1696450"},
    "21.8": {"montadora": "Volvo", "marca": "Eckisil", "aplicacao": "C DUCO / D DUCO / LE DUCO / Radial B7 / B10 / B12",
             "info": "Comp. 102mm, Ø25mm / Comp. 125mm | Aplicação DUCO"},
    "21.9": {"montadora": "Volvo", "marca": "Eckisil", "aplicacao": f"Veículos: {VB}, FH / {MER}"},
    "21.10": {"montadora": "Volvo", "cod_ref": "1696446, 64225252",
              "aplicacao": "B10B / B12 / FH12 / FH16 / FM10 / FM12 / FM7 / FM9 / NH12 / NL10 / NL12"},
    "21.11": {"montadora": "Volvo", "cod_ref": "276100, 3090964",
              "aplicacao": "FH13 Novo / FH13 Clássico / FH12 Clássico / FM13 Novo / FM13 Clássico / FM12 Clássico / FM11 Novo / FM11 Clássico / NH12 Clássico"},
    "21.12": {"montadora": "Volvo", "marca": "Eckisil", "cod_ref": "00823",
              "variacoes": "REF Eckisil: 00823 / REF Quinelato: QA-4411 / REF Farj: 96285-0",
              "aplicacao": f"Volvo {VB} / {MER}"},
    "21.13": {"montadora": "Volvo", "aplicacao": f"Volvo {VB} / {MER}"},
    "21.14": {"montadora": "Volvo", "aplicacao": f"Volvo {VB} / {MER}"},
    "21.15": {"montadora": "Volvo", "aplicacao": f"{MER}, pinça 20706903"},
}
ADD = []

# ---------------- págs. 30-32 (logos Mercedes-Benz / Accelo / Eckisil embutidos nas fotos) ----------------
for c in range(1, 13):
    AJ[f"30.{c}"] = {"montadora": "Mercedes-Benz", "marca": "Eckisil", "aplicacao": "Accelo", "info": "Logo Accelo"}
for c in range(1, 5):
    AJ[f"31.{c}"] = {"montadora": "Mercedes-Benz", "marca": "Eckisil", "aplicacao": "Accelo", "info": "Logo Accelo"}
AJ["31.1"]["info"] = "14 elos | Logo Accelo"
AJ["31.5"] = {"montadora": "Mercedes-Benz, Scania", "marca": "Eckisil",
    "cod_ref": "MB: A6964205301; A6964205401; A6964206201; A6964206301; A6964203001; A6964203101; A6964205701; A6964205801; A6964205901; 6964206001; A3824201201; A3824201101 / Scania: 1517003; 1517004",
    "aplicacao": "Pinças Knorr / Veículos: 1938S, 1944S (a partir de 2003) / Axor 1933S, 2035, 2040, 2044, 2533, 2540, 2544, 2640, 2644, 2825, 2828, 3340, 3344, 4140 / LS1938 até 2003 / Linha Actros / Accelo / Ônibus urbano Mercedes e Scania / L94 a partir de 2004",
    "info": "SKU: 5060067"}
AJ["31.7"] = {"aplicacao": "Pinça freio Knorr", "info": "Alavanca da pinça (ângulo 12° - 122 mm)"}
AJ["31.8"] = {"aplicacao": "Pinça freio Knorr", "info": "Alavanca da pinça (ângulo 0° - 113 mm)"}
AJ["31.9"] = {"aplicacao": "Pinça freio Knorr", "cod_ref": "MY100132", "variacoes": "K0071 / 095.824 / 096.035 / 6006-02 / KVK2901"}
for c in range(1, 13):
    AJ[f"32.{c}"] = {"montadora": "Mercedes-Benz", "marca": "Eckisil"}
AJ["32.1"].update({"aplicacao": "Knorr 22.5 série SK7000; SL7000; SM7000", "info": "Ø da sapata: 69mm | Logo Actros"})
AJ["32.2"].update({"aplicacao": "Knorr 22.5 série SK7000; SL7000; SM7000 / Outros: toda a linha Actros", "info": "Logo Actros"})
AJ["32.3"].update({"aplicacao": "Knorr SN5000 / Outros: Accelo 915C, Accelo 1016", "info": "Logo Accelo"})
AJ["32.4"].update({"aplicacao": "Knorr 22.5 série SK7000; SL7000; SM7000 / Outros: toda a linha Actros e Axor", "info": "Medidas 9,5mm / 78,5mm | Logo Actros"})
AJ["32.5"].update({"aplicacao": "Knorr 22.5 série SK7000; SL7000; SM7000 / Outros: toda a linha Actros e Axor", "info": "Logos Actros / Axor"})
for k in ("32.6", "32.7", "32.8", "32.9"):
    AJ[k].update({"aplicacao": "Knorr SN5000 / Outros: Accelo 915C, Accelo 1016", "info": "Logo Accelo"})
AJ["32.11"].update({"aplicacao": "Mercedes-Benz"})
AJ["32.12"].update({"aplicacao": "Knorr 22.5 série SB6000 / SB7000 / SN6000 / SN7000 / SK6000 / SK7000 / SL7000 / SM7000",
                    "variacoes": "Conversão: Axor 1933S, 2035, 2040, 2044, 2533, 2540, 2544, 2640, 2644, 2825, 2828, 3340, 3344, 4140", "info": "Logo Axor"})

# ---------------- págs. 28-29 (logos Scania + Mercedes-Benz) ----------------
V_STD = "1938S, 1944S (a partir de 2003) / Axor 1933S / Axor 2035 / LS1938 até 2003 / Linha Actros / Accelo / Ônibus urbano Mercedes e Scania"
V_AXOR = ("1938S / 1944S (a partir de 2003) / Axor 1933S, 2035, 2040, 2044, 2533, 2540, 2544, 2640, 2644, 2825, 2828, 3340, 3344, 4140 / "
          "LS 1938 até 2003 / O500 todos / O500U a partir de 2003 / K 124IB a partir de 2004 / L94 a partir de 2004 / O500M a partir de 2003 / Ônibus urbano Mercedes e Scania")
SM = "Scania, Mercedes-Benz"
for c in range(1, 13):
    AJ[f"28.{c}"] = {"montadora": SM, "aplicacao": V_STD}
AJ["28.1"]["info"] = "Aplicação (na foto): Knorr 22.5 série SN6000 / SN7000"
AJ["28.3"]["info"] = "Medidas: 13,5 MM / 78,5 MM"
AJ["28.4"]["descricao"] = "CAVALETE MB 1938S / 1944S (A PARTIR DE 2003)"
AJ["28.6"].update({"aplicacao": V_AXOR + " / Toda a linha Actros"})
AJ["28.9"].update({"aplicacao": V_AXOR})
AJ["28.10"]["info"] = "69mm"
AJ["28.11"]["info"] = "74mm"
AJ["29.1"] = {"montadora": SM, "aplicacao": "Toda a linha Actros / Ônibus urbano Mercedes e Scania", "info": "08 x 16MM | Chave Torx - T45"}
AJ["29.2"] = {"montadora": SM, "aplicacao": "Toda a linha Actros / Ônibus urbano Mercedes e Scania"}
AJ["29.3"] = {"montadora": SM, "aplicacao": V_STD}
AJ["29.4"] = {"montadora": "Scania", "aplicacao": "Veículo: Scania / Knorr série SB7000"}
AJ["29.5"] = {"montadora": "Scania", "aplicacao": "Knorr 22.5 série; SN6000; SN7000; SK7000"}
AJ["29.6"] = {"montadora": "Mercedes-Benz", "aplicacao": "Toda a linha Actros / Knorr 22.5 série; SK6000; SK7000; SL7000; SM7000"}
AJ["29.7"] = {"montadora": "Mercedes-Benz", "aplicacao": "Toda a linha Actros", "info": "Logo Actros"}
AJ["29.8"] = {"montadora": "Mercedes-Benz", "aplicacao": "Knorr 22.5 série SK7000; SL7000; SM7000 / Veículos: toda a linha Actros e Axor", "info": "Logos Axor / Actros"}
AJ["29.9"] = {"montadora": "Mercedes-Benz", "aplicacao": "Accelo 915C / Accelo 1016", "info": "Logo Accelo"}
AJ["29.10"] = {"aplicacao": V_AXOR}
AJ["29.11"] = {"montadora": SM, "aplicacao": V_AXOR}
AJ["29.12"] = {"aplicacao": V_AXOR}

# ---------------- págs. 22-27: páginas Eckisil ----------------
APL_KNORR_OUT = "Outros: Scania 1938S, 1944S (a partir de 2003) e Axor 1933S / Axor 2035 / Axor 2040 / Axor 2044 / Axor 2533"
for pg, cards in ((22, range(1, 13)), (23, range(1, 10)), (24, range(1, 10))):
    for c in cards:
        AJ.setdefault(f"{pg}.{c}", {}).update({"marca": "Eckisil", "montadora": "Volvo"})
for c in range(1, 13):
    AJ.setdefault(f"26.{c}", {}).update({"marca": "Eckisil", "montadora": "Scania, Mercedes-Benz"})
for c in range(1, 6):
    AJ.setdefault(f"27.{c}", {}).update({"marca": "Eckisil", "montadora": "Scania, Mercedes-Benz"})
OUT_V = "Outros: B7 / B7M / B7R / B9R / B10 / B12 / B12M / B12R / FH"
AJ["22.4"]["aplicacao"] = "Ref. Meritor ELSA2 / ELSA195 / ELSA225 / " + OUT_V
AJ["22.5"]["aplicacao"] = "ELSA195 / ELSA225 / Outros: B7 / B7M / B7R / B9R / B10 / B12 / B12M / B12R"
for k in ("22.6", "22.7", "22.8", "24.1"):
    AJ[k]["aplicacao"] = "Ref. Meritor ELSA195 / ELSA225 / MCK1254 / " + OUT_V
for k in ("23.5", "23.6", "23.7", "24.2", "24.3", "24.5", "24.6", "24.7"):
    AJ[k]["aplicacao"] = "Ref. Meritor ELSA195 / ELSA225 / " + OUT_V
AJ["23.8"]["aplicacao"] = "Ref. Meritor ELSA225 / " + OUT_V
AJ["23.9"]["aplicacao"] = "Ref. Meritor ELSA2 / ELSA195 / ELSA225 / " + OUT_V
AJ["24.4"]["aplicacao"] = "Ref. Meritor ELSA2 / ELSA195 / ELSA225 / " + OUT_V
AJ["24.8"]["aplicacao"] = "Ref. Meritor ELSA2 / ELSA195 / ELSA225 / Radial / " + OUT_V
AJ["24.9"]["aplicacao"] = "Ref. Meritor ELSA2 / ELSA195 / ELSA225 / " + OUT_V
AJ["24.7"]["info"] = "Card repetido no catálogo (mesmo produto do card ao lado)"
AJ["22.9"]["aplicacao"] = "Volvo FH / NH / FM12 / B12"
AJ["22.10"]["aplicacao"] = "Volvo FH / NH / FM12 / B12"
AJ["22.12"].update({"montadora": "Scania, Volvo", "aplicacao": "Scania e Volvo", "records": [dict(codigo="49345010", descricao="CONJ. COROA RA1 10 ESTRIAS", tipo="COROA")]})
AJ["25.1"] = {"marca": "Eckisil", "montadora": "Scania, Volvo", "records": [dict(
    codigo="49345010", descricao="CONJ. COROA RA1 10 ESTRIAS", tipo="COROA", aplicacao="Scania / VV",
    info="Código impresso dentro da imagem do card")]}
for k in ("25.2", "25.3", "25.4"):
    AJ[k] = {"marca": "Eckisil", "montadora": "Scania, Mercedes-Benz, Volvo", "aplicacao": "Scania / MB / VV"}
AJ["25.5"] = {"marca": "Eckisil", "montadora": "MAN, Mercedes-Benz", "aplicacao": "MB / MAN"}
AJ["25.6"] = {"marca": "Eckisil", "aplicacao": "Knorr 22.5 série; SN6000; SN7000"}
AJ["25.7"] = {"marca": "Eckisil"}
_K = {
    "26.1": "Knorr 22.5 série; SB6000; SB7000; SN6000; SN7000; SK6000; SK7000; SL7000; SM7000",
    "26.2": "Knorr 22.5 série; SB6000; SB7000; SN6000; SN7000", "26.3": "Knorr 22.5 série; SB6000; SB7000; SN6000; SN7000",
    "26.4": "Knorr 22.5 série; SB6000; SB7000; SN6000; SN7000", "26.5": "Knorr 22.5 série; SB6000; SB7000; SN6000; SN7000",
    "26.6": "Knorr 22.5 série; SB6000; SB7000; SN6000; SN7000",
    "26.7": "Knorr 22.5 série; SB6000; SB7000; SN6000; SN7000; SK6000; SK7000; SL7000; SM7000",
    "26.8": "Knorr 22.5 série; SN6000; SN7000", "26.9": "Knorr 22.5 série; SN6000; SN7000",
    "26.10": "Knorr 22.5 série; SN6000; SN7000; SB6000; SB7000",
    "26.11": "Knorr 22.5 série SB6000 / SB7000 / SN6000 / SN7000 / SK6000 / SK7000 / SL7000 / SM7000",
    "26.12": "Knorr 22.5 série; SB6000; SB7000; SN6000; SN7000; SK6000; SK7000; SL7000; SM7000",
    "27.1": "Knorr SN5000", "27.2": "Knorr 22.5 série; SB6000; SB7000; SN6000; SN7000; SK6000; SK7000; SL7000; SM7000",
    "27.3": "Knorr 22.5 série SN 7000", "27.4": "Knorr 22.5 série SB6000; SB7000; SN6000; SN7000",
    "27.5": "Knorr 22.5 série SB6000 / SB7000 / SN6000 / SN7000 / SK6000 / SK7000 / SL7000 / SM7000",
}
for k, v in _K.items():
    AJ[k]["aplicacao"] = v + " / " + APL_KNORR_OUT

AJ["21.3"]["tipo"] = "PINO"
AJ["31.7"]["descricao"] = "BALANCIN DIANT PINCA FREIO KNORR"
AJ["31.8"]["descricao"] = "BALANCIN TRAS PINCA FREIO KNORR"
AJ["29.2"]["info"] = ""
AJ["29.6"]["info"] = ""
AJ["31.9"]["info"] = ""
AJ["31.7"]["tipo"] = "BALANCIN / ALAVANCA PINÇA"
AJ["31.8"]["tipo"] = "BALANCIN / ALAVANCA PINÇA"
