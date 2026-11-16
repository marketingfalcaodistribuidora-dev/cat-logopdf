# Capítulo 18 - Grampos (págs. 242-248)
import re

from tabela_livre import ler_pagina

TIPOS = [(r"TRAVESSA", "TRAVESSA DE GRAMPO"), (r"PORCA", "PORCA DUPLA"), (r"^GR\b|GRAMPO", "GRAMPO DE MOLA")]
AJ = {}
ADD = []
MANUAIS = set(range(242, 249))
NOTAS = ["Pág. 242: página explicativa (modelos de grampo B, C, D, BA, CA, DA, DLA, BV, CV e como medir: A = bitola, "
         "B = abertura, C = comprimento), sem produtos.",
         "Grampos agrupados por bitola x abertura x tipo; cada comprimento é uma variação. As porcas duplas indicadas ao lado "
         "dos grampos também estão no capítulo Parafusos e Porcas."]
MB_VW_FORD = "Mercedes-Benz, Volkswagen, Ford"

_GR = re.compile(r"^GR\s+(SUSP\s+)?([\d/.,]+)\s*X\s*([\d.,]+)\s*X\s*([\d.,]+)\s*([A-Z]{1,3})?\b", re.I)


def titulo_grampo(desc):
    m = _GR.match(re.sub(r"(\d)\s*D(TRAS|DIANT)", r"\1 D \2", desc.strip()))
    if not m:
        return ""
    susp, bit, ab, _comp, tipo = m.groups()
    bit = bit + ("MM" if re.fullmatch(r"\d+", bit) else "")
    nome = "GRAMPO SUSPENSOR" if susp else "GRAMPO DE MOLA"
    return f"{nome} {bit} X {ab}" + (f" - TIPO {tipo.upper()}" if tipo else "")


def pagina(p, foto_grampo=None, montadora="", **kw):
    regs = ler_pagina(p, **kw)
    for r in regs:
        r.pop("_bbox", None)
        t = titulo_grampo(r["descricao"])
        if t:
            r["_titulo"] = t
            r["_nao_agrupar"] = False
            r["card"] = 100 + sorted({titulo_grampo(x["descricao"]) for x in regs if titulo_grampo(x["descricao"])}).index(t)
            if foto_grampo:
                r["foto_spec"] = {"rect": foto_grampo}
            if montadora:
                r["montadora"] = montadora
        else:
            r["_nao_agrupar"] = True
    ADD.extend(regs)
    return regs


def fix(p, codigo, **campos):
    achou = [r for r in ADD if r["pagina"] == p and r["codigo"] == codigo]
    assert achou, f"fix: {codigo} não está na pág. {p}"
    for r in achou:
        r.update(campos)


pagina(243, foto_grampo=[311, 96, 565, 196], montadora=MB_VW_FORD)
pagina(244, foto_grampo=[427, 303, 534, 555], montadora=MB_VW_FORD)
pagina(245, foto_grampo=[70, 290, 490, 510], montadora=MB_VW_FORD)
pagina(246, foto_grampo=[427, 188, 534, 440], montadora=MB_VW_FORD, dif_tam=15)
pagina(247, foto_grampo=[52, 110, 222, 194], dif_tam=15)
regs248 = pagina(248, gap_primeiro=320, dif_tam=30)

# 243
fix(243, "787882520", info="KTL-20")
for _c in ("787882540", "787882560"):
    fix(243, _c, info="KTL")
for _c in ("787814060", "787814055", "787814065", "787814075", "787814080", "787814085", "787814090",
           "787814076", "787814081", "787814086", "787814091"):
    fix(243, _c, info="LANÇAMENTO")
for _c in ("78188232", "781883220", "782092300", "783092401", "783492320"):
    fix(243, _c, _titulo="GRAMPO DE MOLA FIO ROSCA 3,50 GROSSA - TIPO DA", card=99, _nao_agrupar=False, tipo="GRAMPO DE MOLA", foto_spec={"rect": [432, 658, 551, 722]},
        montadora="")
# 246: código 782092380 com descrição "300"
NOTAS.append("Pág. 246: o código 782092380 está com a descrição 'GR 20 X 92 X 300 D' (o código sugere 380). Os códigos "
             "781872280 aparecem duas vezes (GR 18 X 72 X 280 D DIANT e GR 18 X 82 X 180 D TIANT); 'TIANT' como impresso.")
