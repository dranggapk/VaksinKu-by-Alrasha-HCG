#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mockup alternatif ikon aplikasi VaksinKu (layar utama HP).

Semua ikon digambar sebagai SVG 1024×1024 dari geometri simbol "V" pada logo
(situs/ikon/ikon.svg), lalu ditampilkan dalam beberapa bentuk: kotak membulat
(iPhone), lingkaran (Android), ukuran kecil, dan di layar utama HP.

    python3 mockup/build_ikon.py   → mockup/ikon-alternatif.html + .png
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "src"))
import build_bundle as B  # noqa: E402

TEAL, TEAL_D, MAG = "#38BCBD", "#1F8C8E", "#DC106E"


def simbol_v(garis=TEAL, titik=MAG, inti=TEAL, tebal=54, tepi=None):
    """Simbol V dalam koordinat logo (±0–420 × 0–440), pusat visual (212, 228)."""
    t = f' stroke="{tepi}" stroke-width="14"' if tepi else ""
    return (f'<g stroke="{garis}" stroke-width="{tebal}" stroke-linecap="round">'
            f'<line x1="52" y1="58" x2="212" y2="383"/><line x1="375" y1="57" x2="212" y2="383"/></g>'
            f'<circle cx="52" cy="58" r="44" fill="{titik}"{t}/><circle cx="375" cy="57" r="44" fill="{titik}"{t}/>'
            f'<circle cx="212" cy="383" r="58" fill="{titik}"{t}/><circle cx="212" cy="383" r="21" fill="{inti}"/>')


def taruh(isi, skala=1.36, dx=0, dy=0):
    return f'<g transform="translate({512+dx} {512+dy}) scale({skala}) translate(-212 -228)">{isi}</g>'


def svg(isi, defs=""):
    return f'<svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg"><defs>{defs}</defs>{isi}</svg>'


GRAD_TEAL = (f'<linearGradient id="gt" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4FCFCF"/>'
             f'<stop offset="1" stop-color="{TEAL_D}"/></linearGradient>')
GRAD_MAG = ('<linearGradient id="gm" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F0368C"/>'
            '<stop offset="1" stop-color="#A80D55"/></linearGradient>')

IKON = [
    ("A", "Klasik Putih", "Yang terpasang sekarang. Bersih, paling setia pada logo; menonjol di wallpaper gelap.",
     svg('<rect width="1024" height="1024" fill="#FFFFFF"/>' + taruh(simbol_v()))),
    ("B", "Toska Penuh", "Latar toska bergradasi, garis V putih, titik magenta. Paling mudah dikenali di antara ikon lain.",
     svg('<rect width="1024" height="1024" fill="url(#gt)"/>' + taruh(simbol_v("#FFFFFF", MAG, "#FFFFFF", tepi="#FFFFFF")), GRAD_TEAL)),
    ("C", "Magenta Penuh", "Latar magenta, garis V putih, titik toska. Warna hangat, selaras dengan nuansa ibu & anak.",
     svg('<rect width="1024" height="1024" fill="url(#gm)"/>' + taruh(simbol_v("#FFFFFF", TEAL, "#FFFFFF", tepi="#FFFFFF")), GRAD_MAG)),
    ("D", "V + Garis Logo", "Simbol V dengan garis bawah dan lingkaran target seperti pada logo lengkap.",
     svg('<rect width="1024" height="1024" fill="#FFFFFF"/>' + taruh(
         f'<path d="M212 383 V470 H520" stroke="{TEAL}" stroke-width="30" fill="none" stroke-linejoin="round"/>'
         f'<circle cx="548" cy="470" r="44" fill="{MAG}"/><circle cx="548" cy="470" r="26" fill="#FFFFFF"/>'
         f'<circle cx="548" cy="470" r="13" fill="{MAG}"/>' + simbol_v(), 1.12, -98, -40))),
    ("E", "Perisai", "Simbol V di dalam perisai, senada dengan halaman cover. Pesan: perlindungan keluarga.",
     svg('<rect width="1024" height="1024" fill="#E8F8F8"/>'
         f'<path d="M512 150 L812 262 Q812 690 512 874 Q212 690 212 262 Z" fill="{TEAL}"/>'
         f'<path d="M512 204 L760 298 Q760 660 512 814 Q264 660 264 298 Z" fill="#FFFFFF"/>'
         + taruh(simbol_v(), 0.82, 0, -12))),
    ("F", "V · Ku", "Simbol V ditambah tulisan “Ku” magenta, langsung terbaca sebagai VaksinKu.",
     svg('<rect width="1024" height="1024" fill="#FFFFFF"/>' + taruh(simbol_v(), 0.9, -190, -10)
         + f'<text x="700" y="640" font-family="Baloo 2, sans-serif" font-weight="800" font-size="330" fill="{MAG}" '
           f'text-anchor="middle">Ku</text>')),
]

LAIN = [("#4CAF50", "Telepon"), ("#2196F3", "Pesan"), ("#FF9800", "Kamera"), ("#9C27B0", "Galeri"),
        ("#25D366", "WhatsApp"), ("#EA4335", "Gmail"), ("#607D8B", "Setelan")]


def kartu(kode, nama, ket, s):
    return (f'<div class="kartu"><div class="kode">{kode}</div><div class="nama">{nama}</div>'
            f'<div class="baris"><div class="ios">{s}</div><div class="android">{s}</div>'
            f'<div class="kecil"><div>{s}</div><div>{s}</div></div></div>'
            f'<div class="ket">{ket}</div></div>')


