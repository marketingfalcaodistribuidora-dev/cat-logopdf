# Capítulo 40 - Tacógrafo e Amarração de Carga (págs. 462-464)
TIPOS = [(r"^DISCO", "DISCO TACÓGRAFO"), (r"^BOBINA", "BOBINA TACÓGRAFO"), (r"^CATRACA", "CATRACA"), (r"CINTA", "CINTA"),
         (r"^DISPOSITIVO", "DISPOSITIVO DE AMARRAÇÃO"), (r"^ESTICK", "ESTICADOR DE LONA"), (r"^PROTETOR", "PROTETOR DE CINTA")]
AJ = {}
ADD = []
NOTAS = []
MANUAIS = set(range(462, 465))


def R(p, cod, desc, foto, card=None, **kw):
    r = dict(pagina=p, card=card or (len(ADD) + 1), codigo=cod, descricao=desc, cod_ref="", variacoes="", aplicacao="", info="",
             marca="", montadora="", _nao_agrupar=card is None, foto_spec={"rect": foto})
    r.update(kw)
    ADD.append(r)


def G(p, card, titulo, itens, foto, **kw):
    for c, d in itens:
        R(p, c, d, foto, card=card, _titulo=titulo, **kw)


# 462 (pág. impressa 461): tacógrafo
_DIM = "Dimensões: disco tacógrafo semanal (7 dias) 125KM/H 20x20"
R(462, "5062164", "DISCO TACOGRAFO DML SEMANAL", [70, 215, 250, 380], marca="DML", info=_DIM)
R(462, "5067125", "DISCO TACOGRAFO VDO SEMANAL", [335, 175, 565, 395], marca="VDO", info=_DIM)
R(462, "5067124", "BOBINA DE TACOGRAFO", [240, 470, 565, 790], marca="DML", cod_ref="DML-001B01",
  info="Velocidade máxima do registro na bobina tacógrafo de 150Km/h")
# 463 (pág. impressa 462): catracas e cintas (códigos '@' = referência curta impressa no card)
_IT = dict(marca="Itacorda")
R(463, "@485", "CATRACA CONJ AMARRAÇÃO 3T 9 METROS", [30, 96, 120, 170], info="Código impresso como '@485'", **_IT)
R(463, "@486", "CATRACA CONJ AMARRAÇÃO 5T 9 METROS", [215, 96, 305, 170], info="Código impresso como '@486'", **_IT)
R(463, "7000100", "CATRACA CONJ AMARRAÇÃO 10T 9 METROS", [399, 96, 490, 170], variacoes="@487", **_IT)
R(463, "@483", "CINTA 03 TONELADAS LARANJA 9 METROS", [30, 232, 196, 325], info="Código impresso como '@483'", **_IT)
R(463, "@480", "CINTA 05 TONELADAS LARANJA 9 METROS", [215, 232, 381, 325], info="Código impresso como '@480'", **_IT)
R(463, "@484", "CINTA 10 TONELADAS LARANJA 9 METROS", [399, 232, 565, 325], info="Código impresso como '@484'", **_IT)
R(463, "@585", "CATRACA (CONJ AMARRAÇÃO 3T) 9 METROS", [30, 372, 145, 455], info="Importada | Código impresso como '@585'")
R(463, "@586", "CATRACA (CONJ AMARRAÇÃO 5T) 9 METROS", [215, 372, 330, 455], info="Importada | Código impresso como '@586'")
R(463, "7080404", "CINTA PARA ELEVAÇÃO 4T", [415, 380, 560, 465], info="Dimensão: 12X400CM")
R(463, "7089920", "CINTA SIDER 72CM", [30, 515, 196, 600])
R(463, "5060873", "DISPOSITIVO AMARRACAO DE CARGA", [280, 520, 380, 610], info="Tamanho: 55MM")
R(463, "7080125", "CATRACA FIXA SIDER TRES FUROS ZINCADA", [455, 515, 565, 590], info="Capacidade: 5000KG | Largura: 50mm")
G(463, 13, "ESTICK LONA PRETO", [("7000001", "ESTICK LONA PRETO 35CM"), ("7085060", "ESTICK LONA PRETO 60CM")], [30, 650, 196, 735],
  marca="Mave")
G(463, 14, "CATRACA TENSIONADORA LATERAL FACCHINI", [("4041003", "CATRACA TENSIONADORA LATERAL FACCHINI LD"),
                                                    ("4042003", "CATRACA TENSIONADORA LATERAL FACCHINI LE")],
  [240, 655, 380, 725], montadora="Facchini")
G(463, 15, "CATRACA TENSIONADORA LATERAL FACCHINI", [("4041002", "CATRACA TENSIONADORA LATERAL FACCHINI LD"),
                                                    ("4042002", "CATRACA TENSIONADORA LATERAL FACCHINI LE")],
  [425, 655, 565, 725], montadora="Randon", info="Logo Randon no card")
NOTAS.append("Pág. 463: as catracas e cintas Itacorda / importadas trazem só referências curtas '@485', '@486', '@483', '@480', "
             "'@484', '@585', '@586' (lançadas como código); o card de 10T traz '@487' e o código 7000100. O card 15 diz "
             "'Facchini' na descrição mas tem logo Randon.")
# 464 (pág. impressa 463)
R(464, "71210034", "CATRACA 03 TONELADAS AMARAÇÃO ROBUSTEC", [40, 270, 560, 560], marca="Robustec",
  info="3T | Produzida em material 100% poliéster, que garante menor absorção de água | Utilizado para amarração de cargas como "
       "implementos agrícolas, geradores, caminhões entre outros | Gancho e catraca em aço bicromatizado")
R(464, "6102043", "PROTETOR CINTA ATE 5T", [35, 625, 115, 790])
R(464, "6102044", "PROTETOR CINTA ATE 10T", [300, 625, 395, 790])
