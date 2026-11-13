"""Mostra os registros montados de um capítulo (opcionalmente só algumas páginas): python ver.py <cap> [pag ...]"""
import json, os, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n = int(sys.argv[1]); pags = {int(x) for x in sys.argv[2:]}
for r in json.load(open(os.path.join(BASE, "dados", f"cap{n:02d}.json"), encoding="utf-8")):
    if pags and not pags & {int(x) for x in str(r["pagina"]).split(",")}:
        continue
    print(f"{r['pagina']}.{r['card']} {r['codigo']} | T:{r['tipo']} | D:{r['descricao']} | REF:{r['cod_ref']} | VAR:{r['variacoes']} | APL:{r['aplicacao']} | INF:{r['info']} | M:{r['montadora']} | MP:{r['marca']}{'' if r['foto'] else ' | SEM FOTO'}")
