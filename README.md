# VaksinKu — Prototipe Aplikasi

Prototipe UI/UX aplikasi **VaksinKu by Alrasha Ibumas**: platform digital layanan
vaksinasi keluarga (booking, rekam medis, konsultasi, dan modul korporat/sekolah).

## Cara membuka

Unduh **`VaksinKu-App.html`**, lalu klik dua kali file tersebut — akan langsung
terbuka di browser (Chrome, Edge, Safari, Firefox). Tidak butuh instalasi,
server, atau koneksi internet: logo, ikon, dan font sudah tertanam di dalam file.

## Isi prototipe

Sembilan layar yang bisa diklik:

Tiga belas layar yang bisa diklik:

| # | Layar | Isi utama |
|---|-------|-----------|
| 1 | Splash | Logo + tagline `#VaksinKeluargaJadiMudah` |
| 2 | Onboarding | Pilih segmen: anak, anak sekolah, dewasa, pranikah, lansia, internasional |
| 3 | Login | Google Sign-In + opsi nomor HP (OTP) |
| 4 | Beranda | Booking aktif, reminder, pintasan harga/jadwal/internasional, 3 jenis layanan, promo |
| 5 | Booking | Form satu alur: layanan, pilihan dokter umum/spesialis, jadwal, biaya transparan |
| 6 | Rekam Medis | Kartu vaksinasi digital, status IDL, grafik tumbuh kembang |
| 7 | Chat | Konsultasi dokter + live chat CS 24 jam |
| 8 | Profil | Poin Sehat, daftar pasien, akses harga/jadwal/lokasi, invoice |
| 9 | Korporat | Dashboard cakupan vaksinasi sekolah, booking massal, laporan |
| 10 | Daftar Harga | Price list 17 kategori vaksin, toggle dokter umum ↔ spesialis |
| 11 | Jadwal Vaksin | Tab anak (IDAI 2024), dewasa (PAPDI 2025), pranikah, lansia |
| 12 | Vaksin Internasional | Vaksin wajib haji/umrah, tambahan WHO, harga & paket promo, e-ICV |
| 13 | Tentang & Lokasi | Pilar Aman–Lengkap–Terjangkau, 3 layanan, alur reservasi, dokter, 3 klinik |

Navigasi: bottom nav, tombol **+** di tengah, dan baris pintasan di atas
bingkai ponsel untuk melompat ke layar mana pun.

Prototipe ini hanya front-end (tanpa backend/basis data). Aksi yang belum
punya layar sendiri menampilkan notifikasi kecil "akan tersedia di versi lengkap".

## Sumber data

Seluruh isi harga, jadwal vaksin, layanan, dokter, dan lokasi klinik diambil
dari katalog resmi VaksinKu by Alrasha Ibumas (16 halaman) dan disimpan
terpusat di `src/data_katalog.py`, sehingga pembaruan katalog cukup dilakukan
di satu berkas lalu di-build ulang.

Rujukan yang dipakai di dalam aplikasi:

- Jadwal vaksin anak — **IDAI terbaru 2024**
- Jadwal vaksin dewasa — **rekomendasi PAPDI 2025**
- Vaksin haji & umrah — regulasi Arab Saudi + rekomendasi tambahan WHO
- Call center & booking — **0811-7744-74**

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
  data_katalog.py   Isi katalog: harga, jadwal vaksin, layanan, dokter, klinik
  build_app.py      Menyusun 13 layar + CSS + JS menjadi satu file HTML
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

Pada katalog halaman "Jadwal Vaksin Anak", kotak **0 bulan (lahir)** memuat
dua butir yang sama-sama tertulis "Hep B 0". Di aplikasi butir tersebut
ditampilkan satu kali; mohon dikonfirmasi apakah butir kedua seharusnya
"Polio 0" agar bisa diperbaiki.

Harga **Meningitis (Menivax)** untuk dokter spesialis tidak tercantum di
katalog, sehingga pada tarif dokter spesialis ditampilkan sebagai
"Hubungi CS".
