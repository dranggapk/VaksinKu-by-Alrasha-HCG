# VaksinKu — Aplikasi Vaksinasi Keluarga

Aplikasi **VaksinKu by Alrasha Ibumas**: mengatur jadwal vaksinasi keluarga,
menyimpan rekam medis, dan membuat reservasi — dalam satu berkas HTML yang
berjalan langsung di browser.

## Cara memakai

Repositori ini berisi dua berkas siap pakai:

| Berkas | Isi |
|---|---|
| **`index.html`** | Halaman muka: 9 layar rancangan antarmuka, diambil dari kanvas Claude Design |
| **`VaksinKu-App.html`** | Aplikasi pasien — untuk keluarga yang divaksin |
| **`VaksinKu-Dashboard.html`** | Dashboard manajemen — untuk petugas klinik |

Ketiganya berdiri sendiri — klik dua kali untuk membuka di browser, atau unggah
seluruh folder ke hosting (GitHub Pages dan sejenisnya langsung menyajikan
`index.html`). Aplikasi pasien dipakai keluarga di ponsel; dashboard dipakai
petugas klinik di komputer. Keduanya menyimpan data terpisah di perangkat
masing-masing.

Unduh **`VaksinKu-App.html`**, lalu klik dua kali — aplikasi langsung terbuka di
browser (Chrome, Edge, Safari, Firefox), di ponsel maupun komputer. Tidak butuh
instalasi, server, atau koneksi internet: logo, ikon, dan font sudah tertanam.

Bisa juga diletakkan di hosting mana pun (mis. GitHub Pages) dan dibuka lewat
tautan, atau ditambahkan ke layar utama ponsel lewat menu "Add to Home screen".

## Yang bisa dikerjakan aplikasi ini

| Fitur | Keterangan |
|---|---|
| **Layar pembuka** | Splash, onboarding 3 langkah, dan layar masuk — sesuai rancangan di Claude Design |
| **Pilihan kebutuhan** | Anak / dewasa / umroh & haji / lansia; pilihan ini menyaring rekomendasi vaksin di beranda dan daftar harga |
| **Ikon menu** | Gaya *Flat Filled with Outline* (Alternatif 2 dari lembar desain ikon): isi teal & pink, garis tepi biru tua, di atas lingkaran teal pucat. Dipakai di menu bawah (yang tidak aktif tampil abu-abu), menu Profil, dan pintasan Beranda. Digambar sebagai SVG di `IKON_MENU` pada `app/app.js` |
| **Banner promo** | Slider geser di bawah kartu reservasi/booking, berputar tiap 5 detik dan berhenti begitu disentuh. Berisi 5 banner promo (Bundling HPV, HPV 4, Little Protection, Influenza, Vaksin Dewasa). Diatur di daftar `BANNER` pada `app/app.js`; gambar 1200×540 (20:9) disimpan di `app/banner/` dan ditanam ke berkas aplikasi saat build |
| **Paket promo haji & umrah** | Kartu harga coret dari price list di Beranda |
| **Profil pendaftar** | Nama & nomor HP, dipakai sebagai kontak reservasi |
| **Data pasien** | Tambah/ubah/hapus anggota keluarga; usia dihitung dari tanggal lahir |
| **Jadwal vaksin personal** | Ceklis otomatis menyesuaikan usia: anak mengikuti **IDAI 2024**, dewasa mengikuti **PAPDI 2025** (rentang usia dipilih otomatis) |
| **Kelengkapan vaksinasi** | Persentase dihitung dari vaksin yang sudah jatuh tempo vs yang sudah dicatat |
| **Reservasi** | Form tervalidasi: layanan, lokasi, pasien, dokter, vaksin, tanggal & jam |
| **Biaya nyata** | Total dihitung dari price list resmi; ganti dokter umum ↔ spesialis mengubah total seketika |
| **Kirim ke WhatsApp** | Ringkasan reservasi dikirim ke CS **0811-7744-74** dengan satu ketukan, disertai kode data yang dibaca dashboard klinik |
| **Konsultasi dokter** | Pertanyaan disusun bersama konteks medis pasien, dikirim ke WhatsApp dokter; jawaban dicatat kembali sebagai arsip percakapan |
| **Pengingat otomatis** | Vaksin terlambat, vaksin yang akan jatuh tempo, reservasi mendekat, dan konsultasi tanpa jawaban — dihitung dari tanggal lahir tiap pasien, dengan lencana di beranda |
| **Ekspor ke kalender** | Unduh `.ics` berisi jadwal vaksin & reservasi lengkap dengan alarm H-7 dan H-1, agar pengingat tetap berbunyi walau aplikasi tertutup |
| **Rekam medis** | Riwayat vaksinasi per pasien, otomatis terisi saat reservasi ditandai selesai |
| **Tumbuh kembang** | Catat berat, tinggi, lingkar kepala; grafik berat badan terhadap usia |
| **Daftar harga** | 17 kategori vaksin, dengan pencarian dan pilihan tarif dokter |
| **Vaksin internasional** | Vaksin wajib haji/umrah, rekomendasi WHO, harga & paket promo, e-ICV |
| **Korporat / Sekolah** | Dashboard vaksinasi massal: daftar peserta per kelas/divisi, cakupan terhitung, booking massal ke WhatsApp, estimasi biaya, dan rekap `.csv` |
| **Poin Sehat** | +10 poin setiap vaksinasi selesai |
| **Cadangkan & pulihkan** | Ekspor/impor seluruh data sebagai berkas `.json` |
| **Data contoh** | Sekali klik untuk mencoba aplikasi atau presentasi |

