# Capítulo 54 - Aditivos e Químicos Automotivos (págs. 558-568)
# Listas por caixa: cada caixa (seção) = 1 produto com os códigos como itens; código+descrição via tabela_livre.ler_pagina,
# seções dadas à mão (retângulos pelas bordas das molduras); foto = maior imagem da seção.
import re

from tabela_livre import _spans, ler_pagina

TIPOS = []
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(558, 569))
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


TIPOS += [(r"DOT", "FLUIDO DE FREIO"), (r"ADITIVO|PROTETIVO", "ADITIVO"), (r"DESCARBONIZANTE", "DESCARBONIZANTE"), (r"GRAXA", "GRAXA SPRAY"), (r"VASELINA|SILICONE SPRAY|GRAFITE SPRAY|DESENGRIPANTE|WHITE LUB", "SPRAY"),
          (r"LIMPA CONTATO", "LIMPA CONTATO"), (r"TINTA", "TINTA SPRAY"), (r"SILICONE|SELANTE|PU 40|ORBIFLEX", "SILICONE / SELANTE"), (r"FITA", "FITA"), (r"MARCADOR", "MARCADOR"),
          (r"COLA|ADESIVO|DUREPOXI|SUPER BOND", "ADESIVO"), (r"JUNTA|VEDA|VEDANTE", "VEDANTE"), (r"ESPUMA", "ESPUMA EXPANSIVA"), (r"AGUA", "ÁGUA DESMINERALIZADA")]
