# Capítulo 27 - Acessórios e Ferragens Diversas (págs. 376-381)
TIPOS = [(r"PRESILHA", "PRESILHA"), (r"ENGATE", "ENGATE"), (r"DOBRADI", "DOBRADIÇA"), (r"TRAVA", "TRAVA"), (r"PINO", "PINO"),
         (r"MOLA A BICA|ALFINETE", "MOLA A BICA"), (r"GANCHO", "GANCHO"), (r"SUPORTE", "SUPORTE"), (r"FAIXA", "FAIXA REFLETIVA"),
         (r"CORRENTE", "CORRENTE"), (r"BOCA", "BOCA GRANELEIRA"), (r"REBITE", "REBITE"), (r"QUEBRA", "QUEBRA-DEDO"),
         (r"PARAFUSO|PF ", "PARAFUSO"), (r"ARRUELA|ARR ", "ARRUELA"), (r"NIPLE|NIPPLE", "NIPLE / CONEXÃO"), (r"OLHAL", "OLHAL"),
         (r"ANILHA", "ANILHA"), (r"PORCA", "PORCA"), (r"ESPIG", "ESPIGÃO"), (r"CALCO|CALÇO", "CALÇO")]
AJ = {}
ADD = []
NOTAS = []
MANUAIS = {376}
RD, GU = "Randon", "Guerra"
_Y = [85, 190, 292, 397, 499, 604, 704, 805]
_C3 = [20, 206, 389, 572]


def N(p, c, d, rect, **kw):
    ADD.append(dict(dict(pagina=p, card=len([r for r in ADD if r["pagina"] == p]) + 1, codigo=c, descricao=d, cod_ref="",
                         variacoes="", aplicacao="", info="", marca="", montadora="", _nao_agrupar=True,
                         foto_spec={"rect": rect}), **kw))


def c3(lin, col):
    return [_C3[col], _Y[lin], _C3[col + 1], _Y[lin + 1]]


# 376 (ferragens de carroceria; vários textos impressos como imagem)
N(376, "5065170", "PRESILHA DA CORRENTE TAMPA BITREM (V)", c3(0, 0), info="Abertura 32MM")
N(376, "5065180", "PRESILHA DA TAMPA", c3(0, 1), info="Abertura 40MM")
N(376, "5065250", "ENGATE S DO ENGATE CORRENTE ANTIGO", c3(0, 2))
_C4 = [20, 137, 272, 422, 572]
N(376, "5065190", "ENGATE ELO ENGATE CORRENTE ANTIGA", [_C4[0], 190, _C4[1], 292])
N(376, "5065390", "GANCHO TOMBADOR GUERRA", [_C4[1], 190, _C4[2], 292], montadora=GU)
N(376, "5065470", "PRESILHA MODELO GUERRA 26 MM", [_C4[2], 190, _C4[3], 292], montadora=GU)
N(376, "5065172", "PRESILHA TAMPA U 32MM", [_C4[3], 190, _C4[4], 292])
N(376, "4730614", "PINO TRAVA CORRENTE 1/4", c3(2, 0))
N(376, "4730516", "PINO TRAVA CORRENTE 5/16", c3(2, 0))
N(376, "5660009", "TRAVA PORCA 5/8 CARROCERIA", c3(2, 1))
N(376, "5669005", "TRAVA PORCA 3/4 CARROCERIA", c3(2, 1))
N(376, "5660512", "MOLA A BICA RANDON TP ALFINETE", c3(2, 2), montadora=RD)
N(376, "5068800", "DOBRADICA TRUCK", c3(3, 0), montadora=RD)
N(376, "5065400", "DOBRADIÇA DA TAMPA RANDON", c3(3, 1), montadora=RD)
N(376, "5065340", "DOBRADIÇA RANDON MODERNA", c3(3, 2), montadora=RD)
N(376, "5060511", "ENGATE DA CORRENTE RANDON MODERNA", c3(4, 0), montadora=RD)
N(376, "5065140", "ENGATE DA CORRENTE - ANTIGO - SÓ O GANCHO", c3(4, 1), montadora=RD)
N(376, "5065380", "ENGATE FEMEA TRUCK 200MM", c3(4, 2))
_C6 = [20, 161, 314, 425, 572]
N(376, "5065160", "PRESILHA DE FUEIRO (U)", [_C6[0], 604, _C6[1], 704])
N(376, "5060520", "ENGATE DA DOBRADIÇA TAMPA DA CARROCERIA 32MM LG", [_C6[1], 604, _C6[2], 704])
N(376, "5060519", "ENGATE DOBRADICA TAMPA 32MM (G) FUNDIDO NOVO", [_C6[2], 604, _C6[3], 704])
N(376, "5065130", "ENGATE FEMEA INFERIOR - TAMPA DA CARROCERIA 73MM", [_C6[3], 604, _C6[4], 704])
N(376, "5065430", "ENGATE SUPERIOR DA TAMPA", c3(6, 0))
N(376, "5065120", "ENGATE FEMEA - TAMPA DA CARROCERIA 135MM", c3(6, 1))
N(376, "5065420", "SUPORTE DO ARCO 3MM", c3(6, 2))
NOTAS.append("Pág. 376: várias descrições estão impressas como imagem (transcritas da página).")
# 377
MANUAIS.add(377)
N(377, "5065210", "GANCHO DO TOMBADOR CARROCERIA", [20, 85, 199, 203])
N(377, "5061060", "ARANHA DO ASSOALHO ZINCADA", [199, 85, 389, 203])
N(377, "5060880", "ARANHA DO ASSOALHO - ZB", [389, 85, 572, 203])
for _c, _m in (("2231378", "11/2"), ("2231379", "2"), ("2231380", "21/2"), ("2231381", "3"), ("2231382", "31/2")):
    N(377, _c, f"PF FRANCES ZB C/PO 5/16 X {_m}", [20, 220, 240, 300], _titulo="PARAFUSO FRANCES ZB C/PO 5/16", _nao_agrupar=False,
      card=50)
