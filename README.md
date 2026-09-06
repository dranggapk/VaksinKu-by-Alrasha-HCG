# VaksinKu — Aplikasi Vaksinasi Keluarga

Aplikasi **VaksinKu by Alrasha Ibumas**: mengatur jadwal vaksinasi keluarga,
menyimpan rekam medis, dan membuat reservasi — dalam satu berkas HTML yang
berjalan langsung di browser.

## Cara memakai

Unduh **`VaksinKu-App.html`**, lalu klik dua kali — aplikasi langsung terbuka di
browser (Chrome, Edge, Safari, Firefox), di ponsel maupun komputer. Tidak butuh
instalasi, server, atau koneksi internet: logo, ikon, dan font sudah tertanam.

Bisa juga diletakkan di hosting mana pun (mis. GitHub Pages) dan dibuka lewat
tautan, atau ditambahkan ke layar utama ponsel lewat menu "Add to Home screen".

## Yang bisa dikerjakan aplikasi ini

| Fitur | Keterangan |
|---|---|
| **Profil pendaftar** | Nama & nomor HP, dipakai sebagai kontak reservasi |
| **Data pasien** | Tambah/ubah/hapus anggota keluarga; usia dihitung dari tanggal lahir |
| **Jadwal vaksin personal** | Ceklis otomatis menyesuaikan usia: anak mengikuti **IDAI 2024**, dewasa mengikuti **PAPDI 2025** (rentang usia dipilih otomatis) |
| **Kelengkapan vaksinasi** | Persentase dihitung dari vaksin yang sudah jatuh tempo vs yang sudah dicatat |
| **Reservasi** | Form tervalidasi: layanan, lokasi, pasien, dokter, vaksin, tanggal & jam |
| **Biaya nyata** | Total dihitung dari price list resmi; ganti dokter umum ↔ spesialis mengubah total seketika |
| **Kirim ke WhatsApp** | Ringkasan reservasi dikirim ke CS **0811-7744-74** dengan satu ketukan |
| **Rekam medis** | Riwayat vaksinasi per pasien, otomatis terisi saat reservasi ditandai selesai |
| **Tumbuh kembang** | Catat berat, tinggi, lingkar kepala; grafik berat badan terhadap usia |
| **Daftar harga** | 17 kategori vaksin, dengan pencarian dan pilihan tarif dokter |
| **Vaksin internasional** | Vaksin wajib haji/umrah, rekomendasi WHO, harga & paket promo, e-ICV |
| **Poin Sehat** | +10 poin setiap vaksinasi selesai |
| **Cadangkan & pulihkan** | Ekspor/impor seluruh data sebagai berkas `.json` |
| **Data contoh** | Sekali klik untuk mencoba aplikasi atau presentasi |

## Batasan yang perlu diketahui

- **Data tersimpan di perangkat**, bukan di server. Membersihkan data browser
  akan menghapusnya — gunakan menu *Cadangkan data* sebelum berganti perangkat.
- **Reservasi belum otomatis masuk sistem klinik.** Aplikasi menyusun ringkasan
  dan mengirimkannya ke WhatsApp CS untuk dikonfirmasi petugas. Untuk booking
  yang benar-benar otomatis dibutuhkan server dan integrasi jadwal klinik.
- **Slot waktu belum terhubung ketersediaan riil**; jadwal final dikonfirmasi CS.
- Grafik pertumbuhan menampilkan data pasien sendiri, belum dibandingkan dengan
  kurva WHO (butuh tabel standar WHO yang resmi).

## Sumber data

Harga, jadwal vaksin, layanan, dokter, dan lokasi klinik diambil dari katalog
resmi VaksinKu by Alrasha Ibumas (16 halaman) dan disimpan terpusat di
`src/data_katalog.py` — perbarui di satu berkas itu lalu build ulang.

Rujukan yang dipakai: jadwal anak **IDAI 2024**, jadwal dewasa **PAPDI 2025**,
vaksin haji & umrah sesuai regulasi Arab Saudi dengan tambahan rekomendasi WHO.

## Struktur repositori

```
VaksinKu-App.html    Aplikasi siap pakai (satu berkas, self-contained)
app/                 Sumber aplikasi
  index.html         Kerangka halaman
  styles.css         Design system: token warna, komponen, tata letak
  app.js             Logika: penyimpanan, rute, layar, perhitungan biaya
src/
  data_katalog.py    Isi katalog (harga, jadwal, layanan, dokter, klinik)
  build_bundle.py    Merakit semuanya + font & logo menjadi satu berkas HTML
  uji_app.py         Uji fungsional otomatis di browser headless (32 uji)
  tangkap_layar.py   Tangkap layar aplikasi dengan data contoh
  gen.py             Design system generator mockup statis (versi lama)
  build_app.py       Generator prototipe klik (versi lama)
mockup/              Artboard statis (.dc.html) untuk kanvas desain
katalog/             Halaman katalog hasil koreksi (lihat katalog/README.md)
```

### Membangun ulang

```bash
cd src
python3 build_bundle.py       # → VaksinKu-App.html (font tertanam, siap offline)
python3 build_bundle.py --tanpa-font   # lebih cepat, font dari Google Fonts
python3 uji_app.py            # jalankan 32 uji fungsional
```

`build_bundle.py` mengunduh font dari Google Fonts saat dijalankan, jadi langkah
ini butuh internet — hasil akhirnya tidak.

## Catatan katalog

Pada katalog halaman "Jadwal Vaksin Anak", kotak **0 bulan (lahir)** memuat dua
butir yang sama-sama tertulis "Hep B 0". Sesuai konfirmasi, butir kedua adalah
**Polio 0**; sudah diperbaiki di aplikasi dan pada halaman katalog revisi di
`katalog/`. Untuk kebutuhan cetak, koreksi yang sama masih perlu dilakukan pada
berkas desain master.

Harga **Meningitis (Menivax)** untuk dokter spesialis tidak tercantum di katalog,
sehingga pada tarif spesialis ditampilkan sebagai "Hubungi CS".
