# Capítulo 33 - Elétrica - Terminais, Chicotes e Fios (págs. 402-409)
# Páginas de layout livre (cards mesclados): registros montados à mão a partir da imagem; foto = imagem mais próxima do código.
import re

from tabela_livre import _spans

TIPOS = [(r"^TERMINAL", "TERMINAL"), (r"^CAPA", "CAPA DE TERMINAL"), (r"^FITA", "FITA ISOLANTE"), (r"^SOQ", "SOQUETE"),
         (r"^CHICOTE", "CHICOTE"), (r"^CON\.", "CONECTOR"), (r"^RELE", "RELÉ"), (r"^BOT[ÃA]O", "BOTÃO"), (r"^CHAVE", "CHAVE"),
         (r"^PORTA FUSIVEL", "PORTA FUSÍVEL"), (r"^FUSIVEL|^PORTA (MINI|LAMINA|MAX|VIDRO)", "FUSÍVEL"), (r"^CABO", "CABO"),
         (r"^GARRA", "GARRA DE BATERIA"), (r"^FIO", "FIO"), (r"^SIRENE|^ALARME", "SIRENE"), (r"^MB SOQUETE", "SOQUETE")]
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(402, 410))
_CACHE = {}
_NCOL = {406: 4}  # colunas de cards por página (padrão 3)


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


# 402 (pág. impressa 401): terminais e fitas (descrições impressas como imagem; nº do fabricante no canto do card)
for _c, _d, _f in [
        ("5580105", "TERMINAL ENCAIXE C/TRAVA UNIVERSAL", "7020 C"), ("5581800", "CAPA DE TERMINAL ENCAIXE MACHO 6,3MM", ""),
        ("5581802", "CAPA DE TERMINAL ENCAIXE FEMEA 6,3MM", ""), ("5587009", "TERMINAL OLHAL FURO 3/6 FIO 2,5 MM", "7009"),
        ("5587022", "TERMINAL OLHAL FURO 5/32 F 1,5", "7022 A"), ("5580253", "TERMINAL OLHAL FURO 1/4 F 2,50", "7023 A"),
        ("5587028", "TERMINAL ELETRICO MACHO MENOR", "7028"), ("5580036", "TERMINAL ENCAIXE MOSQUITINHO", "7030"),
        ("5581896", "TERMINAL OLHAL FURO 3/8 GRANDE", "7031"), ("5580120", "TERMINAL ELETRICO MACHO REFORC", "7033"),
        ("5581991", "TERMINAL TUBO MACHO PARA MOTO", "7038"), ("5587821", "TERMINAL OLHAL FURO 8,0 F GROS", "7821"),
        ("5587907", "TERMINAL OLHAL FURO 8,0 F 2,5", "7907")]:
    R(402, _c, _d, variacoes=_f)
R(402, "5100200", "TERMINAL PONTEIRA PEQUENO P/CABO 10 A 25MM²", info="Linha leve | 9,0MM")
R(402, "5100201", "TERMINAL PONTEIRA 13MM AUTOMOV 14MM A 95MM²", info="Médio | 13,0MM / 12,5MM")
R(402, "5101201", "TERMINAL PONTEIRA GRANDE P/CABO 35 A 95MM²", info="15,0MM / 11,5MM")
R(402, "5101202", "TERMINAL PONTEIRA 13MM AUTOMOV 35MM A 50MM²", info="10,0MM / 9,0MM")
R(402, "5101899", "TERMINAL BATERIA SAPINHO P/CABO 10MM A 50MM", info="17,0 MM")
R(402, "5100104", "TERMINAL BATERIA 16MM SAPAO")
R(402, "5591925", "FITA ISOLANTE TECIDO 25MTS")
G(402, 23, "FITA ISOLANTE", [("5590005", "FITA ISOLANTE 05MTS"), ("5590010", "FITA ISOLANTE 10MTS"),
                             ("5590020", "FITA ISOLANTE 20MTS")])
