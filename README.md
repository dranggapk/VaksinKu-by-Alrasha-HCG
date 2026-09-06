# VaksinKu — Prototipe Aplikasi

Prototipe UI/UX aplikasi **VaksinKu by Alrasha Ibumas**: platform digital layanan
vaksinasi keluarga (booking, rekam medis, konsultasi, dan modul korporat/sekolah).

## Cara membuka

Unduh **`VaksinKu-App.html`**, lalu klik dua kali file tersebut — akan langsung
terbuka di browser (Chrome, Edge, Safari, Firefox). Tidak butuh instalasi,
server, atau koneksi internet: logo, ikon, dan font sudah tertanam di dalam file.

## Isi prototipe

Sembilan layar yang bisa diklik:

| # | Layar | Isi utama |
|---|-------|-----------|
| 1 | Splash | Logo + tagline `#VaksinKeluargaJadiMudah` |
| 2 | Onboarding | Pilih kebutuhan: anak / dewasa / Umroh–Haji / lansia |
| 3 | Login | Google Sign-In + opsi nomor HP (OTP) |
| 4 | Beranda | Status booking aktif, reminder jadwal, tumbuh kembang, banner musiman |
| 5 | Booking | Form satu alur + estimasi biaya transparan sebelum konfirmasi |
| 6 | Rekam Medis | Kartu vaksinasi digital, status IDL, grafik tumbuh kembang |
| 7 | Chat | Konsultasi dokter + live chat CS 24 jam |
| 8 | Profil | Poin Sehat, daftar pasien, alamat, invoice |
| 9 | Korporat | Dashboard cakupan vaksinasi sekolah, booking massal, laporan |

Navigasi: bottom nav, tombol **+** di tengah, dan baris pintasan di atas
bingkai ponsel untuk melompat ke layar mana pun.

Prototipe ini hanya front-end (tanpa backend/basis data). Aksi yang belum
punya layar sendiri menampilkan notifikasi kecil "akan tersedia di versi lengkap".

## Identitas visual

| Elemen | Nilai |
|--------|-------|
| Teal | `#56C3C7` (aksen sekunder, ikon, chip) |
| Magenta | `#D11972` (CTA utama, state terpilih) |
| Abu teks | `#262626` / `#606060` |
| Font display | Baloo 2 (judul, angka, tombol) |
| Font teks | Plus Jakarta Sans |

Palet dan tipografi diambil dari logo VaksinKu.

## Struktur repositori

```
VaksinKu-App.html   Prototipe siap pakai (satu file, self-contained)
src/                Generator prototipe (Python) + aset logo
  gen.py            Design system: token warna, pustaka ikon SVG, bottom nav
  build_app.py      Menyusun 9 layar + CSS + JS menjadi satu file HTML
  embed_fonts.py    Menanam font Baloo 2 & Plus Jakarta Sans sebagai data URI
mockup/             Versi artboard statis (.dc.html) untuk kanvas desain
```

### Membangun ulang

```bash
cd src
python3 build_app.py     # → src/vaksinku-app.html (font dimuat dari Google Fonts)
python3 embed_fonts.py   # → src/VaksinKu-App.html (font tertanam, siap offline)
cp VaksinKu-App.html ..  # perbarui file di root repositori
```

`embed_fonts.py` mengunduh font dari Google Fonts saat dijalankan, jadi langkah
ini butuh koneksi internet (hasil akhirnya tidak).

## Catatan

Nomor WhatsApp CS pada layar Login masih placeholder `[Nomor CS VaksinKu]` —
ganti dengan nomor asli sebelum dipakai untuk presentasi eksternal.
