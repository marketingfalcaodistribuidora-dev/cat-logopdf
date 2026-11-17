# Capítulo 31 - Peças Volvo (págs. 396-398)
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
         (r"CANO", "CANO"), (r"PATIN", "PATIN"), (r"PRISIONEIRO", "PRISIONEIRO"), (r"GARFO", "GARFO"), (r"ROLETE", "BUCHA")]
AJ = {}
ADD = []
NOTAS = ["Págs. 396-398: o número original da montadora (REF ORIG) está na coluna de referência."]
MANUAIS = set(range(396, 399))
VV = "Volvo"
_REF = re.compile(r"^(?:REF(?:\.|\s*ORIG(?:INAL)?)?\s*:?\s*)?((?:[A-Z]\s?)?\d{2,3}(?:[ .]\d{2,4}){2,4}(?:-\d+)?)\s+")

for _p in range(396, 399):
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
        _r["montadora"] = VV
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


# 396 (pág. impressa 395)
for _c, _d, _ref, _apl in [
        ("5061196", "BATENTE CAPO TRASEIRO (MAIOR) 52,0 MM ALTURA", "1.611.789", "VV N10/N12 NL10/12"),
        ("5061195", "BATENTE CAPO TRASEIRO (MENOR) 44,0 MM ALTURA", "1.584.539", "VV N10/N12 NL10/12"),
        ("5063229", "BATENTE CAPO TRASEIRO", "8.126.254", "VV FH/NH 12"),
        ("10009078", "BATENTE CABINE VOLVO NL10/12", "6.889.145", "VV NL10/12"),
        ("10009121", "BATENTE CABINE", "1.096.625", "VOLVO FH12"),
        ("10006585", "BATENTE CABINE", "8.141.727", "VV FH12"),
        ("5061194", "BUCHA SUSPENSAO CABINE PEQUENA (19,0X62,0X38,0MM)", "364.572", "VV NL10/12"),
        ("10009124", "BATENTE SUSPENSAO CABINE", "20.429.148", "FH 12 / FM 10 / FM 12"),
        ("10009122", "BATENTE SUSPENSAO CABINE", "20.453.260", "FH 12 / FM 10 / FM 12"),
        ("5061193", "BUCHA SUSPENSAO CABINE GRANDE (19,0X70,0X49,0MM)", "364.571", "")]:
    S(396, _c, _d, _ref, _apl)
# 397 (pág. impressa 396): descrições impressas como imagem (transcritas)
_T = "Descrição impressa como imagem (transcrita)"
for _c, _d, _apl in [
        ("5060835", "COXIM CABINE VOLVO TODOS", ""), ("5060836", "COXIM CAMBIO TRAVESSA VOLVO", ""),
        ("4750887", "PATIN VOLVO DIANT. 6X45", ""), ("5060890", "PATIN VOLVO DIANT. 6X60", ""),
        ("5060919", "PARAFUSO CALÇO CABINE SCANIA/VOLVO 5/8 X 5", ""), ("0740946", "PF. COLETOR VOLVO ROSCA PARCIAL", ""),
        ("5061179", "TRAVA ARANHA CUBO TRAS VOLVO", ""), ("5065525", "TRAVA ARANHA CUBO DIANTEIRO GRAXA VOLVO", ""),
        ("2500809", "PRISIONEIRO CAPA SECA PEQUENO", ""), ("3320716", "7/16 PORCA PRIS. CAPA SECA", ""),
        ("2500810", "PRISIONEIRO CAPA SECA GRANDE", "")]:
    S(397, _c, _d, "", _apl, info=_T)
F(397, "5060919", montadora="Scania, Volvo")
F(397, "5065525", foto_spec={"rect": [299, 574, 376, 642]})
NOTAS.append("Pág. 397: 2500809, 3320716 e 2500810 (prisioneiros e porca da capa seca) não têm logo de montadora no card; "
             "foram mantidos como Volvo por estarem na seção Volvo.")
# 398 (pág. impressa 397)
for _c, _d, _ref, _apl in [
        ("5067435", "FLEXIVEL DIR.HID.360MM", "", "VOLVO NL10/NL12/EDC"),
        ("5066033", "FLEXIVEL DIR.390MM", "", "NL10/NL340"),
        ("5068851", "FLEXIVEL DIR.HID. 410MM VOLVO", "", ""),
        ("5064946", "MANGUEIRA ADMISSAO VOLVO NL10", "", ""),
        ("5064947", "MANGUEIRA PURIFICADOR", "", "VOLVO N12/NL12/EDC"),
        ("5060536", "SUPORTE TRAS CX", "", "VOLVO NL10/NL12/EDC"),
        ("5069499", "ABRACADEIRA ESCAPE", "", "VOLVO FH,NH,EDC,FM"),
        ("5068279", "BUCHA ROLETE PATIM", "", "VOLVO NL10/12/EDC/..."),
        ("5065499", "ABRA ESCAP. COMP VOLVO N10/12", "475499", "N10/N12/NL/B58"),
        ("5063253", "SUPORTE CINTA ESCAPE VOLVO", "8123253", "VV NL TODOS"),
        ("5069964", "GARFO SERVO EMBREAGEM (100MM)", "949964", "VV N10/N12/NL10/NL12")]:
    S(398, _c, _d, _ref, _apl)
for _c, _rect in (("5064946", [342, 251, 523, 343]), ("5060536", [385, 401, 507, 489]), ("5068279", [382, 541, 467, 627])):
    F(398, _c, foto_spec={"rect": _rect})
NOTAS.append("Pág. 398: o card 5066033 traz a aplicação impressa como 'NL10' + barra invertida + 'NL340'.")
F(397, "0740946", foto_spec={"rect": [320, 476, 480, 553]}); F(397, "5060835", foto_spec={"rect": [36, 146, 192, 234]})
