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
         "pelayanan", "persediaan", "transaksi", "pengaturan"]
TANDA_APP = "<script>/*APP-MULAI*/"

# data contoh dimuat lewat jalur aplikasi sendiri supaya layar yang dipotret
# benar-benar memakai angka hasil perhitungan, bukan HTML yang ditulis terpisah
SEED = """<script>
window.addEventListener('load', function () {
  window.confirm = function () { return true; };
  var b = document.querySelector('[data-act="contoh"]');
  if (b) b.click();
  location.hash = '#/%s';
  window.dispatchEvent(new HashChangeEvent('hashchange'));
});
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
