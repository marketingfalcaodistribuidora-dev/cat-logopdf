# Capítulo 20 - Pinos e Buchas (págs. 252-264)
TIPOS = [(r"ALARGADOR", "ALARGADOR"), (r"PINO", "PINO"), (r"BUCHA|EMBUCH", "BUCHA"), (r"ARRUELA", "ARRUELA")]
AJ = {}
ADD = []
MANUAIS = {252, 253}
NOTAS = []
MB = "Mercedes-Benz"


def cel(p, card, codigo, descricao, faixa, info="", **kw):
    """Registro manual com faixa (a foto é a maior imagem da faixa); info substitui o texto miúdo lido."""
    ADD.append(dict(pagina=p, card=card, codigo=codigo, descricao=descricao, faixa=faixa, fonte_titulo=99, _nao_agrupar=True, **kw))
    AJ["cod:" + codigo] = dict(AJ.get("cod:" + codigo, {}), info=info)


# 252 - alargador expansivo (tabela)
for _c, _mod, _faixa in [("9070017", "I", "27,00 a 30,00"), ("9070018", "J", "30,00 a 34,00"), ("9070019", "K", "34,00 a 38,75"),
                         ("9070020", "L", "38,75 a 46,00"), ("9070021", "M", "46,00 a 56,00")]:
    ADD.append(dict(pagina=252, card=1, codigo=_c, descricao=f"ALARGADOR EXPANSIVO COM GUIA MODELO {_mod} {_faixa} MM",
                    _titulo="ALARGADOR EXPANSIVO COM GUIA", tipo="ALARGADOR", info="VENDA SOBE CONSULTA",
                    foto_spec={"rect": [40, 160, 560, 430]}))

# 253 - pinos de mola MB (grade de molduras sobrepostas)
_X0, _XM, _X1 = 20, 297, 575
_Y = [85, 193, 309, 418, 501, 589, 671, 741, 805]
L, R, W = (_X0, _XM), (_XM, _X1), (_X0, _X1)


def _f(col, i, j=None):
    return [col[0], _Y[i], col[1], _Y[j if j is not None else i + 1]]


for _n, (_c, _d, _fx, _inf) in enumerate([
        ("50625130", "MB PINO MOLA DIANT 25 X 130", _f(L, 0), "25MM | 131MM | CEMENTADO 1113/3"),
        ("5060100", "MB PINO MOLA DIANTEIRA 1113/3", _f(R, 0), "25MM | 131MM | COMUM"),
        ("50630140", "MB PINO MOLA TRAS 30 X 140", _f(L, 1), "30MM | 140MM | CEMENTADO 1113/3"),
        ("5060102", "MB PINO MOLA TRASEIRA 1113/3", _f(R, 1), "25MM | 140MM | COMUM"),
        ("50625131", "MB PINO MOLA DIANT OPOSTO 25 X 130 (COMUM)", _f(L, 2), "COMUM"),
        ("50625132", "MB PINO MOLA DIANT OPOSTO 25 X 130 (CEMENTAD)", _f(R, 2),
         "No card consta 'COMUM' abaixo da foto, apesar da descrição 'CEMENTAD'"),
        ("50630150", "MB PINO MOLA TRASEIRA CURTO 30 X 150", _f(W, 3), "Medidas: 30x150mm"),
        ("5063067", "MB BUCHA MOLA DIANTEIRA 1113/3", _f(L, 4), "LATONADA | Int x Ext x Comp: 25.20 x 30.10 x 67.00"),
        ("5063577", "MB BUCHA MOLA TRAZEIRA 1113/1313", _f(R, 4), "LATONADA | Int x Ext x Comp: 30.20 x 35,10 x 77.00"),
        ("5063921", "BUCHA MOLA DIANTEIRA 1113/3 BRONZE", _f(L, 5), "Int x Ext x Comp: 25.20 x 30.10 x 67.00"),
        ("5063922", "BUCHA MOLA TRAZEIRA 1113/3 BRONZE", _f(R, 5), "Int x Ext x Comp: 30.20 x 35,10 x 77.00"),
        ("5060758", "MB PINO PATIM FREIO OLEO 30 X 94MM", _f(L, 6), "94MM"),
        ("5069102", "MB PINO PATIM FREIO OLEO 30 X 102MM", _f(L, 7), "102MM"),
        ("5060759", "MB PINO SAPATA FREIO MODERNA", _f(R, 6, 8), "102MM")]):
    cel(253, _n + 1, _c, _d, _fx, _inf, montadora=MB)
