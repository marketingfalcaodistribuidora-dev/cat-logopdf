# Capítulo 10 - Bolsas e Amortecedores Cabine (págs. 84-121) — leitura visual card a card
# Tabelas "REFERÊNCIAS BINS" são imagens de baixa resolução: registrados os campos legíveis;
# números de referência só quando legíveis com segurança (marcados "lido da tabela-imagem").
MANUAIS = {86} | set(range(89, 111))
LR = "Ref. original lida da tabela-imagem de baixa resolução (conferir)"


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


def B(codigo, desc, tipo, label, bins_ref, montadora, aplicacao="", posicao="", cod_ref="", componentes="", extra="", lr=False):
    info = " | ".join(x for x in (
        f"Ref. BINS {bins_ref}" if bins_ref else "", f"Posição: {posicao}" if posicao else "",
        f"Componentes: {componentes}" if componentes else "", extra, LR if lr else "") if x)
    return R(r(codigo, desc, tipo, variacoes=label, cod_ref=cod_ref, montadora=montadora, aplicacao=aplicacao,
               info=info, marca="BINS"))


MB = "Mercedes-Benz"
TIPOS = [
    (r"VALV", "VÁLVULA NIVELADORA"), (r"MOLA GAS|GAS BAGAGEIRO", "MOLA GÁS"), (r"FOLE", "FOLE PNEUMÁTICO"),
    (r"BUCHA", "BUCHA SUSPENSÃO PNEUMÁTICA"), (r"PINO", "PINO EXCÊNTRICO"),
    (r"HELI", "MOLA HELICOIDAL / AMORTECEDOR CABINE"), (r"AMORT", "AMORTECEDOR CABINE"),
    (r"CABINE|CABINA|BANCO|CAB", "BOLSA CABINE (MOLA PNEUMÁTICA)"),
    (r"SUSP|EIXO|BASE|TRAC|GOMOS|ESTAB|QUINTA", "BOLSA SUSPENSÃO (MOLA PNEUMÁTICA)"), (r"MOLA", "BOLSA (MOLA PNEUMÁTICA)"),
]
AJ = {
    "88.0": {"cod_ref": "", "info": "", "marca": "Suspentech", "tipo": ""},
    # ---------------- pág. 84 (amortecedores / bolsas de cabine BINS) ----------------
    "84.1": B("4018001", "BINS AMORT ST 173 SF CABINE ACTROS PNEU DIANT", "AMORTECEDOR CABINE", "ST 173 SF / 499.0173", "Mp0001", MB,
              "Mercedes-Benz Actros 2010 a 2020 (exceção Novo Actros)", "Dianteiro",
              "9428905319 / 9428905919 / OEM A9438903819", "ST 173 B", "BINS: 0800.0001 | Logo Actros"),
    "84.2": B("4018002", "BINS AMORT ST 174SF CABINE ACTROS PNEU TRAS", "AMORTECEDOR CABINE", "ST 109SF (rótulo no card)", "Mp0002", MB,
              "Actros 2644 / 2646 / 2648 / 2651 / 2653 / 2655 / 3340 / 4144 - Axor 2533 / 2540 / 2541", "Traseiro",
              "942 890 6119", "AC0002 + CA0002", "Conjunto pneumático da suspensão da cabine | Logo Actros", lr=True),
    "84.3": B("4018147", "BINS AMORT CABINE ACCELO DIANT 0801.0047", "AMORTECEDOR CABINE", "", "Ac0047", MB,
              "Atego 2423 / 2425 / 2428 / 2429", "Dianteiro", "", "", "Amortecedor da cabine dianteiro | Código BINS 0801.0047 | Logo Accelo"),
    "84.4": B("4018213", "BINS AMORT ST 012 CABINE SC SERIE4 PNEU TRAS", "BOLSA CABINE", "ST 012", "Ca0013", "Scania",
              "Série 4 CP / CR / CT - Série PGRT CP / CG / CR / CT", "Dianteiro / Traseiro", "", "",
              "Câmara de ar do conjunto pneumático da cabine"),
    "84.5": B("4018017", "SCBINS AMORT ST 219 CABINE SCANIA PNEU TRAS", "BOLSA CABINE", "ST 219", "Ca0017", "Scania",
              "Série \"5\" PGRT CB / CR / CR19", "Traseiro", "", "", "Câmara de ar do conjunto pneumático da cabine"),
    "84.6": B("4018216", "BINS AMORT CABINE SCANIA S4 PNEU DIANT/TRAS", "BOLSA CABINE", "ST 174B", "Ca0016", "Scania",
              "Série 4 - Série PGRT", "Dianteiro / Traseiro", "", "", "Câmara de ar do conjunto pneumático da cabine"),
    "84.7": B("4017536", "BINS AMORT ST 374ES CABINE SCANIA PNEU DIANT", "AMORTECEDOR CABINE", "ST 374 ES", "Mp0036", "Scania",
              "Série 6 CR / CG / CP", "Dianteiro", "", "AC0043 + CA0021", "Conjunto pneumático da suspensão da cabine"),
    "84.8": B("4018143", "BINS AMORT ST 375ES CABINE SÉRIE6 PNEU DIANT", "AMORTECEDOR CABINE", "ST 375 ES", "Ac0043", "Scania",
              "Série 6 CR / CG / CP", "Dianteiro", "2613648", "", "Código BINS 0801.0043"),
    "84.9": B("4018021", "BINS AMORT ST 374 B CABINE SCANIA PNEU DIANT", "BOLSA CABINE", "ST 374 B", "Ca0021", "Scania",
              "Série 4 CR / CG / CT - Série PGRT CG / CR / CT", "", "", ""),
    "84.10": B("4018026", "BINS AMORT ST 232 ES CABINE FH PNEU TRAS", "AMORTECEDOR CABINE", "ST 232 ES", "Mp0026", "Volvo",
               "FH 420 / 460 / 500 / 540 2015 em diante", "Traseiro", "", "", "Conjunto pneumático da suspensão da cabine"),
    "84.11": B("4018517", "BINS AMORT ST 309 ES CABINE VM HELICOD TRAS", "AMORTECEDOR CABINE", "ST 309 ES", "Mh0017", "Volvo",
               "VM 210 / 220 / 240 / 260 / 270 / 310 / 330 todos os anos", "Traseiro", "20504055 / 20712988 / 20908742", "",
               "Conjunto helicoidal da suspensão da cabine | Código BINS 8050017", lr=True),
    "84.12": B("4017509", "BINS AMORT ST117 CABINE FH P DIANT 3975.0009", "AMORTECEDOR CABINE", "ST 117", "Mp0009", "Volvo",
               "FH 400 / 440 / 480 / 500 / 520 2004-2014 - FM 380 / 400 / 440 / 480 / 500 2004-2014", "Dianteiro", "",
               "AC0009 + CA0009", "Conjunto pneumático da suspensão da cabine"),
    # ---------------- pág. 85 ----------------
    "85.1": B("4018133", "BINS AMORT ST 308I CABINE VM PNEU DIANT", "AMORTECEDOR CABINE", "ST 3081", "Ac0033", "Volvo",
              "VM 210 / 220 / 240 / 260 / 270 / 310 / 330 todos os anos", "Dianteiro", "", "", "Amortecedor de cabine"),
    "85.2": B("4018218", "BINS AMORT ST 243 B CABINE FH PNEU DIANT", "BOLSA CABINE", "ST 243 B", "Ca0018", "Volvo",
              "FH 420 / 460 / 500 / 540 2015 em diante", "Dianteiro", "", "", "Câmara de ar do conjunto pneumático da cabine"),
    "85.4": B("4017114", "BINS REP ST 853K MOLA STARA PNEU", "BOLSA SUSPENSÃO", "ST 853 K / 499.0853", "AS0014.C", "Randon",
              "Carretas Randon / Suspensys", "", "", "", "Reposição da mola pneumática"),
    "85.5": B("4017204", "BINS REP ST 016 K MOLA EIXOS HBZ PNEU", "BOLSA SUSPENSÃO", "ST 016 K / 499.0016", "AS0004.SB",
              "Randon, Guerra, Noma", "Carretas Guerra / HBZ / Randon / Suspensys / Silpa / Trik Eixos", "", "", "",
              "Reposição de mola pneumática | Logos Randon / Suspensys"),
    "85.7": B("4017202", "BINS REP ST 144 K MOLA FACCHINI PNEU", "BOLSA SUSPENSÃO", "ST 144 K / 499.0144", "AS0002.SB", "Facchini",
              "Carretas Facchini 2006 - 2007 / Vanderleia 2008 em diante", "", "", "", "Reposição de mola pneumática"),
    "85.8": B("4017213", "BINS REP ST 035 K MOLA FACCHINI PNEU", "BOLSA SUSPENSÃO", "ST 035 K / 499.0035", "AS0013.SB",
              "Facchini, Randon", "Facchini / HBZ / Randon", "", "", "", "Reposição de mola pneumática | Código BINS 41.720.013"),
    "85.10": R(r("4010127", "BUCHA SUSPENSAO BINS PNEUMATICA CAR FACCHINI", "BUCHA SUSPENSÃO PNEUMÁTICA",
                 cod_ref="0308190702 / 0368132201 / 345 320 8144", variacoes="BINS 4180.0127 / IABV 3146 / Thor 13038 / 13070 / 2536-0 / 2536-A-0",
                 aplicacao="Carretas Facchini", montadora="Facchini", marca="BINS",
                 info="Ref. BINS Cm0127 | Bucha de suspensão pneumática | Código BINS 41.800.127")),
    "85.11": R(r("4984507", "4507 PINO EXCENTRICO SUSP PENU FACCHINI", "PINO EXCÊNTRICO", cod_ref="0368146601",
                 variacoes="Mesma TH - 50904092 / Cód. 4507", montadora="Facchini",
                 aplicacao="Bucha da suspensão a ar / Carreta Facchini com suspensão a ar e suspensão KLL",
                 info="Pino excêntrico da suspensão pneumática compatível Facchini | Embalagem 01 | Material SAE 1020 | Corpo 31,5mm x compr. total 283mm x cabeça 80mm x rosca 1\" 8 FPP | Não acompanha porca",
                 foto_spec={"rect": [444, 715, 556, 760]}),
               r("3740001", "PORCA TR UNC I 1\"", "PORCA", info="Porca indicada para o pino excêntrico 4984507",
                 foto_spec={"rect": [440, 772, 470, 798]})),
}


