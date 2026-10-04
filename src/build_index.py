#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merakit index.html dari rancangan Claude Design di folder design/.

Tiap artboard (.dc.html) dibuka kembali sebagai HTML biasa, gaya bersamanya
dipakai satu kali dan dikurung agar tidak bocor ke halaman pembungkus, dan
logonya ditanam sebagai data URI. Hasilnya satu berkas index.html yang berdiri
sendiri — bisa dibuka langsung atau ditaruh di hosting mana pun.

    python3 build_index.py [--tanpa-font]
"""
import base64
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DESAIN = os.path.join(ROOT, "design")
sys.path.insert(0, HERE)

import data_katalog as D  # noqa: E402
from build_bundle import font_css, FONT_CSS_URL  # noqa: E402

# Keterangan tiap layar — ditulis dari konsep VaksinKu dan katalog resminya.
KETERANGAN = {
    "Splash.dc.html": "Pembuka dengan logo dan tagline #VaksinKeluargaJadiMudah.",
    "Onboarding.dc.html": "Pengguna memilih kebutuhannya dulu: anak, dewasa, pranikah, lansia, atau internasional.",
    "Login.dc.html": "Masuk satu ketukan lewat Google, atau nomor HP bagi yang tidak memakai akun Google.",
    "Main.dc.html": "Beranda: status booking aktif, pengingat jadwal, pintasan harga dan jadwal, serta promo musiman.",
    "Booking.dc.html": "Form satu alur. Estimasi biaya tampil sejak awal — perbaikan utama dari aplikasi pembanding.",
    "RekamMedis.dc.html": "Kartu vaksinasi digital, status kelengkapan IDL, dan grafik tumbuh kembang anak.",
    "Chat.dc.html": "Konsultasi dokter dan bantuan CS dalam satu tempat.",
    "Profile.dc.html": "Poin Sehat, daftar pasien satu keluarga, alamat, dan riwayat invoice.",
    "Korporat.dc.html": "Diferensiator VaksinKu: dashboard cakupan sekolah/kantor, booking massal, laporan Dinkes.",
}
TINGGI_LAYAR = 844  # tinggi jendela ponsel; layar yang lebih panjang digulir di dalam bingkai

# Rancangan di kanvas dibuat sebelum katalog resmi tersedia, sehingga masih
# memuat data contoh yang ikut terbawa dari screenshot aplikasi pembanding.
# Halaman ini terbuka untuk umum, jadi data tersebut diluruskan saat dirakit —
# nilai penggantinya sama dengan yang dipakai aplikasi yang berjalan.
# Urutan penting: teks terpanjang diganti lebih dulu.
KOREKSI = [
    # data pribadi orang lain yang tidak boleh ikut terbit
    ("dr.angga.pk@gmail.com", "keluarga@contoh.com"),
    ("Angga Perdana", "Sari Contoh"),
    ("Keluarga Perdana", "Keluarga Contoh"),
    # dokter: pakai nama asli dari katalog Alrasha Ibumas
    ("dr. Melati Anggraini, Sp.A", "dr. Dwi Fachri JH, Sp.A"),
    ("dr. Melati Anggraini", "dr. Dwi Fachri JH, Sp.A"),
    ("dr. Bagas Wirawan, Sp.PD", "dr. Leo Andreas, Sp.PD"),
    ("dr. Bagas Wirawan", "dr. Leo Andreas, Sp.PD"),
    # klinik & alamat: VaksinKu beroperasi di Tanjungpinang
    ("Klinik Sunter", "Klinik Utama Alrasha Ibumas"),
    ("Jl. Gurame No. 5, Lengkong, Kota Bandung", "Jl. Hang Lekir, Batu 10, Tanjungpinang"),
    # jam operasional tidak pernah disebut di katalog VaksinKu
    ("Dokter online: Senin–Jumat 09.00–17.00 · Sabtu 09.00–12.00",
     "Konsultasi dokter lewat Call Center " + D.BRAND["call_center"]),
    # nomor CS sudah diketahui dari katalog
    ("[Nomor CS VaksinKu]", D.BRAND["call_center"]),
]


def baca(nama):
    with open(os.path.join(DESAIN, nama), encoding="utf-8") as f:
        return f.read()


def data_uri(nama):
    with open(os.path.join(DESAIN, nama), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")


def kurung_css(css, lingkup):
    """Kurung gaya artboard ke dalam satu lingkup agar tidak mengenai halaman.

    :root → lingkup (variabel ikut pindah), aturan html/body dibuang karena
    halaman pembungkus yang memilikinya, sisanya diberi awalan lingkup.
    """
    hasil = []
    for blok in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        pemilih, isi = blok[0].strip(), blok[1].strip()
        if not pemilih or not isi:
            continue
        baru = []
        for satu in [p.strip() for p in pemilih.split(",")]:
            if satu in (":root",):
                baru.append(lingkup)
            elif satu in ("html", "body", "html,body"):
                continue
            else:
                baru.append(lingkup + " " + satu)
        if baru:
            hasil.append(", ".join(baru) + "{" + isi + "}")
    return "\n".join(hasil)


def isi_artboard(nama, gambar):
    """Ambil badan artboard, buang pembungkus khas Design Component."""
    mentah = baca(nama)
    badan = re.search(r"<x-dc>([\s\S]*?)</x-dc>", mentah).group(1)
    badan = re.sub(r"<helmet>[\s\S]*?</helmet>", "", badan).strip()
    for berkas, uri in gambar.items():
        badan = badan.replace('src="%s"' % berkas, 'src="%s"' % uri)
        badan = badan.replace('src="./%s"' % berkas, 'src="%s"' % uri)
    for lama, baru in KOREKSI:
        badan = badan.replace(lama, baru)
    return badan


def main():
    tanpa_font = "--tanpa-font" in sys.argv
    kanvas = json.loads(baca("canvas.json"))
    gambar = {n: data_uri(n) for n in os.listdir(DESAIN) if n.lower().endswith(".png")}

    # satu blok gaya dipakai bersama oleh seluruh artboard
    contoh = baca(kanvas["artboards"][0]["file"])
    helmet = re.search(r"<helmet>([\s\S]*?)</helmet>", contoh).group(1)
    css_artboard = kurung_css(re.search(r"<style>([\s\S]*?)</style>", helmet).group(1), ".vk-layar")

    kartu = []
    for i, ab in enumerate(kanvas["artboards"], 1):
        nama = ab["file"]
        judul = re.sub(r"^\d+\.\s*", "", ab.get("title") or nama.replace(".dc.html", ""))
        panjang = ab.get("h", TINGGI_LAYAR) > 900   # 890 = bingkai satu layar penuh
        kartu.append(
            '<figure class="vk-kartu">'
            '<div class="vk-kepala"><span class="vk-no">%02d</span>'
            '<h3>%s</h3>%s</div>'
            '<div class="vk-ponsel"><div class="vk-layar">%s</div></div>'
            '<figcaption>%s</figcaption>'
            "</figure>"
            % (i, judul,
               '<span class="vk-gulir">gulir di dalam layar</span>' if panjang else "",
               isi_artboard(nama, gambar),
               KETERANGAN.get(nama, ""))
        )

    if tanpa_font:
        font = ('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
                '<link href="%s" rel="stylesheet">' % FONT_CSS_URL)
    else:
        print("mengambil font...")
        font = "<style>\n" + font_css() + "\n</style>"

    B = D.BRAND
    halaman = HALAMAN % {
        "font": font,
        "css_artboard": css_artboard,
        "logo": gambar["vaksinku-logo.png"],
        "tagline": B["tagline"],
        "grup": B["group"],
        "telepon": B["call_center"],
        "ig": B["instagram"],
        "web": B["website"],
        "jumlah": len(kanvas["artboards"]),
        "kartu": "\n".join(kartu),
    }
    keluar = os.path.join(ROOT, "index.html")
    with open(keluar, "w", encoding="utf-8") as f:
        f.write(halaman)
    print("wrote %s — %.0f KB, %d layar" % (keluar, os.path.getsize(keluar) / 1024, len(kanvas["artboards"])))


HALAMAN = """<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VaksinKu — Rancangan Aplikasi</title>
<meta name="description" content="Rancangan antarmuka aplikasi VaksinKu by Alrasha Ibumas: %(jumlah)d layar, dari splash sampai modul korporat.">
<meta name="theme-color" content="#2E9BA0">
%(font)s
<style>
:root{
  --teal:#56C3C7; --teal-dark:#2E9BA0; --teal-tint:#E9F9FA;
  --magenta:#D11972; --magenta-dark:#A81260; --magenta-tint:#FDECF3;
  --ink:#262626; --ink-2:#4B4B4B; --ink-3:#606060; --ink-4:#9AA0A6;
  --line:#E6E5E1; --kertas:#F4F3EF; --kartu:#FFFFFF;
  --disp:'Baloo 2',ui-rounded,'Segoe UI',sans-serif;
  --teks:'Plus Jakarta Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{
  margin:0;background:var(--kertas);color:var(--ink);font-family:var(--teks);
  font-size:15px;line-height:1.6;-webkit-font-smoothing:antialiased;
}
img{display:block;max-width:100%%;}
a{color:var(--magenta-dark);}
.vk-bungkus{max-width:1340px;margin:0 auto;padding:0 20px;}

