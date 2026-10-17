# Backend VaksinKu — tahap fondasi (Supabase)

Isi folder ini adalah tahap 1 dari rancangan *Rancangan Backend VaksinKu: Supabase → VPS*:
struktur tabel, aturan akses (RLS), fungsi SQL untuk alur klinik, dan data katalog
3 klinik mitra. Aplikasi pasien dan dashboard **belum** memakai backend ini; itu tahap
berikutnya.

```
migrations/
  20261010000100_skema.sql      20 tabel: katalog, pasien, booking, stok, riwayat, tagihan, audit
  20261010000200_keamanan.sql   Hak akses & RLS: siapa boleh membaca/menulis apa
  20261010000300_fungsi.sql     Fungsi: buat_booking, ubah_status_booking, terima_stok,
                                sesuaikan_stok, catat_pelayanan, terima_pembayaran, buka_pasien
seed.sql                        Kota, klinik, vaksin, price list, dokter (dibuat otomatis)
tests/
  lokal_supabase_shim.sql       Tiruan skema auth Supabase — KHUSUS uji lokal
  uji_hak_akses.sql             52 skenario uji hak akses & alur klinik
```

Hanya fitur PostgreSQL standar yang dipakai, jadi seluruh database bisa dipindah ke
VPS dengan `pg_dump` / `pg_restore`.

## Aturan utama yang dijaga database

- **Pasien** hanya melihat dan mengubah anggota keluarganya sendiri. Catatan dosis yang
  ia tulis sendiri selalu berlabel "dicatat pasien" — tidak bisa menandai diri
  "terverifikasi klinik".
- **Petugas klinik** hanya melihat pasien yang booking di kliniknya (atau yang
  didaftarkan kliniknya). Riwayat dosis dari tempat lain baru terlihat bila pasien
  mencentang *bagikan riwayat* saat booking.
- **Booking, stok, pelayanan, pembayaran** hanya lewat fungsi. Harga dibekukan server dari
  price list klinik; kuota per slot dijaga di database sehingga dua orang tidak bisa
  mengambil slot terakhir bersamaan.
- **Pelayanan** mengurangi stok batch, mencatat mutasi, menulis riwayat dosis
  terverifikasi (dengan No. Batch), dan menerbitkan tagihan dalam satu transaksi.
- **Admin klinik** mengelola price list, dokter, promo, dan petugas kliniknya saja, serta
  membaca jejak audit (siapa membuka data pasien, kapan).
- **Admin VaksinKu** mengelola katalog, tetapi **tidak** membuka data pasien.

## Menguji di komputer sendiri

Butuh PostgreSQL 15+ dan `psql`. Pengujian membuat database `vaksinku_uji` yang baru
setiap kali dijalankan.

```bash
python3 src/uji_supabase.py                                   # 127.0.0.1:54329
PGURL=postgresql://postgres:sandi@localhost:5432 python3 src/uji_supabase.py
```

Setelah `src/data_katalog.py` berubah (mis. price list Jasmine MQ Medika sudah ada),
buat ulang seed: `python3 src/buat_seed_supabase.py`.

## Memasang ke proyek Supabase

1. Buat proyek di supabase.com, region **Southeast Asia (Singapore)**.
2. Pilih salah satu:
   - **SQL Editor**: jalankan ketiga berkas `migrations/` berurutan, lalu `seed.sql`.
   - **Supabase CLI**: `supabase link --project-ref <ref>` lalu `supabase db push`,
     kemudian jalankan `seed.sql` di SQL Editor.
3. **Jangan** jalankan berkas di `tests/` pada proyek Supabase — shim menimpa skema
   auth bawaan dan uji membuat pengguna palsu.
4. Angkat akun petugas pertama lewat SQL Editor (sebagai pemilik proyek):
   ```sql
   insert into public.anggota_klinik (user_id, klinik_id, peran)
   select id, 'alrasha-hcc', 'admin' from auth.users where phone = '62812xxxxxxx';
   ```
   Setelah itu admin klinik bisa menambah petugasnya sendiri.

Yang dibutuhkan aplikasi hanya **Project URL** dan **anon key**. Kunci `service_role`
melewati semua aturan akses: jangan pernah dimasukkan ke aplikasi, dashboard, maupun
dikirim lewat chat.
