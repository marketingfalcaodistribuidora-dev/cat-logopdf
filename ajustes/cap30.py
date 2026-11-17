# Capítulo 30 - Peças Scania (págs. 392-395; 392 = divisória)
# Cards em grade: código vermelho + descrição + aplicação; "REF ORIG" no canto superior; logo da montadora no card.
import re

from cards_grade import ler

TIPOS = [(r"BUCHA", "BUCHA"), (r"JUNTA|JG\b", "JUNTA"), (r"PEDAL", "PEDAL"), (r"RETENTOR", "RETENTOR"),
         (r"RESERVAT[OÓ]RIO|RESERV\b", "RESERVATÓRIO"), (r"MANGUEIRA", "MANGUEIRA"), (r"BATENTE", "BATENTE"),
         (r"KIT", "KIT"), (r"ABRA[CÇ]ADEIRA", "ABRAÇADEIRA"), (r"MANCAL", "MANCAL"), (r"COXIM", "COXIM"),
         (r"CAPA", "CAPA"), (r"ARRUELA", "ARRUELA"), (r"BORRACHA", "BORRACHA"), (r"PORCA", "PORCA"),
         (r"SUPORTE", "SUPORTE"), (r"FLEX[IÍ]VEL", "FLEXÍVEL"), (r"TUB[OI]\b", "TUBO"), (r"BASE", "BASE"),
         (r"COIFA", "COIFA"), (r"TAMPA", "TAMPA"), (r"V[AÁ]LVULA", "VÁLVULA"), (r"FILTRO", "FILTRO"),
         (r"PARAFUSO", "PARAFUSO"), (r"ISOLAD", "ISOLADOR"), (r"LAMINA", "LÂMINA"), (r"CHAVETA", "CHAVETA"), (r"CABE[CÇ]OTE", "CABEÇOTE"),
         (r"COPO", "COPO"), (r"REPARO", "REPARO"), (r"BOIA", "BOIA"), (r"ESTICADOR", "ESTICADOR"), (r"TRAVA", "TRAVA"),
         (r"CANO", "CANO"), (r"ARRUELA", "ARRUELA")]
AJ = {}
ADD = []
NOTAS = ["Págs. 393-395: o número original da montadora (REF ORIG) está na coluna de referência."]
MANUAIS = set(range(392, 396))
SC = "Scania"
_REF = re.compile(r"^(?:REF(?:\.|\s*ORIG(?:INAL)?)?\s*:?\s*)?((?:[A-Z]\s?)?\d{2,3}(?:[ .]\d{2,4}){2,4}(?:-\d+)?)\s+")

for _p in range(393, 396):
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
        _r["montadora"] = SC
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




def S(p, c, d, ref=None, apl=None, **kw):
    """Descrição, referência original e aplicação transcritas do card."""
    kw["descricao"] = d
    if ref is not None:
        kw["cod_ref"] = ref
    if apl is not None:
        kw["aplicacao"] = apl
    kw.setdefault("info", "")
    F(p, c, **kw)


_ESC = "SC 110/115/6/111/FTRSK112/K113"
# 393 (pág. impressa 392)
for _c, _d, _ref, _apl in [
        ("5061152", "JUNTA LUB TURBINA SCANIA 112/3", "2T0.145.757", "12170BT/13170/13190/14170BT..."),
        ("5061153", "JUNTA LUB TURB. SCANIA 112/113", "139.471 / 1671153", ""),
        ("9023440", 'JUNTA COLETOR ESCAPE "JOGO"', "277.272X", "SC 110/111/112"),
        ("4665721", 'JUNTA COLETOR ESCAPE "COBREADA" (MENOR)', "277.273", _ESC),
        ("9023525", 'JUNTA COLETOR ESCAPE "CHAPA" (MENOR)', "277.273", _ESC),
        ("9023528", 'JUNTA COLETOR ESCAPE "CHAPA" (MAIOR)', "277.272", _ESC),
        ("4660049", 'JUNTA COLETOR ESCAPE "COBREADA" (MAIOR)', "277272", _ESC),
        ("0551436", "PARAFUSO 14 X 35 AÇO 10.9 VOLANTE MOTOR", "", ""),
        ("9981807", "LAMINA ACOPLAMENTO SCANIA 112 1828", "280862", ""),
        ("9981839", "LAMINA ACOPLAMENTO SCANIA 113 HW", "318523", ""),
        ("9981808", "LAMINA ACOPLAMENTO MBB 355/SCA110/111", "192638", ""),
        ("5060695", "CHAVETA EIXO ACOPLAMENTO BOMBA INJETORA (05 X 09 X 22MM)", "800695", "SC 111"),
        ("5061163", "CHAVETA EIXO ACOPLAMENTO BOMBA INJETORA (06 X 09 X 22MM)", "800697", "SC 112"),
        ("5060702", "CHAVETA EIXO ACOPLAMENTO ENGR. DISTRIBUICAO (08 X 10,5 X 25MM)", "800702", "SC 111/112"),
        ("9016927", 'VALVULA RETORNO BOMBA INJETORA "MODERNA"', "1358496", "SCANIA 94/114/124/164"),
        ("9981802", "CABECOTE PRE FILTRO DIESEL", "192873", "SC 111/112/113"),
        ("9980640", "COPO DIESEL BOMBA MANUAL (VIDRO)", "192876", "SC TODOS"),
        ("9025551", "REPARO FIXACAO COPINHO BOMBA ALIMENTADORA", "3455860207", "TODOS"),
        ("9025552", "REPARO BOMBA ALIMENTADORA VALVULAS", "550140", "SC TODOS")]:
    S(393, _c, _d, _ref, _apl)
