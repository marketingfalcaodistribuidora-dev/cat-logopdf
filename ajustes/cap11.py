# Capítulo 11 - Filtros (págs. 123-150) — cards com tabelas de equivalência e aplicação (leitor TABELA)
FAIXA_TAB = {p: () for p in (128, 129, 130, 131, 134, 135, 136, 137, 138, 140, 141, 142, 143, 146, 147, 148, 149)}
FAIXA_TAB[133] = (14, 12)
FAIXA_TAB[139] = (13.8, 14)
FAIXA_TAB[144] = (11, 11)
FAIXA_TAB[145] = (13.5, 13.5)
TABELA = set(range(123, 151)) - set(FAIXA_TAB)
TIPOS = [
    (r"COPO", "COPO FILTRO"), (r"SENSOR", "SENSOR"), (r"SECADOR|APU", "FILTRO SECADOR DE AR"),
    (r"\bAR\b|AR PRIM|AR SEC|FILTRO DE AR", "FILTRO DE AR"), (r"HIDR|DIRE[CÇ]", "FILTRO HIDRÁULICO"),
    (r"COMB|DIESEL|RACOR|SEPARADOR", "FILTRO DE COMBUSTÍVEL"), (r"[ÓO]LEO|LUBR", "FILTRO DE ÓLEO"),
    (r"ARLA|UREIA", "FILTRO ARLA"), (r"CABINE|AR CONDICIONADO", "FILTRO DE CABINE"), (r"FILTRO", "FILTRO"),
]
AJ = {}
NOTAS = []
ADD = []
AJ["cod:4920074"] = dict(
    descricao="FILTRO MB OLEO B170 B180 B200 FOECO074", tipo="FILTRO DE ÓLEO", info="LANÇAMENTO 03/25",
    variacoes="Códigos equivalentes: Fram CH10054ECO / Fram CH10054 / Hengst E146HD108 / Japanparts FOECO050 / Japanparts FOECO074 / "
              "Mahle OX1046D / Mahle OX382D / Mann HU612/1x / Mann HU6121X / Mann HU6121 / Purflux / Fram C482 / Sakura EO26400 / "
              "Seineca SEF7080 / Tecfil PEL720 / Vox LE720 / Wega WOE308")
AJ["124.4"] = {"records": [dict(
    codigo="4861060", descricao="FILTRO VW COMB DELIVERY EXPRESS FCD0696", tipo="FILTRO DE COMBUSTÍVEL", cod_ref="2V3127177",
    variacoes="PARKER RE-160LJ-10M-AQII", marca="Parker", montadora="Volkswagen",
    aplicacao="VOLKSWAGEN Constellation 17.280 motor MAN D0836260 2020--> / Constellation 24.280 motor MAN D0836280 2020--> / "
              "Constellation 26.280 E motor MAN D0836280 2020--> / Constellation 31.280 E motor MAN D0836280 2020--> / "
              "Constellation 13.190 E motor MAN D0836280 2020-->",
    info="Código interno impresso como desenho (não é texto no PDF)")]}
AJ["cod:4860381"] = dict(descricao="FILTRO SCANIA G 3 80 2008 A PARKER", cod_ref="SCANIA 1411794 / 1763776 / 1763776",
                         variacoes="PARKER RC-381 / WEGA FCD2042 / MANN WK940/2 / MANN WK940/10", info="LANÇAMENTO",
                         aplicacao="SCANIA 460R EURO 6 motor SUPER Dw6 01-2008->", marca="Parker", montadora="Scania")
NOTAS += ["p124 card 4 e p126 card 1: o código 4861060 aparece em dois cards com descrições diferentes (Delivery Express FCD0696 / Delivery 11.180); registrado numa linha com as duas descrições.",
          "Filtros: cards Parker com tabelas de equivalência (marca → código) e aplicação (montadora, modelo, motor, ano); códigos de montadora ficam em 'Código ref.', demais marcas em 'Variações'."]
