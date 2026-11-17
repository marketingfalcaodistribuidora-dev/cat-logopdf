# Capítulo 26 - Para-lamas e Suportes (págs. 368-375)
TIPOS = [(r"CALCO DE RODA|CAL[ÇC]O DE RODA", "CALÇO DE RODA"), (r"ABRA[CÇ]|^ABRAC", "ABRAÇADEIRA DE PARA-LAMA"),
         (r"SUPORTE|^SUP\b|^SUP ", "SUPORTE DE PARA-LAMA"), (r"PARALAMA|PARA-LAMA|PARA LAMA", "PARA-LAMA")]
AJ = {
    "cod:5063145": {"descricao": "SUPORTE PARALAMA MULTIFUROS REFORCADO UNIVERSAL"},
    "cod:7091359": {"marca": "GRSul", "aplicacao": "Suporte de apoio do para-lama traseiro lado esquerdo compatível Volvo FH a partir de 2015"},
    "cod:7091358": {"marca": "GRSul", "aplicacao": "Suporte de apoio do para-lama traseiro lado direito compatível Volvo FH a partir de 2015"},
    "cod:7094013": {"marca": "GRSul", "cod_ref": "23745207", "montadora": "Volvo",
                    "aplicacao": "Abraçadeira interna do para-lama plástico compatível Volvo FH a partir de 2015"},
    "cod:7094012": {"marca": "GRSul", "cod_ref": "23730878", "montadora": "Volvo",
                    "aplicacao": "Abraçadeira externa do para-lama plástico compatível Volvo FH a partir de 2015"},
}
ADD = []
NOTAS = ["Pág. 369: molduras vazias na metade de baixo."]

MANUAIS = {370, 371}
RP = "Rodoplast"


def N(p, c, d, rect, **kw):
    ADD.append(dict(dict(pagina=p, card=len([r for r in ADD if r["pagina"] == p]) + 1, codigo=c, descricao=d, cod_ref="",
                         variacoes="", aplicacao="", info="", marca=RP, montadora="", _nao_agrupar=True,
                         foto_spec={"rect": rect}), **kw))


# 370 (Rodoplast - Facchini / Guerra)
N(370, "8956620", "PARALAMA INTEIRO FACCHINI SINGLE PRETO", [44, 189, 244, 341], montadora="Facchini", variacoes="Rodoplast 006620",
  cod_ref="0313140002")
N(370, "8957854", "PARALAMA INTEIRO FACCHINI 2012", [372, 205, 572, 341], montadora="Facchini", variacoes="Rodoplast 007854",
  cod_ref="0313360902")
for _c, _d, _ref, _r in [("8956627", "PARALAMA INTEIRO GUERRA 2010 CH 5,5", "006627", [52, 485, 228, 597]),
                         ("8956516", "PARALAMA MEIO GUERRA 2010 DIANTEIRO DIREITO", "006516", [260, 485, 396, 605]),
                         ("8956517", "PARALAMA MEIO GUERRA 2010 DIANTEIRO ESQUERDO", "006517", [428, 485, 572, 605]),
                         ("8956518", "PARALAMA MEIO GUERRA 2010 TRASEIRO DIANTEIRO", "006518", [196, 685, 316, 797]),
                         ("8956519", "PARALAMA MEIO GUERRA 2010 TRASEIRO ESQUERDO", "006519", [476, 685, 572, 797])]:
    N(370, _c, _d, _r, montadora="Guerra", variacoes="Rodoplast " + _ref, aplicacao="Guerra 2010 CH 5,5")
# 371 (Randon / Volvo)
N(371, "8950008", "PARALAMA INTEIRO RANDON 2007 ANTIDERRAPANTE", [36, 133, 212, 245], montadora="Randon", cod_ref="208007595")
N(371, "89512004", "PARALAMA INTEIRO RANDON 2008 S/LOGO TIPO", [324, 125, 500, 229], montadora="Randon",
  info="Para-lama Randon injetado 2008")
N(371, "8955042", "PARALAMA MEIO RANDON 2007 DD/TE S/LOGO", [140, 293, 260, 429], montadora="Randon")
N(371, "8955043", "PARALAMA MEIO RANDON 2007 DE/TD S/LOGO", [332, 285, 468, 429], montadora="Randon")
N(371, "89512009", "PARALAMA MEIO RANDON INJETADO DIANT DIREITO / TRAS ESQUERDO S/LOGO TIPO", [100, 469, 276, 605],
  montadora="Randon", info="Meio para-lama RD injetado 2008/... DD/TE s/logotipo")
