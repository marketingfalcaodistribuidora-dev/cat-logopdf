# Capítulo 21 - Quinta Roda e Coxim (págs. 265-289)
import json
import os

from capitulos import WORK

TIPOS = [(r"COXIM", "COXIM"), (r"BUCHA", "BUCHA"), (r"BATENTE", "BATENTE"), (r"PINO REI", "PINO REI"), (r"ANEL", "ANEL"),
         (r"GANCHO", "GANCHO"), (r"TRAVA", "TRAVA"), (r"MOLA", "MOLA"), (r"PROTETOR", "PROTETOR"), (r"\bPF\b|PARAFUSO", "PARAFUSO"),
         (r"PINO", "PINO"), (r"PORCA", "PORCA"), (r"ENGATE", "ENGATE"), (r"PE DE CARRETA|P[ÉE] DE CARRETA", "PÉ DE CARRETA"),
         (r"MANIVELA", "MANIVELA"), (r"FLANGE", "FLANGE")]
AJ = {}
ADD = []
NOTAS = []
CP, JO, IA, TH = "Canaparts", "Jost", "IABV", "Thor"

# cada código é um produto (as molduras se sobrepõem e juntam códigos de cards diferentes)
NAO_AGRUPAR = set()
for _p in range(265, 290):
    for _c in json.load(open(os.path.join(WORK, "raw", f"p{_p:03d}.json"), encoding="utf-8"))["cards"]:
        NAO_AGRUPAR.add(f"{_p}.{_c['id']}")


def D(codigo, descricao=None, **kw):
    """Corrige um código: descrição (lida da página) e demais campos; info/aplicação vazios por padrão."""
    d = dict(info=kw.pop("info", ""), aplicacao=kw.pop("aplicacao", ""), **kw)
    if descricao is not None:
        d["descricao"] = descricao
    AJ["cod:" + codigo] = d


# ---- pág. 265 (peças de quinta roda Jost; vários textos impressos como imagem)
for _c, _d, _m, _i in [
        ("5060010", "JOST ANEL DE 2' 3 FUROS", CP, ""), ("5062040", "JOST ANEL DE 2' 4 FUROS", CP, ""),
        ("5060300", "TRAVA JOST DE 2\"", CP, ""), ("5060900", "GANCHO JOST DE 2'", CP, ""),
        ("5060200", "PINO GANCHO JOST 2' COM 20MM", CP, ""), ("5062072", "2072 ORIGINAL JOST COXIM MOD 5 RODA", JO, ""),
        ("509805001", "2072 COXIM MOD 5 RODA JOST TH", TH, "Modelo Jost"), ("4982072", "2072 COXIM MOD 5 RODA JOST", IA, ""),
        ("5065200", "FLANGE PINO REI 2\" CARRETA", "", "Carreta - pino rei 2\""),
        ("5060501", "PINO REI DE 2' CARRETA", "", "Carreta - pino rei 2\""),
        ("5060850", "MOLA FECHO 5ª RODA JOST (GARRA TRAVAMENTO)", CP, ""),
        ("5060860", "MOLA DUPLA 5 RODA JOST (RETORNO MANIPILO)", CP, ""),
        ("821216", "JOST PF ALLEN 12 X 16 R 1,75 QUINTA RODA PARA ANEL", "", ""),
        ("821420", "JOST PF ANEL 2\" (14 X 20MM) ALEN", "", ""),
        ("2741435", "PF.FLANGE PINO REI 14X35 ACO", "", "Para flange 2\" | REF: 32.014.50"),
        ("2741645", "PF.FLANGE PINO REI 16X45 ACO", "", "Para flange 3\" 1/2"),
        ("50616110", "JOST PF FIXACAO QUINTA RODA 16 X 110", CP, ""), ("821680", "JOST PF ALLEN 16 X 80 QUINTA RODA", CP, ""),
        ("5062312", "JOST GANCHO 3.1/2", CP, ""), ("5069060", "JOST ANEL 3.1/2 4 FUROS", CP, ""),
        ("5063122", "JOST TRAVA DE 3 1/2", CP, ""), ("5063128", "PINO REI FLANGEADO 3. 1/2 COM 8 FUROS", CP, ""),
        ("5061312", "JOST ANEL 3.1/2 3 FUROS", CP, ""), ("5060270", "PINO DA GARRA TRAVAMENTO 3.1/2\"", "", "61MM x 20MM"),
        ("5063121", "JOST COXIM 5 RODA DE 3.1/2 REFORCADO", "", ""),
        ("50631212", "PINO REI CANAPARTS 3 1/2 COM 12 FUROS", CP, ""),
        ("50631213", "PINO REI 3 1/2 COM 12 FUROS-COM FURO CENTRAL", CP, "")]:
    D(_c, _d, marca=_m, info=_i, montadora="" if _c.startswith(("50652", "50605")) else JO)
NOTAS.append("Pág. 265: peças de quinta roda Jost (Jost na coluna de marca/aplicação; Canaparts, Thor e IABV como marca do produto). "
             "2741435 e 2741645 também estão no capítulo Parafusos e Porcas (pág. 216).")

