-- VaksinKu · dashboard klinik: kelola petugas lewat email akun Google.
-- auth.users tidak terbuka bagi aplikasi, jadi pencarian email dilakukan fungsi
-- SECURITY DEFINER yang memeriksa peran pemanggil lebih dulu.
-- Aman dijalankan ulang (create or replace) — dipakai deploy/perbarui-backend.sh.

-- Daftar petugas sebuah klinik (untuk semua petugas klinik itu).
create or replace function public.daftar_petugas(p_klinik text)
returns table (user_id uuid, email text, nama text, peran text)
language plpgsql stable security definer set search_path = '' as $$
begin
  if not (public.petugas_di(p_klinik) or public.admin_vaksinku()) then
    raise exception 'Hanya petugas klinik ini' using errcode = '42501';
  end if;
  return query
    select a.user_id, coalesce(u.email, '')::text,
           coalesce(nullif(p.nama, ''), u.raw_user_meta_data ->> 'nama', u.raw_user_meta_data ->> 'name', '')::text,
           a.peran
      from public.anggota_klinik a
      join auth.users u on u.id = a.user_id
      left join public.profil p on p.id = a.user_id
     where a.klinik_id = p_klinik
     order by a.peran, 2;
end $$;

-- Admin klinik menambah atau mengubah peran petugas. Orangnya harus sudah pernah
-- masuk ke VaksinKu dengan Google sekali (agar akunnya ada).
create or replace function public.tambah_petugas(p_klinik text, p_email text, p_peran text)
returns void language plpgsql security definer set search_path = '' as $$
declare uid uuid;
begin
  if not (public.admin_klinik_di(p_klinik) or public.admin_vaksinku()) then
    raise exception 'Hanya admin klinik ini' using errcode = '42501';
  end if;
  if p_peran not in ('petugas', 'admin') then raise exception 'Peran tidak dikenal'; end if;
  select id into uid from auth.users where lower(email) = lower(trim(p_email));
  if uid is null then
    raise exception 'Email % belum pernah masuk ke VaksinKu. Minta orangnya membuka vaksinku.app/klinik.html dan masuk dengan Google sekali, lalu tambahkan lagi.', trim(p_email);
  end if;
  insert into public.anggota_klinik (user_id, klinik_id, peran) values (uid, p_klinik, p_peran)
  on conflict (user_id, klinik_id) do update set peran = excluded.peran;
  perform public.catat_audit('anggota_klinik', 'tambah', uid::text, p_klinik);
end $$;

create or replace function public.cabut_petugas(p_klinik text, p_user uuid)
returns void language plpgsql security definer set search_path = '' as $$
begin
  if not (public.admin_klinik_di(p_klinik) or public.admin_vaksinku()) then
    raise exception 'Hanya admin klinik ini' using errcode = '42501';
  end if;
  if p_user = auth.uid() then raise exception 'Tidak bisa mencabut akses diri sendiri'; end if;
  delete from public.anggota_klinik where user_id = p_user and klinik_id = p_klinik;
  perform public.catat_audit('anggota_klinik', 'cabut', p_user::text, p_klinik);
end $$;

revoke execute on function public.daftar_petugas(text), public.tambah_petugas(text, text, text),
  public.cabut_petugas(text, uuid) from public, anon;
grant execute on function public.daftar_petugas(text), public.tambah_petugas(text, text, text),
  public.cabut_petugas(text, uuid) to authenticated;

-- Petugas mendaftarkan pasien datang langsung lalu langsung membaca barisnya
-- (INSERT … RETURNING). pasien_terlihat_klinik() tidak melihat baris yang baru
-- disisipkan dalam perintah yang sama, jadi kolomnya diperiksa langsung di sini.
drop policy if exists "pasien: petugas baca pasien daftarannya" on public.pasien;
create policy "pasien: petugas baca pasien daftarannya" on public.pasien for select to authenticated
  using (profil_id is null and klinik_pendaftar in (select public.klinik_saya()));

-- PostgREST memuat ulang daftar fungsi.
notify pgrst, 'reload schema';
