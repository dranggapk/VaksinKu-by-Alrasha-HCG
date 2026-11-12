-- VaksinKu di VPS · dasar akun & peran (pengganti bagian Supabase yang dipakai migrasi).
-- Dijalankan sekali saat database dibuat, sebelum supabase/migrations/*.sql.
--
-- Peran:
--   authenticator   login milik PostgREST; tidak punya hak apa pun selain berganti peran
--   anon            pengunjung tanpa login (katalog saja, diatur RLS)
--   authenticated   pengguna dengan sesi VaksinKu (diatur RLS)
--   layanan_masuk   dipakai layanan login untuk mendaftarkan akun Google; hanya boleh
--                   menjalankan public.masuk_google()
--   service_role    pemeliharaan; tidak diberikan ke PostgREST

do $$ begin
  if not exists (select 1 from pg_roles where rolname = 'anon') then create role anon nologin; end if;
  if not exists (select 1 from pg_roles where rolname = 'authenticated') then create role authenticated nologin; end if;
  if not exists (select 1 from pg_roles where rolname = 'service_role') then create role service_role nologin bypassrls; end if;
  if not exists (select 1 from pg_roles where rolname = 'layanan_masuk') then create role layanan_masuk nologin; end if;
  if not exists (select 1 from pg_roles where rolname = 'authenticator') then create role authenticator login noinherit; end if;
end $$;
grant anon, authenticated, layanan_masuk to authenticator;

create schema if not exists auth;
grant usage on schema auth to anon, authenticated, service_role;

create table if not exists auth.users (
  id                 uuid primary key default gen_random_uuid(),
  google_sub         text unique,                 -- pengenal akun Google ("sub" pada token)
  phone              text unique,
  email              text unique,
  raw_user_meta_data jsonb default '{}'::jsonb,   -- nama & foto dari Google
  created_at         timestamptz default now(),
  last_sign_in_at    timestamptz
);
revoke all on auth.users from anon, authenticated, layanan_masuk;

-- Identitas pemanggil dibaca dari klaim JWT yang dipasang PostgREST per permintaan.
create or replace function auth.uid() returns uuid language sql stable as $$
  select nullif(coalesce(current_setting('request.jwt.claim.sub', true),
    (nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'sub')), '')::uuid
$$;
grant execute on function auth.uid() to anon, authenticated, service_role;

grant usage on schema public to anon, authenticated, layanan_masuk, service_role;
-- Hak dasar tabel baru; akses sesungguhnya dibatasi ulang oleh migrasi keamanan + RLS.
alter default privileges in schema public grant all on tables to anon, authenticated, service_role;
alter default privileges in schema public grant all on sequences to anon, authenticated, service_role;
alter default privileges in schema public grant execute on functions to anon, authenticated, service_role;
