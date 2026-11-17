# Capítulo 28 - Peças Mercedes-Benz (págs. 382-385)
# Cards em grade: código vermelho + descrição; nº original da Mercedes no canto superior direito.
import re

from cards_grade import ler

TIPOS = [(r"BUCHA", "BUCHA"), (r"TRAVA", "TRAVA"), (r"PARAFUSO|\bPF\b", "PARAFUSO"), (r"VALVULA|VÁLVULA", "VÁLVULA"),
         (r"REP\.?\b|REPARO", "REPARO"), (r"PENEIRA", "PENEIRA"), (r"ABRA[CÇ]ADEIRA|ABRAC", "ABRAÇADEIRA"),
         (r"ARRUELA", "ARRUELA"), (r"FECHO", "FECHO"), (r"TAMPA", "TAMPA"), (r"BORRACHA", "BORRACHA"),
         (r"JUNTA|JG\b", "JUNTA"), (r"TERMINAL", "TERMINAL"), (r"COTOVELO", "COTOVELO"), (r"PINO", "PINO"),
         (r"CILINDRO", "CILINDRO"), (r"BOMBA", "BOMBA"), (r"REGULADOR", "REGULADOR"), (r"FILTRO", "FILTRO"),
         (r"MANCAL", "MANCAL"), (r"ROLAMENTO|ROL\.", "ROLAMENTO"), (r"FLEXIVEL|FLEXÍVEL", "FLEXÍVEL"), (r"SUPORTE", "SUPORTE"),
         (r"LAMINA|LÂMINA", "LÂMINA"), (r"SINCRONIZADOR", "SINCRONIZADOR"), (r"CARDAN", "CARDAN"), (r"PUXADOR", "PUXADOR"),
         (r"BARRA", "BARRA"), (r"SOQUETE", "SOQUETE"), (r"ALAVANCA|ALAV\b", "ALAVANCA"), (r"ABRAC", "ABRAÇADEIRA")]
AJ = {}
ADD = []
NOTAS = ["Págs. 382-385: o número original Mercedes-Benz de cada peça (canto do card) está na coluna de referência."]
MANUAIS = set(range(382, 386))
MB = "Mercedes-Benz"
_REF = re.compile(r"^(?:REF(?:\.|\s*ORIG(?:INAL)?)?\s*:?\s*)?((?:[A-Z]\s?)?\d{2,3}(?:[ .]\d{2,4}){2,4}(?:-\d+)?)\s+")

for _p in range(382, 386):
    for _r in ler(_p):
        info = _r.get("info", "")
        m = re.search(r"REF(?:\.|\s*ORIG(?:INAL)?)?\s*:\s*([\w. \-/]+?)(?:\s*\||$)", info)
        if m and not _r["cod_ref"]:
            _r["cod_ref"] = m.group(1).strip()
            info = (info[:m.start()] + info[m.end():]).strip(" |")
        if not _r["descricao"]:
            m = _REF.match(info)
            if m:
                _r["cod_ref"] = " / ".join(x for x in (_r["cod_ref"], m.group(1)) if x)
                info = info[m.end():]
            _r["descricao"] = re.split(r"\s+\|\s+", info)[0].strip()
            info = " | ".join(re.split(r"\s+\|\s+", info)[1:])
        else:
            m = _REF.match(info + " ")
            if m:
                _r["cod_ref"] = " / ".join(x for x in (_r["cod_ref"], m.group(1)) if x)
                info = info[m.end():]
        _r["info"] = info.strip(" |")
        _r["montadora"] = MB
        ADD.append(_r)


def F(p, c, **kw):
    regs = [r for r in ADD if r["pagina"] == p and r["codigo"] == c]
    assert regs, f"{c} não está na pág. {p}"
    for r in regs:
        r.update(kw)


def D(p, c, d, **kw):
    F(p, c, descricao=d, **kw)


# 382: referências no canto do card que não foram lidas
for _c, _ref in (("9980039", "000.091.0039"), ("5426062", "026 586 01707"), ("5426063", "345 070 02 66"),
                 ("5426162", "345 070 01 66"), ("5420186", "496 078 01 86")):
    F(382, _c, cod_ref=_ref)
