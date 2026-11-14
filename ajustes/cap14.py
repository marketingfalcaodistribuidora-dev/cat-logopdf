# Capítulo 14 - Quinelato (págs. 172-182)
# Págs. 172-177: grade de reparos Quinelato — código vermelho + descrição abaixo da imagem; o texto dentro da
# imagem (embalagem/rótulo "QA-xxxx JOGO DE REPARO ...") é a própria foto do produto.
import json as _json, os as _os, sys as _sys, re as _re
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "scripts"))
from capitulos import WORK as _WORK  # noqa: E402

TIPOS = [(r"SPRING|TRISTOP|CUICA|CIL", "REPARO CUÍCA / SPRING BRAKE"), (r"SECADOR|APU", "REPARO SECADOR DE AR / APU"),
         (r"MANETIN|MANETE", "REPARO VÁLVULA MANETE"), (r"RELE|RE-4|DESCARGA|PEDAL|PROT|V\b|VALV|VAUVULA|VL\b", "REPARO VÁLVULA"),
         (r"COMPRES|CABECOTE|CAMECOTE", "REPARO COMPRESSOR"), (r"SERVO|EMBREAG", "REPARO SERVO EMBREAGEM"),
         (r"PARAF|PF DESAT", "PARAFUSO DESATUADOR"), (r"REP|JG|REPARO|KIT", "JOGO DE REPARO")]


def _cells_auto(pag, ncols=3, x0=25, x1=570, desce=35):
    raw = _json.load(open(_os.path.join(_WORK, "raw", f"p{pag:03d}.json"), encoding="utf-8"))
    sp = [s for c in raw["cards"] for ln in c["lines"] for s in ln]
    cods = sorted([s for s in sp if s["red"] and _re.fullmatch(r"\d{6,10}", s["t"].strip()) and s["size"] >= 14], key=lambda s: s["y"])
    linhas = []
    for s in cods:
        if linhas and abs(linhas[-1][-1]["y"] - s["y"]) < 40:
            linhas[-1].append(s)
        else:
            linhas.append([s])
    w = (x1 - x0) / ncols
    cells, topo = [], 85
    for ln in linhas:
        base = max(s["y"] for s in ln) + desce
        for j in range(ncols):
            cells.append([x0 + j * w, topo, x0 + (j + 1) * w, base])
        topo = base
    return cells


GRADES = {p: {"cells": _cells_auto(p), "fonte": 7, "cod_min": 14} for p in (172, 173, 174, 175, 176, 177)}
AJ = {}
ADD = []
NOTAS = ["Págs. 172-177 (Quinelato): a descrição é a linha impressa abaixo do código; o título técnico (QA-xxxx Jogo de reparo...) está dentro da foto de cada item.",
         "Código QA de cada reparo registrado em 'Código ref.'."]


def POS_PROC(r):
    if r["pagina"] <= 177:
        m = _re.match(r"^\s*(QA-?\s?[\w/.-]+)", r.get("descricao") or "")
        if m and m.group(1).replace(" ", "") not in (r.get("cod_ref") or ""):
            r["cod_ref"] = "Quinelato " + m.group(1).replace(" ", "") + ((" / " + r["cod_ref"]) if r.get("cod_ref") else "")
        r["marca"] = r.get("marca") or "Quinelato"
ADD += [dict(pagina=177, card=12, codigo="4001857", descricao="QA-18057 REPARO DOSADORA FASEII", tipo="JOGO DE REPARO",
             aplicacao="Mercedes Accelo 2012 a 2015 / Actros / Atego / Axor / O-500", montadora="Mercedes-Benz",
             info="Logos Axor / Atego / Actros / Accelo", foto_spec={"rect": [402, 650, 520, 760]})]
AJ.update({
    "cod:4001160": dict(descricao="QA-1160 REP PARCIAL SERVO FREI", cod_ref="2S2129601A", montadora="Mercedes-Benz",
                        info="Reparo servo freio compl. 608 s/ pistão MB"),
    "cod:4000170": dict(descricao="QA-170 BUCHA P/ TAMPA TRASEIRA", cod_ref="T06145661B", montadora="Volkswagen",
                        info="Bucha traseira compressor ar sistema Varga VW 690 790 7110s", tipo="REPARO COMPRESSOR"),
    "cod:4001320": dict(descricao="QA-1320 GUARDA PO SERVO EMB", cod_ref="0002956983 (Mercedes-Benz) / 2RP721437 (Volkswagen) / 8977541824 (Wabco)",
                        montadora="Mercedes-Benz, Volkswagen", info="Guarda-pó servo embreagem"),
})
AJ["cod:4000266"] = dict(descricao="QA-266 REP PARCIAL CUICA 30X30", info="Reparo parcial spring brake Volvo VM17", montadora="Volvo")
AJ["cod:4002040"] = dict(tipo="REPARO SECADOR DE AR / APU")
_M178 = {"4001527": "Volkswagen", "4001061": "Volkswagen", "4002613": "Mercedes-Benz", "4002024": "Volvo", "40011667": "Iveco, Volvo",
         "4002017": "Iveco", "4000881": "Scania", "4000952": "Scania", "4006160": "Volkswagen", "4001673": "Mercedes-Benz", "4001099": "Scania"}
