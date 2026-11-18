# Capítulo 59 - Borracharia, Ar Comprimido e Compressores (págs. 614-623)
# Listas por caixa: cada caixa (seção) = 1 produto com os códigos como itens; código+descrição via tabela_livre.ler_pagina,
# seções dadas à mão (retângulos pelas bordas das molduras); foto = maior imagem da seção.
import re

from tabela_livre import _spans, ler_pagina

TIPOS = []
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(614, 624))
_CACHE = {}


def _itens(p):
    if p not in _CACHE:
        _CACHE[p] = ler_pagina(p)
    return _CACHE[p]


def _dentro(r, x, y):
    return r[0] - 1 <= x <= r[2] + 1 and r[1] - 1 <= y <= r[3] + 1


def S(p, secs, desc=None):
    """secs = [(título, [x0,y0,x1,y1])]; desc = {código: descrição} para corrigir/completar."""
    desc = desc or {}
    sp, imgs = _spans(p)
    # posição de cada item = posição do seu código (spans com o mesmo texto, na ordem)
    pos, usados = {}, set()
    for i in _itens(p):
        cands = [s for s in sp if s["t"].replace(" ", "") == i["codigo"] and id(s) not in usados]
        if cands:
            s = min(cands, key=lambda s: (s["y"], s["x"]))
            usados.add(id(s))
            pos[id(i)] = ((s["x"] + s["x1"]) / 2, s["y"] + 2)
        else:
            pos[id(i)] = (i["_bbox"][0] + 1, i["_bbox"][1] + 1)
    vistos = set()
    for n, (tit, r) in enumerate(secs, 1):
        its = [i for i in _itens(p) if _dentro(r, *pos[id(i)])]
        fotos = [b for b in imgs if _dentro(r, (b[0] + b[2]) / 2, (b[1] + b[3]) / 2) and (b[2] - b[0]) * (b[3] - b[1]) > 400]
        foto = {"rect": [round(v, 1) for v in max(fotos, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))]} if fotos else None
        for i in its:
            k = (i["codigo"], id(i))
            if k in vistos:
                continue
            vistos.add(k)
            d = desc.get(i["codigo"], i["descricao"])
            ADD.append(dict(pagina=p, card=n, codigo=i["codigo"], descricao=re.sub(r"^\+|^-\s*", "", d).strip(), cod_ref="",
                            variacoes="", aplicacao="", info="", marca="", montadora="", _titulo=tit if len(its) > 1 else "",
                            _nao_agrupar=len(its) == 1, foto_spec=foto))
    soltos = [i["codigo"] for i in _itens(p) if not any((i["codigo"], id(i)) == v for v in vistos)]
    assert not soltos, (p, soltos)


def LN(p, area, tol=2.5):
    """{código: texto da mesma linha} para códigos dentro da área (descrição longe do código)."""
    sp, _ = _spans(p)
    x0, y0, x1, y1 = area
    ss = [s for s in sp if x0 <= s["x"] <= x1 and y0 <= s["y"] <= y1]
    out = {}
    for c in ss:
        t = c["t"].replace(" ", "")
        if c["red"] and re.fullmatch(r"\d{6,9}", t):
            lin = sorted([s for s in ss if s is not c and abs(s["y"] - c["y"]) < tol and s["x"] > c["x"] and not s["red"]],
                         key=lambda s: s["x"])
            out[t] = re.sub(r"\s+", " ", " ".join(s["t"] for s in lin)).strip(" -")
    return out


def X(p, cod, d, foto, **kw):
    """Item fora das listas (código solto com foto própria)."""
    r = dict(pagina=p, card=90 + len(ADD), codigo=cod, descricao=d, cod_ref="", variacoes="", aplicacao="", info="", marca="",
             montadora="", _nao_agrupar=True, foto_spec={"rect": foto})
    r.update(kw)
    ADD.append(r)




def P(p, cod, desc, foto=None, **kw):
    """Produto único; foto=None = repetição de produto com foto em outra página (ou sem foto no catálogo)."""
    r = dict(pagina=p, card=500 + len(ADD), codigo=cod, descricao=desc, cod_ref="", variacoes="", aplicacao="", info="", marca="", montadora="",
             _nao_agrupar=True, foto_spec={"rect": foto} if foto else None)
    r.update(kw)
    ADD.append(r)