R(402, "5592020", "FITA ISOLANTE TECIDO 20MTS S/COLA")
NOTAS.append("Pág. 402: o número no canto de cada terminal (7020 C, 7009, 7022 A...) é a referência do fabricante e está em similares.")
# 403 (pág. impressa 402): soquetes ETE (Observação: adaptação - base oval pinos), relés e chaves
_OBS = "Observação: adaptação - base oval pinos"
for _c, _d, _ete, _lamp in [
        ("5587214", "SOQ TODOS LISO 2 POLO PARALELO C/SUP OVAL", "ETE7214", "Lâmpada 1034 | 2 polos"),
        ("5587215", "SOQ TODOS LISO 2 POLO TRANSVERSAIS C/SUP OVAL", "ETE7215", "Lâmpada 1034 | 2 polos"),
        ("5587211", 'SOQ TODOS LISO 2 POLO PARALELO C/SUP "L"', "ETE7211", "Lâmpada 1034 | 2 polos"),
        ("5587212", 'SOQ TODOS LISO 2 POLO TRANSVERSAIS C/SUP "L"', "ETE7212", "Lâmpada 1034 | 2 polos"),
        ("5587213", "SOQ TODOS LISO 1 POLO PARALELO C/SUP OVAL", "ETE7213", "Lâmpada 67/1141"),
        ("5587210", 'SOQ TODOS LISO 1 POLO PARALELO C/SUP "L"', "ETE7210", "Lâmpada 67/1141"),
        ("5587207", "SOQ TODOS LISO 1 POLO PARALELO C/SUP RETO", "ETE7207", "Lâmpada 67/1141"),
        ("5587208", "SOQ TODOS LISO 2 POLO PARALELO C/SUP RETO", "ETE7208", "Lâmpada 1034 | 2 polos"),
        ("5587209", "SOQ TODOS LISO 2 POLO TRANSVERSAIS C/SUP RETO", "ETE7209", "Lâmpada 1034 | 2 polos"),
        ("5587202", "SOQ TODOS LISO 2 POLO PARALELO S/SUPORTE", "ETE7202", "Lâmpada 1034 | 2 polos"),
        ("5587203", "SOQ TODOS LISO 2 POLO TRANSVERSAIS S/SUP", "ETE7203", "Lâmpada 1034 | 2 polos"),
        ("5587201", "SOQ TODOS LISO 1 POLO PARALELO S/SUPORTE", "ETE7201", "Lâmpada 67/1141")]:
    R(403, _c, _d, variacoes=_ete, info=_OBS + " | " + _lamp)
R(403, "5587061", "SOQ TODOS LISO 2 POLO TRANSVERSAIS S/SUP", variacoes="ETE7061",
  cod_ref="MB: 345.544.01.93 / Volvo: 344130 / VW: N0141563",
  aplicacao="Mercedes-Benz: trator / Scania: caminhão / Volkswagen: caminhão / Volvo: ônibus até 90",
  info="Soquete de painel | Isolado para painel lâmina | Lâmpada 69 - normal", montadora="Mercedes-Benz, Scania, Volkswagen, Volvo")
R(403, "5587061", "MB SOQUETE LAMPADA PAINEL ISOL", montadora="Mercedes-Benz", foto=[33, 484, 133, 532])
R(403, "5587090", "CHICOTE FAROL UNIVERSAL C/FIO 1.5MM LAMP H4", variacoes="ETE7090 B",
  info="Chicotes soquetes | 3 vias | Chicote soquete farol lâmpada H4 | Fio 1.5 MM")
R(403, "5590226", "RELE AUX REVERSOR 24V 40A 5 PINOS S/SUPORT", variacoes="Similares: 3112AP / A3845427119 / DNI0226", marca="DNI")
R(403, "5598810", "RELE PISCA LIMPADOR PARA-BRISA MB", aplicacao="Relé pisca 24V MB caminhões Axor e Atego 03/...",
  variacoes="Similares: DNI8810 / 3128AP / A0035445032 / U039", info="Tipo de produto: relé | Quantidade de pólos principais: 18",
  marca="DNI", montadora="Mercedes-Benz")
R(403, "5592299", "BOTÃO PARTIDA CHAVE COMUTADORA", info="Tensão: 12/24V",
  aplicacao="Agrale – tratores / empilhadeiras / caminhões; Case – tratores / empilhadeiras; Fiat Allis – tratores; "
            "Ford – caminhonetes F350 / F550 / F600 / F700; Hyster – empilhadeiras; Maxion – tratores / empilhadeiras; Scania – caminhões")
R(403, "5592085", "CHAVE COMUTADORA GERAL 120W 2 POSIÇÕES",
  info="Potência máx.: 120W | 2 posições (1 puxada): ON / OFF | 2 terminais com parafusos",
  aplicacao="Uso geral; Scania e Ford: caminhões; J.I. Case e Caterpillar: tratores; Hyster: empilhadeiras")
