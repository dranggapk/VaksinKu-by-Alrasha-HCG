-- Uji hak akses & fungsi VaksinKu. Dijalankan oleh src/uji_supabase.py pada
-- database uji yang baru (shim + migrasi + seed). Setiap skenario berjalan
-- sebagai peran 'authenticated' dengan identitas pengguna tertentu, sehingga
-- RLS benar-benar diterapkan seperti di Supabase.

-- ------------------------------------------------------------ perangkat uji
create schema uji;
grant usage on schema uji to anon, authenticated;
create table uji.hasil (no serial, nama text, lulus boolean, detail text);
create table uji.konteks (kunci text primary key, nilai text);
grant select on uji.konteks to anon, authenticated;

create function uji.catat(p_nama text, p_lulus boolean, p_detail text default '') returns void
language sql security definer as $$
  insert into uji.hasil (nama, lulus, detail) values (p_nama, coalesce(p_lulus, false), coalesce(p_detail, ''))
$$;
create function uji.simpan(p_kunci text, p_nilai text) returns void
language sql security definer as $$
  insert into uji.konteks values (p_kunci, p_nilai) on conflict (kunci) do update set nilai = excluded.nilai
$$;
create function uji.ambil(p_kunci text) returns text language sql stable as $$
  select nilai from uji.konteks where kunci = p_kunci
$$;
-- Dijalankan sebagai pemanggil (bukan definer): RLS berlaku pada perintahnya.
create function uji.harus_gagal(p_nama text, p_perintah text, p_pola text) returns void
language plpgsql as $$
begin
  execute p_perintah;
  perform uji.catat(p_nama, false, 'perintah berhasil, seharusnya ditolak');
exception when others then
  perform uji.catat(p_nama, sqlerrm ilike '%' || p_pola || '%', sqlerrm);
end $$;
grant execute on all functions in schema uji to anon, authenticated;

create function uji.sebagai(p_user uuid) returns void language sql as $$
  select set_config('request.jwt.claims', json_build_object('sub', p_user, 'role', 'authenticated')::text, false)
$$;
grant execute on function uji.sebagai(uuid) to anon, authenticated;

-- ------------------------------------------------------------ pengguna uji
insert into auth.users (id, phone, raw_user_meta_data) values
  ('00000000-0000-0000-0000-0000000000a1', '6281200000001', '{"nama":"Ibu Sari"}'),
  ('00000000-0000-0000-0000-0000000000b1', '6281200000002', '{"nama":"Pak Budi"}'),
  ('00000000-0000-0000-0000-0000000000c1', '6281200000003', '{"nama":"Perawat HCC"}'),
  ('00000000-0000-0000-0000-0000000000c2', '6281200000004', '{"nama":"Admin HCC"}'),
  ('00000000-0000-0000-0000-0000000000d1', '6281200000005', '{"nama":"Perawat Ibumas"}'),
  ('00000000-0000-0000-0000-0000000000e1', '6281200000006', '{"nama":"Admin VaksinKu"}');
insert into public.anggota_klinik (user_id, klinik_id, peran) values
  ('00000000-0000-0000-0000-0000000000c1', 'alrasha-hcc', 'petugas'),
  ('00000000-0000-0000-0000-0000000000c2', 'alrasha-hcc', 'admin'),
  ('00000000-0000-0000-0000-0000000000d1', 'alrasha-ibumas', 'petugas');
insert into public.admin_vaksinku (user_id) values ('00000000-0000-0000-0000-0000000000e1');

-- Hari kerja berikutnya (bukan Minggu) dan hari Minggu berikutnya, waktu WIB.
select uji.simpan('besok', (select d::date::text from generate_series(public.hari_ini() + 1, public.hari_ini() + 7, interval '1 day') d
                            where extract(dow from d) <> 0 limit 1));
select uji.simpan('minggu', (select d::date::text from generate_series(public.hari_ini() + 1, public.hari_ini() + 7, interval '1 day') d
                             where extract(dow from d) = 0 limit 1));

-- ============================================================ 1. data awal
select uji.catat('seed: 3 klinik mitra, 2 kota', (select count(*) from public.klinik) = 3 and (select count(*) from public.kota) = 2);
select uji.catat('seed: price list hanya untuk 2 klinik Alrasha',
  (select count(distinct klinik_id) from public.harga_klinik) = 2 and not exists (select 1 from public.harga_klinik where klinik_id = 'jasmine-mq'));
select uji.catat('akun baru otomatis punya profil', (select count(*) from public.profil) = 6,
  (select string_agg(nama, ', ') from public.profil));

