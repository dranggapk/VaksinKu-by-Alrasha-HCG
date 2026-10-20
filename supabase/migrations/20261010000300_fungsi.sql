-- VaksinKu · tahap fondasi · 3/3: fungsi & pemicu
-- Semua penulisan booking, stok, pelayanan, dan tagihan lewat fungsi ini agar
-- aturan (slot, harga, stok, riwayat) ditegakkan database, apa pun aplikasinya.
-- Fungsi SECURITY DEFINER memeriksa hak pemanggil sendiri di awal.

-- ============================================================ waktu klinik (WIB)
create function public.hari_ini() returns date
language sql stable set search_path = '' as $$
  select (now() at time zone 'Asia/Jakarta')::date
$$;

-- ============================================================ pemicu umum
create function public.set_diubah_pada() returns trigger
language plpgsql set search_path = '' as $$
begin
  new.diubah_pada := now();
  return new;
end $$;

create trigger diubah_pada before update on public.klinik for each row execute function public.set_diubah_pada();
create trigger diubah_pada before update on public.profil for each row execute function public.set_diubah_pada();
create trigger diubah_pada before update on public.pasien for each row execute function public.set_diubah_pada();
create trigger diubah_pada before update on public.booking for each row execute function public.set_diubah_pada();
create trigger diubah_pada before update on public.riwayat_dosis for each row execute function public.set_diubah_pada();
create trigger diubah_pada before update on public.harga_klinik for each row execute function public.set_diubah_pada();

-- Profil dibuat otomatis saat akun baru terdaftar (login OTP pertama).
create function public.buat_profil_akun_baru() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  insert into public.profil (id, nama, hp)
  values (new.id, coalesce(new.raw_user_meta_data ->> 'nama', ''), coalesce(new.phone, ''))
  on conflict (id) do nothing;
  return new;
end $$;

create trigger profil_akun_baru after insert on auth.users
  for each row execute function public.buat_profil_akun_baru();

-- ============================================================ jejak audit
create function public.catat_audit(p_tabel text, p_aksi text, p_baris text, p_klinik text)
returns void language sql security definer set search_path = '' as $$
  insert into public.jejak_audit (user_id, klinik_id, tabel, aksi, baris_id)
  values (auth.uid(), p_klinik, p_tabel, p_aksi, coalesce(p_baris, ''))
$$;
revoke execute on function public.catat_audit(text, text, text, text) from public, anon, authenticated;

-- Perubahan data pasien oleh petugas tercatat otomatis.
create function public.audit_pasien() returns trigger
language plpgsql security definer set search_path = '' as $$
declare k text;
begin
  select klinik_id into k from public.anggota_klinik where user_id = auth.uid() limit 1;
  if k is not null then
    perform public.catat_audit(tg_table_name, lower(tg_op), coalesce(new.id, old.id)::text, k);
  end if;
  return coalesce(new, old);
end $$;
create trigger audit_pasien after insert or update or delete on public.pasien
  for each row execute function public.audit_pasien();

-- Petugas membuka detail pasien lewat fungsi ini agar tercatat siapa membuka.
create function public.buka_pasien(p_pasien uuid)
returns setof public.pasien language plpgsql security definer set search_path = '' as $$
declare k text;
begin
  if not public.pasien_terlihat_klinik(p_pasien) and not public.pasien_milik_saya(p_pasien) then
    raise exception 'Pasien tidak ditemukan' using errcode = '42501';
  end if;
  select b.klinik_id into k from public.booking_item bi join public.booking b on b.id = bi.booking_id
   where bi.pasien_id = p_pasien and b.klinik_id in (select public.klinik_saya()) limit 1;
  if k is null then
    select klinik_pendaftar into k from public.pasien where id = p_pasien and klinik_pendaftar in (select public.klinik_saya());
  end if;
  if k is not null then perform public.catat_audit('pasien', 'buka', p_pasien::text, k); end if;
  return query select * from public.pasien where id = p_pasien;
end $$;