## Dashboard manajemen (`VaksinKu-Dashboard.html`)

Sisi klinik dari sistem yang sama: satu berkas HTML untuk dibuka di komputer
petugas. Memakai price list, daftar dokter, dan data klinik dari katalog yang
sama dengan aplikasi pasien.

| Modul | Yang dikerjakan |
|---|---|
| **Ringkasan** | KPI harian, grafik pendapatan 7/14/30 hari (plus tampilan tabel), antrean hari ini, peringatan persediaan |
| **Pendaftaran** | Data induk pasien, nomor rekam medis otomatis berurutan, pencarian, riwayat vaksinasi per pasien |
| **Booking** | Daftar tersaring per status, pembuatan booking yang dicek terhadap kapasitas slot, konfirmasi, batal, tidak hadir |
| **Tempel dari WhatsApp** | Pesan reservasi dari aplikasi pasien ditempel apa adanya: pasien baru didaftarkan, pasien lama dikenali, satu booking dibuat per pasien di slot yang masih muat |
| **Penjadwalan** | Jam buka–tutup, durasi slot, kapasitas, hari libur; tampilan slot per hari dan grafik beban 14 hari ke depan |
| **Pelayanan** | Antrean hari ini, check-in, pemilihan batch otomatis **FEFO**, pencatatan KIPI; penyelesaian memotong stok dan menerbitkan tagihan |
| **Persediaan** | Stok per batch dengan kedaluwarsa dan stok minimum, penerimaan, penyesuaian/pembuangan, buku mutasi, peringatan habis & mendekati tempo |
| **Transaksi** | Tagihan terbit otomatis dari pelayanan, pencatatan pembayaran per metode, rekap harian, ekspor `.csv` |

Alurnya saling terkait: pelayanan yang ditandai selesai **sekaligus** mengurangi
stok batch yang dipakai, menulis mutasi keluar, mencatat rekam medis, dan
menerbitkan tagihan dengan harga dari price list resmi. Tidak ada angka yang
ditanam — semua dihitung dari data yang dimasukkan petugas.

### Batasan dashboard

- **Booking dari aplikasi pasien tidak masuk otomatis.** Tanpa server tidak ada
  jalur sinkronisasi; reservasi tiba lewat WhatsApp. Pesan dari aplikasi membawa
  baris **kode data** (`VKD1.…`) di bagian akhir — petugas menyalin pesannya lalu
  memilih **Booking → Tempel dari WhatsApp**, dan pasien serta booking terbentuk
  tanpa mengetik ulang. Jadwal yang diminta pasien menjadi nilai awal; petugas
  boleh menggesernya bila slot penuh. Pesan yang sama tidak tercatat dua kali.
  Pesan yang diketik pasien sendiri (bukan dari aplikasi) tetap dicatat lewat
  *Booking baru*. Jalur lainnya: berkas cadangan `.json` dari aplikasi pasien bisa
  **diimpor** di menu Pengaturan — pasien dan reservasinya ditambahkan tanpa
  menimpa data yang ada.
- Pasien lama dikenali dari **nama dan tanggal lahir yang sama persis**; beda
  ejaan nama akan terdaftar sebagai pasien baru dan perlu digabung manual.
- **Satu perangkat, satu pengguna.** Data ada di browser komputer itu saja; belum
  ada akun petugas, hak akses, atau jejak audit per pengguna. Beberapa kasir atau
  beberapa cabang belum bisa berbagi satu data.
