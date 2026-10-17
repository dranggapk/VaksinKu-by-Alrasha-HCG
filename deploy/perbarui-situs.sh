#!/bin/sh
# Memperbarui halaman vaksinku.app dari GitHub (dijalankan cron setiap 15 menit).
#
# Hanya MENYALIN berkas statis ke /opt/vaksinku/situs:
#   VaksinKu-App.html       → situs/index.html
#   VaksinKu-Dashboard.html → situs/klinik.html   (dashboard klinik, wajib masuk petugas)
#   situs/privasi.html      → situs/privasi.html
#   situs/manifest.json, situs/ikon/*.png → ikon aplikasi di layar utama HP
# Tidak menjalankan kode apa pun dari repositori, dan tidak menyentuh backend,
# database, maupun sekolahibuhamil.id. Perubahan backend lewat perbarui-backend.sh.
#
# Pasang:  (crontab -l 2>/dev/null; echo "*/15 * * * * /opt/vaksinku/perbarui-situs.sh") | crontab -
set -eu
REPO="https://github.com/dranggapk/VaksinKu-by-Alrasha-HCG.git"
CABANG="${CABANG:-claude/vaksinku-app-continue-3dxaoq}"
DASAR=/opt/vaksinku
SUMBER="$DASAR/sumber"
SITUS="$DASAR/situs"
LOG="$DASAR/perbarui-situs.log"

catat() { echo "$(TZ=Asia/Jakarta date '+%d-%m-%Y %H:%M') $*" >> "$LOG"; }

if [ ! -d "$SUMBER/.git" ]; then
  git clone --quiet --depth 1 --branch "$CABANG" "$REPO" "$SUMBER"
else
  git -C "$SUMBER" fetch --quiet --depth 1 origin "$CABANG" || { catat "GAGAL ambil dari GitHub"; exit 1; }
  git -C "$SUMBER" reset --quiet --hard FETCH_HEAD
fi

# pasang satu berkas bila berubah dan lolos pemeriksaan sederhana
pasang() {
  asal="$1"; tujuan="$2"; minimal="$3"; penanda="$4"
  [ -f "$asal" ] || { catat "GAGAL $asal tidak ada"; return 1; }
  ukuran=$(wc -c < "$asal")
  if [ "$ukuran" -lt "$minimal" ] || ! grep -q "$penanda" "$asal"; then
    catat "TOLAK $(basename "$asal") (ukuran $ukuran, penanda tidak ada)"; return 1
  fi
  if [ -f "$tujuan" ] && cmp -s "$asal" "$tujuan"; then return 0; fi
  cp "$asal" "$tujuan.baru" && chmod 644 "$tujuan.baru" && mv "$tujuan.baru" "$tujuan"
  catat "OK $(basename "$tujuan") diperbarui ke $(git -C "$SUMBER" log -1 --format='%h %s' | cut -c1-80)"
}

pasang "$SUMBER/VaksinKu-App.html" "$SITUS/index.html" 200000 "VaksinKu"
pasang "$SUMBER/situs/privasi.html" "$SITUS/privasi.html" 5000 "Kebijakan Privasi"
pasang "$SUMBER/VaksinKu-Dashboard.html" "$SITUS/klinik.html" 200000 "VaksinKuKlinik" || true
# ikon layar utama HP & manifest aplikasi (berkas PNG diperiksa tanda tangan berkasnya)
mkdir -p "$SITUS/ikon"
pasang "$SUMBER/situs/manifest.json" "$SITUS/manifest.json" 300 '"short_name"' || true
for f in "$SUMBER"/situs/ikon/*.png; do
  [ -f "$f" ] || continue
  head -c 4 "$f" | grep -q PNG && pasang "$f" "$SITUS/ikon/$(basename "$f")" 300 "" || true
done

# simpan 300 baris log terakhir
[ -f "$LOG" ] && tail -n 300 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG" || true