AJ["cod:4866010"] = dict(
    descricao="FILTRO MB COMB ATEGO 1729 PARKER -FCBR217S", cod_ref="MERCEDES BENZ A0004779915", marca="Parker",
    variacoes="Parker RE-160-10M-AQUII / Fleetguard FS20222 / Hengst E821KPD704 / Hengst E822KP D705 / Hengst E822KPD705 / "
              "Hifi Filter SN70518 / Japan Parts FCBR217S / Mann PU9198 / Partmo PP79915SP / Tecfil PEC9915",
    aplicacao="Logos Actros / Accelo / Axor / Atego", montadora="Mercedes-Benz", info="")

# ---------------- pág. 132 (cards Wega: listas "Códigos de Marcas Equivalentes") ----------------
_TR = "Pesada / Máquina agrícola / Trator série T7 - T7.175 (SPS) New Holland 144 cv 2014-> / Trator série T8 - T8.320, T8.350, T8.380, T8.410, T8.435 New Holland FPT 8.7L 2014->"
AJ.update({
    "132.1": {"records": [dict(codigo="4920971", descricao="FILTRO COMBUSTÍVEL DIESEL SCANIA FCD0971", tipo="FILTRO DE COMBUSTÍVEL",
        cod_ref="SCANIA 2878847 / 2879243 / 2779191 / 2780443", marca="Wega", montadora="Scania",
        variacoes="Hengst E826KPD7242 / Hengst E826KPD724-2 / Original Filter OFC1800E / Wega FCD0971 / Wega FCD971")]},
    "132.2": {"records": [dict(codigo="4920970", descricao="FILTRO COMBUSTÍVEL DIESEL SCANIA FCD0970", tipo="FILTRO DE COMBUSTÍVEL",
        cod_ref="SCANIA 2779191 / 2878847 / 2779190", marca="Wega", montadora="Scania",
        variacoes="Hengst E826KPD7242 / Hengst E826KPD724-2 / Original Filter OFC1800E / Wega FCD0970 / Wega FCD970")]},
    "132.3": {"records": [dict(codigo="4925002", descricao="FILTRO ÓLEO ROTATIVO SCANIA 2731875/WOR5002", tipo="FILTRO DE ÓLEO",
        cod_ref="SCANIA 2731875", variacoes="Wega WOR5002", marca="Wega", montadora="Scania")]},
    "132.4": {"records": [dict(codigo="4920953", descricao="FILTRO AR SECUNDÁRIO CUMMINS WAP953/S", tipo="FILTRO DE AR",
        cod_ref="LiuGong 1109N030 / LiuGong 1109N12030", marca="Wega", montadora="LiuGong",
        variacoes="Automotiv Ai3064 / Baldwin Pa5275 / Donaldson P500941 / Fleetguard Af25277 / Sakura A8646 / Tecfil AS109 / "
                  "Turbo Filtros TR25277 / Unifilter SP104905B / Unifilter UA6156P / Wega WAP-953/S / Wega WAP953/S",
        info="Logo LiuGong (pá carregadeira)")]},
    "132.5": {"records": [dict(codigo="4924006", descricao="FILTRO VW CONSTELLATION AR CONDICIONADO AKX4006-2", tipo="FILTRO DE CABINE",
        cod_ref="VOLKSWAGEN 2R2819429", marca="Wega", montadora="Volkswagen",
        variacoes="Authomix FCA4299 / Bosch 0986BF0602 / Corteco 51138 F / Denso Bc2614010270 / Donaldson P750019 / Filtros Bras Fb013 / "
                  "Filtros Mil Fc5801 / Fram Cf10864 / Hengst E4918LI-2 / Idelmax Mx5427 / Japanparts FAAVW07 / Mahle LA652/S / "
                  "Mann Cu22018 / Micron Air MP558-2 / Schuck SK473 / Sogefi Pro PC8401 / Tecfil ACP429 / Tecfil ACP429/9 / "
                  "Turbo Filtros TAC5427 / Vox FAC429/9 / Vox antigo FAC429 / Wega AKX4006-2 / Wix WP10287")]},
    "132.6": {"records": [dict(codigo="4920959", descricao="FILTRO DIESEL/RACOR TRATOR NEW HOLLAN FCD0959", tipo="FILTRO DE COMBUSTÍVEL",
        aplicacao=_TR, marca="Wega", montadora="New Holland", info="Card repetido na mesma página (p.132)")]},
    "132.9": {"skip": True},
    "132.8": {"records": [dict(codigo="4920712", descricao="FILTRO AR PRIMARIO CASE COLHEITADEIRA", tipo="FILTRO DE AR",
        cod_ref="Case 73170678 / New Holland 73170678", montadora="Case, New Holland",
        variacoes="Hitachi 4206272 / Liebherr 550799408 / Fleetguard AF1605M / Tecfil AP1605 / Clark E12570266 / Vox HP1605 / "
                  "Baldwin LL2562 / Donaldson P182042 / Donaldson P624680 / Inpeca SAP1605 / Unifilter UA128407P",
        aplicacao="Compatível com: Volvo 11033950 / Atlas Copco 1610413101 / Komatsu 2090178260 / Cummins 3001893")]},
    "132.7": {"records": [dict(codigo="4927120", descricao="FILTRO VW CONSTELLATION AR CONDICIONADO AKX4006-2", tipo="FILTRO DE AR",
        cod_ref="Case 73170676 / New Holland 73170676 / New Holland 84428273", montadora="Case, New Holland",
        variacoes="Cummins 3013213 / Liebherr 5507995 / Fleetguard AF1604 / Tecfil AS605 / Clark E12570267 / Vox HS605 / "
                  "Donaldson P128408 / Baldwin Pa2563",
        aplicacao="Compatível com: Volvo 11033951 / Komatsu 1236971H1 / Hitachi 12570267",
        info="Título impresso igual ao do 4924006, mas o card mostra filtro de ar de colheitadeira Case")]},
    "132.10": {"records": [dict(codigo="4921010", descricao="FILTRO OLEO TRATOR POWERTECH - 410 CV -WEA010", tipo="FILTRO DE ÓLEO",
        cod_ref="John Deere Dz110513", variacoes="Wega WEA010", marca="Wega", montadora="John Deere")]},
})
NOTAS += ["p132: o card 4920959 aparece duas vezes na página.",
          "p132: o card 4927120 tem o título do 4924006 (VW Constellation ar condicionado), mas a foto e as equivalências são de filtro de ar Case/New Holland."]