F(393, "5061152", montadora="Scania, Volkswagen")
F(393, "9981808", montadora="Mercedes-Benz, Scania")
F(393, "9025551", variacoes="9441080033"); F(393, "9025552", variacoes="9441080175")
_r393 = [r for r in ADD if r["pagina"] == 393][0]
ADD.append(dict(_r393, codigo="8001615", descricao="VALVULA SEGURANÇA 16X1,5 10,4B", cod_ref="303496", aplicacao="", variacoes="",
                info="", card=90, foto_spec={"rect": [32, 304, 176, 353]}, montadora=SC))
ADD.append(dict(_r393, codigo="5060262", descricao="BOIA TANQUE COMB SCANIA", cod_ref="1670262", variacoes="",
                aplicacao="K112/113/T112/R142/143/T112/14", info="Código impresso como '506 0262'", card=91,
                foto_spec={"rect": [396, 705, 545, 762]}, montadora=SC))
NOTAS.append("Pág. 393: 8001615 (válvula de segurança) e 5060262 (boia do tanque, impresso '506 0262') lidos da imagem; as lâminas "
             "de acoplamento 9981807, 9981839 e 9981808 também estão no cap. Peças Mercedes-Benz (pág. 385).")
# 394 (pág. impressa 393)
for _c, _d, _ref, _apl in [
        ("9023467", "JUNTA COLETOR ESCAPE", "287789", "SC 113"),
        ("9023468", "JUNTA COLETOR ESCAPE 1 FURO", "1109288", "SC TRK112"),
        ("9023475", "JUNTA COLETOR ESCAPE 1 FURO", "1336138", "SC TRK112"),
        ("9023494", "JUNTA COLETOR ESCAPE", "1309501", "SC 114/124"),
        ("9023497", "JUNTA COLETOR ADMISSAO 1 FURO", "1374340", "SC 124"),
        ("9023498", "JUNTA COLETOR ADMISSAO TUBO ENTRADA", "1374342", "SC 124114"),
        ("9023474", "JUNTA COLETOR ADMISSAO", "1.675.583", "SC KFS113"),
        ("9023476", "JUNTA COLETOR ADMISSAO", "1675584", "SC FS113"),
        ("9023499", 'JUNTA COLETOR ADMISSAO DUPLA "NA"', "1516474", "SCANIA 94/114/124/164"),
        ("9023504", 'JUNTA COLETOR ADMISSAO DUPLA "CHAPA"', "1.516.474", "SCANIA 94/114/124/164"),
        ("9010106", "BATENTE CABINE", "1.349.805", "SC 114/124"),
        ("9020104", "BATENTE CABINE", "1.349.810", "SC 114/124"),
        ("9011422", "BUCHA AMORTECEDOR 21 X 50MM (MAIOR)", "241922G", "SC T112"),
        ("9011420", "BUCHA AMORTECEDOR TAMANHO ORIGINAL (21X45MM)", "241922P", "SC T112"),
        ("9011484", "BORRACHA AMORTECEDOR SUPERIOR (FURO 22,0 MM)", "137885", "SC TODOS"),
        ("5062025", "BUCHA AMORT.DIANT SCANIA MENOR", "", ""),
        ("5062026", "BUCHA AMORT.DIANT SCANIA MAIOR", "", ""),
        ("9011421", "BUCHA AMORTECEDOR (FURO 20,0 MM)", "307113", "SC 114/124"),
        ("9012287", "CONJUNTO ESTICADOR CINTA TANQUE OLEO DIESEL", "324937X", "SC FTR112/TR142"),
        ("9012210", "CONJUNTO ESTICADOR CINTA TANQUE OLEO DIESEL", "306133X", "SC 113"),
        ("9012288", "CONJUNTO ESTICADOR CINTA TANQUE OLEO DIESEL", "1.398.645", "SC 94/114/124/164")]:
    S(394, _c, _d, _ref, _apl)
NOTAS.append("Pág. 394: 9023499 e 9023504 trazem a mesma referência (1516474 / 1.516.474).")
# 395 (pág. impressa 394)
for _c, _d, _ref, _apl in [
        ("9014792", "PARAFUSO ESTICADOR CINTA TANQUE (08 X 1,25 X 100 MM)", "", "SC 111/112"),
        ("9014805", "PARAFUSO ESTICADOR CINTA TANQUE (10 X 1,50 X 100 MM)", "", "SC 112/113/142"),
        ("5066595", "TRAVA BORRACHA TAMPA CAIXA BATERIA", "366.595", "SC TR113/143"),
        ("10009091", "BUCHA SUSPENSAO CABINE DIANTEIRO", "1.372.432", "SC SERIE 4 TODOS"),
        ("10009090", "BUCHA SUSPENSAO CABINE TRASEIRO", "1.343.134", "SC SERIE 4 TODOS"),
        ("10002279", "COXIM CABINE SUPERIOR", "390.358", "SC T/R 112/113"),
        ("9014009", "MANCAL SUSPENSAO CABINE AR DIANTEIRO 2007/...", "1.744.211", "SC 124R/P94"),
        ("9014007", "MANCAL SUSPENSAO CABINE AR", "1.443.114", "SC 124"),
        ("10009075", "BATENTE CABINE TRASEIRO SUPERIOR", "348.764", "SC R112/3 R142/3"),
        ("10009089", "BUCHA SUSPENSAO CABINE", "716.360", "SC 113"),
        ("10006599", "ARRUELA ESTABILIZADOR CABINE", "", "SC SERIE 4 TODOS"),
        ("5060259", "CANO INJETOR UNIVERSAL SCANIA", "", "")]:
    S(395, _c, _d, _ref, _apl)
F(395, "10006599", info="Impresso como 'ruela Estabilizador' (texto cortado pela foto)")
F(394, "9023504", foto_spec={"rect": [26, 406, 126, 463]})
