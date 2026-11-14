# Capítulo 12 - Sistema de Direção (págs. 151-157): rolamentos, cruzetas, rolamentos de cardan, terminais de direção
import json as _json, os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "scripts"))
from capitulos import WORK as _WORK  # noqa: E402

MANUAIS = {151}
LIMPA_DESC = [r"\bA:\s*B:", r"\bA:\s*$", r"\bB:\s*$", r"\bA:(?=\s)", r"\bB:(?=\s|$)", r"VEÍCULOS APLICÁVEIS.*$"]
TIPOS = [
    (r"CRUZETA", "CRUZETA"), (r"ROL\.?\s*CARDAN|BOR\.?\s*ROL|ROLAMENTO CARDAN", "ROLAMENTO CARDAN (CENTRO)"),
    (r"ROLAMENTO", "ROLAMENTO"), (r"TER\.? DIR|TERMINAL DIR|TTER", "TERMINAL DE DIREÇÃO"), (r"TIRANTE", "TERMINAL TIRANTE"),
]

# pág. 151: lista de rolamentos (um card) + cards próprios
_raw = _json.load(open(_os.path.join(_WORK, "raw", "p151.json"), encoding="utf-8"))
_sp = [s for c in _raw["cards"] for ln in c["lines"] for s in ln]
_lista = []
for _s in _sp:
    if not (_s["red"] and _s["t"].strip().isdigit()):
        continue
    if _s["y"] > 575:
        continue
    _txt = [t for t in _sp if not t["red"] and abs(t["y"] - _s["y"]) < 3 and 0 < t["x"] - _s["x1"] < 30]
    if not _txt:
        _txt = [t for t in _sp if not t["red"] and 0 < t["y"] - _s["y"] < 3 and abs(t["x"] - _s["x"]) < 60]
    if _txt:
        _d = " ".join(t["t"] for t in _txt)
        _d = _d.replace("ROLAMENTO33022", "ROLAMENTO 33022 ").replace("ROLAMENTO33213", "ROLAMENTO 33213 ").replace("ROLAMENTO3782", "ROLAMENTO 3782")
        _lista.append((_s["t"].strip(), _d))
_MARCAS = ("OBM", "VTO", "GIRHOS", "SKF", "TIMKEM", "MERITOR", "SUSPENSYS")
ADD = [dict(pagina=151, card=1, codigo=c, descricao=d, tipo="ROLAMENTO", _titulo="ROLAMENTOS (LISTA)",
            marca=", ".join(m.title() for m in _MARCAS if m in d.upper()), foto_spec={"rect": [336, 98, 526, 209]})
       for c, d in _lista]
ADD += [
    dict(pagina=151, card=2, codigo="5540331", descricao="ROLAMENTO 32218 SKF", tipo="ROLAMENTO", marca="SKF",
         foto_spec={"rect": [176, 608, 290, 671]}),
    dict(pagina=151, card=3, codigo="5543585", descricao="ROLAMENTO 3585/3525 OBM", tipo="ROLAMENTO", marca="OBM",
         foto_spec={"rect": [448, 586, 536, 669]}),
    dict(pagina=151, card=4, codigo="55432309", descricao="ROLAMENTO 32309 TIMKEM", tipo="ROLAMENTO", marca="Timken",
         montadora="Mercedes-Benz, Scania", info="Diâmetro externo 100 mm | Diâmetro interno 45 mm | Largura 38,25 mm",
         foto_spec={"rect": [154, 710, 292, 800]}),
    dict(pagina=151, card=5, codigo="554802601", descricao="ROLAMENTO 802601 MERITOR", tipo="ROLAMENTO", marca="Meritor",
         montadora="Volkswagen, Ford", aplicacao="Rolamento cubo traseiro ext. Ford Cargo Volks Meritor", cod_ref="802601 (580/572)",
         foto_spec={"rect": [486, 677, 564, 779]}),
    dict(pagina=151, card=6, codigo="554802737", descricao="ROLAMENTO 802737 MERITOR", tipo="ROLAMENTO", marca="Meritor",
         montadora="Volkswagen, Ford", aplicacao="Rolamento roda dianteira interno", cod_ref="2RH498628 / 802737 / 2S0498625",
         foto_spec={"rect": [486, 677, 564, 779]}),
]
AJ = {"152.1": {"marca": "", "tipo": "CRUZETA"}}
NOTAS = ["p151: a lista de rolamentos é um card só (1 produto com variações); os rolamentos que também têm card próprio (32218 SKF, 3585 OBM, 32309 Timken, 802601 e 802737 Meritor) aparecem também em linha própria."]
_V = "Volkswagen, Mercedes-Benz"
AJ.update({
    "cod:5061102": dict(cod_ref="", variacoes="Códigos similares: R-252AR | Rol. 88.508", montadora=_V),
    "cod:5061620": dict(cod_ref="", variacoes="Códigos similares: R-252R / R-778R / 88509CB | Rol. 88.509",
                        montadora="Mercedes-Benz, Volkswagen, GM, Ford, Volvo, Iveco, Renault"),
    "cod:5061104": dict(cod_ref="Volkswagen TMJ.521.117 / Ford BD7T.4826-A", variacoes="Códigos similares: R-253R / R-632R / 88510CB | Rol. 88.510",
                        montadora="Mercedes-Benz, Volkswagen, Ford, Volvo, Iveco, Renault"),
    "cod:5068512": dict(cod_ref="", variacoes="Códigos similares: R-3319R / R-752R / 88512CB | Rol. 88.512",
                        montadora="Mercedes-Benz, Volkswagen, Scania, Ford, Volvo, Iveco, Renault"),
    "cod:5061114": dict(cod_ref="345.410.0051", variacoes="R-006R", montadora="Mercedes-Benz"),
    "cod:5063031": dict(cod_ref="1.113.031", variacoes="Códigos similares: FL-124 / R362 / R4011", montadora="Scania"),
})
for _c in ("4972061", "4972060", "4972039", "4972038", "4972048", "4972028", "4972053", "4979105", "4977014", "4977015",
           "4977005", "4977370", "4974091", "4979106", "4979104", "4979103"):
    AJ.setdefault("cod:" + _c, {})["marca"] = "ZM"
AJ["cod:4972048"]["montadora"] = "Mercedes-Benz, DAF"
AJ["cod:4979105"]["montadora"] = "Volkswagen, Ford, Mercedes-Benz"
AJ["cod:4974091"]["montadora"] = "Scania, MAN"
AJ["cod:4979104"]["montadora"] = "Volkswagen, Ford, Mercedes-Benz"
AJ["cod:4979103"]["montadora"] = "Volkswagen, Ford, Mercedes-Benz"
AJ.setdefault("cod:4970641", {})["descricao"] = "TER DIR VW DIREITO CAM 8120 T06415712"
AJ["cod:4970641"]["montadora"] = "Volkswagen"
NOTAS += ["Terminais de direção (págs. 154-157): 'A' e 'B' do desenho (comprimento e rosca) ficam em Informações adicionais; códigos Nakata/TRW/ZL em Código ref.",
          "Marca ZM registrada apenas onde a peça aparece com a marcação ZM na foto.",
          "p155 card 5 e p156 card 6: espaços vazios no catálogo."]
AJ["cod:4970641"]["tipo"] = "TERMINAL DE DIREÇÃO"