def GP(p, card, titulo, itens, foto=None, **kw):
    """Card com lista de códigos = 1 produto; itens = [(código, descrição)]."""
    for c, d in itens:
        r = dict(pagina=p, card=card, codigo=c, descricao=d, cod_ref="", variacoes="", aplicacao="", info="", marca="", montadora="",
                 _titulo=titulo, foto_spec={"rect": foto} if foto else None)
        r.update(kw)
        ADD.append(r)



import json as _json  # noqa: E402
import os as _os  # noqa: E402

from capitulos import WORK as _WORK  # noqa: E402


def _cards(p):
    return [c for c in _json.load(open(_os.path.join(_WORK, "raw", f"p{p:03d}.json"), encoding="utf-8"))["cards"] if c["id"]]


def FA(p, cod):
    """Foto automática: imagem da menor moldura que contém o código, a mais próxima e maior."""
    sp, imgs = _spans(p)
    ss = [s for s in sp if re.sub(r"[^0-9]", "", s["t"]) == cod]
    if not ss:
        return None
    s = ss[0]
    cx, cy = (s["x"] + s["x1"]) / 2, s["y"] + 3
    cs = [c["rect"] for c in _cards(p) if _dentro(c["rect"], cx, cy)]
    r = min(cs, key=lambda r: (r[2] - r[0]) * (r[3] - r[1])) if cs else [0, 0, 600, 850]
    f = [b for b in imgs if _dentro(r, (b[0] + b[2]) / 2, (b[1] + b[3]) / 2) and 700 < (b[2] - b[0]) * (b[3] - b[1]) < 250000] or \
        [b for b in imgs if 700 < (b[2] - b[0]) * (b[3] - b[1]) < 250000]
    if not f:
        return None
    b = min(f, key=lambda b: abs((b[0] + b[2]) / 2 - cx) + abs((b[1] + b[3]) / 2 - cy) - ((b[2] - b[0]) * (b[3] - b[1])) ** 0.5)
    return [round(v, 1) for v in b]


def A(p, cod, desc, foto=None, **kw):
    P(p, cod, desc, foto or FA(p, cod), **kw)


def LS(p, card, titulo, area, foto=None, desc=None, **kw):
    """Lista 'código descrição' dentro da área = 1 produto com itens."""
    d = LN(p, area)
    d.update(desc or {})
    _, imgs = _spans(p)
    if not foto:
        f = [b for b in imgs if _dentro(area, (b[0] + b[2]) / 2, (b[1] + b[3]) / 2) and 700 < (b[2] - b[0]) * (b[3] - b[1]) < 250000]
        foto = [round(v, 1) for v in max(f, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))] if f else None
    GP(p, card, titulo, [(c, re.sub(r"^[-–\\s]+", "", t)) for c, t in d.items()], foto, **kw)


TIPOS += [(r"VULCANIZADOR", "VULCANIZADOR"), (r"NUMERADOR", "NUMERADOR DE PNEUS"), (r"ASSENTADOR", "ASSENTADOR DE TALÃO"), (r"KIT PNEUMATICO", "KIT PNEUMÁTICO"), (r"ENGATE", "ENGATE RÁPIDO"), (r"BICO PARA MANGUEIRA", "BICO PARA MANGUEIRA"),
          (r"FILTRO REG|LUBRIFIL", "FILTRO REGULADOR DE AR"), (r"OLEO", "ÓLEO"), (r"LUBRIFICADOR", "LUBRIFICADOR"), (r"CONTRA PESO", "CONTRA PESO"), (r"CHAVE RODA", "CHAVE DE RODA"), (r"CABO DE TRANSMISS", "CABO"),
          (r"TAMPA", "TAMPA BICO PNEU"), (r"PITO|BICO P|BICO METAL|EXTENSAO", "BICO DE PNEU"), (r"SUPORTE", "SUPORTE"), (r"CALIBRADOR", "CALIBRADOR"), (r"RETIFICA", "RETÍFICA PNEUMÁTICA"), (r"DESTALONADOR|DESCOLADOR", "DESTALONADOR"),
          (r"KIT", "KIT DE REPARO"), (r"MACACO", "MACACO"), (r"CAVALETE", "CAVALETE"), (r"NUCLEO", "SACA NÚCLEO"), (r"INFLADOR", "INFLADOR"), (r"MEDIDOR", "MEDIDOR DE DESGASTE"), (r"MAQUINA|MOTOR|CHAVE MAQ|REPARO", "MÁQUINA SOLTA GRAMPO"),
          (r"TALHA", "TALHA MANUAL"), (r"COMPRESSOR", "COMPRESSOR"), (r"MANG", "MANGUEIRA"), (r"RABO", "RABO DE TATU"), (r"ABRACADEIRA", "ABRAÇADEIRA")]
