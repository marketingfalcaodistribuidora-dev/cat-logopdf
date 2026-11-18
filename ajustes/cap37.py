# Capítulo 37 - Antifurto, Palhetas e Limpador (págs. 437-442)
# 437: kits antifurto (lista de peças no card). 438: lista das palhetas DNA (+ destaque 70028704).
# 439-442: uma palheta por faixa com especificações e aplicação por montadora (mesmo código da lista -> mesclado).
TIPOS = [(r"^KIT ANTI", "KIT ANTIFURTO"), (r"^PALHETA", "PALHETA LIMPADOR"), (r"^BOMBINHA", "BOMBINHA LIMPADOR")]
AJ = {}
ADD = []
NOTAS = ["Págs. 438-442: as palhetas aparecem na lista da pág. 438 e com especificações/aplicação nas págs. 439-442; cada código "
         "foi lançado uma vez com as informações das duas páginas."]
MANUAIS = set(range(437, 443))


def R(p, cod, desc, foto, **kw):
    r = dict(pagina=p, card=len(ADD) + 1, codigo=cod, descricao=desc, cod_ref="", variacoes="", aplicacao="", info="", marca="",
             montadora="", _nao_agrupar=True, foto_spec={"rect": foto})
    r.update(kw)
    ADD.append(r)


# 437 (pág. impressa 436): kits antifurto
R(437, "6020150", "KIT ANTI FURTO BATERIA M8 VOLVO VOLKS MERCEDES IVECO", [40, 100, 290, 280],
  montadora="Volvo, Volkswagen, Mercedes-Benz, Iveco")
R(437, "6020149", "KIT ANTI FURTO BATERIA M10 SCANIA - VOLVO - DAF", [305, 100, 565, 280], montadora="Scania, Volvo, DAF")
R(437, "6020385", "KIT ANTI FURTO VOLVO APOS2015 C/20 ITENS", [30, 580, 295, 700], montadora="Volvo",
  info="Itens: 02 peças 296 - chave antifurto Volvo tampa câmbio, mod, motor, PWM, módulo: Arla, chassis, ABS, APU; "
       "02 peças 297 - paraf antifurto PWM / ECA Volvo; 02 peças 298 - paraf antifurto módulo tampa do câmbio Volvo; "
       "02 peças 299 - paraf antifurto módulo do motor Volvo; 02 peças 370 - paraf antifurto módulo do farol Volvo após ano 2015; "
       "01 peça 300 - paraf antifurto válvula APU Volvo; 01 peça 301 - paraf antifurto bomba dosadora Arla 30mm (curto) Volvo; "
       "01 peça 302 - paraf antifurto bomba dosadora Arla 40mm (longo) Volvo; 01 peça 303 - porca antifurto módulo EBS/ABS (45mm) Volvo; "
       "02 peças 304 - porca antifurto suporte alumínio (3 módulos - ABS - Arla) Volvo; 01 peça 305 - porca antifurto módulo EBS/ABS "
       "(30mm) Volvo; 01 peça 306 - porca antifurto módulo emissões gases Volvo Arla 30mm; 02 peças 307 - porca antifurto módulo "
       "controle dos periféricos chassis, bloqueio diferencial, luze roda... Volvo 30mm")
R(437, "6020392", "KIT ANTI FURTO SCANIA NTG C/19 PECAS.", [300, 580, 565, 700], montadora="Scania",
  info="Itens: 02 peças 277 - chave antifurto geral, módulo servo ECA, dosadora; 02 peças 278 - paraf antifurto servo ECA - Scania "
       "após 2022 aut.; 02 peças 279 - paraf antifurto módulo câmbio após 2015; 02 peças 280 - paraf antifurto módulo motor Scania "
       "motor XPI - NTG; 01 peça 281 - paraf antifurto equalizador (módulo) Scania 2020 NTG; 01 peça 282 - paraf antifurto bomba "
       "dosadora Arla Scania após 2015; 01 peça 283 - paraf antifurto bomba dosadora Arla Scania após 2015; 01 peça 285 - porca "
       "antifurto EBS-ASS curta - 20mm com tucho Scania 2020 NTG; 02 peças 286 - porca antifurto ECU ECC controle emissões (Arla); "
       "02 peças 287 - porca antifurto ECU CMS Scania 2020 NTG2; 02 peças 288 - paraf antifurto farol Scania 2020 NTG lado LD/ESQ; "
       "01 peça - porca antifurto EBS-ABS longa 35mm - com tucho Scania 2020 NTG")
