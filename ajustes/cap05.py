# Capítulo 5 - Mola Freio e Rebite Lona (págs. 40-42)
# As molduras destas páginas se sobrepõem e parte das descrições está em imagem:
# todos os produtos foram lidos visualmente e registrados aqui, com o recorte da foto de cada célula.
MANUAIS = {40, 41, 42}

# grade da pág. 40: 3 colunas x 10 linhas
_X = [(25.1, 206.8), (206.8, 388.4), (388.4, 570.0)]
_Y = [(87.8, 160.9), (160.9, 233.9), (233.9, 307.0), (307.0, 380.0), (380.0, 453.0), (453.0, 526.1),
      (526.1, 599.1), (599.1, 672.0), (672.0, 743.9), (743.9, 804.7)]


def cel(lin, col):
    (x0, x1), (y0, y1) = _X[col], _Y[lin]
    return {"rect": [x0 + 1, y0 + 1, x1 - 1, y1 - 1]}


def M(pag, card, codigo, descricao, tipo, foto, cod_ref="", montadora="", info="", aplicacao="", marca=""):
    return dict(pagina=pag, card=card, codigo=codigo, descricao=descricao, tipo=tipo, foto_spec=foto, cod_ref=cod_ref,
                montadora=montadora, info=info, aplicacao=aplicacao, marca=marca)