_PI = "Pega no engate rápido da carreta 8000695 | Para adaptação de pneumático"
_SG, _SC = dict(marca="Sigma"), dict(marca="Schulz")
# 614 (pág. impressa 613)
A(614, "6070260", "VULCANIZADOR BORRACHARIA CAMINHAO 220V", [450, 94, 560, 274], cod_ref="VPA Caminhão", info="Vulcanização a quente em pneus de caminhões | Braço articulado | 2 conjuntos de calor | Peso 25KG | 110V ou 220V | 2 X 450W")
A(614, "6070002", "VULCANIZADOR BORRACHARIA CAMARA DE AR 220V", [427, 284, 564, 446], info="Conserto em câmara e válvula de automóveis e caminhões | Peso 13KG | 110V ou 220V | 400W | 135ºC")
A(614, "6070004", "VULCANIZADOR BORRACHARIA PASSEIO ARTIC 220V", [455, 459, 561, 619], cod_ref="VPA Passeio", info="Recuperar pneus com pequenos cortes | Peso 20kg | 110 ou 220V | 450W | 140ºC | Tempo médio 30 minutos")
A(614, "6070015", "NUMERADOR DE PNEUS 220V", [29, 652, 293, 765], info="Numerador/marcador elétrico de pneus para controle de frotas | Marcação numérica 0 a 9 | Adaptado para placa de letras ou logotipo")
A(614, "6071120", "ASSENTADOR DE TALAO VILUZ 100/120LB C/VAVULA", [305, 649, 569, 792], marca="Viluz", info="Pressão de trabalho 100/120LB | Reservatório super-reforçado | Válvula de segurança")
# 615 (pág. impressa 614)
for _c, _d, _f in [("9960014", "KIT PNEUMATICO MACHO 1/4 (05 PECAS)", [34, 130, 283, 234]), ("9960015", "KIT PNEUMATICO FEMEA 1/4 (05 PECAS)", [317, 137, 557, 235]),
                   ("9961201", "KIT PNEUMATICO MACHO 1/2 (02 PECAS)", [27, 294, 176, 444]), ("9961202", "KIT PNEUMATICO FEMEA 1/2 (02 PECAS)", [309, 295, 457, 439]),
                   ("8020719", "ENGATE RAPIDO PNEUMATICO FEMEA 1/2", [71, 506, 240, 601]), ("8020721", "ENGATE RAPIDO PNEUMATICO MACHO 1/2", [362, 511, 530, 600]),
                   ("8020722", "ENGATE RAPIDO PNEUMATICO FEMEA 1/4", [50, 635, 228, 799]), ("8020723", "ENGATE RAPIDO PNEUMATICO MACHO 1/4", [358, 684, 528, 789])]:
    A(615, _c, _d, _f)
# 616 (pág. impressa 615)
for _c, _d, _f in [("8001914", "PINO ENGATE FEMEA 16MM P/PNEUMATICA (1/4 X 17MM)", [72, 128, 160, 164]), ("8001945", "PINO ENGATE FEMEA 16MM P/PNEUMATICA (16MM X 17MM)", [241, 128, 338, 166]),
                   ("8001944", "PINO ENGATE FEMEA 1/2 P/PNEUMATICA", [425, 119, 527, 159]), ("8001419", "PINO ENGATE MACHO 1/4 P/PNEUMATICA", [84, 241, 173, 283]),
                   ("8001912", "PINO ENGATE MACHO 1/2 P/PNEUMATICA", [273, 238, 386, 291])]:
    A(616, _c, _d, _f, info=_PI)
