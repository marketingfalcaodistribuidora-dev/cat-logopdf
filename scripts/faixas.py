"""Lista títulos (fonte >= N) e códigos vermelhos com posição: python faixas.py <pag> [fonte_min]"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from capitulos import WORK  # noqa: E402

p = int(sys.argv[1])
fm = float(sys.argv[2]) if len(sys.argv) > 2 else 15.5
raw = json.load(open(os.path.join(WORK, "raw", f"p{p:03d}.json"), encoding="utf-8"))
spans = [s for c in raw["cards"] for ln in c["lines"] for s in ln]
spans.sort(key=lambda s: (round(s["y"]), s["x"]))
for s in spans:
    cod = s["red"] and re.fullmatch(r"\d{5,12}", s["t"].replace(" ", ""))
    if s["size"] >= fm or cod:
        print(f"{'COD ' if cod else '    '}y={s['y']:6.1f} x={s['x']:6.1f}-{s['x1']:6.1f} sz={s['size']:4.1f} {s['t']}")