N(371, "89512008", "PARALAMA MEIO RANDON INJETADO DIANT ESQUERDO / TRAS DIREITO S/LOGO TIPO", [396, 469, 572, 605],
  montadora="Randon", info="Meio para-lama RD injetado 2008/... DE/TD s/logotipo")
N(371, "89511312", "CALÇO DE RODA PARA RODOVIÁRIO", [164, 701, 284, 797], marca="",
  info="Calço de roda rodoviário: ferramenta para garantir a segurança do veículo durante paradas e manobras")
N(371, "5114394", "PARALAMA VOLVO TRASEIRO TRACAO LD 21094394", [324, 685, 468, 797], montadora="Volvo", cod_ref="21094394", marca="")
# 372 (Rodoplast - Mercedes)
MANUAIS.add(372)
MB = "Mercedes-Benz"
_AX = "Axor 2041, 2540, 2544, 4140 após 2006 (fora de estrada)"
N(372, "8956606", "PARALAMA INTEIRO MERCEDES 1938 LS CINZA CLARO", [372, 173, 516, 277], montadora=MB, variacoes="Rodoplast 006606",
  aplicacao="Para-lama tração Mercedes-Benz 1938 LS cinza claro")
N(372, "8956503", "PARALAMA MEIO MERCEDES AXOR TRASEIRO L/ESQU", [100, 301, 204, 397], montadora=MB, aplicacao=_AX)
N(372, "8956502", "PARALAMA MEIO MERCEDES AXOR TRAS L/DIREITO", [276, 301, 380, 397], montadora=MB, aplicacao=_AX)
N(372, "8956080", "CENTRO PARALAMA MERCEDES AXOR", [420, 289, 572, 397], montadora=MB, aplicacao=_AX)
N(372, "8958196", "PARALAMA P CENTRO COM TRAVA MERCEDES AXOR", [156, 469, 292, 581], montadora=MB)
N(372, "8956501", "PARALAMA MEIO MB AXOR/ACTROS DIANTEIRO L/ESQ", [100, 645, 196, 749], montadora=MB, cod_ref="A9305200119",
  aplicacao="Mercedes-Benz Actros / Mercedes-Benz Axor")
N(372, "8956500", "PARALAMA MEIO MB AXOR/ACTROS DIANTEIRO L/DIR", [276, 645, 372, 749], montadora=MB, cod_ref="A9305200119",
  aplicacao="Mercedes-Benz Actros / Mercedes-Benz Axor")
N(372, "8958182", "PRESILHA PARALAMA MB AXOR/ACTROS", [404, 653, 532, 717], montadora=MB,
  aplicacao="Actros 2648, 2548, 2553, 2653 após 2020", tipo="PRESILHA DE PARA-LAMA")
# 373 (Rodoplast - Actros 2022)
for _c, _ref, _pos in (("89512190", "012190", "Dianteiro LE"), ("89512163", "012163", "Dianteiro LD"),
                       ("89512191", "012191", "Traseiro LE"), ("89512189", "012189", "Traseiro LD")):
    AJ["cod:" + _c] = {"cod_ref": "", "variacoes": "Rodoplast " + _ref, "marca": RP, "montadora": MB, "info": "",
                       "aplicacao": f"Para-lama envolvente compatível com Mercedes-Benz Actros 2022/... - {_pos} | Actros de 2010 em diante"}
# 374 (Rodoplast - Scania / Librelato)
MANUAIS.add(374)
N(374, "8956671", "PARALAMA INTEIRO SCANIA S4/S5 GRAFITE", [358, 204, 495, 308], montadora="Scania", variacoes="Rodoplast 006671",
  aplicacao="Para-lama Scania S4 | S5 grafite CH 6,0")
for _c, _d, _ref, _r, _apl in [
        ("8956691", "PARALAMA INTEIRO UNIVERSAL LIBRELATO BI-TREM", "006691", [49, 463, 229, 557], "Para-lama universal rec Librelato bi-trem"),
        ("8957899", "PARALAMA MEIO UNIVERSAL LIBRELATO TRAS ESQUERDO", "007899", [279, 463, 366, 553], "Para-lama universal Librelato traseiro esquerdo"),
        ("8957898", "PARALAMA MEIO UNIVERSAL LIBRELATO TRAS DIREITA", "007898", [459, 463, 546, 553], "Para-lama universal Librelato traseiro direita"),
        ("8956588", "PARALAMA MEIO UNIVERSAL LIBRELATO DIANTEIRO ESQUERDO", "006588", [42, 650, 150, 747], "Para-lama universal Librelato"),
        ("8956587", "PARALAMA MEIO UNIVERSAL LIBRELATO DIANTEIRO DIREITO", "006587", [315, 650, 423, 747], "Para-lama universal Librelato")]:
    N(374, _c, _d, _r, montadora="Librelato", variacoes="Rodoplast " + _ref, aplicacao=_apl)