AJ["cod:50630150"]["aplicacao"] = "Feixe de mola traseiro Mercedes Benz Toco 1924/1935"

# ---- págs. 254-258: buchas de bronze (grade 2 colunas; cada card começa em "REF ORIGINAL")
import re  # noqa: E402

from tabela_livre import _spans  # noqa: E402

_CODE = re.compile(r"^\d{5,12}$")


def _txt(ss):
    linhas = []
    for s in sorted(ss, key=lambda s: (s["y"], s["x"])):
        if linhas and abs(linhas[-1][0] - s["y"]) < 3:
            linhas[-1][1].append(s["t"])
        else:
            linhas.append([s["y"], [s["t"]]])
    return [re.sub(r"\s+", " ", " ".join(l[1])).strip() for l in linhas]


def buchas(p, meio=297.6, montadora_padrao="", fim=805, zonas=None):
    """zonas: [(y0, y1, [x cortes]), ...]; padrão = 2 colunas na página toda."""
    sp, imgs = _spans(p)
    zonas = zonas or [(0, fim, [20, meio, 575])]
    regs = []
    for zy0, zy1, cortes in zonas:
        for k in range(len(cortes) - 1):
            x0, x1 = cortes[k], cortes[k + 1]
            ys = sorted(s["y"] for s in sp if (s["t"].upper().startswith("REF ORIGINAL") or s["t"].upper().startswith("REF:"))
                        and x0 <= s["x"] < x1 and zy0 <= s["y"] < zy1)
            for i, y0 in enumerate(ys):
                y1 = ys[i + 1] - 3 if i + 1 < len(ys) else zy1
                cs = [s for s in sp if x0 <= (s["x"] + s["x1"]) / 2 < x1 and y0 - 3 <= s["y"] < y1]
                cods = [s for s in cs if s["red"] and _CODE.match(s["t"].replace(" ", ""))]
                if not cods:
                    continue
                cod = cods[0]
                ref = [s for s in cs if re.match(r"REF( ORIGINAL)?:", s["t"], re.I)]
                cat = [s for s in cs if not s["red"] and s["size"] < 8 and s["t"].isupper() and s not in ref and s["y"] < y0 + 12]
                dims = [s for s in cs if s["red"] and re.match(r"^[\d.,]+\s*x\s*[\d.,]+", s["t"], re.I)]
                apl_lab = [s for s in cs if s["red"] and s["t"].upper().startswith("APLICA")]
                ya = apl_lab[0]["y"] + 6 if apl_lab else 1e9
                usados = set(map(id, ref + cat + dims + apl_lab + cods))
                resto = [s for s in cs if id(s) not in usados and not (s["red"] and "Int x Ext" in s["t"])]
                apl = [s for s in resto if s["y"] >= ya and s["size"] < 11]
                desc = [s for s in resto if s not in apl and s["y"] >= cod["y"] - 2]
                outros = [s for s in resto if s not in apl and s not in desc]
                info = [f"Int x Ext x Comp: {dims[0]['t']}"] if dims else []
                info += [c["t"].strip().capitalize() for c in cat] + _txt(outros)
                # foto: maior imagem do card
                fotos = [b for b in imgs if x0 <= (b[0] + b[2]) / 2 < x1 and y0 - 3 <= (b[1] + b[3]) / 2 < y1]
                foto = max(fotos, key=lambda b: (b[2] - b[0]) * (b[3] - b[1])) if fotos else None
                regs.append(dict(pagina=p, card=len([r for r in ADD if r["pagina"] == p]) + len(regs) + 1,
                                 codigo=cod["t"].replace(" ", ""), descricao=" ".join(_txt(desc)),
                                 cod_ref=" / ".join(re.sub(r"^REF( ORIGINAL)?:\s*", "", s["t"], flags=re.I) for s in ref),
                                 aplicacao=" / ".join(_txt(apl)), info=" | ".join(x for x in info if x), _nao_agrupar=True,
                                 montadora=montadora_padrao, foto_spec={"rect": foto} if foto else None))
    MANUAIS.add(p)
    ADD.extend(regs)
    return regs


buchas(254, montadora_padrao=MB)
fix_254 = [r for r in ADD if r["codigo"] == "4951012"][0]
fix_254.update(descricao="BUCHA BRONZE FREIO A AR 38,05 X 43.10 X 48.00", aplicacao="Bucha Freio a ar")
for _p in (255, 256, 257, 258):
    buchas(_p, montadora_padrao=MB if _p == 255 else "", zonas=[(0, 627, [20, 297.6, 575]), (627, 805, [20, 206.5, 389.8, 575])] if _p == 255 else None)
