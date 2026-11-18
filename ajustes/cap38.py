# Capítulo 38 - Buzinas e Mangueiras de Limpeza (págs. 443-447; 447 = divisória)
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
MANUAIS = set(range(443, 448))
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


TIPOS = [(r"^KIT", "KIT BUZINA"), (r"^BUZINA", "BUZINA"), (r"^VALVULA", "VÁLVULA BUZINA"), (r"^SUPORTE", "SUPORTE"),
         (r"^BICO", "BICO"), (r"^CONECTOR", "CONECTOR"), (r"^COTOVELO", "COTOVELO"), (r"^TEE", "TEE"), (r"^INSERT", "INSERT"),
         (r"^TUBO", "TUBO NYLON"), (r"^MANG", "MANGUEIRA LIMPEZA CABINE"), (r"^ABRA", "ABRAÇADEIRA")]
NOTAS = []
_K = dict(marca="Kauai")
# 443 (pág. impressa 442): buzina marítima, válvulas, kits
R(443, "55510304", "BUZINA ELETROPNEUMATICA 740MM SEM VALVULA", foto=[40, 175, 300, 290], **_K)
R(443, "7021011", "SUPORTE BUZINA MARITIMA 340 / 740 / 1000MM", foto=[340, 100, 570, 175], marca="Amil")
R(443, "70010009", "VALVULA BUZINA MARITIMA 12V", foto=[110, 300, 245, 350])
R(443, "70010010", "VALVULA BUZINA MARITIMA 24V", foto=[300, 300, 435, 350])
R(443, "7000039", "BICO SAIDA 5/16 VALVULA SOLENOIDE", info="Para tubo de 5/16 ou 08MM", foto=[440, 300, 570, 355])
_ITK = ("Itens: 02 - conector 12 x 1/4 NPT (8010011); 01 - conector 12 x 1/2 NPT (8001091); 01 - tee 12mm plástico (7711201); "
        "01 - cotovelo plástico 12mm (8011212); 02 - cotovelo 12 x 1/4 NPT (8011214) | Conexões de plástico")
R(443, "7001215", "KIT BUZINA MARITIMA (5 PECAS) RAPIDO", info=_ITK, variacoes="Itens: 7711201 / 8011214 / 8001091 / 8010011 / 8011212",
  foto=[30, 430, 300, 625])
R(443, "@7025", "KIT BUZINA MARITIMA (07 PECAS)", foto=[440, 555, 570, 635], **_K,
  info="Itens: 01 - conector 12 x 1/2 NPT rápido; 02 - conector 12 x 1/2 NPT metal; 01 - tee 12mm plástico; 01 - cotovelo "
       "plástico 12mm; 02 - cotovelo 12 x 1/4 NPT | Código impresso como '@7025'")
for _c, _d, _f in [("7711201", "TEE PLASTICO UNIAO 12MM", [120, 455, 215, 480]),
                   ("8010011", "CONECTOR R MACHO 12 X 1/4 NPT", [170, 560, 270, 600]),
                   ("8011212", "COTOVELO PLASTICO INSTANT. 12M", [50, 575, 160, 612]),
                   ("7711200", "INSERT 12MM", [275, 682, 345, 715])]:
    R(443, _c, _d, foto=_f, info="Item de kit de buzina marítima")
G(443, 90, "KIT BUZINA MARITIMA (5 PECAS) CONEXOES EM LATAO", [("8001089", "CONECTOR MACHO OD 12MM X 1/4 NPT"),
                                                              ("8001091", "CONECTOR MACHO OD 12MM X 1/2 NPT"),
                                                              ("7710112", "TEE UNIAO LATAO 12MM"),
                                                              ("8011212", "COTOVELO PLASTICO INSTANT. 12M"),
                                                              ("7711200", "INSERT 12MM")],
  foto=[30, 640, 465, 805], **_K,
  info="Kit buzina conexões - itens: 02 conector 12 x 1/4 NPT; 02 conector 12 x 1/2 NPT; 01 tee 12mm latão; "
       "02 cotovelo plástico 12mm; 08 insert 12mm")
NOTAS.append("Pág. 443: o kit de 07 peças está impresso com o código '@7025'; 771.1201 (tee plástico) está impresso com ponto; "
             "o card 'kit buzina marítima (5 peças) conexões' não tem código próprio e foi lançado com os itens.")
# 444 (pág. impressa 443): conexões, válvulas e buzinas
for _c, _d, _inf in [("8001089", "CONECTOR MACHO OD 12MM X 1/4 NPT", "Para buzina marítima"), ("7710112", "TEE UNIAO LATAO 12MM", ""),
                     ("8001653", "CONECTOR RAPIDO 12MM X 1/2 NPT", "Para válvula buzina"),
                     ("8010005", "CONECTOR R MACHO 12 X 1/2 NPT", "Para válvula buzina"),
                     ("8011214", "COTOVELO R GIR OD. TB 12X1/4NPT", "12mm tubo | 1/4 NPT"),
                     ("8011204", "COTOVELO R GIR OD. TB 12X1/2NPT", "12mm tubo | 1/2 NPT"),
                     ("8010003", "CONECTOR R MACHO 12 X 1/4 BSP", "Para válvula buzina"),
                     ("8001091", "CONECTOR MACHO OD 12MM X 1/2 NPT", "Para válvula buzina"),
                     ("55510304", "BUZINA ELETROPNEUMATICA 740MM", ""), ("70010009", "VALVULA BUZINA MARITIMA 12V", ""),
                     ("70010010", "VALVULA BUZINA MARITIMA 24V", ""), ("55510048", "BUZINA A AR CARACOL UNIVERSAL TODOS CAMINHÕES/ONIBUS", ""),
                     ("7021011", "SUPORTE BUZINA MARITIMA 340 / 740 / 1000MM", ""), ("55510065", "BUZINA 3 CORNETAS", "")]:
    R(444, _c, _d, info=_inf)
