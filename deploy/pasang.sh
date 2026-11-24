#!/bin/sh
# Memasang / memperbarui VaksinKu di /opt/vaksinku. Aman dijalankan berulang:
# .env dan data database yang sudah ada tidak ditimpa.
set -eu
cd "$(dirname "$0")"

if [ ! -f .env ]; then
  umask 077
  cat > .env <<ENV
DB_ADMIN_PASSWORD=$(openssl rand -hex 24)
AUTHENTICATOR_PASSWORD=$(openssl rand -hex 24)
JWT_SECRET=$(openssl rand -hex 32)
GOOGLE_CLIENT_ID=
ENV
  echo ".env dibuat dengan kata sandi acak (jangan dibagikan)."
fi
chmod 600 .env
mkdir -p data/db cadangan
chmod 700 cadangan
chmod +x cadangkan.sh atur-google.sh db/init/*.sh 2>/dev/null || true

docker network inspect vaksinku-edge >/dev/null 2>&1 || docker network create vaksinku-edge
docker compose pull
docker compose up -d
docker network connect vaksinku-edge sih-deployment-caddy-1 2>/dev/null || true

echo "Menunggu layanan siap..."
sleep 8
docker compose ps
echo "== Cek =="
docker exec sih-deployment-caddy-1 wget -qO- http://vaksinku-web/auth/sehat && echo
docker exec sih-deployment-caddy-1 wget -qO- "http://vaksinku-web/api/klinik?select=id" && echo
