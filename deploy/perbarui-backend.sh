#!/bin/sh
# Memperbarui backend VaksinKu di VPS dari salinan repositori /opt/vaksinku/sumber.
# Dijalankan MANUAL oleh pengelola (bukan cron), satu baris:
#
#   sh /opt/vaksinku/sumber/deploy/perbarui-backend.sh
#
# 1. mencadangkan database          4. memuat ulang API & server web VaksinKu
# 2. memasang skrip & Caddyfile baru 5. memperbarui halaman (aplikasi, dashboard klinik)
# 3. menjalankan migrasi database tambahan (aman diulang)
# Hanya menyentuh /opt/vaksinku dan wadah vaksinku-*; sekolahibuhamil.id tidak disentuh.
set -eu
DASAR=/opt/vaksinku
SUMBER="$DASAR/sumber"
CABANG="${CABANG:-claude/vaksinku-app-continue-3dxaoq}"
cd "$DASAR"
[ -d "$SUMBER/.git" ] || { echo "Folder $SUMBER belum ada. Jalankan dulu: $DASAR/perbarui-situs.sh"; exit 1; }
git -C "$SUMBER" fetch --quiet --depth 1 origin "$CABANG"
git -C "$SUMBER" reset --quiet --hard FETCH_HEAD
echo "Versi: $(git -C "$SUMBER" log -1 --format='%h %s' | cut -c1-80)"

echo "1/5 Mencadangkan database..."
./cadangkan.sh

echo "2/5 Memasang skrip baru..."
for f in perbarui-situs.sh cadangkan.sh atur-google.sh jadikan-admin.sh; do
  sed 's/\r$//' "$SUMBER/deploy/$f" > "$DASAR/$f.baru"
  chmod 755 "$DASAR/$f.baru" && mv "$DASAR/$f.baru" "$DASAR/$f"
done
cp web/Caddyfile web/Caddyfile.sebelum
# ditulis ke berkas yang sama (bukan diganti) agar wadah web langsung melihatnya
sed 's/\r$//' "$SUMBER/deploy/web/Caddyfile" > web/Caddyfile

echo "3/5 Migrasi database..."
for m in "$SUMBER"/supabase/migrations/*.sql; do
  n=$(basename "$m")
  # tiga migrasi pertama sudah terpasang saat pasang.sh; yang sesudahnya aman diulang
  [ "$(expr "$n" \> "20261010000300_fungsi.sql")" = 1 ] || continue
  sed 's/\r$//' "$m" | docker exec -i vaksinku-db psql -q -v ON_ERROR_STOP=1 -U vaksinku_admin -d vaksinku
  sed 's/\r$//' "$m" > "db/init/40_$n"
  echo "   terpasang: $n"
done

echo "4/5 Memuat ulang API & server web..."
docker compose kill -s SIGUSR1 api >/dev/null
docker compose restart web >/dev/null

echo "5/5 Memperbarui halaman..."
./perbarui-situs.sh
tail -n 3 perbarui-situs.log
echo "SELESAI"
