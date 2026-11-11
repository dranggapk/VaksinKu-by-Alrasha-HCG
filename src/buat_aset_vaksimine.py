#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Membuat aset merek Vaksimine di vaksimine/ (dipakai build_bundle.py --merek vaksimine).

Sumber: vaksimine/sumber-logo.png (logo Vaksimine by Jasmine MQ Medika),
vaksimine/logo-jasmine.png (logo klinik) dan vaksimine/sumber-poster.jpg (materi promo
influenza Jasmine). Banner digambar lewat Chromium headless dengan font Fredoka & Poppins.

    python3 src/buat_aset_vaksimine.py
"""
import base64
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_bundle as B  # noqa: E402
import merek as M  # noqa: E402

J = os.path.join(ROOT, "vaksimine")
CHROME = "/opt/pw-browsers/chromium"
NAVY, MERAH, SAGE = "#032543", "#DF0111", "#C9D4C4"
CFG = M.MEREK["vaksimine"]
FONTS = B.font_css(CFG["font_url"], CFG["font_rentang"])


def uri(path):
    return M._data_uri(path)


def potret(html, w, h, keluar, transparan=True):
    """Render HTML ke PNG ukuran w×h (jendela dibuat lebih tinggi lalu dipotong)."""
    d = tempfile.mkdtemp()
    f = os.path.join(d, "a.html")
    with open(f, "w", encoding="utf-8") as fh:
        fh.write('<!doctype html><html><head><meta charset="utf-8"><style>%s</style><style>'
                 'html,body{margin:0;background:%s;}</style></head><body>%s</body></html>'
                 % (FONTS, "transparent" if transparan else "#fff", html))
    png = os.path.join(d, "a.png")
    arg = [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
           "--window-size=%d,%d" % (w, h + 200), "--virtual-time-budget=2000", "--screenshot=" + png, "file://" + f]
    if transparan:
        arg.insert(4, "--default-background-color=00000000")
    subprocess.run(arg, capture_output=True, timeout=120)
    im = Image.open(png).convert("RGBA").crop((0, 0, w, h))
    return im


def pangkas(im, pad=8):
    im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())
    c = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    c.paste(im, (pad, pad))
    return c


def tanpa_latar(path):
    """Latar putih logo dijadikan transparan; tepi huruf tetap halus."""
    im = np.asarray(Image.open(path).convert("RGB")).astype(float)
    d = 255 - im.min(axis=2)
    a = np.clip((d - 14) / 40, 0, 1)
    rgb = np.clip(np.where(a[..., None] > 0, (im - 255 * (1 - a[..., None])) / np.maximum(a[..., None], 1e-3), 255), 0, 255)
    return Image.fromarray(np.dstack([rgb, a * 255]).astype(np.uint8), "RGBA")


def main():
    logo = uri(os.path.join(J, "logo-jasmine.png"))   # logo klinik, untuk banner promo
    mentah = tanpa_latar(os.path.join(J, "sumber-logo.png"))

    # logo lengkap: perisai + Vaksimine + by Jasmine MQ Medika
    im = pangkas(mentah)
    im.thumbnail((760, 760), Image.LANCZOS)
    im.save(os.path.join(J, "logo-vaksimine.png"), optimize=True)

    # logo kecil (kepala beranda): tanpa baris "by Jasmine MQ Medika"
    a = np.array(mentah)
    a[450:, 760:, 3] = 0
    im = pangkas(Image.fromarray(a), 4)
    im.thumbnail((520, 520), Image.LANCZOS)
    im.save(os.path.join(J, "logo-vaksimine-kecil.png"), optimize=True)

    # perisai saja, untuk ikon layar utama
    a = np.array(mentah)
    a[:, 760:, 3] = 0
    perisai = pangkas(Image.fromarray(a), 0)
    p_path = os.path.join(tempfile.mkdtemp(), "perisai.png")
    perisai.save(p_path)
    logo_perisai = uri(p_path)

    # ikon layar utama: oval Jasmine di atas putih, sage lembut di bawah
    ikon = potret('<div style="width:1024px;height:1024px;position:relative;background:#fff;overflow:hidden;">'
                  '<div style="position:absolute;left:-10%%;right:-10%%;bottom:-38%%;height:62%%;border-radius:50%%;background:%s;opacity:.55;"></div>'
                  '<img src="%s" style="position:absolute;left:50%%;top:50%%;height:700px;transform:translate(-50%%,-50%%);"></div>' % ("#DCE4EC", logo_perisai),
                  1024, 1024, None, transparan=False).convert("RGB")
    os.makedirs(os.path.join(J, "ikon"), exist_ok=True)
    for nama, uk in (("ikon-512", 512), ("ikon-192", 192), ("apple-touch-icon", 180), ("favicon-32", 32)):
        ikon.resize((uk, uk), Image.LANCZOS).save(os.path.join(J, "ikon", nama + ".png"), optimize=True)
    with open(os.path.join(J, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({
            "name": "Vaksimine by Jasmine MQ Medika", "short_name": "Vaksimine",
            "description": "Jadwal vaksinasi keluarga, rekam medis, dan reservasi vaksin di Jasmine MQ Medika.",
            "lang": "id", "start_url": "/vaksimine/", "scope": "/vaksimine/", "display": "standalone",
            "orientation": "portrait", "background_color": "#FFFFFF", "theme_color": NAVY,
            "icons": [{"src": "/vaksimine/ikon/ikon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
                      {"src": "/vaksimine/ikon/ikon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
                      {"src": "/vaksimine/ikon/ikon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
        }, f, ensure_ascii=False, indent=2)

    # banner promo influenza (1200×540) dari poster Jasmine
    poster = Image.open(os.path.join(J, "sumber-poster.jpg")).convert("RGB")
    s = poster.width / 923
    keluarga = poster.crop((0, int(880 * s), int(470 * s), int(1478 * s)))
    kel_path = os.path.join(tempfile.mkdtemp(), "k.jpg")
    keluarga.save(kel_path, quality=90)
    harga = [("1 orang", "300.000"), ("2 orang", "500.000"), ("3 orang", "725.000"), ("4 orang", "925.000"), ("5 orang", "1.100.000")]
    sel = "".join('<div style="display:flex;justify-content:space-between;gap:10px;padding:6px 2px;border-bottom:1px solid #E6E6E6;">'
                  '<span>%s</span><b>Rp%s</b></div>' % x for x in harga)
    banner = potret(
        '<div style="width:1200px;height:540px;position:relative;overflow:hidden;font-family:Poppins;color:%s;'
        'background:linear-gradient(135deg,#D5DECF 0%%,#C4D0BC 100%%);">'
        '<img src="%s" style="position:absolute;left:0;bottom:0;height:540px;">'
        '<div style="position:absolute;left:478px;top:30px;right:36px;">'
        '<img src="%s" style="height:58px;">'
        '<div style="font-family:Fredoka;font-weight:700;font-size:40px;line-height:1;margin-top:8px;">Promo Vaksin</div>'
        '<div style="font-family:Fredoka;font-weight:700;font-size:92px;line-height:.95;letter-spacing:-1px;'
        'text-shadow:3px 3px 0 #fff,-3px -3px 0 #fff,3px -3px 0 #fff,-3px 3px 0 #fff;">Influenza</div>'
        '<div style="display:flex;gap:20px;margin-top:14px;align-items:flex-start;">'
        '<div style="background:#fff;border-radius:20px;padding:10px 16px 8px;width:420px;font-size:18px;box-shadow:0 6px 18px rgba(15,37,51,.12);">'
        '<div style="background:%s;color:#fff;border-radius:12px;padding:6px 12px;margin-bottom:4px;font-weight:600;font-size:19px;white-space:nowrap;">'
        'Vaxigrip Tiv <span style="font-weight:400;">· 3 strain · per paket</span></div>'
        '<div style="display:grid;grid-template-columns:1fr 1fr;column-gap:18px;">%s</div></div>'
        '<div style="width:230px;font-size:17px;line-height:1.45;padding-top:4px;">Sudah termasuk <b>administrasi, alat kesehatan &amp; jasa dokter</b>'
        '<div style="margin-top:16px;display:inline-block;background:%s;color:#fff;font-weight:600;border-radius:999px;padding:10px 20px;white-space:nowrap;">'
        'Reservasi sekarang</div></div></div></div></div>'
        % (NAVY, uri(kel_path), logo, NAVY, sel, MERAH), 1200, 540, None, transparan=False)
    banner.convert("RGB").save(os.path.join(J, "banner-influenza.webp"), quality=86)
    print("aset Vaksimine dibuat di", J)


if __name__ == "__main__":
    main()
