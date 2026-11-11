#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uji varian JasVacc (JasVacc-App.html, src/merek.py) di browser headless.

Fitur dan logika sama dengan VaksinKu (diuji lengkap oleh uji_app.py); di sini
diperiksa yang khas varian: nama & logo merek, font & warna, klinik bawaan
Jasmine MQ Medika, banner Jasmine, data perangkat terpisah, dan semua layar
utama terbuka tanpa galat JavaScript.

    python3 uji_jasvacc.py
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUNDLE = os.path.join(ROOT, "JasVacc-App.html")
CHROME = "/opt/pw-browsers/chromium"

TEST_JS = r"""
<script>
(function () {
  var hasil = [], galat = [];
  window.addEventListener('error', function (e) { galat.push(e.message); });
  function ok(n, c, d) { hasil.push((c ? 'LULUS' : 'GAGAL') + ' | ' + n + (d ? ' | ' + d : '')); }
  function ganti(hh) { location.hash = hh; window.dispatchEvent(new HashChangeEvent('hashchange')); }
  function teks() { return document.getElementById('app').textContent; }
  var K = window.KATALOG;
  try {
    ok('nama merek di katalog', K.merek && K.merek.nama === 'JasVacc');
    ok('layar pertama: cover JasVacc', !!document.querySelector('.splash') && /^data:image\/png/.test(document.querySelector('.splash-logo').src));
    ok('judul halaman JasVacc', document.title.indexOf('JasVacc') === 0, document.title);
    var gaya = getComputedStyle(document.documentElement);
    ok('warna merek: navy & merah Jasmine', gaya.getPropertyValue('--teal-dark').trim().toUpperCase() === '#0F2533' &&
       gaya.getPropertyValue('--magenta').trim().toUpperCase() === '#EC1D25');
    ok('font merek: Fredoka & Poppins', /Fredoka/.test(gaya.getPropertyValue('--disp')) && /Poppins/.test(gaya.getPropertyValue('--body')));
    ok('tidak ada nama VaksinKu di teks aplikasi', !/VaksinKu(?![A-Za-z])/.test(document.body.innerHTML.replace(/<script[\s\S]*?<\/script>/g, '')));
    window.VaksinKuUji.aturState(function () {});   // simpan state awal ke perangkat
    var st = JSON.parse(localStorage.getItem('jasvacc.v1') || '{}');
    ok('data perangkat terpisah (jasvacc.v1) & klinik bawaan Jasmine MQ', !localStorage.getItem('vaksinku.v1') &&
       st.lokasi && st.lokasi.klinik === 'jasmine-mq', JSON.stringify(st.lokasi || {}));
    // pengguna yang sudah selesai perkenalan
    st.onboarding = { selesai: true, langkah: 2, fokus: ['anak'], layanan: 'klinik' };
    st.profil = { nama: 'Rina', hp: '081200000000' };
    st.pasien = [{ id: 'p1', nama: 'Nadia', tglLahir: '2022-05-12', jenisKelamin: 'Perempuan', hubungan: 'Anak' }];
    localStorage.setItem('jasvacc.v1', JSON.stringify(st));
  } catch (e) { hasil.push('GAGAL | pengecualian: ' + e.message); }
  var tulis = function () {
    if (galat.length) hasil.push('GAGAL | galat konsol: ' + galat.join(' ; '));
    var o = document.createElement('pre'); o.id = 'hasil-uji'; o.textContent = hasil.join('\n'); document.body.appendChild(o);
  };
  // muat ulang state lewat aplikasi: pindah layar satu per satu
  setTimeout(function () {
    try {
      window.VaksinKuUji.aturState(function (S) {
        var b = JSON.parse(localStorage.getItem('jasvacc.v1'));
        S.onboarding = b.onboarding; S.profil = b.profil; S.pasien = b.pasien;
      });
      ganti('#/beranda');
      ok('beranda: logo JasVacc & banner promo influenza Jasmine', /^data:image\/png/.test((document.querySelector('.hero img') || {}).src || '') &&
         document.querySelectorAll('#promo-rel .promo-kartu').length === 1 &&
         /influenza/i.test(document.querySelector('#promo-rel .promo-kartu').getAttribute('aria-label') || ''));
      ok('beranda: klinik Jasmine MQ Medika terpilih', teks().indexOf('Jasmine MQ Medika') >= 0);
      ['booking', 'jadwal', 'rekam', 'profil', 'harga', 'panduan', 'internasional', 'tentang', 'chat', 'notifikasi', 'riwayat-booking', 'pasien']
        .forEach(function (r) {
          ganti('#/' + r);
          ok('layar ' + r + ' terbuka', teks().length > 50 && !/VaksinKu(?![A-Za-z])/.test(teks()));
        });
      ganti('#/tentang');
      ok('tentang: nama grup Jasmine MQ Medika', teks().indexOf('Jasmine MQ Medika') >= 0);
    } catch (e) { hasil.push('GAGAL | pengecualian: ' + e.message + ' @ ' + (e.stack || '').split('\n')[1]); }
    tulis();
  }, 300);
})();
</script>
"""


def main():
    with open(BUNDLE, encoding="utf-8") as f:
        html = f.read().replace("</body>", TEST_JS + "\n</body>")
    tmp = os.path.join(tempfile.mkdtemp(), "uji_jasvacc.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html)
    out = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                          "--allow-file-access-from-files", "--virtual-time-budget=4000", "--dump-dom", "file://" + tmp],
                         capture_output=True, timeout=180).stdout.decode("utf-8", "replace")
    m = re.search(r'<pre id="hasil-uji">([\s\S]*?)</pre>', out)
    if not m:
        print("Skrip uji tidak menghasilkan keluaran.")
        return 1
    baris = [b.strip() for b in m.group(1).strip().split("\n") if b.strip()]
    gagal = [b for b in baris if b.startswith("GAGAL")]
    for b in baris:
        print(("  ok " if b.startswith("LULUS") else "  XX ") + b.split("|", 1)[1].strip())
    print("\n%d uji, %d lulus, %d gagal" % (len(baris), len(baris) - len(gagal), len(gagal)))
    return 1 if gagal else 0


if __name__ == "__main__":
    sys.exit(main())
