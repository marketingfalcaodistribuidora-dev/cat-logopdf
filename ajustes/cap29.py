# Capítulo 29 - Peças Volkswagen e Ford (págs. 386-391; 386 = divisória)
# Cards em grade: código vermelho + descrição + aplicação; "REF ORIG" no canto superior; logo da montadora no card.
import re

from cards_grade import ler

TIPOS = [(r"BUCHA", "BUCHA"), (r"JUNTA|JG\b", "JUNTA"), (r"PEDAL", "PEDAL"), (r"RETENTOR", "RETENTOR"),
         (r"RESERVAT[OÓ]RIO|RESERV\b", "RESERVATÓRIO"), (r"MANGUEIRA", "MANGUEIRA"), (r"BATENTE", "BATENTE"),
         (r"KIT", "KIT"), (r"ABRA[CÇ]ADEIRA", "ABRAÇADEIRA"), (r"MANCAL", "MANCAL"), (r"COXIM", "COXIM"),
         (r"CAPA", "CAPA"), (r"ARRUELA", "ARRUELA"), (r"BORRACHA", "BORRACHA"), (r"PORCA", "PORCA"),
         (r"SUPORTE", "SUPORTE"), (r"FLEX[IÍ]VEL", "FLEXÍVEL"), (r"TUB[OI]\b", "TUBO"), (r"BASE", "BASE"),
         (r"COIFA", "COIFA"), (r"TAMPA", "TAMPA"), (r"V[AÁ]LVULA", "VÁLVULA"), (r"FILTRO", "FILTRO"),
         (r"PARAFUSO", "PARAFUSO"), (r"ISOLAD", "ISOLADOR")]
AJ = {}
ADD = []
NOTAS = ["Págs. 387-391: o número original da montadora (REF ORIG) está na coluna de referência."]
MANUAIS = set(range(386, 392))
VW = "Volkswagen"
_REF = re.compile(r"^(?:REF(?:\.|\s*ORIG(?:INAL)?)?\s*:?\s*)?((?:[A-Z]\s?)?\d{2,3}(?:[ .]\d{2,4}){2,4}(?:-\d+)?)\s+")

for _p in range(387, 392):
    for _r in ler(_p):
        info = _r.get("info", "")
        m = re.search(r"REF(?:\.|\s*ORIG(?:INAL)?)?\s*:\s*([\w. \-/]+?)(?:\s*\||$)", info)
        if m and not _r["cod_ref"]:
            _r["cod_ref"] = m.group(1).strip()
            info = (info[:m.start()] + info[m.end():]).strip(" |")
        if not _r["descricao"]:
            _r["descricao"] = re.split(r"\s+\|\s+", info)[0].strip()
            info = " | ".join(re.split(r"\s+\|\s+", info)[1:])
        _r["info"] = info.strip(" |")
        _r["montadora"] = VW
        ADD.append(_r)


def F(p, c, **kw):
    regs = [r for r in ADD if r["pagina"] == p and r["codigo"] == c]
    assert regs, f"{c} não está na pág. {p}"
    for r in regs:
        r.update(kw)


def D(p, c, d, **kw):
    F(p, c, descricao=d, **kw)


def S(p, c, d, ref=None, apl=None, **kw):
    """Descrição, referência original e aplicação transcritas do card."""
    kw["descricao"] = d
    if ref is not None:
        kw["cod_ref"] = ref
    if apl is not None:
        kw["aplicacao"] = apl
    kw.setdefault("info", "")
    F(p, c, **kw)


MB = "Mercedes-Benz"
# 387 (pág. impressa 386): jogos de juntas de turbina e juntas VW
S(387, "9023103", "JUNTA TURBINA JOGO CHAPA OM352A OM366A/LA", montadora=MB)
S(387, "9023174", 'JUNTA TURBINA "JOGO" MBB 709/912 (TURBOS BIAGGIO)', montadora=MB)
S(387, "9023171", 'JUNTA TURBINA "JOGO" OM364A/LA 710/712/912/914', montadora=MB)
S(387, "9023089", 'JUNTA TURBINA "JOGO" CHAPA PEQUENA OM352A OM366A/LA', info="Chapa", montadora=MB)
S(387, "9023090", 'JUNTA TURBINA "JOGO" COBRE (VOLVO N/NL12) OM355A / OM447 (SC 110/111)',
  info="O card traz o selo 'CHAPA' e a descrição diz 'Cobre'", montadora="Mercedes-Benz, Volvo, Scania")
