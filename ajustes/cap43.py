# Capítulo 43 - Fechaduras, Maçanetas e Acessórios de Cabine (págs. 478-483)
# Cards em grade (cards_grade.ler): código + descrição + "Caminhões ..." (aplicação) + "Nº Orig." / "REF ORIG" / "Código Original".
import re

from cards_grade import ler

TIPOS = [(r"^FECHADURA", "FECHADURA"), (r"^FECHO", "FECHO DO CAPÔ"), (r"^PINO", "PINO FECHO"), (r"^MANIVELA", "MANIVELA DO VIDRO"),
         (r"^BATENTE", "BATENTE DA PORTA"), (r"^MA[CÇ]ANETA|^MAC\b", "MAÇANETA"), (r"^CABO", "CABO DE COMANDO"),
         (r"DOBRADI", "DOBRADIÇA"), (r"^RESERV", "RESERVATÓRIO"), (r"^VARETA", "VARETA"), (r"^SUPORTE", "SUPORTE"),
         (r"^TAMPA", "TAMPA"), (r"^COPO", "COPO FILTRO"), (r"^BALISA|^MASTRO", "BALIZA"), (r"^GUARDA", "GUARDA-PÓ")]
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(478, 484))
_MONT = [(r"\bMB\b|MERCEDES|ATEGO|ACCELO|AXOR|ACTROS|ATRON|ATEXO|HPN|\b(?:608D|709|1113|1214|1418|1620)\b", "Mercedes-Benz"),
         (r"\bVW\b|VOLKS|CONSTELLATION|DELIVERY|GOL\b", "Volkswagen"), (r"FORD|CARGO", "Ford"), (r"SCANIA", "Scania"),
         (r"VOLVO", "Volvo"), (r"IVECO|STRALIS|EUROCARGO", "Iveco")]
_REF = re.compile(r"(N[ºo°]\s*Orig\.?\s*:|REF\.?\s*ORIG(?:INAL)?\.?\s*:*|C[óo]digo\s*Original\s*:|CODIGO ORIGINAL\s*:|N\.O\.\s*:)", re.I)
_APL = re.compile(r"(APLICA[ÇC](?:[ÃA]O|[ÕO]ES)(?:\s*da\s*Pe[çc]a)?\s*:?|Caminh[õo]es\b)", re.I)

for _p in range(478, 484):
    for _r in ler(_p):
        t = re.sub(r"\s+", " ", _r.pop("_texto", "")).strip()
        cod = _r["codigo"]
        t = re.sub(r"^%s\s*" % cod[-3:] if re.match(r"\d{3,4}\s", t) else r"^$", "", t)
        t = re.sub(r"^\d{3,4}\s+(?=[A-Za-z])", "", t)
        refs = []
        partes = _REF.split(t)
        base = partes[0]
        for k in range(1, len(partes) - 1, 2):
            v = partes[k + 1].strip(" |")
            m = _APL.search(v)
            if m and m.start() > 0:
                base += " " + v[m.start():]
                v = v[:m.start()]
            refs.append(v.strip(" |,"))
        m = _APL.search(base)
        desc, apl = (base[:m.start()], base[m.start():]) if m else (base, "")
        apl = re.sub(r"^APLICA[ÇC](?:[ÃA]O|[ÕO]ES)(?:\s*da\s*Pe[çc]a)?\s*:?\s*", "", apl, flags=re.I).strip(" -|")
        _r.update(descricao=desc.strip(" -|").upper(), cod_ref=" / ".join(x for x in refs if x), aplicacao=apl, info="",
                  montadora=", ".join(dict.fromkeys(m for rx, m in _MONT if re.search(rx, desc + " " + apl, re.I))))
        ADD.append(_r)


def F(p, c, **kw):
    regs = [r for r in ADD if r["pagina"] == p and r["codigo"] == c]
    assert regs, f"{c} não está na pág. {p}"
    for r in regs:
        r.update(kw)


MB = "Mercedes-Benz"
# 478 (pág. impressa 477)
F(478, "7050111", descricao="PINO FECHO CAPO CAMINHOES 1214-618 APOS 1990", cod_ref="964.880.01.60", montadora=MB)
F(478, "5067051", descricao="MB DOBRADICA CAPO 1620 A 1938", cod_ref="384.887.7051", montadora=MB)
NOTAS.append("Pág. 478: o número curto antes de algumas descrições (312, 313...) são os últimos dígitos do código; 'Atexo' impresso "
             "assim nos cards 7050594/7050595.")
