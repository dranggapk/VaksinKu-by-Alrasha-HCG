-- VaksinKu di VPS · pendaftaran/masuk akun Google.
-- Dipanggil layanan login (deploy/backend/auth) SETELAH token Google diverifikasi di
-- server: tanda tangan, aplikasi tujuan (aud), penerbit, masa berlaku, email terverifikasi.
-- Menghasilkan id akun VaksinKu; profil dibuat otomatis oleh pemicu profil_akun_baru.

create or replace function public.masuk_google(p_sub text, p_email text, p_nama text, p_foto text)
returns uuid language plpgsql security definer set search_path = '' as $$
declare
  v_id uuid;
begin
  if coalesce(trim(p_sub), '') = '' or coalesce(trim(p_email), '') = '' then
    raise exception 'Data akun Google tidak lengkap';
  end if;

  update auth.users
     set email = lower(p_email),
         raw_user_meta_data = coalesce(raw_user_meta_data, '{}'::jsonb)
                              || jsonb_build_object('nama', coalesce(p_nama, ''), 'foto', coalesce(p_foto, '')),
         last_sign_in_at = now()
   where google_sub = p_sub
  returning id into v_id;

  if v_id is null then
    insert into auth.users (google_sub, email, raw_user_meta_data, last_sign_in_at)
    values (p_sub, lower(p_email), jsonb_build_object('nama', coalesce(p_nama, ''), 'foto', coalesce(p_foto, '')), now())
    returning id into v_id;
  end if;
  return v_id;
end $$;

revoke execute on function public.masuk_google(text, text, text, text) from public, anon, authenticated;
grant execute on function public.masuk_google(text, text, text, text) to layanan_masuk;
