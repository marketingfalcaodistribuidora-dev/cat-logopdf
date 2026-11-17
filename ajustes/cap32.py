# Capítulo 32 - Elétrica: Chaves, Alternadores e Partida (págs. 399-401)
# 399: chaves gerais / ignição e cabo terra (cards grandes, texto em curvas em parte).
# 400-401: lançamentos ZM em grade de 3 colunas: código vermelho, descrição (fonte maior; a última linha é a aplicação),
#          e em fonte pequena "ZM xx.xxx.xx", "REF ORIG:" e similares (ARIELO, BOSCH, DELCO REMY, PRESTOLITE, MITSUBISHI...).
import re

from cards_grade import ler
from tabela_livre import _spans

TIPOS = [(r"^CHAVE", "CHAVE"), (r"^CABO", "CABO"), (r"^ALTERNADOR", "ALTERNADOR"), (r"^ESTATOR", "ESTATOR"), (r"^ROTOR", "ROTOR"),
         (r"^INDUZIDO", "INDUZIDO"), (r"^RELE AUX", "RELÉ AUXILIAR DE PARTIDA"), (r"^RELE", "RELÉ DE PARTIDA"),
         (r"^IMPULSOR", "IMPULSOR DE PARTIDA"), (r"^PINHA", "PINHÃO"), (r"^MOTOR PARTIDA", "MOTOR DE PARTIDA")]
AJ = {}
ADD = []
NOTAS = ["Págs. 400-401 (lançamentos ZM): o código ZM vai em similares junto das referências de outros fabricantes "
         "(Arielo, Bosch, Delco Remy, Prestolite, Mitsubishi, BZM, Zen, Lucas Indiel, WAI); a REF ORIG da montadora vai em referência."]
MANUAIS = set(range(399, 402))
_MONT = [(r"\bMB\b|MERCEDES|ACCELO|ATEGO|AXOR", "Mercedes-Benz"), (r"\bVW\b|VOLKS|TITAN", "Volkswagen"), (r"FORD|CARGO", "Ford"),
         (r"VOLVO", "Volvo"), (r"IVECO", "Iveco"), (r"SCANIA", "Scania"), (r"MITSUBISHI|FUSO", "Mitsubishi"), (r"\bMAN\b", "MAN"),
         (r"CHEVROLET", "Chevrolet"), (r"CUMMINS", "Cummins"), (r"MWM", "MWM")]


def _mont(t):
    return ", ".join(dict.fromkeys(m for rx, m in _MONT if re.search(rx, t, re.I)))