# ---- pág. 266 (Jost, Maxion, Cobrasma, Fontaine)
MX, CB, FT = "Maxion", "Cobrasma", "Fontaine"
for _c, _d, _mont, _marca, _i, _ref in [
        ("5060830", "JOST KIT 5 RODA 3 1/2", JO, "", "", ""),
        ("5066250", "JOST KIT CONVERSOR 3.1/2 PARA 2\"", JO, CP, "Produtos relacionados: PF.051 / PRU.0172 / PRU.0173", ""),
        ("5061100", "ANEL MAXION DE 2'", MX, CP, "", ""), ("5060017", "GANCHO MAXION DE 2'", MX, CP, "", ""),
        ("5061200", "TRAVA MAXION DE 2'", MX, CP, "", ""), ("5060016", "PINO GANCHO MAXION 2' C/ 16MM", MX, CP, "", ""),
        ("5068700", "MAXION MOLA FECHO 5 RODA (GARRA TRAVAMENTO)", MX, CP, "", ""),
        ("4982087", "2087 COXIM 5ª RODA MAXION", MX, IA, "", ""),
        ("5063900", "GANCHO COBRASMA DE 2'", CB, "", "", ""), ("5060041", "ANEL ENTALHADO COBRASMA", CB, "", "", ""),
        ("5064300", "PINO ENTALHADO COBRASMA", CB, "", "Carreta - pino rei 2\"", ""),
        ("5063123", "FONTAINE ANEL 2\"", FT, "", "", ""), ("5063125", "FONTAINE GANCHO 2\"", FT, "", "", ""),
        ("5062061", "TRAVA GAVIAO 5 RODA FONTAIME", FT, "", "", ""), ("5067160", "KIT 5 RODA FONTAINE 2\"", FT, "", "", ""),
        ("4982300", "2300 BUCHA 5 RODA FONTAINE", FT, IA, "Fonteine até 2000 5 roda 2\" | Ext. 71,3MM x Int 51,4MM x Comp 101,5 MM", "")]:
    D(_c, _d, montadora=_mont, marca=_marca, info=_i)
AJ["cod:5066250"]["variacoes"] = "QR00130J00 (similar)"
AJ["cod:5066250"]["cod_ref"] = ""
D("4982159", "2159 BUCHA 5 RODA COMPATÍVEL GUERRA/FONTAIN", montadora="Guerra, Fontaine, Randon", marca=IA,
  cod_ref="921226663", variacoes="MESMA TH - 50913015 / Cód: 2293",
  aplicacao="Suspensão pneumática FS250 / Compatível com o veículo: Randon FS250 Nova",
  info="Arruela de nylon suspensão pneumática FS250 compatível Suspensys | Material: nylon | Embalagem: 10 | "
       "Ext. 159 mm x Int. 78 mm x Espessura 6,5 mm")

# ---- pág. 267
D("557101203", "CABO TERRA 5ª RODA", info="30 CM")
D("7004002", "PROTETOR 5ª RODA CANAPARTS JOST", montadora=JO, marca=CP, info="Modelo Jost")
D("5062120", "JOST SAPATA 120MM QUINTA RODA", montadora=JO, marca=CP, info="LANÇAMENTO | Comprimento 405MM | Altura 120MM | Modelo Jost")
D("5062150", "JOST SAPATA 150MM QUINTA RODA", montadora=JO, marca=CP, info="LANÇAMENTO | Comprimento 405MM | Altura 150MM | Modelo Jost")
D("5060903", "JOST QUINTA RODA 2\" SEM SAPATA", montadora=JO, marca=CP)
D("5060447", "QUINTA RODA JOST 2\" SAPATA 150MM", montadora=JO, marca=JO)
TIPOS[:0] = [(r"SAPATA", "SAPATA DE QUINTA RODA"), (r"QUINTA RODA", "QUINTA RODA"), (r"CABO TERRA", "CABO TERRA"),
             (r"KIT", "KIT DE QUINTA RODA")]
AJ["cod:509805001"]["tipo"] = "COXIM"

# ---- pág. 268
D("5061550", "ENGATE AUTOMÁTICO COMPLETO C/ PINO 52 MM", info="LANÇAMENTO",
  aplicacao="Ford Novo Cargo 1932 4X2 2622 6X4 2628 6X4 2632 6X4 3132 6X4 2011 a 2015 / Ford Cargo 2628E 2632E 5032E 6332E "
            "2006 a 2011 / Carreta FNV, Silpa, Canavieira", montadora="Ford")
D("5060452", "CORPO ENGATE IGREJINHA COM PINO 50MM", cod_ref="5084012272/M", info="LANÇAMENTO")
D("5060711", "PF EIXO CENTRAL TRAVA PINO REI 5A RODA", info="Usa-se: 5064270 PORCA CASTELO M42 X 50 X 70")
D("5064270", "PORCA CASTELO M42 X 50 X 70", info="Usa-se: 5060711 PF EIXO CENTRAL TRAVA PINO REI 5A RODA")
D("5065800", "PONTEIRA GIRATORIA SEMI-REBOQUE COMPLETA M45", aplicacao="Carreta florestal",
  info="Usa-se: 5063400 PORCA CASTELO PONTEIRA SEMI-REBOQUE M45 X 63")
D("5063400", "PORCA CASTELO PONTEIRA SEMI-REBOQUE M45 X 63", aplicacao="Carreta florestal",
  foto_spec={"rect": [395, 452, 570, 624]}, info="Código impresso só no quadro 'USA-SE' do card da ponteira; foto no card vizinho")
D("5063707", "KIT TRAVA PINO REI", info="LANÇAMENTO")
D("5060077", "PRATO APOIO TRAVA PINO REI", info="LANÇAMENTO")
D("5061220", "MOLA DA TRAVA DO PINO REI 5A RODA", info="LANÇAMENTO", tipo="MOLA")
AJ["cod:5060077"]["tipo"] = "PRATO DE APOIO"

# ---- pág. 269
D("5060333", "BALANCA EIXO TANDEM 2325 2314/ 3833250112", montadora="Mercedes-Benz",
  aplicacao="MB 2318, 2314, 2325, 2414, 2418, 2428, 2423", info="Aplica-se rolamento 32018 / 331958")
