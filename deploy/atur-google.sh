#!/bin/sh
# Memasang Client ID Google ke layanan masuk:  ./atur-google.sh 1234-abc.apps.googleusercontent.com
set -eu
cd "$(dirname "$0")"
case "${1:-}" in
  *.apps.googleusercontent.com) ;;
  *) echo "Pakai: ./atur-google.sh <CLIENT_ID>.apps.googleusercontent.com"; exit 1 ;;
esac
if grep -q '^GOOGLE_CLIENT_ID=' .env; then
  sed -i "s|^GOOGLE_CLIENT_ID=.*|GOOGLE_CLIENT_ID=$1|" .env
else
  echo "GOOGLE_CLIENT_ID=$1" >> .env
fi
docker compose up -d auth
sleep 2
docker exec sih-deployment-caddy-1 wget -qO- http://vaksinku-web/auth/sehat && echo