# 375 (parabarros)
import re  # noqa: E402

TIPOS.insert(0, (r"PARABARRO", "PARABARRO"))
TIPOS.insert(0, (r"SUPORTE PARABARRO", "SUPORTE DE PARABARRO"))
AJ.update({
    "cod:896620570": {"descricao": "PARABARRO RANDON NEW 620MM X 570MM", "montadora": "Randon", "info": ""},
    "cod:896500360": {"descricao": "PARABARRO SCANIA DIANT 500MM X 360MM", "variacoes": "P-001", "montadora": "Scania", "info": ""},
    "cod:896610380": {"descricao": "PARABARRO SCANIA TRAS 610MM X 380MM", "variacoes": "P-002", "montadora": "Scania", "info": ""},
    "cod:896590490": {"descricao": "PARABARRO VOLKSWAGEM TRANS 590MM X 490MM", "variacoes": "P-046", "montadora": "Volkswagen"},
    "cod:896690530": {"descricao": "PARABARRO GUERRA PAZ ESTRADA 690MM X 530MM", "info": "Impresso '6900MM X 530MM' | 'É paz na estrada'"},
    "cod:896700500": {"descricao": "PARABARRO CARRETA SEM LOGO 700MM X 500MM"},
})
for _c, _d, _ref, _cm in (("8960048", "SUPORTE PARABARRO 50 CM", "Ds0048", "36,75"), ("8960038", "SUPORTE PARABARRO 60 CM", "Ds0038", "36,87"),
                          ("8960039", "SUPORTE PARABARRO 70 CM", "Ds0039", "35,22")):
    AJ["cod:" + _c] = {"descricao": _d, "cod_ref": _ref, "info": f"Medida {_cm} mm"}


def POS_PROC(r):
    if str(r["pagina"]) != "375" or not r["descricao"].startswith("PARABARRO"):
        return
    d = r["descricao"]
    m = re.search(r"\s+(LANÇAMENTO \d\d/\d\d)", d)
    lanc = m.group(1) if m else ""
    d = re.sub(r"\s+LANÇAMENTO \d\d/\d\d", "", d)
    m = re.search(r"\s+((?:VOLVO FH/NH|VOLVO Fh16|Volvo|Scania S4|Caminhões).*)$", d)
    extra = m.group(1) if m else ""
    if m:
        d = d[:m.start()]
    if d.strip() == "PARABARRO" and r.get("info"):
        partes = r["info"].split(" / ")
        d = "PARABARRO " + partes[0]
        r["info"] = " / ".join(partes[1:])
        m2 = re.search(r"\s+((?:VOLVO FH/NH|VOLVO Fh16).*)$", d)
        if m2:
            extra = m2.group(1)
            d = d[:m2.start()]
    extra = (extra + " " + r.get("info", "").replace(" / ", " ")).strip()
    cod800 = re.findall(r"800\.\d{3}", extra)
    extra = re.sub(r"\s*800\.\d{3}", "", extra)
    extra = re.sub(r"\s*Material:\s*", " | Material: ", extra).strip(" |")
    r["descricao"] = d.strip()
    r["info"] = " | ".join(x for x in (lanc, extra) if x)
    if cod800:
        r["variacoes"] = "Ref. " + " / ".join(cod800)


_POS1 = POS_PROC


def POS_PROC(r):  # noqa: F811
    _POS1(r)
    if r["descricao"].startswith("PARABARRO"):
        r["tipo"] = "PARABARRO"
    elif r["descricao"].startswith("SUPORTE PARABARRO"):
        r["tipo"] = "SUPORTE DE PARABARRO"
AJ["cod:896700500"]["montadora"] = "Randon"
AJ["cod:896600500"] = {"montadora": "Randon"}
NOTAS.append("Pág. 375: os parabarros 'carreta sem logo' (896700500, 896600500) têm o logo Randon no card; 896690530 está impresso "
             "como '6900MM X 530MM'. Págs. 370-374: o código Rodoplast (00xxxx) de cada para-lama está na coluna de similares.")
