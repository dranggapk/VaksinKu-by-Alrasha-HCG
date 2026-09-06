#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inline the latin subsets of the two brand faces as data: URIs so the
standalone HTML renders with the real brand typography with no network."""
import base64, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
CSS_URL = ("https://fonts.googleapis.com/css2?"
           "family=Baloo+2:wght@600;700;800"
           "&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap")
# Google serves one variable woff2 per family+subset, so one @font-face with a
# weight range replaces the per-weight blocks it emits.
WEIGHT_RANGE = {"Baloo 2": "600 800", "Plus Jakarta Sans": "400 800"}


def fetch(url, binary=False):
    out = subprocess.run(["curl", "-sS", "-m", "40", "-A", UA, url],
                         capture_output=True, check=True)
    return out.stdout if binary else out.stdout.decode("utf-8")


blocks = re.findall(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{[^}]*\})", fetch(CSS_URL))

faces = {}  # family -> (url, unicode_range)
for subset, block in blocks:
    if subset != "latin":
        continue
    family = re.search(r"font-family:\s*'([^']+)'", block).group(1)
    url = re.search(r"src:\s*url\((https://[^)]+\.woff2)\)", block).group(1)
    urange = re.search(r"unicode-range:\s*([^;]+);", block).group(1).strip()
    faces.setdefault(family, (url, urange))

rules = []
for family, (url, urange) in faces.items():
    raw = fetch(url, binary=True)
    b64 = base64.b64encode(raw).decode("ascii")
    print(f"  {family}: {len(raw)/1024:.1f} KB woff2")
    rules.append(
        "@font-face{font-family:'%s';font-style:normal;font-weight:%s;font-display:swap;"
        "src:url(data:font/woff2;base64,%s) format('woff2');unicode-range:%s;}"
        % (family, WEIGHT_RANGE[family], b64, urange)
    )

font_css = "\n".join(rules)
print(f"inline font CSS: {len(font_css)/1024:.0f} KB")

with open(os.path.join(HERE, "vaksinku-app.html"), encoding="utf-8") as f:
    html = f.read()

link_tags = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
             '<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800'
             '&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">')
if link_tags not in html:
    sys.exit("link tags not found — the app template changed, aborting")

html = html.replace(link_tags, "<style>\n" + font_css + "\n</style>")

out_path = os.path.join(HERE, "VaksinKu-App.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)
print("wrote", out_path, f"{os.path.getsize(out_path)/1024:.0f} KB")
