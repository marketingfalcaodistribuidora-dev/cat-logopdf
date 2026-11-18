# Capítulo 41 - Peças Arla 32 (págs. 465-472)
# Cards: código vermelho no canto + descrição + "APLICAÇÃO:" + "CONVERSÃO:" (números originais) -> conversão em referência.
import json
import os
import re

from capitulos import WORK
from tabela_livre import _spans

TIPOS = [(r"^TAMPA", "TAMPA ARLA"), (r"^CONEX", "CONEXÃO ARLA"), (r"^TUBO|^TUBULA", "TUBO ARLA"), (r"^SENSOR", "SENSOR ARLA"),
         (r"^ABRA", "ABRAÇADEIRA ARLA"), (r"^FILT", "FILTRO ARLA"), (r"^BICO", "BICO ARLA"), (r"^CINTA", "CINTA ARLA"),
         (r"^BOMBA", "BOMBA ARLA"), (r"^MODULO|^MÓDULO", "MÓDULO ARLA"), (r"^RESERV", "RESERVATÓRIO ARLA"), (r"^VALV", "VÁLVULA ARLA"),
         (r"^REPARO|^KIT", "REPARO / KIT ARLA"), (r"^AQUEC", "AQUECEDOR ARLA"), (r"^CHICOTE", "CHICOTE ARLA"), (r"^MANG", "MANGUEIRA ARLA")]
AJ = {}
ADD = []
NOTAS = ["Págs. 465-472 (Arla 32): os números de 'CONVERSÃO' do card (originais da montadora / similares) estão na coluna de "
         "referência; as tabelas 'Códigos de marcas equivalentes' dos filtros WEGA estão em similares."]
MANUAIS = set(range(465, 473))
_MONT = [(r"\bMB\b|MERCEDES|ATEGO|ACCELO|AXOR|ACTROS", "Mercedes-Benz"), (r"\bVW\b|VOLKS|CONSTELLATION|DELIVERY", "Volkswagen"),
         (r"FORD|CARGO", "Ford"), (r"SCANIA|\bSC\b", "Scania"), (r"VOLVO|\bFH\b|\bFM\b|\bVM\b", "Volvo"),
         (r"IVECO|STRALIS|TECTOR|TRAKKER|DAILY", "Iveco"), (r"\bDAF\b", "DAF"), (r"\bMAN\b", "MAN"), (r"CUMMINS", "Cummins")]
_LAB = re.compile(r"(APLICA[ÇC][ÃA]O\s*:|CONVERS[ÃA]O\s*:|REF\.?\s*ORIG(?:INAL)?\.?\s*:*)", re.I)


def _linhas(ss):
    out = []
    for s in sorted(ss, key=lambda s: (s["y"], s["x"])):
        if out and abs(out[-1][0] - s["y"]) < 2.5:
            out[-1][1].append(s)
        else:
            out.append([s["y"], [s]])
    return [" ".join(x["t"].strip() for x in sorted(l[1], key=lambda s: s["x"])) for l in out]


def ler(p):
    raw = json.load(open(os.path.join(WORK, "raw", f"p{p:03d}.json"), encoding="utf-8"))
    sp, imgs = _spans(p)
    regs = []
    for c in raw["cards"]:
        if not c["id"] or not c["codes"]:
            continue
        x0, y0, x1, y1 = c["rect"]
        cs = [s for s in sp if x0 - 1 <= s["x"] and s["x1"] <= x1 + 3 and y0 - 1 <= s["y"] + 2 <= y1 + 1]
        cods = [s for s in cs if s["red"] and re.fullmatch(r"\d{6,10}", s["t"].strip()) and s["size"] >= 7]
        if not cods:
            continue
        txt = re.sub(r"\s+", " ", " ".join(_linhas([s for s in cs if s not in cods and s["size"] >= 4]))).strip()
        partes = _LAB.split(txt)
        desc, apl, conv = partes[0].strip(" -"), [], []
        for k in range(1, len(partes) - 1, 2):
            (apl if partes[k].upper().startswith("APLIC") else conv).append(partes[k + 1].strip(" ,.-"))
        fotos = [b for b in imgs if x0 - 2 <= (b[0] + b[2]) / 2 <= x1 + 2 and y0 - 2 <= (b[1] + b[3]) / 2 <= y1 + 2
                 and (b[2] - b[0]) * (b[3] - b[1]) > 600]
        foto = max(fotos, key=lambda b: (b[2] - b[0]) * (b[3] - b[1])) if fotos else [x0, y0, x1, y1]
        cod = cods[0]["t"].strip()
        t = desc + " " + " ".join(apl)
        regs.append(dict(pagina=p, card=c["id"], codigo=cod, descricao=desc.upper(), cod_ref=" / ".join(conv), variacoes="",
                         aplicacao=" / ".join(apl), info="", marca="", _nao_agrupar=True,
                         montadora=", ".join(dict.fromkeys(m for rx, m in _MONT if re.search(rx, t, re.I))),
                         foto_spec={"rect": [round(v, 1) for v in foto]}))
    return regs


