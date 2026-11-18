# Capítulo 42 - Tampas de Tanque e Radiador, Antena PX, Registros e Cordas (págs. 473-477)
TIPOS = [(r"^TAMPA RADIADOR", "TAMPA RADIADOR"), (r"^TAMPA OLEO", "TAMPA ÓLEO MOTOR"), (r"^TAMPA", "TAMPA TANQUE"),
         (r"^ANTENA", "ANTENA PX"), (r"^CABO", "CABO PX"), (r"^KIT", "KIT MONTAGEM ANTENA"), (r"^REGISTRO", "REGISTRO"),
         (r"^REDU", "REDUÇÃO"), (r"^PINO", "PINO ENGATE"), (r"CORDA", "CORDA")]
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(473, 478))


def R(p, cod, desc, foto, card=None, **kw):
    r = dict(pagina=p, card=card or (len(ADD) + 1), codigo=cod, descricao=desc, cod_ref="", variacoes="", aplicacao="", info="",
             marca="", montadora="", _nao_agrupar=card is None, foto_spec={"rect": foto})
    r.update(kw)
    ADD.append(r)


def G(p, card, titulo, itens, foto, **kw):
    for c, d in itens:
        R(p, c, d, foto, card=card, _titulo=titulo, **kw)


# 473 (pág. impressa 472): tampas anti-vazamento e antena PX
R(473, "7001101", "TAMPA ANTI VAZ GRANDE 2 PF VOLVO/FH/IVECO/MB", [55, 110, 195, 345], montadora="Volvo, Iveco, Mercedes-Benz",
  info="Diâmetro rosca: 10mm | Diâmetro: 110mm ext x 105mm int x 33mm alt")
R(473, "7001102", "TAMPA ANTIV ROSCA INT VW/SCANIA 124/S4/S5", [225, 93, 380, 340], montadora="Volkswagen, Scania",
  info="Diâmetro rosca: 63mm | Diâmetro: 97mm ext x 88mm int x 30mm alt")
R(473, "7001103", "TAMPA ANTI VAZAMENTO SCANIA 111/112/113/ARL", [415, 92, 565, 330], montadora="Scania",
  info="Diâmetro rosca: 10mm | Diâmetro: 87mm ext x 80mm int x 23mm alt")
R(473, "7032025", "ANTENA PX ARGENTINA BLACK COM PROLONGADOR", [225, 420, 255, 585],
  info="Melhor potência de transmissão do mercado SWR 1X1 | Altura 1,63cm (como impresso) | Melhor resistência | Melhor potência | "
       "Melhor performance")
R(473, "7030121", "CABO PX C/CONECTOR SOLD 5,475M", [257, 410, 403, 519])
R(473, "7030016", "KIT MONTAGEM ANTENA PX", [420, 450, 570, 560])
NOTAS.append("Pág. 473: o card 6 da página está vazio.")
# 474 (pág. impressa 473): tampas tanque / radiador (marca Mavi? logos 'Kit' nos cards)
R(474, "231014", "TAMPA TANQUE COMBUSTIVEL", [29, 118, 128, 220], info="Campeão de vendas | Código impresso com 6 dígitos",
  montadora="Agco, Agrale, Ford, Mercedes-Benz, Scania, Volvo, Volkswagen",
  aplicacao="Marcas: Agco, Agrale, Ford, MBB, Scania, Volvo, VW | Segmento: agrícola, pesado | Agco (tanque com rosca interna); "
            "Ford – Cargo 02>; F-4000 05>, nº original 2C45-9W030-AA/2C45.9W030-BA; VW – caminhões, ônibus, microônibus 13-150, "
            "13-180, 13-190, 15-180, 15-190, 17-210, 17-310, 17-220, 18-310, 23-310, 24-220, 26-260, 26-310, 31-310, 31-260 – 05/02>, "
            "nº original 2Z0.201.551 / 2T0.201.551; Scania – série IV (114) 97>; MBB; Volvo; Agrale (tanque com rosca interna), "
            "nº original 143.67.83/151.79.66/151.47.75 | Vedada (texto do card parcialmente coberto pelo selo)")