S(387, "9023092", 'JUNTA TURBINA "JOGO" COBRE (VOLVO N/NL12) OM355A / OM447 (SC 110/111)', info="Cobre",
  montadora="Mercedes-Benz, Volvo, Scania")
S(387, "9023095", 'JUNTA TURBINA "JOGO" CHAPA OM449 (SC 112/113) (VV N/NL10)', montadora="Mercedes-Benz, Scania, Volvo")
S(387, "9023183", "JUNTA BASE TURBINA", montadora="")
F(387, "4664889", cod_ref="", variacoes="48.898 PAK-CV", montadora=MB)
F(387, "4660041", descricao="JG JUNTA TURBINA MBB OM-352A / 366A LACON / GARRET", montadora=MB)
F(387, "4667426", descricao="JG JUNTA TURBINA VOLVO N/NL-12 / B-12 TODOS", variacoes="74.260-CV", cod_ref="6889541", montadora="Volvo")
F(387, "4664863", descricao="JUNTA COMPRESSOR DE AR MODERNO MERCEDES BENZ BR-400 - OM - 447 / 449", cod_ref="", variacoes="48633 PP",
  montadora=MB)
S(387, "5015215", "JUNTA BASE TURBINA MWM 229/4 TURBO - CHAPA", "2R0145215", "VW 7110S")
S(387, "5015455", "JUNTA BASE TURBINA MWM X10 - CHAPA", "TAF145453", "7110/7120/8120/8140/8150/9150")
S(387, "5013484", "JUNTA TAMPA VALVULA MWM MOTOR X10 4/6CILINDROS", "TAE103483", "F12000/14000")
S(387, "5013483", "JUNTA TAMPA VALVULAS FINA BORRACHA P/ MWM 229/3/4/6", "T11103483", "F12000/14000")
S(387, "5013485", "JUNTA TAMPA VALVULA CUMMINS MOTOR SERIE B 5.9L - VOLKS", "2RL103483A", "12.170BT/13.170/13.190/14.170BT")
S(387, "5015453", 'JUNTA TURBINA "JOGO" MWM X10 "04 CILINDROS"', "TAF145453", "VW 7.110/7.120/8.120/8.140/8.150",
  info="Impresso como 'JJUNTA'")
S(387, "5013136", "JUNTA TUBO CURVA AR ADMISSAO TURBINA", "2RE253135", "7.120/8.120/8.140/8.150/9.150...")
S(387, "5010079", "PARAFUSO COXIM TRAS CABINA VW", "2TA899369", info="Descrição impressa como imagem (transcrita)")
S(387, "5013135", 'JUNTA TURBINA "JOGO" MWM X10 "06 CILINDROS"', "2RD253135", "VW 13.180/14.150/14.200/15.180")
NOTAS.append("Pág. 387: 5015455 e 5015453 trazem a mesma referência impressa (TAF145453); 4664889, 4660041, 4667426 e 4664863 "
             "também estão na pág. 384 (cap. Peças Mercedes-Benz).")
# 388 (pág. impressa 387)
for _c, _d, _ref, _apl in [
        ("5010078", "PEDAL ACELERADOR ALCA ABERTA", "T00721507C", ""), ("5010077", "PEDAL ACELERADOR ALCA FECHADA", "T00721507", ""),
        ("5010066", "RETENTOR EIXO S-5009", "TE3607029", ""), ("5010070", "BUCHA TRAMBULADOR CAMBIO VW", "TJG11549", ""),
        ("5010075", "RESERVATORIO OLEO EMBREAGEM VW", "2RD721441", "")]:
    S(388, _c, _d, _ref, _apl, info="Descrição impressa como imagem (transcrita)")
