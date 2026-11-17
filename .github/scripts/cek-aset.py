#!/usr/bin/env python3
"""Memastikan semua file lokal yang dirujuk index.html dan fonts/fonts.css benar-benar ada."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WAJIB = ["index.html", "fonts/fonts.css", "vendor/three/three.module.js", "vendor/animejs/anime.esm.min.js"]

hilang = [p for p in WAJIB if not (ROOT / p).is_file()]

html = (ROOT / "index.html").read_text(encoding="utf-8")
rujukan = set(re.findall(r"""["'](\.?/?(?:img|vendor|fonts)/[^"'`\s]+)["']""", html))
for r in sorted(rujukan):
    if "${" in r:  # path dinamis dari JavaScript, tidak bisa dicek statis
        continue
    path = ROOT / r.lstrip("./") if not r.startswith("./") else ROOT / r[2:]
    if r.endswith("/"):
        if not path.is_dir():
            hilang.append(r)
    elif not path.is_file():
        hilang.append(r)

css_dir = ROOT / "fonts"
for u in re.findall(r"url\(['\"]?([^)'\"]+)['\"]?\)", (css_dir / "fonts.css").read_text(encoding="utf-8")):
    if not (css_dir / u).is_file():
        hilang.append(f"fonts/{u}")

# Gambar histologi dipanggil lewat hxImgSrc(id) -> img/hx/<id>.jpg
for id_ in set(re.findall(r"""img:\s*["']([\w-]+)["']""", html)):
    if not (ROOT / "img/hx" / f"{id_}.jpg").is_file() and (ROOT / "img/hx").is_dir():
        hilang.append(f"img/hx/{id_}.jpg")

if hilang:
    print("File yang dirujuk tapi tidak ditemukan:")
    for h in sorted(set(hilang)):
        print("  -", h)
    sys.exit(1)
print(f"OK: {len(rujukan)} rujukan aset di index.html dan semua font ditemukan.")