R(474, "237115", "TAMPA RADIADOR MB ANTIGO 7 LBS", [219, 126, 378, 183], montadora="Mercedes-Benz",
  cod_ref="344.501.03.15 / 045.501.00.15-B", aplicacao="608 OM 88 / 1113 88 / 2013 88")
R(474, "234615", "TAMPA RADIADOR MB MODERNO", [412, 117, 557, 204], montadora="Mercedes-Benz",
  cod_ref="364.501.70.15 / 000.501.46.15", info="Original 10 Lbs | 0,60 a 0,89bar / valvulada")
R(474, "237100", "TAMPA RADIADOR MB ACCELO/ AXOR", [84, 263, 199, 355], montadora="Mercedes-Benz", cod_ref="000.501.67.15",
  aplicacao="Motores 457, 904, 906, 1938 04", info="0,80 a 1,20bar | Valvulada")
R(474, "2370061", "TAMPA RADIADOR 7LBS FORD/AGRALE/GMC", [229, 263, 386, 359], montadora="Agrale, Ford, GM, Mercedes-Benz",
  aplicacao="Agrale - todos; Ford - F-100 a F-22000; GM; Mercedes Benz pick-up 6 cilindros; GMC - todos",
  info="7Lbs | 0,35 a 0,50 bar | Valvulada")
R(474, "2370141", "TAMPA RADIADOR FORD CARGO / VW", [445, 265, 564, 348], montadora="Ford, Volkswagen",
  cod_ref="Ford: T11.121.484A / XC458100BA; VW: TJG.121.484", aplicacao="Ford caminhões Cargo; VW caminhões e ônibus",
  info="13Lbs | 0,80 a 1,10bar | Valvulada")
R(474, "2370701", "TAMPA RADIADOR FORD CARGO / VW/ FIAT", [79, 409, 201, 489], montadora="Ford, Volkswagen, Fiat",
  aplicacao="1600-D, 1800-D; Fiat 70, 80, 130, 140, 120, 190H - todos; Ford caminhões Cargo 84; VW caminhões e ônibus",
  info="0,60 a 0,75bar | Valvulada")
R(474, "2370761", "TAMPA RADIADOR FORD F1000/4000 /GM D20", [270, 404, 384, 490], montadora="Ford, GM",
  cod_ref="Ford: 52.252.299 / 94.629.748; GM: T71.121.484-B / 2SB-121.484",
  aplicacao="Ford F-1000, F-4000, F-12000, F-14000 92-98; GM AC20 85-96, AC40 85-96, ACD 91-95, Custon 11.000 a 14.000 85-96, D20 85",
  info="0,40 a 0,80bar | Valvulada")
R(474, "2310501", "TAMPA RADIADOR MB BENZ / SCANIA", [455, 403, 567, 488], montadora="Mercedes-Benz, Scania",
  cod_ref="344.018.01.68 / 344.018.03.68 / 344.018.02.68 / 430/018.00.61 / 102.018.04.02 / 290.040.12.39", aplicacao="Todos")
R(474, "237068", "TAMPA OLEO MOTOR 1113 ANTIGO", [46, 559, 195, 631], montadora="Mercedes-Benz", cod_ref="344 010 70 68",
  aplicacao="L 1111/1113/LPO/0352")
R(474, "7021020", "TAMPA PLASTICA SCANIA ARLA C/ CHAVE", [400, 558, 568, 654], montadora="Scania", marca="Amil")
R(474, "8003120", "TAMPA TANQUE SCANIA MODELO ORIGINAL", [90, 695, 198, 780], montadora="Scania", cod_ref="1369848")
R(474, "7008345", "TAMPA TANQUE ARLA AZUL", [265, 681, 349, 762], montadora="Scania", aplicacao="Série 5 cabine R",
  cod_ref="112524 e 1918345")