- **Tidak terhubung mesin EDC atau payment gateway**; pembayaran dicatat manual.
- **Bukan rekam medis elektronik resmi.** Belum ada integrasi SATUSEHAT maupun
  pelaporan ke Dinas Kesehatan; ekspor `.csv` disediakan untuk diolah lebih lanjut.
- Harga tagihan diambil saat vaksinasi dicatat, jadi perubahan price list
  setelahnya tidak mengubah tagihan yang sudah terbit.

## Batasan yang perlu diketahui

- **Data tersimpan di perangkat**, bukan di server. Membersihkan data browser
  akan menghapusnya — gunakan menu *Cadangkan data* sebelum berganti perangkat.
- **Reservasi belum otomatis masuk sistem klinik.** Aplikasi menyusun ringkasan
  dan mengirimkannya ke WhatsApp CS untuk dikonfirmasi petugas. Untuk booking
  yang benar-benar otomatis dibutuhkan server dan integrasi jadwal klinik.
- **Konsultasi bukan chat real-time.** Tidak ada balasan otomatis dan tidak ada
  jawaban yang dibuat aplikasi. Pertanyaan dikirim lewat WhatsApp ke dokter/CS,
  lalu jawaban yang Anda terima dicatat sendiri ke dalam aplikasi supaya
  tersimpan bersama rekam medis. Fitur ini juga bukan untuk keadaan gawat
  darurat — peringatan tersebut ditampilkan di layar konsultasi.
- **Notifikasi latar belakang tidak tersedia.** Berkas HTML yang dibuka langsung
  tidak bisa memakai Service Worker, sehingga aplikasi tidak dapat memunculkan
  notifikasi saat ditutup. Notifikasi browser hanya muncul **selagi aplikasi
  terbuka**, dan izinnya kerap ditolak browser pada berkas lokal. Karena itu
  pengingat yang berbunyi saat aplikasi tertutup disediakan lewat **ekspor
  kalender** — cara ini bekerja di Google Calendar maupun kalender bawaan ponsel.
- **Masuk hanya bersifat lokal.** Tidak ada server, jadi tidak ada OTP dan tidak
  ada akun yang bisa dipakai lintas perangkat. Nama dan nomor yang diisi di layar
  masuk tersimpan di perangkat itu saja. Tombol *Lanjutkan dengan Google* sengaja
  ditampilkan nonaktif beserta alasannya — bukan tombol pura-pura — karena OAuth
  membutuhkan server dan alamat situs yang terdaftar.
- **Modul korporat/sekolah menghitung dari data yang Anda masukkan sendiri.**
  Cakupan, estimasi biaya, dan rekap semuanya diturunkan dari daftar peserta di
  perangkat ini; belum ada sinkronisasi dengan sistem sekolah, HRD, maupun
  pencatatan imunisasi pemerintah. Rekap `.csv` berformat umum — kolomnya perlu
  disesuaikan bila Dinas Kesehatan meminta templat tertentu. Yang ditampilkan
  adalah *estimasi* biaya dari price list; invoice resmi tetap terbit dari klinik.
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
index.html                 Halaman muka: galeri 9 layar rancangan (satu berkas)
VaksinKu-App.html          Aplikasi pasien (satu berkas, self-contained)
VaksinKu-Dashboard.html    Dashboard manajemen klinik (satu berkas)
design/                    Artboard hasil ekspor kanvas Claude Design
app/                       Sumber aplikasi pasien
  index.html               Kerangka halaman
  styles.css               Design system: token warna, komponen, tata letak
  banner/                  Gambar banner promo Beranda (1200×540, WebP)
  app.js                   Logika: penyimpanan, rute, layar, perhitungan biaya
admin/                     Sumber dashboard manajemen
  index.html               Kerangka halaman
  styles.css               Design system dashboard (sidebar, tabel, grafik)
  app.js                   Modul booking s.d. transaksi, grafik, dan panel
src/
  data_katalog.py          Isi katalog (harga, jadwal, layanan, dokter, klinik)
  build_bundle.py          Merakit aplikasi pasien + font & logo jadi satu berkas
  build_admin.py           Merakit dashboard manajemen jadi satu berkas
  uji_app.py               Uji fungsional aplikasi pasien (101 uji)
  uji_admin.py             Uji fungsional dashboard (78 uji)
  tangkap_layar.py         Tangkap layar aplikasi pasien
  tangkap_dashboard.py     Tangkap layar dashboard
  ambil_desain.py          Ekspor isi kanvas Claude Design ke folder design/
  build_index.py           Merakit index.html dari design/
  gen.py                   Design system generator mockup statis (versi lama)
  build_app.py             Generator prototipe klik (versi lama)