ADD = [
    # ---------------- pág. 40 ----------------
    M(40, 1, "5665316", "MOLA 2 GOMOS PRETA 05MM GROSSA", "MOLA SAPATA 2 GOMOS", cel(0, 0), info="208MM"),
    M(40, 2, "5660829", "MOLA A CARRETA 2 GOMOS AZUL 6MM ORIGINAL", "MOLA SAPATA 2 GOMOS", cel(0, 1), info="208MM | 06 MM"),
    M(40, 3, "5660408", "MOLA A CARRETA 2 GOMOS C/GANCHO", "MOLA SAPATA 2 GOMOS", cel(0, 2), info="220MM"),
    M(40, 4, "5660832", "MOLA PATIM SUBSTITUI 2 GOMOS", "MOLA PATIM", cel(1, 0), info="200MM | Menor"),
    M(40, 5, "5660831", "MOLA PATIM SUBSTITUI 2 GOMOS", "MOLA PATIM", cel(1, 1), info="220MM | Maior"),
    M(40, 6, "5660828", "MOLA PATIM PEQUENA CAMARAO", "MOLA PATIM", cel(1, 2), info="Camarão | Mola de freio carreta | 130MM"),
    M(40, 7, "5660830", "MOLA FREIO AR", "MOLA FREIO", cel(2, 0), montadora="Mercedes-Benz"),
    M(40, 8, "5660854", "MOLA A SAPATA FORD E GUERRA", "MOLA SAPATA", cel(2, 1), montadora="Volkswagen, Ford, Guerra", info="Camarão | 145MM"),
    M(40, 9, "5660610", "MOLA A DUPLA 207MM SCANIA MENO", "MOLA DUPLA", cel(2, 2), montadora="Scania", info="207MM"),
    M(40, 10, "5660609", "MOLA A SCANIA DUP D/T 255M LONGA", "MOLA DUPLA", cel(3, 0), montadora="Scania", info="255MM"),
    M(40, 11, "5660611", "MOLA A DUPLA SCANIA D/T 270MM LONGA", "MOLA DUPLA", cel(3, 1), montadora="Scania", info="270MM"),
    M(40, 12, "5661434", "MOLA PATIM DIANT. / TRAS. SCANIA", "MOLA PATIM", cel(3, 2), montadora="Scania"),
    M(40, 13, "5660482", "MOLA A CAR. GUERRA MENOR 226M", "MOLA SAPATA", cel(4, 0), montadora="Guerra", info="Menor | 226MM"),
    M(40, 14, "5660105", "MOLA A CAR.GUERRA MAIOR 235MM", "MOLA SAPATA", cel(4, 1), montadora="Guerra", info="Maior | 235MM"),
    M(40, 15, "5660974", "MOLA A VOLVO PATIM DIANTEIRO", "MOLA PATIM", cel(4, 2), montadora="Volvo"),
    M(40, 16, "5660975", "MOLA A VOLVO PATIM TRASEIRO", "MOLA PATIM", cel(5, 0), montadora="Volvo"),
    M(40, 17, "5660426", "MOLA PEQUENA PARACHOQUE 180MM", "MOLA PARACHOQUE", cel(5, 1), info="Pequena | 180MM"),
    M(40, 18, "5660340", "MOLA PARACHOQUE GRANDE", "MOLA PARACHOQUE", cel(5, 2), info="Grande | 500MM"),
    M(40, 19, "5660216", "MOLA A ACEL MERCEDES 366", "MOLA ACELERADOR", cel(6, 0), montadora="Mercedes-Benz"),
    M(40, 20, "5660204", "MOLA A ACEL. MERCEDES MACIA", "MOLA ACELERADOR", cel(6, 1), montadora="Mercedes-Benz"),
    M(40, 21, "5660512", "MOLA A BICA RANDON TP ALFINETE", "MOLA BICA", cel(6, 2), montadora="Randon"),
    M(40, 22, "5660009", "TRAVA PORCA 5/8 CARROCERIA", "TRAVA PORCA", cel(7, 0)),
    M(40, 23, "5669005", "TRAVA PORCA 3/4 CARROCERIA", "TRAVA PORCA", cel(7, 0)),
    M(40, 24, "5660868", "MOLA RT PEDAL/ACEL 1420 14150/14200/ONIBUS 16180CO", "MOLA ACELERADOR", cel(7, 1), cod_ref="TAR.721.619", montadora="Volkswagen"),
    M(40, 25, "5660872", "MOLA RT CABO ACELERADOR 14170BT/16220/16300/24220/35300", "MOLA ACELERADOR", cel(7, 2), cod_ref="TAR.721.619A", montadora="Volkswagen", info="150mm"),
    M(40, 26, "5668927", "MOLA A ACELE 65MM 7.90/7.110 VOLKS 7.90S/7.110S", "MOLA ACELERADOR", cel(8, 0), cod_ref="T12.721.339", montadora="Volkswagen"),
    M(40, 27, "5660863", "MOLA A FIX PATIM D/T 105MM VW VW 6.90/7.90/7.110S", "MOLA PATIM", cel(8, 1), cod_ref="T06.609.283", montadora="Volkswagen"),
    M(40, 28, "5668922", "MOLA A PATIM F 8. 120 0D/160MM MICRO 8.120OD/8150OD/9150OD", "MOLA PATIM", cel(8, 2), cod_ref="2R0.609.465", montadora="Volkswagen"),
    M(40, 29, "5660866", "MOLA A PATIM T 7.100/8.140 VW 7.100S/8.140", "MOLA PATIM", cel(9, 0), cod_ref="2RD.607.039", montadora="Volkswagen"),
    M(40, 30, "5661893", "MOLA A PATIM FORD CARGO C-1119", "MOLA PATIM", cel(9, 1), montadora="Ford"),
    # ---------------- pág. 41 ----------------
    M(41, 1, "5664001", "MOLA A PATIM ACTROS -ATEGO-LK E LN-MK-SK-NG", "MOLA PATIM", {"rect": [26, 89, 297, 274]},
      cod_ref="346.993.0810", montadora="Mercedes-Benz", info="Interno 240mm | Aço 4,20mm | Ref. 5MB-4001 | Logos Actros / Atego"),
    M(41, 2, "5664002", "MOLA A PATIM AXOR - ACTROS MP2 MP3 ATEGO", "MOLA PATIM", {"rect": [299, 89, 571, 274]},
      cod_ref="945.993.0010", montadora="Mercedes-Benz", info="Interno 235mm | Aço 4,00mm | Ref. 5MB-4002 | Logos Axor / Actros / Atego"),
    M(41, 3, "5665021", "MOLA A PATIM NOVA DAILY 3.0 16V 70C16 / 70C17", "MOLA PATIM", {"rect": [26, 276, 297, 474]},
      cod_ref="50006868", montadora="Iveco", info="Interno 120mm | Aço 3,00mm | Ref. 5IVC-5021"),
    M(41, 4, "5665022", "MOLA A PATIM IVECO PRETA ONIBUS 170S28", "MOLA PATIM", {"rect": [299, 276, 571, 474]},
      cod_ref="500057411 / MO 223", montadora="Iveco", info="Interno 227mm | Aço 5,50mm | Ref. 5IVC-5022"),
    M(41, 5, "5668947", "MOLA FIXACAO SAPATA FREIO VW DELIVERY EXPRESS", "MOLA PATIM", {"rect": [26, 476, 297, 661]},
      cod_ref="MO-216", montadora="Volkswagen", info="Interno 155mm | Aço 4,50mm | Ref. 5MVW-8947"),
    M(41, 6, "5660010", "MOLA A PATIM DAF CF 85 / XF 105", "MOLA PATIM", {"rect": [299, 476, 571, 661]},
      cod_ref="1340297", montadora="DAF"),
    M(41, 7, "5660001", "MOLA ASA DELTA", "MOLA ASA DELTA", {"rect": [26, 665, 571, 805]}),
    # ---------------- pág. 42 ----------------
    M(42, 1, "9291708", "REBITE ALUMINIO MACICO 07X08 F4000 NOVA(05XX07X10MM)", "REBITE MACIÇO", {"rect": [430, 157, 553, 236]}),
    M(42, 1, "9291012", "REBITE MACICO 10X12(6X19)", "REBITE MACIÇO", {"rect": [430, 157, 553, 236]}),
    M(42, 1, "9291014", "REBITE ALUMINIO M 10 X 14", "REBITE MACIÇO", {"rect": [430, 157, 553, 236]}),
    M(42, 1, "9290846", "REBITE MACICO 10X16(6X25)", "REBITE MACIÇO", {"rect": [430, 157, 553, 236]}),
    M(42, 1, "9290889", "REBITE MACICO 13X12(8X19)", "REBITE MACIÇO", {"rect": [430, 157, 553, 236]}),
    M(42, 1, "9290855", "REBITE MACICO 13X16(8X25)", "REBITE MACIÇO", {"rect": [430, 157, 553, 236]}),
    M(42, 1, "9379033", "REBITE M ALUM 3/8X7/8 CAB LENT", "REBITE MACIÇO", {"rect": [430, 157, 553, 236]}),
    M(42, 2, "9290217", "REBITE ST ALU 03X06", "REBITE SEMI-TUBULAR", {"rect": [416, 351, 567, 459]}),
    M(42, 2, "9290218", "REBITE ST ALU 04X06", "REBITE SEMI-TUBULAR", {"rect": [416, 351, 567, 459]}),
    M(42, 2, "9290706", "REBITE ST ALU 07X06", "REBITE SEMI-TUBULAR", {"rect": [416, 351, 567, 459]}),
    M(42, 2, "9290708", "REBITE ST ALU 07X08 F.4000", "REBITE SEMI-TUBULAR", {"rect": [416, 351, 567, 459]}),
    M(42, 2, "9290710", "REBITE ST ALU 07X10 F.4000 NOVA", "REBITE SEMI-TUBULAR", {"rect": [416, 351, 567, 459]}),
    M(42, 2, "9290619", "REBITE ST ALU 10X12(6X19)", "REBITE SEMI-TUBULAR", {"rect": [416, 351, 567, 459]}),
    M(42, 2, "9291162", "REBITE ST ALU 10X14(6X22)", "REBITE SEMI-TUBULAR", {"rect": [416, 351, 567, 459]}),
    M(42, 2, "9291163", "REBITE ST ALU 10X16(6X25)", "REBITE SEMI-TUBULAR", {"rect": [416, 351, 567, 459]}),
    M(42, 2, "9291164", "REBITE ST ALU 13X12(8X19)", "REBITE SEMI-TUBULAR", {"rect": [416, 351, 567, 459]}),
    M(42, 3, "9372010", "REBITE LENTILHA 3/16 X 1/2", "REBITE LENTILHA", {"rect": [488, 495, 553, 535]}),
    M(42, 4, "9292102", "REBITE B TB 10X12", "REBITE BICROMATIZADO", {"rect": [394, 600, 510, 661]}),
    M(42, 4, "9290112", "REBITE B TB 10X14", "REBITE BICROMATIZADO", {"rect": [394, 600, 510, 661]}),
    M(42, 4, "9291314", "REBITE B TB 13X14", "REBITE BICROMATIZADO", {"rect": [394, 600, 510, 661]}),
    M(42, 4, "9290825", "REBITE B TB 13X16", "REBITE BICROMATIZADO", {"rect": [394, 600, 510, 661]}),
    M(42, 5, "3173061", "PORCA REBITE LI PLA 3,0 M6", "PORCA REBITE", {"rect": [49, 704, 286, 798]}),
    M(42, 6, "3173008", "PORCA REBITE LI PLA 3,0 M8", "PORCA REBITE", {"rect": [337, 704, 567, 798]}),
]
NOTAS = [
    "p42: o código 3173061 aparece duas vezes na camada de texto do PDF (uma oculta sob o card PORCA REBITE M6); registrado uma vez, como visível no catálogo.",
]
