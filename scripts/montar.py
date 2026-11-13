"""Monta os registros de produtos de um capítulo a partir da extração bruta + ajustes manuais.

Uso: python montar.py <num_capitulo>

Lê   scripts/capitulos.py (nome e páginas do capítulo)
     <WORK>/raw/pNNN.json (saída do extrair.py)
     ajustes/capNN.py      (correções feitas na revisão visual, opcional)
Gera dados/capNN.json e as fotos em "Fotos Catálogo 2026/NN - Nome/".
"""
import importlib.util
import json
import os
import re
import sys
import unicodedata

import pymupdf as fitz

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "scripts"))
from capitulos import CAPITULOS, PDF, WORK  # noqa: E402

FOTOS_DIR = os.path.join(BASE, "Fotos Catálogo 2026")
CODE_RE = re.compile(r"^\d{5,12}$")

_P = r"^[\s»•*\-–>]*"
LBL_REF = re.compile(_P + r"(REF\b|REF\.|REFER|ORIG|C[ÓO]D|SUBST|OEM|N[º°]\s*ORIG|BALC)", re.I)
LBL_SIM = re.compile(_P + r"(SIMILAR|C[ÓO]D(IGO)?\.?\s+SIMILAR|CONVERS|EQUIVAL|INTERCAMB|OUTRAS\s+REF)", re.I)
LBL_APL = re.compile(_P + r"(APLICA|COMPAT|VE[IÍ]CULO)", re.I)


def norm_txt(s):
    return re.sub(r"\s+", " ", s).strip()


def safe_name(s, maxlen=120):
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r'[\\/:*?"<>|]+', "-", s)
    s = re.sub(r"\s+", " ", s).strip().strip(".")
    return s[:maxlen].strip()


def merge_codes(line):
    """Une spans vermelhos numéricos adjacentes (ex.: '76 800' + '1680')."""
    out = []
    for s in line:
        if out and s["red"] and out[-1]["red"] and re.fullmatch(r"[\d ]+", out[-1]["t"]) and re.fullmatch(r"[\d ]+", s["t"]) and s["x"] - out[-1]["x1"] < 6:
            out[-1] = dict(out[-1], t=out[-1]["t"] + s["t"], x1=s["x1"])
        else:
            out.append(dict(s))
    for s in out:
        if s["red"] and re.fullmatch(r"[\d ]+", s["t"]):
            s["t"] = s["t"].replace(" ", "")
    return out


def is_code(s):
    return s["red"] and CODE_RE.match(s["t"])


def line_text(line):
    return norm_txt(" ".join(s["t"] for s in line))


def classify_info(lines_txt):
    """Separa linhas de informação em ref / similares / aplicação / outras."""
    ref, sim, apl, info = [], [], [], []
    cur = None
    for t in lines_txt:
        head = t[:40]
        if LBL_SIM.search(head):
            cur = sim
        elif LBL_APL.search(head):
            cur = apl
        elif LBL_REF.search(head):
            cur = ref
            ref.append(t)
            # "REF: 00973" já traz o valor: as linhas seguintes não são referência (salvo continuação com "/")
            if re.search(r":\s*\S", t) and not t.rstrip().endswith("/"):
                cur = None
            continue
        elif cur is not None and (t.endswith(":") or len(t) > 60):
            cur = None
        (cur if cur is not None else info).append(t)
    return ref, sim, apl, info


MONT_KW = [
    (r"\bVOLVO\b", "Volvo"), (r"\bSCANIA\b|\bSC\b", "Scania"), (r"MERCEDES|\bMBB?\b|\bM\.?B\.?\b", "Mercedes-Benz"),
    (r"\bVW\b|VOLKSWAGEN", "Volkswagen"), (r"\bFORD\b", "Ford"), (r"\bIVECO\b", "Iveco"), (r"\bDAF\b", "DAF"),
    (r"\bMAN\b", "MAN"), (r"\bAGRALE\b", "Agrale"), (r"\bRANDON\b", "Randon"), (r"\bGUERRA\b", "Guerra"),
    (r"\bFACCHINI\b", "Facchini"), (r"\bNOMA\b", "Noma"), (r"\bLIBRELATO\b", "Librelato"), (r"\bKRONE\b", "Krone"),
]


def montadora_texto(desc):
    out = []
    for pat, nome in MONT_KW:
        if re.search(pat, desc or "", re.I) and nome not in out:
            out.append(nome)
    return ", ".join(out)


_REF_LBL = re.compile(r"^\s*(Refer[êe]ncias?:?|REF\b\.?\s*(ORIGINAL|ORIG)?\b\.?\s*:?|C[ÓO]D(IGO)?\.?\s*(DE\s+F[ÁA]BRICA|ORIG(INAL)?)\.?\s*:?|Subst\.\s*o\s*c[óo]d\.\s*original:?|C[óo]digos?\s+originais:?|Original:?)\s*", re.I)