/* --- kepala halaman --- */
.vk-atas{padding:56px 0 40px;text-align:center;}
.vk-atas img{width:230px;margin:0 auto 22px;}
.vk-atas .vk-tag{
  display:inline-block;font-size:12.5px;font-weight:700;letter-spacing:.04em;
  color:var(--teal-dark);background:var(--teal-tint);border-radius:999px;padding:7px 16px;
}
.vk-atas h1{
  font-family:var(--disp);font-size:clamp(28px,5vw,40px);font-weight:800;
  margin:20px 0 10px;line-height:1.2;text-wrap:balance;
}
.vk-atas p{max-width:62ch;margin:0 auto;color:var(--ink-2);}
.vk-aksi{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:26px;}
.vk-btn{
  font-family:var(--disp);font-weight:700;font-size:15px;border-radius:999px;
  padding:13px 24px;text-decoration:none;display:inline-flex;align-items:center;gap:9px;
}
.vk-btn.utama{background:var(--magenta);color:#fff;}
.vk-btn.utama:hover{background:var(--magenta-dark);}
.vk-btn.garis{background:#fff;border:1.6px solid var(--teal);color:var(--teal-dark);}
.vk-btn.garis:hover{background:var(--teal-tint);}

/* --- galeri layar --- */
.vk-galeri{
  display:grid;gap:42px 28px;padding:26px 0 64px;justify-items:center;
  grid-template-columns:repeat(auto-fill,minmax(min(414px,100%%),1fr));
}
.vk-kartu{margin:0;width:414px;max-width:100%%;}
.vk-kepala{display:flex;align-items:baseline;gap:10px;margin-bottom:14px;flex-wrap:wrap;}
.vk-no{
  font-family:var(--disp);font-size:13px;font-weight:800;color:#fff;background:var(--teal-dark);
  border-radius:999px;padding:3px 10px;
}
.vk-kepala h3{font-family:var(--disp);font-size:18px;font-weight:800;margin:0;}
.vk-gulir{font-size:11px;color:var(--ink-4);border:1px solid var(--line);border-radius:999px;padding:2px 9px;}
.vk-ponsel{
  width:414px;max-width:100%%;padding:12px;border-radius:38px;
  background:linear-gradient(160deg,#22252A,#111214);
  box-shadow:0 26px 50px -24px rgba(20,20,20,.5),0 8px 20px -12px rgba(20,20,20,.3);
}
.vk-layar{
  width:390px;max-width:100%%;height:%(tinggi)spx;border-radius:28px;overflow:hidden auto;background:#FAFAF9;
  scrollbar-width:thin;scrollbar-color:#C9C8C3 transparent;
}
.vk-layar::-webkit-scrollbar{width:5px;}
.vk-layar::-webkit-scrollbar-thumb{background:#C9C8C3;border-radius:3px;}
.vk-kartu figcaption{
  font-size:13px;color:var(--ink-3);line-height:1.6;margin-top:14px;max-width:46ch;
}

/* --- gaya artboard, dikurung agar tidak bocor ke halaman --- */
%(css_artboard)s
.vk-layar .frame{min-height:100%%;}

/* --- catatan & kaki --- */
.vk-catatan{
  background:#fff;border:1px solid var(--line);border-radius:20px;padding:24px;margin-bottom:56px;
}
.vk-catatan h2{font-family:var(--disp);font-size:19px;font-weight:800;margin:0 0 10px;}
.vk-catatan p{margin:0 0 10px;color:var(--ink-2);font-size:14px;}
.vk-catatan p:last-child{margin-bottom:0;}
.vk-kaki{
  background:var(--teal-dark);color:#fff;padding:36px 0;
}
.vk-kaki .vk-bungkus{display:flex;gap:18px;flex-wrap:wrap;align-items:center;justify-content:space-between;}
.vk-kaki .vk-telp{font-family:var(--disp);font-size:22px;font-weight:800;}
.vk-kaki .vk-kecil{font-size:12.5px;opacity:.85;}
.vk-kaki a{color:#fff;text-decoration:underline;text-underline-offset:3px;}
@media (max-width:413px){
  /* layar rancangan lebarnya tetap 390px; pada ponsel sempit dikecilkan
     dengan zoom supaya tinggi gulirnya ikut menyesuaikan */
  .vk-ponsel{padding:8px;border-radius:30px;}
  .vk-layar{border-radius:22px;height:600px;}
  .vk-layar .frame{zoom:.86;}
}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto;}}
</style>
</head>
<body>

<header class="vk-atas">
  <div class="vk-bungkus">
    <img src="%(logo)s" alt="VaksinKu by Alrasha Ibumas">
    <span class="vk-tag">%(tagline)s</span>
    <h1>Rancangan Aplikasi VaksinKu</h1>
    <p>%(jumlah)d layar antarmuka untuk layanan vaksinasi keluarga %(grup)s — dari pembuka,
       pendaftaran, rekam medis, sampai modul korporat untuk sekolah dan kantor.</p>
    <div class="vk-aksi">
      <a class="vk-btn utama" href="VaksinKu-App.html">Buka aplikasi yang berjalan</a>
      <a class="vk-btn garis" href="#layar">Lihat rancangan layar</a>
    </div>
  </div>
</header>

<main class="vk-bungkus" id="layar">
  <div class="vk-galeri">
%(kartu)s
  </div>

  <section class="vk-catatan">
    <h2>Tentang halaman ini</h2>
    <p>Layar di atas adalah rancangan antarmuka — tampilannya nyata (HTML, bukan gambar),
       tetapi tombolnya belum berfungsi. Rancangan ini dipakai sebagai acuan desain.</p>
    <p>Aplikasi yang benar-benar berjalan ada di
       <a href="VaksinKu-App.html">VaksinKu-App.html</a>: data pasien tersimpan di perangkat,
       jadwal vaksin dihitung dari tanggal lahir, biaya dihitung dari price list resmi, dan
       reservasi dikirim ke WhatsApp untuk dikonfirmasi petugas.</p>
    <p>Harga, jadwal vaksin, dan data klinik mengikuti katalog resmi VaksinKu; jadwal anak
       memakai rujukan IDAI 2024 dan jadwal dewasa rekomendasi PAPDI 2025.</p>
  </section>
</main>

<footer class="vk-kaki">
  <div class="vk-bungkus">
    <div>
      <div class="vk-kecil">Call Center &amp; Booking</div>
      <div class="vk-telp">%(telepon)s</div>
    </div>
    <div class="vk-kecil">
      %(ig)s · <a href="https://%(web)s">%(web)s</a><br>%(grup)s
    </div>
  </div>
</footer>

</body>
</html>
"""
HALAMAN = HALAMAN.replace("%(tinggi)s", str(TINGGI_LAYAR))

if __name__ == "__main__":
    main()