for _c, _d, _ref, _apl in [
        ("5015467", "MANGUEIRA LIGACAO TURBINA 62X90MM SILICONE VERMELHO", "2RK145467", "VW 14.220/16.220/24.220/26.220"),
        ("9011710", "SEMI-CASQUILHO BARRA TORCAO SUSPENSAO CABINE", "2Z0.513.371", "VW DELIVERY/5.140/8.150/8/9.150E"),
        ("5019717", "JUNTA TUBO COLETOR AR ADMISSAO ENTRADA", "2TA129717", "7.100/7.120/8.100/8.120/8.140/150"),
        ("5012166", "BUCHA AMORT.D CABINE CONSTELLATION", "2R2.899.541", "VW 13.180E 15.180E 17.250 19.320.."),
        ("5012168", "BUCHA AMORT. T CABINE CONSTELLATION", "2R2.899.542", "VW 13.180E 15.180E 17.250 19.320.."),
        ("5013001", "BUCHA MOLA SUSP DIANT/TRAS VW 6.90/7.90", "TJG.899.441", "VW 6.90/7.90/7.110/11.130/14.210"),
        ("5013288", "BUCHA AMORT. CABINE CONSTELLATION", "2R2.899.542A", "VW 17.250 19.320 24.250 26.260..."),
        ("5012179", "BUCHA AMORTECEDOR SUSPENSAO PNEUMATICA", "2Z0.513.371", "VW 18310 TITAN 17240OT/18310OT"),
        ("5012178", "BUCHA SUP. AMORT. DI CONSTELLATION", "TAC.413.435", "VW 12.140H/12.140T/12.170BT/..."),
        ("5012177", "BATENTE SUSP. DIANTEIRO CONSTELLATION", "TAP.411.1111", "VW 7.100/7.110/7.120/8.100/."),
        ("10004029", "BUCHA PONTE MANCAL TRAVAMENTO CABINE", "600.899.397", "VW 7.90 ATE 14140"),
        ("5012188", "BUCHA AMORT. TRAZ VW CONSTELLATION", "TJG.413.435B", "VW 12140/5300 BUS16180/210"),
        ("10009294", "BUCHA SUSPENSAO CABINE BI-PARTIDO", "2R0.805.244", "14150/13190/13180/13170E"),
        ("10001635", "BATENTE CABINE TRASEIRO", "600.899.425", "VW 6.90/11.130/13.130 (R-264)"),
        ("10001664", "BATENTE CABINE APOIO", "600.899.313A", "VW 7.90S/7.110S/11.130/11.140/"),
        ("9011666", "BUCHA MANCAL ESTABILIZADOR TRASEIRO (32 MM)", "600.511.421", "VW 6.90/7.90")]:
    S(388, _c, _d, _ref, _apl)
# 389 (pág. impressa 388)
for _c, _d, _ref, _apl in [
        ("5013287", "BUCHA AMORT. SUP CABINE CONSTELLATION", "2R2.899.542A", "VW 13.180E 15.180E 17.250 19.320..."),
        ("5013301", "KIT SUP. BARRA BASC C CONSTELLATION", "2R0.805.244", "14150/13190/13180/13170E"),
        ("5010056", "BUCHA TIRANTE BARRA ESTABILIZADOR DIANTEIRO (INF)", "2SL.411.071A", "VW 12.140H/12.170BT/12.180"),
        ("5010057", "BUCHA BARRA ESTABILIZADORA DIANTEIRO", "TAR.411.041", "VW 12140H/12170BT/12180/13170/"),
        ("5013296", "BATENTE SUP D CABINE CONSTELLATION", "2R2.899.177", "VW 13.180E 15.180E 17.250 19.320..."),
        ("9020910", "BUCHA TIRANTE BARRA ESTABILIZADOR DIANT.SUPERIOR", "2SL.411.071", "VW 12.140H/12.170BT/12.180"),
        ("5010058", "ABRACADEIRA BARRA ESTAB DIANTEIRO", "TAR.411.053", "VW 12.140H/12.170BT/12.180/"),
        ("5010060", "MANCAL ABRACADEIRA ESTAB. TRASEIRA", "T16.511.319", "12.140H/12.170BT/12.140T/12.180/"),
        ("5010061", "ISOLAD.BARRA ESTAB. TRASEIRA", "TJG.511.413", "VW 12140 ATE 16220 BUS 16180"),
        ("5013300", "BUCHA PARTE TRAZ MOTOR CONSTELLATION", "2S2199382-A / 2VG199381 / 611200127700.0", ""),
        ("5013122", "COXIM CABINE PARTE DIANTEIRO VW", "TJG899607",
         "80/7.100/7.120/8.100/8.120/8.140/8.150/8.150E/12.140H/12.140T/12"),
        ("5013091", "COXIM CABINE PARTE TRASEIRA VW", "2RD899397", "VW TODOS"),
        ("9020911", "BUCHA AMORTECEDOR DIANT. INFERIOR FURO 22MM", "T11.413.441A", "VW 6.90 ATE 16210"),
        ("9011728", "BUCHA AMORTECEDOR C/TUBO DIANTEIRO", "T06.513.441", "7100/7110/7120/790S/8140/8150"),
        ("9020922", "BUCHA AMORTECEDOR C/TUBO DIANTEIRO SUPERIOR", "", "VW 12170 ATE 22160"),
        ("9010904", "ARRUELA AMORTECEDOR DIANTEIRO INFERIOR", "T11.413.431B", "VW 11.130/13.130/14.120"),
        ("9020918", "BUCHA TIRANTE BARRA ESTABILIZADORA DIANTEIRA", "T06.411.045", "VW 6.80/6.90/7.90/7.110"),
        ("9020310", "BORRACHA ESTABILIZADOR DIANTEIRO", "04.183.055", "VW 11.130/13.130"),
        ("9020317", "BUCHA OLHAL BARRA ESTABILIZ. DIANTEIRO (BORRACHA)", "T21.411.045", "13.130/14.210/16.170/16.220"),
        ("9020313", "BUCHA OLHAL BARRA ESTABILIZ. DIANTEIRO BI-PARTIDA BORRACHA", "T21.411.045", "13130/14210/16170/220 BUS16180")]:
    S(389, _c, _d, _ref, _apl)