fix(246, "782092380", foto_spec={"rect": [45, 714, 205, 782]}, montadora="")
fix(246, "782092280", foto_spec={"rect": [45, 714, 205, 782]}, montadora="")
# 247: cada tipo num quadro; a passagem dos grampos de mola 24MM
for _c, _rect, _inf in [("782492340", [52, 110, 222, 194], ""), ("782492360", [52, 110, 222, 194], ""),
                        ("782414036", [54, 241, 164, 305], ""), ("782410532", [320, 245, 445, 300], ""),
                        ("782710249", [80, 360, 225, 430], ""), ("782414534", [82, 478, 228, 548], ""),
                        ("782414536", [82, 478, 228, 548], ""), ("782092340", [55, 590, 210, 665], "FIO ROSCA 3,50 GROSSA"),
                        ("783092420", [55, 590, 210, 665], "FIO ROSCA 3,50 GROSSA"),
                        ("782410216", [58, 712, 172, 790], "Grampo de Mola Tipo \"B\" Dianteiro 24 x 102 x 160 Polido (Volvo)"),
                        ("782410218", [58, 712, 172, 790], "Grampo de Mola Tipo \"B\" Dianteiro 24 x 102 x 160 Polido (Volvo)")]:
    fix(247, _c, foto_spec={"rect": _rect}, info=_inf)
for _c in ("782410216", "782410218"):
    fix(247, _c, montadora="Volvo")
fix(247, "3162400", descricao="PORCA DUPLA 24 X 2,0. MB")
NOTAS.append("Pág. 247: no último quadro a porca 3162400 está descrita como 'PORCA DUPLA 30MM MB FINA' (nos demais quadros é "
             "PORCA DUPLA 24 X 2,0. MB); mantida a descrição de 24 X 2,0.")
# 248: grampo de baú - os mesmos códigos do GR 5/8 X 92 B da pág. 244
_BAU = [r["codigo"] for r in regs248 if r.get("_titulo")]
ADD[:] = [r for r in ADD if not (r["pagina"] == 248 and r["codigo"] in _BAU)]
for r in ADD:
    if r["pagina"] == 244 and r["codigo"] in _BAU:
        r["info"] = "Também apresentado como GRAMPO DE BAÚ (pág. 248)"
NOTAS.append("Pág. 248 (Grampo de Baú): os códigos " + ", ".join(_BAU) + " são os mesmos do GR 5/8 X 92 B da pág. 244; "
             "registrados uma vez (pág. 244), com a observação.")
fix(248, "3165800", descricao="PORCA DUPLA POL 5/8 UNC")
fix(248, "78005892", descricao="TRAVESSA GRAMPO 5/8 X 92.", foto_spec={"rect": [400, 345, 552, 390]})

# porcas duplas (texto das caixinhas embaralhado na leitura)
for _p, _c, _d in [(243, "3160078", "PORCA DUPLA POL 7/8 UNF."), (243, "3160018", "PORCA DUPLA 18 X 1,5 MB"),
                   (243, "3162025", "PORCA DUPLA 20 X 2,5. MA"), (243, "3160300", "PORCA DUPLA 30MM MA 3,50 GROSSA."),
                   (244, "3160012", "PORCA DUPLA POL 1/2 UNF."), (244, "3160916", "PORCA DUPLA POL 9/16 UNF."),
                   (244, "3160058", "PORCA DUPLA POL 5/8 UNF"), (247, "3162403", "PORCA DUPLA 24 X 3,0. MA")]:
    fix(_p, _c, descricao=_d)


def POS_PROC(r):
    if r.get("tipo") in ("PORCA DUPLA", "TRAVESSA DE GRAMPO"):
        r["montadora"] = ""  # "MA"/"MB" = rosca métrica grossa/fina

# 246/247: descrição em letra pequena, desalinhada do código (lida da página)
for _p, _c, _d in [(246, "782092380", "GR 20 X 92 X 300 D"), (246, "782092280", "GR 20 X 92 X 280 D"),
                   (247, "782492340", "GR 24 X 92 X 340 D"), (247, "782492360", "GR 24 X 92 X 360 D"),
                   (247, "782414036", "GR 24 X 140 X 360 BA"), (247, "782410532", "GR 24 X 105 X 320 DLA PASSO 3,0"),
                   (247, "782710249", "GR 27 X 102 X 490 CA TEMP"), (247, "782414534", "GR 24 X 145 X 340 CA"),
                   (247, "782414536", "GR 24 X 145 X 360 CA"), (247, "782410216", "GR 24 X 102 X 160 B PASSO 3,00"),
                   (247, "782410218", "GR 24 X 102 X 180 B PASSO 3,00")]:
    _t = titulo_grampo(_d)
    fix(_p, _c, descricao=_d, tipo="GRAMPO DE MOLA", _titulo=_t, _nao_agrupar=False, card=200 + len(_t))
for _c in ("3162400", "3162403"):
    fix(247, _c, descricao="PORCA DUPLA 24 X 2,0. MB" if _c == "3162400" else "PORCA DUPLA 24 X 3,0. MA")