# 479 (pág. impressa 478)
for _c, _d in (("7051140", "CABO ABERTURA CAPO S/MACAN"),):
    F(479, _c, descricao=_d, cod_ref="693.750.70.84", montadora=MB)
for _c in ("7051141", "7051142", "7051143"):
    F(479, _c, montadora=MB)
F(479, "7051209", montadora=MB)
NOTAS.append("Pág. 479: 7050914 (dir.) e 7050913 (esq.) trazem a mesma referência 973.760.01.04.")
# 481 (pág. impressa 480): maçanetas
F(481, "7054330", descricao="MACANETA SCANIA SERIE 4/5 EXT LE 1544330", aplicacao="Para Scania série 4 / série 5",
  cod_ref="Scania 1488409 / 1544330", montadora="Scania")
F(481, "7056975", descricao="MACANETA SCANIA 112 EXT LE 1306975", montadora="Scania",
  aplicacao="Scania P93, R112, R113, R142, R143, T112, T113, T142", variacoes="Ref. similar: 001303 Cipec / 1306975 Scania / 356085 Scania")
F(481, "7130559", descricao="MACANETA MB AXOR/ACTROS EXT LD A9417600559", aplicacao="Família Accelo", montadora=MB)
F(481, "7054710", descricao="MACANETA IVECO EUROCARGO EXT LE 98404710", montadora="Iveco",
  aplicacao="Eurocargo 1998 a 2012 160E21/160E23/170E22/170E24/230E22/230E24/260E25; Eurotech 1997 a 2005 370/420/440; "
            "Eurotrakker 1997 a 2005 380/420")
F(481, "7050459", descricao="MACANETA MB AXOR/ACTROS EXT LE 9417600459", aplicacao="Veículos Mercedes Axor / Actros", montadora=MB)
F(481, "7051334", descricao="MACANETA VOLVO FH/FM EXT LE 8191334", aplicacao="Volvo FH12 FH16 FM7 FM12 FM9 NH12", montadora="Volvo")
F(481, "7056873", descricao="MACANETA VOLVO VM EXT LE 24426873", aplicacao="VM 2020 A .... (220, 270, 310, 330)", montadora="Volvo")
F(481, "7057205", descricao="MACANETA VW CONSTELLATION EXT LD 2R2837205", montadora="Volkswagen")
for _c, _d, _o, _a in (
        ("50050280", "MAÇANETA EXTERNA PORTA DIANTEIRA-UNIVERSAL LADO DIREITO C/CHAVE", "50280", "Mercedes-Benz Atron"),
        ("50050279", "MAÇANETA EXTERNA PORTA DIANTEIRA-UNIVERSAL LADO ESQUERDO C/CHAVE", "50279", "Mercedes-Benz Atron"),
        ("50050386", "MAÇANETA INT. PTA. DIANT. - DIR.", "50386", "Mercedes-Benz Accelo"),
        ("50050387", "MAÇANETA INT. PTA. DIANT. ESQ.", "50387", "Mercedes-Benz Accelo")):
    F(481, _c, descricao=_d, variacoes="Código original (fabricante): " + _o, cod_ref="", aplicacao=_a, montadora=MB)
