#!/bin/sh
# Cadangan harian database VaksinKu ke /opt/vaksinku/cadangan (14 terakhir disimpan).
# Jam server memakai UTC: 19.15 UTC = 02.15 WIB. Jadwalkan:  (crontab -l 2>/dev/null; echo "15 19 * * * /opt/vaksinku/cadangkan.sh") | crontab -
set -eu
cd "$(dirname "$0")"
umask 077
mkdir -p cadangan
f="cadangan/vaksinku-$(date +%Y%m%d-%H%M).sql.gz"
docker exec vaksinku-db pg_dump -U vaksinku_admin -d vaksinku --no-owner | gzip > "$f"
ls -1t cadangan/vaksinku-*.sql.gz | tail -n +15 | xargs -r rm --
echo "Cadangan: $f ($(du -h "$f" | cut -f1))"
