#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mockup tiga alternatif halaman cover (layar pembuka) aplikasi VaksinKu.

Ilustrasi digambar sebagai SVG (tanpa gambar luar) dengan warna logo baru.
Keluaran: mockup/cover-alternatif.html (+ .png lewat Chromium headless).

    python3 mockup/build_cover.py
"""
import base64
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "src"))
import build_bundle as B  # noqa: E402

TEAL, TEAL_D, MAG, MAG_D = "#38BCBD", "#1F8C8E", "#DC106E", "#A80D55"
KULIT = ["#F6D2B6", "#EBC09D", "#D9A47E"]


def b64(p):
    with open(p, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


LOGO = b64(os.path.join(ROOT, "src", "vaksinku-logo.png"))
LOGO_MARK = b64(os.path.join(ROOT, "src", "vaksinku-logo-mark.png"))
with open(os.path.join(HERE, "simbol-v.svg"), encoding="utf-8") as f:
    SIMBOL = f.read().replace('<rect width="1024" height="1024" fill="#FFFFFF"/>', "")
SIMBOL_96 = SIMBOL.replace('width="1024" height="1024"', 'width="96" height="96"')


# ------------------------------------------------------------------ tokoh
def wajah(cx, cy, r, mata="senyum"):
    """Mata melengkung tersenyum, pipi merona, mulut."""
    ex, ey, s = r * 0.38, cy - r * 0.02, r * 0.16
    if mata == "tidur":
        m = (f'<path d="M{cx-ex-s} {ey} q{s} {s*0.9} {2*s} 0 M{cx+ex-s} {ey} q{s} {s*0.9} {2*s} 0" '
             f'stroke="#3A2A2A" stroke-width="{r*0.07:.1f}" fill="none" stroke-linecap="round"/>')
    else:
        m = (f'<path d="M{cx-ex-s} {ey} q{s} {-s*1.1} {2*s} 0 M{cx+ex-s} {ey} q{s} {-s*1.1} {2*s} 0" '
             f'stroke="#3A2A2A" stroke-width="{r*0.08:.1f}" fill="none" stroke-linecap="round"/>')
    pipi = (f'<circle cx="{cx-r*0.55}" cy="{cy+r*0.28}" r="{r*0.14}" fill="#F48FB1" opacity=".55"/>'
            f'<circle cx="{cx+r*0.55}" cy="{cy+r*0.28}" r="{r*0.14}" fill="#F48FB1" opacity=".55"/>')
    mulut = (f'<path d="M{cx-r*0.2} {cy+r*0.3} q{r*0.2} {r*0.24} {r*0.4} 0" stroke="#A33B4B" '
             f'stroke-width="{r*0.07:.1f}" fill="#fff" stroke-linecap="round"/>')
    return m + pipi + mulut


def tokoh(x, y, t=1.0, kulit=0, baju=TEAL, rambut="#3B2A25", hijab=None, jenis="dewasa",
          celana="#4A5A7A", aksesori=""):
    """Tokoh berdiri, kaki di (x, y). t = skala (dewasa = tinggi ±220)."""
    k = KULIT[kulit]
    if jenis == "anak":
        t *= 0.66
    r = 34 * t                      # jari-jari kepala
    leher = y - 120 * t
    hy = leher - r * 0.85           # pusat kepala
    w = 46 * t                      # setengah lebar badan
    g = []
    # kaki
    g.append(f'<rect x="{x-w*0.62}" y="{y-58*t}" width="{w*0.55}" height="{58*t}" rx="{10*t}" fill="{celana}"/>')
    g.append(f'<rect x="{x+w*0.07}" y="{y-58*t}" width="{w*0.55}" height="{58*t}" rx="{10*t}" fill="{celana}"/>')
    # badan
    g.append(f'<path d="M{x-w} {y-50*t} L{x-w} {leher+22*t} Q{x-w} {leher} {x-w+22*t} {leher} L{x+w-22*t} {leher} '
             f'Q{x+w} {leher} {x+w} {leher+22*t} L{x+w} {y-50*t} Z" fill="{baju}"/>')
    # lengan
    g.append(f'<rect x="{x-w-13*t}" y="{leher+8*t}" width="{20*t}" height="{62*t}" rx="{10*t}" fill="{baju}"/>')
    g.append(f'<rect x="{x+w-7*t}" y="{leher+8*t}" width="{20*t}" height="{62*t}" rx="{10*t}" fill="{baju}"/>')
    g.append(f'<circle cx="{x-w-3*t}" cy="{leher+72*t}" r="{9*t}" fill="{k}"/>')
    g.append(f'<circle cx="{x+w+3*t}" cy="{leher+72*t}" r="{9*t}" fill="{k}"/>')
    if hijab:
        g.append(f'<path d="M{x-r*1.25} {leher+30*t} Q{x-r*1.3} {hy-r*1.35} {x} {hy-r*1.3} '
                 f'Q{x+r*1.3} {hy-r*1.35} {x+r*1.25} {leher+30*t} Z" fill="{hijab}"/>')
        g.append(f'<ellipse cx="{x}" cy="{hy+r*0.08}" rx="{r*0.82}" ry="{r*0.9}" fill="{k}"/>')
    else:
        g.append(f'<rect x="{x-9*t}" y="{leher-8*t}" width="{18*t}" height="{14*t}" fill="{k}"/>')
        g.append(f'<circle cx="{x}" cy="{hy}" r="{r}" fill="{k}"/>')
        if rambut:
            g.append(f'<path d="M{x-r*1.04} {hy+r*0.05} Q{x-r*1.15} {hy-r*1.25} {x} {hy-r*1.08} '
                     f'Q{x+r*1.2} {hy-r*1.2} {x+r*1.04} {hy+r*0.05} Q{x+r*0.6} {hy-r*0.55} {x-r*0.1} {hy-r*0.5} '
                     f'Q{x-r*0.7} {hy-r*0.45} {x-r*1.04} {hy+r*0.05} Z" fill="{rambut}"/>')
    g.append(wajah(x, hy + r * 0.05, r))
    g.append(aksesori.format(x=x, y=y, t=t, leher=leher, hy=hy, r=r, w=w))
    return "".join(g)


def jas_dokter(x, y, t):
    """Jas putih di atas badan tokoh perawat/dokter + stetoskop."""
    w, leher = 46 * t, y - 120 * t
    return (f'<path d="M{x-w} {y-50*t} L{x-w} {leher+22*t} Q{x-w} {leher} {x-w+22*t} {leher} L{x-6*t} {leher} L{x-6*t} {y-50*t} Z" fill="#FFFFFF"/>'
            f'<path d="M{x+w} {y-50*t} L{x+w} {leher+22*t} Q{x+w} {leher} {x+w-22*t} {leher} L{x+6*t} {leher} L{x+6*t} {y-50*t} Z" fill="#FFFFFF"/>'
            f'<path d="M{x-16*t} {leher+4*t} q0 {38*t} {16*t} {44*t} q{16*t} {-6*t} {16*t} {-44*t}" stroke="#5B6B7B" stroke-width="{3.5*t}" fill="none"/>'
            f'<circle cx="{x}" cy="{leher+50*t}" r="{6*t}" fill="#5B6B7B"/>'
            f'<rect x="{x+w*0.35}" y="{leher+30*t}" width="{14*t}" height="{18*t}" rx="2" fill="{TEAL}"/>')


def bayi(x, y, t=1.0, selimut="#FFFFFF"):
    """Bayi dibedong dalam gendongan; (x, y) = pusat bedong."""
    r = 20 * t
    return (f'<ellipse cx="{x}" cy="{y}" rx="{38*t}" ry="{24*t}" fill="{selimut}" stroke="#F3C6D8" stroke-width="2"/>'
            f'<circle cx="{x-26*t}" cy="{y-14*t}" r="{r}" fill="{KULIT[0]}"/>'
            f'<path d="M{x-46*t} {y-18*t} Q{x-40*t} {y-42*t} {x-14*t} {y-30*t}" fill="#7A5A4A"/>'
            + wajah(x - 26 * t, y - 12 * t, r, "tidur"))


def suntik(x, y, s=1.0, rot=-35):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
            f'<rect x="-34" y="-9" width="56" height="18" rx="4" fill="#FFFFFF" stroke="{TEAL_D}" stroke-width="3"/>'
            f'<rect x="-30" y="-5" width="30" height="10" rx="2" fill="{MAG}" opacity=".85"/>'
            f'<rect x="22" y="-4" width="12" height="8" fill="{TEAL_D}"/><line x1="34" y1="0" x2="56" y2="0" stroke="#7A8A9A" stroke-width="3"/>'
            f'<rect x="-46" y="-3" width="12" height="6" fill="{TEAL_D}"/><rect x="-50" y="-12" width="5" height="24" rx="2" fill="{TEAL_D}"/></g>')


def hati(x, y, s=1.0, warna=MAG, op=0.8):
    return (f'<path transform="translate({x} {y}) scale({s})" d="M0 6 C-12 -6 -6 -16 0 -9 C6 -16 12 -6 0 6 Z" '
            f'fill="{warna}" opacity="{op}"/>')


def bunga(x, y, s=1.0):
    kel = "".join(f'<ellipse cx="0" cy="-9" rx="5" ry="9" fill="#FFFFFF" transform="rotate({a})"/>' for a in range(0, 360, 72))
    return f'<g transform="translate({x} {y}) scale({s})">{kel}<circle r="4" fill="#F7C948"/></g>'


def daun(x, y, s=1.0, rot=0):
    return (f'<path transform="translate({x} {y}) rotate({rot}) scale({s})" d="M0 0 Q18 -30 0 -60 Q-18 -30 0 0 Z" '
            f'fill="#5DAA7A"/><path transform="translate({x} {y}) rotate({rot}) scale({s})" d="M0 0 L0 -55" stroke="#3E8A5C" stroke-width="2"/>')


def keluarga(lebar=390, tinggi=330):
    """Ilustrasi keluarga + tenaga kesehatan, gaya serupa contoh cover."""
    dasar = tinggi - 4
    s = []
    # semak & bunga di kiri-kanan
    for x0, arah in ((14, 1), (lebar - 14, -1)):
        for i, rot in enumerate((-30, 0, 30)):
            s.append(daun(x0 + arah * i * 10, dasar - 30, 1.1, rot * arah))
        s.append(bunga(x0 + arah * 22, dasar - 90, 1.2))
        s.append(bunga(x0 + arah * 6, dasar - 48, 0.9))
    # gelembung harapan: bayi dalam awan
    s.append(f'<ellipse cx="{lebar/2}" cy="58" rx="62" ry="40" fill="#FFFFFF" opacity=".75"/>'
             f'<ellipse cx="{lebar/2-40}" cy="70" rx="26" ry="20" fill="#FFFFFF" opacity=".75"/>'
             f'<ellipse cx="{lebar/2+42}" cy="68" rx="28" ry="20" fill="#FFFFFF" opacity=".75"/>')
    s.append(bayi(lebar / 2 + 10, 62, 0.9))
    s.append(hati(lebar / 2 - 60, 40, 1.1) + hati(lebar / 2 + 70, 34, 0.9, TEAL))
    # baris belakang: kakek, nenek, ayah
    s.append(tokoh(92, dasar - 40, 0.92, 1, "#6E9C7E", "#C9CED6", celana="#55616E"))
    s.append(f'<g fill="none" stroke="#3A2A2A" stroke-width="2.4"><circle cx="{92-11}" cy="{dasar-40-120*0.92-34*0.92*0.85}" r="9"/>'
             f'<circle cx="{92+11}" cy="{dasar-40-120*0.92-34*0.92*0.85}" r="9"/></g>')
    s.append(tokoh(150, dasar - 46, 0.86, 0, "#B89BC9", None, hijab="#C9CED6", celana="#8A7A9A"))
    s.append(tokoh(lebar - 92, dasar - 40, 0.95, 1, "#8FB3E0", "#3B2A25", celana="#3F4F6A"))
    # baris depan: perawat, ibu hamil + bayi, anak-anak, bidan
    s.append(tokoh(52, dasar, 0.9, 0, "#9EC5E8", None, hijab="#7FA6D6", celana="#4A5A7A"))
    s.append(jas_dokter(52, dasar, 0.9))
    s.append(tokoh(lebar / 2 + 6, dasar, 1.0, 0, "#F4A6C1", None, hijab="#E57AA3", celana="#C76A8E"))
    s.append(bayi(lebar / 2 + 4, dasar - 92, 0.8, "#FFF7FB"))
    s.append(tokoh(lebar / 2 - 62, dasar, 0.95, 2, TEAL, "#3B2A25", jenis="anak", celana="#2F6F70"))
    s.append(tokoh(lebar / 2 + 74, dasar, 0.95, 0, "#F7C948", "#5A3A2A", jenis="anak", celana="#C98A2E"))
    s.append(tokoh(lebar - 44, dasar, 0.88, 1, "#E8D3C0", None, hijab="#F1D9C8", celana="#B5967E"))
    s.append(suntik(lebar - 20, dasar - 120, 0.6, -60))
    s.append(hati(30, dasar - 160, 0.9) + hati(lebar - 30, dasar - 175, 0.8, TEAL))
    return f'<svg viewBox="0 0 {lebar} {tinggi}" width="100%" style="display:block;">{"".join(s)}</svg>'


def perisai():
    """Ilustrasi B: perisai berlogo + ikon vaksin melayang."""
    return (f'<svg viewBox="0 0 390 300" width="100%" style="display:block;">'
            f'<circle cx="195" cy="160" r="128" fill="#FFFFFF" opacity=".55"/>'
            f'<circle cx="195" cy="160" r="96" fill="#FFFFFF" opacity=".7"/>'
            f'<path d="M195 62 L268 92 Q268 196 195 238 Q122 196 122 92 Z" fill="{TEAL}"/>'
            f'<path d="M195 78 L254 102 Q254 186 195 220 Q136 186 136 102 Z" fill="#FFFFFF"/>'
            f'<g transform="translate(160 112) scale(0.068)">{SIMBOL.split(">",1)[1].rsplit("</svg>",1)[0]}</g>'
            f'<path d="M172 186 l14 14 l28 -30" stroke="{MAG}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            + suntik(70, 92, 0.9, -30) + suntik(318, 214, 0.8, 150)
            + f'<g transform="translate(316 74)"><rect x="-14" y="-6" width="28" height="44" rx="7" fill="#FFFFFF" stroke="{TEAL_D}" stroke-width="3"/>'
              f'<rect x="-14" y="10" width="28" height="18" fill="{MAG}" opacity=".8"/><rect x="-10" y="-16" width="20" height="12" rx="3" fill="{TEAL_D}"/></g>'
            + f'<g transform="translate(66 220)"><rect x="-24" y="-20" width="48" height="44" rx="8" fill="#FFFFFF" stroke="{TEAL_D}" stroke-width="3"/>'
              f'<rect x="-24" y="-20" width="48" height="12" rx="6" fill="{MAG}"/><g fill="{TEAL}"><circle cx="-10" cy="4" r="4"/><circle cx="4" cy="4" r="4"/><circle cx="-10" cy="16" r="4"/>'
              f'<circle cx="4" cy="16" r="4"/></g><circle cx="16" cy="16" r="5" fill="{MAG}"/></g>'
            + hati(110, 40, 1.2) + hati(286, 150, 1.0, TEAL) + hati(150, 268, 0.9) + bunga(250, 266, 1.0) + bunga(40, 150, 0.9)
            + '</svg>')


def ibu_anak():
    """Ilustrasi C: ibu, anak, dan perawat di klinik."""
    s = ['<svg viewBox="0 0 390 300" width="100%" style="display:block;">',
         '<rect x="40" y="70" width="310" height="230" rx="26" fill="#FFFFFF" opacity=".6"/>',
         f'<rect x="250" y="96" width="74" height="60" rx="10" fill="#FFFFFF" stroke="{TEAL}" stroke-width="3"/>',
         f'<path d="M287 110 v32 M271 126 h32" stroke="{MAG}" stroke-width="9" stroke-linecap="round"/>',
         tokoh(120, 296, 1.05, 0, "#F4A6C1", None, hijab="#E57AA3", celana="#C76A8E"),
         tokoh(182, 296, 1.05, 2, "#F7C948", "#3B2A25", jenis="anak", celana="#C98A2E"),
         tokoh(272, 296, 1.0, 1, "#9EC5E8", None, hijab="#7FA6D6", celana="#4A5A7A"),
         jas_dokter(272, 296, 1.0),
         suntik(318, 200, 0.7, -70),
         f'<circle cx="214" cy="200" r="11" fill="#FFFFFF" stroke="{TEAL_D}" stroke-width="2"/>',
         f'<rect x="207" y="196" width="14" height="8" rx="3" fill="#F7C948"/>',
         hati(70, 60, 1.2), hati(340, 50, 1.0, TEAL), hati(200, 40, 0.8), bunga(30, 280, 1.1), bunga(360, 280, 1.0),
         '</svg>']
    return "".join(s)


# ------------------------------------------------------------------ layar
def hp(isi, latar):
    return (f'<div class="hp" style="background:{latar};"><div class="statusbar"><span>08.18</span>'
            f'<span>5G ▮▮▮ 34</span></div>{isi}</div>')


def alt_a():
    isi = (f'<div class="tengah" style="padding-top:96px;">'
           f'<div class="lingkar"><img src="{LOGO}" alt="VaksinKu by Alrasha Health Care Group" style="width:150px;"></div>'
           f'<div class="judul">VaksinKu</div>'
           f'<div class="tagline">“Lindungi Keluarga,<br>Lengkapi Imunisasinya”</div></div>'
           f'<div class="ilus">{keluarga()}</div>')
    return hp(isi, "linear-gradient(180deg,#FDEFF5 0%,#FBE3EE 55%,#F9E6EF 100%)")


def alt_b():
    isi = (f'<div class="tengah" style="padding-top:84px;">'
           f'<div class="kartu-logo"><img src="{LOGO}" alt="VaksinKu by Alrasha Health Care Group" style="width:220px;"></div>'
           f'<div class="tagline" style="color:{TEAL_D};margin-top:22px;">Aman · Lengkap · Terjangkau</div>'
           f'<div class="sub">Jadwal vaksin, rekam medis, dan reservasi<br>vaksinasi keluarga dalam satu aplikasi.</div></div>'
           f'<div class="ilus" style="bottom:46px;">{perisai()}</div>'
           f'<div class="titik"><i class="on"></i><i></i><i></i></div>')
    return hp(isi, f"linear-gradient(180deg,#E3F6F6 0%,#D2F0F0 60%,#C3EBEB 100%)")


def alt_c():
    gelombang = (f'<svg viewBox="0 0 390 120" width="100%" style="position:absolute;top:342px;left:0;display:block;" preserveAspectRatio="none">'
                 f'<path d="M0 40 Q100 0 200 36 T390 30 V120 H0 Z" fill="#FFF7FA"/></svg>')
    isi = (f'<div style="position:absolute;inset:0 0 auto 0;height:420px;background:linear-gradient(160deg,{TEAL} 0%,#2AA6A8 100%);"></div>'
           + gelombang +
           f'<div class="tengah" style="padding-top:78px;position:relative;">'
           f'<div class="lingkar" style="width:150px;height:150px;box-shadow:0 14px 34px rgba(0,60,60,.25);">'
           f'<div style="width:96px;height:96px;">{SIMBOL_96}</div></div>'
           f'<div class="judul" style="color:#fff;margin-top:16px;">VaksinKu</div>'
           f'<div style="color:#E6FBFB;font-size:13px;font-weight:600;margin-top:-4px;">by Alrasha Health Care Group</div></div>'
           f'<div style="position:absolute;top:468px;left:0;right:0;text-align:center;padding:0 34px;">'
           f'<div class="tagline" style="color:{MAG};">#VaksinKeluargaJadiMudah</div></div>'
           f'<div class="ilus">{ibu_anak()}</div>')
    return hp(isi, "#FFF7FA")


CSS = """
*{box-sizing:border-box;margin:0;padding:0;}
body{background:#EEF0F2;font-family:'Plus Jakarta Sans',sans-serif;color:#1E2A32;padding:40px 24px 60px;}
h1{font-family:'Baloo 2',sans-serif;font-size:30px;text-align:center;}
.pengantar{max-width:860px;margin:6px auto 30px;text-align:center;color:#5A6670;font-size:15px;line-height:1.6;}
.deret{display:flex;flex-wrap:wrap;gap:34px;justify-content:center;}
.kolom{display:flex;flex-direction:column;align-items:center;gap:14px;}
.label{font-family:'Baloo 2',sans-serif;font-weight:800;font-size:20px;}
.label small{display:block;font-family:'Plus Jakarta Sans',sans-serif;font-weight:500;font-size:13px;color:#5A6670;text-align:center;max-width:330px;line-height:1.5;}
.hp{position:relative;width:390px;height:844px;border-radius:44px;overflow:hidden;box-shadow:0 0 0 10px #1E2328,0 24px 60px rgba(0,0,0,.25);}
.statusbar{position:relative;z-index:3;display:flex;justify-content:space-between;padding:14px 28px 0;font-size:13px;font-weight:700;color:#3A3A3A;}
.tengah{display:flex;flex-direction:column;align-items:center;text-align:center;}
.lingkar{width:176px;height:176px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;
  box-shadow:0 18px 40px rgba(220,16,110,.14);}
.kartu-logo{background:#fff;border-radius:28px;padding:26px 26px 22px;box-shadow:0 16px 40px rgba(31,140,142,.16);}
.judul{font-family:'Baloo 2',sans-serif;font-weight:800;font-size:30px;color:#2A2A33;margin-top:26px;}
.tagline{font-family:'Plus Jakarta Sans',sans-serif;font-style:italic;font-size:17px;line-height:1.6;color:#6B5A66;margin-top:8px;}
.sub{font-size:13px;color:#4F6B6C;line-height:1.6;margin-top:10px;}
.ilus{position:absolute;left:0;right:0;bottom:0;}
.titik{position:absolute;bottom:22px;left:0;right:0;display:flex;gap:7px;justify-content:center;}
.titik i{width:7px;height:7px;border-radius:50%;background:#1F8C8E;opacity:.35;display:block;}
.titik i.on{width:18px;border-radius:4px;background:#DC106E;opacity:1;}
"""


def main():
    fonts = B.font_css()
    html = (f'<!doctype html><html lang="id"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>Cover VaksinKu — Alternatif</title><style>{fonts}</style><style>{CSS}</style></head><body>'
            f'<h1>Alternatif Halaman Cover VaksinKu</h1>'
            f'<div class="pengantar">Layar pertama saat aplikasi dibuka, memakai logo baru <b>VaksinKu by Alrasha Health Care Group</b>. '
            f'Ilustrasi digambar ulang dengan warna logo (toska &amp; magenta) sehingga tetap tajam di semua ukuran layar.</div>'
            f'<div class="deret">'
            f'<div class="kolom">{alt_a()}<div class="label">A · Keluarga<small>Paling mirip contoh: logo dalam lingkaran putih, '
            f'latar merah muda lembut, ilustrasi keluarga tiga generasi bersama tenaga kesehatan.</small></div></div>'
            f'<div class="kolom">{alt_b()}<div class="label">B · Perisai Toska<small>Latar toska segar, logo lengkap dalam kartu, '
            f'ilustrasi perisai perlindungan dengan ikon vaksin.</small></div></div>'
            f'<div class="kolom">{alt_c()}<div class="label">C · Ikon &amp; Gelombang<small>Atas toska bergelombang dengan ikon aplikasi '
            f'(sama dengan ikon di layar utama HP), ibu &amp; anak bersama perawat.</small></div></div>'
            f'</div></body></html>')
    out = os.path.join(HERE, "cover-alternatif.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", out)
    png = os.path.join(HERE, "cover-alternatif.png")
    subprocess.run(["/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
                    "--hide-scrollbars", "--window-size=1400,1230", "--screenshot=" + png, "file://" + out],
                   capture_output=True, timeout=120)
    print("wrote", png)


if __name__ == "__main__":
    main()


# ------------------------------------------------------------------ cover terpilih (alternatif 1, Okt 2026)
def _kartu_ikon(x, y, ikon, s=58):
    """Kartu putih membulat melayang dengan ikon garis."""
    return (f'<g transform="translate({x} {y})"><rect x="{-s/2}" y="{-s/2}" width="{s}" height="{s}" rx="16" '
            f'fill="#FFFFFF" filter="url(#bayang-kartu)"/>{ikon}</g>')


IKON_SUNTIK = (f'<g stroke="{TEAL}" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round" transform="rotate(-45)">'
               '<rect x="-12" y="-5" width="22" height="10" rx="2"/><path d="M10 0 h9 M-12 0 h-5 M-17 -6 v12 M-6 -5 v4 M0 -5 v4"/></g>')
IKON_KALENDER = (f'<g stroke="{MAG}" stroke-width="2.6" fill="none" stroke-linecap="round">'
                 '<rect x="-13" y="-11" width="26" height="24" rx="4"/><path d="M-13 -3 h26 M-7 -15 v7 M7 -15 v7"/>'
                 f'</g><g fill="{MAG}"><rect x="-8" y="2" width="4" height="4" rx="1"/><rect x="-2" y="2" width="4" height="4" rx="1"/>'
                 '<rect x="4" y="2" width="4" height="4" rx="1"/><rect x="-8" y="7" width="4" height="4" rx="1"/></g>')
IKON_KELUARGA = (f'<g stroke="{TEAL}" stroke-width="2.6" fill="none" stroke-linecap="round">'
                 '<circle cx="0" cy="-6" r="6"/><path d="M-11 12 q0 -10 11 -10 q11 0 11 10 z"/>'
                 '<circle cx="-13" cy="-3" r="4.5"/><path d="M-21 11 q0 -8 8 -8"/>'
                 '<circle cx="13" cy="-3" r="4.5"/><path d="M21 11 q0 -8 -8 -8"/></g>')
IKON_HATI = (f'<path d="M0 11 C-17 0 -13 -13 -5 -12 C-2 -12 0 -9 0 -7 C0 -9 2 -12 5 -12 C13 -13 17 0 0 11 Z" '
             f'stroke="{MAG}" stroke-width="2.8" fill="none" stroke-linejoin="round"/>')


def perisai_3d():
    """Ilustrasi cover: perisai 3D toska dengan centang magenta, orbit, dan kartu ikon."""
    perisai = "M195 70 C232 92 268 102 300 104 C300 210 262 286 195 326 C128 286 90 210 90 104 C122 102 158 92 195 70 Z"
    dalam = "M195 96 C226 113 254 121 278 123 C278 211 247 271 195 303 C143 271 112 211 112 123 C136 121 164 113 195 96 Z"
    orbit = 'transform="rotate(-14 195 205)"'
    return (
        '<svg viewBox="0 0 390 370" width="100%" style="display:block;" xmlns="http://www.w3.org/2000/svg"><defs>'
        '<linearGradient id="pr-luar" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#CFF4F8"/>'
        '<stop offset=".55" stop-color="#A6E6EE"/><stop offset="1" stop-color="#7FD3DF"/></linearGradient>'
        '<linearGradient id="pr-dalam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F4FDFE"/>'
        '<stop offset=".5" stop-color="#E3F8FB"/><stop offset=".5" stop-color="#D2F2F7"/><stop offset="1" stop-color="#C4EDF3"/></linearGradient>'
        f'<linearGradient id="pr-centang" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F45A9F"/><stop offset="1" stop-color="{MAG}"/></linearGradient>'
        f'<linearGradient id="pr-orbit" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{MAG}"/>'
        '<stop offset=".7" stop-color="#E84A93"/><stop offset="1" stop-color="#F6A8CB"/></linearGradient>'
        '<filter id="bayang-kartu" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="6" stdDeviation="7" '
        'flood-color="#7AA7B4" flood-opacity=".22"/></filter>'
        '<filter id="bayang-perisai" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="12" stdDeviation="12" '
        'flood-color="#5FB8C6" flood-opacity=".35"/></filter>'
        '<filter id="kabur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter></defs>'
        '<ellipse cx="195" cy="342" rx="92" ry="12" fill="#8FC9D2" opacity=".35" filter="url(#kabur)"/>'
        # orbit bagian belakang
        f'<path d="M58 205 A137 44 0 0 1 332 205" {orbit} stroke="url(#pr-orbit)" stroke-width="4" fill="none" opacity=".75"/>'
        # perisai
        f'<path d="{perisai}" fill="url(#pr-luar)" filter="url(#bayang-perisai)"/>'
        f'<path d="{dalam}" fill="url(#pr-dalam)"/>'
        '<path d="M195 96 C164 113 136 121 112 123 C112 150 116 175 123 197 C150 160 175 128 195 96 Z" fill="#FFFFFF" opacity=".45"/>'
        '<path d="M158 196 L186 226 L240 160" stroke="#B90F62" stroke-width="30" fill="none" stroke-linecap="round" '
        'stroke-linejoin="round" transform="translate(3 6)" opacity=".25"/>'
        '<path d="M158 196 L186 226 L240 160" stroke="url(#pr-centang)" stroke-width="30" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M164 194 L184 216" stroke="#FFFFFF" stroke-width="5" opacity=".35" stroke-linecap="round"/>'
        # orbit bagian depan + titik
        f'<path d="M332 205 A137 44 0 0 1 58 205" {orbit} stroke="url(#pr-orbit)" stroke-width="4" fill="none"/>'
        f'<g {orbit} fill="{MAG}"><circle cx="58" cy="205" r="9"/><circle cx="332" cy="205" r="9"/><circle cx="170" cy="248" r="10"/></g>'
        + _kartu_ikon(62, 80, IKON_SUNTIK) + _kartu_ikon(326, 66, IKON_KALENDER, 52)
        + _kartu_ikon(338, 238, IKON_KELUARGA, 62) + _kartu_ikon(62, 312, IKON_HATI, 56)
        + '</svg>')


def ombak_cover():
    """Gelombang lembut toska (kiri) & merah muda (kanan) di dasar layar cover."""
    return ('<svg viewBox="0 0 390 260" preserveAspectRatio="none" width="100%" height="100%" style="display:block;" '
            'xmlns="http://www.w3.org/2000/svg"><defs>'
            '<linearGradient id="om-t" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#C9EFF1"/>'
            '<stop offset="1" stop-color="#E9F8F9" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="om-p" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FDEAF3" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#FAD6E6"/></linearGradient></defs>'
            '<path d="M0 40 C90 10 170 60 250 130 C290 165 320 210 340 260 H0 Z" fill="url(#om-t)"/>'
            '<path d="M390 70 C300 80 210 150 140 260 H390 Z" fill="url(#om-p)"/></svg>')