for _c, _m in (("7710142", "1/4' X 2'"), ("7715162", "5/16 2'"), ("4730382", "3/8' X 2'"), ("4737162", "7/16'X 2'")):
    N(377, _c, f"QUEBRA DEDO {_m}", [20, 311, 110, 399], _titulo="QUEBRA DEDO", _nao_agrupar=False, card=51)
N(377, "4731400", "QUEBRA DEDO 1/4\" X 1 1/2\" C/ CORRENTE", [20, 399, 200, 471], _titulo="QUEBRA DEDO C/ CORRENTE", _nao_agrupar=False, card=52)
N(377, "4731600", "QUEBRA DEDO 5/16\" X 40MM C/ CORRENTE", [20, 399, 200, 471], _titulo="QUEBRA DEDO C/ CORRENTE", _nao_agrupar=False, card=52)
for _c, _m in (("9133801", "3/8 X 1"), ("9131201", "1/2 X 1")):
    N(377, _c, f"REBITE LISO {_m}", [20, 599 - 128 + 10, 200, 599 - 30], info="Rebite maciço liso cabeça redonda")
for _c, _d in [("4730485", "4,0X28X90"), ("4730595", "5,0X95"), ("4732550", "2,5X18X50"), ("4733059", "3 X 18 X 59"),
               ("4734100", "4,8X29X100"), ("4734511", "4X29X120")]:
    N(377, _c, "TRAVA R IMPLEMENTOS " + _d, [90, 610, 190, 795], _titulo="TRAVA R IMPLEMENTOS", _nao_agrupar=False, card=53)
N(377, "4734140", "TRAVA R TOMBADOR CARRETA 4X140", [90, 610, 190, 795])
N(377, "4734724", "TRAVA R PARAFUSO CARRETA", [90, 610, 190, 795])
NOTAS.append("Pág. 377: os parafusos franceses 2231378-2231382 também estão no capítulo Parafusos e Porcas (pág. 229).")
# 378 (faixas refletivas)
MANUAIS.add(378)
N(378, "9822154", "FAIXA 3M LATERAL ESQUERDA", [27, 92, 270, 140], marca="3M")
N(378, "9821464", "FAIXA 3M LATERAL DIREITO", [345, 92, 552, 140], marca="3M")
N(378, "9822155", "FAIXA 3M PARA CHOQUE 10X2,40M", [40, 195, 240, 316], marca="3M", info="10 x 2,40M")
N(378, "7070003", "FAIXA ISOFLEX LATERAL ESQUERDA", [27, 580, 195, 610], marca="Isoflex", variacoes="@7073")
N(378, "7070001", "FAIXA ISOFLEX LATERAL DIREITA", [318, 580, 555, 610], marca="Isoflex", variacoes="@7071")
N(378, "7070002", "FAIXA ISOFLEX PARA CHOQUE 10X2,40M", [27, 690, 215, 795], marca="Isoflex", variacoes="@7072",
  info="10 x 2,40M | Comprimento 120CM LD + 120CM LE | Total 240CM")
NOTAS.append("Pág. 378: as faixas Avery Dennison (original Randon) aparecem só com as marcações '@17' (lado direito), '@18' (lado "
             "esquerdo) e '@19' (para-choque 2,4), sem código interno; não foram incluídas.")