mockup/              Artboard statis (.dc.html) untuk kanvas desain
katalog/             Halaman katalog hasil koreksi (lihat katalog/README.md)
```

### Membangun ulang

```bash
cd src
python3 build_bundle.py       # → VaksinKu-App.html (font tertanam, siap offline)
python3 build_admin.py        # → VaksinKu-Dashboard.html
python3 build_bundle.py --tanpa-font   # lebih cepat, font dari Google Fonts
python3 uji_app.py            # 101 uji fungsional aplikasi pasien
python3 uji_admin.py          # 78 uji fungsional dashboard
python3 tangkap_layar.py      # tangkap layar aplikasi pasien
python3 tangkap_dashboard.py  # tangkap layar dashboard
python3 build_index.py        # → index.html dari folder design/
```

Bila rancangan di Claude Design diubah, ekspor ulang lalu rakit ulang:

```bash
python3 ambil_desain.py <berkas-halaman-kanvas.html>   # → design/
python3 build_index.py
```

`build_bundle.py` mengunduh font dari Google Fonts saat dijalankan, jadi langkah
ini butuh internet — hasil akhirnya tidak.

## Dari rancangan ke aplikasi

Sembilan layar pada kanvas Claude Design kini punya padanan yang benar-benar
berjalan di `VaksinKu-App.html`:

| Layar rancangan | Wujud fungsionalnya |
|---|---|
| 1. Splash | Layar pembuka saat aplikasi pertama kali dibuka; berpindah sendiri atau saat diketuk |
| 2. Onboarding | Tiga langkah: pengenalan, pilih kebutuhan vaksinasi, pilih cara layanan — pilihannya tersimpan dan dipakai |
| 3. Login | Akun lokal: nama & nomor HP tervalidasi, mengisi profil pendaftar (lihat batasan di atas) |
| 4. Beranda | Reservasi aktif, banner promo, vaksin yang belum lengkap, rekomendasi sesuai kebutuhan, pintasan layanan |
| 5. Booking Vaksinasi | Form tervalidasi dengan biaya nyata dan kirim ke WhatsApp |
| 6. Rekam Medis | Riwayat vaksinasi per pasien dan catatan tumbuh kembang |
| 7. Chat & Konsultasi | Pertanyaan berkonteks medis, dikirim ke WhatsApp, jawaban diarsipkan |
| 8. Profil | Data pendaftar, pasien, alamat, pengaturan, cadangan data |
| 9. Modul Korporat/Sekolah | Dashboard cakupan, daftar peserta, booking massal, rekap `.csv` |

Angka pada rancangan (320 peserta, coverage 77%, invoice Rp48 juta, dan
sejenisnya) adalah angka contoh untuk mockup. Di aplikasi, semua angka dihitung
dari data yang dimasukkan pengguna — tidak ada yang ditanam sebagai hiasan.

## Catatan rancangan

Rancangan di kanvas Claude Design dibuat sebelum katalog resmi tersedia,
sehingga masih memuat data contoh yang terbawa dari screenshot aplikasi
pembanding. Karena `index.html` terbuka untuk umum, data itu diluruskan saat
perakitan — daftar penggantinya ada di `KOREKSI` pada `src/build_index.py`:

- nama dan alamat email pribadi pada layar Profil diganti contoh netral;
- nama dokter diganti dokter asli Alrasha Ibumas (dr. Dwi Fachri JH Sp.A,
  dr. Leo Andreas Sp.PD);
- klinik dan alamat diarahkan ke Tanjungpinang, bukan kota pada screenshot;
- jam konsultasi yang tidak pernah disebut katalog diganti nomor call center.

Agar konsisten, sebaiknya perubahan yang sama juga diterapkan di kanvas
Claude Design-nya.

## Catatan katalog

Pada katalog halaman "Jadwal Vaksin Anak", kotak **0 bulan (lahir)** memuat dua
butir yang sama-sama tertulis "Hep B 0". Sesuai konfirmasi, butir kedua adalah
**Polio 0**; sudah diperbaiki di aplikasi dan pada halaman katalog revisi di
`katalog/`. Untuk kebutuhan cetak, koreksi yang sama masih perlu dilakukan pada
berkas desain master.

Harga **Meningitis (Menivax)** untuk dokter spesialis tidak tercantum di katalog,
sehingga pada tarif spesialis ditampilkan sebagai "Hubungi CS".