_H, _C, _O, _T, _3M = dict(marca="Hitech"), dict(marca="Car 80"), dict(marca="Orbi Química"), dict(marca="Tekbond"), dict(marca="3M")
_IC = "Indicado para linha leve automotiva e motocicletas"
# 558-562 (págs. impressas 557-561): linha Hitech
P(558, "9806000", "DOT 3 500ML HITECH", [46, 137, 140, 317], variacoes="HT-6000", info="Sistema hidráulico de frenagem de veículos automotivos | Ponto de ebulição > 205 °C | Úmido > 140 °C | Teor de água < 0,20% | Embalagem 24 x 500 ml / 40 x 200 ml | Linha leve", **_H)
P(558, "9806010", "DOT 4 500ML HITECH", [46, 315, 151, 491], variacoes="HT-6010", info="Sistema hidráulico de frenagem de automóveis, caminhões, ônibus, tratores | Ponto de ebulição > 230 °C | Úmido > 155 °C | Teor de H2O < 0,20% | Embalagem 24 x 500 / 40 x 200 ml | Linha leve e pesada", **_H)
P(558, "9806050", "DOT 5 500ML HITECH", [57, 501, 136, 648], variacoes="HT-6050", info="Lançamento | AP: BR9292-Tipo 5.1, SAE J 1703 e FMVSS N°116, DOT 5.1", **_H)
P(558, "9802070", "ADITIVO SUPER DIESEL S10 500ML", [74, 661, 167, 805], info="Colossos S10 Diesel | Ação descarbonizante | Limpeza do filtro de partículas diesel e DPF | Mata fungos e bactérias | Proteção contra corrosão", **_H)
_VU = "Concentrado sintético com base orgânica; protege contra corrosão no sistema de arrefecimento | Vida útil linha leve: 6 meses ou 30.000 km | Embalagem 12 x 1 L"
P(559, "9801012", "ADITIVO RADIADOR HITECH ORGANICO ALTA PERF 1L", [78, 223, 204, 462], variacoes="HT-10000", info=_VU, **_H)
P(559, "9800486", "ADITIVO RADIADOR CARRO DIESEL", [22, 551, 310, 810], info=_VU, **_H)
_RA = "Aplicação: a cada 01 litro de aditivo utiliza-se 08 litros de água | Diluição 1/8 | Super concentrado à base de polímeros sintetizados; proteção contra corrosão e cavitação"
P(560, "9805050", "ADITIVO RADIADOR HITECH SUPER CONCENTRADO 1L", [72, 230, 186, 439], variacoes="HT-5050", info=_RA + " | Embalagem 24 x 1 L", **_H)
P(560, "9805054", "ADITIVO RADIADOR HITECH SUPER CONCENTRADO 5L", [65, 580, 215, 785], variacoes="HT-5050", info=_RA, **_H)
P(561, "9802030", "ADITIVO COMBUSTIVEL ANTI ENTUPIMENTO 200ML", [72, 221, 218, 494], variacoes="HT-2030", info="Aditivo de combustível Tech Diesel | Trata até 200 litros | Evita entupimentos, principalmente do filtro do combustível | Mantém injetores limpos | Embalagem 24 x 200 ml", **_H)
P(561, "9802060", "ADITIVO RADIADOR ANTI ENTUPIMENTO ORGANICO 200ML", [83, 574, 206, 804], info="Não contém ácidos corrosivos | Biodegradável | Todos os tipos de radiadores automotivos, cargo, moto e motores estacionários | Embalagem 24 x 200 ml", **_H)
P(562, "9807020", "ADITIVO CONDICIONADOR METAIS 200ML", [93, 220, 208, 464], info="Tech Motor | Proteção contra desgaste, redução de atrito, proteção anticorrosiva e antioxidante | Motores a gasolina, etanol, GNV e diesel; compressores; equipamentos agrícolas; barcos; câmbio manual", **_H)
P(562, "9807040", "ADITIVO MOTOR REDUCAO FUMACA 500ML", [84, 571, 212, 791], variacoes="HT-7040", info="Stop Smoke | Reduz a emissão de fumaça, preenche as folgas, recupera a compressão | Motores a gasolina, álcool, diesel e GNV com alta quilometragem", **_H)
# 563-564 (págs. impressas 562-563): linha Car 80
P(563, "9840080", "DESCARBONIZANTE CAR 80", [203, 144, 280, 433], info=_IC + " | Limpa e descarboniza todo o sistema de alimentação de motores de 2 e 4 tempos, carburadores, bicos injetores e TBI", **_C)
P(563, "9791429", "GRAXA BRANCA DE LITIO SPRAY", [479, 153, 555, 412], info="Indicado para linha leve e pesada automotiva e motocicletas | Lubrificação pesada; não derrete, não sai na chuva ou água", **_C)
P(563, "9792059", "VASILINA SPREY", [202, 512, 288, 774], info=_IC, **_C)
P(563, "9792058", "SILICONE SPREY", [474, 511, 548, 766], info=_IC, **_C)
P(564, "9840002", "LIMPA CONTATO CAR", [463, 98, 545, 407], info="Lançamento | Limpa contato elétrico e eletrônico | Recupera a condutividade | Limpa e seca instantaneamente", **_C)
_SN = "Lançamento | Silicone neutro formador de juntas | Vedação de peças flangeadas, cárter, carcaça do diferencial, caixa de transmissão | Cárter, coletor de admissão, tampas de válvulas, diferencial e distribuição do motor"
P(564, "9848098", "SILICONE NEUTRO FORMADOR DE JUNTAS 8098 BLACK", [225, 456, 559, 547], info=_SN, **_C)
P(564, "9848099", "SILICONE NEUTRO FORMADOR DE JUNTAS 8099 GREY", [274, 652, 557, 716], info=_SN, **_C)
# 565-566 (págs. impressas 564-565): linha Orbi Química
P(565, "9800116", "WHITE LUB SUPER DESENGRIPANTE E PROTETIVO", [294, 88, 570, 336], variacoes="Cód. Orbi 146", info="Âmbar | 300ml/209g | Caixa 12 unidades", **_O)
P(565, "97522238", "DESENGRIPANTE PROMO ORBI 300ML/150G ORBI", [72, 248, 112, 392], **_O)
P(565, "8791986", "GRAFITE SPRAY", [203, 248, 251, 403], **_O)
P(565, "9800394", "ORBI LIMPA CONTATOS", [310, 295, 349, 422], variacoes="Cód. Orbi 7", info="Limpa contatos elétricos e eletrônicos | Incolor | 300ml/209g | Caixa 12 unidades", **_O)
GP(565, 6, "SELANTE ALTA TEMPERATURA", [("9800330", "SELANTE ALTA TEMPERATURA CINZA / PRETO"), ("9800115", "SELANTE ALTA TEMPERATURA VERMELHO")], [90, 442, 241, 592], **_T)
P(565, "9800486", "ORBI PROTETIVO PARA RADIADORES ROSA 1 LITRO", [466, 504, 508, 607], info="Anticorrosivo e antifervura | Diluição 50% água desmineralizada e 50% aditivo | Caixa 06 unidades", **_O)
P(565, "9800485", "ORBI PROTETIVO PARA RADIADORES AZUL 1 LITRO", [513, 504, 555, 608], info="Anticorrosivo e antifervura | Diluição 50% água desmineralizada e 50% aditivo | Caixa 06 unidades", **_O)
P(565, "9800329", "ORBIVED - ADESIVO DE SILICONE", [30, 681, 86, 785], variacoes="Cód. Orbi 5542", info="Multiuso flexível | Incolor | 50g - blister | Caixa 12 unidades | Não indicado como selante para motores", **_O)
P(565, "9800021", "ORBI-POX - ADESIVO EPÓXI", [228, 684, 283, 779], variacoes="Cód. Orbi 241", info="Componente A+B - pequenos reparos | Cura inicial em 10 minutos e total em 24 horas | Incolor | 40g (2x20g) | Caixa 12 unidades", **_O)
P(565, "9800316", "TRAVA PARAFUSOS TEK E ROSCAS 10G TEKBOND ANT0879", [293, 613, 364, 763], **_T)
P(565, "9800317", "AUTO LOCK TRAVA ROLAMENTO 10G", [436, 613, 506, 754], **_T)
NOTAS.append("Pág. 565: 9800329 é 'Orbived adesivo de silicone' e também 'selante alta temperatura incolor' (págs. 551 e 565); 9800486 é 'protetivo para radiadores rosa' e 'aditivo radiador carro "
             "diesel' (pág. 559); mantidos como impressos.")
