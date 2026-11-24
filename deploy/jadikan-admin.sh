#!/bin/sh
# Menjadikan akun Google sebagai ADMIN dashboard klinik (langkah awal).
# Selanjutnya admin menambah petugas sendiri di dashboard: Pengaturan → Petugas klinik.
#
#   /opt/vaksinku/jadikan-admin.sh email@gmail.com alrasha-hcc
#   /opt/vaksinku/jadikan-admin.sh email@gmail.com semua        (semua klinik)
#
# Orangnya harus sudah pernah membuka https://vaksinku.app/klinik.html dan masuk dengan Google.
set -eu
if [ $# -ne 2 ]; then
  echo "Pakai: $0 <email-google> <id-klinik|semua>"
  echo "ID klinik yang ada:"
  docker exec vaksinku-db psql -At -U vaksinku_admin -d vaksinku -c "select '  ' || id || '  (' || nama || ')' from public.klinik order by id"
  exit 1
fi
docker exec -i vaksinku-db psql -At -v ON_ERROR_STOP=1 -U vaksinku_admin -d vaksinku -v email="$1" -v klinik="$2" <<'SQL'
with u as (select id from auth.users where lower(email) = lower(trim(:'email'))),
ins as (
  insert into public.anggota_klinik (user_id, klinik_id, peran)
  select u.id, k.id, 'admin' from u, public.klinik k where k.id = :'klinik' or :'klinik' = 'semua'
  on conflict (user_id, klinik_id) do update set peran = 'admin'
  returning klinik_id)
select case
  when not exists (select 1 from u) then 'BELUM: email ini belum pernah masuk. Buka https://vaksinku.app/klinik.html, masuk dengan Google, lalu ulangi perintah ini.'
  when not exists (select 1 from ins) then 'BELUM: id klinik tidak dikenal. Jalankan perintah tanpa isian untuk melihat daftarnya.'
  else 'BERHASIL: ' || :'email' || ' menjadi admin di ' || (select string_agg(klinik_id, ', ') from ins)
end;
SQL