# 379
MANUAIS.add(379)
N(379, "50928000", "BOCA GRANELEIRO RANDON UNIVERSAL", [20, 135, 293, 360], montadora=RD, info="Ferro | Com trava de segurança resistente")
N(379, "50928002", "BOCA GRANELEIRO GUERRA UNIVERSAL", [293, 160, 572, 375], montadora=GU)
N(379, "5660512", "MOLA A BICA RANDON TP ALFINETE", [20, 382, 210, 425], montadora=RD + ", " + GU)
_CINF = ("Valor por metro | Corrente soldada para uso geral, não calibrada, indicada apenas para amarração; não utilizar para "
         "elevação de cargas, pessoas e/ou animais | Aço de baixo carbono, baixa resistência à abrasão | Tratamento zincado "
         "branco, resistente à oxidação/corrosão")
for _c, _d in [("6013218", "CORRENTE ZINCADA BRANCA 3,2MM 1/8"), ("6014532", "CORRENTE ZINCADA BRANCA 4,0MM 5/32"),
               ("6016514", "CORRENTE ZINCADA BRANCA 6,5MM 1/4"), ("6018516", "CORRENTE ZINCADA BRANCA 8,0MM 5/16"),
               ("6019538", "CORRENTE ZINCADA BRANCA 9,5MM 3/8"), ("6016515", "CORRENTE 6,5MM 1/4 ZB LONGO METRO")]:
    N(379, _c, _d, [290, 545, 560, 800], _titulo="CORRENTE ZINCADA BRANCA", _nao_agrupar=False, card=50, info=_CINF, tipo="CORRENTE")
NOTAS.append("Pág. 379: a mola a bica 5660512 também está na pág. 376 (mesma peça).")
# 380 (conexões de latão)
MANUAIS.add(380)
for _c, _d, _r in [("7995302", "NIPLE CANO COMPL. COMPRES. B15 MACHO MEDIDA INTERNA 15 MM", [20, 85, 296, 190]),
                   ("7998302", "NIPLE CANO COMPRES. B18 MACHO MEDIDA INTERNA 18 MM", [296, 85, 572, 190]),
                   ("7995202", "NIPLE CANO COMP ASSENT C15 FEMEA MEDIDA INTERNA 13 X 15 MM", [20, 190, 296, 280]),
                   ("7998202", "NIPLE CANO COMP ASS ASSENT RC C18 FEMEA MEDIDA INTERNA 18 X15", [296, 190, 572, 280]),
                   ("7996100", "PORCA ENCAN. COMPRSSOR 26 MM", [20, 280, 296, 364]),
                   ("7992102", "PORCA SOBREPOSTA 22 X 1,5 TUBO 15", [296, 280, 572, 364]),
                   ("7990461", "ANILHA CANO COMPRES.", [20, 364, 296, 460])]:
    N(380, _c, _d, _r)
_OL = [("9988005", "08MM", "05MM"), ("9981005", "10MM", "05MM"), ("9981008", "10MM", "08MM"), ("9980337", "10MM", "06MM"),
       ("9980336", "10MM", "07MM"), ("9981179", "12MM", "3/8"), ("9981205", "12MM", "05MM"), ("9981211", "12MM", "11MM"),
       ("9981212", "12MM", "06MM"), ("9982253", "12MM", "07MM"), ("9980064", "12MM", "1/2"), ("9982252", "13MM", "10MM"),
       ("9981309", "13MM", "10MM"), ("9981346", "13MM", "12MM"), ("9981308", "14MM", "3/8"), ("9980012", "14MM", "06MM"),
       ("9982250", "14MM", "08MM"), ("9981620", "14MM", "10MM"), ("9982257", "14MM", "11MM"), ("9982254", "14MM", "12MM"),
       ("9980750", "16MM", "3/8"), ("9980751", "16MM", "05MM"), ("9982255", "16MM", "07MM"), ("9982256", "16MM", "10MM"),
       ("9981611", "16MM", "11MM"), ("7711612", "16MM", "12MM"), ("9981638", "3/8", "16MM")]
for _c, _pf, _esp in _OL:
    N(380, _c, f"OLHAL PF {_pf} ESPIGAO {_esp}", [50, 469, 176, 517], _titulo="OLHAL (ESPIGÃO)", _nao_agrupar=False, card=50,
      tipo="OLHAL")
N(380, "9980752", "OLHAL P/ MANGUEIRA 1/2", [50, 469, 176, 517], _titulo="OLHAL (ESPIGÃO)", _nao_agrupar=False, card=50, tipo="OLHAL",
  info="Na lista, a linha de 7711612 termina em 'P/' e a de 9980752 traz só 'MANGUEIRA 1/2'")
for _c, _d in [("9980817", "08 X 17 3 FUROS"), ("9981871", "10 X 20 DIESEL"), ("9981872", "12 X 24 DIESEL"), ("9980016", "1/2"),
               ("9980873", "14 X 25 DIESEL"), ("9980874", "16 X 30 DIESEL"), ("9980197", "16 X 45 DIESEL DUPLO"),
               ("9981832", "18 X 32 3 FUROS"), ("9982645", "26 X 45 3 FUROS"), ("9982240", "22 X 40 4 FUROS")]:
    N(380, _c, "PARAFUSO OCO " + _d, [332, 523, 470, 613], _titulo="PARAFUSO OCO", _nao_agrupar=False, card=51, tipo="PARAFUSO OCO")