def P86(card, codigo, desc, tipo, rect, montadora="", info="", cod_ref=""):
    return dict(pagina=86, card=card, codigo=codigo, descricao=desc, tipo=tipo, foto_spec={"rect": rect},
                montadora=montadora, info=info, cod_ref=cod_ref, marca="BINS")


ADD = [
    P86(1, "4010852", "ST852 MOLA PNEUM SUSP EIXO 2 GOMOS VOLVO BINS", "BOLSA SUSPENSÃO", [60, 104, 160, 224], "Volvo"),
    P86(2, "4011890", "ST189K MB MOLA PNEU S/BAS TRA.TERCE EIXO BINS", "BOLSA SUSPENSÃO", [247, 106, 336, 217], MB),
    P86(3, "4010307", "ST307K BINS MOLA PNEUM S/BASE SUSP CARRET KLL", "BOLSA SUSPENSÃO", [440, 104, 524, 222]),
    P86(4, "4010038", "ST038K BINS MOLA PNEU S/BASE SUSP EIXO TRAC", "BOLSA SUSPENSÃO", [67, 290, 161, 407]),
    P86(5, "4013011", "AMORT BINS ATRON TRAS TODOS 1215 695 326 0000", "AMORTECEDOR SUSPENSÃO", [212, 284, 385, 407], MB,
        "Amortecedor de suspensão | Logo Atron", "695 326 0000"),
    P86(6, "4013012", "AMORT BINS ATEGO DIANT 1315 688 323 0300", "AMORTECEDOR SUSPENSÃO", [403, 292, 563, 395], MB,
        "Amortecedor de suspensão | Logo Atego", "688 323 0300"),
    P86(7, "4013033", "AMORT BINS VM TDS - FM 6X4 DIANT 1629405", "AMORTECEDOR SUSPENSÃO", [33, 446, 193, 611], "Volvo",
        "Amortecedor de suspensão", "1629405"),
]
NOTAS = [
    "Cap. 10: as tabelas 'REFERÊNCIAS BINS' estão no PDF como imagens de ~120 px; campos de texto foram transcritos, números de referência só quando legíveis (marcados para conferência).",
    "p85 cards 3, 6 e 9: cards só com logo (Volvo, Randon, Facchini).",
]


