#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Banner promo beranda VaksinKu berdasarkan harga Katalog VaksinKu 2026.

Hanya memakai harga resmi katalog (src/data_katalog.py): tidak ada harga promo karangan.
Foto orang diambil dari banner VaksinKu sebelumnya (app/banner/arsip/); ilustrasi Ka'bah
dan pranikah digambar sebagai SVG. Hasil: app/banner/*-2026.webp (1200×540).

    python3 src/buat_banner_2026.py
"""
import base64
import os
import subprocess
import sys
import tempfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_bundle as B  # noqa: E402
import data_katalog as D  # noqa: E402

CHROME = "/opt/pw-browsers/chromium"
ARSIP = os.path.join(ROOT, "app", "banner", "arsip")
KELUAR = os.path.join(ROOT, "app", "banner")
TEAL, TEAL_D, TEAL_T, MAG, MAG_D, INK = "#2FB3B8", "#137C82", "#E4F7F8", "#D9177A", "#A81260", "#123B45"


def uri(path, mime=None):
    with open(path, "rb") as f:
        raw = f.read()
    mime = mime or {".png": "image/png", ".webp": "image/webp", ".jpg": "image/jpeg"}[os.path.splitext(path)[1]]
    return "data:%s;base64,%s" % (mime, base64.b64encode(raw).decode("ascii"))


def harga(merk, kolom="umum"):
    for r in D.HARGA:
        if r[4] == merk:
            return r[6] if kolom == "umum" else r[5]
    raise KeyError(merk)


def foto_kanan(nama, x0=600):
    """Potongan foto sisi kanan banner lama (orang/model)."""
    im = Image.open(os.path.join(ARSIP, nama)).convert("RGB")
    p = os.path.join(tempfile.mkdtemp(), "f.jpg")
    im.crop((x0, 0, im.width, im.height)).save(p, quality=92)
    return uri(p)


LOGO = uri(os.path.join(ROOT, "src", "vaksinku-logo.png"))
CSS = """
*{box-sizing:border-box;margin:0;padding:0;}
html,body{background:#fff;}
.b{width:1200px;height:540px;position:relative;overflow:hidden;font-family:'Plus Jakarta Sans';color:%(INK)s;
  background:linear-gradient(120deg,#FFFFFF 0%%,#F1FBFB 55%%,#DDF3F4 100%%);}
.foto{position:absolute;right:0;bottom:0;height:540px;-webkit-mask-image:linear-gradient(to right,transparent 0,#000 22%%);}
.kiri{position:absolute;left:44px;top:30px;width:690px;}
.logo{height:46px;}
.pita{display:inline-block;background:%(MAG)s;color:#fff;font-weight:700;font-size:17px;border-radius:999px;padding:5px 16px;margin-top:12px;}
.judul{font-family:'Baloo 2';font-weight:800;font-size:58px;line-height:.95;color:%(TEAL_D)s;margin-top:10px;letter-spacing:-.5px;}
.judul em{font-style:normal;color:%(MAG)s;}
.sub{font-size:19px;font-weight:600;color:%(INK)s;margin-top:6px;}
.kartu{display:flex;gap:14px;margin-top:16px;}
.k{background:#fff;border-radius:18px;padding:12px 16px;box-shadow:0 8px 22px rgba(19,124,130,.14);border:1.5px solid #D6EEEF;min-width:190px;}
.k .n{font-weight:800;font-size:19px;color:%(TEAL_D)s;line-height:1.15;}
.k .m{font-size:14px;color:#5A6B70;margin-top:2px;}
.k .h{font-family:'Baloo 2';font-weight:800;font-size:30px;color:%(MAG_D)s;line-height:1;margin-top:8px;}
.k .h small{font-size:15px;font-weight:700;color:#5A6B70;}
.k .c{font-size:15px;color:#8A9599;text-decoration:line-through;margin-top:6px;}
.k.utama{background:linear-gradient(135deg,%(TEAL)s,%(TEAL_D)s);border:none;color:#fff;}
.k.utama .n,.k.utama .m,.k.utama .h,.k.utama .h small{color:#fff;}
.k.utama .c{color:#CFEFF0;}
.hemat{display:inline-block;background:%(MAG)s;color:#fff;font-size:12px;font-weight:800;border-radius:999px;padding:3px 10px;margin-left:6px;vertical-align:middle;}
.kaki{position:absolute;left:44px;bottom:24px;display:flex;align-items:center;gap:16px;font-size:15px;color:#4A5B60;}
.cta{background:%(TEAL_D)s;color:#fff;font-weight:800;border-radius:999px;padding:11px 24px;font-size:17px;}
.cat{position:absolute;left:44px;bottom:78px;font-size:13.5px;color:#5A6B70;}
""" % dict(INK=INK, MAG=MAG, TEAL_D=TEAL_D, TEAL=TEAL, MAG_D=MAG_D)


def kaki(ajakan="Booking Sekarang →"):
    return ('<div class="kaki"><span class="cta">%s</span><span>WhatsApp <b>%s</b> · @alrashaibumasgroup</span></div>'
            % (ajakan, D.BRAND["call_center"].replace("-", " ")))


def catatan(t="Harga dokter umum · sudah termasuk jasa dokter, vaksin, bahan habis pakai & administrasi"):
    return '<div class="cat">%s</div>' % t


def kartu(nama, merk, hrg, coret=None, satuan="", utama=False, label=""):
    return ('<div class="k%s"><div class="n">%s%s</div><div class="m">%s</div><div class="h"><small>Rp</small>%s%s</div>%s</div>'
            % (" utama" if utama else "", nama, '<span class="hemat">%s</span>' % label if label else "", merk, hrg,
               '<small> %s</small>' % satuan if satuan else "", '<div class="c">Rp%s</div>' % coret if coret else ""))


KABAH = """<svg viewBox="0 0 520 540" width="520" height="540" style="position:absolute;right:0;bottom:0;">
<defs><linearGradient id="lg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9F7F8"/><stop offset="1" stop-color="#BFE6E8"/></linearGradient></defs>
<circle cx="300" cy="230" r="210" fill="url(#lg)"/>
<path d="M120 120 q120 -70 300 -10" stroke="#fff" stroke-width="4" fill="none" stroke-dasharray="10 10"/>
<g transform="translate(400 96) rotate(-12)"><path d="M0 0 l60 0 l14 -8 l8 0 l-8 14 l-14 2 l-20 22 l-12 0 l10 -22 l-28 2 l-8 10 l-8 0 l4 -14 z" fill="#137C82"/></g>
<g transform="translate(170 250)">
<polygon points="0,40 150,0 260,40 260,230 110,270 0,230" fill="#1E2328"/>
<polygon points="0,40 110,80 110,270 0,230" fill="#2B3137"/>
<polygon points="0,40 150,0 260,40 110,80" fill="#3A4148"/>
<polygon points="0,92 110,132 110,148 0,108" fill="#D4A63A"/>
<polygon points="110,132 260,92 260,108 110,148" fill="#E8BE52"/>
<rect x="150" y="150" width="34" height="62" rx="4" fill="#D4A63A" transform="skewY(-15)"/>
</g>
<ellipse cx="300" cy="530" rx="260" ry="26" fill="#9BD5D8" opacity=".6"/>
</svg>"""

CINCIN = """<svg viewBox="0 0 520 540" width="520" height="540" style="position:absolute;right:0;bottom:0;">
<defs><linearGradient id="emas" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F6D57A"/><stop offset="1" stop-color="#C9952E"/></linearGradient></defs>
<circle cx="300" cy="250" r="215" fill="#FCE4EE"/>
<circle cx="250" cy="290" r="92" fill="none" stroke="url(#emas)" stroke-width="26"/>
<circle cx="360" cy="290" r="92" fill="none" stroke="url(#emas)" stroke-width="26"/>
<path d="M360 140 l22 -30 l22 30 l-22 22 z" fill="#BFE9F2" stroke="#fff" stroke-width="4"/>
<g fill="#D9177A" opacity=".85"><path d="M140 140 c-14 -18 -38 -4 -24 18 l24 22 l24 -22 c14 -22 -10 -36 -24 -18z"/>
<path d="M450 410 c-10 -13 -28 -3 -18 13 l18 16 l18 -16 c10 -16 -8 -26 -18 -13z"/></g>
<g fill="#fff"><circle cx="180" cy="430" r="14"/><circle cx="200" cy="445" r="9"/><circle cx="470" cy="170" r="11"/></g>
</svg>"""


def banner(isi, kanan):
    return '<div class="b">%s%s</div>' % (kanan, isi)


def render(html, keluar):
    d = tempfile.mkdtemp()
    f = os.path.join(d, "b.html")
    with open(f, "w", encoding="utf-8") as fh:
        fh.write('<!doctype html><html><head><meta charset="utf-8"><style>%s</style><style>%s</style></head><body>%s</body></html>'
                 % (FONTS, CSS, html))
    png = os.path.join(d, "b.png")
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--window-size=1200,800",
                    "--virtual-time-budget=2000", "--screenshot=" + png, "file://" + f], capture_output=True, timeout=120)
    Image.open(png).convert("RGB").crop((0, 0, 1200, 540)).save(keluar, quality=88)
    print("  ", os.path.relpath(keluar, ROOT))


def main():
    global FONTS
    FONTS = B.font_css()
    pt, apm = D.PAKET_INTERNASIONAL[1], D.PAKET_INTERNASIONAL[0]
    hi = dict((n, h) for n, h, _ in D.HARGA_INTERNASIONAL)
    lg = '<img class="logo" src="%s">' % LOGO

    render(banner('<div class="kiri">%s<div class="pita">Haji · Umrah · Luar Negeri</div>'
                  '<div class="judul">Paket Vaksin <em>Haji &amp; Umrah</em></div>'
                  '<div class="sub">Wajib Meningitis &amp; Polio · e-ICV terbit di klinik</div>'
                  '<div class="kartu">%s%s</div>'
                  '<div class="sub" style="font-size:16px;margin-top:12px;">Satuan: Polio (IPV) Rp%s · Meningitis Rp%s</div></div>%s%s'
                  % (lg, kartu(pt["nama"], " + ".join(["Polio", "Meningitis", "Influenza"]), pt["harga"], pt["coret"], utama=True, label="HEMAT"),
                     kartu(apm["nama"], "Polio + Meningitis + Apotek Mini Marwa", apm["harga"], apm["coret"], label="HEMAT"),
                     hi["Polio (IPV)"], hi["Meningitis"], catatan("Harga sudah termasuk jasa dokter, vaksin, bahan habis pakai & administrasi"),
                     kaki()), KABAH), os.path.join(KELUAR, "haji-umrah-2026.webp"))

    render(banner('<div class="kiri">%s<div class="pita">1 dosis setiap tahun</div>'
                  '<div class="judul">Vaksin <em>Influenza</em></div>'
                  '<div class="sub">Lindungi keluarga dari flu &amp; komplikasinya</div>'
                  '<div class="kartu">%s%s</div></div>%s%s'
                  % (lg, kartu("Flubio", "3 strain", harga("Flubio")), kartu("Vaxigrip TIV", "3 strain", harga("Vaxigrip TIV"), utama=True),
                     catatan(), kaki()), '<img class="foto" src="%s">' % foto_kanan("influenza-bareng.webp", 640)),
           os.path.join(KELUAR, "influenza-2026.webp"))

    render(banner('<div class="kiri">%s<div class="pita">Cegah Kanker Serviks</div>'
                  '<div class="judul">Vaksin <em>HPV</em></div>'
                  '<div class="sub">3 dosis untuk perlindungan optimal (0 – 2 – 6 bulan)</div>'
                  '<div class="kartu">%s%s</div></div>%s%s'
                  % (lg, kartu("HPV 4", "Melindungi dari 4 tipe HPV", harga("HPV 4"), satuan="/dosis", utama=True),
                     kartu("HPV 9 · Gardasil 9", "Melindungi dari 9 tipe HPV", harga("Gardasil 9"), satuan="/dosis"),
                     catatan(), kaki()), '<img class="foto" src="%s">' % foto_kanan("hpv4-diperpanjang.webp", 700)),
           os.path.join(KELUAR, "hpv-2026.webp"))

    render(banner('<div class="kiri">%s<div class="pita">Sesuai jadwal IDAI 2024</div>'
                  '<div class="judul">Vaksin Dasar <em>Si Kecil</em></div>'
                  '<div class="sub">Lengkapi imunisasi buah hati di klinik atau Home Care</div>'
                  '<div class="kartu">%s%s%s</div></div>%s%s'
                  % (lg, kartu("Infanrix Hexa", "6 penyakit dalam 1 vaksin", harga("Infanrix Hexa"), utama=True),
                     kartu("PCV 20", "Prevenar 20 · pneumonia", harga("Prevenar 20")),
                     kartu("Rotavirus", "Rotateq · diare berat", harga("Rotateq")),
                     catatan("Harga per dosis, dokter umum · sudah termasuk jasa dokter, vaksin, BHP & administrasi"), kaki()),
                  '<img class="foto" src="%s" style="height:540px;">' % foto_kanan("little-protection.webp", 690)),
           os.path.join(KELUAR, "anak-2026.webp"))

    render(banner('<div class="kiri">%s<div class="pita">Persiapan sebelum menikah</div>'
                  '<div class="judul">Vaksin <em>Pranikah</em></div>'
                  '<div class="sub">5 vaksin, dimulai 7 bulan sebelum hari pernikahan</div>'
                  '<div class="kartu" style="flex-wrap:wrap;width:700px;gap:10px;">%s%s%s%s%s</div></div>%s%s'
                  % (lg, kartu("HPV 4", "3 dosis", harga("HPV 4"), utama=True), kartu("MMR", "2 dosis", harga("MMR")),
                     kartu("Tetanus (Tdap)", "1 dosis", harga("Adacel")), kartu("Hepatitis B", "3 dosis", harga("Engerix-B Dewasa")),
                     kartu("Influenza", "tiap tahun · mulai", harga("Flubio")),
                     catatan("Harga per dosis, dokter umum · sudah termasuk jasa dokter, vaksin, BHP & administrasi"), kaki()),
                  CINCIN).replace('class="k"', 'class="k" style="min-width:0;padding:9px 14px;"')
           .replace('class="k utama"', 'class="k utama" style="min-width:0;padding:9px 14px;"'),
           os.path.join(KELUAR, "pranikah-2026.webp"))

    render(banner('<div class="kiri">%s<div class="pita">Baru di VaksinKu</div>'
                  '<div class="judul">Vaksin <em>Baru</em> Tersedia</div>'
                  '<div class="sub">Untuk perjalanan, perlindungan hati, dan meningitis</div>'
                  '<div class="kartu">%s%s%s</div></div>%s%s'
                  % (lg, kartu("Yellow Fever", "Stamaril", harga("Stamaril"), utama=True),
                     kartu("Hepatitis A + B", "Twinrix", harga("Twinrix")),
                     kartu("Meningitis Konjugat", "MenQuadfi", harga("MenQuadfi")), catatan(), kaki()),
                  '<img class="foto" src="%s">' % foto_kanan("bundling-hpv.webp", 680)),
           os.path.join(KELUAR, "vaksin-baru-2026.webp"))


if __name__ == "__main__":
    main()
