# Capítulo 39 - Acessórios Cromados Nicolini (págs. 448-461)
# Páginas de layout livre (cards mesclados): registros montados à mão a partir da imagem; foto = imagem mais próxima do código.
import re

from tabela_livre import _spans

TIPOS = [(r"^LED LUMENS|^LED ", "LÂMPADA LED"), (r"^LAMPADA LED", "LÂMPADA LED"), (r"^LAMPADA", "LÂMPADA"), (r"^LANT", "LANTERNA"), (r"^FAROL", "FAROL"), (r"^SUPORTE", "SUPORTE"), (r"^GIRO", "GIROFLEX"), (r"^TERMINAL", "TERMINAL"), (r"^CAPA", "CAPA DE TERMINAL"), (r"^FITA", "FITA ISOLANTE"), (r"^SOQ", "SOQUETE"),
         (r"^CHICOTE", "CHICOTE"), (r"^CON\.", "CONECTOR"), (r"^RELE", "RELÉ"), (r"^BOT[ÃA]O", "BOTÃO"), (r"^CHAVE", "CHAVE"),
         (r"^PORTA FUSIVEL", "PORTA FUSÍVEL"), (r"^FUSIVEL|^PORTA (MINI|LAMINA|MAX|VIDRO)", "FUSÍVEL"), (r"^CABO", "CABO"),
         (r"^GARRA", "GARRA DE BATERIA"), (r"^FIO", "FIO"), (r"^SIRENE|^ALARME", "SIRENE"), (r"^MB SOQUETE", "SOQUETE")]
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(448, 462))
_CACHE = {}
_NCOL = {}  # colunas de cards por página (padrão 3)


def _pag(p):
    if p not in _CACHE:
        _CACHE[p] = _spans(p)
    return _CACHE[p]