# ---------------- págs. 89-110: Suspentech (faixas horizontais; texto e foto extraídos da faixa) ----------------
def F(pag, card, codigo, y0, y1, x0=25, x1=570, montadora="", **kw):
    d = dict(pagina=pag, card=card, codigo=codigo, faixa=[x0, y0, x1, y1], montadora=montadora, marca="Suspentech",
             fonte_titulo=17)
    d.update(kw)
    return d


V, SC, MBZ, IV = "Volvo", "Scania", "Mercedes-Benz", "Iveco"
ADD += [
    F(89, 1, "4990022", 88, 262, montadora=V), F(89, 2, "4990025", 262, 450, montadora=V),
    F(89, 3, "4990400", 450, 632, montadora=V), F(89, 4, "4990098", 632, 805, montadora=V),
    F(90, 1, "4990072", 88, 265, montadora=V), F(90, 2, "4990080", 265, 455, montadora=V),
    F(90, 3, "4990081", 455, 635, montadora=V), F(90, 4, "4990082", 635, 805, montadora=V),
    F(91, 1, "4990184", 88, 265, montadora=V), F(91, 2, "4991840", 265, 445, montadora=V),
    F(91, 3, "4990186", 445, 590, montadora=V), F(91, 4, "4990234", 590, 685, montadora=V, fonte_titulo=16),
    F(91, 5, "4990309", 685, 805, montadora=V, descricao="ST309ES VOLVO CJ MOLA HELI CABINE DIANT TRAS"),
    F(92, 1, "4992340", 88, 265, montadora=V), F(92, 2, "4990235", 265, 445, montadora=V),
    F(92, 3, "4990046", 445, 628, montadora=V), F(92, 4, "4990460", 628, 805, montadora=V),
]


def F2(pag, card, pares, y0, y1, x0=25, x1=570, **kw):
    """Faixa com 2 produtos (ex.: com base / sem base): mesma foto e textos, títulos próprios."""
    return [F(pag, card, c, y0, y1, x0, x1, descricao=d, **kw) for c, d in pares]


