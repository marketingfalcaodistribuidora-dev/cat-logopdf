"""Cards com diagramação própria: ficha técnica organizada em colunas."""

PRETO = [17, 17, 17]
FICHAS = {
    "6212019": dict(
        titulo="MOTOBOMBA GASOLINA P/AGUA PX50, 7 CV, 2, 600",
        cabecalho="Principais características",
        itens=[
            ("Altura manométrica máxima, m", "30"), ("Altura, mm", "445"), ("Arranque", "manual"),
            ("Capacidade do tanque de combustível, L", "3"), ("Ciclo do motor", "quatro tempos"),
            ("Cilindrada do motor, cm³", "212"), ("Comprimento, mm", "510"), ("Consumo de combustível, L/h", "1.9000"),
            ("Desempenho, L/min", "1000"), ("Diâmetro de entrada, mm", "80"), ("Diâmetro de saída", "80 mm"),
            ("Fabricante de motores", "Denzel"), ("Funcionalidades", "ajuste de pressão"),
            ("Indicação e visores", "sensor de nível de óleo baixo"), ("Largura, mm", "385"), ("Material do corpo", "metal"),
            ("Nível de potência sonora, dB", "110"), ("Potência do motor, cv", "7"),
            ("Tamanho máximo de partículas sólidas, mm", "3"), ("Tipo", "para água limpa"),
            ("Tipo de combustível", "AI-92"), ("Tipo de motor", "a gasolina"), ("Volume de óleo no cárter, L", "0.6000"),
        ],
    ),
}


def aplicar(ops):
    saida = []
    for o in ops:
        ficha = FICHAS.get(str(o[6])[6:]) if o[0] == "t" and str(o[6]).startswith("Dados ") else None
        if not ficha:
            saida.append(o)
            continue
        cod = str(o[6])[6:]
        x, topo, largura = o[1], o[2] - 66, o[3]
        saida.append(["t", x, topo, largura - 160, 84, [[[ficha["titulo"], "b", 7, PRETO]], [[ficha["cabecalho"], "b", 7, PRETO]]],
                      o[6], "l"])
        itens = ficha["itens"]
        por_coluna = (len(itens) + 2) // 3
        w = (largura - 80) // 3
        for c in range(3):
            parte = itens[c * por_coluna:(c + 1) * por_coluna]
            paras = [[[rot + ":", "b", 6.5, PRETO], [" " + val, "r", 6.5, PRETO]] for rot, val in parte]
            saida.append(["t", x + c * (w + 40), topo + 88, w, 390, paras, "Ficha %s coluna %d" % (cod, c + 1), "l"])
    return saida
