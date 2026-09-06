#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merakit aplikasi VaksinKu menjadi satu berkas HTML mandiri.

Menggabungkan app/index.html + app/styles.css + app/app.js + katalog
(dari data_katalog.py) + logo dan font sebagai data URI, sehingga berkas
hasilnya bisa dibuka langsung di browser tanpa internet.

    python3 build_bundle.py [--tanpa-font]
"""
import base64
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
APP = os.path.join(ROOT, "app")
sys.path.insert(0, HERE)

import data_katalog as D  # noqa: E402

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
FONT_CSS_URL = ("https://fonts.googleapis.com/css2?"
                "family=Baloo+2:wght@600;700;800"
                "&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap")
WEIGHT_RANGE = {"Baloo 2": "600 800", "Plus Jakarta Sans": "400 800"}


# --------------------------------------------------------------- katalog → JS
def usia_ke_bulan(teks):
    """'0 bulan' → 0 · '6 tahun 3 bulan' → 75 · '11–18 tahun' → 132."""
    t = teks.lower().replace("–", "-")
    awal = t.split("-")[0].strip() if "-" in t.split(" ")[0] + " " else t
    m = re.search(r"(\d+)\s*tahun(?:\s*(\d+)\s*bulan)?", t)
    if m:
        return int(m.group(1)) * 12 + int(m.group(2) or 0)
    m = re.search(r"(\d+)\s*bulan", t)
    return int(m.group(1)) if m else 0


def rentang_tahun(teks):
    """'19 – 21 tahun' → (19, 21) · '60 tahun ke atas' → (60, 200)."""
    angka = [int(x) for x in re.findall(r"\d+", teks)]
    if "ke atas" in teks.lower():
        return angka[0], 200
    if len(angka) >= 2:
        return angka[0], angka[1]
    return angka[0], angka[0]


def b64_file(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def katalog_js():
    harga = []
    for no, kategori, sediaan, merk, spes, umum in D.HARGA:
        harga.append({
            "id": "v%d-%d" % (int(no), len(harga)),
            "kategori": kategori, "sediaan": sediaan, "merk": merk,
            "spesialis": "" if spes == "—" else spes, "umum": umum,
        })

    jadwal_anak = [{
        "usia": usia, "badge": badge or "", "usiaBulan": usia_ke_bulan(usia), "items": items,
    } for usia, badge, items in D.JADWAL_ANAK]

    jadwal_dewasa = []
    for usia, keys in D.JADWAL_DEWASA:
        lo, hi = rentang_tahun(usia)
        jadwal_dewasa.append({
            "usia": usia, "minTahun": lo, "maxTahun": hi,
            "items": [{"nama": D.dosis(k)[0], "dosis": D.dosis(k)[1]} for k in keys],
        })

    data = {
        "brand": {
            "tagline": D.BRAND["tagline"], "callCenter": D.BRAND["call_center"],
            "callCenterLabel": D.BRAND["call_center_label"], "instagram": D.BRAND["instagram"],
            "website": D.BRAND["website"], "group": D.BRAND["group"],
        },
        "pilar": D.PILAR,
        "layanan": D.LAYANAN,
        "termasuk": D.TERMASUK,
        "harga": harga,
        "hargaInternasional": [
            {"nama": n, "harga": hrg, "coret": coret} for n, hrg, coret in D.HARGA_INTERNASIONAL
        ],
        "paketTriple": {
            "nama": D.PAKET_TRIPLE["nama"], "isi": D.PAKET_TRIPLE["isi"],
            "harga": D.PAKET_TRIPLE["harga"], "coret": D.PAKET_TRIPLE["coret"],
        },
        "jadwalAnak": jadwal_anak,
        "jadwalDewasa": jadwal_dewasa,
        "catatanDewasa": D.JADWAL_DEWASA_CATATAN,
        "pranikahVaksin": D.JADWAL_PRANIKAH_VAKSIN,
        "pranikahWaktu": D.JADWAL_PRANIKAH_WAKTU,
        "lansia": D.JADWAL_LANSIA,
        "internasionalWajib": D.VAKSIN_INTERNASIONAL_WAJIB,
        "internasionalTambahan": D.VAKSIN_INTERNASIONAL_TAMBAHAN,
        "dokter": D.DOKTER,
        "klinik": D.KLINIK,
        "alurReservasi": D.ALUR_RESERVASI,
        "logoMark": "data:image/png;base64," + b64_file(os.path.join(HERE, "vaksinku-logo-mark.png")),
        "logoFull": "data:image/png;base64," + b64_file(os.path.join(HERE, "vaksinku-logo.png")),
    }
    js = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return "window.KATALOG=" + js.replace("</", "<\\/") + ";"


# --------------------------------------------------------------- font
def font_css():
    out = subprocess.run(["curl", "-sS", "-m", "40", "-A", UA, FONT_CSS_URL],
                         capture_output=True, check=True).stdout.decode("utf-8")
    blocks = re.findall(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{[^}]*\})", out)
    faces, rules = {}, []
    for subset, block in blocks:
        if subset != "latin":
            continue
        family = re.search(r"font-family:\s*'([^']+)'", block).group(1)
        url = re.search(r"src:\s*url\((https://[^)]+\.woff2)\)", block).group(1)
        urange = re.search(r"unicode-range:\s*([^;]+);", block).group(1).strip()
        faces.setdefault(family, (url, urange))
    for family, (url, urange) in faces.items():
        raw = subprocess.run(["curl", "-sS", "-m", "40", "-A", UA, url],
                             capture_output=True, check=True).stdout
        print("  %s: %.1f KB" % (family, len(raw) / 1024))
        rules.append(
            "@font-face{font-family:'%s';font-style:normal;font-weight:%s;font-display:swap;"
            "src:url(data:font/woff2;base64,%s) format('woff2');unicode-range:%s;}"
            % (family, WEIGHT_RANGE[family], base64.b64encode(raw).decode("ascii"), urange)
        )
    return "\n".join(rules)


# --------------------------------------------------------------- rakit
def main():
    tanpa_font = "--tanpa-font" in sys.argv
    with open(os.path.join(APP, "index.html"), encoding="utf-8") as f:
        html = f.read()
    with open(os.path.join(APP, "styles.css"), encoding="utf-8") as f:
        css = f.read()
    with open(os.path.join(APP, "app.js"), encoding="utf-8") as f:
        js = f.read()

    if tanpa_font:
        fonts = ('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
                 '<link href="' + FONT_CSS_URL + '" rel="stylesheet">')
    else:
        print("mengambil font...")
        fonts = "<style>\n" + font_css() + "\n</style>"

    html = html.replace("<!--FONTS-->", fonts)
    html = html.replace("/*STYLES*/", css)
    html = html.replace("/*KATALOG*/", katalog_js())
    html = html.replace("/*APP*/", js)

    out = os.path.join(ROOT, "VaksinKu-App.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote %s — %.0f KB" % (out, os.path.getsize(out) / 1024))


if __name__ == "__main__":
    main()