SCN = dict(montadora=SC)
ADD += [
    F(93, 1, "4990232", 88, 200, montadora=V), F(93, 2, "4990407", 200, 297, montadora=V),
    F(93, 3, "4990398", 297, 396, montadora=V), F(93, 4, "4990061", 396, 494, montadora=V, fonte_titulo=15.5),
    *F2(93, 5, [("4990064", "St064 MOLA PNEUM TRACAO VOLVO DIANT MAIOR"), ("4990640", "ST064K MOLA PNEUM S/BASE VOLVO DIANT MAIOR")],
        494, 655, montadora=V),
    *F2(93, 6, [("4990038", "St038 MOLA PNEU COMP SUSP EIXO TRAC TER EIXO"), ("4990380", "ST038K MOLA PNEU S/BASE SUSP EIXO TRAC TER EX")],
        655, 805, montadora="Volvo, Ford, Volkswagen"),
    *F2(94, 1, [("4991370", "St137 MOLA PNEUM COMPL TRACAO VOLVO"), ("4990137", "ST137K MOLA PNEUM S/BASE VOLVO 2004 2014")],
        88, 282, montadora=V),
    *F2(94, 2, [("4990230", "St230 VOLVO MOLA PNEU COMP SUSP EIXO TRACAO"), ("4992300", "ST230K VOLVO MOLA PNEU S/BASE SUSP EIX TRACAO")],
        282, 456, montadora=V),
    *F2(94, 3, [("4992290", "ST229K VOLV MOLA PNEU S/BASE SUSP EIXO TRACAO"), ("4990229", "St229 VOLVO MOLA PNEU COMP SUSP EIXO TRACAO")],
        456, 640, montadora=V),
    F(94, 4, "4990366", 640, 805, montadora=V),
    F(95, 1, "4990089", 88, 242, montadora="Volvo, Iveco"),
    F(95, 2, "4994048", 242, 383, montadora=V, descricao="ST4048 FOLE PNEU SUSP EIXO DIANT/TRAS VOLVO B",
      cod_ref="8127152 / 6882797", variacoes="Firestone 950009 / 20 / Contitech FD 200-19 S / Goodyear 8325", fonte_titulo=12),
    F(96, 1, "4990012", 88, 262, 25, 295, descricao="St012 MOLA PNEUM CABINE TRAS S4", fonte_titulo=14, **SCN),
    F(96, 2, "4990013", 88, 262, 295, 570, descricao="St013 SCANIA MOLA PNEU CABINE TRAS SERIE 3T", fonte_titulo=14, **SCN),
    F(96, 3, "4990014", 262, 447, 25, 295, descricao="St014 SCANIA MOLA PNEU CABINE TRAS SERIE 3R", fonte_titulo=14, **SCN),
    F(96, 4, "4990015", 262, 447, 295, 570, descricao="St015 MOLA PNEUM CABINE S4", fonte_titulo=14, **SCN),
    F(96, 5, "4990414", 447, 630, 25, 295, descricao="ST414 CONJ MOLA PNEU CABINE SCANIA S6", fonte_titulo=14, **SCN),
    F(96, 6, "4990413", 447, 630, 295, 570, descricao="ST413 CONJ MOLA PNEU CABINE SCANIA", fonte_titulo=14, **SCN),
    F(97, 1, "4990125", 88, 212, **SCN), F(97, 2, "4990130", 212, 310, **SCN), F(97, 3, "4990171", 310, 418, **SCN),
    F(97, 4, "4990374", 418, 552, **SCN), F(97, 5, "4993740", 552, 685, **SCN), F(97, 6, "4990375", 685, 805, **SCN),
    F(98, 1, "4990211", 88, 198, **SCN), F(98, 2, "4990218", 198, 302, **SCN), F(98, 3, "4990219", 302, 408, **SCN),
    F(98, 4, "4990304", 408, 545, **SCN), F(98, 5, "4990002", 545, 672, **SCN), F(98, 6, "4990139", 672, 805, **SCN),
]
NOTAS += ["p96 card 7: card só com o logo Scania.", "p95 cards 4-6: espaços vazios."]

IVC = dict(montadora=IV)
MBB = dict(montadora=MBZ)
ADD += [
    F(99, 1, "4990209", 88, 250, **SCN), F(99, 2, "4990376", 250, 403, **SCN),
    F(99, 3, "4990001", 403, 545, descricao="ST001SF AMORT SCANIA PNEU CABINE DIANT S4",
      info="Código interno não impresso neste card; código do índice Suspentech (p.88)", **SCN),
    F(99, 4, "4990037", 545, 665, **SCN), F(99, 5, "4990213", 665, 805, **SCN),
    F(100, 1, "4990172", 88, 203, **SCN),
    *F2(100, 2, [("4990017", "St017 MOLA PNEUM COMPL TRACAO S4"), ("4990170", "ST017K MOLA PNEUM S/BASE TRACAO S4/S5")], 203, 355, **SCN),
    *F2(100, 3, [("4990030", "St030 SCANIA MOLA PNEU COMP SUP TERC EIXO"), ("4990300", "ST030K SCANIA MOLA PNEU S/BASE SUP TERC EIXO")], 355, 540, **SCN),
    F(100, 4, "4990320", 540, 673, descricao="ST032BSE BASE MOLA PNEUM S/BASE S5", tipo="BASE MOLA PNEUMÁTICA",
      info="LANÇAMENTO 25/03", fonte_titulo=11, **SCN),
    *F2(100, 5, [("4993200", "St032 MOLA PNEUM SCANIA SÉRIE 5 E 6 -2010"), ("4990032", "ST032K MOLA PNEUM S/BASE S5")], 673, 805,
        fonte_titulo=11, **SCN),
    F(101, 1, "4990360", 88, 268, **IVC), F(101, 2, "4990036", 268, 450, **IVC),
    F(101, 3, "4990420", 450, 633, **IVC), F(101, 4, "4990042", 633, 805, **IVC),
    F(102, 1, "4990337", 88, 222, **IVC), F(102, 2, "4990297", 350, 480, montadora="Volkswagen"),
    F(102, 3, "4990108", 480, 633, montadora="Volkswagen"), F(102, 4, "4990109", 633, 805, montadora="Volkswagen"),
    F(103, 1, "4991730", 88, 257, **MBB), F(103, 2, "4991173", 257, 448, **MBB),
    F(103, 3, "4990253", 448, 630, **MBB), F(103, 4, "4992530", 630, 805, **MBB),
    F(104, 1, "4991740", 88, 245, **MBB),
    F(104, 2, "4991890", 245, 415, variacoes="Kit reposição: OEM A9423280001 / Firestone 950504 / Contitech 4390 / Goodyear 9507", **MBB),
    *F2(104, 3, [("4990455", "ST455 MOLA MB PNEUM COMPLETA S/SENSOR TER EIX"), ("4994550", "ST455K MOLA MB PNEUM COMPLETA S/SENSOR TER EIX")],
        415, 585, fonte_titulo=11, **MBB),
    F(104, 4, "4991173", 585, 703, descricao="St173 SF CONJ MOLA PNEUM MB ACTROS DIANT", variacoes="BINS 401.8001",
      fonte_titulo=10, **MBB),
    F(104, 5, "4990107", 703, 805, descricao="ST107SF CONJ MB MOLA HELICOIDAL CABINE TRAS", fonte_titulo=10, **MBB),
]
NOTAS += ["p102: espaço vazio entre os cards ST337SF e ST297SF.",
          "p99 card ST001SF: código interno não impresso; vinculado ao código 4990001 do índice Suspentech (p.88)."]

