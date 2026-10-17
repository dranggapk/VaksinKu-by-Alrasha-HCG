# Memperbarui folder Unduhan\VaksinKu dengan versi terbaru dari GitHub.
# Dijalankan otomatis oleh Task Scheduler (lihat alat\README.md), atau manual:
#   powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\Downloads\VaksinKu\alat\perbarui-vaksinku.ps1"
#
# Folder ini salinan hanya-baca: perubahan yang Anda buat di dalamnya akan ditimpa.
param(
  [string]$Cabang = "claude/vaksinku-app-continue-3dxaoq",
  [string]$Folder = "$env:USERPROFILE\Downloads\VaksinKu"
)
$ErrorActionPreference = "Stop"
$Repo = "https://github.com/dranggapk/VaksinKu-by-Alrasha-HCG.git"
$Log = "$env:USERPROFILE\Downloads\VaksinKu-pembaruan.log"

try {
  if (-not (Test-Path "$Folder\.git")) {
    git clone --quiet --depth 1 --branch $Cabang $Repo $Folder
  } else {
    git -C $Folder fetch --quiet --depth 1 origin $Cabang
    git -C $Folder reset --quiet --hard FETCH_HEAD
    git -C $Folder clean --quiet -fd
  }
  $versi = git -C $Folder log -1 --format="%h %cd %s" --date=format:"%d-%m-%Y %H:%M"
  "$(Get-Date -Format 'dd-MM-yyyy HH:mm')  OK  $versi" | Add-Content $Log
} catch {
  "$(Get-Date -Format 'dd-MM-yyyy HH:mm')  GAGAL  $($_.Exception.Message)" | Add-Content $Log
  exit 1
}
