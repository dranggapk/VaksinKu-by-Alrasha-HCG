# -*- coding: utf-8 -*-
"""Varian merek aplikasi pasien dari satu kode yang sama.

    python3 build_bundle.py                 → VaksinKu-App.html  (merek bawaan)
    python3 build_bundle.py --merek jasvacc → JasVacc-App.html   (Jasmine MQ Medika)

Varian hanya mengganti tampilan: nama, logo, font, warna, banner, dan kontak merek.
Fitur, jadwal, price list, dan server (/api, /auth) tetap sama, sehingga setiap
perbaikan VaksinKu otomatis ikut ke varian lain. Aset JasVacc ada di jasvacc/
(dibuat src/buat_aset_jasvacc.py).
"""
import base64
import colorsys
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def _data_uri(path):
    tipe = {".png": "image/png", ".webp": "image/webp", ".jpg": "image/jpeg", ".svg": "image/svg+xml"}
    with open(path, "rb") as f:
        return "data:%s;base64,%s" % (tipe[os.path.splitext(path)[1].lower()], base64.b64encode(f.read()).decode("ascii"))


MEREK = {
    "vaksinku": {"keluaran": "VaksinKu-App.html"},
    "jasvacc": {
        "keluaran": "JasVacc-App.html",
        "nama": "JasVacc",
        "oleh": "by Jasmine MQ Medika",
        "kunci_data": "jasvacc.v1",           # data perangkat terpisah dari VaksinKu
        "jalur": "/jasvacc",                  # disajikan di vaksinku.app/jasvacc/
        "klinik": "jasmine-mq", "kota": "bandung",
        "situs": "https://vaksinku.app/jasvacc",
        "brand": {"group": "Jasmine MQ Medika", "instagram": "@jasmine_mqmedika", "website": "jasminemqmedika"},
        "logo_full": "jasvacc/logo-jasvacc.png",
        "logo_mark": "jasvacc/logo-jasvacc-kecil.png",
        "banner": [{
            "gambar": "jasvacc/banner-influenza.webp",
            "alt": "Promo vaksin influenza Vaxigrip Tiv 3 strain: 1 orang Rp300.000, 2 orang Rp500.000, "
                   "3 orang Rp725.000, 4 orang Rp925.000, 5 orang Rp1.100.000.",
            "act": "go", "arg": "booking", "klinik": ["jasmine-mq"],
        }],
        # font dari materi promo Jasmine: judul bulat tebal + teks geometris
        "font_url": ("https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700"
                     "&family=Poppins:wght@400;500;600;700&display=swap"),
        "font_rentang": {"Fredoka": "500 800", "Poppins": "400 800"},
        "font_ganti": {"'Baloo 2'": "'Fredoka'", "Baloo 2": "Fredoka", "Plus Jakarta Sans": "Poppins"},
        "theme_color": "#0F2533",
        # palet poster Jasmine: navy, hijau sage, merah Jasmine, putih
        "token": {
            "--teal": "#6E8F69", "--teal-dark": "#0F2533", "--teal-deep": "#0A1A24",
            "--teal-tint": "#EEF2EB", "--teal-tint2": "#DCE5D6",
            "--magenta": "#EC1D25", "--magenta-dark": "#BE141B", "--magenta-tint": "#FDECEC", "--magenta-tint2": "#FAD4D5",
            "--bg": "#F4F6F2", "--stage-1": "#E9EEE6", "--stage-2": "#DCE5D6",
        },
    },
}


def _ubah_warna(m):
    """Warna toska → navy (gelap) / sage (terang); merah muda-magenta → merah Jasmine.
    Abu-abu dan warna lain dibiarkan."""
    hx = m.group(0)[1:]
    if len(hx) == 3:
        hx = "".join(c * 2 for c in hx)
    r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    deg = h * 360
    if s < 0.22 or l > 0.985:
        return m.group(0)
    if 160 <= deg <= 205:
        if l < 0.42:
            h2, s2, l2 = 203 / 360, 0.55, l * 0.62
        else:
            h2, s2, l2 = 100 / 360, min(s, 0.5) * 0.45, l
    elif deg >= 300 or deg <= 4:
        h2, s2, l2 = 358 / 360, max(s, 0.78), l
    else:
        return m.group(0)
    r2, g2, b2 = colorsys.hls_to_rgb(h2, l2, s2)
    return "#%02X%02X%02X" % (round(r2 * 255), round(g2 * 255), round(b2 * 255))


def terapkan_katalog(cfg, js):
    if "nama" not in cfg:
        return js
    awal = "window.KATALOG="
    data = json.loads(js[len(awal):-1])
    data["brand"].update(cfg["brand"])
    data["logoFull"] = _data_uri(os.path.join(ROOT, cfg["logo_full"]))
    data["logoMark"] = _data_uri(os.path.join(ROOT, cfg["logo_mark"]))
    banner = []
    for b in cfg["banner"]:
        b = dict(b)
        b["gambar"] = _data_uri(os.path.join(ROOT, b["gambar"]))
        banner.append(b)
    data["merek"] = {"nama": cfg["nama"], "banner": banner, "klinik": cfg["klinik"], "kota": cfg["kota"]}
    data["google"]["situs"] = cfg["situs"]
    return awal + json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + ";"


def tulis_privasi(cfg):
    """Kebijakan Privasi untuk jalur varian (nama merek diganti; isi hukumnya sama)."""
    if "nama" not in cfg:
        return
    with open(os.path.join(ROOT, "situs", "privasi.html"), encoding="utf-8") as f:
        s = f.read()
    s = re.sub(r"VaksinKu(?![A-Za-z])", cfg["nama"], s).replace("by Alrasha Health Care Group", cfg["oleh"])
    with open(os.path.join(ROOT, "jasvacc", "privasi.html"), "w", encoding="utf-8") as f:
        f.write(s)


def terapkan_html(cfg, html):
    if "nama" not in cfg:
        return html
    html = html.replace("'vaksinku.v1'", "'%s'" % cfg["kunci_data"])
    # nama merek di teks (bukan nama variabel seperti VaksinKuSinkron)
    html = re.sub(r"VaksinKu(?![A-Za-z])", cfg["nama"], html)
    html = html.replace("by Alrasha Health Care Group", cfg["oleh"])
    for lama, baru in cfg["font_ganti"].items():
        html = html.replace(lama, baru)
    html = re.sub(r"(?<![&\w])#[0-9A-Fa-f]{6}(?![0-9A-Fa-f\w])", _ubah_warna, html)
    token = ":root{" + "".join("%s:%s;" % kv for kv in cfg["token"].items()) + "}"
    html = html.replace("</head>", "<style>%s</style>\n</head>" % token, 1)
    html = re.sub(r'<meta name="theme-color" content="[^"]*">', '<meta name="theme-color" content="%s">' % cfg["theme_color"], html)
    j = cfg["jalur"]
    html = html.replace('href="/manifest.json"', 'href="%s/manifest.json"' % j)
    html = html.replace('href="/ikon/', 'href="%s/ikon/' % j)
    return html