TIPOS.insert(0, (r"BUCHA", "BUCHA"))


def _r(c):
    return [r for r in ADD if r["codigo"] == c][0]


_r("4951280").update(descricao="BUCHA BRONZE AGRALE MANGA EIXO W.8 MICRO BUS", aplicacao="Bucha Manga Eixo W.8 Micro Bus")
_r("4951219").update(aplicacao="")
_r("4951040")["info"] = "Int x Ext x Comp: 25.60 x 31.85 x 98.00 | Bucha da mola / suspensão | MESMA 495.1042 / BRONZE"
_r("4951042")["info"] = "Int x Ext x Comp: 25.60 x 31.85 x 98.00 | Bucha da mole / suspensão | MESMA 495.1040 / MESMA 501.1004 / LATÃO"
for _c, _m in (("4951549", "Agrale"), ("4951280", "Agrale")):
    _r(_c)["montadora"] = _m
NOTAS.append("Págs. 254-258: buchas de bronze; 'Int x Ext x Comp' (medidas), categoria (manga do eixo, feixe de mola, freio) e "
             "observações 'MESMA ...' estão na coluna de informações. Pág. 258: metade de baixo vazia.")

# 259-260
AJ["259.1"] = {"descricao": "PINO MOLA DT CURTO CEMENTADO FORD CARGO 1\"X156MM", "cod_ref": "E4HT 5A314 AA",
               "aplicacao": "CARGO 1622/1730/2422/3530/4030", "info": "1\"X156MM", "montadora": "Ford"}
AJ["259.2"] = {"descricao": "PINO MOLA DT LONGO CEMENTADO FORD CARGO 1\"X170MM", "cod_ref": "TJC 411 175",
               "aplicacao": "CARGO 1622/1730/2422/3530/4030", "info": "1\"X170MM", "montadora": "Ford"}
AJ["259.3"] = {"descricao": "BUCHA FO 0270 DIANT P/TRAS E TRAS CARGO 113 1113/1313/1514", "montadora": "Ford",
               "info": "Int x Ext x Comp: 25.60 x 31.85 x 98.00 | MESMA 495.1042 / BRONSE | MESMA 495.1040 / BRONSE"}
AJ["259.4"] = {"montadora": "Ford"}
AJ["260.1"] = {"_titulo": "ARRUELA ENCOSTO MOLA", "tipo": "ARRUELA"}
AJ["cod:4103260"] = {"descricao": "ARRUELA ENC MOLA TZ FORD 32,5X60X1,90MM", "info": "60MM x 32,5MM x 1,90MM",
                     "montadora": "Volkswagen, Ford"}
AJ["cod:4102650"] = {"info": "50MM x 26MM x 1,90MM", "montadora": "Volkswagen, Ford"}
NOTAS.append("Pág. 260: as arruelas 4103260 e 4102650 têm 'FORD' na descrição e logo da Volkswagen no card.")

# ---- págs. 261-264: embuchamentos (kits de manga de eixo)
TIPOS.insert(0, (r"EMBUCH", "EMBUCHAMENTO (KIT MANGA DE EIXO)"))
TIPOS.insert(0, (r"CHIME", "CHIME"))
AJ["261.1"] = {"cod_ref": "BD2DY 3111A", "variacoes": "REF: FO02.CH00", "aplicacao": "F4000 (…/96)",
               "info": "MED: 26,80MM | Medidas (STD): 26,80 ao 27,80 | Foto ilustrativa", "montadora": "Ford"}
AJ["261.2"] = {"cod_ref": "BF5T 3111E", "variacoes": "REF: FO03.CH00", "aplicacao": "F4000 Moderno (93/98)",
               "info": "MED: 28,65MM | Medidas (STD): 28,65 ao 29,55", "montadora": "Ford"}
AJ["261.11"] = {"cod_ref": "DC463115BA", "variacoes": "REF: FO12.CH00", "aplicacao": "Extra pesado 2042/2842",
                "info": "MED: 50,00MM | Medidas (STD): 50,00 ao 50,30", "montadora": "Ford, Volkswagen"}
AJ["261.12"] = {"cod_ref": "T11498629B", "variacoes": "348-P / VA018B", "info": "MED: 41,00MM | Embuchamento manga eixo 0.20 41MM"}
AJ["261.8"] = {"descricao": "EMBUCHAMENTO VOLKS 13180 COM CHIME", "aplicacao": "VOLKS 13.150/13.160/13.180 SERIE 2000"}
AJ["262.6"] = {"descricao": "CHIME BRONZE VW 9.150 P/ EMBU 33,00", "cod_ref": "2RO407393", "variacoes": "VW03CH",
               "aplicacao": "Manga de eixo Volkswagen 9.150 e 8.150 eixo SIFCO", "info": "Medida do chime: 34,20 x 53,00 x 16,00"}