for _p in range(465, 473):
    ADD.extend(ler(_p))


def F(p, c, **kw):
    regs = [r for r in ADD if r["pagina"] == p and r["codigo"] == c]
    assert regs, f"{c} não está na pág. {p}"
    for r in regs:
        r.update(kw)


def N(p, card, cod, desc, foto, **kw):
    r = dict(pagina=p, card=card, codigo=cod, descricao=desc, cod_ref="", variacoes="", aplicacao="", info="", marca="",
             montadora="", _nao_agrupar=True, foto_spec={"rect": foto})
    r.update(kw)
    ADD.append(r)


def EQ(p, rect, max_size=5):
    """Tabela 'Códigos de marcas equivalentes': pares marca/código, linha a linha."""
    sp, _ = _spans(p)
    x0, y0, x1, y1 = rect
    ss = sorted([s for s in sp if x0 <= s["x"] <= x1 and y0 <= s["y"] <= y1 and s["size"] <= max_size and not s["red"]],
                key=lambda s: (s["y"], s["x"]))
    L = []
    for s in ss:
        if L and abs(L[-1][0] - s["y"]) < 1.8:
            L[-1][1].append(s)
        else:
            L.append([s["y"], [s]])
    pares = []
    for _, l in L:
        l.sort(key=lambda s: s["x"])
        toks = [t["t"].strip() for t in l if t["t"].strip()]
        for i in range(0, len(toks) - 1, 2):
            pares.append(f"{toks[i]} {toks[i + 1]}")
    return "Equivalentes: " + " / ".join(dict.fromkeys(pares))


# 465 (pág. impressa 464)
N(465, 4, "5170670", "CONEXAO BICO ARLA DOSADORA 90GRAUS 8MM SCANIA", [440, 100, 560, 160], aplicacao="Diversos, Scania euro 5/6/7",
  cod_ref="2159098, 2159100, 6413587, Ng8", montadora="Scania", info="Código impresso como imagem")
N(465, 7, "5171178", "TAMPA ARLA RESERV. C CHAVE S/GARGALO SCANIA", [305, 228, 425, 285], aplicacao="Série 5 só caminhões",
  cod_ref="109323, 1813412, 2038563, 2158045, 2158045, 222615, 2278297, 2477313", montadora="Scania",
  info="Código impresso como imagem")
F(465, "5175731", montadora="Scania")
F(465, "5172086", descricao="FILTRO ARLA MODERNO REFIL C/ORING R450/500", montadora="Scania", info="Impresso como 'FILTO'")
F(465, "4920090", descricao="FILTRO ARLA KIT MB ACCELO/ATEGO/SCANI WEA009K", marca="Wega", montadora="Mercedes-Benz, Scania",
  variacoes="Equivalentes: DAF 2122909 / Fendt ACP0153520 / Fleetguard Uf106 / Hengst E104UD350 / Hifi Kd70436 / "
            "Japanparts FUBR08S / Mann U58/6 / Mann U58/9KIT / Mann U58/7 / Mercedes A0001420589 / Mercedes A0001420789 / "
            "Mercedes A0001420989 / Mercedes A0001421089 / Fleetguard UF106 / MWM MM100832 / Original 1420789 / Original 1420989 / "
            "Original 11150708 / Original 11450803 / Original 4388378 / Original 6051964 / Original 1420589 / "
            "Original Filter OFU8007KIT / Scania 2655854 / Tecfil PEA180 / Wega WEA009K")
F(465, "4920004", descricao="FILTRO ARLA SCANIA G400 12.7 24V 2017 WEA004", marca="Wega", montadora="Scania",
  variacoes=EQ(465, [454, 505, 563, 614], 3.5))
# 466 (pág. impressa 465)
F(466, "231403", info="Lançamento | Código impresso com 6 dígitos")
F(466, "5172152", descricao="FILTRO ARLA VOLVO HF/FM WEA008", info="Impresso como 'FILTO'")
F(466, "5172320", descricao="TAMPA ARLA FILTRO VOLVO", info="Impresso como 'FILTO'")
F(466, "4920012", descricao="FILTRO URÉIA REFIL IVECO STRALIS WEA012", marca="Wega", variacoes="Equivalentes: Volvo 21954674",
  montadora="Iveco, Volvo")