def limpar_ref(t):
    partes = [p.strip() for p in (t or "").split(" / ")]
    out = []
    for p in partes:
        q = _REF_LBL.sub("", p).strip(" :/")
        if q:
            out.append(q)
    return " / ".join(out)


def limpar_apl(t):
    t = re.sub(r"\s*/\s*-\s*", ", ", t or "")
    t = re.sub(r"^\s*(Aplica[çc][ãa]o|Aplica[çc][õo]es|APLICA[ÇC][ÃA]O|Ve[íi]culos?)\s*:?\s*(/|,)?\s*", "", t, flags=re.I)
    t = re.sub(r"(Ve[íi]culos?|Aplica[çc][ãa]o)\s*:\s*,", r"\1:", t, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip(" ,/")
    return t


def tipo_auto(desc, tipos):
    d = desc or ""
    for pat, t in tipos:
        if re.search(pat, d, re.I):
            return t
    w = re.sub(r"^[\d\s\-–]+", "", d).split()
    return w[0].upper() if w else ""


def load_ajustes(n):
    path = os.path.join(BASE, "ajustes", f"cap{n:02d}.py")
    if not os.path.exists(path):
        return {}, [], [], [], set()
    spec = importlib.util.spec_from_file_location(f"aj{n}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "AJ", {}), getattr(mod, "ADD", []), getattr(mod, "TIPOS", []), getattr(mod, "NOTAS", []), set(getattr(mod, "MANUAIS", set()))


def photo_spec(card):
    """Define a foto do card: {'xref': n} para extrair a imagem original, ou {'rect': [...]} para renderizar a região."""
    crect = fitz.Rect(card["rect"])
    imgs = []
    for i in card["images"]:
        r = fitz.Rect(i["bbox"]) & crect
        if r.is_empty or (r.width < 30 and r.height < 30):
            continue
        imgs.append((r, i))
    if not imgs:
        return None
    mx = max(r.width * r.height for r, _ in imgs)
    big = [(r, i) for r, i in imgs if r.width * r.height >= 0.2 * mx]
    if len(big) == 1:
        r, i = big[0]
        tf = i.get("tf") or [1, 0, 0, 1]
        if i["xref"] > 0 and abs(tf[1]) < 1e-3 and abs(tf[2]) < 1e-3 and tf[0] > 0 and tf[3] > 0:
            return {"xref": i["xref"], "rect": [round(v, 1) for v in r]}
    u = fitz.Rect(big[0][0])
    for r, _ in big[1:]:
        u |= r
    return {"rect": [round(v, 1) for v in u]}


def salvar_foto(doc, pno, spec, path):
    from PIL import Image
    import io
    if spec.get("xref"):
        try:
            pix = fitz.Pixmap(doc, spec["xref"])
            info = doc.extract_image(spec["xref"])
            smask = info.get("smask", 0)
            if pix.colorspace and pix.colorspace.n not in (1, 3):
                pix = fitz.Pixmap(fitz.csRGB, pix)
            if pix.alpha:
                pix = fitz.Pixmap(pix, 0)
            img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
            if smask:
                m = fitz.Pixmap(doc, smask)
                mask = Image.open(io.BytesIO(m.tobytes("png"))).convert("L").resize(img.size)
                bg = Image.new("RGB", img.size, "white")
                bg.paste(img, (0, 0), mask)
                img = bg
            if img.width > 1400 or img.height > 1400:
                img.thumbnail((1400, 1400))
            elif max(img.size) < 400 and min(img.size) >= 20:  # imagem muito pequena no PDF: amplia para uso
                f = 400 / max(img.size)
                img = img.resize((round(img.width * f), round(img.height * f)), Image.LANCZOS)
            if img.width >= 40 and img.height >= 40:
                img.save(path, "JPEG", quality=88)
                return
        except Exception:
            pass
    # renderiza a região sem os textos
    tmp = fitz.open()
    tmp.insert_pdf(doc, from_page=pno - 1, to_page=pno - 1)
    pg = tmp[0]
    for b in pg.get_text("dict")["blocks"]:
        if b.get("type") == 0:
            pg.add_redact_annot(fitz.Rect(b["bbox"]))
    pg.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE)
    pix = pg.get_pixmap(dpi=170, clip=fitz.Rect(spec["rect"]))
    pix.save(path, jpg_quality=88)


def build_card(page, card):
    lines = [merge_codes(l) for l in card["lines"]]
    codes_pos = [(li, si) for li, l in enumerate(lines) for si, s in enumerate(l) if is_code(s)]
    recs = []
    if not codes_pos:
        return recs, lines
    # tamanho típico das linhas
    sizes = [s["size"] for l in lines for s in l if not s["red"]]
    # modo lista: códigos com texto à direita na mesma linha
    with_right = 0
    for li, si in codes_pos:
        rest = [s for s in lines[li][si + 1:] if not is_code(s)]
        if rest and not rest[0]["red"]:
            with_right += 1
    list_mode = len(codes_pos) >= 2 and with_right >= max(1, len(codes_pos) * 0.5)
    used = set()
    if list_mode:
        row_sizes = []
        for li, si in codes_pos:
            desc_spans = []
            for s in lines[li][si + 1:]:
                if is_code(s):
                    break
                desc_spans.append(s)
            row_sizes += [s["size"] for s in desc_spans]
        rs = sorted(row_sizes)[len(row_sizes) // 2] if row_sizes else 10
        code_lines = {li for li, _ in codes_pos}
        title = None
        titles_at = {}
        for li, l in enumerate(lines):
            if li not in code_lines and max(s["size"] for s in l) >= rs * 1.35:
                if all(s["red"] for s in l) and line_text(l).isupper() and not any(ch.isdigit() for ch in line_text(l)):
                    title = line_text(l)
                elif not all(s["red"] for s in l):
                    title = line_text([s for s in l if not s["red"]])
                else:
                    titles_at[li] = title
                    continue
                used.add(li)
            titles_at[li] = title
        first_title = next((t for t in titles_at.values() if t), None)
        for li, si in codes_pos:
            desc_spans = []
            for s in lines[li][si + 1:]:
                if is_code(s):
                    break
                desc_spans.append(s)
            used.add(li)
            recs.append({
                "codigo": lines[li][si]["t"],
                "descricao": line_text(desc_spans),
                "tipo": titles_at.get(li) or first_title or "",
                "_y": lines[li][si]["y"],
                "_x": lines[li][si]["x"],
            })
        extra = [line_text(l) for li, l in enumerate(lines) if li not in used]
        ref, sim, apl, info = classify_info(extra)
        for r in recs:
            r.update(cod_ref=" / ".join(ref), variacoes=" / ".join(sim), aplicacao=" / ".join(apl), info=" / ".join(info))
        return recs, lines

    # modo card individual (um ou mais códigos sem descrição ao lado)
    li0, si0 = codes_pos[0]
    desc_parts = []
    right = [s for s in lines[li0][si0 + 1:] if not s["red"]]
    if right:
        desc_parts.append(line_text(right))
    used.add(li0)
    # linhas seguintes com o mesmo "peso" de fonte e sem rótulos
    cand = [(li, l) for li, l in enumerate(lines) if li != li0 and not any(is_code(s) for s in l)]
    non_lbl = [(li, l) for li, l in cand if not (LBL_REF.search(line_text(l)[:30]) or LBL_SIM.search(line_text(l)[:30]) or LBL_APL.search(line_text(l)[:30]))]
    nonred = [(li, l) for li, l in non_lbl if not all(s["red"] for s in l)]
    if nonred:
        maxs = max(max(s["size"] for s in l) for _, l in nonred)
        desc_lines = [li for li, l in nonred if max(s["size"] for s in l) >= maxs * 0.8]
        # mantém só um bloco contíguo
        block = []
        for li in sorted(desc_lines):
            if not block or li - block[-1] <= 1:
                block.append(li)
            else:
                break
        if not desc_parts or (lines[block[0]][0]["size"] >= 8 if block else False):
            for li in block:
                desc_parts.append(line_text([s for s in lines[li] if not s["red"]]))
                used.add(li)
    other_codes = [lines[li][si]["t"] for li, si in codes_pos[1:]]
    for li, si in codes_pos[1:]:
        if len(lines[li]) == 1:
            used.add(li)
    extra = [line_text(l) for li, l in enumerate(lines) if li not in used]
    ref, sim, apl, info = classify_info(extra)
    desc = norm_txt(" ".join(desc_parts))
    recs.append({
        "codigo": lines[li0][si0]["t"],
        "descricao": desc,
        "tipo": "",
        "cod_ref": " / ".join(ref),
        "variacoes": " / ".join(sim),
        "aplicacao": " / ".join(apl),
        "info": " / ".join(info),
        "_outros_codigos": other_codes,
        "_y": lines[li0][si0]["y"],
        "_x": lines[li0][si0]["x"],
    })
    return recs, lines


def main():
    n = int(sys.argv[1])
    cap = CAPITULOS[n]
    nome, p0, p1 = cap["nome"], cap["ini"], cap["fim"]
    AJ, ADD, TIPOS, NOTAS, MANUAIS = load_ajustes(n)
    doc = fitz.open(PDF)
    pasta = os.path.join(FOTOS_DIR, f"{n:02d} - {safe_name(nome)}")
    os.makedirs(pasta, exist_ok=True)
    for fn in os.listdir(pasta):  # regera as fotos do capítulo do zero
        if fn.lower().endswith(".jpg"):
            os.remove(os.path.join(pasta, fn))
    out, alertas = [], []
    for pno in range(p0, p1 + 1):
        raw = json.load(open(os.path.join(WORK, "raw", f"p{pno:03d}.json"), encoding="utf-8"))
        if pno in MANUAIS:  # página lida e registrada manualmente (ADD)
            continue
        for card in raw["cards"]:
            key = f"{pno}.{card['id']}"
            aj = AJ.get(key, {})
            if aj.get("skip"):
                continue
            recs, _ = build_card(pno, card)
            if "records" in aj:  # registros escritos manualmente para o card
                recs = [dict(r) for r in aj["records"]]
            if not recs:
                if card["id"] != 0 and (card["images"] or card["lines"]):
                    alertas.append(f"p{pno} card {card['id']}: sem código vermelho (imgs={len(card['images'])}, linhas={len(card['lines'])})")
                continue
            prect = aj["foto"] if "foto" in aj else photo_spec(card)
            for i, r in enumerate(recs):
                r.setdefault("tipo", "")
                for k in ("cod_ref", "variacoes", "aplicacao", "info", "marca", "montadora"):
                    r.setdefault(k, "")
                for k, v in aj.items():
                    if k in ("skip", "records", "foto", "por_codigo"):
                        continue
                    if k.startswith("+"):  # acrescenta ao campo
                        f = k[1:]
                        r[f] = norm_txt((r.get(f, "") + " / " + v) if r.get(f) else v)
                    elif not (k in r and k in ("descricao",) and "records" in aj):
                        r[k] = v
                for k, v in aj.get("por_codigo", {}).get(r["codigo"], {}).items():
                    r[k] = v
                r["capitulo"] = nome
                r["cap_num"] = n
                r["pagina"] = pno
                r["card"] = card["id"]
                r["ordem"] = pno * 1000 + card["id"] * 50 + i
                r["foto_spec"] = r.get("foto_spec", prect)
                out.append(r)
    for r in ADD:
        r = dict(r)
        for k in ("tipo", "cod_ref", "variacoes", "aplicacao", "info", "marca", "montadora"):
            r.setdefault(k, "")
        r.update(capitulo=nome, cap_num=n)
        r.setdefault("ordem", r["pagina"] * 1000 + r.get("card", 0) * 50 + 49)
        out.append(r)

    # pós-processamento: tipo, montadora pelo texto, limpeza de rótulos
    for r in out:
        if r.pop("_manual", False):
            pass
        if not r.get("tipo"):
            r["tipo"] = tipo_auto(r["descricao"], TIPOS)
        if not r.get("montadora"):
            r["montadora"] = montadora_texto(r["descricao"])
        r["cod_ref"] = limpar_ref(r.get("cod_ref"))
        r["aplicacao"] = limpar_apl(r.get("aplicacao"))

    # fotos
    nomes_usados = {}
    for r in out:
        if not r.get("foto_spec"):
            r["foto"] = ""
            r.pop("foto_spec", None)
            continue
        base = safe_name(r["descricao"] or r["tipo"], 100) + " - " + safe_name(r["codigo"])
        k = base.lower()
        if k in nomes_usados:
            nomes_usados[k] += 1
            base = f"{base} ({nomes_usados[k]})"
        else:
            nomes_usados[k] = 1
        fn = base + ".jpg"
        salvar_foto(doc, r["pagina"], r.pop("foto_spec"), os.path.join(pasta, fn))
        r["foto"] = os.path.relpath(os.path.join(pasta, fn), BASE).replace("\\", "/")
    # limpa campos auxiliares
    for r in out:
        for k in [k for k in r if k.startswith("_")]:
            r.pop(k)
    os.makedirs(os.path.join(BASE, "dados"), exist_ok=True)
    with open(os.path.join(BASE, "dados", f"cap{n:02d}.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    with open(os.path.join(BASE, "dados", f"cap{n:02d}_notas.json"), "w", encoding="utf-8") as f:
        json.dump({"capitulo": nome, "cap_num": n, "notas": NOTAS}, f, ensure_ascii=False, indent=1)
    print(f"Capítulo {n} - {nome}: {len(out)} registros, {sum(1 for r in out if r['foto'])} com foto")
    for a in alertas:
        print("ALERTA", a)


if __name__ == "__main__":
    main()