ADD += [
    F(105, 1, "4990106", 88, 220, **MBB), F(105, 2, "4990174", 220, 345, **MBB), F(105, 3, "4990703", 345, 495, **MBB),
    F(105, 4, "4990292", 495, 647, montadora="Librelato", variacoes="Rodofort"),
    F(105, 5, "4990878", 647, 805, descricao="ST878 MOLA PNEUM ESTAB QUINTA RODA S/RETORNO", info="Dolly"),
    *F2(106, 1, [("4990352", "St352 MB MOLA PNEU COMPLETA SUSP EIXO"), ("4993520", "ST352K MB MOLA PNEU S/BASE SUSP EIXO")],
        88, 260, fonte_titulo=14, **MBB),
    *F2(106, 2, [("4990207", "St207 MB MOLA PNEU COMP TRACAO TERC EIXO"), ("4992070", "ST207K MB MOLA PNEU S/BASE TRACAO TERC EIXO")],
        260, 445, fonte_titulo=14, **MBB),
    F(106, 3, "4990338", 445, 633, 25, 290, descricao="St338 K MOLA PNEUM MB AXOR/ ACTROS-SEM SENSOR", fonte_titulo=12, **MBB),
    F(106, 4, "4994008", 445, 633, 290, 570, descricao="ST4008 FOLE PNEU SUSP EIXO DIANT MERCEDES", info="LANÇAMENTO 03/25",
      tipo="FOLE PNEUMÁTICO", fonte_titulo=11.5, **MBB),
    F(106, 5, "4990056", 633, 805, 25, 290, descricao="St056 TODOS CONJ COMP VALV NIVELADORA 1/4 NPT", fonte_titulo=11.5),
    F(106, 6, "4990216", 633, 805, 290, 570, descricao="ST216K ACTROS/AXOR MOLA TERCEIRO EIXO", info="LANÇAMENTO 03/25",
      fonte_titulo=11.5, **MBB),
]

FAC = dict(montadora="Facchini")
RAN = dict(montadora="Randon")
ADD += [
    *F2(107, 1, [("4990144", "ST144K MOLA PNEUM SUSP FACCHINI VANDERLEIA"), ("4991440", "St144 MOLA PNEU COMP SUSP FACCHINI VANDERLEIA")],
        88, 235, variacoes="BINS 401.7202", fonte_titulo=14.5, **FAC),
    F(107, 2, "4990142", 235, 353, 25, 300, descricao="ST142K MOLA FACCHINI PNEU S/BASE SUSP EIXOLA", fonte_titulo=11, **FAC),
    F(107, 3, "4993900", 235, 353, 300, 570, descricao="ST039K SUSPENTECH MOLA PNEU C/SUP FACCHINI / HBZ / TRÊS EIXOS",
      fonte_titulo=11, **FAC),
    F(107, 4, "4990870", 353, 485, 25, 300, descricao="ST870 MOLA PNEU FACCHINI/RODOFORT", fonte_titulo=11, **FAC),
    F(107, 5, "4990822", 353, 485, 300, 570, descricao="ST822 MOLA PNEUM SUSP EIXO 2 GOMOS FACCHINI", fonte_titulo=11, **FAC),
    F(107, 6, "4990829", 485, 633, 25, 300, descricao="St829 MOLA PNEUM SUSP EIXO 2 GOMOS FACCHINI", fonte_titulo=11, **FAC),
    *F2(107, 7, [("4990086", "ST086 MOLA PNEUM FACCHINI C/BASE"), ("4998600", "ST086K MOLA PNEUM FACCHINI S/BASE")],
        485, 633, 300, 570, fonte_titulo=10.5, **FAC),
    F(107, 8, "4990035", 633, 805, descricao="ST035K MOLA PNEUM FACCHINI / AGRÍCOLA / INDUS", variacoes="Equivalente BINS: 4017213",
      fonte_titulo=13, **FAC),
    *F2(108, 1, [("4990353", "St353 RANDON MOLA PNEU COMPLETA SUSP EIXO"), ("4993530", "ST353K RANDON MOLA PNEU S/BASE SUSP EIXO")],
        88, 260, fonte_titulo=13, **RAN),
    F(108, 2, "4990853", 260, 445, descricao="St853 MOLA PNEUM SUSP EIXO 2 GOMOS", variacoes="Equivalente BINS: 4017114",
      fonte_titulo=14, **RAN),
    *F2(108, 3, [("4990160", "St016 MOLA PNEUM COMPL 4 PINO RANDON"), ("4990016", "ST016K MOLA PNEUM RANDON S/BASE 4 PINOS")],
        445, 630, variacoes="BINS 401.7204", fonte_titulo=14, **RAN),
    F(108, 4, "4990866", 630, 805, descricao="St866 FOLE PNEUM SUSP JOST / RANDON",
      variacoes="Equivalente BINS: 4017120 / Equivalente Jarflex: 4960866", fonte_titulo=14.5, montadora="Randon, Jost"),
]

