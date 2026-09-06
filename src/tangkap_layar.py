#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tangkap layar aplikasi VaksinKu dengan data contoh, untuk pemeriksaan visual.

    python3 tangkap_layar.py [nama-layar ...]
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUNDLE = os.path.join(ROOT, "VaksinKu-App.html")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
KELUAR = os.path.join(tempfile.gettempdir(), "vaksinku-layar")

LAYAR = {
    "beranda": "#/beranda", "booking": "#/booking", "jadwal": "#/jadwal",
    "rekam": "#/rekam", "harga": "#/harga", "profil": "#/profil",
    "tentang": "#/tentang", "internasional": "#/internasional",
}

SEED = """
<script>
(function () {
  var tujuan = '__TARGET__';
  if (sessionStorage.getItem('siap')) {
    location.hash = tujuan;
    window.dispatchEvent(new HashChangeEvent('hashchange'));
    return;
  }
  sessionStorage.setItem('siap', '1');
  window.confirm = function () { return true; };
  location.hash = '#/profil';
  window.dispatchEvent(new HashChangeEvent('hashchange'));
  var b = document.querySelector('[data-act="contoh"]');
  if (b) b.click();
  var d = JSON.parse(localStorage.getItem('vaksinku.v1'));
  var besok = new Date(Date.now() + 2 * 864e5).toISOString().slice(0, 10);
  d.draft = {
    layanan: 'homecare', klinikIdx: 0, alamatId: d.alamat[0].id, institusi: '', institusiAlamat: '',
    pasienIds: [d.pasien[0].id], vaksinIds: ['v7-11', 'v6-10'], dokter: 'umum',
    tanggal: besok, jam: '10:00', catatan: ''
  };
  d.booking = [{
    id: 'b1', kode: 'VK-880231', dibuat: new Date().toISOString(), status: 'menunggu',
    layanan: 'homecare', lokasi: 'Rumah — Jl. Contoh No. 10, Tanjungpinang Kota',
    pasienIds: [d.pasien[0].id], vaksinIds: ['v7-11'], dokter: 'umum',
    tanggal: besok, jam: '10:00', catatan: '',
    rincian: [{ nama: 'Influenza — Vaxigrip Tetra', harga: 400000 }], tanpaHarga: [],
    perPasien: 400000, total: 400000, pendaftar: { nama: 'Contoh Pengguna', hp: '0812xxxxxxx' }
  }];
  localStorage.setItem('vaksinku.v1', JSON.stringify(d));
  location.href = location.pathname + tujuan;
})();
</script>
"""


def main():
    pilih = sys.argv[1:] or list(LAYAR)
    os.makedirs(KELUAR, exist_ok=True)
    with open(BUNDLE, encoding="utf-8") as f:
        html = f.read()
    for nama in pilih:
        if nama not in LAYAR:
            print("layar tidak dikenal:", nama)
            continue
        doc = html.replace("</body>", SEED.replace("__TARGET__", LAYAR[nama]) + "\n</body>")
        tmp = os.path.join(tempfile.gettempdir(), "_layar_%s.html" % nama)
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(doc)
        png = os.path.join(KELUAR, nama + ".png")
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--allow-file-access-from-files",
             "--hide-scrollbars", "--window-size=470,930", "--virtual-time-budget=4000",
             "--screenshot=" + png, "file://" + tmp],
            capture_output=True, timeout=90)
        print(("  ok " if os.path.exists(png) else "  XX ") + png)


if __name__ == "__main__":
    main()