A(616, "8000695", "ENGATE RAPIDO CARR. 16MM", [457, 210, 553, 243])
A(616, "8000694", "ENGATE RAPIDO CARR. 1/2MM", [453, 279, 554, 319])
A(616, "8000415", "BICO PARA MANGUEIRA 1/2 X 1/2N", [79, 361, 242, 430], info="14MM")
A(616, "8000416", "BICO PARA MANGUEIRA 1/4 X 1/2N", [107, 501, 275, 576])
A(616, "6010022", "FILTRO REGUALDOR AR 1/2 PROFISSIONAL", [301, 431, 406, 627], **_SG)
A(616, "9791353", "OLEO LUB. P/ EQUIP PNEUMATIC", [40, 677, 100, 793])
A(616, "6021400", "LUBRIFICADOR P/CHAVE PNEUMATICA 1/4", [158, 644, 288, 711])
A(616, "9901414", "ENGATE AR COMPRESSOR 1/4 M X F 1/4", [378, 656, 571, 806], marca="Schulz")
# 617 (pág. impressa 616)
GP(617, 1, "CONTRA PESO GARRA BAIXA", [(c, f"CONTRA PESO GARRA BAIXA {g}") for c, g in (("8101549", "10G"), ("8101550", "15G"), ("8101551", "20G"), ("8101552", "25G"), ("8101553", "30G"), ("8101554", "35G"),
                                                                                         ("8101555", "40G"), ("8101556", "45G"), ("8101557", "50G"), ("8101559", "60G"))],
   [134, 96, 205, 150], info="Embalagem 100 unidades (10G a 35G) e 050 unidades (40G a 60G) | Contrapeso para roda comum | Ferro zincado")
A(617, "8101579", "CONTRA PESO ADESIVO 10/5", [30, 185, 149, 286], info="Embalagem 100 unidades | Roda em liga leve | Ferro zincado | Fita colante dupla face")
A(617, "9934855", "CHAVE RODA CRUZ 17X19 X 13/16 23MM /20 | 17X19 X 21X23 350MM", [240, 220, 304, 275], info="Promoção")
A(617, "6013500", "CABO DE TRANSMISSÃO DE CARGA TIPO CHUPETA 300A", [424, 227, 499, 298], marca="Riosul", info="Promoção")
for _c, _d, _f in [("8100003", "TAMPA PLASTICA BICO PNEU", [33, 335, 92, 407]), ("8101976", "PITO P PNEU ARO 13 S CAMARA", [234, 336, 340, 383]), ("8101722", "PITO P PNEU ARO 14 S CAMARA", [412, 336, 518, 383]),
                   ("8100001", "BICO PNEU S/C BASE FERRO 313", [50, 413, 183, 453]), ("8100574", "BICO PNEU S/C B.BORRACHA CURTO 90MM", [216, 410, 377, 445]), ("7710274", "BICO PNEU S/C B.BORRACHA 573", [403, 410, 544, 445]),
                   ("8100274", "BICO PNEU S/C RODA RAIADA BOR. 573", [32, 493, 203, 523]), ("8100576", "BICO PNEU S/C B.BORRACHA LONGO 576", [32, 493, 203, 523]), ("7711500", "BICO PLASTICO PNEU EXTENSAO 150MM", [221, 482, 372, 509]),
                   ("7711501", "BICO PLASTICO PNEU EXTENSAO PRETA 150MM", [388, 490, 564, 512]), ("7711503", "BICO METAL PNEU EXTENSAO 110MM", [37, 548, 203, 564]), ("7714005", "EXTENSAO FLEXIVEL 210MM", [219, 540, 370, 566]),
                   ("8106180", "BICO PNEU AGRICULA BASE FERRO TR-618A", [386, 546, 483, 584]), ("7000200", "SUPORTE SIMPLES P/EXTENSAO BICO", [28, 612, 130, 668]), ("9963145", "RETIFICA PNEUMATICA 1/4 2400 RPM", [214, 618, 384, 753])]:
    A(617, _c, _d, _f)