R(474, "0231004", "TAMPA TANQUE COMB MB AXOR 105 MM", [419, 697, 533, 786], montadora="Mercedes-Benz, Volkswagen, Ford, GM",
  info="Tampa tanque comb diesel - VW/Ford/GM/MB caminhão")
NOTAS.append("Pág. 474: vários códigos têm 6 dígitos (231014, 237115, 234615, 237100, 237068) e 0231004 começa com zero; "
             "o card 11 está vazio. 7008345 traz a mesma aplicação/conversão do 5171483 (Arla, pág. 465).")
# 475 (pág. impressa 474)
R(475, "5162353", "TAMPA TANQUE VOLVO FH 2010 C/CHAVE LATERAL", [57, 97, 170, 174], montadora="Volvo",
  aplicacao="B58, F10, F12, F16, FH 12, FH 16, FL 10, FL 12, FL6, FL7, FM 10, FM 12, FM7, FM9, FS7, N10, N12, NH12, NL10, NL12")
R(475, "5162351", "TAMPA TANQUE VOLVO FH/ FM/NH C/CHAVE CENTRAL", [241, 102, 359, 170], montadora="Volvo",
  aplicacao="FH 1994 a 2015; FMX 2010 a 2015")
R(475, "237105", "TAMPA TANQUE COMB MB C/CHAVE GRANDE PRETA", [437, 95, 562, 182], montadora="Mercedes-Benz",
  cod_ref="12120, 1800329, 3444700105, 3444700305, 3444703005, 3864707005, 3864707105, 521487")
# 476 (pág. impressa 475): registros, reduções e pinos de engate
_E, _D = (25, 298), (298, 570)
for _c, _d, _x, _y in [("7001105", "REGISTRO EMENDA 5/16", _E, (90, 228)), ("7001106", "REGISTRO BORBOLETA P13 MANGUEIRA", _D, (90, 228)),
                       ("7001104", "REGISTRO BOTIJAO P13", _E, (232, 415)), ("7000031", "REGISTRO BORBOLETA COM BICO RODOAR", _D, (232, 415)),
                       ("7000030", "REGISTRO FXF C/ BICO RODOAR", _E, (419, 594)), ("7000240", "REGISTRO FXF", _D, (419, 594)),
                       ("7000140", "REDUÇÃO P/13", _E, (598, 697)), ("7001107", "PINO ENGATE SAIDA 08MM", _D, (598, 697)),
                       ("7000150", "REDUÇÃO P/2", _E, (701, 805)), ("7001108", "PINO ENGATE ESCAMA 5/16", _D, (701, 805))]:
    R(476, _c, _d, [_x[0], _y[0], _x[1], _y[1]])
# 477 (pág. impressa 476): cordas Itacorda
G(477, 1, "CORDA PET TRANÇADA ECOFRIENDLY (ROLO)", [("0008233", "@CORDA PET 08MM 233MTS"), ("0001156", "@CORDA PET 10MM 156MTS")],
  [28, 100, 570, 400], marca="Itacorda", info="Corda trançada ecofriendly | rolo")
G(477, 2, "ITACORDA OLEADA (CORDA TRANÇADA POLIÉSTER VIRGEM - SACO)",
  [("0008301", "@ITACORDA OLEADA 08MM 300MTS"), ("0008150", "@ITACORDA OLEADA 08MM 150MTS"),
   ("0001031", "@ITACORDA OLEADA 10MM 300MTS"), ("0001015", "@ITACORDA OLEADA 10MM 150MTS")], [28, 480, 300, 790],
  marca="Itacorda", info="Corda trançada poliéster virgem oleada | saco | 100% poliéster virgem | Espessura 8mm (5/16) e 10mm (3/8)")