-- ============================================================ 2. pengunjung belum masuk
set role anon;
select uji.catat('anon: price list terbuka', (select count(*) from public.harga_klinik) = 58);
select uji.harus_gagal('anon: data pasien tertutup', 'select * from public.pasien', 'permission denied');
select uji.harus_gagal('anon: tidak bisa booking',
  'select public.buat_booking(''alrasha-hcc'',''klinik'','''',current_date,''09:00'',''umum'','''',false,''[]'')', 'permission denied');
reset role;

-- ============================================================ 3. pasien mengelola keluarganya
set role authenticated;
select uji.sebagai('00000000-0000-0000-0000-0000000000a1');
insert into public.pasien (profil_id, nama, tgl_lahir, jenis_kelamin, hubungan)
values ('00000000-0000-0000-0000-0000000000a1', 'Nadia', current_date - 400, 'Perempuan', 'Anak'),
       ('00000000-0000-0000-0000-0000000000a1', 'Rafa', current_date - 90, 'Laki-laki', 'Anak');
select uji.simpan('nadia', (select id::text from public.pasien where nama = 'Nadia'));
select uji.simpan('rafa', (select id::text from public.pasien where nama = 'Rafa'));
select uji.catat('pasien: menambah anggota keluarga', (select count(*) from public.pasien) = 2);
select uji.harus_gagal('pasien: tidak bisa menambah pasien atas nama akun lain',
  'insert into public.pasien (profil_id, nama, tgl_lahir) values (''00000000-0000-0000-0000-0000000000b1'', ''Titipan'', current_date - 10)',
  'row-level security');
insert into public.riwayat_dosis (pasien_id, kunci, label, tanggal, tempat, no_batch, sumber)
values (uji.ambil('nadia')::uuid, '{hepb:0}', 'Hepatitis B 0', current_date - 399, 'Puskesmas', 'HB0-77', 'pasien');
select uji.catat('pasien: mencatat riwayat dosis sendiri', (select count(*) from public.riwayat_dosis) = 1);
select uji.harus_gagal('pasien: tidak bisa membuat catatan "terverifikasi klinik"',
  format('insert into public.riwayat_dosis (pasien_id, kunci, tanggal, sumber, diverifikasi) values (%L, ''{bcg:1}'', current_date, ''pasien'', true)', uji.ambil('nadia')),
  'row-level security');
select uji.harus_gagal('pasien: tidak bisa memalsukan sumber klinik',
  format('insert into public.riwayat_dosis (pasien_id, kunci, tanggal, sumber, klinik_id) values (%L, ''{bcg:1}'', current_date, ''klinik'', ''alrasha-hcc'')', uji.ambil('nadia')),
  'row-level security');

select uji.sebagai('00000000-0000-0000-0000-0000000000b1');
select uji.catat('keluarga lain: tidak melihat pasien & riwayat Ibu Sari',
  (select count(*) from public.pasien) = 0 and (select count(*) from public.riwayat_dosis) = 0);
insert into public.pasien (profil_id, nama, tgl_lahir) values ('00000000-0000-0000-0000-0000000000b1', 'Budi Jr', current_date - 800);
select uji.simpan('budijr', (select id::text from public.pasien where nama = 'Budi Jr'));
reset role;

-- ============================================================ 4. booking dari aplikasi
set role authenticated;
select uji.sebagai('00000000-0000-0000-0000-0000000000a1');
select uji.simpan('b1', (select (public.buat_booking('alrasha-hcc', 'klinik', '', uji.ambil('besok')::date, '09:00', 'umum',
  'Alergi telur ringan', false, jsonb_build_array(jsonb_build_object('pasien_id', uji.ambil('nadia'), 'vaksin_id', 'v7-11')))).id::text));
select uji.catat('booking: dibuat dengan status baru & kode VK-',
  (select status = 'baru' and kode like 'VK-%' from public.booking where id = uji.ambil('b1')::uuid),
  (select kode from public.booking where id = uji.ambil('b1')::uuid));
select uji.catat('booking: harga ditetapkan server dari price list (Rp400.000)',
  (select harga from public.booking_item where booking_id = uji.ambil('b1')::uuid) = 400000);
select uji.catat('booking: lokasi klinik tersimpan di profil',
  (select klinik_id from public.profil where id = '00000000-0000-0000-0000-0000000000a1') = 'alrasha-hcc');
select uji.harus_gagal('booking: tidak bisa memesan untuk pasien keluarga lain',
  format('select public.buat_booking(''alrasha-hcc'',''klinik'','''',%L,''10:00'',''umum'','''',false,%L)',
         uji.ambil('besok'), jsonb_build_array(jsonb_build_object('pasien_id', uji.ambil('budijr'), 'vaksin_id', 'v7-11'))),
  'Pasien tidak dikenal');