A(617, "9941345", 'CONJUNTO LUBRIFIL 1/2" PROFISSIONAL', [392, 612, 466, 696], info="Filtragem, regulagem de pressão do ar comprimido e lubrificação de toda linha pneumática", **_SG)
A(617, "10024116", "CLB-750/GII-20 CALIBRADOR DE PNEUS", [30, 687, 124, 804], marca="Planatc", cod_ref="CLB-750/GII-20", info="Calibrador de parede em ABS | PSI/BAR | Display de 3 dígitos 1,5\" | Função pneu vazio | Mangueira de 20 mts | 220 volts")
A(617, "6010022", "FILTRO REGULADOR AR 1/2 PROFISSIONAL", [390, 706, 439, 797], **_SG)
# 618 (pág. impressa 617)
A(618, "6024628", "DESTALONADOR DE PNEU MANUAL 1200MM", [43, 112, 546, 143])
A(618, "6020200", "CALIBRADOR ANALOG C/BICO 0 A 200 PSI -1/4", [125, 178, 293, 346])
A(618, "6020900", "KIT REPARO P/REMENDO PNEU CARRO", [329, 184, 529, 282])
A(618, "6025202", "DESCOLADOR PNEU AGRICOLA", [30, 351, 192, 454], info="Pneus agrícolas e caminhão | Encaixe chave de impacto 1/2 | Ferro maciço | Aro simples ou de uma única peça | Ônibus, tratores, veículos grandes | 30 x 8,5 x 30 cm | 11,20 Kg")
A(618, "6021392", "KIT DESMOTAGEM CARRO 5 PÇS LT-A1932", [346, 351, 489, 502], cod_ref="LT-A1932")
A(618, "6021500", "MACACO TIPO SANFONA R 1,5 TON", [36, 636, 199, 784], info="Fabricado em ferro | Acompanha manivela | Altura máx. 35 cm, mín. 10 cm | Capacidade 1,5 TON")
A(618, "6020201", "CAVALETE 2 TON (PAR)", [312, 603, 518, 801], info="Estrutura metálica reforçada | 10 posições com pino trava | Altura 275 a 425 mm | Capacidade 2 TON | 2,7 Kg")
# 619 (pág. impressa 618)
for _c, _d, _f, _i in [("6020025", "FERRAMENTA SACA NUCLEO 25MM", [30, 99, 263, 149], ""), ("6020060", "FERRAMENTA SACA NUCLEO 60MM", [330, 100, 560, 160], ""), ("6020100", "FERRAMENTA SACA NUCLEO 100MM", [45, 170, 330, 212], ""),
                       ("6020002", "FERRAMENTA SACA NUCLEO 2 USOS", [47, 255, 197, 343], ""), ("6020004", "FERRAMENTA SACA NUCLEO OMEGA 4 USOS", [263, 274, 370, 347], ""), ("6020014", "NUCLEO CURTO NIQUELADO", [420, 239, 491, 349], ""),
                       ("6022800", "CALIBRADOR C/MED 280MM ALUM BICO RETO", [67, 396, 517, 444], ""), ("6021414", "INFLADOR DUPLO LONGO BICO RETO 1/4 C/EMBORACHADO", [32, 512, 560, 575], ""),
                       ("6020209", "INFLADOR DUPLO 150MM 1/4/BICO", [46, 610, 300, 669], "Lançamento"), ("6024140", "BICO INFLADOR COM PRISILHA 1/4", [32, 681, 172, 796], ""),
                       ("6022013", "MEDIDOR DESGASTE DE PNEU AÇO", [302, 678, 435, 801], "Lançamento")]:
    A(619, _c, _d, _f, info=_i)