def layar(kode, s, gelap):
    sel = []
    for i in range(12):
        if i == 5:
            sel.append(f'<div class="app"><div class="ik">{s}</div><span>VaksinKu</span></div>')
        else:
            w, n = LAIN[i % len(LAIN)]
            sel.append(f'<div class="app"><div class="ik" style="background:{w};opacity:.85;"></div><span>{n}</span></div>')
    latar = ("linear-gradient(160deg,#20304A,#3A2E5A 60%,#1D3B44)" if gelap
             else "linear-gradient(160deg,#F6D9E4,#D9EEF0 60%,#F3EAD8)")
    warna = "#fff" if gelap else "#2A2A33"
    return (f'<div class="hp" style="background:{latar};color:{warna};"><div class="jam">08.18</div>'
            f'<div class="grid">{"".join(sel)}</div><div class="cap">{kode}</div></div>')


CSS = """
*{box-sizing:border-box;margin:0;padding:0;}
body{background:#EEF0F2;font-family:'Plus Jakarta Sans',sans-serif;color:#1E2A32;padding:36px 28px 50px;}
h1{font-family:'Baloo 2',sans-serif;font-size:30px;text-align:center;}
h2{font-family:'Baloo 2',sans-serif;font-size:21px;margin:34px 0 14px;text-align:center;}
.pengantar{max-width:900px;margin:6px auto 26px;text-align:center;color:#5A6670;font-size:15px;line-height:1.6;}
.deret{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;max-width:1240px;margin:0 auto;}
.kartu{background:#fff;border-radius:22px;padding:18px 18px 16px;box-shadow:0 6px 20px rgba(0,0,0,.06);position:relative;}
.kode{position:absolute;top:16px;right:18px;font-family:'Baloo 2',sans-serif;font-weight:800;font-size:22px;color:#C7CDD3;}
.nama{font-family:'Baloo 2',sans-serif;font-weight:800;font-size:19px;margin-bottom:12px;}
.baris{display:flex;align-items:center;gap:18px;}
.ios svg,.ios{width:132px;height:132px;border-radius:30px;overflow:hidden;display:block;flex-shrink:0;}
.android svg,.android{width:112px;height:112px;border-radius:50%;overflow:hidden;display:block;flex-shrink:0;}
.ios,.android{box-shadow:0 0 0 1px rgba(0,0,0,.06),0 6px 14px rgba(0,0,0,.10);}
.kecil{display:flex;flex-direction:column;gap:10px;}
.kecil div{width:44px;height:44px;border-radius:11px;overflow:hidden;box-shadow:0 0 0 1px rgba(0,0,0,.08);}
.kecil div:last-child{width:28px;height:28px;border-radius:7px;}
.kecil svg{width:100%;height:100%;display:block;}
.ket{font-size:13px;color:#5A6670;line-height:1.55;margin-top:12px;}
.layar{display:flex;flex-wrap:wrap;gap:18px;justify-content:center;}
.hp{width:180px;height:370px;border-radius:30px;padding:22px 8px;position:relative;box-shadow:0 0 0 7px #1E2328,0 14px 30px rgba(0,0,0,.25);}
.jam{text-align:center;font-family:'Baloo 2',sans-serif;font-size:34px;font-weight:700;margin-bottom:14px;}
.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px 4px;}
.app{display:flex;flex-direction:column;align-items:center;gap:4px;}
.app span{font-size:8px;font-weight:600;white-space:nowrap;}
.ik{width:34px;height:34px;border-radius:9px;overflow:hidden;}
.ik svg{width:100%;height:100%;display:block;}
.cap{position:absolute;bottom:12px;left:0;right:0;text-align:center;font-family:'Baloo 2',sans-serif;font-weight:800;opacity:.75;}
"""


def main():
    kartu_html = "".join(kartu(*x) for x in IKON)
    layar_html = "".join(layar(k, s, i % 2 == 0) for i, (k, _, _, s) in enumerate(IKON))
    html = (f'<!doctype html><html lang="id"><head><meta charset="utf-8"><title>Ikon VaksinKu — Alternatif</title>'
            f'<style>{B.font_css()}</style><style>{CSS}</style></head><body>'
            f'<h1>Alternatif Ikon Aplikasi VaksinKu</h1>'
            f'<div class="pengantar">Setiap ikon ditampilkan sebagai kotak membulat (iPhone), lingkaran (sebagian Android), '
            f'dan ukuran kecil seperti di notifikasi/tab browser. Semua digambar dari simbol “V” pada logo '
            f'<b>VaksinKu by Alrasha HCC</b>, sehingga tetap tajam di semua ukuran.</div>'
            f'<div class="deret">{kartu_html}</div>'
            f'<h2>Di layar utama HP (wallpaper gelap &amp; terang bergantian)</h2>'
            f'<div class="layar">{layar_html}</div></body></html>')
    out = os.path.join(HERE, "ikon-alternatif.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    png = os.path.join(HERE, "ikon-alternatif.png")
    subprocess.run(["/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
                    "--hide-scrollbars", "--window-size=1300,1300", "--virtual-time-budget=3000", "--screenshot=" + png,
                    "file://" + out], capture_output=True, timeout=120)
    print("wrote", out, "dan", png)


if __name__ == "__main__":
    main()