select uji.harus_gagal('booking: hari libur klinik ditolak',
  format('select public.buat_booking(''alrasha-hcc'',''klinik'','''',%L,''09:00'',''umum'','''',false,%L)',
         uji.ambil('minggu'), jsonb_build_array(jsonb_build_object('pasien_id', uji.ambil('rafa'), 'vaksin_id', 'v7-11'))),
  'libur');
select uji.harus_gagal('booking: tanggal lampau ditolak',
  format('select public.buat_booking(''alrasha-hcc'',''klinik'','''',current_date - 3,''09:00'',''umum'','''',false,%L)',
         jsonb_build_array(jsonb_build_object('pasien_id', uji.ambil('rafa'), 'vaksin_id', 'v7-11'))),
  'masa lalu');
select uji.harus_gagal('booking: jam di luar jam layanan ditolak',
  format('select public.buat_booking(''alrasha-hcc'',''klinik'','''',%L,''20:00'',''umum'','''',false,%L)',
         uji.ambil('besok'), jsonb_build_array(jsonb_build_object('pasien_id', uji.ambil('rafa'), 'vaksin_id', 'v7-11'))),
  'jam layanan');
select uji.harus_gagal('booking: tidak bisa langsung menulis tabel booking',
  'insert into public.booking (kode, klinik_id, layanan, tanggal, jam) values (''X'', ''alrasha-hcc'', ''klinik'', current_date + 1, ''09:00'')',
  'permission denied');
reset role;

-- Kapasitas slot: diperkecil jadi 1, slot 09:00 sudah terisi Nadia.
update public.klinik set kapasitas_slot = 1 where id = 'alrasha-hcc';
set role authenticated;
select uji.sebagai('00000000-0000-0000-0000-0000000000a1');
select uji.harus_gagal('booking: slot penuh ditolak oleh database',
  format('select public.buat_booking(''alrasha-hcc'',''klinik'','''',%L,''09:00'',''umum'','''',false,%L)',
         uji.ambil('besok'), jsonb_build_array(jsonb_build_object('pasien_id', uji.ambil('rafa'), 'vaksin_id', 'v7-11'))),
  'penuh');
-- Klinik tanpa price list (Jasmine MQ): booking tetap bisa, harga dikonfirmasi klinik.
select uji.simpan('bj', (select (public.buat_booking('jasmine-mq', 'klinik', '', uji.ambil('besok')::date, '09:00', 'umum', '', false,
  jsonb_build_array(jsonb_build_object('pasien_id', uji.ambil('rafa'), 'vaksin_id', 'v4-7')))).id::text));
select uji.catat('booking: klinik tanpa price list → harga dikonfirmasi klinik (null)',
  (select harga is null from public.booking_item where booking_id = uji.ambil('bj')::uuid));
reset role;
update public.klinik set kapasitas_slot = 3 where id = 'alrasha-hcc';

-- ============================================================ 5. pemisahan antar klinik
set role authenticated;
select uji.sebagai('00000000-0000-0000-0000-0000000000c1');
select uji.catat('petugas HCC: melihat booking kliniknya saja',
  (select count(*) from public.booking) = 1 and (select klinik_id from public.booking limit 1) = 'alrasha-hcc');
select uji.catat('petugas HCC: melihat pasien yang booking di kliniknya (Nadia saja)',
  (select string_agg(nama, ',') from public.pasien) = 'Nadia', (select string_agg(nama, ',') from public.pasien));
select uji.catat('petugas HCC: riwayat luar klinik tidak terlihat tanpa izin pasien',
  (select count(*) from public.riwayat_dosis) = 0);
select uji.catat('petugas HCC: melihat nama & HP pendaftar booking',
  (select hp from public.profil where id = '00000000-0000-0000-0000-0000000000a1') = '6281200000001');
select uji.sebagai('00000000-0000-0000-0000-0000000000d1');
select uji.catat('petugas Ibumas: tidak melihat booking, pasien, profil klinik lain',
  (select count(*) from public.booking) = 0 and (select count(*) from public.pasien) = 0 and (select count(*) from public.profil) = 1);
select uji.harus_gagal('petugas Ibumas: tidak bisa mengonfirmasi booking klinik lain',
  format('select public.ubah_status_booking(%L, ''terkonfirmasi'')', uji.ambil('b1')), 'tidak ditemukan');
reset role;

