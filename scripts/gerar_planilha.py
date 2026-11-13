"""Gera a planilha Catalogo_Falcao_2026.xlsx a partir de dados/capNN.json."""
import glob
import json
import os
import re
import unicodedata

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(BASE, "Catalogo_Falcao_2026.xlsx")

COLS = [
    ("Categoria", 22, "capitulo"),
    ("Marca (montadora / aplicação)", 26, "montadora"),
    ("Marca do produto", 18, "marca"),
    ("Tipo", 26, "tipo"),
    ("Código interno", 14, "codigo"),
    ("Descrição", 48, "descricao"),
    ("Código ref. (original)", 30, "cod_ref"),
    ("Variações / outras referências", 40, "variacoes"),
    ("Aplicação", 40, "aplicacao"),
    ("Informações adicionais", 50, "info"),
    ("Foto", 16, "foto"),
    ("Página(s)", 12, "pagina"),
]


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn").upper()


def num(tok):
    tok = tok.replace(",", ".")
    if "/" in tok:
        a, b = tok.split("/", 1)
        try:
            return float(a) / float(b)
        except (ValueError, ZeroDivisionError):
            return 0.0
    try:
        return float(tok)
    except ValueError:
        return 0.0


def chave_tamanho(desc):
    d = re.sub(r"\(\s*\d+[,.]?\d*\s*\)\s*$", "", desc or "")  # remove "(3,25)" final
    d = re.sub(r"\bIMP\b.*$", "", d)
    toks = re.findall(r"\d+(?:[.,]\d+)?(?:/\d+)?", d)
    return tuple(num(t) for t in toks[:6])


def chave(r):
    mont = sem_acento(r.get("montadora"))
    marca = sem_acento(r.get("marca"))
    return (
        mont == "", mont,
        marca == "", marca,
        sem_acento(r.get("tipo")),
        chave_tamanho(r.get("descricao")),
        sem_acento(r.get("descricao")),
        r.get("ordem", 0),
    )


def aba_nome(n, nome, usados):
    base = f"{n:02d} {nome}"
    base = re.sub(r"[\[\]\*\?/\\:]", "-", base)[:31]
    k, i = base, 2
    while k in usados:
        k = base[:28] + f" {i}"
        i += 1
    usados.add(k)
    return k


HDR_FILL = PatternFill("solid", fgColor="1E1E20")
HDR_FONT = Font(bold=True, color="FFC300")
THIN = Side(style="thin", color="D0D0D0")


def escrever(ws, regs, com_categoria=True):
    cols = COLS if com_categoria else COLS[1:]
    for j, (h, w, _) in enumerate(cols, 1):
        c = ws.cell(row=1, column=j, value=h)
        c.fill, c.font = HDR_FILL, HDR_FONT
        c.alignment = Alignment(vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.row_dimensions[1].height = 30
    for i, r in enumerate(regs, 2):
        for j, (_, _, k) in enumerate(cols, 1):
            v = r.get(k, "")
            if k == "foto":
                if v:
                    c = ws.cell(row=i, column=j, value="ver foto")
                    c.hyperlink = v
                    c.font = Font(color="0563C1", underline="single")
                else:
                    ws.cell(row=i, column=j, value="sem foto")
                continue
            c = ws.cell(row=i, column=j, value=v)
            if k == "codigo":
                c.number_format = "@"
            c.alignment = Alignment(vertical="top", wrap_text=k in ("descricao", "cod_ref", "variacoes", "aplicacao", "info"))
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{max(1, len(regs) + 1)}"


def main():
    caps = {}
    for f in sorted(glob.glob(os.path.join(BASE, "dados", "cap[0-9][0-9].json"))):
        regs = json.load(open(f, encoding="utf-8"))
        if regs:
            caps[regs[0]["cap_num"]] = regs
    wb = Workbook()
    resumo = wb.active
    resumo.title = "Resumo"
    resumo.append(["Nº", "Categoria", "Páginas do PDF", "Produtos (linhas)", "Códigos únicos", "Com foto", "Aba"])
    for c in resumo[1]:
        c.fill, c.font = HDR_FILL, HDR_FONT
    usados = {"Resumo", "Todos os produtos"}
    todos = []
    for n in sorted(caps):
        regs = sorted(caps[n], key=chave)
        todos += regs
        nome = regs[0]["capitulo"]
        ws = wb.create_sheet(aba_nome(n, nome, usados))
        escrever(ws, regs, com_categoria=False)
        pags = [int(x) for r in regs for x in str(r["pagina"]).split(",")]
        resumo.append([n, nome, f"{min(pags)}–{max(pags)}", len(regs), len({r['codigo'] for r in regs}),
                       sum(1 for r in regs if r.get("foto")), ws.title])
    ws = wb.create_sheet("Todos os produtos", 1)
    escrever(ws, todos, com_categoria=True)
    resumo.append([])
    resumo.append(["", "TOTAL", "", len(todos), len({r['codigo'] for r in todos}), sum(1 for r in todos if r.get("foto"))])
    for j, w in enumerate([5, 36, 14, 16, 15, 10, 32], 1):
        resumo.column_dimensions[get_column_letter(j)].width = w
    resumo.append([])
    resumo.append(["", "Ordenação: categoria → marca (montadora) → marca do produto → tipo → tamanho crescente."])
    resumo.append(["", "Fotos: pasta 'Fotos Catálogo 2026', um arquivo por produto, nomeado com a descrição e o código."])
    resumo.append(["", "Produtos repetidos no catálogo (mais de uma marca/categoria) aparecem em cada lugar onde constam."])
    obs = wb.create_sheet("Observações")
    obs.append(["Categoria", "Observação da leitura (cards sem código interno, repetições, marcas não visíveis etc.)"])
    for c in obs[1]:
        c.fill, c.font = HDR_FILL, HDR_FONT
    obs.column_dimensions["A"].width = 32
    obs.column_dimensions["B"].width = 150
    for f in sorted(glob.glob(os.path.join(BASE, "dados", "cap[0-9][0-9]_notas.json"))):
        d = json.load(open(f, encoding="utf-8"))
        for nota in d["notas"]:
            obs.append([f"{d['cap_num']:02d} {d['capitulo']}", nota])
    wb.save(SAIDA)
    print("planilha:", SAIDA, "linhas:", len(todos))


if __name__ == "__main__":
    main()