ADD += [
    *F2(109, 1, [("4990307", "St307 MOLA PNEUM COM BASE SUSP CARRETA KLL"), ("4993070", "ST307K MOLA PNEUM S/BASE SUSP CARRETA KLL")],
        88, 260, fonte_titulo=13, montadora="Noma, Randon",
        info="Obs.: o quadro do card repete o texto do ST 016 / ST 016 K (Randon / Suspensys / Noma / Ibero, base inferior)"),
    *F2(109, 2, [("4990143", "St143 MOLA PNEUM COM BASE SUSP GUERRA"), ("4991430", "ST143K MOLA PNEUM S/BASE SUSP GUERRA")],
        260, 445, fonte_titulo=13, montadora="Guerra"),
    F(109, 3, "4990840", 445, 630, montadora="Randon, Guerra", fonte_titulo=13),
    F(109, 4, "4990852", 630, 805, montadora="Volvo, Randon, Guerra", fonte_titulo=13),
    F(110, 1, "4994000", 88, 260, descricao="St4000 FOLE PNEUM SUSP EIO DIANT 334 X 224", variacoes="Equivalente Jarflex: 4964000",
      info="6.13", fonte_titulo=14, **RAN),
    F(110, 2, "4994001", 260, 445, descricao="St4001 FOLE PNEUM 3 EIXO 380 MM X 225 MM", info="7.14", fonte_titulo=14, **RAN),
    F(110, 3, "4994002", 445, 630, descricao="St4002 FOLE PNEUM SUSP DIANT 380 X 195 MM", variacoes="Equivalente Jarflex: 4964002",
      info="7.15", fonte_titulo=14, **RAN),
    *F2(110, 4, [("4990045", "St045 MOLA PNEUM COM BASE SUSP RANDON"), ("4990450", "ST045K MOLA PNEUM S/BASE SUSP RANDON")],
        630, 805, fonte_titulo=13, montadora="Randon"),
]
NOTAS += ["p110: o card lista ST045K antes de St045, mas os códigos seguem o índice da p.88 (4990045 = ST045 com base; 4990450 = ST045K sem base).",
          "p109: o quadro do card ST307/ST307K repete o texto do ST016 (provável erro de diagramação do catálogo)."]

MANUAIS |= {111}
ADD += [
    F(111, 1, "4990353", 88, 262, descricao="ST353 RANDON MOLA PNEU COMPLETA SUSP EIXO", fonte_titulo=15, montadora="Randon"),
    F(111, 2, "4990861", 262, 445, descricao="ST861 MOLA PNEUM SUSP A AR", fonte_titulo=15, montadora="Noma"),
]
_S = dict(marca="Suspentech")
AJ.update({
    "112.1": dict(montadora="Scania", **_S), "112.2": dict(montadora="Scania", **_S), "112.3": dict(montadora="Scania", **_S),
    "112.4": dict(montadora="Volvo", **_S), "112.5": dict(montadora="Volvo", **_S), "112.7": dict(montadora="Volvo", **_S),
    "112.8": dict(montadora="Volvo", **_S), "112.9": dict(montadora="Volvo", **_S),
    "112.10": R(r("4990342", "ST342 ES - CONJ MOLA HELICOIDAL CAB TRAS", "MOLA HELICOIDAL / AMORTECEDOR CABINE",
                  cod_ref="BC45-5C398-BA", aplicacao="Cabine leito 2011 a 2019 / Compatível: Ford Cargo", montadora="Ford", **_S)),
})
AJ.update({"113.1": dict(montadora="Randon", tipo="AMORTECEDOR SUSPENSÃO"),
           "113.2": dict(montadora="DAF", **_S), "113.3": dict(montadora="DAF", **_S)})

# págs. 114-115: Continental / pág. 116: Firestone (cards simples, lidos automaticamente)
for _c in range(1, 13):
    for _pg in (114, 115, 116):
        AJ.setdefault(f"{_pg}.{_c}", {})["ref_oem"] = True
    AJ.setdefault(f"114.{_c}", {}).setdefault("marca", "Continental")
    AJ.setdefault(f"115.{_c}", {}).setdefault("marca", "Continental")
    AJ.setdefault(f"116.{_c}", {}).setdefault("marca", "Firestone")