-- Pasien membagikan riwayat lewat booking kedua → riwayat luar klinik ikut terlihat.
set role authenticated;
select uji.sebagai('00000000-0000-0000-0000-0000000000a1');
select uji.simpan('b2', (select (public.buat_booking('alrasha-hcc', 'klinik', '', uji.ambil('besok')::date, '10:00', 'umum', '', true,
  jsonb_build_array(jsonb_build_object('pasien_id', uji.ambil('nadia'), 'vaksin_id', 'v13-22')))).id::text));
select uji.harus_gagal('pasien: tidak bisa mengonfirmasi booking sendiri',
  format('select public.ubah_status_booking(%L, ''terkonfirmasi'')', uji.ambil('b2')), 'hanya bisa diubah oleh klinik');
select public.ubah_status_booking(uji.ambil('b2')::uuid, 'batal');
select uji.catat('pasien: membatalkan booking berstatus baru',
  (select status from public.booking where id = uji.ambil('b2')::uuid) = 'batal');
select uji.sebagai('00000000-0000-0000-0000-0000000000c1');
select uji.catat('petugas HCC: riwayat terlihat setelah pasien membagikannya',
  (select count(*) from public.riwayat_dosis) = 1 and (select no_batch from public.riwayat_dosis limit 1) = 'HB0-77');
reset role;

-- ============================================================ 6. stok, pelayanan, tagihan
set role authenticated;
select uji.sebagai('00000000-0000-0000-0000-0000000000c1');
select uji.simpan('stok', (select (public.terima_stok('alrasha-hcc', 'v7-11', 'VXG-2611A', current_date + 300, 10)).id::text));
select uji.harus_gagal('stok: batch kedaluwarsa tidak boleh diterima',
  'select public.terima_stok(''alrasha-hcc'', ''v7-11'', ''LAMA-1'', current_date - 1, 5)', 'kedaluwarsa');
select uji.harus_gagal('stok: petugas tidak bisa menerima stok untuk klinik lain',
  'select public.terima_stok(''alrasha-ibumas'', ''v7-11'', ''X-1'', current_date + 100, 5)', 'Hanya petugas');
select public.ubah_status_booking(uji.ambil('b1')::uuid, 'terkonfirmasi');
select uji.harus_gagal('pelayanan: ditolak sebelum pasien check-in',
  format('select public.catat_pelayanan(%L, %L, %L, null, '''', '''')', uji.ambil('b1'), uji.ambil('nadia'),
         jsonb_build_array(jsonb_build_object('vaksin_id', 'v7-11', 'stok_id', uji.ambil('stok'), 'kunci', jsonb_build_array('flu:1')))),
  'check-in');
select public.ubah_status_booking(uji.ambil('b1')::uuid, 'hadir');
select uji.harus_gagal('pelayanan: dosis yang tidak terkandung dalam vaksin ditolak',
  format('select public.catat_pelayanan(%L, %L, %L, null, '''', '''')', uji.ambil('b1'), uji.ambil('nadia'),
         jsonb_build_array(jsonb_build_object('vaksin_id', 'v7-11', 'stok_id', uji.ambil('stok'), 'kunci', jsonb_build_array('hepb:1')))),
  'tidak terkandung');
select public.catat_pelayanan(uji.ambil('b1')::uuid, uji.ambil('nadia')::uuid,
  jsonb_build_array(jsonb_build_object('vaksin_id', 'v7-11', 'stok_id', uji.ambil('stok'), 'kunci', jsonb_build_array('flu:1'))),
  null, '', 'Suhu 36,7');
select uji.catat('pelayanan: stok batch berkurang 1 dan tercatat di buku mutasi',
  (select sisa from public.stok_batch where id = uji.ambil('stok')::uuid) = 9
  and (select count(*) from public.mutasi_stok where jenis = 'keluar') = 1);
select uji.catat('pelayanan: riwayat dosis terverifikasi dengan No. Batch',
  exists (select 1 from public.riwayat_dosis where sumber = 'klinik' and diverifikasi and no_batch = 'VXG-2611A' and kunci = '{flu:1}'));
select uji.catat('pelayanan: tagihan terbit sesuai harga booking',
  (select total from public.tagihan) = 400000, (select nomor || ' ' || total from public.tagihan));
select uji.catat('pelayanan: booking otomatis selesai',
  (select status from public.booking where id = uji.ambil('b1')::uuid) = 'selesai');
select uji.simpan('tagihan', (select id::text from public.tagihan limit 1));
reset role;

