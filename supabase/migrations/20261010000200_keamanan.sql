-- VaksinKu · tahap fondasi · 2/3: hak akses (Row Level Security)
-- Aturan dijalankan database untuk setiap baris, bukan oleh aplikasi.
-- Fungsi bantu SECURITY DEFINER agar kebijakan tidak saling memanggil RLS
-- (mencegah rekursi) dan cepat; search_path dikosongkan, nama ditulis lengkap.

-- ============================================================ fungsi bantu peran
create function public.klinik_saya() returns setof text
language sql stable security definer set search_path = '' as $$
  select klinik_id from public.anggota_klinik where user_id = auth.uid()
$$;

create function public.petugas_di(k text) returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (select 1 from public.anggota_klinik where user_id = auth.uid() and klinik_id = k)
$$;

create function public.admin_klinik_di(k text) returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (select 1 from public.anggota_klinik
                 where user_id = auth.uid() and klinik_id = k and peran = 'admin')
$$;

create function public.admin_vaksinku() returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (select 1 from public.admin_vaksinku where user_id = auth.uid())
$$;

create function public.pasien_milik_saya(p uuid) returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (select 1 from public.pasien where id = p and profil_id = auth.uid())
$$;

-- Pasien terlihat oleh klinik bila pernah booking di sana atau didaftarkan klinik itu.
create function public.pasien_terlihat_klinik(p uuid) returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (
    select 1 from public.booking_item bi join public.booking b on b.id = bi.booking_id
    where bi.pasien_id = p and b.klinik_id in (select public.klinik_saya())
  ) or exists (
    select 1 from public.pasien where id = p and klinik_pendaftar in (select public.klinik_saya())
  )
$$;

-- Riwayat dosis dari luar klinik hanya terlihat bila pasien membagikannya saat booking.
create function public.riwayat_dibagikan(p uuid) returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (
    select 1 from public.booking_item bi join public.booking b on b.id = bi.booking_id
    where bi.pasien_id = p and b.bagikan_riwayat and b.klinik_id in (select public.klinik_saya())
  ) or exists (
    select 1 from public.pasien where id = p and klinik_pendaftar in (select public.klinik_saya())
  )
$$;

create function public.booking_milik_saya(b uuid) returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (select 1 from public.booking where id = b and profil_id = auth.uid())
$$;

create function public.booking_klinik_saya(b uuid) returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (select 1 from public.booking where id = b and klinik_id in (select public.klinik_saya()))
$$;

-- ============================================================ hak dasar tabel
-- Supabase memberi anon & authenticated hak penuh pada tabel baru; dipersempit di sini.
revoke all on all tables in schema public from anon, authenticated;
revoke all on all sequences in schema public from anon, authenticated;

-- Katalog boleh dibaca sebelum masuk (price list terbuka).
grant select on public.kota, public.klinik, public.vaksin, public.harga_klinik,
  public.dokter, public.promo to anon, authenticated;
grant insert, update, delete on public.klinik, public.harga_klinik, public.dokter,
  public.promo, public.kota, public.vaksin to authenticated;

grant select, update on public.profil to authenticated;
grant select, insert, update, delete on public.pasien, public.riwayat_dosis,
  public.rencana_puskesmas to authenticated;
grant select, insert, update, delete on public.anggota_klinik to authenticated;
grant select on public.admin_vaksinku to authenticated;
-- Booking, stok, pelayanan, tagihan: dibaca langsung, ditulis lewat fungsi (3/3).
grant select on public.booking, public.booking_item, public.stok_batch, public.mutasi_stok,
  public.layanan, public.tagihan, public.pembayaran, public.jejak_audit to authenticated;

-- ============================================================ RLS menyala di semua tabel
alter table public.kota              enable row level security;
alter table public.klinik            enable row level security;
alter table public.vaksin            enable row level security;
alter table public.harga_klinik      enable row level security;
alter table public.dokter            enable row level security;
alter table public.promo             enable row level security;
alter table public.profil            enable row level security;
alter table public.pasien            enable row level security;
alter table public.anggota_klinik    enable row level security;
alter table public.admin_vaksinku    enable row level security;
alter table public.booking           enable row level security;
alter table public.booking_item      enable row level security;
alter table public.stok_batch        enable row level security;
alter table public.layanan           enable row level security;
alter table public.mutasi_stok       enable row level security;
alter table public.riwayat_dosis     enable row level security;
alter table public.rencana_puskesmas enable row level security;
alter table public.tagihan           enable row level security;
alter table public.pembayaran        enable row level security;
alter table public.jejak_audit       enable row level security;