AJ["cod:4927998"] = dict(descricao="FILTRO VW DELIVERY 98 MB 712E 02 FA7889S AR", tipo="FILTRO DE AR")
AJ["cod:4920009"] = dict(
    descricao="FILTRO ARLA UREIA REFIL WEA009", tipo="FILTRO ARLA", marca="Wega", montadora="Mercedes-Benz, DAF, Scania",
    cod_ref="Original 4388378 / 6051964 / 1420589 / 1420789 / 1420989 / 11150708 / 11450803 / M. Benz A0001420589 / A0001420789 / "
            "A0001420989 / A0001421089 / DAF 2122909 / Scania 2655854 / MWM MM100832 / Fendt ACP0153520",
    variacoes="Fleetguard UF106 / Hengst E104UD350 / Hifi KD70436 / Japanparts FUBR08S / Mann U58/6 / Mann U58/9KIT / Mann U58/7 / "
              "Orig Filter OFU8007KIT / Tecfil PEA180 / Wega WEA009",
    info="Filtro do Arla (filtro de uréia)", aplicacao="")
AJ["cod:4922280"] = dict(
    descricao="FILTRO VOLV COMBUSTIVEL DIESEL FCD2280", tipo="FILTRO DE COMBUSTÍVEL", marca="Wega", montadora="Volkswagen, Cummins, LiuGong",
    cod_ref="Cummins 5294779 / 5301449 / 5364946 / 5405295 / LiuGong 111700181 / LiuGong Sp160254",
    variacoes="Baldwin BF9869 / Fleetguard FS36247 / Donaldson P502484",
    info="Tipo: filtro de combustível separador blindado com dreno | Altura 200 mm | Diâmetro externo 110 mm | Rosca 1-14UNF-2B")