NOTAS.append("Pág. 437: kit 6020385 diz 'C/20 ITENS' e kit 6020392 'C/19 PEÇAS'; a lista de peças está em informações.")
# 438 (pág. impressa 437): lista DNA
_LISTA = [("70020341", 'PALHETA LIMPADOR 20" CONEX BIONETA'), ("70022406", 'PALHETA LIMPADOR 22" DAF'),
          ("70024900", 'PALHETA LIMPADOR 24" CONEX GANCHO ESTREITO'), ("70024901", 'PALHETA LIMPADOR 24" CONEXAO GANCHO LARGO'),
          ("70024908", 'PALHETA LIMPADOR 24" CONEXAO PARAFUSO'), ("70024406", 'PALHETA LIMPADOR 24" DAF'),
          ("70024606", 'PALHETA LIMPADOR 24" GANCHO ESTREITO C/ESGUI'), ("70024012", 'PALHETA LIMPADOR 24" VW DELIVERY NOVO'),
          ("70026901", 'PALHETA LIMPADOR 26" CONEXAO CANCHO LARGO'), ("70026900", 'PALHETA LIMPADOR 26" CONEXAO GANCHO ESTREITO'),
          ("70026908", 'PALHETA LIMPADOR 26" FORD CARGO 2000 A 2011'), ("70027901", 'PALHETA LIMPADOR 27" CONEXAO GANCHO LARGO'),
          ("70028406", 'PALHETA LIMPADOR 28" MB ACTROS 2016 A 2020'), ("70028704", 'PALHETA LIMPADOR 28" MB ACTROS 2021 EM DIANTE'),
          ("70028705", 'PALHETA LIMPADOR 28" SCANIA NTG'), ("70028706", 'PALHETA LIMPADOR 28" VOLVO SCANIA S 5')]
for _c, _d in _LISTA:
    R(438, _c, _d, [80, 140, 570, 300], marca="DNA")