F(382, "9987207", descricao="REP. BOMBA ALIMENTADORA COPO/ELEM. 9941080044 OM 314/321/326/352/352A/355", cod_ref="344 586 72 07")
F(382, "5060009", info="3,75mm | Original")
F(382, "9981550", montadora="MWM")
# 383: descrições impressas como imagem (transcritas)
for _c, _d in [("5060142", "MB ABRAC FILTRO AR 1620 ORIGIN"), ("5060006", "MB TAMPA LAT TRAMBULADOR 1113"),
               ("5067165", "MB BORRACHA VALV INSP PEQ 366"), ("5061405", "MB BOR VALV INSP FILTRO 1620"),
               ("5066906", "MB TAMPA FILTRO ALUM 1935/41"), ("5060912", "MB TAMPA FILTRO AR PLAS 1620"),
               ("5060764", "MB PINO ALGEMA CURTO DIANT.TRAS. 22X27MM L1113/1313/LPO PC"),
               ("5061039", "MB REGULADOR EMBREAGEM COMP 1313"), ("5060739", "MB REG.EMB COMP 175MM 1113"),
               ("5067035", "MB FLEX EMBR HID 217MM 1318 AO 1938"), ("5060732", "MB ALAV EMB BOOMERANGUE S/REBA"),
               ("5060136", "MB COTOVELO EMBR SUP NY 1620"), ("5060074", "MB PINO ALAV EMBREAGEM 1313/22"),
               ("5067089", "MB BARRA ESTABILIZADORA 330MM 1620"), ("5060020", "MB PUXADOR FREIO MAO MB TODOS"),
               ("5069090", "BOMBA MANUAL ALUMINIO MODERNA TODOS 2.447.010.033"),
               ("9981098", "BOMBA MANUAL LATÃO TAMPA NYLON TODOS"), ("5060126", "MB CILINDRO FREIO MOTOR 352/355 ROSC 12X1,75MM"),
               ("5066026", "MB CILINDRO FREIO MOTOR L1618/20/...")]:
    D(383, _c, _d)
F(383, "9981098", cod_ref="000 090 00 50")
F(383, "5060764", cod_ref="312 423 18 18")
_sp383 = [r for r in ADD if r["pagina"] == 383][0]
ADD.append(dict(_sp383, codigo="5067326", descricao="MB CILINDRO ACIONAMENTO FREIO MOTOR OM 352/355", cod_ref="3454307326",
                foto_spec={"rect": [212, 702, 380, 758]}, info="Código impresso como '506.7326'", card=90))
ADD.append(dict(_sp383, codigo="5061019", descricao="MB SOQUETE LAMPADA PAINEL ISOLADO", cod_ref="0005451019",
                foto_spec={"rect": [418, 710, 545, 768]}, info="Código impresso como '506.1019'", card=91))
NOTAS.append("Pág. 383: descrições impressas como imagem (transcritas); 5067326 e 5061019 estão impressos como '506.7326' e "
             "'506.1019'.")
# 384
for _c, _d in [("5067060", "MB FECHO INFERIOR CAPO 1113/2213"), ("5060162", "MB FECHO SUP CAPO ANTIGO HPN TODOS BICUDO"),
               ("5060262", "MB FECHO INF CAPO ANTIGO HPN TODOS BICUDO"),
               ("5060060", "MB FECHO INF CAPO MOD. TRAVA DEITADA HPN TODOS BICUDOS"),
               ("5060161", "MB FECHO SUP CAPO MODER HPN TODOS BICUDO"), ("5060146", "MB TERMINAL LONG 8MM HPN TODOS"),
               ("5060426", "MB TERMINAL 5MM"), ("7716090", "TERMINAL ACELERADOR 06 X 06"), ("7710222", "TERMINAL ACELERADOR 08 X 06"),
               ("7715146", "TERMINAL ACELERADOR 08 X 08")]:
    D(384, _c, _d)
F(384, "5060146", cod_ref="3649920422"); F(384, "5060426", info="05MM x 05MM")
F(384, "7716090", info="06MM x 06MM"); F(384, "7710222", info="06MM x 08MM"); F(384, "7715146", info="08MM x 08MM")
F(384, "4667426", descricao="JG JUNTA TURBINA VOLVO N/NL-12 / B-12 TODOS", variacoes="74.260-CV", cod_ref="6889541", montadora="Volvo")
F(384, "4664863", descricao="JUNTA COMPRESSOR DE AR MODERNO MERCEDES BENZ BR-400 - OM - 447 / 449", cod_ref="", variacoes="48633 PP")
F(384, "4664889", cod_ref="", variacoes="48.898 PAK-CV")
F(384, "5066203", info="10mm x 12mm | Mercedes todos", cod_ref="071805.016203")
_r384 = [r for r in ADD if r["pagina"] == 384][0]
ADD.append(dict(_r384, codigo="5060160", descricao="MB FECHO SUPERIOR CAPO 1113/2213", cod_ref="322.880.0160", card=90, info="Código impresso como '506 0160'",
                foto_spec={"rect": [392, 88, 480, 160]}, tipo="FECHO"))
