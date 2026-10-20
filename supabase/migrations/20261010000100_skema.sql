-- VaksinKu · tahap fondasi · 1/3: struktur tabel
-- Rancangan: "Rancangan Backend VaksinKu: Supabase → VPS".
-- Hanya fitur PostgreSQL standar agar bisa dipindah ke VPS dengan pg_dump.

-- ============================================================ katalog & mitra
create table public.kota (
  id          text primary key,                 -- slug, mis. 'tanjungpinang'
  nama        text not null,
  aktif       boolean not null default true,
  dibuat_pada timestamptz not null default now()
);

create table public.klinik (
  id             text primary key,              -- slug, mis. 'alrasha-hcc'
  kota_id        text not null references public.kota (id),
  nama           text not null,
  alamat         text not null default '',      -- kosong = belum diterima
  telepon_wa     text not null default '',
  jam_buka       time not null default '08:00',
  jam_tutup      time not null default '16:00',
  durasi_slot    integer not null default 30 check (durasi_slot between 5 and 240),
  kapasitas_slot integer not null default 3 check (kapasitas_slot between 1 and 50),
  hari_libur     smallint[] not null default '{0}',   -- 0 = Minggu … 6 = Sabtu
  aktif          boolean not null default true,
  dibuat_pada    timestamptz not null default now(),
  diubah_pada    timestamptz not null default now(),
  check (jam_tutup > jam_buka)
);

create table public.vaksin (
  id          text primary key,                 -- sama dengan id di aplikasi, mis. 'v12-20'
  kategori    text not null,
  sediaan     text not null,
  merek       text not null,
  antigen     text[] not null default '{}',     -- mis. {dtp,hib,hepb,ipv}
  aktif       boolean not null default true
);

-- Price list & ketersediaan per klinik. Tidak ada baris = harga dikonfirmasi klinik.
create table public.harga_klinik (
  klinik_id       text not null references public.klinik (id) on delete cascade,
  vaksin_id       text not null references public.vaksin (id),
  harga_umum      integer check (harga_umum >= 0),
  harga_spesialis integer check (harga_spesialis >= 0),
  harga_coret     integer check (harga_coret >= 0),
  tersedia        boolean not null default true,
  diubah_pada     timestamptz not null default now(),
  primary key (klinik_id, vaksin_id)
);

create table public.dokter (
  id           uuid primary key default gen_random_uuid(),
  klinik_id    text not null references public.klinik (id) on delete cascade,
  nama         text not null,
  spesialisasi text not null default '',
  inisial      text not null default '',
  aktif        boolean not null default true
);

create table public.promo (
  id             uuid primary key default gen_random_uuid(),
  klinik_id      text references public.klinik (id) on delete cascade,  -- null = semua klinik
  judul          text not null,
  gambar_url     text not null default '',
  teks_alt       text not null default '',
  tujuan         text not null default 'booking',
  urutan         integer not null default 0,
  berlaku_sampai date,
  aktif          boolean not null default true
);

-- ============================================================ pasien
-- Satu profil per akun login (auth.users). Dibuat otomatis oleh pemicu.
create table public.profil (
  id                    uuid primary key references auth.users (id) on delete cascade,
  nama                  text not null default '',
  hp                    text not null default '',
  kota_id               text references public.kota (id),
  klinik_id             text references public.klinik (id),
  persetujuan_data_pada timestamptz,
  dibuat_pada           timestamptz not null default now(),
  diubah_pada           timestamptz not null default now()
);

create table public.pasien (
  id               uuid primary key default gen_random_uuid(),
  profil_id        uuid references public.profil (id) on delete cascade,  -- null = didaftarkan klinik
  klinik_pendaftar text references public.klinik (id),                      -- klinik yang mendaftarkan
  nama             text not null check (length(trim(nama)) > 0),
  tgl_lahir        date not null,
  jenis_kelamin    text not null default '' check (jenis_kelamin in ('', 'Perempuan', 'Laki-laki')),
  hubungan         text not null default '',
  hp               text not null default '',
  jadwal_anak      text not null default 'idai' check (jadwal_anak in ('idai', 'kia')),
  endemis          boolean not null default false,
  rv               text not null default '' check (rv in ('', 'rv1', 'rv5')),
  kondisi          jsonb not null default '{}'::jsonb,
  dibuat_pada      timestamptz not null default now(),
  diubah_pada      timestamptz not null default now(),
  check (profil_id is not null or klinik_pendaftar is not null)
);
create index on public.pasien (profil_id);

create table public.anggota_klinik (
  user_id     uuid not null references auth.users (id) on delete cascade,
  klinik_id   text not null references public.klinik (id) on delete cascade,
  peran       text not null check (peran in ('petugas', 'admin')),
  dibuat_pada timestamptz not null default now(),
  primary key (user_id, klinik_id)
);

create table public.admin_vaksinku (
  user_id     uuid primary key references auth.users (id) on delete cascade,
  dibuat_pada timestamptz not null default now()
);