for _c in ("32018", "331958"):
    AJ["cod:" + _c] = {"skip": True}
D("5060070", "BALANCA MANCAL SCANIA 94/114/124 1399489", montadora="Scania", aplicacao="Scania: Série 4 - 94 / 114 / 124")
D("5062727", "KIT EMBUC SCANIA 94/114/124", montadora="Scania", aplicacao="Scania: Série 4 - 94 / 114 / 124", tipo="KIT")
D("5062020", "MANCAL BOOGIE 23CM SEMI REBOQUE 301008762", montadora="Noma, Randon", info="26T",
  aplicacao="Semi reboque suspensão boogie / single point (entre eixos 1437MM)")
D("5063535", "ANEL ORING 113 X 103 X 5 (346 05543)", montadora="Randon", foto_spec={"rect": [213, 271, 384, 441]})
D("5061067", "BUCHA MANCAL SINGLE POINT 23CM RAND301006968", montadora="Randon",
  aplicacao="Randon para mancal de 23CM suspensão Rodoforte")
NOTAS.append("Pág. 269: 32018 e 331958 são os rolamentos indicados para a balança 5060333 (ficaram na coluna de informações). "
             "Metade de baixo da página com molduras vazias.")

# ---- pág. 270 (pé de carreta)
BZ = "BZ Automotive"
D("50933002", "PE DE CARRETA CONJUNTO 2 PEÇAS 28T", info="Conjunto | Medidas: 23CM / 93CM / 77CM")
D("50933000", "SUPORTE DO PE DE CARRETA UNIVERSAL")
D("8790580", "KIT REPARO PARCIAL PE DE CARRETA", aplicacao="BZ0579, BZ0579A, BZ0579B", info="Modelo Jost", montadora=JO, tipo="KIT")
D("8790834", "MANIVELA PE DE CARRETA 72 CM", aplicacao="BZ0320, BZ0579, BZ0579A, BZ0579B e BZ2062", tipo="MANIVELA")
D("8790494", "KIT REPARO PARCIAL PE CARRETA BZ0320", marca=BZ, aplicacao="Pé de carreta (50933002)", tipo="KIT")
D("8790833", "BARRA CENTRAL PE DE CARRETA 160 CM", info="25MM",
  aplicacao="Carretas: todas, aplica com itens BZ Automotive BZ0320, BZ0579, BZ0579A, BZ0579B e BZ2062", tipo="BARRA CENTRAL")
D("5090988", "PE DE CARRETA IMP 14T DOLLY",
  info="Pé de carreta com pé de apoio Dolly, 14ton, sapata T | Sapata móvel em T | Pé de apoio Dolly com 2 velocidades | "
       "Engrenagens com redução de velocidade | Estrutura reforçada | Capacidade de levantamento: 14 toneladas | "
       "Velocidade de aproximação alta: 5,4 mm (volta) | baixa: 0,7 mm (volta) | Capacidade estática: 32 toneladas | "
       "Altura de levantamento padrão: 430 mm | Peso por conjunto padrão: 48 kg | Comprimento do pé fechado: 870 mm | "
       "aberto: 1.300 mm")

# ---- pág. 271 (protetores de quinta roda; grade de molduras sobrepostas)
_XL, _XR = (20, 295), (295, 571)
_Y71 = [85, 258, 402, 584, 726, 805]
for _c, _d, _col, _row, _mont, _i in [
        ("7002200", "PROTETOR 5A RODA JOST MODERNO", _XL, 0, JO, "Jost moderno"),
        ("7002201", "PROTETOR 5A RODA JOST ANTIGO A", _XR, 0, JO, "Jost antigo"),
        ("7003013", "PROTETOR 5A RODA REDONDO BRANCO", _XR, 1, "", "Protetor deslizante quinta roda universal redondo + trava"),
        ("7004001", "PROTETOR 5ª RODA JOST", _XL, 2, JO, "Furação modelo moderno | Fabbof Q 1001"),
        ("7004000", "PROTETOR 5ª RODA JOST", _XR, 2, JO, "Antiga"),
        ("7004003", "PROTETOR 5ª RODA FONTAINE", _XL, 3, FT, ""),
        ("7004004", "PROTETOR 5ª RODA MAXION", _XR, 3, MX, ""),
        ("7000830", "PARAFUSO PROTETOR 5 RODA 08 X 30 C/PORCA", (20, 571), 4, "", "")]:
    D(_c, _d, montadora=_mont, info=_i, foto_spec={"rect": [_col[0], _Y71[_row], _col[1], _Y71[_row + 1]]},
      tipo="PARAFUSO" if _c == "7000830" else "PROTETOR")
AJ["cod:7004002"]["foto_spec"] = {"rect": [20, 258, 295, 402]}
NOTAS.append("Pág. 271: 7004002 (protetor Canaparts Jost) também está na pág. 267. Pág. 272: página de anúncio "
             "(lançamento Suporte Rei), sem códigos.")

# ---- págs. 273-289: coxins Suporte Rei (pág. 273 = índice; demais = cards com "R-xxx")
import re  # noqa: E402

from tabela_livre import _spans  # noqa: E402

SR = "Suporte Rei"
MANUAIS = set(range(273, 290))
_IDX = {}
for _s in _spans(273)[0]:
    pass
_sp273 = _spans(273)[0]
for _s in _sp273:
    if _s["red"] and re.fullmatch(r"\d{5,12}", _s["t"]):
        _viz = sorted([x for x in _sp273 if not x["red"] and abs(x["y"] - _s["y"]) < 2 and 0 <= x["x"] - _s["x1"] < 40],
                      key=lambda x: x["x"])
        if _viz:
            _IDX[_s["t"]] = _viz[0]["t"].strip()