for r in ADD:
    if r["pagina"] == 384 and r["codigo"].startswith("77"):
        r["montadora"] = ""
# 385
F(385, "5061102", descricao="MB BOR.ROL.CT.40MM 912+(VOLKS)", aplicacao="MB 709, 709-E, 712, 809, 812, 912, 914",
  info="Serve também: VW 6.80, 6.90, 7.90, 8.140, 7100, 7110, S13.130, 11160, 11130, L80, 8140CO/CE", montadora="Mercedes-Benz, Volkswagen")
F(385, "5061620", descricao="MB BOR.ROL.CT 45MM MB1620(VOLKS)",
  aplicacao="MB 1620, 1418, 1218, 1518, 1618, 2318, 2418, 1718, 1614, 1418-E, OF-1620",
  info="Serve também: VW 12.140H, 12.140T, 12.170BT, 14.150, 14.170BT, 14.200, 14.210, 14.220, 16.170, 16.170BT, 16.210, 16.220, "
       "16.300, 22.140, 22.160, 22.210, VW Ônibus 16.180", montadora="Mercedes-Benz, Volkswagen")
F(385, "5068512", descricao="MB BOR.ROL.CT.60MM IVECO VOLVO",
  aplicacao="Iveco: Cursor 450E37/819E31/Eurotech HM450E37/HM200E37 | MBB: 1632/1634/1938/2428/2638 | "
            "Volvo: N10/12/NL10/12/B10M/12/FM10/12/FH12/FM12/NH12", montadora="Volvo, Iveco, Mercedes-Benz")
F(385, "5061114", descricao="MB BOR.ROL.CT. 40MM INT 1113..", cod_ref="345.410.0051")
F(385, "5061091", descricao="ROLAMENTO CARDAN SCANIA 112/113 COM BORRACHA COM CAVA 55 MM", montadora="Scania",
  info="Descrição impressa como imagem (transcrita)")
F(385, "5063031", montadora="Scania")
F(385, "5067340", descricao="MB SUPORTE CARDAN 1113 A 2213", cod_ref="3454107340")
F(385, "5062932", descricao="MB FLEXIVEL BOMBA ALIMENT. FILTRO L 1113/1313/1513/2013/2213/608D ORIGINAL",
  variacoes="395MM (ref. 352 070 29 32) / INJETORA 453MM (ref. 352 070 30 32)", cod_ref="352 070 29 32 / 352 070 30 32",
  info="O código 5062932 aparece em dois cards da página (395MM e injetora 453MM)")
F(385, "9981807", montadora="Scania"); F(385, "9981839", montadora="Scania"); F(385, "9981808", montadora="Mercedes-Benz, Scania")
_r385 = [r for r in ADD if r["pagina"] == 385][0]
for _k, (_c, _d, _ref, _rect, _inf) in enumerate([
        ("5060140", "MB REP. SINCRONIZADOR 2A A 5A G3 50/60/61 PC", "337 262 01 40", [25, 410, 140, 470], ""),
        ("5060274", "MB REP. SINCRONIZADOR 1A E RE GE 50/60/61 PC", "337 262 02 74", [208, 408, 325, 462], ""),
        ("5065625", "MB REP. SINCRONIZADOR 1A/RE L 1111/1113/1513/O362/LPO PC", "322 260 56 25", [25, 502, 128, 566], ""),
        ("5068545", "MB REP. SINCRONIZADOR 2A A 5A L 1111/1113/1513/O362/LPO/I PC", "332 260 85 45", [208, 508, 318, 572], ""),
        ("5064032", "MB FLEX BOMBA INJ. AO FILTRO 483MM-OLHAL 14MM OM366/OM366A", "352 070 40 32", [30, 612, 205, 656],
         "Código impresso como '506 4032'")]):
    ADD.append(dict(_r385, codigo=_c, descricao=_d, cod_ref=_ref, card=90 + _k, info=_inf, aplicacao="", variacoes="",
                    foto_spec={"rect": _rect}, montadora=MB))
NOTAS.append("Pág. 385: os códigos dos sincronizadores (5060140, 5060274, 5065625, 5068545) e do 5064032 estão impressos em preto "
             "junto da descrição; 5062932 aparece em dois cards (flexível 395MM e injetora 453MM) e foi lançado uma vez com as duas medidas.")
