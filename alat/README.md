# Folder VaksinKu yang selalu terbaru di laptop

`perbarui-vaksinku.ps1` menyalin repositori ke `Unduhan\VaksinKu` dan, lewat Task
Scheduler, mengambil versi terbaru setiap 30 menit. Berkas yang biasa dipakai:

| Berkas | Isi |
|---|---|
| `VaksinKu-App.html` | Aplikasi pasien |
| `VaksinKu-Dashboard.html` | Dashboard klinik |
| `situs\privasi.html` | Kebijakan Privasi |

Catatan pembaruan ada di `Unduhan\VaksinKu-pembaruan.log`.

## Pemasangan (sekali)

1. Pasang Git: `winget install --id Git.Git -e` (lalu tutup dan buka lagi PowerShell).
2. Ambil pertama kali — jendela login GitHub akan muncul sekali bila repositori privat:
   ```powershell
   git clone --depth 1 --branch claude/vaksinku-app-continue-3dxaoq https://github.com/dranggapk/VaksinKu-by-Alrasha-HCG.git "$env:USERPROFILE\Downloads\VaksinKu"
   ```
3. Jadwalkan setiap 30 menit:
   ```powershell
   schtasks /create /f /tn "Perbarui VaksinKu" /sc minute /mo 30 /tr "powershell -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File \"$env:USERPROFILE\Downloads\VaksinKu\alat\perbarui-vaksinku.ps1\""
   ```

Perbarui sekarang juga: `schtasks /run /tn "Perbarui VaksinKu"`.
Hentikan: `schtasks /delete /tn "Perbarui VaksinKu" /f`.

Setelah pull request digabung ke cabang utama, ganti nama cabang di skrip (`$Cabang`)
menjadi `main`.