NOTAS.append("Pág. 481: códigos 500xxxxx (8 dígitos) trazem 'Código Original' de 5 dígitos (referência do fabricante, em similares).")
# 482 (pág. impressa 481)
F(482, "7132156", montadora="Volkswagen")
# 483 (pág. impressa 482): diversos MB e maçanetas/batentes
for _c, _d, _ref, _apl, _m in [
        ("0230365", "RESERVATÓRIO ÓLEO BOMBA HIDRÁULICA ZF", "384 466 70 02", "0370/0371/0400/HPN/FP N/LN", "Mercedes-Benz, Volkswagen, Ford"),
        ("5061167", "VARETA DO HIDRÁULICO MODERNO", "000 466 11 67", "OF/OH-1315", MB),
        ("5066938", "SUPORTE DA PLACA", "693 885 70 14", "", MB),
        ("7005127", "TAMPA COROTE PLÁSTICO", "", "", ""),
        ("5066937", "SUPORTE PLACA CINZA", "", "", MB), ("5066936", "SUPORTE PLACA PRETA", "", "", MB),
        ("5063761", "COPO FILTRO OLEO COMB. (MAIOR)", "376 092 71 04", "O366 moderno 1620/1723", MB),
        ("5063762", "COPO FILTRO OLEO", "382.092.7003", "", MB),
        ("5067001", "BALISA PLÁSTICA", "344 595 70 01", "AGL/L-1111/1113/1313/1513/1519", MB),
        ("5060701", "MASTRO MB MOD CURTO", "384 595 70 01", "1214/1941", MB),
        ("5067000", "BALISA PLÁSTICA MODERNA TODOS", "384 595 70 01", "1214/1941", MB),
        ("5068546", "BALISA ORIENTAÇÃO PLÁSTICA", "308 564", "T112/142/113", "Scania"),
        ("5063442", "GUARDA-PO CAMBIO SUPERIOR", "344 267 00 96", "L1113/1313/1513/2013/2213", MB),
        ("5060423", "MACANETA PINO FERRO MARROM", "", "", ""), ("5060422", "MACANETA PINO FERRO CINZA", "", "", "")]:
    F(483, _c, descricao=_d, cod_ref=_ref, aplicacao=_apl, montadora=_m)
F(483, "5066937", info="Foto ilustrativa"); F(483, "5066936", info="Foto ilustrativa")
F(483, "5060423", info="Foto ilustrativa"); F(483, "5060422", info="Foto ilustrativa")
F(483, "5060701", variacoes="GCO-393"); F(483, "5063442", variacoes="GCO-379")
for _c, _d, _o, _a, _m in [
        ("50020303", "BATENTE DA PTA. DIANT. - ESQ.", "20303", "Volkswagen Delivery - Kombi Clipper 75 à 13 - Titan - Tractor - Worker", "Volkswagen"),
        ("50020302", "BATENTE DA PTA. DIANT. - DIR.", "20302", "Volkswagen Delivery - Kombi Clipper 75 à 13 - Titan - Tractor - Worker", "Volkswagen"),
        ("50021328", "MAÇANETA INT. PTA. DIANT. - DIR. CINZA ESCURO", "21328", "Volkswagen 13-150 00 em diante - 13-170 00 em diante", "Volkswagen"),
        ("50021527", "MAÇANETA INT. PTA. DIANT. - ESQ. GRAFITE", "21527", "Volkswagen Constellation", "Volkswagen"),
        ("50031221", "MAÇANETA EXT. PTA. DIANT. - ESQ. S/CHAVE", "31221", "Ford Cargo GII após 11", "Ford")]:
    F(483, _c, descricao=_d, variacoes="Código original (fabricante): " + _o, cod_ref="", aplicacao=_a, montadora=_m)
NOTAS.append("Pág. 483: textos de vários cards impressos como imagem (transcritos); 0230365 (reservatório óleo ZF) também está no "
             "cap. Peças Volkswagen e Ford e 7005127 (tampa corote) no cap. Nicolini; 5060701 e 5067000 trazem o mesmo N.O. 384 595 70 01.")
# 480 (pág. impressa 479): manivelas VW - separa a aplicação de carros da descrição
F(480, "7050650", descricao="MANIVELA REGULADORA DO VIDRO PLÁSTICA CINZA",
  aplicacao="Gol - Saveiro - Parati GII/GIII/GIV/GV / Fox após 03 / Polo após 02 / Caminhões Worker - Delivery - Titan")
for _c, _cor in (("7050419", "PRETA"), ("7050420", "CINZA")):
    F(480, _c, descricao=f"MANIVELA REGULADORA DO VIDRO - PLÁSTICA {_cor}",
      aplicacao="Gol BX/Brasília/Kombi/Fusca/Gol GII/Santana/Passat/Variant/TL/Voyage/linha VW após 87 / "
                "Caminhões Worker/Delivery/Tractor/Titan")
F(480, "7050781", montadora="Scania")
F(481, "7056976", montadora="Scania")
F(478, "7050111", aplicacao="Caminhões 1214-618 após 1990")