def _zm(p):
    sp, _ = _spans(p)
    fotos = {r["codigo"]: r["foto_spec"] for r in ler(p)}
    cods = [s for s in sp if s["red"] and re.fullmatch(r"\.?\d{9,10}", s["t"].strip()) and s["size"] >= 6.5]
    regs = []
    for s in sorted(cods, key=lambda s: (round(s["y"] / 20), s["x"])):
        col = min(int(((s["x"] + s["x1"]) / 2 - 25) // 182), 2)
        x0, x1 = 25 + col * 182, 25 + (col + 1) * 182
        abaixo = [t["y"] for t in cods if t is not s and x0 <= t["x"] < x1 and t["y"] > s["y"] + 5]
        y1 = min(abaixo) - 6 if abaixo else 812
        cs = [t for t in sp if t is not s and x0 - 1 <= t["x"] < x1 and s["y"] - 2 <= t["y"] < y1]
        grandes = [t for t in cs if t["size"] >= 6.5 and not t["red"]]
        peq = [t for t in cs if t["size"] < 6.5]
        lin = []
        for t in sorted(grandes, key=lambda t: (t["y"], t["x"])):
            if lin and abs(lin[-1][0] - t["y"]) < 2.5:
                lin[-1][1] += " " + t["t"].strip()
            else:
                lin.append([t["y"], t["t"].strip()])
        lin = [l[1] for l in lin]
        desc, apl = (" ".join(lin[:-1]), lin[-1]) if len(lin) > 1 else (" ".join(lin), "")
        zm, ref, sim = [], [], []
        atual = None
        for t in sorted(peq, key=lambda t: (t["y"], t["x"])):
            x = t["t"].strip()
            if re.match(r"ZM\b", x):
                zm.append(re.sub(r"^ZM\s*(ZM\s*)?", "", x))
                atual = None
            elif re.match(r"REF\.?\s*ORIG", x, re.I):
                v = re.sub(r"^REF\.?\s*ORIG\.?\s*:?\s*", "", x, flags=re.I)
                atual = ref
                if v:
                    ref.append(v)
            elif re.match(r"[A-Za-z][A-Za-z ]+:", x) or re.match(r"BOSCH\b", x):
                sim.append(re.sub(r"^BOSCH\s+(?=\d)", "BOSCH: ", x))
                atual = sim
            elif atual is not None:
                atual[-1:] = [(atual[-1] + " " + x).strip()] if atual else [x]
            else:
                ref.append(x)
        codigo = s["t"].strip().lstrip(".")
        regs.append(dict(pagina=p, card=len(regs) + 1, codigo=codigo, descricao=desc.strip(" .").upper(), marca="ZM",
                         cod_ref=" ".join(ref).strip(), variacoes=" / ".join([f"ZM {z}" for z in zm] + sim),
                         aplicacao=apl, info="", montadora=_mont(desc + " " + apl), _nao_agrupar=True,
                         foto_spec=fotos.get(codigo) or fotos.get(s["t"].strip())))
    return regs


for _p in (400, 401):
    ADD.extend(_zm(_p))


def F(p, c, **kw):
    regs = [r for r in ADD if r["pagina"] == p and r["codigo"] == c]
    assert regs, f"{c} não está na pág. {p}"
    for r in regs:
        r.update(kw)


_b = dict(_nao_agrupar=True, variacoes="", info="", cod_ref="", aplicacao="", marca="", montadora="")
# 399: chaves e cabo terra (texto em parte impresso como imagem)
ADD[0:0] = [
    dict(_b, pagina=399, card=1, codigo="7000628", descricao="CHAVE IGNICAO UNIVERSAL",
         aplicacao="Adaptação: uso geral, automotivo, tratores, caminhões, máquinas agrícolas, empilhadeiras, jeep, gaiola",
         foto_spec={"rect": [160, 106, 386, 221]}),
    dict(_b, pagina=399, card=2, codigo="557094004", descricao="CHAVE MB GERAL MANUAL 250A", cod_ref="A3845457008",
         montadora="Mercedes-Benz", foto_spec={"rect": [40, 232, 255, 372]}),
    dict(_b, pagina=399, card=3, codigo="557094015", descricao="CHAVE ATEGO/AXOR GERAL MANUAL", montadora="Mercedes-Benz",
         aplicacao="Atego / Axor", foto_spec={"rect": [29, 391, 253, 558]}),
    dict(_b, pagina=399, card=4, codigo="557101203", descricao="CABO TERRA 5ª RODA", info="30 CM",
         foto_spec={"rect": [22, 599, 570, 731]})]
# 401: dois cards com código e 1ª linha impressos como imagem
ADD += [
    dict(_b, pagina=401, card=90, codigo="160028180", descricao="RELE PARTIDA MB 24V", aplicacao="MB 1215/1218", marca="ZM",
         variacoes="ZM 2-818 / BOSCH: 1.987.BE2.017", montadora="Mercedes-Benz", foto_spec={"rect": [211, 66, 296, 125]},
         info="Código impresso como imagem (transcrito)"),
    dict(_b, pagina=401, card=91, codigo="168581801", descricao="IMPULSOR PARTIDA FORD/MB/VW/VOLVO 07 ESTRIAS",
         aplicacao="Aplica no pião ZM 85.818.05", marca="ZM", variacoes="ZM 85.818.01 / BZM: 99.1679.0 / DELCO REMY: 10515810",
         montadora="Ford, Mercedes-Benz, Volkswagen, Volvo", foto_spec={"rect": [394, 67, 445, 126]},
         info="Código e 1ª linha impressos como imagem (transcritos)")]
F(400, "1600040700", info="Código impresso com 10 dígitos", foto_spec={"rect": [392, 384, 463, 443]})
F(400, "1690014820", info="Código impresso com 10 dígitos", foto_spec={"rect": [24, 638, 100, 695]})
F(400, "169455001", descricao="ESTATOR P/ALTERNADOR MB.ACCELO 24V/80A NCB1")
NOTAS.append("Pág. 400: os códigos 1600040700 (relé auxiliar partida Ford FT8500) e 1690014820 (relé partida Ford 12V) estão impressos "
             "com 10 dígitos, diferente dos demais (9); foram mantidos como impressos.")
NOTAS.append("Pág. 401: 160028180 (relé partida MB 24V) e 168581801 (impulsor partida 07 estrias) têm código impresso como imagem.")
