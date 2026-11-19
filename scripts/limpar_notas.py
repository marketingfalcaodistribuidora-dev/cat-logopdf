"""Remove dos cards as anotações feitas durante a leitura do PDF.

A planilha e o CSV continuam com o texto original; só o que é impresso no card muda.
"""
import re

REMOVER = re.compile(
    r"^(\d+:\s*)?("
    r"Descrição (impressa|conforme)|Texto impresso|Texto presente|Título (impresso|cita|do card)|"
    r"Código (impresso|interno impresso|interno não impresso|e \d+ª linha)|Impresso\b|\d+ impresso em|"
    r"Lista impressa|Consta só|Card (com os códigos|repetido)|Canto do card|Na pág\.|Na lista consta|"
    r"No card\b|O card\b|O código \S+ aparece|O quadro do card|O texto do card|Sem foto própria|"
    r"Ref\. original lida|Também (descrito|apresentado|listada|em card|anunciada)|Aplicação '|"
    r"Vista explodida|Campeão de vendas?$|Vedada \(texto do card"
    r")",
    re.I,
)
TROCAS = [
    (r"^Obs\.: o quadro do card repete o texto do ST \d+ / ", ""),
    (r"^Texto do card:\s*", ""),
    (r"^Logos? no card:\s*", ""),
    (r"^Logos?\s+", ""),
    (r"\s*\(logos?\):", ":"),
    (r"\s*\(rótulo no card\)", ""),
    (r"\s*\(sem código\)", ""),
    (r"\s*\(ref\. original impressa\)", ""),
    (r"\s*\((como impresso|impresso em cm|impresso no card|texto do card|na foto)\)", ""),
    (r"\s*\((lista completa no card|lista no card|tabela de aplicação do card)\)", ""),
    (r"\s*-\s*lista completa no card", ""),
    (r"\s+e demais (Volvo|versões) listad[oa]s no card( \(todas as versões\))?", ""),
    (r"\s+listadas no card", ""),
    (r"\s+no card$", ""),
    (r"\s*\(a lista não tem foto própria\)", ""),
    (r"\s*\(tabela com nº[^)]*\)", ""),
    (r"^Selo de lançamento$", ""),
    (r"\bLANÇAMENTOS?\b\s*:?\s*(\d{2}/\d{2,4})?\s*", ""),
]
TROCAS = [(re.compile(a, re.I), b) for a, b in TROCAS]


def sem_lancamento(texto):
    """Tira a palavra LANÇAMENTO do fim de descrições."""
    return re.sub(r"\s+LANÇAMENTOS?\s*$", "", texto, flags=re.I)


def limpar(texto):
    """Devolve o campo sem as anotações, mantendo o restante exatamente igual."""
    saida = []
    for seg in texto.split(" | "):
        novo = seg
        for rx, sub in TROCAS:
            novo = rx.sub(sub, novo)
        if novo.strip() and not REMOVER.match(novo.strip()):
            saida.append(novo)
    return " | ".join(saida)