P(566, "9801343", "ORBI COLA JUNTAS", [30, 156, 155, 244], variacoes="Cód. Orbi 5911", info="Adesivo para juntas de motores | Resistente de -20 ºC a 120 ºC | Âmbar | 75g - bisnaga | Caixa 12 unidades", **_O)
P(566, "9801181", "ORBI SELANTE PARA RADIADOR", [261, 130, 312, 256], variacoes="Cód. Orbi 4853", info="Veda e elimina os vazamentos | Branca | 200ml | Caixa 12 unidades", **_O)
P(566, "9800097", "TINTA SPRAY PRETO FOSCO ALTA TEMP 350ML", [331, 146, 361, 242], info="Resistente até 600 ºC", marca="White Color")
GP(566, 3, "TINTA SPRAY WHITE COLOR USO GERAL 340ML/220G", [("9800092", "TINTA SPRAY WHITE COLOR PRETO BRILHANTE"), ("9800096", "TINTA SPRAY WHITE COLOR PRETO FOSCO"), ("9800099", "TINTA SPRAY WHITE COLOR BRANCO BRILHANTE"),
                                                           ("9800180", "TINTA SPRAY WHITE COLOR BRANCO FOSCO"), ("9791895", "TINTA SPRAY WHITE COLOR CROMADO")],
   [417, 144, 567, 212], marca="White Color", info="Uso geral, ótimo acabamento | Caixa 06 unidades")