-- ============================================================ katalog & mitra
create policy "katalog: kota aktif terbuka" on public.kota for select using (aktif or (select public.admin_vaksinku()));
create policy "katalog: admin vaksinku kelola kota" on public.kota for all to authenticated
  using ((select public.admin_vaksinku())) with check ((select public.admin_vaksinku()));

create policy "klinik: aktif terbuka" on public.klinik for select
  using (aktif or (select public.admin_vaksinku()) or public.petugas_di(id));
create policy "klinik: admin klinik ubah kliniknya" on public.klinik for update to authenticated
  using (public.admin_klinik_di(id) or (select public.admin_vaksinku()))
  with check (public.admin_klinik_di(id) or (select public.admin_vaksinku()));
create policy "klinik: admin vaksinku tambah" on public.klinik for insert to authenticated
  with check ((select public.admin_vaksinku()));
create policy "klinik: admin vaksinku hapus" on public.klinik for delete to authenticated
  using ((select public.admin_vaksinku()));

create policy "vaksin: terbuka" on public.vaksin for select using (true);
create policy "vaksin: admin vaksinku kelola" on public.vaksin for all to authenticated
  using ((select public.admin_vaksinku())) with check ((select public.admin_vaksinku()));

create policy "harga: terbuka" on public.harga_klinik for select
  using (tersedia or public.petugas_di(klinik_id) or (select public.admin_vaksinku()));
create policy "harga: admin klinik kelola kliniknya" on public.harga_klinik for all to authenticated
  using (public.admin_klinik_di(klinik_id) or (select public.admin_vaksinku()))
  with check (public.admin_klinik_di(klinik_id) or (select public.admin_vaksinku()));

create policy "dokter: aktif terbuka" on public.dokter for select using (aktif or public.petugas_di(klinik_id));
create policy "dokter: admin klinik kelola" on public.dokter for all to authenticated
  using (public.admin_klinik_di(klinik_id) or (select public.admin_vaksinku()))
  with check (public.admin_klinik_di(klinik_id) or (select public.admin_vaksinku()));

create policy "promo: berlaku terbuka" on public.promo for select
  using ((aktif and (berlaku_sampai is null or berlaku_sampai >= current_date))
         or (klinik_id is not null and public.petugas_di(klinik_id)) or (select public.admin_vaksinku()));
create policy "promo: admin klinik kelola" on public.promo for all to authenticated
  using ((klinik_id is not null and public.admin_klinik_di(klinik_id)) or (select public.admin_vaksinku()))
  with check ((klinik_id is not null and public.admin_klinik_di(klinik_id)) or (select public.admin_vaksinku()));

-- ============================================================ profil & pasien
create policy "profil: pemilik baca" on public.profil for select to authenticated
  using (id = (select auth.uid()));
create policy "profil: petugas baca pendaftar booking kliniknya" on public.profil for select to authenticated
  using (exists (select 1 from public.booking b where b.profil_id = profil.id
                 and b.klinik_id in (select public.klinik_saya())));
create policy "profil: pemilik ubah" on public.profil for update to authenticated
  using (id = (select auth.uid())) with check (id = (select auth.uid()));

create policy "pasien: pemilik baca" on public.pasien for select to authenticated
  using (profil_id = (select auth.uid()));
create policy "pasien: petugas baca pasien kliniknya" on public.pasien for select to authenticated
  using (public.pasien_terlihat_klinik(id));
create policy "pasien: pemilik tambah" on public.pasien for insert to authenticated
  with check (profil_id = (select auth.uid()) and klinik_pendaftar is null);
create policy "pasien: petugas daftarkan pasien tanpa akun" on public.pasien for insert to authenticated
  with check (profil_id is null and klinik_pendaftar in (select public.klinik_saya()));
create policy "pasien: pemilik ubah" on public.pasien for update to authenticated
  using (profil_id = (select auth.uid())) with check (profil_id = (select auth.uid()));
create policy "pasien: petugas ubah pasien tanpa akun dari kliniknya" on public.pasien for update to authenticated
  using (profil_id is null and klinik_pendaftar in (select public.klinik_saya()))
  with check (profil_id is null and klinik_pendaftar in (select public.klinik_saya()));
create policy "pasien: pemilik hapus" on public.pasien for delete to authenticated
  using (profil_id = (select auth.uid()));

-- ============================================================ riwayat dosis & rencana puskesmas
create policy "riwayat: pemilik baca" on public.riwayat_dosis for select to authenticated
  using (public.pasien_milik_saya(pasien_id));