-- ============================================================ booking
-- p_item: [{"pasien_id": "...", "vaksin_id": "v7-11"}, …]
-- Harga diambil dari harga_klinik di sini, bukan dari aplikasi.
create function public.buat_booking(
  p_klinik text, p_layanan text, p_lokasi text, p_tanggal date, p_jam time,
  p_tarif text, p_catatan text, p_bagikan_riwayat boolean, p_item jsonb
) returns public.booking language plpgsql security definer set search_path = '' as $$
declare
  kl public.klinik;
  b public.booking;
  petugas boolean := public.petugas_di(p_klinik);
  it jsonb;
  pid uuid;
  vid text;
  hk public.harga_klinik;
  terisi integer;
  baru integer;
begin
  if auth.uid() is null then raise exception 'Harus masuk terlebih dahulu' using errcode = '42501'; end if;
  select * into kl from public.klinik where id = p_klinik and aktif;
  if not found then raise exception 'Klinik tidak ditemukan' using errcode = 'P0002'; end if;
  if p_tarif not in ('umum', 'spesialis') then raise exception 'Tarif tidak dikenal'; end if;
  if jsonb_typeof(p_item) <> 'array' or jsonb_array_length(p_item) = 0 then
    raise exception 'Pilih minimal satu pasien dan satu vaksin';
  end if;
  if p_tanggal < public.hari_ini() then raise exception 'Tanggal tidak boleh di masa lalu'; end if;
  if extract(dow from p_tanggal)::smallint = any (kl.hari_libur) then
    raise exception 'Klinik libur pada tanggal tersebut';
  end if;
  if p_jam < kl.jam_buka or p_jam >= kl.jam_tutup then raise exception 'Jam di luar jam layanan klinik'; end if;

  -- Satu slot dikunci selama transaksi: dua pemesan bersamaan tidak bisa melebihi kapasitas.
  perform pg_advisory_xact_lock(hashtext(p_klinik || p_tanggal::text || p_jam::text));
  select count(distinct bi.pasien_id) into terisi
    from public.booking bk join public.booking_item bi on bi.booking_id = bk.id
   where bk.klinik_id = p_klinik and bk.tanggal = p_tanggal and bk.jam = p_jam
     and bk.status not in ('batal', 'tidak_hadir');
  select count(distinct (e ->> 'pasien_id')) into baru from jsonb_array_elements(p_item) e;
  if terisi + baru > kl.kapasitas_slot then
    raise exception 'Slot % penuh (sisa %), pilih jam lain', to_char(p_jam, 'HH24:MI'), greatest(kl.kapasitas_slot - terisi, 0);
  end if;

  insert into public.booking (kode, klinik_id, profil_id, layanan, lokasi, tanggal, jam, tarif, status,
                              catatan, bagikan_riwayat, sumber, dibuat_oleh)
  values ('VK-' || to_char(now() at time zone 'Asia/Jakarta', 'YYMMDD') || '-' || lpad(nextval('public.urut_booking')::text, 4, '0'),
          p_klinik, case when petugas then null else auth.uid() end, p_layanan, coalesce(p_lokasi, ''),
          p_tanggal, p_jam, p_tarif, case when petugas then 'terkonfirmasi' else 'baru' end,
          coalesce(p_catatan, ''), coalesce(p_bagikan_riwayat, false),
          case when petugas then 'petugas' else 'aplikasi' end, auth.uid())
  returning * into b;

  for it in select * from jsonb_array_elements(p_item) loop
    pid := (it ->> 'pasien_id')::uuid;
    vid := it ->> 'vaksin_id';
    if not (public.pasien_milik_saya(pid) or (petugas and public.pasien_terlihat_klinik(pid))
            or (petugas and exists (select 1 from public.pasien where id = pid and klinik_pendaftar = p_klinik))) then
      raise exception 'Pasien tidak dikenal' using errcode = '42501';
    end if;
    if not exists (select 1 from public.vaksin where id = vid and aktif) then raise exception 'Vaksin % tidak dikenal', vid; end if;
    select * into hk from public.harga_klinik where klinik_id = p_klinik and vaksin_id = vid;
    if found and not hk.tersedia then raise exception 'Vaksin % sedang tidak tersedia di klinik ini', vid; end if;
    insert into public.booking_item (booking_id, pasien_id, vaksin_id, harga)
    values (b.id, pid, vid, case when p_tarif = 'spesialis' then hk.harga_spesialis else hk.harga_umum end);
  end loop;

  -- Pendaftar booking dari aplikasi menautkan pilihan lokasi ke profilnya.
  if not petugas then
    update public.profil set kota_id = kl.kota_id, klinik_id = kl.id where id = auth.uid();
  end if;
  return b;