AJ["cod:4922302"] = {"variacoes": "Wega FCD2302 / Wega FCD-2302", "info": "", "marca": "Wega"}
AJ["cod:4927998"]["variacoes"] = ("Mann Filter / Tecfil (logos): C17308 / Ap7998 / Fram EU CA283A / Inpeca SAP7810 / Mahle LX910 / "
                                  "Mann EU C17308 / Tecfil AP7998 / Vox HP7998 / Wega WAP285 / Bosch EU 0986B03531")
AJ["cod:4927998"]["info"] = "OBSERVAÇÕES: Utilizado com filtro de segurança FS7998S"
AJ["cod:4927998"]["montadora"] = "Ford, Volkswagen, Mercedes-Benz"

# pág. 136 topo: grade 2x2 sem bordas na coluna direita -> transcrição manual (foto por recorte)
AJ["cod:4920050"] = dict(descricao="FILTRO MAN OLEO TGX 29440 33440 FUBR05S", tipo="FILTRO DE ÓLEO",
    cod_ref="MAN 07W103464 / MAN 51018046002", variacoes="Tecfil (logo): ESAO3464 / Wega WEOD001 / Tecfil ESAO3464",
    info="OBSERVAÇÕES: FUBR05S", montadora="MAN, Volkswagen", aplicacao="", foto_spec={"rect": [28, 90, 120, 225]})
AJ["cod:4921610"] = dict(descricao="FILTRO MAN AR TGX 29440 33440 212 FABR161S", tipo="FILTRO DE AR",
    cod_ref="MAN 81084050021 / MAN 81084050016 / MAN 81084050020",
    variacoes="Mann Filter / Tecfil (logos): C271250/1 / ARS9842 / Mann EU C271250/1 / Tecfil ARS9842 / Hengst E428L01 / Vox HD9842 / "
              "Fleetguard AF25894 / Filfilter HP2592 / Baldwin RS4971 / Mahle LX1024 / Donaldson P782936 / Wega WAP120",
    info="OBSERVAÇÕES: aplicado com filtro de segurança FS161S", montadora="MAN, Volkswagen", aplicacao="",
    foto_spec={"rect": [28, 270, 112, 444]})
AJ["cod:4920473"] = dict(descricao="FILTRO VW MAN 17.280 OLEO WEGA WOE473", tipo="FILTRO DE ÓLEO", marca="Wega",
    cod_ref="Volkswagen 07W115436 / M. Benz 51055040096 / Man 51055040096",
    variacoes="Baldwin P7145 / Donaldson P576664 / Fleetguard Lf3754 / Gonher G3754 / Hengst E161HD28 / Japanparts FOECO015 / "
              "Luberfiner Lp8741 / Mahle OX155D / Mann HU947/2X / Original Filter OFL0535E / Parker / Racor REL814 / Purolator L1957 / "
              "Sakura EO68020 / Tecfil PEL2011 / Ufi 2500500 / Vox LE2011 / Wega WOE473 / Wix 57711 / Wix WI57711",
    info="", montadora="Volkswagen, MAN, Mercedes-Benz", aplicacao="", foto_spec={"rect": [298, 105, 380, 260]})