_MONT = {"114.1": SC, "114.2": SC, "114.3": SC, "114.4": "Randon, Noma", "114.5": "Randon", "114.6": "Randon",
         "114.7": "Randon", "114.8": MBZ, "114.9": MBZ, "114.10": MBZ, "114.11": V, "114.12": "Guerra",
         "115.1": "Facchini", "115.2": "Facchini", "115.3": "Facchini", "115.4": "Facchini", "115.5": "Facchini",
         "115.6": "Facchini", "115.7": "Randon", "115.8": "Facchini", "115.9": "", "115.10": "Facchini",
         "115.11": "Guerra", "115.12": "Randon",
         "116.1": "Randon", "116.2": "Facchini", "116.3": "Facchini", "116.4": SC, "116.5": V, "116.6": "Randon",
         "116.7": "", "116.8": "", "116.9": V, "116.10": V, "116.11": V, "116.12": IV}
for _k, _m in _MONT.items():
    if _m:
        AJ[_k]["montadora"] = _m
NOTAS += ["Págs. 114-116: cada card traz o código Continental/Firestone e as referências OEM; o código Continental/Firestone fica na descrição e as referências em Informações adicionais."]

MANUAIS |= {118, 119}
JF = dict(marca="Jarflex")
ADD += [
    F(118, 1, "4960866", 88, 228, descricao="St866 FOLE PNEUM SUSP JOST / RANDON", variacoes="Equivalente BINS: 4017120 / Suspentech: 4990866",
      tipo="FOLE PNEUMÁTICO", fonte_titulo=20, montadora="Randon, Jost", **JF),
    F(118, 2, "4964000", 228, 378, descricao="St4000 FOLE PNEUM SUSP EIO DIANT 334 X 224", variacoes="Equivalente Suspentech: 4994000",
      tipo="FOLE PNEUMÁTICO", info="6.13", fonte_titulo=20, montadora="Randon", **JF),
    F(118, 3, "4964001", 378, 518, descricao="St4001 FOLE PNEUM 3 EIXO 380 MM X 225 MM", variacoes="Equivalente Suspentech: 4994001",
      tipo="FOLE PNEUMÁTICO", info="7.14", fonte_titulo=20, montadora="Randon", **JF),
    F(118, 4, "4964002", 518, 646, descricao="St4002 FOLE PNEUM SUSP DIANT 380 X 195 MM", variacoes="Equivalente Suspentech: 4994002",
      tipo="FOLE PNEUMÁTICO", info="7.15 | O quadro do card repete o texto do ST 866", fonte_titulo=16, montadora="Randon", **JF),
    F(118, 5, "4994003", 646, 805, descricao="ST4003 FOLE PNEU SUSP EIXO ENCAIXE 380 X 260", tipo="FOLE PNEUMÁTICO",
      cod_ref="Volvo OEM A6953270001 / Jost AD00115J00 / 70000109236",
      variacoes="Firestone 950532 / 290-3 / Goodyear 8077",
      aplicacao="Caminhões Volvo (linha pesada, trucks e carretas), Mercedes-Benz (OEM A6953270001), carretas com suspensores Jost (OEM AD00115J00 / 70000109236)",
      info="7.14 | Dimensões: 555x380x260mm", fonte_titulo=18, marca="Suspentech", montadora="Jost, Volvo, Mercedes-Benz"),
    F(119, 1, "4960714", 88, 175, 25, 297, descricao="CJ SUSPENSOR 7.14 SR STANDAR", tipo="CONJUNTO SUSPENSOR",
      info="Conjunto suspensor 7.14 semirreboque STD completo", fonte_titulo=14, **JF),
    F(119, 2, "4960940", 88, 175, 297, 570, descricao="BASE SUSPENSOR REBAIXADO 940MM", tipo="BASE SUSPENSOR",
      info="Base suspensor 7.14 SR rebaixado", fonte_titulo=14, **JF),
    F(119, 3, "4967140", 175, 352, 25, 297, descricao="4421.000 - CJ SUSPENSOR 7.14 TK E SR MENOR", tipo="CONJUNTO SUSPENSOR",
      cod_ref="4421.000", fonte_titulo=13.5, **JF),
    F(119, 4, "4960700", 175, 352, 297, 570, descricao="4206.900 - TAMPA SUSPENSOR 700MM", tipo="TAMPA SUSPENSOR",
      cod_ref="4206.900", fonte_titulo=12, **JF),
    F(119, 5, "4964030", 352, 540, 25, 297, descricao="FLANGE 6.13 ROSCA M16 X 1,5 C/FURO MOD JOST - PARTE SUP", tipo="FLANGE SUSPENSOR",
      info="Fole pequena | Aplica-se ao fole 496.4000 6.13", fonte_titulo=99, montadora="Jost", **JF),
    F(119, 6, "4964500", 352, 540, 297, 570, descricao="FLANGE 7.14 ROSCA M16 X 1,5 C/FURO MOD JOST - PARTE SUP", tipo="FLANGE SUSPENSOR",
      info="Fole grande | Aplica-se aos foles 496.4001 7.14 e 496.4002 7.15", fonte_titulo=99, montadora="Jost", **JF),
    F(119, 7, "4964031", 540, 720, 25, 297, descricao="4030.002 - FLANGE 6.13 SEM FURO PARA BUJÃO - PARTE INF", tipo="FLANGE SUSPENSOR",
      cod_ref="4030.002", aplicacao="Flanges para suspensor pneumático", info="LANÇAMENTO", fonte_titulo=99, **JF),
    F(119, 8, "4964501", 540, 720, 297, 570, descricao="4500.003 - FLANGE 7.14 SEM FURO PARA BUJÃO - PARTE INF", tipo="FLANGE SUSPENSOR",
      cod_ref="4500.003", aplicacao="Flanges para suspensor", info="LANÇAMENTO", fonte_titulo=99, **JF),
]