R(403, "55904244", "RELE COMANDO PISCA MB UNIVERSAL 4 PINOS S/SUP", info="Potência máx.: 500W | Voltagem: 24V",
  aplicacao="Caminhões e ônibus; Busscar; Caio; Ciferal; Marcopolo; Mercedes-Benz; Nielson; Randon; Volare; Volvo",
  montadora="Mercedes-Benz, Volvo")
R(403, "5590212", "RELE AUXILIAR MB UNIVERSAL 4 PINOS C/SUP",
  info="Voltagem: 24V | Relé auxiliar universal, 4 terminais, com suporte, corrente 40A",
  aplicacao="Universal, uso geral; Scania: caminhões e ônibus – 76/...; Marcopolo: caminhões e ônibus", montadora="Mercedes-Benz")
NOTAS.append("Pág. 403: o código 5587061 aparece em dois cards (soquete 2 polos transversais com dados de soquete de painel, e "
             "MB soquete lâmpada painel isol); o ETE de cada soquete está em similares; 55904244 está impresso com 8 dígitos.")
# 404 (pág. impressa 403): fusíveis (um card por família) e cabos
G(404, 1, "FUSIVEL MINI G732", [(c, f"PORTA MINI {a}AMP") for c, a in (("7320005", "05"), ("7320010", "10"), ("7320015", "15"),
                                                                     ("7320020", "20"), ("7320025", "25"), ("7320030", "30"))],
  foto=[88, 117, 139, 175])
G(404, 2, "FUSIVEL LAMINA G731", [("7310005", "PORTA LAMINA 05AMP BEGE"), ("7310010", "PORTA LAMINA 10AMP VERM"),
                                  ("7310015", "PORTA LAMINA 15AMP AZUL"), ("7310020", "PORTA LAMINA 20AMP AMAR"),
                                  ("7310025", "PORTA LAMINA 25AMP BRAN"), ("7310030", "PORTA LAMINA 30AMP VERD")],
  foto=[268, 121, 333, 164])
G(404, 3, "FUSIVEL MAX G731", [("7313000", "PORTA MAX 30AMP VERD"), ("7314000", "PORTA MAX 40AMP LARAN"),
                               ("7315000", "PORTA MAX 50AMP VERM"), ("7316000", "PORTA MAX 60AMP AZUL"),
                               ("7317000", "PORTA MAX 70AMP BEGE"), ("7318000", "PORTA MAX 80AMP TRANS"),
                               ("7310100", "PORTA MAX 100AMP ROXO")], foto=[445, 125, 517, 168])
G(404, 4, "FUSIVEL DE VIDRO", [("7320473", "PORTA VIDRO 10AMP"), ("7320457", "PORTA VIDRO 15AMP"), ("7320472", "PORTA VIDRO 20AMP"),
                               ("7320474", "PORTA VIDRO 25AMP")], foto=[49, 294, 175, 373])
G(404, 5, "FUSIVEL PORCELANA", [("7301500", "FUSIVEL PORCELANA 15AMP MARON"), ("7303000", "FUSIVEL PORCELANA 30AMP PRETO")],
  foto=[236, 290, 358, 384])
G(404, 6, "PORTA FUSIVEL", [("5591445", "PORTA FUSIVEL LAMINA"), ("5591669", "PORTA FUSIVEL MAX REFORC")], foto=[409, 287, 546, 387])
R(404, "6013500", "CABO DE TRANSMISSÃO DE CARGA TIPO CHUPETA 300A", marca="Riosul", foto=[28, 494, 290, 618])
R(404, "5589202", "CHICOTE SENSOR PRESSAO OLEO", cod_ref="389202", aplicacao="SC 94/114/124/164/F112/113", montadora="Scania", foto=[410, 476, 555, 568])
R(404, "7000600", "CABO CHUPETA 600A 5MTS REFORCADO",
  info="Especificações: 600 amperes | 5 metros de comprimento | Bitola de 10mm | Revestimento cobreado | Garras tipo jacaré", foto=[114, 679, 364, 786])