def _foto(p, cod, min_area=500, acima_primeiro=False):
    sp, imgs = _pag(p)
    ss = [s for s in sp if s["t"].replace(" ", "").strip() == cod] or [s for s in sp if cod in s["t"].replace(" ", "")]
    if not ss:
        return None
    s = ss[0]
    cx, cy = (s["x"] + s["x1"]) / 2, s["y"]
    w = 545 / _NCOL.get(p, 3)
    col = int((cx - 25) // w)
    cand = [b for b in imgs if (b[2] - b[0]) * (b[3] - b[1]) >= min_area and int(((b[0] + b[2]) / 2 - 25) // w) == col]
    if not cand:
        return None
    # imagens entre este código e o próximo código vermelho da mesma coluna (foto abaixo); senão, acima
    outros = [t["y"] for t in sp if t["red"] and re.fullmatch(r"\d{7,9}", t["t"].replace(" ", "")) and t is not s
              and int(((t["x"] + t["x1"]) / 2 - 25) // w) == col]
    prox = min([y for y in outros if y > cy + 5], default=900)
    ant = max([y for y in outros if y < cy - 5], default=0)
    abaixo = [b for b in cand if cy - 15 <= (b[1] + b[3]) / 2 < prox]
    acima = [b for b in cand if ant < (b[1] + b[3]) / 2 < cy]
    cand = (acima or abaixo or cand) if acima_primeiro else (abaixo or acima or cand)
    b = min(cand, key=lambda b: abs((b[0] + b[2]) / 2 - cx) + abs((b[1] + b[3]) / 2 - cy))
    return {"rect": [round(v, 1) for v in b]}


def R(p, cod, desc, card=None, foto=None, acima=False, **kw):
    r = dict(pagina=p, card=card or (len(ADD) + 1), codigo=cod, descricao=desc, cod_ref="", variacoes="", aplicacao="", info="",
             marca="", montadora="", _nao_agrupar=card is None)
    r.update(kw)
    r["foto_spec"] = {"rect": foto} if foto else _foto(p, cod, acima_primeiro=acima)
    ADD.append(r)
    return r


def G(p, card, titulo, itens, foto=None, **kw):
    """Card com vários códigos = 1 produto (itens = [(código, descrição)])."""
    for c, d in itens:
        R(p, c, d, card=card, foto=foto, _titulo=titulo, **kw)


TIPOS = [(r"^CAPA", "CAPA DE PORCA"), (r"^CALOTA", "CALOTA"), (r"^ESPELHO", "ESPELHO DE RODA")]
NOTAS = ["Págs. 448-461 (Nicolini): a referência Nicolini de cada linha (CPP, CLP, CLM...) está em similares; linhas sem código "
         "Falcão no card não viram produto."]
_N = dict(marca="Nicolini")


def K(p, card, titulo, itens, foto, refs="", **kw):
    """Card Nicolini: itens = [(código, descrição)]; refs = linhas do card (referências Nicolini)."""
    kw = dict(_N, **kw)
    if len(itens) == 1:
        R(p, itens[0][0], itens[0][1], foto=foto, variacoes=refs, **kw)
    else:
        G(p, card, titulo, itens, foto=foto, variacoes=refs, **kw)


# 448 (pág. impressa 447): capas de porca (ABS cromadas e ABS black)
_CR = "ABS cromada"
K(448, 1, "CAPA DE PORCA SEXTAVADA", [("5061805", "CAPA DE PORCA SEXTAVADA Nº 18"), ("5061900", "CAPA DE PORCA SEXTAVADA Nº 19"),
                                      ("5101035", "CAPA DE PORCA SEXTAVADA Nº 21")], [53, 147, 143, 201],
  "CPP1034 - Nº 18 / CPP1032 - Nº 19 / CPP1035 - Nº 21 / CPP1065 - Nº 22 (sem código)", info=_CR)
K(448, 2, "", [("5062400", "CAPA DE PORCA SEXTAVADA Nº 24 BAIXA")], [180, 139, 282, 189], "CPP1036 - Nº 24 baixa", info=_CR)
K(448, 3, "CAPA DE PORCA SEXTAVADA", [("5062401", "CAPA DE PORCA SEXTAVADA Nº 24 ALTA"), ("5060027", "CAPA DE PORCA SEXTAVADA Nº 27")],
  [337, 143, 425, 195], "CPP1001 - Nº 24 alta / CPP1002 - Nº 27", info=_CR)
K(448, 4, "CAPA DE PORCA SEXTAVADA", [("5060030", "CAPA DE PORCA SEXTAVADA Nº 30"), ("5060032", "CAPA DE PORCA SEXTAVADA Nº 32"),
                                      ("5060033", "CAPA DE PORCA SEXTAVADA Nº 33")], [464, 138, 553, 190],
  "CPP1003 - Nº 30 / CPP1006 - Nº 32 / CPP1009 - Nº 33", info=_CR)
K(448, 5, "CAPA DE PORCA BELGA", [("7001811", "CAPA DE PORCA BELGA Nº 24"), ("7001810", "CAPA DE PORCA BELGA Nº 27"),
                                  ("5063200", "CAPA DE PORCA BELGA Nº 32"), ("5063300", "CAPA DE PORCA BELGA Nº 33")],
  [54, 270, 144, 340], "Ver marca - Nº 24 / ver marca - Nº 27 / CPP1080 - Nº 32 / CPP1081 - Nº 33", info=_CR)
K(448, 7, "CAPA DE PORCA BOLIVIANA", [("7001918", "CAPA DE PORCA BOLIVIANA Nº 18"), ("7001919", "CAPA DE PORCA BOLIVIANA Nº 19"),
                                      ("7001921", "CAPA DE PORCA BOLIVIANA Nº 21"), ("7001824", "CAPA DE PORCA BOLIVIANA Nº 24"),
                                      ("7001809", "CAPA DE PORCA BOLIVIANA Nº 27"), ("5061105", "CAPA DE PORCA BOLIVIANA Nº 32/33")],
  [333, 280, 409, 335], "Ver marca - Nº 18, 19, 21, 24, 27 / CPP1105 - Nº 32/33", info=_CR)
K(448, 9, "CAPA DE PORCA MEXICANA", [("7001089", "CAPA DE PORCA MEXICANA Nº 32"), ("7001090", "CAPA DE PORCA MEXICANA Nº 33")],
  [58, 385, 141, 442], "CPP1089 - Nº 32 / CPP1090 - Nº 33", info=_CR)
K(448, 10, "", [("50603233", "CAPA DE PORCA RUSSA Nº 32/33")], [194, 381, 268, 436], "CPP1103 - Nº 32/33", info=_CR)
K(448, 11, "CAPA DE PORCA GREGA", [("7003332", "CAPA DE PORCA GREGA Nº 32/33"), ("7002333", "CAPA DE PORCA GREGA Nº 32/33 (VER MARCA)")],
  [325, 386, 417, 449], "CPP1145 - Nº 32/33 / ver marca - Nº 32/33", info=_CR)
K(448, 12, "", [("7003323", "CAPA DE PORCA BRASILEIRISSIMA Nº 32/33")], [474, 380, 559, 440], "Ver marca - Nº 32/33", info=_CR)
K(448, 13, "CAPA DE PORCA SUICA", [("7007032", "CAPA DE PORCA SUICA Nº 32"), ("7003233", "CAPA DE PORCA SUICA Nº 32/33"),
                                  ("7007033", "CAPA DE PORCA SUICA Nº 33")], [69, 521, 127, 601], "Ver marca", info=_CR + " | 60MM")
K(448, 14, "", [("7000124", "CAPA DE PORCA GERMANY COM ABA Nº 32/33")], [212, 510, 280, 591], "", info=_CR)
K(448, 15, "", [("7000125", "CAPA DE PORCA GERMANY SEM ABA Nº 32/33")], [338, 506, 401, 595], "Ver marca", info=_CR)
K(448, 16, "", [("5062700", "CAPA PORCA CROM 27MM COMPATIVEL MB ACTORS/AXOR")], [453, 513, 527, 587], "Ver marca", info=_CR,
  montadora="Mercedes-Benz")
K(448, 17, "", [("5063030", "CAPA PORCA CROM CH 30MM SCANIA MODERNA")], [77, 667, 138, 730], "Ver marca", info=_CR, montadora="Scania")
K(448, 18, "", [("7001136", "CAPA DE PORCA BOLIVIANA Nº 32/33 BLACK")], [208, 743, 274, 800], "CPP1136 - Nº 32/33", info="ABS black")
K(448, 19, "CAPA DE PORCA BELGA BLACK", [("7001134", "CAPA DE PORCA BELGA Nº 32 BLACK"), ("7001135", "CAPA DE PORCA BELGA Nº 33 BLACK")],
  [328, 752, 400, 807], "CPP1134 - Nº 32 / CPP1135 - Nº 33", info="ABS black")
K(448, 20, "CAPA DE PORCA SEXTAVADA BLACK", [("5060320", "CAPA DE PORCA SEXTAVADA Nº 32 BLACK"),
                                            ("5060330", "CAPA DE PORCA SEXTAVADA Nº 33 BLACK")], [487, 748, 545, 785],
  "CPP1131 - Nº 24 / CPP1132 - Nº 27 / CPP1133 - Nº 30 (sem código) / CPP1119 - Nº 32 / CPP1094 - Nº 33", info="ABS black")
NOTAS.append("Pág. 448: as capas italiana (CPP1092/CPP1091), argentina (CPP1039/CPP1040) e parte das sextavadas não têm código "
             "Falcão no card; 50603233 (capa russa) está impresso com 8 dígitos; 'ACTORS' impresso assim no card 5062700.")
# 449 (pág. impressa 448): calotas e componentes
K(449, 1, "CALOTA TOP LINE", [("7002384", "CALOTA TOP LINE PAR"), ("7002003", "CALOTA TOP LINE DIREITA"),
                              ("7002007", "CALOTA TOP LINE ESQUERDA")], [70, 155, 206, 237],
  "CLP2075 - par / CLP4162 - direita / CLP4163 - esquerda", info="ABS / cromada com refletivo laranja")
K(449, 3, "", [("7007012", "CALOTA CROM EVOLUTION RETA SEM REFLETIVO(2016)")], [406, 137, 535, 236], "Ver marca")
K(449, 4, "", [("7001016", "CALOTA 3 PONTAS COM CALIBRADOR DE PNEU (METAL)")], [425, 259, 525, 344],
  "CLM1016 - com calibrador de pneu / CLM1017 - sem calibrador de pneu", info="Cromada / ar")
K(449, 5, "", [("7001120", "CALOTA 4 PONTAS HÉLICE PAR COM CALIBRADOR DE PNEU")], [78, 408, 198, 495],
  "CLM1020 - par com calibrador de pneu / CLM3019 - lado direito / CLM3020 - lado esquerdo", info='Sob encomenda | Cromada / aro 16"')
K(449, 6, "", [("7001125", "CALOTA 5 PONTAS COM CALIBRADOR DE PNEU")], [333, 400, 444, 493],
  "CLM1014 - com calibrador de pneu / CLM1015 - sem calibrador de pneu", info='Cromada / aro 20" / par')
K(449, 7, "", [("7001116", "CALOTA 3 PONTAS ABS COM CALIBRADOR DE PNEU ARO 16")], [69, 549, 161, 630],
  "CLP1006 - com calibrador de pneu / CLP1007 - sem calibrador de pneu", info='Calota em ABS | Cromada / aro 16" / par')
K(449, 8, "", [("7001320", "CALOTA 3 PONTAS ABS COM CALIBRADOR DE PNEU ARO 20")], [381, 548, 453, 628],
  "CLP1001 - com calibrador de pneu / CLP1003 - sem calibrador de pneu", info='Calota em ABS | Cromada / aro 20" / par')
K(449, 9, "", [("7001321", "CALOTA 3 PONTAS COM CALIBRADOR DE PNEU ARO 22")], [55, 686, 156, 763],
  "CLM1009 - com calibrador de pneu / CLM1011 - sem calibrador de pneu", info='Cromada / aro 22" / par')
K(449, 10, "", [("7002011", "CALOTA 10 FUROS 2 SUPORTE RODA DIANTEIRA")], [226, 674, 332, 773], "CLM1004 - roda dianteira",
  info='Cromada / aro 20" / par')
R(449, "5095033", "ESPELHO RODA CONJUNTO (RANDON)", foto=[420, 680, 534, 801], montadora="Randon")
NOTAS.append("Pág. 449: a calota PLP 2000 (CLP2076 / CLP4167 / CLP4168) não tem código Falcão no card.")
# 450 (pág. impressa 449): componentes e cano rodo ar
TIPOS += [(r"^SUPORTE", "SUPORTE DA CALOTA"), (r"^BICO", "BICO"), (r"^ALONGADOR", "ALONGADOR DE CINEMÁTICO"),
          (r"^CINEM", "CINEMÁTICO"), (r"^CANO", "CANO RODO AR"), (r"^CONECTOR", "CONECTOR"), (r"^TEE", "TEE"),
          (r"^NIPLE", "NIPLE"), (r"^PORCA", "PORCA"), (r"^LUVA", "LUVA"), (r"^ENGATE", "ENGATE RÁPIDO")]
K(450, 1, "", [("7001001", "SUPORTE DA CALOTA COM TUDO 45MM")], [110, 121, 177, 195], "SPM1004 - com tudo 45mm / ver marca",
  info="Zincado / veículos com calibrador de pneu")
K(450, 2, "", [("7000040", "BICO DE SAÍDA 5/16 X 7/16 24F")], [253, 114, 338, 198], "MPN120456",
  info="Para sextavados / cinemáticos com saída 5/16")
K(450, 3, "ALONGADOR DE CINEMÁTICO", [("7001008", "ALONGADOR DE CINEMÁTICO 20MM"), ("7001025", "ALONGADOR DE CINEMÁTICO 25MM"),
                                      ("7001002", "ALONGADOR DE CINEMÁTICO 30MM"), ("7001004", "ALONGADOR DE CINEMÁTICO 40MM"),
                                      ("7001003", "ALONGADOR DE CINEMÁTICO 60MM"), ("7001080", "ALONGADOR DE CINEMÁTICO 80MM")],
  [407, 154, 527, 209], "ACM1020 - 25MM / ACM1021 - 40MM / ACM1023 - 60MM / ACM1024 - 80MM / demais: ver marca")
K(450, 4, "", [("7001110", "CINEMÁTICO BÁSICO")], [113, 280, 298, 380], "CIC10001",
  info="Fixador na flange / transfere o ar da rede aos pneus")
R(450, "7008005", "CINEMÁTICO TACO AR", foto=[355, 264, 530, 376], marca="Taco-Ar", variacoes="Ver marca")
G(450, 6, "CANO RODO AR ALUMINIO", [("7000060", "CANO RODO AR ALUMINIO 0,60"), ("7000070", "CANO RODO AR ALUMINIO 0,70"),
                                    ("7000005", "CANO RODO AR ALUMINIO 0,80"), ("7000006", "CANO RODO AR ALUMINIO 0,90"),
                                    ("7000007", "CANO RODO AR ALUMINIO 1,00"), ("7000008", "CANO RODO AR ALUMINIO 1,20"),
                                    ("7001500", "CANO RODO AR ALUMINIO 1,50")], foto=[50, 505, 580, 635])
# 451 (pág. impressa 450): conexões e componentes do painel
K(451, 1, "", [("7000036", "CONECTOR TEE DE REDE")], [75, 170, 158, 225], "PNC20129", info="Conexões de rede | 5/16 | Distribuição de ar pela rede")
R(451, "7000101", "TEE BUZINA 1/4 X 5/16 X 1/4 COMPLETO", foto=[197, 152, 263, 204])
R(451, "8001618", "TEE UNIAO EMENDA NYLON 1/4", foto=[314, 168, 385, 214])
K(451, 4, "", [("7000013", "NIPLE DE EMENDA")], [430, 148, 524, 235], "PNC20116", info="5/16 | Efetuar emenda na rede quando necessário")
K(451, 5, "", [("7000034", "PORCA SEXTAVADA MULTIUSO")], [85, 290, 146, 354], "MPN120009",
  info="Fixação de tubos de nylon PA6 e PA12 pela rede e rodas")
K(451, 6, "", [("7711500", "BICO PLASTICO PNEU EXTENSÃO")], [217, 310, 351, 372], "Ver marca")
R(451, "7000035", "PORCA CALOTA RODO AR GRANDE", foto=[425, 290, 501, 369])
R(451, "7000216", "PORCA TEE BUZINA 1/4", foto=[84, 444, 147, 506])
R(451, "7000045", "PORCA TEE REDE 5/16", foto=[239, 441, 316, 517])
K(451, 10, "", [("7000038", "LUVA VEDADORA TAMPÃO")], [427, 448, 493, 502], "MPN120008", info="Isolar as saídas de ar das conexões quando necessário")
R(451, "7000228", "BICO SAIDA AR DIRETO FEMEA 16 X MACHO 7/16", foto=[101, 673, 178, 733],
  info="Obs: porca não acompanha | Rosca fêmea 16MM | Rosca macho 7/16 | Porca multi-uso de rodoar")
K(451, 12, "", [("7000226", "ENGATE RÁPIDO COM PORCA GIRATÓRIO ZAMAC")], [365, 642, 474, 692], "MPN120667",
  info="Engate rápido com porca giratória para sextavados (vasculhar cabine)")
# 452 (pág. impressa 451): componentes do rodo ar
TIPOS += [(r"^SEXTAVADO", "SEXTAVADO"), (r"^QUADRADO", "QUADRADO"), (r"^EXTENS", "EXTENSÃO DA VÁLVULA"), (r"^PINO", "PINO ENGATE"),
          (r"^V[AÁ]LVULA", "VÁLVULA DE RETENÇÃO"), (r"^PROLONGADOR", "PROLONGADOR DE VÁLVULA"), (r"^ABRA", "ABRAÇADEIRA")]
_CRR = "Conector a rede a roda"
K(452, 1, "", [("7000014", "SEXTAVADO CURTO")], [64, 115, 157, 187], "MPN120016", info=_CRR)
R(452, "7000099", "SUPORTE SEXTAVADO EM L UNIVERSAL", foto=[204, 96, 268, 174])
R(452, "7000015", "QUADRADO CURTO CARROCERIA MADEIRA", foto=[314, 125, 414, 180], info=_CRR)
R(452, "7007000", "QUADRADO LONGO C/PORCA 70MM", foto=[440, 125, 530, 178], info=_CRR)
R(452, "7000085", "QUADRADO LONGO C/PORCA 85MM", foto=[65, 270, 158, 317], info=_CRR)
R(452, "7004038", "QUADRADO CARROCERIA MADEIRA 40MM", foto=[181, 259, 299, 320], info=_CRR)
R(452, "7000233", "QUADRADO CURTO 2 SAIDAS", foto=[315, 253, 411, 337], info=_CRR)
K(452, 8, "", [("7000430", "EXTENSÃO DA VÁLVULA DE RETENÇÃO BICO CURVO")], [457, 259, 520, 328], "MPN120010 - com porca giratória",
  info="Adaptado no bico do pneu externo facilitando a colocação do prolongador")
K(452, 9, "", [("7000043", "EXTENSÃO DA VÁLVULA DE RETENÇÃO BICO CURVO FIXO")], [58, 411, 147, 471], "PNC20221 - bico curvo fixo com guia",
  info="Porca fixa | Adaptado no bico do pneu externo facilitando a colocação do prolongador")
R(452, "7001100", "PINO ENGATE PARA RODOAR", foto=[176, 423, 274, 473])
R(452, "7001000", "ENGATE PARA RODOAR COM PINO", foto=[312, 419, 416, 467])
R(452, "7004103", "ENGATE PARA GAS COM CONECTOR 5/16", foto=[433, 431, 539, 463])
R(452, "7004138", "ENGATE PARA GAS COM CONECTOR 3/8", foto=[57, 568, 164, 603])
R(452, "7004104", "ENGATE PARA BUJAO COM PINO 3/8 E PORCA RODOAR", foto=[184, 566, 289, 614])
K(452, 15, "", [("7000012", "VÁLVULA DE RETENÇÃO DE AR PROLONGADOR ZERO")], [312, 563, 399, 621], "MPN120017",
  info="Adaptável em todos os bicos de pneus")
R(452, "7004047", "PROLONGADOR VALVULA LONGO", foto=[418, 541, 541, 626])
R(452, "7000012", "PROLONGADOR VALVULA RETENCAO Z", foto=[50, 711, 159, 782])
K(452, 18, "", [("7001005", "ABRAÇADEIRA REDONDA PARA REDE PCT. 100 UNIDS")], [187, 707, 281, 741], "PAT1005 - para rede / pct. 100unids",
  info="Ver marca | Fixação das mangueiras de nylon")
R(452, "8016608", "TEE UNIAO PLASTICA 6 X 6 X 8", foto=[344, 712, 389, 745], info="Buzina 6MM / buzina 6MM / 8MM rodo ar")
R(452, "8016606", "TEE UNIAO PLASTICA 8 X 8 X 6", foto=[464, 716, 526, 759], info="8MM / 8MM / 6MM")
NOTAS.append("Pág. 452: o código 7000012 aparece em dois cards (válvula de retenção de ar prolongador zero e prolongador válvula "
             "retenção Z); 7001005 (abraçadeira redonda) também está como abraçadeira para mangueira rodo ar no cap. 38 (pág. 446).")
# 453 (pág. impressa 452): flanges
TIPOS += [(r"^FLANGE", "FLANGE")]
for _c, _d, _f, _kw in [
        ("7000009", "FLANGE CARR. DIV S/FURO GRANDE", [51, 86, 158, 201], dict(marca="Nicolini / Capanema")),
        ("7000010", "FLANGE RANDON NOVA 4 FUROS PEQUENA", [227, 86, 329, 202], dict(marca="Nicolini / Capanema", montadora="Randon")),
        ("7009062", "FLANGE EM U MB 1620 FORD CARG VW", [380, 94, 523, 199],
         dict(marca="Capanema", montadora="Mercedes-Benz, Ford, Volkswagen")),
        ("7000081", "FLANGE DIANT MB/VW/FORD", [69, 228, 173, 320],
         dict(marca="Capanema", variacoes="Ver marca", montadora="Mercedes-Benz, Volkswagen, Ford")),
        ("7009048", "FLANGE TRACAO MB 1111 A 1113 PEITINHO (140MM)", [220, 220, 353, 323], dict(variacoes="Ver marca", montadora="Mercedes-Benz")),
        ("7000092", "FLANGE TRACAO MB 1313 A 1620 PEITAO (210MM)", [396, 227, 506, 309], dict(variacoes="Ver marca", montadora="Mercedes-Benz")),
        ("7009066", "FLANGE TRACAO 04 PES", [88, 359, 186, 474],
         dict(marca="Nicolini", montadora="Mercedes-Benz, Volkswagen, Ford")),
        ("7000080", "FLANGE DIANT 1111 A 1630", [251, 356, 361, 460], dict(variacoes="Ver marca", montadora="Mercedes-Benz")),
        ("7009045", "FLANGE DIANT VW 790 /8.140/8.150", [421, 355, 524, 450], dict(variacoes="Ver marca", montadora="Volkswagen")),
        ("7009067", "FLANGE TRAÇÃO TRIPÉ VOLVO FH/NH", [78, 498, 171, 605], dict(variacoes="Ver marca", montadora="Volvo")),
        ("7009029", "FLANGE DIANTEIRA AGRALE VOLARE ROSCA W8", [252, 500, 369, 604], dict(montadora="Agrale, Volare")),
        ("7003058", "FLANGE TRAÇÃO MODELO MB", [400, 497, 509, 602],
         dict(variacoes="PNC30058", marca="Nicolini", montadora="Mercedes-Benz, Volkswagen, Iveco",
              aplicacao="Compatível com VW 7.90 / Iveco / Vertis 90V / 16/1")),
        ("7003033", "FLANGE MODELO VOLVO FH GLOBETROTTHER", [51, 735, 282, 804], dict(variacoes="PNC30033", marca="Nicolini", montadora="Volvo")),
        ("7003034", "FLANGE MODELO VOLVO DISCO", [330, 702, 559, 770],
         dict(variacoes="PNC30034", marca="Nicolini", montadora="Volvo, Scania, Iveco", aplicacao="Compatível com Scania e Iveco"))]:
    R(453, _c, _d, foto=_f, **_kw)
# 454 (pág. impressa 453): painéis, motor interclima, refil palha
TIPOS += [(r"^PAINEL", "PAINEL"), (r"^ESCOVA", "ESCOVA"), (r"^MOTOR", "MOTOR INTERCLIMA"), (r"^REFIL", "REFIL PALHA"),
          (r"^COROTE", "COROTE"), (r"^SUP", "SUPORTE"), (r"^TAMPA", "TAMPA COROTE"), (r"^TORNEIRA", "TORNEIRA")]
_TA = dict(marca="Taco-Ar", variacoes="Ver marca")
R(454, "7001009", "PAINEL MB 1620", foto=[69, 142, 145, 219], montadora="Mercedes-Benz", **_TA)
R(454, "7001050", "PAINEL SLIM", foto=[220, 157, 322, 206], **_TA)
R(454, "7001056", "PAINEL VW CONSTELLATION", foto=[399, 157, 497, 215], montadora="Volkswagen", **_TA)
R(454, "2059", "ESCOVA DO MOTOR DO INTERCLIMA 12V / 24V", foto=[62, 378, 210, 465], variacoes="Ver marca",
  info="Código impresso como '2059'")
R(454, "7004412", "MOTOR INTERCLIMA 12V", foto=[237, 380, 376, 452], variacoes="Ver marca")
R(454, "7004424", "MOTOR INTERCLIMA 24V", foto=[388, 376, 531, 450], variacoes="Ver marca")
K(454, 7, "", [("7001007", "REFIL PALHA UNIVERSAL")], [368, 540, 491, 645], "MPN110001 - universal / ver marca",
  info="Reposição do perfil de palha")
NOTAS.append("Pág. 454: a escova do motor do interclima está impressa com o código '2059' (4 dígitos).")
# 455 (pág. impressa 454): corotes (reservatório de água)
_AG = "Armazenamento de água"
K(455, 1, "", [("7001026", "COROTE ESPELHADO 26 LITROS SUPORTE ABERTO")], [97, 166, 222, 280],
  "COR1001 - suporte aberto / COR1002 - suporte fechado (sem código)", info=_AG)
K(455, 2, "", [("7001006", "COROTE PRETO 26 LITROS SUPORTE ABERTO")], [334, 150, 478, 272], "COR1003 - suporte aberto", info=_AG)
K(455, 3, "", [("7001033", "COROTE ESPELHADO 15 LITROS SUPORTE ABERTO")], [86, 374, 220, 501], "COR1018 - suporte aberto", info=_AG)
K(455, 4, "", [("7001032", "COROTE PRETO 15 LITROS SUPORTE ABERTO")], [377, 386, 493, 505], "COR1031 - suporte aberto", info=_AG)
R(455, "7000318", "COROTE 42 LTS COMUM BEPO", foto=[88, 582, 224, 724], marca="Bepo")
# 456 (pág. impressa 455): suportes, tampas e torneira de corote
K(456, 1, "", [("7001029", "SUPORTE 26 LITROS ABERTO")], [94, 153, 202, 296], "COR1029 - aberto")
K(456, 2, "", [("7001051", "SUP PARA COROTE 50 LTS (CINTA)")], [400, 151, 523, 312], "COR1073",
  info="Suporte fixação do reservatório (corote)")
R(456, "7001021", "TAMPA COROTE D'AGUA NICOLINE COM FURO", foto=[60, 358, 241, 452], marca="Nicolini",
  variacoes="COR1020 - com furo", info="Também anunciada como 'tampa plástica do corote Nicolini'")
R(456, "7005127", "TAMPA PLASTICA COROTE D'AGUA 16/25L", foto=[83, 494, 219, 564], variacoes="Ver marca")
R(456, "7001022", "TAMPA COROTE D'AGUA 50L NICOLINI", foto=[360, 583, 502, 713], marca="Nicolini")
K(456, 6, "", [("7005000", "TORNEIRA PLÁSTICA PARA COROTE")], [34, 662, 234, 815], "MR01053 - para corote")
NOTAS.append("Pág. 456: o código 7001021 aparece em dois cards (tampa corote d'água Nicoline com furo e tampa plástica do corote "
             "Nicolini COR1020 - com furo); foi lançado uma vez.")
# 457 (pág. impressa 456): suportes (lançamento 03/25)
_L = "Lançamento 03/25"
R(457, "4731086", "SUPORTE BOTIJAO GAS 13KG", foto=[61, 142, 193, 328], info=_L)
R(457, "7000044", "SUPORTE EXTINTOR 08,10,12 KG", foto=[319, 159, 535, 302], info=_L)
R(457, "4731173", "SUPORTE GANCHO REDE", foto=[60, 397, 198, 582], info=_L)
R(457, "4731106", "SUPORTE COROTE AGUA SEM CINTA P/CAVALO", foto=[316, 422, 563, 576], info=_L)
# 458-459 (págs. impressas 457-458): tabelas de ponteiras e tubos (só as linhas com código Falcão)
TIPOS += [(r"^PONTEIRA", "PONTEIRA"), (r"^TUBO", "TUBO"), (r"^LUVA", "LUVA DE AMPLIAÇÃO")]


def TB(p, card, titulo, linhas, foto, extra=""):
    """linhas = [(código, ref Nicolini, descrição, comprimento/medida, diâmetro)] -> 1 produto com itens."""
    for c, ref, d, comp, diam in linhas:
        R(p, c, f"{d} {diam}".strip(), card=card, foto=foto, _titulo=titulo, marca="Nicolini",
          variacoes=ref, info=" | ".join(x for x in (f"Comprimento/medida: {comp}" if comp else "", f"Diâmetro: {diam}", extra) if x))


TB(458, 1, "PONTEIRA RETA CROMADA", [("7002204", "PTM2004", "PONTEIRA RETA CROMADA CURTA", "290mm", '4"'),
                                     ("7004121", "PTM2005", "PONTEIRA RETA CROMADA LONGA", "290mm", '4"1/2'),
                                     ("7002206", "PTM2006", "PONTEIRA RETA CROMADA", "290mm", '5"')], [46, 85, 168, 158])
TB(458, 2, "PONTEIRA ESCAPE CURVA LONGA CROMADA", [("7000450", "PTM2007", "PONTEIRA ESCAPE CURVA LONGA", "50cm", '4"'),
                                                   ("7004512", "PTM2008", "PONTEIRA ESCAPE CURVA LONGA", "50cm", '4"1/2'),
                                                   ("7005500", "PTM2011", "PONTEIRA ESCAPE CURVA", "50cm", '5"')], [36, 198, 218, 277])
TB(458, 3, "PONTEIRA CHANFRADA CROMADA CURVA LONGA",
   [("7003120", "PTM1003", "PONTEIRA CHANFRADA CROMADA CURVA LONGA", "450mm", '3"1/2'),
    ("7004127", "PTM1016", "PONTEIRA CHANFRADA CROMADA CURVA LONGA", "750mm", '4"1/2')], [33, 373, 161, 436])
TB(458, 4, "PONTEIRA ESCAPE CURVA CROMADA (CURVA CURTA)",
   [("7003250", "PTM2009", "PONTEIRA ESCAPE CURVA CROMADA", "250mm", '3"'),
    ("7003122", "PTM2010", "PONTEIRA ESCAPE CURVA CROMADA", "250mm", '3"1/2'),
    ("7000401", "PTM2001", "PONTEIRA ESCAPE CURVA CROMADA", "290mm", '4"'),
    ("7004120", "PTM2002", "PONTEIRA ESCAPE CURVA CROMADA", "290mm", '4"1/2'),
    ("7005290", "PTM2003", "PONTEIRA ESCAPE CURVA CROMADA", "290mm", '5"')], [45, 462, 158, 526])
TB(458, 5, "PONTEIRA RETA AMERICANA CROMADA (CHANFRADA - AMERICANA)",
   [("7004250", "PTM1028", "PONTEIRA RETA AMERICANA CROMADA", "280mm", '4"'),
    ("7004123", "PTM1029", "PONTEIRA RETA AMERICANA CROMADA", "300mm", '4"1/2'),
    ("7004124", "PTM1033", "PONTEIRA RETA AMERICANA CROMADA", "430mm", '4"1/2')], [31, 563, 143, 611])
TB(458, 6, "PONTEIRA CHANFRADA CROMADA CURVA CURTA",
   [("7000212", "PTM1001", "PONTEIRA CHANFRADA CROMADA CURVA CURTA", "300mm", '2"1/2'),
    ("7003350", "PTM1004", "PONTEIRA CHANFRADA CROMADA CURVA CURTA", "350mm", '3"'),
    ("7000312", "PTM1002", "PONTEIRA CHANFRADA CROMADA CURVA CURTA", "350mm", '3" 1/2'),
    ("7004430", "PTM1009", "PONTEIRA CHANFRADA CROMADA CURVA CURTA", "430mm", '4"'),
    ("7000412", "PTM1006", "PONTEIRA CHANFRADA CROMADA CURVA CURTA", "450mm", '4" 1/2'),
    ("7005360", "PTM1027", "PONTEIRA CHANFRADA CROMADA CURVA CURTA", "360mm", '5"'),
    ("7005510", "PTM1014", "PONTEIRA CHANFRADA CROMADA CURVA CURTA", "510mm", '5"')], [24, 658, 133, 779])
NOTAS.append("Págs. 458-459 (tabelas Nicolini): só as linhas com código Falcão viraram itens; a referência PTM/TLM/LVM está em similares; "
             "na pág. 458 o texto das tabelas está impresso como imagem (transcrito) e a ref. do 7005290 aparece sobreposta (PTM2003).")
TB(459, 1, "TUBO LATERAL CROMADO", [("7001250", "TLM1008", "TUBO LATERAL CROMADO", "1250mm", '3"'),
                                    ("7001270", "TLM1003", "TUBO LATERAL CROMADO", "1270mm", '4"'),
                                    ("7001510", "TLM1017", "TUBO LATERAL CROMADO", "1510mm", '4"'),
                                    ("7001160", "TLM1006", "TUBO LATERAL CROMADO", "1160mm", '4"1/2'),
                                    ("7001360", "TLM1037", "TUBO LATERAL CROMADO", "1360mm", '4"1/2'),
                                    ("7001590", "TLM1007", "TUBO LATERAL CROMADO", "1590mm", '4"1/2'),
                                    ("7001970", "TLM1004", "TUBO LATERAL CROMADO", "1970mm", '4"1/2'),
                                    ("7001591", "TLM1050", "TUBO LATERAL CROMADO", "1590mm", '5"')], [39, 125, 187, 334])
TB(459, 2, "TUBOS CURVADO ZINCADO 90° GRAUS", [("7003900", "TLM1018", "TUBOS CURVADO ZINCADO 90° GRAUS", "400mm x 400mm", '3"'),
                                              ("7009031", "TLM1009", "TUBOS CURVADO ZINCADO 90° GRAUS", "400mm x 400mm", '3"1/2'),
                                              ("7009044", "TLM1010", "TUBOS CURVADO ZINCADO 90° GRAUS", "420mm x 420mm", '4"'),
                                              ("7009041", "TLM1011", "TUBOS CURVADO ZINCADO 90° GRAUS", "520mm x 520mm", '4"1/2'),
                                              ("7005552", "ACM1043", "TUBOS CURVADO ZINCADO 90° GRAUS", "520mm x 520mm", '5"')],
   [37, 376, 160, 480])
TB(459, 3, "LUVAS DE AMPLIAÇÃO ZINCADA", [("7003400", "LVM1002", "LUVAS DE AMPLIAÇÃO ZINCADA", "", '3" PARA 4"'),
                                         ("7003312", "LVM1003", "LUVAS DE AMPLIAÇÃO ZINCADA", "", '3" PARA 3"1/2'),
                                         ("7003124", "LVM1004", "LUVAS DE AMPLIAÇÃO ZINCADA", "", '3"1/2 PARA 4"'),
                                         ("7004413", "LVM1005", "LUVAS DE AMPLIAÇÃO ZINCADA", "", '4" PARA 4"1/2'),
                                         ("7004125", "LVM1006", "LUVAS DE AMPLIAÇÃO ZINCADA", "", '4"1/2 PARA 5"')], [45, 541, 147, 627])
TB(459, 4, "TUBO RETO SEM TRATAMENTO", [("7003213", "TLM1013", "TUBO RETO SEM TRATAMENTO", "2000mm", '3"'),
                                       ("7003214", "TLM1014", "TUBO RETO SEM TRATAMENTO", "2000mm", '3"1/2'),
                                       ("7004215", "TLM1015", "TUBO RETO SEM TRATAMENTO", "2000mm", '4"'),
                                       ("7004216", "TLM1016", "TUBO RETO SEM TRATAMENTO", "2000mm", '4"1/2'),
                                       ("7005249", "TLM1049", "TUBO RETO SEM TRATAMENTO", "2000mm", '5"')], [32, 673, 137, 775],
   extra="Sob encomenda")
# 460-461 (págs. impressas 459-460): sobre tampas de cubo (grade 3 x 4; código "@xxxx" no canto = ref. curta)
TIPOS += [(r"^SOBRE TAMPA", "SOBRE TAMPA DE CUBO")]
_G3 = [(27, 208), (210, 390), (392, 570)]
_G4 = [(92, 268), (272, 450), (454, 630), (634, 805)]


def ST(p, k, cod, d, mont="", info=""):
    x, y = _G3[k % 3], _G4[k // 3]
    R(p, cod, d, foto=[x[0], y[0], x[1], y[1]], montadora=mont, info=info, variacoes="@" + cod[-4:])


_MB = "Mercedes-Benz"
for _k, (_c, _d, _m, _i) in enumerate([
        ("7001806", "SOBRE TAMPA CUBO 4 FUROS RANDON CROMADA", "Randon", ""),
        ("7001808", "SOBRE TAMPA CUBO 5 FUROS GUERRA CROMADA", "Guerra", ""),
        ("7001800", "SOBRE TAMPA CUBO TRACAO ACCELO 8 F MB", _MB, ""),
        ("7001803", "SOBRE TAMPA DE CUBO DIANTEIRO MERCEDES BENZ ATEGO", _MB, ""),
        ("7001804", "SOBRE TAMPA DE CUBO DIANTEIRO MERCEDES BENZ - AXOR (TRAÇÃO 1620)", _MB, ""),
        ("7001807", "SOBRE TAMPA DE CUBO DIANTEIRO MERCEDES BENZ 1113 A 1620", _MB, "Código impresso como '700.1807'"),
        ("7001819", "SOBRE TAMPA CUBO MD ACCELLO", _MB, ""),
        ("7001817", "SOBRE TAMPA CUBO TRACAO ATEGO 8 FUROS MB ANTIGO", _MB, "190MM"),
        ("7001822", "SOBRE TAMPA CUBO TRACAO ATEGO 8 FUROS MODELO NOVO", _MB, "220MM"),
        ("7001816", "SOBRE TAMPA CUBO TRUCK 4 FUROS", _MB, ""),
        ("7001820", "SOBRE TAMPA CUBO TRACAO FORD 8 FUROS", "Ford", ""),
        ("7001821", "SOBRE TAMPA CUBO DIANT FORD", "Ford", "")]):
    ST(460, _k, _c, _d, _m, _i)
for _k, (_c, _d, _m, _i) in enumerate([
        ("7001802", "SOBRE TAMPA DE CUBO VOLVO - FH A PARTIR DE 1998", "Volvo", ""),
        ("7001814", "SOBRE TAMPA CUBO TRACAO VOLVO FH/NH", "Volvo", ""),
        ("7001815", "SOBRE TAMPA CUBO TRACAO VOLVO VM", "Volvo", ""),
        ("7001805", "SOBRE TAMPA DE CUBO DIANTEIRO VOLKSWAGEM", "Volkswagen", "Canto do card: @1865"),
        ("7001812", "SOBRE TAMPA CUBO TRACAO VOLKSWAGEM", "Volkswagen", ""),
        ("7001834", "SOBRE TAMPA CUBO DIANT 3/4 VOLKSWAGEM", "Volkswagen", ""),
        ("7001801", "SOBRE TAMPA DE CUBO TRAÇÃO SCANIA", "Scania", ""),
        ("7001813", "SOBRE TAMPA CUBO TRUCK SCANIA", "Scania", ""),
        ("7001835", "SOBRE TAMPA CUBO DIANT SCANIA S5", "Scania", ""),
        ("7001818", "SOBRE TAMPA 10 FUROS CUBO TRACAO MB ACTROS / AXOR", _MB, ""),
        ("7001891", "SOBRE TAMPA CUBO TRACAO MAN 12F", "MAN", ""),
        ("7000118", "SOBRE TAMPA CUBO 4 FUROS GRANDE CROMADA", "", "Canto do card: @7118")]):
    ST(461, _k, _c, _d, _m, _i)
NOTAS.append("Págs. 460-461: o '@xxxx' no canto de cada card (últimos 4 dígitos) está em similares; 7001807 está impresso como "
             "'700.1807'; o card 7001805 traz '@1865' e o 7000118 '@7118' no canto.")