for _c, _m in _M178.items():
    AJ.setdefault("cod:" + _c, {}).update(montadora=_m, marca="Quinelato")
AJ["cod:4001527"]["aplicacao"] = "13/15170/17210/300/18310/40300..."
AJ["cod:40011667"].update(cod_ref="", variacoes="Similar 090312 / 22101753")
AJ["cod:4001099"].update(cod_ref="II 35.254 / 1.408.333 / DFR9325 / DPM98A / DPM98B", info="")
AJ["cod:4002613"]["info"] = "Logos Actros / Axor"
NOTAS.append("p178: o card 4001527 aparece duas vezes na página.")
GRADES[179] = {"rows": [85, 266, 449, 629], "cols": [20, 205, 390, 575], "fonte": 7, "cod_min": 9}
AJ.update({
    "cod:8790003": dict(descricao="VALVULA DESC RAPIDA 20 MM X 1/2 POLEGADA ADER 890300", tipo="VÁLVULA", cod_ref="ADER 890300",
                        info="1/4 polegada / 1/4 polegada / 1/2 MM"),
    "cod:8790006": dict(descricao="VALVULA DESC RAPIDA 16 MM X 16 MM MBB TODOS MERCEDES", tipo="VÁLVULA", montadora="Mercedes-Benz", info="16MM / 16MM / 16MM"),
    "cod:8790005": dict(descricao="VALVULA DESC RAPIDA 16 MM X 22 MM 1,5 SEMI-REB RANDON", tipo="VÁLVULA", montadora="Randon", info="16MM / 16MM / 22MM"),
    "cod:8790007": dict(descricao="VALVULA DESC RAP VW/FORD 1/4X3/8", tipo="VÁLVULA", cod_ref="TJG407610A", montadora="Volkswagen, Ford",
                        info="1/2 polegada / 1/2 polegada / 16 MM"),
    "cod:8791414": dict(descricao="VALVULA DESC RAPIDA 1/4X1/4NPT", tipo="VÁLVULA", info="1/4 polegada"),
    "cod:8002940": dict(descricao="VALVULA TIC-TAC 1/4 NPT CARRET", tipo="VÁLVULA", info=""),
    "cod:8002941": dict(descricao="VALVULA TIC-TAC 16X1,5 CARRETA", tipo="VÁLVULA", info=""),
})
for _c in ("8790003", "8790006", "8790005", "8790007", "8791414", "8002940", "8002941"):
    AJ["cod:" + _c]["marca"] = ""
GRADES[180] = {"cells": [[20, 85, 208, 260], [208, 85, 391, 260], [391, 85, 575, 260], [20, 260, 391, 447], [391, 260, 575, 447],
                         [20, 447, 208, 612], [208, 447, 391, 629], [391, 447, 575, 570], [391, 570, 575, 685],
                         [20, 612, 208, 706], [208, 629, 391, 808], [20, 706, 208, 808], [391, 685, 575, 808]], "fonte": 9, "cod_min": 9}
AJ.update({
    "cod:5061512": dict(descricao="CILINDRO ACION ACELERADOR MB L 1620 1618 1621 1218 1418 LS1632 1935", tipo="CILINDRO ACIONADOR",
                        cod_ref="1727377 / 0000721512", info="", montadora="Mercedes-Benz", marca=""),
    "cod:5066026": dict(descricao="MB CILINDRO FREIO MOTOR 1620", tipo="CILINDRO FREIO MOTOR", cod_ref="000.430.4926",
                        aplicacao="Accelo / Atego 1218/1315/1518/1718", info="Niple 12mm", montadora="Mercedes-Benz", marca=""),
    "cod:5060126": dict(descricao="MB CILINDRO FREIO MOTOR 352 L1114/1316/1318/1518", tipo="CILINDRO FREIO MOTOR", cod_ref="000.430.0126",
                        info="224MM (furo cabeça pistão até o final do eixo roscado)", montadora="Mercedes-Benz", marca=""),
    "cod:8000689": dict(descricao="+DRENO BALÃO DE AR M22", tipo="DRENO", marca="", info=""),
    "cod:8000522": dict(descricao="DRENO BALAO AR 1/2 VW / FORD", tipo="DRENO", marca="", montadora="Volkswagen, Ford", info=""),
    "cod:8001992": dict(descricao="REGISTRO TORNEIRA BALAO AR MACHO 1/4 X 1/4 FEMEA TODOS", tipo="REGISTRO", marca="",
                        info="1/4 macho / 1/4 fêmea | Polegada x milímetro: 1/4 = 12,6M"),
    "cod:8001993": dict(descricao="REGISTRO TONEIRA BALAO AR M 1/4 X F 1/4 NPT BORBOLETA", tipo="REGISTRO", marca="",
                        info="1/4 macho / 1/4 fêmea | Polegada x milímetro: 1/4 = 12,6M"),
    "cod:8001995": dict(descricao="REGISTRO AR CARRETAS 1/4 X 1/4 NPT", tipo="REGISTRO", marca="", info="1/4 fêmea / 1/4 fêmea | 1/4 = 12,6M"),
    "cod:8001996": dict(descricao="REGISTRO AR CARRETAS 3/8 X 3/8 NPT", tipo="REGISTRO", marca="", info="3/8 fêmea / 3/8 fêmea | 3/8 = 16,44M"),
    "cod:8001997": dict(descricao="REGISTRO AR CARRETAS 1/2 X 1/2 NPT", tipo="REGISTRO", marca="", info="1/2 fêmea / 1/2 fêmea | 1/2 = 20,07M"),
    "cod:8001994": dict(descricao="TORNEIRA TANQUE KIT ADAP VW", tipo="REGISTRO", marca="", montadora="Volkswagen", info=""),
})
for _c in ("8005170", "8005180", "8005190", "8005191", "8000414"):
    AJ["cod:" + _c] = {"tipo": "VÁLVULA ESFERA MINI", "marca": "", "info": ""}