R(404, "5590053", "GARRA BATERIA 600 AMP (2 PECAS)", info="Lançamento", foto=[378, 632, 558, 734])
# 405 (pág. impressa 404): conectores / chicotes de reparo ETE
for _c, _d, _ete, _inf in [
        ("5586731", "CON. INJECAO ELETRONICA ETE7731", "ETE7731",
         "KitChic Bico Injetor-Sensor Temp-Bobina Ign-Farol Milha-Lanterna Diant-Fiat-Uno Palio Tempra-GM Cors"),
        ("5587743", "CON. INJECAO ELETRONICA ETE7743", "ETE7743", "Chicote Injetor Sensor Temperatura-Tipo Bosch, fêmea 2.8 mm"),
        ("5587741", "CON. SENSOR BORBOLETA ETE7741", "ETE7741",
         "Chicote Rep Sensor Posição Borboleta TPS 14059/062 - GM EFI-MPFI - Pressostato - Fiat-GM-VW-Ford - 3V"),
        ("9997745", "CON. INJECAO ELETRONICA 2 VIAS ETE 7745", "ETE 7745",
         "Chicote Reparo Sensor De Temp. - GM Monza-Kadett-Ipanema-Omega-Blazer-Corsa - 2 Vias - Fêmea 1.6mm"),
        ("5517599", "CON. CHI ALTERNATOR MB 1938 4", "ETE7599",
         "Chicote Reparo Alternador Mercedes Benz 1938 - Caminhões Constellation - 80 Ampères - 24 Volts"),
        ("5587656", "CON. REPARO SENSOR ETE7656", "ETE7656", "Chicote Reparo Sensor Luz de Ré Ônibus - Caminhão - 2 Vias - Macho - 2,8mm"),
        ("5585709", "CON. SENSOR BORBOLETA 5709", "ETE5709",
         "Chicote Bico Injetor Caminhão VW-Ford - Regulador de Voltagem Alternador GM-Agile-Montana - 2 Vias"),
        ("5587886", "CON. SENSOR TEMPERATURA", "ETE7886",
         "Chicote Rep. Sensor Temp-Lanterna Traseira-Farol Milha-Trava Elétrica-GM-Ford-VW - 2 Vias F 1.6mm"),
        ("5589886", "CON. SENSOR TEMPERATURA", "ETE9886", "Chicote Conector Alto Falante - 2 Vias Macho 1.6 mm"),
        ("5587735", "CON. SENSOR BORBOLETA 7735", "ETE7735",
         "Chicote Reparo Sensor Posição Borboleta Diagnóstico Magneti Marelli - Fiat Uno-Palio-Tempra - 3 Vias"),
        ("5587885", "CON. SENSOR TEMPERATURA VW - GOL MI - FOR", "ETE7885",
         "Chicote Reparo Sensor Temperatura - VW - Gol MI - Ford - 1 Via - Fêmea - 1.6mm"),
        ("5100112", "CHICOTE 5 VIAS LANTERNA GUERRA ETE7760", "ETE7760",
         "Chicote Para Reparo Diversos - Chicote Caminhões Lanterna Guerra-Rondon 5 Vias - Fêmea - 1,6mm")]:
    R(405, _c, _d, variacoes=_ete, info=_inf)
for r in ADD:
    if r["pagina"] == 405 and r["codigo"] == "5517599":
        r["montadora"] = "Mercedes-Benz"
    if r["pagina"] == 405 and r["codigo"] == "5100112":
        r["montadora"] = "Guerra"
R(405, "5518425", "CHICOTE 7 VIAS LANTERNA 7665 SC/MB",
  cod_ref="Mercedes-Benz: 15406270 / 1791171 / 25402381 | Volvo: 3963412 / 3981460 / 3981461",
  info="Chicote Rep Lanterna Mercedes Benz-Volvo-Scania - Conexões Lant 1025-1047-1048-1053-1054-1245-1246",
  montadora="Mercedes-Benz, Volvo, Scania")
R(405, "5587799", "CHICOTE 2 VIAS P/LANT LED TAPA SOL SC 7799", montadora="Volkswagen, Scania",
  aplicacao="Audi, Scania, Amarok, tapa sol, Volkswagen, Amarok, Gol G III - plug alternador, Gol G III / Golf / Jetta - "
            "plug alternador, Saveiro, Volvo e FH13 - pisca")
