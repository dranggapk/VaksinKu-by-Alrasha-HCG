#!/bin/sh
# Dijalankan sekali oleh image postgres saat database dibuat: memberi kata sandi
# login PostgREST dari .env (AUTHENTICATOR_PASSWORD).
set -eu
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
  -c "alter role authenticator with login password '${AUTHENTICATOR_PASSWORD}'"
