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

## Membatalkan semuanya

```bash
cd /root/sih-production/sih-deployment
cat Caddyfile.cadangan-vaksinku > Caddyfile
docker exec sih-deployment-caddy-1 caddy reload --config /etc/caddy/Caddyfile --adapter caddyfile
docker network disconnect vaksinku-edge sih-deployment-caddy-1
cd /opt/vaksinku && docker compose down
```

## Memperbarui aplikasi

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