P(566, "9800548", "ORBI VEDA ESCAPE", [35, 340, 125, 418], variacoes="Cód. Orbi 5910", info="Vedante para escapamento | Cinza | 100g - bisnaga | 12 colmeias", **_O)
P(566, "9800242", "ORBI PLUS 1304 - VEDANTE SEMI SECATIVO", [200, 344, 287, 434], variacoes="Cód. Orbi 1453", info="Para roscas e flanges em geral | Branca | 100g - cartucho | Caixa 12 unidades", **_O)
P(566, "9801775", "ORBI FOAM - ESPUMA EXPANSIVA", [331, 278, 380, 416], info="Aplicação manual e excelente aderência | Expande até 3 vezes e rende até 30 litros | Bege | 300ml/190g | Caixa 12 unidades", **_O)
P(566, "9801429", "SILICONE INCOLOR ACETICO TUBO 280ML", [63, 519, 113, 651], **_O)
P(566, "9809036", "VEDA BAU CINZA PU 40 FIX 280ML", [192, 495, 245, 654], **_T)
P(566, "97517778", "ORBIFLEX USO GERAL PU 40 BRANCO 360G", [313, 504, 363, 652], **_O)
P(566, "9780339", "AGUA DESMINERALIZADA 1LT", [389, 521, 452, 643], marca="Radnaq")
P(566, "9780003", "DOT 3", [35, 678, 93, 803], marca="Radnaq")
P(566, "9780004", "DOT 4", [296, 681, 350, 802], marca="Radnaq")
# 567 (pág. impressa 566)
for _c, _d, _f, _kw in [("9801133", "ADESIVO DE CONTATO", [36, 69, 104, 123], {}), ("9800242", "ELIMINA JUNTA 1304 SEMI.S ORBI", [238, 92, 374, 120], _O),
                        ("9811104", "ELIMINA JUNTA 1104 SEMI-SECATI", [422, 97, 535, 125], dict(marca="Three Bond")), ("9811215", "SILICONE 1215J THREEBOND CINZA 85GRS", [39, 130, 72, 185], dict(marca="Three Bond")),
                        ("9821343", "COLA DE JUNTA 3M ORIGINAL", [210, 134, 284, 183], _3M), ("9811446", "SUPER BOND THEREE BOND 2G", [405, 132, 439, 184], dict(marca="Three Bond")),
                        ("9800312", "DUREPOXI 50 GRS LOCTITE", [29, 194, 110, 244], dict(marca="Loctite", info="2 horas")), ("9801054", "MANTA ASFALTICA P/TELHADO 30CM X 10M ALUM", [211, 196, 237, 248], {}),
                        ("9790060", "ANTI EMBAÇANTE 60ML MAXI VISAO", [405, 193, 430, 250], {}),
                        ("9805000", "SOLDA BLOCO LÍQUIDA WONDER 500ML", [28, 256, 61, 314], dict(marca="Wonder Weld", info="Recupera, sem desmontar o motor, rachaduras em cabeçotes, blocos de cilindros, guias e folgas nas sedes das válvulas e câmaras de água | Somente motores refrigerados a água")),
                        ("9800893", "PO DE RADIADOR WONDER WELD 60GR", [210, 256, 244, 314], dict(marca="Wonder Weld", info="Adicionar aos poucos no reservatório de água, ligar o motor em baixa rotação por 25 minutos e completar o nível")),
                        ("9800277", "GRAFITE EM PO FRASCO PEQUENO", [398, 256, 443, 313], {}), ("6016001", "MARCADOR ESF 60ML 2MM VERMELHO", [40, 328, 194, 369], {}),
                        ("6016002", "MARCADOR ESF 60ML 2MM BRANCO", [224, 327, 378, 368], {}), ("6016003", "MARCADOR ESF 60ML 2MM AZUL", [412, 326, 566, 367], {})]:
    P(567, _c, _d, _f, **_kw)
NOTAS.append("Pág. 567: 9800242 aparece como 'Orbi Plus 1304 vedante semi secativo' (pág. 566) e 'elimina junta 1304 semi.s Orbi'.")
# 568 (pág. impressa 567)
for _c, _d, _f, _kw in [("9744779", "COLA INSTANTANEA MARCENEIRO AEP 400 100G", [131, 95, 187, 232], dict(cod_ref="AEP400", info="Cianoacrilato | Transparente | 0,100 kg | Cura inicial 30 segundos | Cura final 24 horas")),
                        ("9801516", "ADESIVO INSTANTÂNIO 20G", [190, 91, 235, 213], {}), ("6011651", "FITA CREP SIMPLES 18X50 LONA FREIO", [318, 92, 387, 168], {}),
                        ("981650", "FITA CREPE AUTO 18MM", [319, 196, 408, 261], dict(marca="Norton", info="Código impresso com 6 dígitos")), ("9824850", "FITA CREPE SIMPLES 48X50", [311, 293, 423, 363], _3M),
                        ("9800872", "FITA VEDA ROSCA 12MMX10M", [34, 252, 165, 375], {}), ("9820110", "FITA DUPLA FACE 12MM X 1MT", [42, 399, 118, 455], _3M),
                        ("9821203", "FITA EMB. TRANSP. 50MTS", [313, 380, 421, 475], {}), ("9821496", "FITA DUPLA FACE 3M 12MM X 20MTS", [33, 490, 147, 596], _3M),
                        ("9821468", "FITA DUPLA FACE VHB 12MM X 20MTS", [56, 596, 171, 703], _3M), ("9821469", "FITA DUPLA FACE VHB 19MM X 20MTS", [48, 701, 179, 802], _3M)]:
    P(568, _c, _d, _f, **_kw)
