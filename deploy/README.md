# Memasang VaksinKu di VPS bersama sekolahibuhamil.id — tahap 1

Tahap ini menayangkan **https://vaksinku.app** (aplikasi pasien) dan
**https://vaksinku.app/privasi.html** (Kebijakan Privasi). Backend dan database
VaksinKu menyusul di tahap berikutnya, di folder yang sama.

## Susunan

```
internet ──► Caddy sih-deployment (port 80/443, HTTPS otomatis)
               ├─ api.sekolahibuhamil.id  → license-service   (tidak diubah)
               ├─ cms.sekolahibuhamil.id  → directus          (tidak diubah)
               └─ vaksinku.app            → vaksinku-web      (BARU, lewat jaringan vaksinku-edge)
```

| Milik VaksinKu | Letak |
|---|---|
| Berkas & pengaturan | `/opt/vaksinku` |
| Wadah | `vaksinku-web` (proyek Docker `vaksinku`) |
| Jaringan | `vaksinku-edge` — hanya berisi `vaksinku-web` dan Caddy |
| Batas sumber daya | 128 MB RAM, 0,5 CPU |

Yang disentuh dari sih-deployment hanya dua hal, keduanya bisa dibatalkan:
1. Caddy disambungkan ke jaringan `vaksinku-edge` (`docker network connect`, tanpa restart).
2. Satu blok `vaksinku.app` **ditambahkan di akhir** `Caddyfile` (isi lama tidak diubah),
   diperiksa dengan `caddy validate`, lalu dimuat dengan `caddy reload` (tanpa henti).

Caddy sih-deployment tidak menulis log akses (Caddyfile tidak memakai `log`), dan hanya
meneruskan permintaan; ia tidak menyimpan data VaksinKu.

## Langkah

Sebelum mulai: buat **snapshot** di hPanel (Backup & Monitoring → Snapshot).
Setiap blok perintah dijalankan di VPS (`root@srv1888911:~#`) kecuali Langkah 2.

### 1. Buat folder & pengaturan VaksinKu (VPS)

Salin isi `docker-compose.yml` dan `web/Caddyfile` dari folder ini ke
`/opt/vaksinku/` — perintah siap-tempel ada di pesan panduan, atau:

```bash
mkdir -p /opt/vaksinku/web /opt/vaksinku/situs
nano /opt/vaksinku/docker-compose.yml     # tempel isi docker-compose.yml
nano /opt/vaksinku/web/Caddyfile          # tempel isi web/Caddyfile
docker network create vaksinku-edge
```

### 2. Kirim berkas aplikasi (PowerShell di laptop, BUKAN di VPS)

```powershell
scp "$env:USERPROFILE\Downloads\VaksinKu-App.html" root@187.77.147.232:/opt/vaksinku/situs/index.html
scp "$env:USERPROFILE\Downloads\privasi.html"      root@187.77.147.232:/opt/vaksinku/situs/privasi.html
```

### 3. Jalankan & sambungkan (VPS)

```bash
cd /opt/vaksinku && docker compose up -d
docker network connect vaksinku-edge sih-deployment-caddy-1
docker exec sih-deployment-caddy-1 wget -qO- http://vaksinku-web/privasi.html | grep -o "<title>.*</title>"
```

Baris terakhir harus menampilkan `<title>Kebijakan Privasi · VaksinKu</title>`.

### 4. Tambah blok vaksinku.app ke Caddy sih — dengan cadangan & pembatalan otomatis (VPS)

```bash
cd /root/sih-production/sih-deployment
cp Caddyfile Caddyfile.cadangan-vaksinku
cat >> Caddyfile <<'BLOK'
<isi blok-caddy-sih.txt>
BLOK
if docker exec sih-deployment-caddy-1 caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile; then
  docker exec sih-deployment-caddy-1 caddy reload --config /etc/caddy/Caddyfile --adapter caddyfile && echo "BERHASIL"
else
  cat Caddyfile.cadangan-vaksinku > Caddyfile; echo "GAGAL - Caddyfile dikembalikan seperti semula"
fi
```

`cat >>` dan `cat … >` menulis ke berkas yang sama (tidak membuat berkas baru), sehingga
wadah Caddy langsung melihat perubahannya. Jangan memakai `sed -i` pada `Caddyfile`.

### 5. Periksa (VPS & browser)

```bash
curl -sI https://cms.sekolahibuhamil.id | head -1
curl -sI https://api.sekolahibuhamil.id | head -1
sleep 30; curl -sI https://vaksinku.app | head -1
```

Dua baris pertama harus sama seperti sebelum pemasangan. Baris ketiga `HTTP/2 200`
(sertifikat HTTPS dibuat otomatis; bila belum, tunggu 1–2 menit lalu ulangi).

## Tahap 2 — backend (database, API, masuk dengan Google)

Paket lengkap dirakit `src/buat_paket_vps.py` menjadi `dist/vaksinku-vps.tar.gz`
(berisi compose, Caddyfile, layanan masuk, SQL database, aplikasi, Kebijakan Privasi).
Rahasia (`.env`) dibuat di VPS oleh `pasang.sh` dan tidak pernah ada di paket/repositori.