AJ["cod:4920805"] = dict(descricao="FILTRO VW MAN 17260 COMB WEGA FCD0805", tipo="FILTRO DE COMBUSTÍVEL", marca="Wega",
    cod_ref="Volkswagen 2V3127177", variacoes="Mann PU9218 / Racor RE160LJ10MAQII / Racor RE-160LJ-10M-AQII",
    info="", montadora="Volkswagen, MAN", aplicacao="", foto_spec={"rect": [298, 280, 420, 440]})

# pág. 135: tabelas de 3 colunas "Código Wega | Código Concorrente | Marca" lidas do texto do PDF
import json as _json, os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "scripts"))
from capitulos import WORK as _WORK  # noqa: E402


def _tab3(pag, prefixo, y0, y1):
    raw = _json.load(open(_os.path.join(_WORK, "raw", f"p{pag:03d}.json"), encoding="utf-8"))
    spans = [s for c in raw["cards"] for ln in c["lines"] for s in ln if y0 <= s["y"] <= y1 and s["size"] < 9]
    linhas = {}
    for s in spans:
        linhas.setdefault((round(s["y"]), s["x"] > 420), []).append(s)
    pares = []
    for k in sorted(linhas, key=lambda k: (k[1], k[0])):
        toks = [s["t"].strip() for s in sorted(linhas[k], key=lambda s: s["x"]) if s["t"].strip()]
        if toks and toks[0].startswith(prefixo) and len(toks) >= 3:
            pares.append((" ".join(toks[2:]), toks[1]))
    return pares


_OEMS = ("Volvo", "Chevrolet", "Deutz", "CNH", "MWM", "GM", "Ford", "Iveco", "Mercedes", "M. Benz", "Scania", "Volkswagen", "Cummins")
for _cod, _pre, _y0, _y1, _desc, _tipo in (
        ("4922400", "WO-480", 88, 420, "FILTRO VW OLEO LUBRIFICANTE FOBR24S", "FILTRO DE ÓLEO"),
        ("4920346", "WEO-0512", 88, 420, "FILTRO VW DIRECAO HIDRAULICA WEO0512", "FILTRO HIDRÁULICO")):
    _p = _tab3(135, _pre, _y0, _y1)
    AJ["cod:" + _cod] = dict(
        descricao=_desc, tipo=_tipo, marca="Wega",
        cod_ref=" / ".join(f"{m} {c}" for m, c in _p if m.startswith(_OEMS)),
        variacoes=f"Código Wega {_pre} / " + " / ".join(f"{m} {c}" for m, c in _p if not m.startswith(_OEMS)),
        info="")
AJ["cod:4922400"]["variacoes"] = "Mann Filter (logo): W962 / " + AJ["cod:4922400"]["variacoes"]
AJ["cod:4922400"]["montadora"] = "Volkswagen"
AJ["cod:4922215"] = dict(descricao="FILTRO VOLKSWAGEN COMB FCD2215", marca="Wega", montadora="Volkswagen, Agrale", info="",
    cod_ref="Agrale 6008006040007 / Volkswagen 2R0201511 / Volkswagen 2R0127177 / Volkswagen 2RO127177",
    variacoes="Bosch 986450729 / Delkraft DSA518/1 / Delphi EFS110 / Donaldson P550897 / Japanparts FCBR85S / KSPG 50013871 / "
              "Mann WK950/14 / Master Parts MM100351 / MWM 60 / Seineca Antigo SEI2654 / Sogefi Pro / Fram FP6302 / Tecfil PSD970/1 / "
              "TRP 915025 / Turbo Filtros TBC970 / Vox FBS970/1 / Vox Antigo FBS2627")
AJ["cod:4920287"] = dict(descricao="FILTRO VOLVO AR WAP287/S", marca="Wega", montadora="Volkswagen", info="",
    cod_ref="",
    variacoes="American Motors Corp AE20100 / American Motors Corp SFA1600S / Land Rover 36014523 / Liebherr 510659308 / "
              "Liebherr Cf1600 / ASAS Hf347 / Atlas Copco 161956900 / Atlas Copco 16195699 / Loesing 24058 / Logan CFA518M")