R(405, "5585718", "CON. SENSOR FASE TODOS ETE5718", variacoes="ETE5718 / Kit ETE 4718", info="3 vias | Reparo sensor de fase / "
  "bobina YR4 / luz do freio / sensor flauta / óleo",
  aplicacao="Agrale / Fiat / Ford: caminhão; GM: Meriva / Iveco; MB: Sprinter; New Holland; VW: caminhão; Volvo: L90 F")
R(405, "5587881", "CON.LANT TRAS MB 1620 ETE7881", variacoes="ETE7881 / Kit ETE 7881", montadora="Mercedes-Benz",
  info="5 vias | Reparo medidor fluxo ar-condicionado / medidor massa de ar / conexão coletor admissão integrado / lanterna "
       "traseira / farol | Contrapeça ETE 9881 | Aplica-se terminal ETE 7802",
  aplicacao="Fiat: Uno 1.6 MPI / Tempra / Tipo 93 até 95; Ford: Escort XR3 / Ka; GM: Vectra / Omega / Monza; "
            "VW: Gol GTI / Pointer após 95; Volvo: FM")
R(405, "5587218", "SOQUETE GARRA UNIV.2 POLOS", variacoes="ETE 7218",
  info="Pinos desencontrados | Lâmpada 1034 | Tipo de veículo: carro / caminhonete")
R(405, "5597902", "SOQUETE P/LAMPADA PINGAO VW MB ETE7902", variacoes="ETE7902", cod_ref="547953055 / 7078472",
  info="Chicote utilizado: ETE7743", montadora="Volkswagen, Mercedes-Benz",
  aplicacao="Fiat: Palio, Marea, Bravo; Ford: Escort, Verona; MB / Mercedes-Benz: 1620; VW / Volkswagen: Logus, Pointer "
            "(após 1993), Gol (após 1995), Saveiro (após 1997), Constellation")
R(405, "5587493", "SOQUETE P/LAMPADA PINGO DAGUA ETE7493", variacoes="ETE7493", aplicacao="Universal",
  info="Soquete chicote soquete globo óptico base de vidro para adaptação lâmpada 5W")
NOTAS.append("Pág. 405: o ETE de cada conector está em similares e a descrição técnica (texto miúdo do card) em informações.")
# 406 (pág. impressa 405): chicotes de reparo (código do fabricante "CÓD.: CX..."; todos bivolt)
for _c, _d, _cx in [
        ("5518541", "CHICOTE FUSIVEL COM TAMPA FIXAÇÃO VEDADO - 8541", "CX02.8541"), ("5517179", "CHICOTE REPARO 2 VIAS - 7179", "CX02.7179"),
        ("5518427", "CHICOTE 7 VIAS LANTERNA 7001156 AMARELO LE", "ASX8427"), ("5518426", "CHICOTE 7 VIAS LANTERNA 7001156 VERDE LD", "CX02.8541"),
        ("5517664", "CHICOTE REPARO 4 VIAS 7664", "CX04.7664"), ("5517734", "CHICOTE REPARO 4 VIAS 7734", "CX04.7734"),
        ("5517599", "CHICOTE REPARO 5 VIAS 7599", "CX05.7599"), ("5517595", "CHICOTE REPARO 5 VIAS 7595", "CX05.7595"),
        ("5517090", "CHICOTE REPARO 3 VIAS H4 7090", "CX03.7090"), ("5519760", "CHICOTE 5 VIAS 9760", "CX05.7760"),
        ("5586731", "CON. INJECAO ELETRONICA ETE 7731", "CX02.771"), ("5517198", "PORTA FUSIVEL 1,50MM 7198", "CX02.7198"),
        ("5517191", "PORTA FUSIVEL 2,50MM", "CX02.7198A"), ("5517780", "CHICOTE REPARO FAROL 10 VIAS SELADO 7780", "CX10.7780"),
        ("5587743", "CON. INJECAO ELETRONICA ETE7743", "CX02.7743"), ("5515114", "CHICOTE 2 VIAS BOMBA DE CUMBUSTIVEL 5114", "CX02.5114"),
        ("5517493", "CHICOTE SOQUETE T10 7493", "CX02.7493"), ("5517140", "CHICOTE SOQUETE FAROL LAMPADA H7 7140", "CX03.7140"),
        ("5517743", "CHICOTE SENSOR DE TEMP 2 VIAS 7743", "CX02.7743")]:
    R(406, _c, _d, variacoes="Cód. " + _cx, info="Bivolt", acima=True)