end $$;

-- Pasien: batal selama status 'baru'. Petugas: alur baru → terkonfirmasi → hadir.
-- Status 'selesai' hanya dari catat_pelayanan.
create function public.ubah_status_booking(p_booking uuid, p_status text)
returns public.booking language plpgsql security definer set search_path = '' as $$
declare b public.booking;
begin
  select * into b from public.booking where id = p_booking for update;
  if not found then raise exception 'Booking tidak ditemukan' using errcode = 'P0002'; end if;
  if public.petugas_di(b.klinik_id) then
    if not ((b.status = 'baru' and p_status in ('terkonfirmasi', 'batal'))
         or (b.status = 'terkonfirmasi' and p_status in ('hadir', 'batal', 'tidak_hadir'))
         or (b.status = 'hadir' and p_status = 'tidak_hadir')) then
      raise exception 'Status % tidak bisa diubah menjadi %', b.status, p_status;
    end if;
  elsif b.profil_id = auth.uid() then
    if not (b.status = 'baru' and p_status = 'batal') then
      raise exception 'Booking yang sudah dikonfirmasi hanya bisa diubah oleh klinik';
    end if;
  else
    raise exception 'Booking tidak ditemukan' using errcode = '42501';
  end if;
  update public.booking set status = p_status where id = p_booking returning * into b;
  return b;
end $$;

-- ============================================================ stok
create function public.terima_stok(p_klinik text, p_vaksin text, p_no_batch text, p_kedaluwarsa date, p_jumlah integer)
returns public.stok_batch language plpgsql security definer set search_path = '' as $$
declare s public.stok_batch;
begin
  if not public.petugas_di(p_klinik) then raise exception 'Hanya petugas klinik ini' using errcode = '42501'; end if;
  if p_jumlah is null or p_jumlah < 1 then raise exception 'Jumlah dosis minimal 1'; end if;
  if p_kedaluwarsa <= public.hari_ini() then raise exception 'Batch yang sudah kedaluwarsa tidak boleh diterima'; end if;
  insert into public.stok_batch (klinik_id, vaksin_id, no_batch, kedaluwarsa, jumlah, sisa)
  values (p_klinik, p_vaksin, trim(p_no_batch), p_kedaluwarsa, p_jumlah, p_jumlah)
  on conflict (klinik_id, vaksin_id, no_batch) do update
    set jumlah = public.stok_batch.jumlah + excluded.jumlah, sisa = public.stok_batch.sisa + excluded.sisa
  returning * into s;
  insert into public.mutasi_stok (stok_id, jenis, jumlah, keterangan, oleh)
  values (s.id, 'masuk', p_jumlah, 'Penerimaan', auth.uid());
  return s;
end $$;

-- p_jenis: 'buang' (rusak/kedaluwarsa), 'koreksi' (hasil hitung, boleh +/−), 'masuk'
create function public.sesuaikan_stok(p_stok uuid, p_jenis text, p_jumlah integer, p_keterangan text)
returns public.stok_batch language plpgsql security definer set search_path = '' as $$
declare s public.stok_batch; d integer;
begin
  select * into s from public.stok_batch where id = p_stok for update;
  if not found or not public.petugas_di(s.klinik_id) then raise exception 'Stok tidak ditemukan' using errcode = '42501'; end if;
  d := case p_jenis when 'buang' then -abs(p_jumlah) when 'masuk' then abs(p_jumlah) when 'koreksi' then p_jumlah end;
  if d is null or d = 0 then raise exception 'Jenis atau jumlah penyesuaian tidak valid'; end if;
  if s.sisa + d < 0 then raise exception 'Sisa stok tidak cukup (sisa %)', s.sisa; end if;
  update public.stok_batch set sisa = sisa + d, jumlah = jumlah + greatest(d, 0) * (p_jenis = 'masuk')::int
   where id = p_stok returning * into s;
  insert into public.mutasi_stok (stok_id, jenis, jumlah, keterangan, oleh)
  values (s.id, p_jenis, d, coalesce(p_keterangan, ''), auth.uid());
  return s;
