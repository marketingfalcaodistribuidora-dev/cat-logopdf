# Capítulo 15 - Mangueiras Valman (págs. 183-190)
# Os cards não trazem nome do produto, só aplicação (AP), código original e dimensão: a descrição foi montada como
# "MANGUEIRA SILICONE VALMAN <dimensão>" (marca Valman só nos códigos 537xxxxx); a montadora vem do logo do card.
import re as _re

TIPOS = [(r"RETARDER", "MANGUEIRA RETARDER"), (r"MANG|MANGUEIRA", "MANGUEIRA SILICONE")]
_PREF = {"5371": "Agrale", "5373": "Volkswagen, MAN", "5375": "Ford", "5377": "Mercedes-Benz", "5372": "Scania"}
_LOGO = {"5063352": "Volvo", "5061013": "Volvo", "5062293": "Scania", "5066382": "Mercedes-Benz", "5063813": "Volkswagen",
         "5068202": "Scania", "10011133": "Volkswagen", "5066481": "Volvo", "7750005": "Volvo", "5061012": "Volvo"}


def POS_PROC(r):
    d = r.get("descricao") or ""
    info = r.get("info") or ""
    dim = _re.search(r"DIMENS[ÃA]O:?\s*([\dxX ,.]+)", info, _re.I)
    dim = dim.group(1).strip().upper().replace(" ", "") if dim else ""
    if d.startswith("AP:"):
        r["aplicacao"] = d[3:].strip()
        r["descricao"] = ("MANGUEIRA SILICONE VALMAN " + dim).strip()
        r["tipo"] = "MANGUEIRA SILICONE"
    else:
        m = _re.search(r"\s+AP:\s*(.*)$", d)
        if m:
            r["aplicacao"] = m.group(1)
            r["descricao"] = d[:m.start()]
        mi = _re.search(r"AP:\s*([^|/]+(?:/[^|]+?)?)\s*(?:/|\|)\s*Dimens", info)
        if mi and not r.get("aplicacao"):
            r["aplicacao"] = mi.group(1).strip()
    r["info"] = ("Dimensão: " + dim) if dim else _re.sub(r"AP:.*?(?=Dimens|$)", "", info).strip(" /|")
    r["cod_ref"] = _re.sub(r"^C[ÓO]D\.?:?\s*", "", r.get("cod_ref") or "")
    r["montadora"] = _LOGO.get(r["codigo"]) or _PREF.get(r["codigo"][:4]) or r.get("montadora", "")
    r["marca"] = "Valman" if r["codigo"].startswith("537") else ""
    if not r["codigo"].startswith("537") and r["descricao"].startswith("MANGUEIRA SILICONE VALMAN"):
        r["descricao"] = r["descricao"].replace("MANGUEIRA SILICONE VALMAN", "MANGUEIRA SILICONE")


AJ = {"cod:5062293": dict(descricao="MANGUEIRA TUBO RETARDER SCANIA P/G/R 114/124", tipo="MANGUEIRA RETARDER",
                          variacoes="Similares: 1797845 / 35324 / 2155439 / 90191193", aplicacao="P / G / R 114 / 124 / 164 / 94", info=""),
      "cod:5063352": dict(descricao="MANG SIL VOLVO 065 X 085 X 270", aplicacao="NL10/NL12")}
ADD = []
NOTAS = ["Mangueiras Valman: os cards trazem só aplicação, código original e dimensão; a montadora foi lida do logo de cada card.",
         "p189: card 5063352 informa dimensão 70X70X240 no texto e 065 X 085 X 270 no título (mantidos os dois).",
         "p189 cards 9-12: vazios."]