_MONT_SR = [(r"\bMBB?\b|MERCEDES", "Mercedes-Benz"), (r"\bVW\b|VOLKS", "Volkswagen"), (r"\bFORD\b", "Ford"),
            (r"\bSC\b|SCANIA", "Scania"), (r"\bDAF\b", "DAF"), (r"\bMAN\b", "MAN"), (r"VOLVO|\bVOL\b", "Volvo"),
            (r"IVECO", "Iveco"), (r"VOLARE", "Volare"), (r"\bMWM\b", "MWM"), (r"\bGM\b|CHEVROLET", "GM-Chevrolet"),
            (r"AGRALE", "Agrale"), (r"CUMMINS", "Cummins")]
_BOILER = re.compile(r"OBS:\s*Ao substituir os coxins verificar o N[ºo]\.? ?Original da peça\.?\s*Em caso de\s*dúvida,?\s*"
                     r"verificar o\s*N[ºo]\.?\s*do chassi e consultar concessionária\.?", re.I)
_REFTOK = re.compile(r"^[A-Z0-9]{0,6}[\d][\w.\-/]*$")


def _linhas(ss, tol=2.2):
    out = []
    for s in sorted(ss, key=lambda s: (s["y"], s["x"])):
        if out and abs(out[-1][0] - s["y"]) < tol:
            out[-1][1].append(s)
        else:
            out.append([s["y"], [s]])
    return [" ".join(x["t"].strip() for x in sorted(l[1], key=lambda s: s["x"])) for l in out]