R(406, "5587687", "CON. REPARO BIONETA ETE7687 MACHO", variacoes="ETE7687", montadora="Mercedes-Benz, Volvo, Scania",
  aplicacao="Mercedes Benz - Accelo / Actros / Atego / Axor; Volvo - FH460 / FH500 / FH540 (1958 à 2015); SC - P310",
  info="Logos no card: Scania, Volvo, Mercedes-Benz, Volkswagen, Iveco")
NOTAS.append("Pág. 406: 5518426 traz o mesmo 'CÓD.: CX02.8541' do 5518541; 5517599, 5586731 e 5587743 também estão na pág. 405; "
             "5587743 e 5517743 trazem o mesmo CÓD. CX02.7743; a aplicação do 5587687 diz 'Volvo FH460/FH500/FH540 (1958 à 2015)'.")
# 407 (pág. impressa 406): sirenes de marcha-ré DNI e ASX
_ESP = {
    "5594001": ("DNI4001", "SIRENE DE MARCHA-RÉ 12V", "Tensão de funcionamento: 12Vdc | Corrente: 0,1A | Acabamento em ABS na cor preta | "
                "Base móvel | Som intermitente | Piezoelétrica | Pressão sonora: 100dB aprox. | Dimensões aprox.: 5,8 x 4,3 x 3,8cm"),
    "5594002": ("DNI4002", "SIRENE DE MARCHA-RÉ 24V", "Tensão de funcionamento: 24Vdc | Corrente: 0,1A | Acabamento em ABS na cor preta | "
                "Base móvel | Som intermitente | Piezoelétrica | Pressão sonora: 100dB aprox. | Dimensões aprox.: 5,8 x 4,3 x 3,8cm"),
    "5594029": ("DNI4029", "SIRENE DE MARCHA-RÉ RESISTENTE À ÁGUA BIVOLT 12/24V",
                "Tensão de funcionamento: 12/24Vdc - bivolt | Corrente: 0,3A | Pressão sonora aprox.: 110dB a 1m | Som intermitente | "
                "Piezoelétrica | Com sistema de redução de som para uso noturno, de 110dB para 80dB aprox. | Resistente à água | "
                "Acabamento em ABS | Cor: preto | Base fixa | Fixação por parafusos (não inclusos) | Dimensões aprox.: 5,5 x 7,5 x 7cm"),
    "5594027": ("DNI4127", "SIRENE DE MARCHA-RÉ BIVOLT 12/24V",
                "Tensão de funcionamento: 12/24Vdc - bivolt | Corrente: 60mA | Pressão sonora aprox.: 110dB a 1m | Com sistema de redução "
                "de som para uso noturno, de 110dB para 80dB aprox. | Som intermitente | Piezoelétrica | Cor: preta | Acabamento em ABS | "
                "Base fixa | Fixação por parafusos (não inclusos) | Dimensões aprox.: 5,5 x 7,1 x 4,8cm"),
    "5594054": ("DNI4054", "SIRENE PIEZOELÉTRICA 6 SONS 24V",
                "Tensão de funcionamento: 24Vdc | Corrente: 0,3A | Pressão sonora aproximada: 115dB | 6 sons | Piezoelétrica | "
                "Acabamento em ABS | Cor: preto | Base fixa | Fixação por parafusos (não inclusos) | Dimensões aprox.: 7,8 x 7,8 x 8cm"),
    "5594050": ("DNI4050", "SIRENE PIEZOELÉTRICA 6 SONS 12V",
                "Tensão de funcionamento: 12Vdc | Corrente: 0,3A | Pressão sonora aproximada: 115dB | 6 sons | Piezoelétrica | "
                "Acabamento em ABS | Cor: preta | Base fixa | Fixação por parafusos (não inclusos) | Dimensões aprox.: 7,8 x 7,8 x 8cm")}
for _c, (_ref, _d, _inf) in _ESP.items():
    R(407, _c, _d, variacoes=_ref, info=_inf, marca="DNI", aplicacao="Linha automotiva para sistemas de marcha-ré",
      foto={"5594001": [60, 110, 131, 164], "5594002": [29, 170, 145, 258], "5594029": [28, 264, 148, 376],
            "5594027": [34, 399, 147, 508], "5594054": [340, 395, 459, 508], "5594050": [36, 514, 145, 618]}[_c])
