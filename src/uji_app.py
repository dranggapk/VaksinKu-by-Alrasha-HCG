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
  function kirim(idForm) {
    var el = typeof idForm === 'string' ? document.getElementById(idForm) : idForm;
    if (!el) { hasil.push('GAGAL | form tidak ada: ' + idForm); return false; }
    var hashSebelum = location.hash;
    el.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    if (location.hash !== hashSebelum) window.dispatchEvent(new HashChangeEvent('hashchange'));
    return true;
  }
  function st() { try { return JSON.parse(localStorage.getItem('vaksinku.v1')) || {}; } catch (e) { return {}; } }
  function ganti(h) { location.hash = h; window.dispatchEvent(new HashChangeEvent('hashchange')); }

  var K2 = window.KATALOG;
  try {
    /* 1. boot */
    ok('katalog termuat', !!(window.KATALOG && window.KATALOG.harga.length), (window.KATALOG || {}).harga.length + ' baris harga');

    /* 1b. pemakaian pertama: splash → onboarding → masuk */
    ok('splash tampil saat pertama dibuka', !!document.querySelector('.splash') && location.hash === '#/splash', location.hash);
    klik('.splash');
    ok('splash lanjut ke onboarding', location.hash === '#/onboarding' && !!document.querySelector('.onb'), location.hash);
    ok('onboarding mulai dari langkah 1', document.body.textContent.indexOf('Satu aplikasi untuk vaksinasi keluarga') > 0);
    klik('[data-act="onb-lanjut"]');
    ok('langkah 2 menampilkan pilihan kebutuhan', document.querySelectorAll('[data-act="toggle-fokus"]').length === 4,
       document.querySelectorAll('[data-act="toggle-fokus"]').length + ' pilihan');
    klik('[data-act="onb-lanjut"]');
    ok('lanjut ditolak sebelum memilih kebutuhan', (st().onboarding || {}).langkah === 1, 'langkah ' + (st().onboarding || {}).langkah);
    klik('[data-act="toggle-fokus"][data-arg="anak"]');
    ok('pilihan kebutuhan tersimpan', (st().onboarding.fokus || [])[0] === 'anak', JSON.stringify(st().onboarding.fokus));
    ok('jumlah vaksin yang cocok dihitung', /\d+ jenis vaksin cocok/.test(document.body.textContent),
       (document.body.textContent.match(/(\d+) jenis vaksin cocok/) || [])[1] + ' vaksin');
    klik('[data-act="onb-lanjut"]');
    ok('langkah 3 menampilkan cara layanan', document.querySelectorAll('[data-act="set-fokus-layanan"]').length === 3);
    klik('[data-act="set-fokus-layanan"][data-arg="klinik"]');
    klik('[data-act="onb-lanjut"]');
    ok('onboarding selesai menuju layar masuk', location.hash === '#/masuk' && !!document.getElementById('form-masuk'), location.hash);

    /* 1c. masuk sebagai akun lokal */
    var fm = document.getElementById('form-masuk');
    fm.elements.nama.value = '';
    fm.elements.hp.value = '12';
    kirim(fm);
    ok('masuk menolak data tidak lengkap', !st().onboarding.selesai && document.querySelectorAll('.errmsg').length === 2,
       document.querySelectorAll('.errmsg').length + ' pesan galat');
    ok('tombol Google dinonaktifkan apa adanya', !!document.querySelector('button[disabled]') &&
       document.body.textContent.indexOf('Masuk dengan Google belum tersedia') > 0);
    fm = document.getElementById('form-masuk');
    fm.elements.nama.value = 'Ibu Sari';
    fm.elements.hp.value = '081234567890';
    kirim(fm);
    ok('profil terisi dari layar masuk', st().profil && st().profil.nama === 'Ibu Sari', JSON.stringify(st().profil));
    ok('masuk mengantar ke beranda', location.hash === '#/beranda', location.hash);
    ok('layanan pilihan onboarding jadi bawaan booking', (st().draft || {}).layanan === 'klinik', (st().draft || {}).layanan);

    /* 1d. beranda */
    ok('beranda tampil', !!document.querySelector('.device') && document.body.textContent.indexOf('Halo') >= 0);
    ok('bottom nav tampil', document.querySelectorAll('.navitem').length === 4);
    ok('rekomendasi sesuai kebutuhan tampil', document.body.textContent.indexOf('Sesuai kebutuhan Anda') > 0);

    /* 1e. banner promo di bawah tombol booking (daftar BANNER di app.js) */
    var pita = document.getElementById('promo-rel');
    var slide = document.querySelectorAll('.promo-kartu');
    ok('banner promo tampil di beranda', !!pita && slide.length > 1, slide.length + ' banner');
    ok('titik indikator sejumlah banner', document.querySelectorAll('#promo-titik i').length === slide.length);
    var sebelumBanner = document.querySelector('.promo').previousElementSibling;
    ok('banner tepat di bawah kartu tombol Booking Vaksinasi',
       !!sebelumBanner && sebelumBanner.textContent.indexOf('Booking Vaksinasi') > 0,
       sebelumBanner ? sebelumBanner.textContent.trim().slice(0, 34).replace(/\s+/g, ' ') : '-');
    ok('tiap banner punya judul atau teks alternatif, dan tujuan',
       [].every.call(slide, function (b) {
         var judul = b.querySelector('.promo-judul');
         return ((judul && judul.textContent.length > 3) || (b.getAttribute('aria-label') || '').length > 10) &&
           !!b.getAttribute('data-act');
       }));
    var gbr = document.querySelectorAll('.promo-kartu img');
    ok('gambar banner tertanam di berkas (jalan tanpa internet)', gbr.length > 0 &&
       [].every.call(gbr, function (g) { return g.getAttribute('src').indexOf('data:image/') === 0; }),
       gbr.length + ' gambar');
    ok('banner bergambar tanpa teks tidak digelapkan',
       [].every.call(slide, function (b) {
         return !b.querySelector('img') || b.querySelector('.promo-judul') || !b.querySelector('.tirai');
       }));

    /* indikator mengikuti posisi geseran */
    pita.style.scrollBehavior = 'auto';
    pita.scrollLeft = (pita.clientWidth + 10) * 2;
    pita.dispatchEvent(new Event('scroll'));
    var titikOn = [].findIndex.call(document.querySelectorAll('#promo-titik i'), function (t) { return t.className === 'on'; });
    ok('titik aktif mengikuti geseran', titikOn === 2, 'titik aktif ke-' + (titikOn + 1));
    pita.scrollLeft = 0;
    pita.dispatchEvent(new Event('scroll'));

    ok('banner tidak membuat beranda meluber ke samping',
       document.querySelector('.scroll').scrollWidth === document.querySelector('.scroll').clientWidth,
       document.querySelector('.scroll').scrollWidth + ' vs ' + document.querySelector('.scroll').clientWidth);

    var tujuan = '#/' + slide[0].getAttribute('data-arg');
    klik('.promo-kartu', 0);
    ok('ketukan banner membuka layar terkait', location.hash === tujuan, location.hash);
    ganti('#/beranda');

    /* 2. profil bisa diubah */
    ganti('#/profil');
    isi('[data-field="profil.nama"]', 'Ibu Sari Dewi');
    isi('[data-field="profil.hp"]', '081234567890');
    ok('profil tersimpan', st().profil && st().profil.nama === 'Ibu Sari Dewi', JSON.stringify(st().profil));
    ok('menu korporat tersedia di profil', document.body.textContent.indexOf('Korporat / Sekolah') > 0);

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

    /* 5b. pesan WhatsApp membawa kode data untuk dashboard klinik */
    var bukaAsli = window.open;
    window.open = function (u) { window.__waBooking = u; return null; };
    klik('[data-act="wa-booking"]');
    window.open = bukaAsli;
    var pesanBk = decodeURIComponent((window.__waBooking || '').split('text=')[1] || '');
    var kd = pesanBk.match(/VKD1\.([A-Za-z0-9_-]+)/), isiKd = null;
    try {
      var b64 = kd[1].replace(/-/g, '+').replace(/_/g, '/');
      while (b64.length % 4) b64 += '=';
      isiKd = JSON.parse(decodeURIComponent(escape(atob(b64))));
    } catch (e) {}
    ok('pesan reservasi memuat kode data', !!kd, kd ? kd[0].length + ' karakter' : pesanBk.slice(-60));
    ok('kode data sesuai reservasi', !!isiKd && isiKd.k === b.kode && isiKd.t === b.tanggal && isiKd.j === b.jam &&
       JSON.stringify(isiKd.v) === JSON.stringify(b.vaksinIds), isiKd ? isiKd.k + ' · ' + isiKd.v.length + ' vaksin' : '-');
    var pk = st().pasien.filter(function (x) { return x.id === b.pasienIds[0]; })[0] || {};
    ok('kode data membawa nama & tanggal lahir pasien', !!isiKd && isiKd.p[0][0] === pk.nama && isiKd.p[0][1] === pk.tglLahir,
       isiKd ? isiKd.p[0].join(' / ') : '-');

    /* 6. tandai selesai */
    window.confirm = function () { return true; };
    klik('[data-act="selesai-booking"]');
    var s6 = st();
    ok('status jadi selesai', s6.booking[0].status === 'selesai');
    ok('riwayat vaksin tercatat', s6.riwayat.length > 0, s6.riwayat.length + ' catatan');
    ok('poin bertambah', s6.poin === 10, s6.poin + ' poin');

    /* 6b. vaksin dari reservasi tercatat sebagai dosis jadwal anak */
    var rFlu = s6.riwayat.filter(function (r) { return r.sumber === 'booking'; })[0];
    ok('vaksin reservasi dipetakan ke dosis jadwal', !!rFlu && (rFlu.kunci || []).indexOf('flu:1') >= 0,
       rFlu ? JSON.stringify(rFlu.kunci) : '-');

    /* 7. jadwal anak: IDAI ↔ KIA, ceklis per dosis dengan No. Batch */
    ganti('#/jadwal');
    var selIdai = document.querySelectorAll('.idai-dosis');
    ok('tabel ceklis IDAI tampil', selIdai.length > 40, selIdai.length + ' dosis');
    ok('jadwal bawaan IDAI 2024', document.body.textContent.indexOf('Jadwal IDAI 2024') > 0);
    ok('dosis terlewat tidak dihitung kurang (Rotavirus usia 5 thn)',
       !!document.querySelector('[data-arg$="|rv1"].st-terlewat'));
    var bar = function () { var i = document.querySelector('.bar > i'); return i ? i.style.width : '-'; };
    var persenSebelum = bar();
    klik('[data-act="buka-dosis"][data-arg$="|bcg"]');
    var fd = document.getElementById('form-dosis');
    ok('lembar catat dosis terbuka', !!fd && !!fd.elements.batch);
    fd.elements.tanggal.value = (new Date().getFullYear() - 5) + '-06-01';
    fd.elements.tempat.value = 'Posyandu';
    fd.elements.batch.value = 'BCG-2104A';
    fd.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    var rBcg = st().riwayat.filter(function (r) { return (r.kunci || []).indexOf('bcg:1') >= 0; })[0];
    ok('dosis tercatat dengan No. Batch', !!rBcg && rBcg.batch === 'BCG-2104A' && rBcg.tempat === 'Posyandu',
       rBcg ? rBcg.batch + ' · ' + rBcg.tempat : '-');
    ok('ceklis mengubah kelengkapan', persenSebelum !== bar(), persenSebelum + ' → ' + bar());

    klik('[data-act="buka-dosis"][data-arg$="|dtp1"]');
    var fd2 = document.getElementById('form-dosis');
    fd2.elements.batch.value = 'HX-77';
    fd2.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));

    klik('[data-act="ganti-jadwal"][data-arg$="|kia"]');
    ok('ganti ke jadwal Buku KIA', st().pasien[0].jadwalAnak === 'kia' && document.querySelectorAll('table.kia tr.kia-baris').length > 15,
       document.querySelectorAll('table.kia tr.kia-baris').length + ' baris');
    ok('BCG tercatat terbaca di tabel KIA', !!document.querySelector('[data-arg$="|k-bcg"] .cek'));
    ok('DTP 1 saja belum memenuhi DPT-HB-Hib 1', !document.querySelector('[data-arg$="|k-dpt1"] .cek'));
    klik('[data-act="buka-dosis"][data-arg$="|k-dpt1"]');
    ok('dosis kombinasi menjelaskan antigen yang tercatat', document.body.textContent.indexOf('sekaligus mencatat') > 0);
    ok('lewat batas program: masih bisa dikejar di klinik, tidak ditawarkan gratis',
       document.body.textContent.indexOf('masih boleh dikejar') > 0 && !document.querySelector('[data-act="pkm-dosis"]'));
    klik('[data-act="tutup-sheet"]');
    klik('[data-act="buka-dosis"][data-arg$="|k-bias-mr"]');
    klik('[data-act="pkm-dosis"][data-arg$="|k-bias-mr"]');
    ok('rencana gratis di Puskesmas tersimpan', !!(st().pasien[0].pkm || {})['mr:3']);
    klik('[data-act="tutup-sheet"]');
    klik('[data-act="ganti-jadwal"][data-arg$="|idai"]');
    ok('kembali ke IDAI, catatan tetap', st().pasien[0].jadwalAnak === 'idai' &&
       !!document.querySelector('[data-arg$="|bcg"].st-selesai') && !!document.querySelector('[data-arg$="|dtp1"].st-selesai'));

    /* 7b. perbandingan jadwal, kondisi khusus, tanda gratis di Puskesmas */
    ganti('#/jadwal-banding');
    ok('perbandingan IDAI vs KIA tampil', document.querySelectorAll('.mk-banding tr.beda').length > 5,
       document.querySelectorAll('.mk-banding tr.beda').length + ' dosis berbeda');
    ganti('#/pasien-form/' + st().pasien[0].id);
    var fk = document.getElementById('form-pasien');
    fk.elements['kondisi-bblr'].checked = true;
    fk.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    ganti('#/jadwal');
    ok('kondisi khusus memunculkan peringatan', document.body.textContent.indexOf('Berat lahir kurang dari 2.000 g') > 0);
    ganti('#/harga');
    ok('tanda gratis di Puskesmas di daftar harga', document.body.textContent.indexOf('Gratis di Puskesmas (anak)') > 0);

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

    /* 13. modul korporat / sekolah */
    ganti('#/korporat');
    ok('modul korporat minta data institusi dulu', !!document.getElementById('form-korporat'));
    kirim('form-korporat');
    ok('institusi kosong ditolak', !st().korporat.nama && document.querySelectorAll('.errmsg').length === 2,
       document.querySelectorAll('.errmsg').length + ' pesan galat');
    klik('[data-act="kor-jenis"][data-arg="sekolah"]');
    var fk = document.getElementById('form-korporat');
    fk.elements.nama.value = 'SDN 001 Tanjungpinang';
    fk.elements.periode.value = 'Tahun Ajaran 2026/2027';
    kirim(fk);
    ok('dashboard institusi dibuat', st().korporat.nama === 'SDN 001 Tanjungpinang' && location.hash === '#/korporat',
       st().korporat.jenis + ' · ' + location.hash);
    ok('dashboard sekolah memuat jadwal BIAS', document.body.textContent.indexOf('Jadwal BIAS') > 0 &&
       document.body.textContent.indexOf('HPV dosis 2 untuk siswi') > 0);

    /* tempel daftar nama sekaligus */
    ganti('#/korporat-massal');
    var fmm = document.getElementById('form-massal-kor');
    fmm.elements.unit.value = '1A';
    fmm.elements.nama.value = '1. Ahmad Fauzi\n2. Bunga Lestari\n\n3. Citra Ramadhani\nAhmad Fauzi\n';
    kirim(fmm);
    var ps = st().korporat.peserta;
    ok('tempel daftar menambah peserta', ps.length === 3, ps.length + ' peserta');
    ok('nomor urut dibuang dari nama', ps[0].nama === 'Ahmad Fauzi', ps.map(function (x) { return x.nama; }).join(', '));
    ok('nama kembar tidak diduplikasi', ps.filter(function (x) { return x.nama === 'Ahmad Fauzi'; }).length === 1);

    /* tambah satu per satu */
    ganti('#/korporat-peserta');
    var fp = document.getElementById('form-peserta-kor');
    fp.elements.nama.value = 'Dewi Anggraini';
    fp.elements.unit.value = '1B';
    kirim(fp);
    ok('peserta tunggal ditambahkan', st().korporat.peserta.length === 4,
       st().korporat.peserta.length + ' peserta');

    /* tandai sudah divaksin */
    ganti('#/korporat');
    klik('[data-act="kor-tab"][data-arg="peserta"]');
    ok('daftar peserta dikelompokkan per kelas', document.querySelectorAll('[data-act="kor-toggle"]').length === 4);
    klik('[data-act="kor-toggle"]', 0);
    var sudahP = st().korporat.peserta.filter(function (x) { return x.status === 'sudah'; });
    ok('peserta bisa ditandai sudah divaksin', sudahP.length === 1 && sudahP[0].tanggal === new Date(Date.now() - new Date().getTimezoneOffset() * 6e4).toISOString().slice(0, 10),
       sudahP.length ? sudahP[0].nama + ' · ' + sudahP[0].tanggal : '-');

    klik('[data-act="kor-tab"][data-arg="ringkasan"]');
    ok('coverage dihitung dari daftar peserta', document.body.textContent.indexOf('25%') > 0,
       (document.body.textContent.match(/(\d+)%/) || [])[0]);
    ok('cakupan per kelas tampil', document.querySelectorAll('.bar > i').length === 2,
       document.querySelectorAll('.bar > i').length + ' kelas');

    /* laporan: booking massal */
    klik('[data-act="kor-tab"][data-arg="laporan"]');
    window.__waTerakhir = '';
    klik('[data-act="kor-kirim"]');
    ok('booking massal butuh jenis vaksin', !window.__waTerakhir, window.__waTerakhir || '(tidak dikirim)');
    var vFlu = K2.harga.filter(function (v) { return v.kategori.indexOf('Influenza') === 0 && v.umum; })[0];
    isi('[data-field="kor.vaksinId"]', vFlu.id);
    isi('[data-field="kor.tanggal"]', besok);
    var satuanFlu = parseInt(vFlu.umum.replace(/\D/g, ''), 10);
    var harapEst = 'Estimasi biayaRp' + (3 * satuanFlu).toLocaleString('id-ID') +
      '3 peserta belum divaksin \u00d7 Rp' + satuanFlu.toLocaleString('id-ID');
    ok('estimasi biaya massal terhitung', document.body.textContent.indexOf(harapEst) > 0,
       harapEst.replace('Estimasi biaya', ''));
    klik('[data-act="kor-kirim"]');
    var waKor = decodeURIComponent(window.__waTerakhir || '');
    ok('permintaan massal dikirim ke WhatsApp', waKor.indexOf('Booking Massal') > 0 &&
       waKor.indexOf('SDN 001 Tanjungpinang') > 0 && waKor.indexOf('3 orang') > 0,
       (window.__waTerakhir || '').slice(0, 34) + '...');

    /* rekap csv */
    var csvTeks = null, blobAsli2 = window.Blob;
    window.Blob = function (bagian, opsi) { csvTeks = String(bagian[0]); return new blobAsli2(bagian, opsi); };
    klik('[data-act="kor-csv"]');
    window.Blob = blobAsli2;
    var barisCsv = (csvTeks || '').trim().split('\r\n');
    ok('rekap csv dibuat', !!csvTeks && csvTeks.indexOf('SDN 001 Tanjungpinang') > 0,
       barisCsv.length + ' baris');
    ok('csv memuat semua peserta', barisCsv.length === 13 && barisCsv[barisCsv.length - 1].indexOf('Dewi Anggraini') > 0,
       barisCsv[barisCsv.length - 1]);
    ok('csv mencatat status vaksinasi', (csvTeks || '').indexOf(';Sudah;') > 0 && (csvTeks || '').indexOf(';Belum;') > 0);

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