F(466, "4920006", descricao="FILTRO ARLA URÉIA IVECO VOLVO WEA006", marca="Wega", variacoes=EQ(466, [32, 629, 205, 805]),
  montadora="Iveco, Volvo")
# 467 (pág. impressa 466)
F(467, "4920080", descricao="TAMPA SISTEMA ARLA REFIL WEGA TFA008 PARA FH 500 12-19", marca="Wega",
  variacoes="Equivalentes: Volvo 21376707 / Volkswagen 2P0131980 / Volkswagen 2V3131510 / MAN 81154036152 / Ford BH3T6737AA",
  info="Aplica-se com o filtro WEA-008", montadora="Volvo, Volkswagen, MAN, Ford")
F(467, "4920014", descricao="FILTRO ARLA REFIL VW DELIVERY 3.8 9.170 WEA014", marca="Wega", montadora="Volkswagen",
  variacoes="Equivalentes: Volvo 20742759 / Volvo 82269261 / Volvo 23251838 / Mack 82269261 / Mack 23251838 / Hifi-Filter SD70439 "
            "/ Nissan 5282269261 / Mann U5010 / Renault 7482269261 / Fleetguard Uf113")
F(467, "4920001", descricao="FILTRO ARLA VOLKS TGX 2.4 29.440 WEGA WEA001", marca="Wega", montadora="Volkswagen, MAN",
  variacoes="Equivalentes: Hengst E101UD178 / Turbo Filtros TEA1546 / Hengst E101UD324 / UFI 3194800 / Japanparts FUBR03S / "
            "UFI 4400100 / Mahle UX1D / Volkswagen 2V5131759A / MAN 81154036089 / Wega WEA001 / Mann U620/4YKIT / WIX W74B196 / "
            "MWM MM100831")
# 468 (pág. impressa 467)
F(468, "5175499", descricao="PRE-FILTRO ARLA VALVULA DOSADORA 32 MB", info="Impresso como 'DISADOTRA'")
F(468, "5177068", info="Impresso 'COMPETO'")
F(468, "5171125", descricao="VALVULA MAGNETICA MB 3/2 VIAS 24V TOMADA QUAD", cod_ref="000 997 3512",
  aplicacao="1718/1722/1725/1728/1933/2035/2040..", info="Dimensões: 10 x 10 x 10 cm | Peso: 553 kg (como impresso)")
F(468, "5178703", descricao="VALVULA ARLA SOLENOIDE 3/2 VIA 2 SAIDA OPOSTA", info="Válvula solenoide magnética controle de fluxo 3/2 vias",
  montadora="Mercedes-Benz")
F(468, "5170263", descricao="DOSADORA EURO 5/6 2016 24V FASE 2 VAZAO 250ML", cod_ref="Original 0001405339 / A0001405539",
  info="Dosadora bomba Arla euro 5 2ª fase e euro 6 1ª fase (modelo botinha serve euro 5 segunda fase e euro 6 primeira fase)",
  aplicacao="MB Accelo: 1016/1316/815 // MB Atego: 1419/1719/1726/1729/2426/2430/2730/3026/3030 // MB Atron: 1635 // "
            "MB Axor: 1933/3131 // MB micro ônibus: LO916 // MB ônibus: OF1519/OF1620/OF1721/OF1724")
# 469-471
for _p, _c in ((469, "5171348"), (470, "5175526"), (470, "5171377"), (470, "5172754"), (470, "5170365"), (471, "5179825"), (471, "5179179")):
    F(_p, _c, montadora="Mercedes-Benz")
F(470, "4001857", descricao="QA-18057 REPARO DOSADORA FASEII", variacoes="QA-18057",
  aplicacao="Mercedes Accelo 2012 a 2015 / Actros / Atego / Axor / O-500")
F(471, "5179180", descricao="FILTRO ARLA MODERNO REFIL MB", info="Impresso como 'FILTO'")
F(471, "5176005", info="Impresso 'AXOS/ACT'")
NOTAS.append("Págs. 465-471: alguns cards repetem a mesma 'conversão' de outro produto (ex.: 5172072 peneira Volvo e 5178916 válvula "
             "Actros trazem a conversão/aplicação do 5170119 Delivery; 5179180 traz a conversão Volvo do 5172152; 5171352 traz a do "
             "5174137); mantido como impresso. 5170670 e 5171178 têm o código impresso como imagem; 231403 está impresso com 6 dígitos.")
