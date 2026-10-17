#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tangkap layar dashboard manajemen dengan data contoh, untuk pemeriksaan visual.

    python3 tangkap_dashboard.py [nama-layar ...]
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUNDLE = os.path.join(ROOT, "VaksinKu-Dashboard.html")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
KELUAR = os.path.join(tempfile.gettempdir(), "vaksinku-dashboard")

LAYAR = ["ringkasan", "booking", "pendaftaran", "penjadwalan",
         "pelayanan", "persediaan", "transaksi", "pengaturan", "tempel-wa"]
TANDA_APP = "<script>/*APP-MULAI*/"

# data contoh dimuat lewat jalur aplikasi sendiri supaya layar yang dipotret
# benar-benar memakai angka hasil perhitungan, bukan HTML yang ditulis terpisah
SEED = r"""<script>
window.addEventListener('load', function () {
  window.confirm = function () { return true; };
  var b = document.querySelector('[data-act="contoh"]');
  if (b) b.click();
  var layar = '%s';
  location.hash = '#/' + (layar === 'tempel-wa' ? 'booking' : layar);
  window.dispatchEvent(new HashChangeEvent('hashchange'));
  if (layar === 'tempel-wa') setTimeout(tempelContoh, 300);
});
// panel "Tempel dari WhatsApp" berisi pesan seperti yang dikirim aplikasi pasien
function tempelContoh() {
  var K = window.KATALOG, d = new Date(Date.now() + 3 * 864e5);
  if (d.getDay() === 0) d = new Date(d.getTime() + 864e5);
  var iso = function (x) { return new Date(x.getTime() - x.getTimezoneOffset() * 6e4).toISOString().slice(0, 10); };
  var v = K.harga.filter(function (x) { return /^(Influenza|MMR)/.test(x.kategori) && x.umum; }).slice(0, 2);
  var data = { k: 'VK-482913', n: 'Rina Ramadhani', h: '081299998888', l: 'klinik', lo: K.klinik[0][0],
    t: iso(d), j: '10:00', d: 'umum', c: '', v: v.map(function (x) { return x.id; }),
    p: [['Nadia Putri', '2021-05-12', 'Perempuan'], ['Zahra Ramadhani', '2024-02-03', 'Perempuan']] };
  var kode = 'VKD1.' + btoa(unescape(encodeURIComponent(JSON.stringify(data))))
    .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  document.querySelector('[data-act="form-tempel-wa"]').click();
  var ta = document.getElementById('teks-wa');
  ta.value = 'Halo VaksinKu, saya ingin reservasi vaksinasi.\n\nKode: VK-482913\n...\n\n' +
    'Kode data untuk petugas klinik (mohon tidak diubah):\n' + kode;
  ta.dispatchEvent(new Event('input', { bubbles: true }));
}
</script>
"""


def main():
    pilih = sys.argv[1:] or LAYAR
    os.makedirs(KELUAR, exist_ok=True)
    with open(BUNDLE, encoding="utf-8") as f:
        html = f.read()
    for nama in pilih:
        if nama not in LAYAR:
            print("layar tidak dikenal:", nama)
            continue
        doc = html.replace("</body>", (SEED % nama) + "</body>")
        tmp = os.path.join(tempfile.gettempdir(), "_dash_%s.html" % nama)
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(doc)
        png = os.path.join(KELUAR, nama + ".png")
        if os.path.exists(png):
            os.remove(png)
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--allow-file-access-from-files",
             "--hide-scrollbars", "--window-size=1440,980", "--virtual-time-budget=5000",
             "--screenshot=" + png, "file://" + tmp],
            capture_output=True, timeout=90)
        print(("  ok " if os.path.exists(png) else "  XX ") + png)
    return 0


if __name__ == "__main__":
    sys.exit(main())