AJ["cod:4920710"] = {"-variacoes": r"LUBRIFICANTE Wo710", "-info": r"FILTR[^|]*", "marca": "Wega", "montadora": "Volkswagen"}
AJ["cod:4926600"] = {"-variacoes": r"Fabricante C[óo]digo"}
AJ["cod:4920711"] = dict(cod_ref="Ford 3318853 / Ford 3825970", marca="Wega", info="",
    variacoes="AC Delco PF1217 / Advance Mixer 15067 / Advance Mixer A3000 / AG Chem Equipment 711049 / AG Chem Equipment AG711049 / "
              "Fil ZP51 / Filfilter ZP3051 / Fleetguard LF9009 / Massey Ferguson 72501533 / Massey Ferguson 72516560 / "
              "Master Parts MM100225 / McCormick 707154A1 / Mi-Jack 23160167")
AJ["cod:4920101"] = {"-variacoes": r"OBSERVA[ÇC][ÕO]ES: FAADF01", "+info": "OBSERVAÇÕES: FAADF01"}
AJ["cod:4920210"] = {"tipo": "FILTRO DE ÓLEO", "marca": "Wega", "montadora": "Mercedes-Benz, MAN", "-variacoes": r" \.(?= |$)"}
AJ["cod:4920199"] = {"marca": "Wega"}
AJ["cod:4922277"] = {"marca": "Wega", "montadora": "New Holland, Case"}
AJ["cod:4920277"] = {"marca": "Wega"}
AJ["cod:4926100"] = dict(descricao="FILTRO IVECO SEP C/COPO FIXO FCBR61S", tipo="COPO FILTRO", montadora="Iveco, Mercedes-Benz",
    cod_ref="Original A4570920001Kz / Mercedes-Benz 4570920001 / P502461", info="Wega FCD3091/1 / FCBR61S / KC647/1 / Plus PSD480/6 / WK1050/1 Iveco",
    variacoes="Mann WK1050/1 / Wega FCD3090/1 / Mahle KC647D / KC126/1 / Parker R9030Mb / Tecfil PSD480/1 / Turbo Filtros TBC480 / "
              "Vox FBS480/1 / Racor R12010Mb / R12030M / Japanparts FCBR83S")
AJ["cod:4922124"] = {"-variacoes": r"Conversões: ", "montadora": "Iveco"}
MANUAIS = {150}
ADD += [
    dict(pagina=150, card=1, codigo="5062262", descricao="MB FILTRO SECADOR AR 1620 MASTER", tipo="FILTRO SECADOR DE AR",
         cod_ref="100000216083", marca="Master", montadora="Mercedes-Benz, Volvo, MAN, Agrale, Iveco, Ford",
         foto_spec={"rect": [35, 95, 160, 250]}),
    dict(pagina=150, card=2, codigo="5061604", descricao="FILTRO APU SEC AR TECFIL - DSF0203 SCANIA TDS", tipo="FILTRO SECADOR DE AR",
         marca="Tecfil", montadora="Scania", aplicacao="Scania P 310 2005 a 2021", foto_spec={"rect": [35, 290, 180, 450]}),
    dict(pagina=150, card=3, codigo="5118262", descricao="COPO VOLVO FILTRO RACOR 20478262", tipo="COPO FILTRO",
         cod_ref="204788262 (ref. original impressa)", montadora="Volvo", foto_spec={"rect": [360, 495, 575, 625]}),
    dict(pagina=150, card=4, codigo="9910130", descricao="CINTA PARA FILTRO SECADOR DE AR", tipo="FERRAMENTA (CINTA SACA FILTRO)",
         cod_ref="101020", aplicacao="Motores Mercedes-Benz", montadora="Mercedes-Benz",
         info="Saca filtro de óleo tipo cinta com abertura de 134 a 137mm | 101020 impresso em vermelho no card",
         foto_spec={"rect": [290, 650, 410, 740]}),
]