def cards_rei(p):
    import pymupdf as fitz  # noqa: F401
    raw = json.load(open(os.path.join(WORK, "raw", f"p{p:03d}.json"), encoding="utf-8"))
    sp, imgs = _spans(p)
    n = 0
    cards = [c for c in raw["cards"] if c["id"] != 0]
    _iabv = [s for s in sp if "IABV" in s["t"]]
    big = [s for s in sp if s["red"] and re.fullmatch(r"\d{7,9}", s["t"]) and s["size"] >= 9
           and not any(abs(i["y"] - s["y"]) < 6 and 0 <= s["x"] - i["x1"] < 30 for i in _iabv)
           and not s["t"].startswith("498")]

    def _cods_em(r):
        return [s for s in big if r[0] <= (s["x"] + s["x1"]) / 2 <= r[2] and r[1] <= s["y"] + 3 <= r[3]]
    _cob = {id(s) for c in cards for s in _cods_em(c["rect"])}
    _sobra = [s for s in big if id(s) not in _cob]
    if any(len(_cods_em(c["rect"])) > 1 for c in cards) or _sobra:  # molduras fundidas/ausentes: grade pelos códigos
        _so_sobra = not any(len(_cods_em(c["rect"])) > 1 for c in cards)
        linhas = []
        for s in sorted(big, key=lambda s: s["y"]):
            if linhas and s["y"] - linhas[-1][-1]["y"] < 15:
                linhas[-1].append(s)
            else:
                linhas.append([s])
        ncol = max(len(l) for l in linhas)
        xs = [25 + k * (545 / ncol) for k in range(ncol + 1)]
        tops = [min(s["y"] for s in l) - 10 for l in linhas] + [806]
        if not _so_sobra:
            cards = []
        for i, l in enumerate(linhas):
            for s in l:
                if _so_sobra and id(s) in _cob:
                    continue
                k = min(int(((s["x"] + s["x1"]) / 2 - 25) // (545 / ncol)), ncol - 1)
                cards.append(dict(id=100 + len(cards), rect=[xs[k], tops[i], xs[k + 1], tops[i + 1]]))
    for c in cards:
        x0, y0, x1, y1 = c["rect"]
        cs = [s for s in sp if x0 - 1 <= (s["x"] + s["x1"]) / 2 <= x1 + 1 and y0 - 1 <= s["y"] + s["size"] / 2 <= y1 + 1]
        cods = [s for s in cs if s["red"] and re.fullmatch(r"\d{5,12}", s["t"].replace(" ", ""))]
        if not cods:
            continue
        big = max(cods, key=lambda s: s["size"])
        cods = [s for s in cods if s["size"] >= big["size"] - 1]
        rcod = [s for s in cs if re.fullmatch(r"R-\s?[\w.]+", s["t"].strip())]
        resto = [s for s in cs if s not in cods and s not in rcod]
        txt = re.sub(r"\s+", " ", " ".join(_linhas(resto))).strip()
        txt = _BOILER.sub(" ", txt)
        m = re.search(r"Subst(?:itui|\.)\s*(?:o\s*)?(?:N[ºo°]\.?\s*)?(?:Orig(?:inal)?\.?|o c[óo]d\. original:?)\s*", txt, re.I)
        ref = []
        if m:
            toks = re.split(r"\s+", txt[m.end():])
            k = 0
            while k < len(toks) and (toks[k] == "/" or _REFTOK.match(toks[k].strip("/,;()")) or toks[k] in ("-",)):
                if toks[k] not in ("/", "-"):
                    ref.append(toks[k].strip("/,;()"))
                k += 1
            txt = (txt[:m.start()] + " " + " ".join(toks[k:])).strip()
        for cod in cods:
            n += 1
            codigo = cod["t"].replace(" ", "")
            idx = _IDX.get(codigo, "")
            r_nome = rcod[0]["t"].replace(" ", "") if rcod else ""
            desc = re.sub(r"^R-\S+\s+", "", idx) if idx else ""
            fotos = [b for b in imgs if x0 - 2 <= (b[0] + b[2]) / 2 <= x1 + 2 and y0 - 2 <= (b[1] + b[3]) / 2 <= y1 + 2]
            foto = max(fotos, key=lambda b: (b[2] - b[0]) * (b[3] - b[1])) if fotos else None
            ms = [mm for rx, mm in _MONT_SR if re.search(rx, idx + " " + txt)]
            ADD.append(dict(pagina=p, card=c["id"], codigo=codigo, descricao=desc, marca=SR, _nao_agrupar=True,
                            variacoes=f"Suporte Rei {r_nome}" if r_nome else "", cod_ref=" / ".join(ref),
                            info=re.sub(r"\s+", " ", txt).strip(" |"), montadora=", ".join(dict.fromkeys(ms)),
                            foto_spec={"rect": foto} if foto else None, _sem_idx=not idx))


for _p in range(274, 290):
    cards_rei(_p)
NOTAS.append("Págs. 273-289 (coxins Suporte Rei): descrição curta conforme o índice da pág. 273; o texto completo do card "
             "(tarja, rosca, aplicação, sugestão) está em informações; o aviso padrão 'OBS: Ao substituir os coxins verificar o "
             "Nº original da peça...' foi omitido. Código Suporte Rei (R-xxx) na coluna de similares.")
# códigos que só aparecem no índice da pág. 273 (sem card)
_COM_CARD = {r["codigo"] for r in ADD if r["pagina"] >= 274}
for _c, _d in _IDX.items():
    if _c not in _COM_CARD:
        ADD.append(dict(pagina=273, card=1, codigo=_c, descricao=re.sub(r"^R-\S+\s+", "", _d), marca=SR, _nao_agrupar=True,
                        variacoes="Suporte Rei " + _d.split()[0], foto_spec=None,
                        info="Consta só no índice Suporte Rei (pág. 273), sem card com foto",
                        montadora=", ".join(dict.fromkeys(mm for rx, mm in _MONT_SR if re.search(rx, _d)))))
_CORTE = re.compile(r"\s(?=\(Tarja|Rosca\b|Largura\b|Aplicar\b|Sugest[ãa]o\b|OBS\b|Obs\b|MB:|Dimens|Fabricad|Actros:|Volvo:|"
                    r"Scania:|VW:|Ford:|DAF:|MAN:|Iveco:|Aplica[çc][ãa]o)")
for _r in ADD:
    if _r["pagina"] >= 274 and not _r["descricao"] and _r.get("info"):
        _frase = _CORTE.split(_r["info"], 1)[0].strip(" .")
        _r["descricao"] = _frase[:140].upper()
        _r["_desc_card"] = True

# estrutura do texto dos cards Suporte Rei: título "R-xxx ...", Aplicação, Dimensões, IABV, Produtos relacionados, Compatível
_LAB = re.compile(r"(Aplica[çc](?:[ãa]o|[õo]es)\s*:|DIMENS[ÕO]ES\s*:|Dimens[õo]es\s*:|Produtos relacionados\s*:|Compat[ií]vel\s*:|"
                  r"Montadoras\s*:|IABV\s+(?=\d)|Sugest[ãa]o Rei\s*:)", re.I)
for _r in ADD:
    if _r["pagina"] < 274:
        continue
    t = _r.get("info", "")
    _iab = re.findall(r"IABV\s*(?:-\s*\d{3,4}\s+)?(\d{7})", t)
    t = re.sub(r"IABV\s*(?:-\s*\d{3,4}\s+)?\d{7}", " ", t).strip()
    partes = _LAB.split(t)
    corpo, campos = partes[0].strip(), {}
    for k in range(1, len(partes) - 1, 2):
        lab = partes[k].strip().rstrip(":").lower()
        campos.setdefault(lab[:6], []).append(partes[k + 1].strip(" -/"))
    apl = campos.get("aplica", [])
    iabv = _iab + [re.match(r"\d+", x).group(0) for x in campos.get("iabv", []) if re.match(r"\d+", x)]
    resto_iabv = [re.sub(r"^\d+\s*", "", x) for x in campos.get("iabv", [])]
    info = [corpo] + [x for x in resto_iabv if x]
    for lab, nome in (("dimens", "Dimensões"), ("produt", "Produtos relacionados"), ("compat", "Compatível"),
                      ("montad", "Montadoras"), ("sugest", "Sugestão Rei")):
        for x in campos.get(lab, []):
            if x:
                info.append(f"{nome}: {x}")
    m = re.match(r"^(R-\s?[\w.]+)\s+([A-ZÀ-Ú0-9 /().,*\-+'\"]+?)(?=\s+[A-Z][a-zà-ú]|\s*$)", corpo)
    if m and (_r.get("_desc_card") or not _r["descricao"]):
        _r["descricao"] = m.group(2).strip()
        if not _r.get("variacoes"):
            _r["variacoes"] = "Suporte Rei " + m.group(1).replace(" ", "")
        info[0] = corpo[m.end():].strip()
    elif _r.get("_desc_card") and corpo.upper().startswith(_r["descricao"][:30]):
        info[0] = corpo[len(_r["descricao"]):].strip(" .")
    _r["aplicacao"] = " / ".join(apl)
    _r["info"] = " | ".join(x for x in info if x)
    if iabv:
        _r["variacoes"] = " / ".join(x for x in (_r.get("variacoes", ""), "IABV " + " / ".join(iabv)) if x)


def _reg(c):
    return [r for r in ADD if r["codigo"] == c and r["pagina"] >= 273]


def M(montadora, *codigos):
    """Montadora conforme logos do card."""
    for c in codigos:
        for r in _reg(c):
            r["montadora"] = montadora


def F(c, **kw):
    for r in _reg(c):
        r.update(kw)


MB_, VW_, FD_, SC_, VO_, AG_ = "Mercedes-Benz", "Volkswagen", "Ford", "Scania", "Volvo", "Agrale"
# 281
M("Volkswagen", "5000634", "5000610", "5000226")
M("Volkswagen, Volvo", "5000617")
M("Toyota", "5000210")
M(AG_, "5000951", "5000955", "5000961")
M("Scania, MAN", "5000877")
M(SC_, "5000329", "5000876")
F("5003062", descricao="SUPORTE FORD CARDAN ROL. 45MM", montadora="Volkswagen, Mercedes-Benz, Ford, Volvo, Agrale",
  cod_ref="2TO.521.351 / TJG/TMG.521.117 / 000.410.0222 / BG4X.4800-BA / 263.000 / 6012.009.021.00.6",
  variacoes="Suporte Rei R-3062", info="VW: substitui o Nº orig. 2TO.521.351 / TJG/TMG.521.117 e Suporte Rei R-3034 | "
  "Mercedes-Benz: substitui o Nº orig. 000.410.0222, Suporte Rei R-3030 e R-3034 | Ford: substitui o Nº orig. BG4X.4800-BA e "
  "Suporte Rei R-3034 | Volvo: substitui o Nº orig. 263.000, Suporte Rei R-3030 e R-3034 | Agrale / Volare: substitui o Nº "
  "orig. 6012.009.021.00.6 e Suporte Rei R-3034")


def M_pag(p, montadora, exceto=()):
    for r in ADD:
        if r["pagina"] == p and r["codigo"] not in exceto:
            r["montadora"] = montadora


# 274: todos com logo Mercedes-Benz, exceto o refil R-1206A (VW)
M_pag(274, MB_, exceto=("50012061",))
M(VW_, "50012061")
NOTAS.append("Págs. 273-289: em alguns cards a descrição curta do índice cita outra montadora que a do logo/texto do card "
             "(ex.: R-782 e R-3308 'COXIM VW' com logo Mercedes-Benz); a coluna de montadora segue o card.")
# 275: todos Mercedes-Benz
M_pag(275, MB_)
F("5000293", info="Coxim inferior da suspensão do quadro do radiador. Aplicar porca sext. M10 x 1,5 | 322.504.0212 = exportação | "
                  "Sugestão Rei: substituir os dois coxins (lado direito e lado esquerdo) | MB: 1924 - 1929 - 1932 - 1933 - 1934")
F("5000751", descricao="BUCHA MB TUBO OLHAL AMORTECEDOR",
  info="D. Bucha: Ext. 40mm x Int. 18,5mm x 20mm x Comp. 40,5mm | D. Espaçador: Ext. 35mm x Int. 19mm x Comp. 13mm | "
       "D. Tubo: Ext. 20mm x Int. 16,2mm x Comp. 63mm | (R-751) compatível com veículos Mercedes-Benz | "
       "Aplicações: suspensão dianteira (batentes, buchas do amortecedor, estabilizador e pino do tirante)")
F("5000480", info="Dimensões: Ext. 58mm x Int. 20,2mm x Comp. 61,5mm")
F("5003251", descricao="TUBO ESPACADOR DA BUCHA DA MOLA", variacoes="Suporte Rei R-3251 / IABV 4982060",
  info="Dimensões: Ext. 36mm x 31,5mm x 30mm x Int. 17,5mm x 18,5mm x")
F("5003393", info="Comp. 85,5mm")
F("5000496", info="Dimensões: Ext. 50mm x 53mm x Int.")
F("50034551", info="Coxim do braço da barra com apoio lateral da articulação da suspensão dianteira da cabine")
# 276 (Mercedes-Benz) e 277 (Volkswagen)
M_pag(276, MB_)
M_pag(277, VW_)
F("5003452", descricao="COXIM MB SUSP CABINE", aplicacao="Atego: 712/714K/714L/715L/716/716L",
  info="(R-3452) compatível com veículos Mercedes-Benz | Aplicações: suspensão da cabine (coxim, batente e bucha) | "
       "Montadoras: Mercedes-Benz")
F("5001285", cod_ref="TJG.711.116", info=" ".join(r["info"] for r in _reg("5001285")).replace("TJG.711.116 ", ""))
# 278-279
M_pag(278, VW_)
M("Ford, GM-Chevrolet", "5002700")
M("Mercedes-Benz, Volkswagen", "5003528")
M_pag(279, VW_)
F("5000631", cod_ref="2TA.899.369 / TAM.899.397",
  info=" ".join(r["info"] for r in _reg("5000631")).replace("TAM.899.397 ", ""))
F("5000627", cod_ref="TJG.899.369 / TJG.899.397 / 2TK.899.397-B / 2T0.899.397-C",
  info=" ".join(r["info"] for r in _reg("5000627")).replace("TJG.899.369 / TJG.899.397 / 2TK.899.397-B / 2T0.899.397-C ", ""))
# 280 (VW) e 282 (Scania)
M_pag(280, VW_)
M("Mercedes-Benz, Volkswagen", "5003706")
for _c, _ref in (("5000278", "TPL.199.381-A"), ("50002781", "TJG.199.381")):
    F(_c, cod_ref=_ref, info=" ".join(r["info"] for r in _reg(_c)).replace(_ref + " ", ""))
M_pag(282, SC_)
F("5000893", descricao="COXIM DA ARTICULAÇÃO DA SUSPENSÃO DO CAPÔ", aplicacao="Scania: T 114, T 124",
  info="Dimensões: Ext. 55mm x Int. 10,5mm x Comp. 70mm | Obs: efetuar a montagem do coxim com a seta sentido da cabine")
NOTAS.append("R-370F (5003706) aparece na pág. 274 (logo Mercedes-Benz) e na pág. 280 (logo VW, refs. Ford AC45...).")
# 283 (Scania) e 284
M_pag(283, SC_)
M("Volare", "5000098")
M(SC_, "5000866")
M("MAN", "50012001", "50012004", "5005045", "5001277")
M("DAF", "50012701", "50012702", "50012700", "50012703", "50012704")
# 285 (Volvo) e 286 (mancais de cardan)
M_pag(285, VO_)
F("50022629", descricao="REFIL BI PART SUSP CABINE")
_APL_1094 = ("VW Delivery | Ford: F 350 - F 4000 ano 2009 / 2010 em diante | Iveco Daily, Nova Daily, Nova Daily Scudato, Scudato, "
             "Ônibus: 50C16 - 70C17 - City Class - Ecoline (Maxivan) / (Scudato)")
F("50000061", descricao="COXIM DO MANCAL COM ROLAMENTO Ø INTERNO 40 MM DO EIXO CARDAN", aplicacao="MB 1113 ao 2213 (adaptação)",
  info="Montado com rolamento importado", montadora=MB_, tipo="COXIM")
F("5001094", descricao="MANCAL COMPLETO MODELO ORIGINAL COM ROLAMENTO BLINDADO, Ø INTERNO 40MM DO EIXO CARDAN",
  cod_ref="2P0.598.549 / 2P0.521.533 / 2P0.598.351 / 42.530.546", aplicacao=_APL_1094, info="",
  montadora="Volkswagen, Ford, Iveco", tipo="MANCAL")
F("50010941", descricao="ROL. 88.508 2RS", aplicacao=_APL_1094, info="Rolamento", montadora="Volkswagen, Ford, Iveco",
  tipo="ROLAMENTO")
F("5001307", descricao="CONJUNTO COMPLETO DE COXINS TRASEIRO DA SUSPENSÃO DA CABINE",
  cod_ref="23B.899.397 / 2R0.899.531 / WHT.008.105 / 2R2.803.875-C", aplicacao="VW Delivery, E-Delivery",
  info="Parafuso, porca, arruela, buchas e coxins", montadora=VW_, tipo="COXIM")
F("50020041", descricao="COXIM DO MANCAL COM ROLAMENTO DUPLA VEDAÇÃO, PISTA LARGA Ø INTERNO 70 MM DO EIXO CARDAN",
  aplicacao="VW Constellation | Volvo | MAN | Iveco", info="Aplicar em mancal com encaixe",
  montadora="Volkswagen, Iveco, Volvo, MAN", tipo="COXIM")
F("5000319", descricao="BATENTE DO FEIXE DE MOLA DO EIXO DA SUSPENSÃO TRASEIRA (ALTURA 150 MM)",
  info="Fabricado em chapa de aço de 12,5 mm", montadora=VO_, tipo="BATENTE")
NOTAS.append("Pág. 286: metade de baixo da página vazia.")
# 287
M("Iveco", "5006160", "5006155")
M(VO_, "5002236", "5002265", "5002251", "5000321", "5000671")
M("MWM", "5000644", "5000649", "5001221", "5000523")
M("MWM, Cummins", "5002266")
F("5001221", cod_ref="2P0.199.379", info=" ".join(r["info"] for r in _reg("5001221")).replace("Substitui Nº. 2P0.199.379 ", ""))
F("5002236", descricao="BATENTE DIANTEIRO DA SUSPENSÃO DA CABINE", tipo="BATENTE")
F("5002266", descricao="ANTIVIBRADOR DE ARRASTE NO VIRABREQUIM DO MOTOR CUMMINS", tipo="ANTIVIBRADOR")
NOTAS.append("Págs. 285/287: R-2236 (índice 'COXIM FORD') e R-2265 (índice 'COXIM SC') têm logo Volvo e aplicação Volvo; "
             "R-2266 (índice 'COXIM MWM BARRA ESTAB') é um antivibrador do virabrequim Cummins.")
# 288 (Ford)
M_pag(288, FD_)
M("Volkswagen, Ford, Agrale, Volare", "5000603")
M(VW_, "5000604", "5000612")
M("Ford, GM-Chevrolet", "5002700")
for _c, _ref in (("5000277", "TJG.899.607"), ("5000614", "TAM.899.397"),
                 ("5000628", "NFN.630090-AB / N 0221504 / E5HT.5A160-AA / TJG.899.397")):
    F(_c, cod_ref=" / ".join(x for x in (_reg(_c)[0]["cod_ref"], _ref) if x),
      info=" ".join(r["info"] for r in _reg(_c)).replace(_ref + " ", ""))
F("5000612", descricao="BUCHA AMORTECEDOR TRASEIRO SUPER/INFER (19X44M)", cod_ref="2RD.513.481",
  aplicacao="7100/7110/7120/8100/8120/815..", tipo="BUCHA")
F("5000603", variacoes="Suporte Rei R-603 / Produtos relacionados: IABV 2051", info="Dimensões: Ext. 59mm x Int. 44mm x Comp. 69,5mm | "
  "Compatível: VW, Ford, Agrale / Volare | Subst. o cód. original: *")
F("5000604", variacoes="Suporte Rei R-604 / Produtos relacionados: IABV 2058", info="Dimensões: Ext. 42mm x 45mm x Int. 26mm x "
  "Comp. 50mm | Compatível: VW")
# 289 (mancais de cardan)
_MAN = "COXIM DO MANCAL ({}) DO EIXO CARDAN COM ROLAMENTO Ø INTERNO {} MM"
_GERAL = "Mercedes-Benz, Volkswagen, GM-Chevrolet, Ford, Volvo, Iveco, Volare"
for _c, _d, _ref, _apl, _inf, _mont in [
        ("5003527", "COXIM DIANTEIRO DO SUPORTE DE FIXAÇÃO DA ARTICULAÇÃO DA SUSPENSÃO DA CABINE", "979.317.0012", "MB Accelo",
         "OBS: Verificar as condições dos amortecedores dianteiros da suspensão da cabine | Sugestão Rei: substituir os dois "
         "coxins (lado direito e lado esquerdo)", MB_),
        ("5000362", _MAN.format("SISTEMA ORIGINAL", 60), "1.113.031", "Scania | Ônibus",
         "Com bico graxeiro e retentores Ø interno 82 mm e 72 mm", SC_),
        ("5004010", _MAN.format("SISTEMA SUPORTE REI", 55), "208.394 / 177.526 / 189.513", "Scania | Ônibus",
         "Com bico graxeiro, pista de vedação do retentor | Substitui também Suporte Rei R-331 - R-331A - R-4007 e R-4017", SC_),
        ("5004011", _MAN.format("SISTEMA SUPORTE REI", 60), "1.113.031", "Scania | Ônibus",
         "Com bico graxeiro e retentores Ø interno 82 mm e 72 mm | Substitui também Suporte Rei R-362, R-4008 - R-4018", SC_),
        ("5004012", _MAN.format("SISTEMA SUPORTE REI", 60), "1.113.033 / 294.271", "Scania | Ônibus",
         "Com bico graxeiro e retentores Ø interno 77 mm e 72 mm | Substitui também Suporte Rei R-363, R-4013 - R-4023", SC_),
        ("50061001", "COXIM DO MANCAL COM ROLAMENTO PISTA LARGA Ø INTERNO 40 MM DO EIXO CARDAN", "2RBK.2117",
         "Ford F 350 - F 4000 ano 2000 em diante, Cargo", "Aplicar em suporte sem encaixe", FD_),
        ("50007781", "COXIM DO MANCAL COM ROLAMENTO PISTA LARGA Ø INTERNO 45 MM DO EIXO CARDAN", "",
         "MB, VW, GM, Ford, Volvo, Iveco, Volare", "Rol. 88.509 | Aplicar em mancal com encaixe", _GERAL),
        ("50009681", "COXIM DO MANCAL COM ROLAMENTO PISTA LARGA Ø INTERNO 40 MM DO EIXO CARDAN", "",
         "MB, VW, GM, Ford, Volvo, Iveco, Volare", "Rol. 88.508 | Aplicar em mancal com encaixe", _GERAL),
        ("5005069", "BUCHA DA BARRA ESTABILIZADORA DO EIXO DA SUSPENSÃO DIANTEIRA (SEM ALMA DE AÇO)", "2.392.175", "Scania",
         "Dimensões: Ext. 73,5mm x Int. 36,5mm x Comp. 69mm", SC_)]:
    F(_c, descricao=_d, cod_ref=_ref, aplicacao=_apl, info=_inf, montadora=_mont)
NOTAS.append("Pág. 289: quatro molduras vazias.")
M(SC_, "5000033", "5000026", "5000034", "5000029")
_TIPO_FIM = [(r"^APAR", "APARADOR DO CAPÔ"), (r"^BAT|BATENTE", "BATENTE"), (r"^PROT", "PROTETOR"), (r"^CINTA", "CINTA"),
             (r"^BORRACHA", "BORRACHA"), (r"ROL\.|ROLAMENTO", None), (r"^CONJ", "CONJUNTO DE COXINS"), (r"^REF|REFIL", "COXIM"),
             (r"^COX|COXIM", "COXIM"), (r"^BUCHA|MEIA BUCHA|^TUBO ESPACADOR", "BUCHA"), (r"^APOIO", "APOIO DE COXIM"),
             (r"^SUPORTE", "SUPORTE DE CARDAN"), (r"^MANCAL", "MANCAL"), (r"^CAPA", "CAPA ISOLANTE"),
             (r"CABO TERRA", "CABO TERRA"), (r"^JOST QUINTA|^QUINTA RODA", "QUINTA RODA"), (r"SAPATA", "SAPATA DE QUINTA RODA"),
             (r"^MOLA|MAXION MOLA", "MOLA"), (r"SUPORTE DO PE", "SUPORTE DO PÉ DE CARRETA"),
             (r"^KIT", "KIT"), (r"PINO REI", "PINO REI"), (r"^PINO", "PINO"), (r"BALANCA", "BALANÇA"), (r"ANEL", "ANEL"),
             (r"TRAVA", "TRAVA"), (r"GANCHO", "GANCHO"), (r"^MOLA|MAXION MOLA", "MOLA"), (r"PROTETOR", "PROTETOR"),
             (r"PF|PARAFUSO", "PARAFUSO"), (r"PORCA", "PORCA"), (r"ENGATE", "ENGATE"), (r"FLANGE", "FLANGE"),
             (r"PONTEIRA", "PONTEIRA"), (r"PE DE CARRETA", "PÉ DE CARRETA")]


def POS_PROC(r):
    d = r["descricao"].upper()
    if r.get("tipo") in ("ANTIVIBRADOR", "ROLAMENTO", "MANIVELA", "BARRA CENTRAL", "PRATO DE APOIO", "KIT"):
        return
    for rx, t in _TIPO_FIM:
        if re.search(rx, d):
            if t:
                r["tipo"] = t
            break