end $$;

-- ============================================================ pelayanan
-- p_item: [{"vaksin_id": "v7-11", "stok_id": "…", "kunci": ["flu:1"]}, …]
-- "kunci" = dosis jadwal yang dipenuhi (dihitung dashboard dari src/jadwal_anak.py);
-- database memastikan antigennya memang terkandung dalam vaksin tersebut.
-- Satu transaksi: stok berkurang, riwayat dosis terverifikasi, tagihan terbit.
create function public.catat_pelayanan(
  p_booking uuid, p_pasien uuid, p_item jsonb, p_dokter uuid, p_kipi text, p_catatan text
) returns public.layanan language plpgsql security definer set search_path = '' as $$
declare
  b public.booking;
  l public.layanan;
  kl public.klinik;
  it jsonb;
  s public.stok_batch;
  v public.vaksin;
  k text;
  kunci text[];
  hrg integer;
  item_tagihan jsonb := '[]'::jsonb;
  total integer := 0;
begin
  select * into b from public.booking where id = p_booking for update;
  if not found or not public.petugas_di(b.klinik_id) then raise exception 'Booking tidak ditemukan' using errcode = '42501'; end if;
  if b.status <> 'hadir' then raise exception 'Pasien belum check-in (status %)', b.status; end if;
  if not exists (select 1 from public.booking_item where booking_id = b.id and pasien_id = p_pasien) then
    raise exception 'Pasien tidak terdaftar di booking ini';
  end if;
  if jsonb_typeof(p_item) <> 'array' or jsonb_array_length(p_item) = 0 then raise exception 'Belum ada vaksin yang dicatat'; end if;
  select * into kl from public.klinik where id = b.klinik_id;

  insert into public.layanan (booking_id, pasien_id, klinik_id, petugas, dokter_id, kipi, catatan)
  values (b.id, p_pasien, b.klinik_id, auth.uid(), p_dokter, coalesce(p_kipi, ''), coalesce(p_catatan, ''))
  returning * into l;

  for it in select * from jsonb_array_elements(p_item) loop
    select * into v from public.vaksin where id = it ->> 'vaksin_id';
    if not found then raise exception 'Vaksin % tidak dikenal', it ->> 'vaksin_id'; end if;
    select * into s from public.stok_batch where id = (it ->> 'stok_id')::uuid for update;
    if not found or s.klinik_id <> b.klinik_id or s.vaksin_id <> v.id then
      raise exception 'Batch stok tidak cocok untuk %', v.merek;
    end if;
    if s.sisa < 1 then raise exception 'Stok batch % habis', s.no_batch; end if;
    if s.kedaluwarsa <= public.hari_ini() then raise exception 'Batch % sudah kedaluwarsa', s.no_batch; end if;

    kunci := coalesce(array(select jsonb_array_elements_text(coalesce(it -> 'kunci', '[]'::jsonb))), '{}');
    foreach k in array kunci loop
      if not (split_part(k, ':', 1) = any (v.antigen)) then
        raise exception 'Dosis % tidak terkandung dalam %', k, v.merek;
      end if;
    end loop;

    update public.stok_batch set sisa = sisa - 1 where id = s.id;
    insert into public.mutasi_stok (stok_id, jenis, jumlah, keterangan, layanan_id, oleh)
    values (s.id, 'keluar', -1, 'Pelayanan ' || b.kode, l.id, auth.uid());

    insert into public.riwayat_dosis (pasien_id, kunci, label, tanggal, tempat, faskes, merek, no_batch,
                                      sumber, klinik_id, layanan_id, diverifikasi)
    values (p_pasien, kunci, v.kategori || ' — ' || v.merek, public.hari_ini(), 'Klinik', kl.nama, v.merek,
            s.no_batch, 'klinik', b.klinik_id, l.id, true);

    select bi.harga into hrg from public.booking_item bi
     where bi.booking_id = b.id and bi.pasien_id = p_pasien and bi.vaksin_id = v.id;
    if hrg is null then
      select case when b.tarif = 'spesialis' then harga_spesialis else harga_umum end into hrg
        from public.harga_klinik where klinik_id = b.klinik_id and vaksin_id = v.id;
    end if;
    item_tagihan := item_tagihan || jsonb_build_object('vaksin_id', v.id, 'nama', v.kategori || ' — ' || v.merek,
                                                       'no_batch', s.no_batch, 'harga', coalesce(hrg, 0));
    total := total + coalesce(hrg, 0);
  end loop;

  insert into public.tagihan (nomor, klinik_id, layanan_id, profil_id, item, total)
  values ('INV/' || to_char(now() at time zone 'Asia/Jakarta', 'YYYY') || '/' || lpad(nextval('public.urut_tagihan')::text, 5, '0'),
          b.klinik_id, l.id, (select profil_id from public.pasien where id = p_pasien), item_tagihan, total);

  -- Semua pasien dalam booking sudah dilayani → booking selesai.
  if not exists (select 1 from public.booking_item bi where bi.booking_id = b.id
                 and not exists (select 1 from public.layanan x where x.booking_id = b.id and x.pasien_id = bi.pasien_id)) then
    update public.booking set status = 'selesai' where id = b.id;
  end if;
  perform public.catat_audit('layanan', 'catat', l.id::text, b.klinik_id);
  return l;