S(389, "5068653", "CAPA PEDAL EMBREAGEM /FREIO", "",
  "Caminhão VW até 1994 680 / 690 / 790s / 7110s / 11130 / 11140 / 12140 / 12140H / 13130 / 14140 / 14150 / 14200 / 14210 / "
  "14220 / 16170 / 16210 / 16220 / 24220 / 24250 / 35300")
NOTAS.append("Pág. 389: 9020317 e 9020313 trazem a mesma referência impressa (T21.411.045).")
# 390 (pág. impressa 389)
for _c, _d, _ref, _apl in [
        ("9011669", "BUCHA MANCAL ESTABILIZADOR DIANTEIRO", "2S0.411.041A", "WORKER / 13.170E / 15.180E"),
        ("9011679", "BUCHA BORRACHA ESTABILIZADOR TRASEIRO", "", "MICRO 5140EOD/8140EOD/9150EOD"),
        ("9015156", 'PORCA CASTELO CUBO RODA DIANTEIRO 1"1/2-ROSCA 18G 5/16', "NF.385.602AB", "12180/14220/15170/18310"),
        ("9015212", "PORCA CARCACA EIXO (ROCKWELL)", "TJG.501.471", "14150/14200/16200/210/35300"),
        ("5010053", "SUPORTE BARRA ESTABILIZADORA DIANTEIRO", "2RG.411.049", "VW 12.140H/12.170BT/12.180/"),
        ("5010052", "BUCHA BATENTE SUSP. DIANTEIRO", "TGG411111", ""),
        ("5010059", "BUCHA AMORTECEDOR (48,0X25,0X24,0MM)", "TAC.413.435", "VW 12.140H/12.140T/12.170BT/..."),
        ("5010008", "FLEXIVEL RETORNO COMP. VW 7.10", "2RD121072", ""),
        ("5010011", "RESERVATORIO FLUIDO EMB.VW TOD", "2RD721441", ""),
        ("5010301", "TUBO INJ. 1º CIL. DELIVERY VW", "2P0130301", ""), ("5010004", "TUBO INJ. 1º CIL. MWM 7.100/8", "2RD130301", ""),
        ("5010001", "TUBO INJ. 2º CIL. DELIVERY VW", "2P0130302", ""), ("5010005", "TUBO INJ. 2º CIL. MWM 7.100/8", "2RD130302", ""),
        ("5010002", "TUBO INJ. 3º CIL. DELIVERY VW", "2P0130303", ""), ("5010006", "TUBO INJ. 3º CIL. MWM 7.100/8", "2RD130303", ""),
        ("5010003", "TUBO INJ. 4º CIL. DELIVERY VW", "2P0130304", ""), ("5010007", "TUBO INJ. 4º CIL. MWM 7.100/8", "2P0130304", ""),
        ("5014265", "BUCHA ESP. SUP CABINE CONSTELLAT", "", "")]:
    S(390, _c, _d, _ref, _apl)
