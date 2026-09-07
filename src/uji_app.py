#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uji fungsional aplikasi VaksinKu di browser headless.

Menyuntikkan skrip uji ke dalam bundel, menjalankan alur nyata (isi profil,
tambah pasien, buat reservasi, tandai selesai), lalu melaporkan hasilnya.

    python3 uji_app.py
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUNDLE = os.path.join(ROOT, "VaksinKu-App.html")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

TEST_JS = r"""
<script>
(function () {
  var hasil = [], galat = [];
  window.addEventListener('error', function (e) { galat.push(e.message); });

  function ok(nama, syarat, detail) {
    hasil.push((syarat ? 'LULUS' : 'GAGAL') + ' | ' + nama + (detail ? ' | ' + detail : ''));
  }
  function klik(sel, ke) {
    var els = document.querySelectorAll(sel);
    var el = ke == null ? els[0] : els[ke];
    if (!el) { hasil.push('GAGAL | elemen tidak ada: ' + sel); return false; }
    var hashSebelum = location.hash;
    el.click();
    if (location.hash !== hashSebelum) window.dispatchEvent(new HashChangeEvent('hashchange'));
    return true;
  }
  function isi(sel, nilai) {
    var el = document.querySelector(sel);
    if (!el) { hasil.push('GAGAL | input tidak ada: ' + sel); return false; }
    el.value = nilai;
    el.dispatchEvent(new Event('input', { bubbles: true }));
    return true;
  }
  function st() { try { return JSON.parse(localStorage.getItem('vaksinku.v1')) || {}; } catch (e) { return {}; } }
  function ganti(h) { location.hash = h; window.dispatchEvent(new HashChangeEvent('hashchange')); }

  var K2 = window.KATALOG;
  try {
    /* 1. boot */
    ok('katalog termuat', !!(window.KATALOG && window.KATALOG.harga.length), (window.KATALOG || {}).harga.length + ' baris harga');
    ok('beranda tampil', !!document.querySelector('.device') && document.body.textContent.indexOf('Halo') >= 0);
    ok('bottom nav tampil', document.querySelectorAll('.navitem').length === 4);

    /* 2. profil */
    ganti('#/profil');
    isi('[data-field="profil.nama"]', 'Ibu Sari');
    isi('[data-field="profil.hp"]', '081234567890');
    ok('profil tersimpan', st().profil && st().profil.nama === 'Ibu Sari', JSON.stringify(st().profil));

    /* 3. tambah pasien */
    ganti('#/pasien-form');
    var f = document.getElementById('form-pasien');
    f.elements.nama.value = 'Nadia';
    f.elements.tglLahir.value = (new Date().getFullYear() - 5) + '-05-12';
    f.elements.hubungan.value = 'Anak';
    f.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    ok('pasien tersimpan', st().pasien.length === 1, JSON.stringify(st().pasien[0] || {}));

    /* 3b. validasi form ditolak saat kosong */
    ganti('#/pasien-form');
    document.getElementById('form-pasien').dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    ok('form kosong ditolak', st().pasien.length === 1 && document.querySelectorAll('.errmsg').length >= 2,
       document.querySelectorAll('.errmsg').length + ' pesan galat');

    /* 4. booking: validasi dulu */
    ganti('#/booking');
    klik('[data-act="kirim-booking"]');
    ok('booking kosong ditolak', st().booking.length === 0 && document.querySelectorAll('.errmsg').length > 0,
       document.querySelectorAll('.errmsg').length + ' pesan galat');

    /* 5. booking: isi lengkap */
    klik('[data-act="set-layanan"][data-arg="klinik"]');
    ok('klinik tampil', document.querySelectorAll('[data-act="set-klinik"]').length === window.KATALOG.klinik.length);
    klik('[data-act="set-klinik"]', 0);
    klik('[data-act="toggle-pasien"]');
    klik('[data-act="buka-vaksin"]');
    ok('daftar vaksin terbuka', !!document.querySelector('.sheet'));
    isi('#cari-vaksin', 'influenza');
    var kartu = document.querySelectorAll('[data-act="toggle-vaksin"]');
    ok('pencarian vaksin bekerja', kartu.length > 0 && kartu.length < window.KATALOG.harga.length,
       kartu.length + ' hasil untuk "influenza"');
    klik('[data-act="toggle-vaksin"]', 0);
    klik('[data-act="tutup-sheet"]');
    var besok = new Date(Date.now() + 864e5).toISOString().slice(0, 10);
    isi('[data-field="tanggal"]', besok);
    klik('[data-act="set-jam"][data-arg="10:00"]');

    var totalTeks = document.body.textContent.match(/Total estimasi[\s\S]{0,40}?(Rp[\d.]+)/);
    ok('estimasi biaya terhitung', !!totalTeks && totalTeks[1] !== 'Rp0', totalTeks ? totalTeks[1] : '-');

    /* harga berubah saat dokter spesialis dipilih */
    var sebelum = st().draft ? JSON.stringify(st().draft.dokter) : '';
    klik('[data-act="set-dokter"][data-arg="spesialis"]');
    var totalSpes = document.body.textContent.match(/Total estimasi[\s\S]{0,40}?(Rp[\d.]+)/);
    ok('tarif spesialis mengubah total', totalSpes && totalTeks && totalSpes[1] !== totalTeks[1],
       totalTeks[1] + ' → ' + (totalSpes ? totalSpes[1] : '-'));
    klik('[data-act="set-dokter"][data-arg="umum"]');

    klik('[data-act="kirim-booking"]');
    var b = st().booking[0];
    ok('reservasi tersimpan', !!b && b.status === 'menunggu', b ? b.kode + ' · ' + b.total : '-');
    ok('pindah ke detail reservasi', location.hash.indexOf('booking-detail') > 0, location.hash);
    ok('draft dibersihkan', st().draft == null);

    /* 6. tandai selesai */
    window.confirm = function () { return true; };
    klik('[data-act="selesai-booking"]');
    var s6 = st();
    ok('status jadi selesai', s6.booking[0].status === 'selesai');
    ok('riwayat vaksin tercatat', s6.riwayat.length > 0, s6.riwayat.length + ' catatan');
    ok('poin bertambah', s6.poin === 10, s6.poin + ' poin');

    /* 7. jadwal & ceklis */
    ganti('#/jadwal');
    var ceklis = document.querySelectorAll('[data-act="toggle-riwayat"]');
    ok('ceklis jadwal tampil', ceklis.length > 10, ceklis.length + ' item');
    var bar = function () { var i = document.querySelector('.bar > i'); return i ? i.style.width : '-'; };
    var persenSebelum = bar();
    ceklis[0].click();
    var persenSesudah = bar();
    ok('ceklis mengubah kelengkapan', persenSebelum !== persenSesudah, persenSebelum + '% → ' + persenSesudah + '%');

    /* 8. rekam medis + pertumbuhan */
    ganti('#/rekam');
    ok('rekam medis tampil', document.body.textContent.indexOf('Riwayat vaksinasi') > 0);
    ganti('#/tumbuh-form/' + st().pasien[0].id);
    var ft = document.getElementById('form-tumbuh');
    ft.elements.berat.value = '17.5';
    ft.elements.tinggi.value = '108';
    ft.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    ok('pengukuran tersimpan', st().pertumbuhan.length === 1, JSON.stringify(st().pertumbuhan[0] || {}));

    /* 9. daftar harga */
    ganti('#/harga');
    var barisAwal = document.querySelectorAll('table.price tr').length;
    isi('#cari-harga', 'hepatitis');
    var barisCari = document.querySelectorAll('table.price tr').length;
    ok('pencarian harga bekerja', barisCari > 0 && barisCari < barisAwal, barisAwal + ' → ' + barisCari + ' baris');
    klik('[data-act="set-tarif"][data-arg="spesialis"]');
    ok('tarif spesialis tampil', document.body.textContent.indexOf('Rp550.000') > 0 || document.body.textContent.indexOf('Rp375.000') > 0);

    /* 9b. konsultasi dokter */
    window.open = function (u) { window.__waTerakhir = u; return null; };
    ganti('#/chat');
    ok('layar konsultasi tampil', document.body.textContent.indexOf('Cara kerja konsultasi') > 0);
    ok('nav konsultasi ada', document.body.textContent.indexOf('Konsultasi') > 0);

    klik('[data-act="go"][data-arg="chat-baru"]');
    klik('[data-act="kirim-konsul"]');
    ok('konsultasi kosong ditolak', (st().konsultasi || []).length === 0 && document.querySelectorAll('.errmsg').length > 0,
       document.querySelectorAll('.errmsg').length + ' pesan galat');

    var sel = document.querySelector('[data-fieldk="pasienId"]');
    sel.value = st().pasien[0].id;
    sel.dispatchEvent(new Event('input', { bubbles: true }));
    klik('[data-act="set-topik"][data-arg="1"]');
    var ta = document.querySelector('[data-fieldk="pertanyaan"]');
    ta.value = 'Anak saya demam 38 derajat sejak semalam setelah vaksin. Apakah perlu dibawa ke klinik?';
    ta.dispatchEvent(new Event('input', { bubbles: true }));
    var pv = document.querySelector('.pratinjau').textContent;
    ok('pratinjau memuat pertanyaan', pv.indexOf('demam 38 derajat') > 0);
    ok('pratinjau melampirkan data pasien', pv.indexOf('Kelengkapan vaksin sesuai usia') > 0,
       'konteks ' + (pv.indexOf('Usia:') > 0 ? 'ada' : 'tidak ada'));

    klik('[data-act="kirim-konsul"]');
    var kk = (st().konsultasi || [])[0];
    ok('konsultasi tersimpan', !!kk && kk.status === 'terkirim', kk ? kk.kode + ' · ' + kk.topik : '-');
    ok('pesan pertama tercatat', !!kk && kk.pesan.length === 1 && kk.pesan[0].dari === 'saya');
    ok('WhatsApp dibuka dengan isi pesan', (window.__waTerakhir || '').indexOf('wa.me') > 0 &&
       decodeURIComponent(window.__waTerakhir).indexOf('demam 38 derajat') > 0,
       (window.__waTerakhir || '').slice(0, 30) + '...');
    ok('draft konsultasi dibersihkan', st().draftKonsul == null);

    /* catat jawaban dokter */
    var fj = document.getElementById('form-jawaban');
    fj.elements.jawaban.value = 'Demam ringan pasca vaksin wajar. Kompres hangat, cukupi cairan. Bila di atas 39 derajat atau kejang, segera ke klinik.';
    fj.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    var kk2 = st().konsultasi[0];
    ok('jawaban dokter tercatat', kk2.pesan.length === 2 && kk2.pesan[1].dari === 'dokter');
    ok('status jadi dijawab', kk2.status === 'dijawab', kk2.status);
    ok('gelembung percakapan tampil', document.querySelectorAll('.bubble').length === 2,
       document.querySelectorAll('.bubble').length + ' gelembung');

    klik('[data-act="selesai-konsul"]');
    ok('konsultasi bisa diselesaikan', st().konsultasi[0].status === 'selesai');

    /* 9c. pengingat & notifikasi */
    ganti('#/notifikasi');
    var kartu2 = document.querySelectorAll('.notif');
    ok('layar pengingat tampil', document.body.textContent.indexOf('Pengingat di kalender ponsel') > 0);
    ok('pengingat terbentuk dari data', kartu2.length > 0, kartu2.length + ' pengingat');

    var teksNotif = document.querySelector('.notif').textContent;
    ok('pengingat menyebut vaksin terlambat', document.body.textContent.indexOf('terlambat') > 0,
       teksNotif.slice(0, 60).replace(/\s+/g, ' '));

    var baruAwal = document.querySelectorAll('.notif.baru').length;
    klik('[data-act="baca-semua"]');
    ok('tandai dibaca bekerja', document.querySelectorAll('.notif.baru').length === 0 && baruAwal > 0,
       baruAwal + ' baru → 0');
    ok('status baca tersimpan', Object.keys((st().notif || {}).dibaca || {}).length > 0);

    klik('[data-act="toggle-set"][data-arg="vaksin"]');
    ok('pengingat vaksin bisa dimatikan', st().pengaturan.vaksin === false &&
       document.querySelectorAll('.notif').length < kartu2.length,
       kartu2.length + ' → ' + document.querySelectorAll('.notif').length + ' pengingat');
    klik('[data-act="toggle-set"][data-arg="vaksin"]');
    klik('[data-act="set-lead"][data-arg="3"]');
    ok('jarak pengingat reservasi tersimpan', st().pengaturan.leadBooking === 3, 'H-' + st().pengaturan.leadBooking);

    /* ekspor kalender: cek isi berkas .ics yang dihasilkan */
    var icsTeks = null;
    var blobAsli = window.Blob;
    window.Blob = function (bagian, opsi) { icsTeks = String(bagian[0]); return new blobAsli(bagian, opsi); };
    window.URL.createObjectURL = function () { return 'blob:uji'; };
    window.URL.revokeObjectURL = function () {};
    klik('[data-act="unduh-ics"]');
    window.Blob = blobAsli;
    ok('berkas kalender dibuat', !!icsTeks && icsTeks.indexOf('BEGIN:VCALENDAR') === 0,
       icsTeks ? icsTeks.length + ' karakter' : 'kosong');
    ok('kalender memuat alarm pengingat', !!icsTeks && icsTeks.indexOf('BEGIN:VALARM') > 0 &&
       icsTeks.indexOf('TRIGGER:-P7D') > 0);
    ok('kalender memuat jadwal vaksin bertanggal', !!icsTeks && /DTSTART;VALUE=DATE:\d{8}/.test(icsTeks),
       (icsTeks.match(/BEGIN:VEVENT/g) || []).length + ' acara');
    ok('kalender ditutup dengan benar', !!icsTeks && /END:VCALENDAR$/.test(icsTeks.trim()));

    /* 10. layar informasi */
    [['#/internasional', 'Meningitis'], ['#/tentang', K2.klinik[0][0]], ['#/jadwal-info/pranikah', 'HPV'],
     ['#/jadwal-info/lansia', 'Pneumonia'], ['#/riwayat-booking', 'VK-'], ['#/alamat', 'alamat']].forEach(function (r) {
      ganti(r[0]);
      var teks = document.querySelector('.device').textContent;
      ok('layar ' + r[0] + ' tampil', teks.indexOf(r[1]) >= 0, teks.length + ' karakter');
    });

    /* 11. alamat */
    ganti('#/alamat-form');
    var fa = document.getElementById('form-alamat');
    fa.elements.label.value = 'Rumah';
    fa.elements.kecamatan.value = 'Tanjungpinang Kota';
    fa.elements.alamat.value = 'Jl. Contoh No. 1';
    fa.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    ok('alamat tersimpan', st().alamat.length === 1);

    /* 12. persistensi */
    ok('data bertahan di localStorage', !!localStorage.getItem('vaksinku.v1'),
       Math.round((localStorage.getItem('vaksinku.v1') || '').length / 1024) + ' KB');
  } catch (e) {
    hasil.push('GAGAL | pengecualian: ' + e.message + ' @ ' + (e.stack || '').split('\n')[1]);
  }

  if (galat.length) hasil.push('GAGAL | galat konsol: ' + galat.join(' ; '));
  var out = document.createElement('pre');
  out.id = 'hasil-uji';
  out.textContent = hasil.join('\n');
  document.body.appendChild(out);
})();
</script>
"""


def main():
    with open(BUNDLE, encoding="utf-8") as f:
        html = f.read()
    html = html.replace("</body>", TEST_JS + "\n</body>")
    tmp = os.path.join(tempfile.gettempdir(), "_uji_vaksinku.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html)

    out = subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
         "--allow-file-access-from-files", "--virtual-time-budget=6000",
         "--dump-dom", "file://" + tmp],
        capture_output=True, timeout=180).stdout.decode("utf-8", "replace")

    m = re.search(r'<pre id="hasil-uji">([\s\S]*?)</pre>', out)
    if not m:
        print("Skrip uji tidak menghasilkan keluaran. Cuplikan DOM:")
        print(out[:1500])
        return 1
    baris = [b.strip() for b in m.group(1).strip().split("\n") if b.strip()]
    gagal = [b for b in baris if b.startswith("GAGAL")]
    for b in baris:
        tanda = "  ok " if b.startswith("LULUS") else "  XX "
        print(tanda + b.split("|", 1)[1].strip())
    print("\n%d uji, %d lulus, %d gagal" % (len(baris), len(baris) - len(gagal), len(gagal)))
    return 1 if gagal else 0


if __name__ == "__main__":
    sys.exit(main())