-- ============================================================ 7. hasil kembali ke pasien
set role authenticated;
select uji.sebagai('00000000-0000-0000-0000-0000000000a1');
select uji.catat('pasien: melihat dosis terverifikasi klinik + No. Batch',
  exists (select 1 from public.riwayat_dosis where diverifikasi and no_batch = 'VXG-2611A'));
select uji.catat('pasien: melihat tagihannya', (select count(*) from public.tagihan) = 1);
update public.riwayat_dosis set no_batch = 'DIUBAH' where sumber = 'klinik';
delete from public.riwayat_dosis where sumber = 'klinik';
select uji.catat('pasien: catatan klinik tidak bisa diubah atau dihapus',
  exists (select 1 from public.riwayat_dosis where sumber = 'klinik' and no_batch = 'VXG-2611A'));
select uji.harus_gagal('pasien: tidak bisa mencatat pembayaran',
  format('select public.terima_pembayaran(%L, 400000, ''Tunai'')', uji.ambil('tagihan')), 'tidak ditemukan');
select uji.sebagai('00000000-0000-0000-0000-0000000000b1');
select uji.catat('keluarga lain: tidak melihat booking, tagihan, layanan Ibu Sari',
  (select count(*) from public.booking) = 0 and (select count(*) from public.tagihan) = 0 and (select count(*) from public.layanan) = 0);
select uji.sebagai('00000000-0000-0000-0000-0000000000c1');
select public.terima_pembayaran(uji.ambil('tagihan')::uuid, 400000, 'QRIS');
select uji.catat('pembayaran: tagihan lunas', (select status from public.tagihan) = 'lunas');
reset role;

-- ============================================================ 8. price list & petugas
set role authenticated;
select uji.sebagai('00000000-0000-0000-0000-0000000000c1');
update public.harga_klinik set harga_umum = 1 where klinik_id = 'alrasha-hcc' and vaksin_id = 'v7-11';
select uji.sebagai('00000000-0000-0000-0000-0000000000c2');
update public.harga_klinik set harga_umum = 410000 where vaksin_id = 'v7-11';
reset role;
select uji.catat('harga: petugas biasa tidak bisa mengubah price list; admin hanya kliniknya',
  (select harga_umum from public.harga_klinik where klinik_id = 'alrasha-hcc' and vaksin_id = 'v7-11') = 410000
  and (select harga_umum from public.harga_klinik where klinik_id = 'alrasha-ibumas' and vaksin_id = 'v7-11') = 400000);
set role authenticated;
select uji.sebagai('00000000-0000-0000-0000-0000000000c2');
insert into public.anggota_klinik (user_id, klinik_id, peran) values ('00000000-0000-0000-0000-0000000000b1', 'alrasha-hcc', 'petugas');
select uji.harus_gagal('admin klinik: tidak bisa menambah petugas di klinik lain',
  'insert into public.anggota_klinik (user_id, klinik_id, peran) values (''00000000-0000-0000-0000-0000000000a1'', ''alrasha-ibumas'', ''admin'')',
  'row-level security');
select uji.sebagai('00000000-0000-0000-0000-0000000000a1');
select uji.harus_gagal('pasien: tidak bisa mengangkat diri jadi petugas',
  'insert into public.anggota_klinik (user_id, klinik_id, peran) values (''00000000-0000-0000-0000-0000000000a1'', ''alrasha-hcc'', ''admin'')',
  'row-level security');
reset role;
delete from public.anggota_klinik where user_id = '00000000-0000-0000-0000-0000000000b1';

-- ============================================================ 9. jejak audit
set role authenticated;
select uji.sebagai('00000000-0000-0000-0000-0000000000c1');
select nama from public.buka_pasien(uji.ambil('nadia')::uuid);
select uji.harus_gagal('petugas: tidak bisa membuka pasien yang tidak berobat di kliniknya',
  format('select public.buka_pasien(%L)', uji.ambil('budijr')), 'tidak ditemukan');
select uji.catat('audit: petugas biasa tidak membaca jejak audit', (select count(*) from public.jejak_audit) = 0);
select uji.sebagai('00000000-0000-0000-0000-0000000000c2');
select uji.catat('audit: admin klinik melihat siapa membuka data pasien',
  exists (select 1 from public.jejak_audit where aksi = 'buka' and user_id = '00000000-0000-0000-0000-0000000000c1'));
select uji.sebagai('00000000-0000-0000-0000-0000000000e1');
select uji.catat('admin VaksinKu: tidak membuka data pasien', (select count(*) from public.pasien) = 0);
reset role;

-- ------------------------------------------------------------ hasil
select (case when lulus then 'LULUS' else 'GAGAL' end) || ' | ' || nama || ' | ' || detail from uji.hasil order by no;