end $$;

-- ============================================================ pembayaran
create function public.terima_pembayaran(p_tagihan uuid, p_jumlah integer, p_metode text)
returns public.tagihan language plpgsql security definer set search_path = '' as $$
declare t public.tagihan;
begin
  select * into t from public.tagihan where id = p_tagihan for update;
  if not found or not public.petugas_di(t.klinik_id) then raise exception 'Tagihan tidak ditemukan' using errcode = '42501'; end if;
  if t.status = 'lunas' then raise exception 'Tagihan % sudah lunas', t.nomor; end if;
  if p_jumlah is null or p_jumlah < 1 then raise exception 'Jumlah pembayaran tidak valid'; end if;
  insert into public.pembayaran (tagihan_id, jumlah, metode, oleh) values (t.id, p_jumlah, p_metode, auth.uid());
  update public.tagihan set dibayar = dibayar + p_jumlah,
         status = case when dibayar + p_jumlah >= total then 'lunas' else 'belum' end
   where id = t.id returning * into t;
  return t;
end $$;

-- ============================================================ hak eksekusi
-- Fungsi bantu RLS dipanggil kebijakan, bukan oleh aplikasi secara langsung.
revoke execute on all functions in schema public from public, anon;
grant execute on function public.klinik_saya(), public.petugas_di(text), public.admin_klinik_di(text),
  public.admin_vaksinku(), public.pasien_milik_saya(uuid), public.pasien_terlihat_klinik(uuid),
  public.riwayat_dibagikan(uuid), public.booking_milik_saya(uuid), public.booking_klinik_saya(uuid),
  public.hari_ini() to anon, authenticated;
grant execute on function public.buat_booking(text, text, text, date, time, text, text, boolean, jsonb),
  public.ubah_status_booking(uuid, text), public.terima_stok(text, text, text, date, integer),
  public.sesuaikan_stok(uuid, text, integer, text),
  public.catat_pelayanan(uuid, uuid, jsonb, uuid, text, text),
  public.terima_pembayaran(uuid, integer, text), public.buka_pasien(uuid) to authenticated;
grant usage on sequence public.urut_booking, public.urut_tagihan to authenticated;