-- ============================================================ operasional klinik
create sequence public.urut_booking;
create table public.booking (
  id              uuid primary key default gen_random_uuid(),
  kode            text not null unique,
  klinik_id       text not null references public.klinik (id),
  profil_id       uuid references public.profil (id) on delete set null,
  layanan         text not null check (layanan in ('homecare', 'klinik', 'corporate')),
  lokasi          text not null default '',
  tanggal         date not null,
  jam             time not null,
  tarif           text not null default 'umum' check (tarif in ('umum', 'spesialis')),
  status          text not null default 'baru'
                  check (status in ('baru', 'terkonfirmasi', 'hadir', 'selesai', 'batal', 'tidak_hadir')),
  catatan         text not null default '',
  bagikan_riwayat boolean not null default false,
  sumber          text not null default 'aplikasi' check (sumber in ('aplikasi', 'petugas', 'whatsapp')),
  dibuat_oleh     uuid,
  dibuat_pada     timestamptz not null default now(),
  diubah_pada     timestamptz not null default now()
);
create index on public.booking (klinik_id, tanggal, jam);
create index on public.booking (profil_id);

create table public.booking_item (
  id         uuid primary key default gen_random_uuid(),
  booking_id uuid not null references public.booking (id) on delete cascade,
  pasien_id  uuid not null references public.pasien (id) on delete cascade,
  vaksin_id  text not null references public.vaksin (id),
  harga      integer,                     -- dibekukan saat booking; null = dikonfirmasi klinik
  unique (booking_id, pasien_id, vaksin_id)
);
create index on public.booking_item (pasien_id);

create table public.stok_batch (
  id          uuid primary key default gen_random_uuid(),
  klinik_id   text not null references public.klinik (id) on delete cascade,
  vaksin_id   text not null references public.vaksin (id),
  no_batch    text not null check (length(trim(no_batch)) > 0),
  kedaluwarsa date not null,
  jumlah      integer not null check (jumlah > 0),
  sisa        integer not null check (sisa >= 0),
  dibuat_pada timestamptz not null default now(),
  unique (klinik_id, vaksin_id, no_batch)
);

create table public.layanan (
  id          uuid primary key default gen_random_uuid(),
  booking_id  uuid not null references public.booking (id),
  pasien_id   uuid not null references public.pasien (id),
  klinik_id   text not null references public.klinik (id),
  petugas     uuid not null,
  dokter_id   uuid references public.dokter (id),
  kipi        text not null default '',
  catatan     text not null default '',
  dibuat_pada timestamptz not null default now(),
  unique (booking_id, pasien_id)
);

create table public.mutasi_stok (
  id          uuid primary key default gen_random_uuid(),
  stok_id     uuid not null references public.stok_batch (id) on delete cascade,
  jenis       text not null check (jenis in ('masuk', 'keluar', 'buang', 'koreksi')),
  jumlah      integer not null,           -- bertanda: keluar/buang negatif
  keterangan  text not null default '',
  layanan_id  uuid references public.layanan (id),
  oleh        uuid,
  dibuat_pada timestamptz not null default now()
);

-- Riwayat dosis per kunci antigen:urutan (sama dengan aplikasi, src/jadwal_anak.py),
-- sehingga pilihan jadwal IDAI ↔ Buku KIA tetap bekerja.
create table public.riwayat_dosis (
  id           uuid primary key default gen_random_uuid(),
  pasien_id    uuid not null references public.pasien (id) on delete cascade,
  kunci        text[] not null default '{}',   -- mis. {dtp:1,hib:1,hepb:1}
  label        text not null default '',
  tanggal      date not null,
  tempat       text not null default '',
  faskes       text not null default '',
  merek        text not null default '',
  no_batch     text not null default '',
  foto_path    text not null default '',        -- berkas di Storage (privat)
  sumber       text not null check (sumber in ('pasien', 'klinik')),
  klinik_id    text references public.klinik (id),
  layanan_id   uuid references public.layanan (id),
  diverifikasi boolean not null default false,
  dibuat_pada  timestamptz not null default now(),
  diubah_pada  timestamptz not null default now()
);
create index on public.riwayat_dosis (pasien_id);

create table public.rencana_puskesmas (
  pasien_id   uuid not null references public.pasien (id) on delete cascade,
  kunci       text not null,                  -- kunci dosis, mis. 'dtp:1+hib:1+hepb:1'
  dibuat_pada timestamptz not null default now(),
  primary key (pasien_id, kunci)
);

create sequence public.urut_tagihan;
create table public.tagihan (
  id          uuid primary key default gen_random_uuid(),
  nomor       text not null unique,
  klinik_id   text not null references public.klinik (id),
  layanan_id  uuid not null unique references public.layanan (id),
  profil_id   uuid references public.profil (id) on delete set null,
  item        jsonb not null default '[]'::jsonb,
  total       integer not null default 0 check (total >= 0),
  dibayar     integer not null default 0 check (dibayar >= 0),
  status      text not null default 'belum' check (status in ('belum', 'lunas')),
  dibuat_pada timestamptz not null default now()
);

create table public.pembayaran (
  id          uuid primary key default gen_random_uuid(),
  tagihan_id  uuid not null references public.tagihan (id) on delete cascade,
  jumlah      integer not null check (jumlah > 0),
  metode      text not null check (metode in ('Tunai', 'Transfer', 'QRIS', 'Kartu debit/kredit', 'Asuransi')),
  oleh        uuid,
  dibuat_pada timestamptz not null default now()
);

-- Jejak audit: siapa membuka atau mengubah data pasien, kapan.
create table public.jejak_audit (
  id          bigint generated always as identity primary key,
  user_id     uuid,
  klinik_id   text,
  tabel       text not null,
  aksi        text not null,
  baris_id    text not null default '',
  dibuat_pada timestamptz not null default now()
);
create index on public.jejak_audit (klinik_id, dibuat_pada desc);