for _c in ("6021212", "6021214", "60114516"):
    AJ["cod:" + _c] = {"tipo": "ESPIGÃO FIXO", "marca": "", "info": "Mang / Rosca M"}
GRADES[180]["cod_min"] = 6
_ESF = {"8005170": "VALVULA ESFERA MINI FEMEA 1/2 X F 1/2", "8005180": "VALVULA ESFERA MINI FEMEA 1/4 X F 1/4",
        "8005190": "VALVULA ESFERA MINI FEMEA 3/8 X F 3/8", "8005191": "VALVULA ESFERA MINI MACHO 3/8 X F 3/8",
        "8000414": "VALVULA ESFERA MINI MACHO 1/4 X M 1/4"}
for _c, _d in _ESF.items():
    AJ["cod:" + _c].update(descricao=_d, _titulo="VALVULA ESFERA MINI", _nao_agrupar=False)
_ESP = {"6021212": "ESPIGAO FIXO M1/2 X 1/2 MANG", "6021214": "ESPIGAO FIXO M1/2 X 1/4 MANG", "60114516": "ESPIGAO FIXO M1/4 X 5/16 MANG"}
for _c, _d in _ESP.items():
    AJ["cod:" + _c].update(descricao=_d, _titulo="ESPIGAO FIXO", _nao_agrupar=False)
AJ["181.1"] = {"_titulo": "CORREIA CONTITECH", "marca": "Contitech", "tipo": "CORREIA"}
GRADES[182] = {"rows": [85, 255, 422, 571, 686, 808], "cols": [20, 208, 391, 575], "cols_linha": {4: [20, 297, 575]},
               "fonte": 7.5, "cod_min": 9}
TIPOS.insert(0, (r"TENSOR|TENSIONADOR", "TENSOR POLIA / CORREIA"))
TIPOS.insert(0, (r"CHAVE SETA", "CHAVE DE SETA"))
AJ.update({
    "cod:5062570": dict(cod_ref="5412002570", montadora="Mercedes-Benz", marca=""),
    "cod:5061970": dict(cod_ref="4572001970", montadora="Mercedes-Benz", marca=""),
    "cod:5063270": dict(cod_ref="4572003270", montadora="Mercedes-Benz", marca=""),
    "cod:5066191": dict(cod_ref="504046191", montadora="Iveco", marca=""),
    "cod:5113113": dict(cod_ref="1503113", montadora="Scania", marca=""),
    "cod:5062181": dict(cod_ref="1512181", montadora="Scania", marca=""),
    "cod:5061534": dict(cod_ref="1503114", montadora="Scania", marca=""),
    "cod:5064315": dict(cod_ref="3154315", montadora="Volvo", marca=""),
    "cod:5068408": dict(cod_ref="20739751 / 20935521 / 21422765", montadora="Volvo", marca="Vetor", info="LANÇAMENTO"),
    "cod:5119980": dict(cod_ref="3979980", montadora="Volvo", marca=""),
    "cod:5062051": dict(montadora="Volkswagen", marca=""),
    "cod:5161703": dict(descricao="TENSOR CORR ALTER VOLVO FH2003 DT", aplicacao="Volvo FH13, FM13 e FMX", cod_ref="", montadora="Volvo", marca=""),
    "cod:5500124": dict(descricao="CHAVE SETA SCANIA S4 CINZA 1402448C", cod_ref="1402448C", montadora="Scania", marca=""),
    "cod:5505409": dict(descricao="CHAVE SETA VOLVO FH12", cod_ref="3172170", variacoes="REF similar Volvo 202339", montadora="Volvo", marca=""),
})
NOTAS.append("p182: tensores e chaves de seta aparecem sob o cabeçalho QUINELATO no catálogo.")
AJ["cod:5068408"].update(descricao="TENSOR CORR ALTER VOLVO FH13/FH400/FH4800", tipo="TENSOR POLIA / CORREIA")
AJ["cod:5062570"]["descricao"] = "TENSOR POLIA ALTERNADOR POLIA LISA MB MERCEDES BENZ ACTROS"