R(407, "5515105", "SIRENE - 1 TOM", variacoes="ASX5105", info="Bivolt | Alt: 4cm | Comp: 4,5cm | Prof: 6,2cm", marca="ASX", foto=[39, 636, 222, 789])
R(407, "5515106", "SIRENE RE ASX", info="Bivolt | 06 tons | Com LED", marca="ASX")
NOTAS.append("Pág. 407: o código DNI de cada sirene (DNI4001...) está em similares; a sirene DNI4127 tem código 5594027.")
# 408 (pág. impressa 407): fios (rolos de 100 m), conectores, interruptores e espaguetes
for _c, _d in [("5591000", "FIO 1,0 - 100MTS PRETO"), ("5591500", "FIO 1,5 - 100MTS PRETO"), ("5591400", "FIO 2,5 - 100MTS PRETO"),
               ("5594000", "FIO 4,0 - 100MTS PRETO"), ("5590100", "FIO 1,0 - 100MTS VERMELHO"), ("5591300", "FIO 1,5 - 100MTS VERMELHO"),
               ("5592500", "FIO 2,5 - 100MTS VERMELHO"), ("5591010", "FIO 1,0 - 100MTS VERDE"), ("5590150", "FIO 4,0 - 100MTS VERDE"),
               ("5591200", "FIO 1,0 - 100MTS AMARELO"), ("5991100", "FIO 1,0 - 100MTS AZUL"), ("5994100", "FIO 4,0 - 100MTS AZUL"),
               ("55921100", "FIO BICOLOR 2 X 1,0 - 100MTS"), ("55921510", "FIO BICOLOR 2 X 1.5 - 100MTS"),
               ("5593551", "CONECTOR 02 VIAS C/TERMINAIS"), ("5593511", "CONECTOR 04 VIAS C/TERMINAIS"),
               ("5590197", "ESPAGUETE CORRUGADO 13,0 MM P/FIO - 020MTS PT"), ("5590192", "ESPAGUETE 4,0MM P/FIO - 100MTS PRETO"),
               ("5518303", "CHAVE TIC TAC 3 ESTAGIOS BIVOLT A")]:
    R(408, _c, _d)
R(408, "5592185", "INTERRUPTOR TIC-TAC BAU PUX. DNI", marca="DNI")
R(408, "5591989", "INTERRUPTOR TIC-TAC BAU.", info="15 A - 12 V | 7.5 A - 24 V")
NOTAS.append("Pág. 408: 55921100 e 55921510 (fios bicolor) estão impressos com 8 dígitos; o fio 4,0 azul (5994100) aparece com foto "
             "de rolo branco.")
# 409 (pág. impressa 408): cabos PP (foto = card inteiro: cabo + rolo) e chicotes injetados; demais cards da página vazios
_COLS = [(27, 200), (210, 385), (395, 568)]
_ROWS = [(90, 180), (194, 285), (296, 386), (399, 492)]
for _k, (_c, _d) in enumerate([
        ("5590210", "CABO PP 2 X 1,0MM 050MTS PRETO"), ("5590753", "CABO PP 2 X 1,5MM - 050MTS PRETO"),
        ("5592250", "CABO PP 2 X 2,5MM 050MTS PRETO"), ("5590310", "CABO PP 3 X 1,0MM 050MTS PRETO"),
        ("5590759", "CABO PP 4 X 1,5MM - 050MTS PRETO"), ("5590510", "CABO PP 5 X 1,0MM 050MTS PRETO"),
        ("5590410", "CABO PP 4 X 1,0MM 050MTS PRETO"), ("5597100", "CABO PP 7 X 1,0MM 025MTS PRETO"),
        ("5597501", "CABO PP 7 X 1,5MM - 050MTS PRETO"), ("5590610", "CABO PP 6 X 1,0MM 050MTS PRETO"),
        ("5593525", "CHICOTE 2 VIAS INJETADO 4,00 MM"), ("5593524", "CHICOTE 4 VIAS INJETADO 4,00 MM")]):
    _x, _y = _COLS[_k % 3], _ROWS[_k // 3]
    R(409, _c, _d, foto=[_x[0], _y[0], _x[1], _y[1]])
for _r in ADD:
    if _r["pagina"] == 402 and _r["codigo"] == "5580105":
        _r["foto_spec"] = {"rect": [47, 140, 146, 203]}
