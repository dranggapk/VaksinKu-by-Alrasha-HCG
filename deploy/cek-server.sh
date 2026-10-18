#!/bin/sh
# Memeriksa kesehatan VaksinKu di VPS dan menyalakan lagi bagian yang mati.
# Aman dijalankan kapan saja; hanya menyentuh wadah vaksinku-* (sekolahibuhamil.id tidak disentuh).
#
#   sh /opt/vaksinku/sumber/deploy/cek-server.sh
cd /opt/vaksinku || exit 1
uji_api() { docker exec vaksinku-web wget -qO- -T 5 'http://api:3000/klinik?select=id' >/dev/null 2>&1; }

echo "== Status wadah VaksinKu =="
docker compose ps --format 'table {{.Name}}\t{{.State}}\t{{.Status}}'

echo "== API (database lewat PostgREST) =="
if uji_api; then
  echo "API: OK"
else
  echo "API: TIDAK MERESPONS. Log terakhir:"
  docker compose logs --tail=25 api
  echo "Menyalakan lagi API..."
  docker compose up -d api >/dev/null 2>&1
  sleep 6
  if uji_api; then echo "API: OK setelah dinyalakan lagi"; else echo "API: MASIH GAGAL - kirim tangkapan layar ini"; fi
fi

echo "== Layanan masuk Google =="
docker exec vaksinku-web wget -qO- -T 5 http://auth:8080/auth/sehat 2>/dev/null && echo || {
  echo "AUTH: tidak merespons, menyalakan lagi..."; docker compose up -d auth >/dev/null 2>&1; }

echo "== Database =="
docker exec vaksinku-db pg_isready -U vaksinku_admin -d vaksinku
echo "SELESAI"