F(390, "5010301", info="Impresso como 'TUBI INJ.'")
F(390, "0230365", montadora="Volkswagen, Ford", info="")
NOTAS.append("Pág. 390: textos dos cards impressos como imagem (transcritos); 5010007 traz a mesma referência do 5010003 "
             "(2P0130304); 5010011 e 5010075 (pág. 388) trazem a mesma referência (2RD721441).")
# 391 (pág. impressa 390)
for _r in ADD:
    if _r["pagina"] == 391 and _r["codigo"] == "5010013":
        _r.update(descricao='JUNTA TP VALV CUMMINS "B" 5.9L', cod_ref="TAE103483", montadora="Ford", info="", aplicacao="")
S(391, "5014262", "BASE V DES.VW MENOR CONSTELLATION")
S(391, "5014261", "BASE V DES.VW MAIOR CONSTELLATION")
S(391, "4660018", "JUNTA TAMPA VALVULAS FINA BORRACHA P/ MWM 229/3/4/6", "T12103483", "VW 71105/12140",
  info="Título do card: TAMPA VALV FINA BORR P/MWM 229", montadora="Ford, Volkswagen")
S(391, "4660348", "JUNTA TAMPA VALVULA MWM MOTOR X10 4/6CILINDROS", "TAE.103.483")
S(391, "4982224", "COIFA MARCHA VW 7.100/17.210", info="Impresso como '4982224 - 2224 COIFA MARCHA'")
S(391, "4660020", "JUNTA TAMPA VALVULAS (CORTICA FINA) P/MWM226/224", "T12.103.483", "VW TODOS")
S(391, "4663483", "JUNTA TAMPA VALVULAS (CORTICA GROSSA) P/MWM 229", "T11.103.483", "VW TODOS")
S(391, "5010015", "COXIM D.FIX.MOT. CUM. B/5.9L", "E5HT6038DA", montadora="Ford")
S(391, "4667119", "JG JUNTA TURBINA VOLKSWAGEM D-226 6 CILINDROS (CARACOL MAIOR)", "", variacoes="71198-CV")
S(391, "5015215", "JUNTA BASE TURBINA MWM 229/4 TURBO - CHAPA", "2R0145215", "VW 7110S")
S(391, "5064027", "TAMPA CUBO VW 8.150E/9.150E", "2RO407345B", info="65MM")
S(391, "4661426", "71.426B JUNTA TAMPA VALV MWM", "", variacoes="71826B", montadora="MWM")
S(391, "4661947", "71.947-PH JUNTA BOMBA HIDRAULICA MWM X-10", "", variacoes="71947PH", montadora="MWM")
S(391, "9981550", "VÁLVULA RETORNO BOMBA ALIMENTADORA MWM C/ESFERA", montadora="MWM")
S(391, "9982472", "FILTRO BOMBA MWM", montadora="MWM")
# fotos: recortes sem os textos/logos
for _p, _c, _rect in [(391, "5010013", [393, 93, 477, 159]), (391, "4982224", [42, 192, 189, 340]),
                      (391, "5064027", [37, 504, 120, 593]), (390, "0230365", [420, 296, 508, 354]),
                      (390, "5010004", [40, 502, 170, 560]), (390, "5010005", [400, 502, 545, 560]),
                      (390, "5010006", [215, 603, 352, 662]), (390, "5010003", [391, 603, 490, 657]),
                      (390, "5010007", [50, 703, 195, 760]), (390, "5010301", [397, 398, 497, 455]),
                      (390, "5010011", [212, 399, 292, 457])]:
    F(_p, _c, foto_spec={"rect": _rect})
NOTAS.append("Pág. 391: o código 5010013 aparece impresso duas vezes (no card da junta Cummins e, solto, no card da base 5014261); "
             "5015215 repete a pág. 387; 9981550 também está no cap. Peças Mercedes-Benz (pág. 382).")
