#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merakit dashboard manajemen VaksinKu menjadi satu berkas HTML mandiri.

Memakai katalog, logo, dan font yang sama dengan aplikasi pasien
(lihat build_bundle.py), lalu menggabungkannya dengan sumber di admin/.

    python3 build_admin.py [--tanpa-font]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ADMIN = os.path.join(ROOT, "admin")
sys.path.insert(0, HERE)

import build_bundle as B  # noqa: E402


def main():
    tanpa_font = "--tanpa-font" in sys.argv
    with open(os.path.join(ADMIN, "index.html"), encoding="utf-8") as f:
        html = f.read()
    with open(os.path.join(ADMIN, "styles.css"), encoding="utf-8") as f:
        css = f.read()
    with open(os.path.join(ADMIN, "app.js"), encoding="utf-8") as f:
        js = f.read()

    if tanpa_font:
        fonts = ('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
                 '<link href="' + B.FONT_CSS_URL + '" rel="stylesheet">')
    else:
        print("mengambil font...")
        fonts = "<style>\n" + B.font_css() + "\n</style>"

    html = html.replace("<!--FONTS-->", fonts)
    html = html.replace("/*STYLES*/", css)
    html = html.replace("/*KATALOG*/", B.katalog_js())
    html = html.replace("/*APP*/", js)

    out = os.path.join(ROOT, "VaksinKu-Dashboard.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote %s — %.0f KB" % (out, os.path.getsize(out) / 1024))


if __name__ == "__main__":
    main()