```
web  (Caddy)  /         → aplikasi & privasi.html
              /auth/*   → auth  (Node, verifikasi token Google → sesi VaksinKu)
              /api/*    → api   (PostgREST → PostgreSQL VaksinKu, dibatasi peran + RLS)
db   (PostgreSQL 16)    data di /opt/vaksinku/data/db, hanya di jaringan internal
```

Langkah (buat snapshot di hPanel dulu):

```powershell
# laptop
scp "$env:USERPROFILE\Downloads\vaksinku-vps.tar.gz" root@187.77.147.232:/tmp/
```
```bash
# VPS
cd /opt && tar xzf /tmp/vaksinku-vps.tar.gz && cd /opt/vaksinku && ./pasang.sh
```

`pasang.sh` aman diulang: membuat `.env` hanya bila belum ada, tidak menyentuh data,
dan tidak mengubah apa pun milik sih-deployment selain memastikan Caddy-nya tersambung
ke jaringan `vaksinku-edge`. Hasil yang diharapkan di akhir:
`{"ok":true,"clientId":false}` dan daftar 3 klinik.

Setelah Client ID Google dibuat: `./atur-google.sh <ID>.apps.googleusercontent.com`,
lalu unggah ulang aplikasi yang dibangun dengan Client ID tersebut.

Cadangan harian database:

```bash
(crontab -l 2>/dev/null; echo "15 19 * * * /opt/vaksinku/cadangkan.sh") | crontab -
```

Uji di komputer pengembang: `node src/uji_backend.mjs` (PostgreSQL + PostgREST + layanan
masuk + Caddyfile, dengan server kunci Google tiruan) dan `python3 src/uji_supabase.py`
(aturan akses database).

## Membatalkan semuanya

```bash
cd /root/sih-production/sih-deployment
cat Caddyfile.cadangan-vaksinku > Caddyfile
docker exec sih-deployment-caddy-1 caddy reload --config /etc/caddy/Caddyfile --adapter caddyfile
docker network disconnect vaksinku-edge sih-deployment-caddy-1
cd /opt/vaksinku && docker compose down      # data database tetap tersimpan di data/db
```

## Memperbarui aplikasi

### Otomatis dari GitHub (disarankan)

`perbarui-situs.sh` mengambil repositori ke `/opt/vaksinku/sumber` setiap 15 menit dan
menyalin `VaksinKu-App.html` → `situs/index.html` serta `situs/privasi.html` bila berubah
(diperiksa ukuran & penandanya, diganti secara atomik). Tidak ada kode dari repositori
yang dijalankan; backend & database tetap diperbarui manual lewat `pasang.sh`.

```bash
apt-get install -y git        # bila belum ada
(crontab -l 2>/dev/null; echo "*/15 * * * * /opt/vaksinku/perbarui-situs.sh") | crontab -
/opt/vaksinku/perbarui-situs.sh && cat /opt/vaksinku/perbarui-situs.log
```

### Manual

Aplikasi saja (tanpa perubahan database), dari laptop:

```powershell
scp "$env:USERPROFILE\Downloads\VaksinKu-App.html" root@187.77.147.232:/opt/vaksinku/situs/index.html
```

Sinkronisasi: setelah masuk dengan Google, profil, anggota keluarga, dan riwayat dosis
dikirim ke `/api` (lihat `app/sinkron.js`); foto label vaksin tetap di perangkat. Catatan
dosis dari klinik hanya diterima, tidak bisa diubah dari aplikasi.

Reservasi online: bila pengguna masuk dengan Google dan server terjangkau, tombol *Kirim
Reservasi* memanggil `/api/rpc/buat_booking` — server memeriksa hari libur, jam layanan, dan
kuota per jam (kapasitas klinik), lalu membekukan harga dari `harga_klinik` dan memberi kode
`VK-YYMMDD-nnnn`. Status reservasi ikut diperbarui saat sinkron; pasien bisa membatalkan selama
status masih `baru`. Tanpa sesi/server, reservasi disimpan di perangkat dan dikirim lewat WhatsApp.

Cukup ulangi Langkah 2 dengan berkas baru; tidak perlu restart apa pun.

## Bila sih-deployment dibuat ulang

Jika tim sekolahibuhamil.id menjalankan ulang wadahnya (`docker compose up` dengan
perubahan, atau `down` lalu `up`), sambungan jaringan di Langkah 3 hilang dan vaksinku.app
menampilkan galat 502 — sekolahibuhamil.id tetap normal. Sambungkan lagi:

```bash
docker network connect vaksinku-edge sih-deployment-caddy-1
```

## Pindah ke VPS sendiri

Salin `/opt/vaksinku` ke VPS baru, jalankan Caddy sendiri di sana dengan blok yang sama,
ubah record A `vaksinku.app` ke IP baru, lalu jalankan bagian *Membatalkan semuanya* di
VPS lama.
