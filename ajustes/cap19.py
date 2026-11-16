# Capítulo 19 - Equipamentos de Solda (págs. 249-251)
TIPOS = [(r"ELETRODO", "ELETRODO DE SOLDA"), (r"ARAME", "ARAME DE SOLDA"), (r"MAQ", "MÁQUINA DE SOLDA"),
         (r"LUVA", "LUVA DE SOLDAGEM"), (r"MANGUEIRA", "MANGUEIRA DE OXIGÊNIO")]
VD, WW, ESAB = "Vonder", "Weld West Arco", "ESAB"
_KG = "Preço por kg"
AJ = {
    "cod:6053250": {"marca": WW, "info": "5KGS | " + _KG + " | Classificações: AWS / ASME SFA 5.1 / E6013 | Diâmetro: 3,25mm | "
                    "Corrente: 85-160A | Tensão: 20-30V | Tipo corrente: CA >= 50V/CC+ e CC- | Caixa com 5kg | "
                    "Resistência à tração: 480 - 520Mpa | Alongamento: 22 - 24%"},
    "cod:6010025": {"marca": VD, "info": "5KGS | " + _KG},
    "cod:6059218": {"descricao": "ELETRODO 9218 FERRO FUNDIDO AÇO LIMÁVEL", "marca": ESAB, "tipo": "ELETRODO DE SOLDA",
                    "info": "Descrição impressa como imagem no card"},
    "cod:6016040": {"marca": VD},
    "cod:6053252": {"descricao": "ELETRODO 7018 3,25 MM WELD WEST ARCO", "marca": WW,
                    "info": "5KGS | " + _KG + " | Eletrodo de solda 6013 3,25 X 350MM Weld West Arco | Caixa com 1,0KG - ESAB"},
    "cod:6017018": {"descricao": "ELETRODO VD 7018 3,25 MM VD", "marca": VD, "info": "5KGS | " + _KG},
    "cod:6050400": {"descricao": "ELETRODO 7018 4,00 MM CONARCO", "marca": "ESAB / Conarco", "info": "25KGS"},
    "cod:6017040": {"descricao": "ELETRODO VD 7018 4,00 MM VD", "marca": VD, "info": "5KGS | " + _KG},
    "cod:6056213": {"descricao": "ELETRODO 6013 2,00 MM WELD WEST ARCO", "marca": WW, "info": "5KGS | " + _KG},
    "cod:6012025": {"descricao": "ELETRODO 6013 2,50 MM VD (CAIXA 5 KGS)", "marca": VD, "tipo": "ELETRODO DE SOLDA",
                    "info": "5Kgs | " + _KG},
    "250.1": {"_titulo": "ARAME SOLDA MIG VONDER 15", "marca": VD},
    "cod:6051508": {"descricao": "ARAME SOLDA MIG CORESHIELD 15 0,8MM 4,5K", "marca": ESAB, "tipo": "ARAME DE SOLDA",
                    "info": "Descrição impressa como imagem no card"},
    "cod:6017405": {"marca": VD},
}
ADD = []
MANUAIS = {251}
_M = "Descrição impressa como imagem no card"
for _c, _d, _rect, _inf, _marca in [
        ("7745160", "MANGUEIRA OXIGENIO DUPLA 5/16 MAÇARICO", [279, 92, 553, 301], "", ""),
        ("6052021", "MAQ INVERSORA SOLDA LHN202I 10KVA 60H 220V", [49, 323, 258, 467],
         _M + " | Tensão da rede: 220V +/-10% | Frequência da rede: 50/60Hz", ESAB),
        ("6052421", "MAQ INVERSORA DE SOLDA TIG 200A LHN 242I 220V", [49, 485, 258, 632],
         _M + " | Tensão de alimentação: 1Ø - 220V (+/-10%) | Frequência: 50/60 Hz | Tensão em vazio: 83 V | "
              "Faixa de corrente: 10 - 200 A", ESAB),
        ("6058062", "LUVA SOLDAGEM PRETA MD BLACK", [42, 654, 222, 801],
         _M + " | Dimensões (C x L x A): 17 x 9 x 4 cm | Peso: 0,200 Kg", "")]:
    ADD.append(dict(pagina=251, card=len(ADD) + 1, codigo=_c, descricao=_d, info=_inf, marca=_marca,
                    foto_spec={"rect": _rect}))
NOTAS = ["Pág. 249: o código 6017040 (ELETRODO VD 7018 4,00 MM VD) aparece em dois cards iguais; registrado uma vez.",
         "Pág. 250: metade de baixo da página com molduras vazias.",
         "Pág. 251: textos dos cards (exceto códigos e o da mangueira) impressos como imagem; transcritos da página."]