NOTAS.append("Pág. 380: na lista de olhais as descrições estão quebradas entre linhas a partir de 9981212; foram remontadas como "
             "'OLHAL PF <furo> ESPIGAO <medida>'. Conferir 7711612 / 9980752 (P/ MANGUEIRA 1/2).")
# 381
MANUAIS.add(381)
MB, SC = "Mercedes-Benz", "Scania"
_R = [85, 224, 326, 418, 520, 654, 805]
_X = [20, 200, 380, 571]


def g(i, j):
    return [_X[j], _R[i], _X[j + 1], _R[i + 1]]


N(381, "4601166", "ARRUELA COBRE CONICA 4 X 10", [20, 85, 233, 224], tipo="ARRUELA")
N(381, "9981873", "CHUMBO LACRE FURADO BOMBA INJETORA", [233, 85, 378, 224], montadora=SC + ", " + MB, tipo="CHUMBO LACRE")
N(381, "4601508", "GRAMPO DUPLO BICO MERCEDES", [378, 85, 571, 224], montadora=MB, tipo="GRAMPO")
for _c, _d in [("4601984", "ARR. COBRE 14 X 20"), ("4601589", "ARR. COBRE 9,5 X 1 X 20"), ("4601169", "ARR. COBRE 9,5X 2 X 20"),
               ("4601167", "ARR. COBRE CUMINS 7,4X15X1,8"), ("4601168", "ARR. COBRE MAX 7,4X15X1,4")]:
    N(381, _c, _d, [210, 250, 270, 320], _titulo="ARRUELA COBRE", _nao_agrupar=False, card=50, tipo="ARRUELA", marca="G460")
for _c, _d in [("4601070", "CALCO BICO AÇO 0,10X3,15X7,0"), ("461570", "CALCO BICO AÇO 0,15X3,15X7,0"),
               ("4602070", "CALCO BICO AÇO 0,20X3,15X7,0"), ("4602570", "CALCO BICO AÇO 0,25X3,15X7,0"),
               ("4603602", "CALCO BICO PKS 4,4X15,0X0,20"), ("4600360", "CALCO BICO PKS 4,4X15,0X0,25")]:
    N(381, _c, _d, [505, 260, 565, 320], _titulo="CALCO BICO AÇO", _nao_agrupar=False, card=51, tipo="CALÇO", marca="G460")
N(381, "9981957", "PRESILHA BATENTE LIMITADOR FUMAÇA BCH SCANIA", g(2, 0), montadora=SC, tipo="PRESILHA")
N(381, "9980296", "JUNTA TAMPA VALVULA SCANIA 110/112 CB", g(2, 1), montadora=SC, tipo="JUNTA")
N(381, "9980301", "JUNTA ADMISSAO OM364/366A ACO", g(2, 2), montadora=MB, tipo="JUNTA")
N(381, "5063814", "MB TORRE CAMBIO MOD/ALUM ALTA", g(3, 0), montadora=MB, cod_ref="345.260.3814", tipo="TORRE DE CÂMBIO")
N(381, "9981802", "TAMPA ANTI-FILTRO SCANIA DIVERSOS", g(3, 1), montadora=SC, tipo="TAMPA")
N(381, "5067038", "MB CABECOTE FILTRO COMB 1620", g(4, 1), montadora=MB, cod_ref="3760907038", tipo="CABEÇOTE DE FILTRO")
N(381, "9980917", "ESPACADOR TAMPA VÁLVULA SCANIA124", g(4, 2), montadora=SC, tipo="ESPAÇADOR")
N(381, "5060072", "MB PORCA C/COLAR EIXO ENTALHADO", g(5, 0), montadora=MB, cod_ref="345 262 00 72", tipo="PORCA",
  aplicacao="L 1313/2213/0362/1111/OH352/G32 PC")
N(381, "5064121", "MB PORCA PONTEIRA CARDAN AUTOTRAVANTE 32 X 1,5MM 1620", g(5, 1), montadora=MB, tipo="PORCA")
N(381, "5060272", "MB PORCA MANGA D'EIXO FREIO A AR (40)", g(5, 2), montadora=MB, cod_ref="360 332 02 72", tipo="PORCA",
  aplicacao="OF 1313/1513/1518/L1620 PC")
NOTAS.append("Pág. 381: 9981873 (chumbo lacre) aparece duas vezes na página; 5060272 tem o código impresso em preto.")
for _r in ADD:
    if _r["descricao"].startswith("QUEBRA DEDO"):
        _r["tipo"] = "QUEBRA-DEDO"