# 445 (pág. impressa 444): kit buzina marítima e buzinas
R(445, "1224", "KIT BUZINA MARITIMA", foto=[35, 130, 570, 490], **_K,
  variacoes="Itens: 10304 (buzina marítima 740mm) / 70010010 (válvula buzina marítima 24V) / 7720705 (tubo nylon 12 x 9 - 10 metros)",
  info="Kit buzina: 02 buzinas marítima 740mm; 01 válvula buzina 24V; 01 cotovelo fêmea x fêmea 12 x 12mm; 02 cotovelo tubo 12mm x "
       "1/4 rosca; 01 tee plástico 12mm; 02 conector metal 12 x 1/2; 01 conector tubo 12 x 1/2 rosca plástico; 10 mts tubo 12 x 9 | "
       "Código impresso como '1224'")
R(445, "7720705", "TUBO NYLON 12 X 9 10 METROS", foto=[175, 380, 300, 460])
R(445, "55510048", "BUZINA A AR CARACOL UNIVERSAL TODOS CAMINHÕES/ONIBUS", foto=[60, 620, 300, 800], **_K)
R(445, "55510065", "BUZINA 3 CORNETAS", foto=[330, 550, 570, 720], **_K)
NOTAS.append("Pág. 445: o kit buzina marítima está impresso com o código '1224' e a buzina dentro dele como '10304' "
             "(provavelmente 55510304).")
# 446 (pág. impressa 445): mangueiras espirais de limpeza da cabine
for _c, _d in [("7720002", "MANG LIMPEZA CABINE VERMELHA C/BICO"), ("7720003", "MANG LIMPEZA CABINE AZUL C/BICO"),
               ("7720004", "MANG LIMPEZA CABINE CINZA C/BICO"), ("7720001", "MANG LIMPEZA CABINE PRETA C/BICO"),
               ("7720006", "MANG LIMPEZA CABINE VERMELHA SIMPL"), ("7720005", "MANG LIMPEZA CABINE AZUL SIMPL"),
               ("7720008", "MANG LIMPEZA CABINE CINZA SIMPL"), ("7720007", "MANG LIMPEZA CABINE PRETA SIMPL"),
               ("7729026", "BICO MANGUEIRA LIMPEZA CABINE"), ("7001005", "ABRACADEIRA PARA MANGUEIRA RODO AR")]:
    R(446, _c, _d)
NOTAS.append("Pág. 446: 7720001 a 7720004 trazem só a cor no card (mangueira espiral com bico); a descrição foi completada como "
             "'MANG LIMPEZA CABINE <cor> C/BICO'.")
# fotos pelas caixas reais das imagens
_FOT = {(443, "55510304"): [33, 157, 291, 257], (443, "7021011"): [317, 92, 550, 181], (443, "70010009"): [106, 266, 224, 374],
        (443, "70010010"): [271, 268, 382, 382], (443, "7000039"): [421, 297, 556, 352], (443, "@7025"): [400, 500, 569, 591],
        (443, "7711201"): [130, 432, 180, 468], (443, "8010011"): [160, 558, 242, 600], (443, "8011212"): [78, 576, 138, 618],
        (443, "7711200"): [270, 684, 350, 716], (445, "1224"): [35, 118, 560, 410], (445, "7720705"): [160, 336, 256, 412],
        (445, "55510048"): [74, 555, 251, 747], (445, "55510065"): [305, 508, 537, 662],
        (444, "55510304"): [391, 512, 565, 578], (444, "70010009"): [89, 460, 205, 580], (444, "70010010"): [275, 460, 391, 581],
        (444, "7021011"): [44, 709, 193, 799], (444, "55510048"): [419, 663, 547, 803], (444, "55510065"): [213, 652, 381, 765],
        (444, "8001089"): [56, 144, 164, 203], (444, "7710112"): [230, 113, 365, 189], (444, "8001653"): [397, 93, 475, 156],
        (444, "8010005"): [393, 182, 458, 236], (444, "8011214"): [425, 291, 531, 338], (444, "8011204"): [412, 369, 537, 445],
        (444, "8010003"): [74, 323, 157, 392], (444, "8001091"): [228, 317, 361, 399]}
for _r in ADD:
    k = (_r["pagina"], _r["codigo"])
    if k in _FOT:
        _r["foto_spec"] = {"rect": _FOT[k]}
    if _r["pagina"] == 443 and _r["card"] == 90:
        _r["foto_spec"] = {"rect": [30, 680, 360, 775]}