create policy "riwayat: klinik baca catatannya & yang dibagikan" on public.riwayat_dosis for select to authenticated
  using ((sumber = 'klinik' and klinik_id in (select public.klinik_saya()))
         or public.riwayat_dibagikan(pasien_id));
-- Pasien hanya menulis catatannya sendiri; catatan klinik (terverifikasi) dibuat lewat catat_pelayanan.
create policy "riwayat: pemilik tambah catatan sendiri" on public.riwayat_dosis for insert to authenticated
  with check (public.pasien_milik_saya(pasien_id) and sumber = 'pasien' and not diverifikasi
              and klinik_id is null and layanan_id is null);
create policy "riwayat: pemilik ubah catatan sendiri" on public.riwayat_dosis for update to authenticated
  using (public.pasien_milik_saya(pasien_id) and sumber = 'pasien')
  with check (public.pasien_milik_saya(pasien_id) and sumber = 'pasien' and not diverifikasi
              and klinik_id is null and layanan_id is null);
create policy "riwayat: pemilik hapus catatan sendiri" on public.riwayat_dosis for delete to authenticated
  using (public.pasien_milik_saya(pasien_id) and sumber = 'pasien');

create policy "rencana: pemilik kelola" on public.rencana_puskesmas for all to authenticated
  using (public.pasien_milik_saya(pasien_id)) with check (public.pasien_milik_saya(pasien_id));

-- ============================================================ petugas & admin
create policy "anggota: lihat keanggotaan sendiri & rekan klinik" on public.anggota_klinik for select to authenticated
  using (user_id = (select auth.uid()) or klinik_id in (select public.klinik_saya()) or (select public.admin_vaksinku()));
create policy "anggota: admin klinik kelola kliniknya" on public.anggota_klinik for insert to authenticated
  with check (public.admin_klinik_di(klinik_id) or (select public.admin_vaksinku()));
create policy "anggota: admin klinik ubah kliniknya" on public.anggota_klinik for update to authenticated
  using (public.admin_klinik_di(klinik_id) or (select public.admin_vaksinku()))
  with check (public.admin_klinik_di(klinik_id) or (select public.admin_vaksinku()));
create policy "anggota: admin klinik cabut kliniknya" on public.anggota_klinik for delete to authenticated
  using ((public.admin_klinik_di(klinik_id) and user_id <> (select auth.uid())) or (select public.admin_vaksinku()));

create policy "admin vaksinku: lihat diri sendiri" on public.admin_vaksinku for select to authenticated
  using (user_id = (select auth.uid()));

-- ============================================================ operasional (baca saja; tulis lewat fungsi)
create policy "booking: pemilik baca" on public.booking for select to authenticated
  using (profil_id = (select auth.uid()));
create policy "booking: klinik baca" on public.booking for select to authenticated
  using (klinik_id in (select public.klinik_saya()));

create policy "booking item: pemilik baca" on public.booking_item for select to authenticated
  using (public.booking_milik_saya(booking_id));
create policy "booking item: klinik baca" on public.booking_item for select to authenticated
  using (public.booking_klinik_saya(booking_id));

create policy "stok: klinik baca" on public.stok_batch for select to authenticated
  using (klinik_id in (select public.klinik_saya()));
create policy "mutasi: klinik baca" on public.mutasi_stok for select to authenticated
  using (exists (select 1 from public.stok_batch s where s.id = stok_id and s.klinik_id in (select public.klinik_saya())));

create policy "layanan: pemilik baca" on public.layanan for select to authenticated
  using (public.pasien_milik_saya(pasien_id));
create policy "layanan: klinik baca" on public.layanan for select to authenticated
  using (klinik_id in (select public.klinik_saya()));

create policy "tagihan: pemilik baca" on public.tagihan for select to authenticated
  using (profil_id = (select auth.uid()));
create policy "tagihan: klinik baca" on public.tagihan for select to authenticated
  using (klinik_id in (select public.klinik_saya()));

create policy "pembayaran: pemilik baca" on public.pembayaran for select to authenticated
  using (exists (select 1 from public.tagihan t where t.id = tagihan_id and t.profil_id = (select auth.uid())));
create policy "pembayaran: klinik baca" on public.pembayaran for select to authenticated
  using (exists (select 1 from public.tagihan t where t.id = tagihan_id and t.klinik_id in (select public.klinik_saya())));

create policy "audit: admin klinik baca kliniknya" on public.jejak_audit for select to authenticated
  using (public.admin_klinik_di(klinik_id) or (select public.admin_vaksinku()));