MANUAIS |= {120, 121}
_KIT = ("Válvula acionamento 1/4\" (1 un); válvula descarga rápida 1/2\" x 1/4\" (1 un); manômetro 1/8\" NPT x 40 mm (1 un); "
        "conector macho rosca 1/4\" x tubo 1/4\" (1 un); conector macho rosca 1/2\" x tubo 1/4\" (1 un); bujão 1/4\" (1 un); "
        "cotovelo macho rosca 1/4\" x tubo 1/4\" (1 un); conector T macho 1/4\" NPT x fêmea 1/8\" x tubo 1/4\" (1 un); "
        "niple reto M16 x 1/4\" (1 un); inserto tubo 1/4\" (4 un); tubo nylon 1/4\" x 1,00 mm (8 m); parafuso sex RP UNC 3/16\" x 2\" (3 un); "
        "porca sex 3/16\" UNC CH 5/16\" (3 un); bucha espaçadora válv. acionamento (3 un)")
ADD += [
    F(120, 1, "4960885", 95, 342, 34, 561, descricao="CJ SUSPENSOR 6.13 TRUCK MB1513 -S/GRAMP 850MM", tipo="CONJUNTO SUSPENSOR",
      info="Medidas 560 / 280 / 520 / 850 | Obs.: bolsa pneumática 6.13 | Suspensor truck chassi até 860 mm reto", fonte_titulo=99,
      montadora=MBZ, marca="Jarflex"),
    F(120, 2, "4963805", 342, 455, 34, 561, descricao="SUPORTE SUSPENSOR FIXAÇÃO REBAIXO 110MM", tipo="SUPORTE SUSPENSOR",
      info="18X27MM", fonte_titulo=99, marca="Jarflex"),
    F(120, 3, "4960451", 455, 790, 34, 561, descricao="KIT PNEUMÁTICO SUSPENSOR DO TERCEIRO EIXO TRUCK", tipo="KIT PNEUMÁTICO SUSPENSOR",
      info="Rosca 1/4\" - tubo Ø 1/4\" | Itens: " + _KIT, fonte_titulo=99, marca="Jarflex"),
]
_C121 = [(25, 307), (307, 570)]


def C121(card, codigo, desc, tipo, lin, col, **kw):
    ys = [(150, 284), (284, 400), (400, 522), (522, 610), (610, 805)]
    (x0, x1), (y0, y1) = _C121[col], ys[lin]
    d = dict(pagina=121, card=card, codigo=codigo, descricao=desc, tipo=tipo, faixa=[x0, y0, x1, y1], fonte_titulo=99)
    d.update(kw)
    return d


ADD += [
    C121(1, "5118859", "MOLA AMORT CABINE TRAS VOLVO FH/FM TODOS", "MOLA HELICOIDAL / AMORTECEDOR CABINE", 0, 0, cod_ref="3198859", montadora=V),
    C121(2, "5118836", "MOLA AMORT DIANT VOLVO FH/FM 2004 ...", "MOLA HELICOIDAL / AMORTECEDOR CABINE", 0, 1, cod_ref="3198836",
         variacoes="Códigos similares: 21111925, 1075355, 8158197", montadora=V),
    C121(3, "5118971", "AMORTECEDOR CABINE VOLVO FH13", "AMORTECEDOR CABINE", 1, 0, cod_ref="22128971",
         aplicacao="New FH - Novo FH 2015 a 2020", montadora=V),
    C121(4, "5118849", "AMORT VOLVO HORI CABINE FH/FM ( ST 063 SF )", "AMORTECEDOR CABINE", 1, 1, cod_ref="3198849", montadora=V),
    C121(5, "5110540", "AMORT BOLSA DIANT IVECO CABINE STRALIS", "AMORTECEDOR CABINE", 2, 0, cod_ref="504080540", montadora=IV),
    C121(6, "5110241", "AMORT BOLSA TRAS IVECO CABINE STRALIS", "AMORTECEDOR CABINE", 2, 1, cod_ref="504060241",
         aplicacao="Stralis 380 410 420 440 460 480", montadora=IV),
    C121(7, "5112103", "AMORTECEDOR CABINE HORIZONTAL TRASEIRO MB AXOR", "AMORTECEDOR CABINE", 3, 0, cod_ref="9583172103",
         aplicacao="MB Axor 1933 2035 2040 2044 2533 2535 2536 2540 2640 2644 3340 3344 4140 4144", montadora=MBZ,
         faixa=[25, 522, 307, 805]),
    C121(8, "5119348", "AMORT VOLVO GRADE FRONTAL FH12 ( ST 098 )", "MOLA GÁS", 3, 1, montadora=V),
    C121(9, "5119668", "BARRA VOLVO ESTABILIZADORA CABINE 1629668", "BARRA ESTABILIZADORA CABINE", 4, 1, cod_ref="1629668", montadora=V),
]
NOTAS += ["p121: as duas células superiores da página estão vazias no catálogo.",
          "p117 e p122: páginas de capa (Jarflex / Filtro), sem produtos."]