# 620 (pág. impressa 619)
_MG = "Obs: soquete não incluso | 380v | 5CV | Cabeça giratória 360º | 18 r/min | Torque 550 KGF | Trifásico"
A(620, "6022250", "MAQUINA ELETRICA SOLTAR PORCA GRAMPO 380V BICO GIRATORIO CURTA", [358, 96, 568, 252], info="Lançamento | " + _MG)
A(620, "6025600", "MAQUINA ELETRICA SOLTAR PORCA GRAMPO BICO GIRATORIO LONGA", [162, 263, 569, 409], info=_MG)
A(620, "6028040", "CHAVE MAQ GRAMPO MOLA CR800 220V/380V 40AMP", [44, 502, 222, 673], info="Lançamento")
A(620, "60256560", "MOTOR 360 MAQUINA ELETRICA SOLTA PORCA GRAMPO", [330, 505, 569, 660], cod_ref="56560")
A(620, "6020056", "REPARO KIT MAQUINA SOLTA GRAMPO MOLA 360 GR", [229, 712, 550, 802])
# 621-622 (págs. impressas 620-621)
A(621, "6020206", "TALHA MANUAL 2 TON 6MTS - CORRENTE", [262, 236, 517, 518], info="Içamento de cargas e objetos pesados | Ganchos para cargas até 2.000 Kg")
A(621, "9900011", "OLEO MS LUB SCHULZ COMPRESSOR", [39, 610, 128, 794], info="Para compressores de ar alternativos de pistão | Óleo mineral | 1 litro", **_SC)
_TR = "Troca de óleo: 1,5 LT primeira troca 8 horas; 1,5 LT segunda troca 40 horas; demais a cada 200 horas"
A(622, "9907759", "COMPRESSOR AR CSL 20 BR/200 BRAVO 220/380V", [284, 96, 488, 250], info="20/200 litros | 175 lbf/pol² | 20 pés³/min (566 l/min) | Trifásico | 5 HP | 970 RPM | 2 cilindros | 84 dB | Saída 1/2\" | " + _TR, **_SC)
A(622, "9909346", "COMPRESSOR AR PISTAO FORT MSW 40/425 220/380V", [266, 280, 560, 486], info="40/425 litros | 10 hp | 427 L | 496 kg | 650 x 1380 x 1990 mm | 40 pcm (1132 l/min) | 175 lbf/pol² | 3 pistões em V | " + _TR, **_SC)
A(622, "9903459", "COMPRESSOR AR PISTAO FORT MSW 60/425 220/380V", [244, 497, 565, 756], info="60/427 litros | Trifásico 220/380 V | 15 CV - 11 KW | 60 pcm (1699 L/min) | 175 lbf/pol² | 427 L | Inmetro registro 001245/2018", **_SC)
A(622, "9901011", "OLEO COMPRESSOR SCHULZ 1LT", [132, 647, 198, 770], info="MS Lub: protege contra desgaste e oxidação e reduz o atrito", **_SC)
# 623 (pág. impressa 622)
A(623, "7741260", "MANG.BOR. PNEUMATICA AZUL REFORCADA 1/2", [246, 118, 501, 252])
A(623, "8000415", "BICO PARA MANGUEIRA AZUL 1/2 X 1/2 NPT", [61, 154, 183, 206], info="Para adaptação de pneumático | 14MM")
P(623, "8000413", "BICO PARA MANGUEIRA AZUL 1/2 X 1/2 NPT", [61, 154, 183, 206], info="Citado em 'aplica-se na mangueira azul' (02 peças)")
A(623, "8001226", "RABO DE TATU 12 OU 1/2 P/MANG AZUL LAVAGEM", [225, 259, 382, 295])
A(623, "9990456", "ABRACADEIRA MANG. 1/2 POSTO LAVAGEM", [40, 331, 194, 397], info="Aplica-se na mangueira azul (02 peças)")
A(623, "9941345", 'CONJUNTO LUBRIFIL 1/2" PROFISSIONAL', [89, 494, 239, 665], info="Filtragem, regulagem de pressão e lubrificação da linha pneumática | Rosca fêmea 1/2 NPT", **_SG)
NOTAS.append("Pág. 623: o bico azul 1/2 x 1/2 NPT está impresso com o código 8000415 no card e 8000413 na lista 'aplica-se na mangueira azul'; os dois foram lançados.")