NOTAS.append("Pág. 438: 70028704 (palheta 28\" MB Actros 2021 em diante) aparece em destaque e na lista; não tem página de detalhe.")
# 439-442: detalhes (especificações + aplicação)
_DET = {
    "70020341": (439, [25, 95, 570, 252], "20 polegadas | 500mm | Conexão baioneta ao original",
                 "Agrale: 1600D de 1987 a 1991, 1800D de 1987 a 1991, 4500D de 1992 a 1998, 5000D de 1992 a 1998, 510-Deutz de 1992 a 1998; "
                 "Puma: 4T de 1979 a 1984, 6T de 1979 a 1984; Volkswagen: caminhões 6T de 1981 a 1992, caminhões 7T de 1981 a 1992; "
                 "Mercedes Benz: 608 de 1975 a 1988, 708 de 1975 a 1988, série L de 1975 a 1988"),
    "70022406": (439, [25, 256, 570, 432], "22 polegadas | 550mm | Conexão gancho largo | Conector modelo similar ao original",
                 "DAF: F95 de 1991 a 1997, XF 2013 em diante, XF105 2006 em diante, XF95 1997 em diante"),
    "70024012": (439, [25, 437, 570, 598], "24 polegadas | 600mm | Conexão específica 012",
                 "Volkswagen: Amarok 2013 em diante, Delivery 2018 em diante"),
    "70024406": (439, [25, 603, 570, 805], "24 polegadas | 600mm | Conexão gancho largo | Conector modelo similar ao original",
                 "DAF: CF 2013 em diante, CF65 1998 em diante, CF75 1998 em diante, F65 de 1993 a 1998, F85 de 1992 a 1998"),
    "70024606": (440, [25, 91, 570, 262], "24 polegadas | 600mm | Conexão gancho 8,5mm | Esguicho",
                 "Iveco: Daily de 2007 a 2017; Renault: Master de 2002 a 2012; Volvo: VM17, VM23, VM260, VM270, VM310 de 2003 a 2017"),
    "70024900": (440, [25, 267, 570, 447], "24 polegadas | 600mm | Conexão gancho 8,5mm",
                 "Volkswagen: Constellation de 2000 a 2017, Worker 2006 em diante"),
    "70024901": (440, [25, 452, 570, 634], "",
                 "Volkswagen: Delivery de 2000 a 2017, Worker de 2000 a 2017; Volvo: FH de 2007 a 2011; Agrale: 13000 de 2007 a 2012, "
                 "8500 CD de 2003 a 2012, 8500 CE de 2003 a 2012, 9200 de 2003 a 2012; Mercedes Benz: Accelo 715C 2003 em diante, "
                 "Accelo 915C 2003 em diante, Atron 2012 em diante, séries L, LA, LAK, LB, LK, LS 2001 em diante"),
    "70024908": (440, [25, 639, 570, 805], "24 polegadas | 600mm | Conexão parafuso P01",
                 "Agrale: 6000 de 1992 a 2012, 7000DX de 1992 a 2005, 7500TDX de 1992 a 2005, 8500 TD de 1997 a 2003, MA 7.5T de 1992 a "
                 "2005; Volkswagen: caminhões de 1992 a 1999; Scania: série T/R de 1891 a 1990; Mercedes Benz: 1114, 709, 710, 912, 914 "
                 "1988 em diante, 712C e 914C 1998 em diante, cara chata 1988 em diante, série L de 1988 a 2000"),
    "70026900": (441, [25, 91, 570, 262], "26 polegadas | 660mm | Conexão gancho estreito (8,5mm)",
                 "Volvo: NH12 de 1996 a 2006; Mercedes Benz: 1938 S e 1944 S 1998 em diante, Atego de 2004 a 2006, Axor de 2001 a 2006; "
                 "Iveco: Stralis 2008 em diante, Tector 2011 em diante; Ford: Cargo 2011 em diante"),
    "70026901": (441, [25, 267, 570, 447], "26 polegadas | 660mm | Conexão gancho largo (11,5mm)",
                 "Volvo: FH10 e FH12 de 1994 a 2006, FM10 e FM12 de 2000 a 2006, NH10 e NH12 1994 em diante; Iveco: Cavallino, Cursor, "
                 "Fire, Star, Tech de 1998 a 2012, Eurocargo, Trakker de 2004 a 2012, Stralis, Tector de 2004 a 2010; "
                 "Mercedes Benz: Atego, Atron, Axor 2006 em diante"),
    "70026908": (441, [25, 452, 570, 634], "26 polegadas | 660mm | Conexão parafuso P01", "Ford: todos até 2011"),
    "70027901": (441, [25, 639, 570, 805], "27 polegadas | 685mm | Conexão gancho largo (11,5mm)",
                 "Man: TGL, TGM, TGS, TGX, TGX V8 2011 em diante; Scania: 114, 124, 94, série 4 P/R/T de 1998 a 2007, série 5 P/G/R 2008 "
                 "em diante"),
    "70028406": (442, [25, 91, 583, 265], "28 polegadas | 711mm | Conexão gancho | Conector modelo similar ao original",
                 "Mercedes Benz: Actros 2010 em diante"),
    "70028705": (442, [25, 270, 583, 456], "28 polegadas | 711mm | Conexão gancho | Conector similar original | Com esguicho e suporte",
                 "Scania: NTG série 6 2019 em diante"),
    "70028706": (442, [25, 459, 583, 650], "28 polegadas | 711mm | Conexão gancho largo (11,5mm) | Com esguicho e suporte",
                 "Volvo: FH novo 2020 em diante, FH12 de 2013 a 2017, FH13 e FH16 2013 em diante; Scania: série 5 de 2008 a 2018")}
_DESC = dict(_LISTA)
_MONT = [("Agrale", "Agrale"), ("Volkswagen", "Volkswagen"), ("Mercedes", "Mercedes-Benz"), ("DAF", "DAF"), ("Iveco", "Iveco"),
         ("Renault", "Renault"), ("Volvo", "Volvo"), ("Scania", "Scania"), ("Ford", "Ford"), ("Man:", "MAN"), ("Puma", "Puma")]
for _c, (_p, _rect, _esp, _apl) in _DET.items():
    R(_p, _c, _DESC[_c], _rect, marca="DNA", info=("Especificações: " + _esp) if _esp else "", aplicacao=_apl,
      montadora=", ".join(m for k, m in _MONT if k in _apl))
for _r in ADD:
    if _r["pagina"] == 438 and _r["codigo"] in _DET:
        _r["foto_spec"] = None  # foto vem da página de detalhe
    if _r["codigo"] == "70028704":
        _r.update(montadora="Mercedes-Benz", aplicacao="MB Actros 2021 em diante")
# 442: bombinhas do interclima
R(442, "7001200", "BOMBINHA INTERCLIMA 12V", [25, 655, 300, 805], info="Especificações: água/gasolina | Bico fino | 24V")
R(442, "7002400", "BOMBINHA INTERCLIMA 24V", [302, 655, 583, 805], info="Especificações: água/gasolina | Bico fino | 24V")
NOTAS.append("Pág. 442: a bombinha interclima 7001200 está anunciada como 12V, mas a especificação do card diz 24V.")
NOTAS.append("Pág. 442: a palheta 70028406 está descrita como 'MB ACTROS 2016 A 2020' e a aplicação do card diz 'Actros 2010 em diante'.")