AJ["262.7"] = {"cod_ref": "1904698", "variacoes": "REF: IV01.BB00", "aplicacao": "IVECO STRALLIS/TRAKER/EURO",
               "info": "MED: 43,00MM | Medidas: INF 43,00 / SUP 53,00"}
AJ["262.11"] = {"cod_ref": "8.127.759", "variacoes": "K-15.1467", "aplicacao": "Volvo: FH-12 / NH-12 / Ano 2.000 até 2.004",
                "info": "NOVO | Diâmetro: 51,00mm | Manga de eixo com bucha nylon / bronze | Pino: 223,00mm | Pino temperado | "
                        "Reparo para um lado (1 lado) | 01 bucha nylon/bronze, 01 pino, 01 kit de componentes"}
AJ["262.12"] = {"cod_ref": "550.257", "info": "MED: 45,00MM"}
AJ["263.12"] = {"descricao": "EMBUCH 35MM MERCEDES ACCELO 915 STD PINO CONICO",
                "info": "OBS: Pino cônico | Medida superior 27,MM | Medida inferior 35,00 | Comprimento 176 MM"}
AJ["264.1"] = {"info": "MED: 50,00MM"}
AJ["264.3"] = {"descricao": "EMBUCH MB ACTROS 4140/4844 MED: 54,00MM", "cod_ref": "942 332 0806", "variacoes": "REF: MB14.CH00",
               "aplicacao": "ACTROS 4140/4844", "info": "MED: 54,00MM | Medidas (STD): 54,00 ao 54,30"}
NOTAS.append("Págs. 261-264: embuchamentos (kits de pino, buchas e chime da manga de eixo); 'MED' (medida) na coluna de "
             "informações, código original em referência. Pág. 264: só 3 produtos, demais molduras vazias.")
_MONT20 = [(r"MERC|\bMB\b|ACCELO|AXOR|ACTROS", "Mercedes-Benz"), (r"VOLKS|\bVW\b", "Volkswagen"), (r"F CARGO|F4000|FORD", "Ford"),
           (r"IVECO", "Iveco"), (r"VOLVO", "Volvo"), (r"SCANIA", "Scania")]


def POS_PROC(r):
    p = int(str(r["pagina"]).split(",")[0])
    if 261 <= p <= 264:
        d = r["descricao"]
        if "FOTO ILUSTRATIVA" in d:
            r["descricao"] = d = re.sub(r"\s*FOTO ILUSTRATIVA", "", d).strip()
            r["info"] = " | ".join(x for x in (r.get("info", ""), "Foto ilustrativa") if x)
        r["descricao"] = d = re.sub(r"C/CHIM E\b", "C/CHIME", d)
        r["tipo"] = "CHIME" if d.startswith("CHIME") else "EMBUCHAMENTO (KIT MANGA DE EIXO)"
        # MED: dentro da referência -> informações
        ref = r.get("cod_ref", "")
        med = re.findall(r"MED:\s*[\d,]+MM", ref)
        if med:
            ref = re.sub(r"\s*MED:\s*[\d,]+MM", "", ref).strip(" /")
        r["cod_ref"] = re.sub(r"^ORIG\s+", "", ref)
        inf0 = re.sub(r"FOTO ILUSTRATIVA", "Foto ilustrativa", r.get("info", ""))
        info = [x.strip() for x in re.split(r"\s*[/|]\s*", inf0) if x.strip()] if "|" not in inf0 else [inf0]
        if med or info:
            meds = [re.sub(r"MED:\s*", "MED: ", m) for m in med] + [re.sub(r"MED:\s*", "MED: ", x) for x in info]
            r["info"] = " | ".join(dict.fromkeys(meds))
        if not r.get("montadora") or r["montadora"] in ("Mercedes-Benz",):
            txt = d + " " + r.get("aplicacao", "")
            ms = [m for rx, m in _MONT20 if re.search(rx, txt)]
            if "REF ORIG VW" in r.get("_raw", "") or "VW" in r.get("cod_ref", ""):
                ms.append("Volkswagen")
            r["montadora"] = ", ".join(dict.fromkeys(ms))
AJ["cod:50630150"]["foto_spec"] = {"rect": [40, 422, 245, 470]}
