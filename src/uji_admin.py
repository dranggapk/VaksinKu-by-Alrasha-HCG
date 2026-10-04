#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uji fungsional dashboard manajemen VaksinKu di browser headless.

Menjalankan alur nyata dari sisi petugas: daftarkan pasien, terima stok,
buat booking, check-in, catat vaksinasi (stok berkurang, tagihan terbit),
terima pembayaran, lalu periksa angka di layar ringkasan.

    python3 uji_admin.py
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUNDLE = os.path.join(ROOT, "VaksinKu-Dashboard.html")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

TEST_JS = r"""
<script>
(function () {
  var hasil = [], galat = [];
  window.addEventListener('error', function (e) { galat.push(e.message); });

  function ok(nama, syarat, detail) {
    hasil.push((syarat ? 'LULUS' : 'GAGAL') + ' | ' + nama + (detail ? ' | ' + detail : ''));
  }
  function el(sel, ke) {
    var els = document.querySelectorAll(sel);
    return ke == null ? els[0] : els[ke];
  }
  function klik(sel, ke) {
    var e = el(sel, ke);
    if (!e) { hasil.push('GAGAL | elemen tidak ada: ' + sel); return false; }
    var sebelum = location.hash;
    e.click();
    if (location.hash !== sebelum) window.dispatchEvent(new HashChangeEvent('hashchange'));
    return true;
  }
  function isi(sel, nilai) {
    var e = el(sel);
    if (!e) { hasil.push('GAGAL | input tidak ada: ' + sel); return false; }
    e.value = nilai;
    e.dispatchEvent(new Event('input', { bubbles: true }));
    return true;
  }
  function kirim(id, nilai) {
    var f = document.getElementById(id);
    if (!f) { hasil.push('GAGAL | form tidak ada: ' + id); return false; }
    for (var k in (nilai || {})) if (f.elements[k]) f.elements[k].value = nilai[k];
    f.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    return true;
  }
  function st() { try { return JSON.parse(localStorage.getItem('vaksinku.admin.v1')) || {}; } catch (e) { return {}; } }
  function ganti(h) { location.hash = h; window.dispatchEvent(new HashChangeEvent('hashchange')); }
  function teks() { return document.body.textContent; }
  function bukaStok() { ganti('#/persediaan'); klik('[data-act="form-stok"]'); }
  function aturLibur(aktif) {
    ganti('#/pengaturan');
    [].forEach.call(document.querySelectorAll('[data-act="toggle-libur"]'), function (b) {
      var hidup = b.classList.contains('on');
      var hari = +b.getAttribute('data-arg');
      var mau = aktif.indexOf(hari) >= 0;
      if (hidup !== mau) b.click();
    });
  }
  function hariIni() { var d = new Date(); return new Date(d.getTime() - d.getTimezoneOffset() * 6e4).toISOString().slice(0, 10); }
  function geser(n) {
    var p = hariIni().split('-'), d = new Date(+p[0], +p[1] - 1, +p[2] + n);
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  }

  var K2 = window.KATALOG;
  window.confirm = function () { return true; };
  try {
    /* 1. boot */
    ok('katalog termuat', !!(K2 && K2.harga.length), K2.harga.length + ' baris harga');
    ok('kerangka dashboard tampil', !!document.querySelector('.sidebar') && !!document.querySelector('.utama'));
    ok('tujuh menu operasional tersedia', document.querySelectorAll('.navitem').length === 8,
       document.querySelectorAll('.navitem').length + ' menu');
    ok('ringkasan menyapa keadaan kosong', teks().indexOf('Mulai dari mana?') > 0);

    /* 2. pendaftaran pasien */
    ganti('#/pendaftaran');
    klik('[data-act="form-pasien"]');
    ok('panel pendaftaran terbuka', !!document.getElementById('form-pasien'));
    kirim('form-pasien', {});
    ok('pendaftaran kosong ditolak', (st().pasien || []).length === 0 && document.querySelectorAll('.errmsg').length === 2,
       document.querySelectorAll('.errmsg').length + ' pesan galat');
    kirim('form-pasien', { nama: 'Nadia Putri', tglLahir: geser(-1800), jk: 'Perempuan', hp: '12' });
    ok('nomor HP tidak valid ditolak', (st().pasien || []).length === 0 && document.querySelectorAll('.errmsg').length === 1);
    kirim('form-pasien', { nama: 'Nadia Putri', tglLahir: geser(-1800), jk: 'Perempuan', hp: '081234567890' });
    var p1 = (st().pasien || [])[0];
    ok('pasien tersimpan', !!p1 && p1.nama === 'Nadia Putri', p1 ? p1.noRM : '-');
    ok('nomor rekam medis berurutan', !!p1 && p1.noRM === 'RM00001', p1 ? p1.noRM : '-');
    ok('panel tertutup setelah simpan', !document.querySelector('.panel'));
    ok('pasien tampil di tabel', teks().indexOf('Nadia Putri') > 0);

    klik('[data-act="form-pasien"]');
    kirim('form-pasien', { nama: 'Bayu Pratama', tglLahir: geser(-12000), jk: 'Laki-laki', hp: '081200000000' });
    ok('pasien kedua memakai nomor RM berikutnya', st().pasien[1].noRM === 'RM00002', st().pasien[1].noRM);

    /* 3. persediaan: stok masuk */
    ganti('#/persediaan');
    ok('persediaan kosong terdeteksi', teks().indexOf('Belum ada stok tercatat') > 0);
    klik('[data-act="form-stok"]');
    kirim('form-stok', { vaksinId: '', batch: '', kedaluwarsa: '', jumlah: '' });
    ok('stok masuk kosong ditolak', (st().stok || []).length === 0 && document.querySelectorAll('.errmsg').length === 4,
       document.querySelectorAll('.errmsg').length + ' pesan galat');
    var vFlu = K2.harga.filter(function (v) { return v.kategori.indexOf('Influenza') === 0 && v.umum; })[0];
    kirim('form-stok', { vaksinId: vFlu.id, batch: 'FL-LAMA', kedaluwarsa: geser(-5), jumlah: '10' });
    ok('batch kedaluwarsa ditolak saat penerimaan', (st().stok || []).length === 0,
       document.querySelectorAll('.errmsg').length + ' pesan galat');
    kirim('form-stok', { vaksinId: vFlu.id, batch: 'FL-2608A', kedaluwarsa: geser(300), jumlah: '20', minimum: '5' });
    bukaStok();
    kirim('form-stok', { vaksinId: vFlu.id, batch: 'FL-2512B', kedaluwarsa: geser(60), jumlah: '4', minimum: '5' });
    ganti('#/persediaan');
    ok('dua batch tercatat', (st().stok || []).length === 2, st().stok.map(function (s) { return s.batch; }).join(', '));
    ok('mutasi masuk tercatat', (st().mutasi || []).length === 2);
    ok('ringkasan stok menjumlahkan batch', teks().indexOf('24 dosis') > 0);
    ok('batch dekat kedaluwarsa ditandai', teks().indexOf('batch < 90 hari') > 0 || teks().indexOf('60 hari') > 0);

    /* 4. booking */
    /* hari libur diuji dulu, lalu dikosongkan agar sisa uji tidak bergantung
       pada hari apa berkas uji ini dijalankan */
    var hariIniWd = new Date(hariIni() + 'T00:00:00').getDay();
    aturLibur([hariIniWd]);
    ganti('#/booking');
    klik('[data-act="form-booking"]');
    isi('[data-pd="tanggal"]', hariIni());
    ok('tanggal hari libur ditolak di booking', teks().indexOf('ditandai hari libur') > 0 &&
       document.querySelectorAll('[data-act="pd-jam"]').length === 0);
    aturLibur([]);

    ganti('#/booking');
    klik('[data-act="form-booking"]');
    ok('panel booking terbuka', !!document.querySelector('[data-pd="pasienId"]'));
    klik('[data-act="simpan-booking"]');
    ok('booking kosong ditolak', (st().booking || []).length === 0 && document.querySelectorAll('.errmsg').length >= 3,
       document.querySelectorAll('.errmsg').length + ' pesan galat');
    isi('[data-pd="pasienId"]', st().pasien[0].id);
    isi('[data-pd="tanggal"]', hariIni());
    var slotPertama = document.querySelector('[data-act="pd-jam"]');
    ok('slot jam dihitung dari jam layanan', document.querySelectorAll('[data-act="pd-jam"]').length === 16,
       document.querySelectorAll('[data-act="pd-jam"]').length + ' slot');
    slotPertama.click();
    isi('[data-act="pd-tambah-vaksin"]', vFlu.id);
    ok('vaksin masuk ke daftar booking', teks().indexOf('Estimasi tagihan') > 0);
    klik('[data-act="simpan-booking"]');
    var b1 = (st().booking || [])[0];
    ok('booking tersimpan', !!b1 && b1.status === 'terkonfirmasi', b1 ? b1.kode : '-');
    ok('kode booking berpola BK-', !!b1 && /^BK-\d{6}-001$/.test(b1.kode), b1 ? b1.kode : '-');

    /* 4b. kapasitas slot */
    ganti('#/pengaturan');
    isi('[data-field="jadwal.kapasitas"]', '1');
    ok('kapasitas slot tersimpan', st().jadwal.kapasitas === 1, String(st().jadwal.kapasitas));
    ganti('#/booking');
    klik('[data-act="form-booking"]');
    isi('[data-pd="pasienId"]', st().pasien[1].id);
    isi('[data-pd="tanggal"]', hariIni());
    var jamPenuh = document.querySelector('[data-act="pd-jam"]');
    ok('slot penuh dinonaktifkan', jamPenuh.hasAttribute('disabled'), jamPenuh.textContent.trim());
    document.querySelectorAll('[data-act="pd-jam"]')[1].click();
    isi('[data-act="pd-tambah-vaksin"]', vFlu.id);
    klik('[data-act="simpan-booking"]');
    ok('booking kedua masuk slot lain', (st().booking || []).length === 2, st().booking[1].jam);

    /* 5. penjadwalan */
    ganti('#/penjadwalan');
    ok('layar penjadwalan menampilkan slot', document.querySelectorAll('.slot').length === 16,
       document.querySelectorAll('.slot').length + ' slot');
    ok('kapasitas terpakai dihitung', teks().indexOf('2 / 16 kapasitas terpakai') > 0);
    ok('grafik beban tergambar', !!document.querySelector('#g-beban svg'),
       document.querySelectorAll('#g-beban .kolom').length + ' kolom');
    ok('grafik beban punya area sentuh', document.querySelectorAll('#g-beban .hit').length === 14);

    /* 6. pelayanan */
    ganti('#/pelayanan');
    ok('antrean hari ini terbentuk', document.querySelectorAll('.antre').length === 2,
       document.querySelectorAll('.antre').length + ' antrean');
    klik('[data-act="checkin"]');
    ok('check-in mengubah status', st().booking[0].status === 'hadir', st().booking[0].status);
    klik('[data-act="form-layanan"]');
    ok('panel pelayanan terbuka', !!document.querySelector('[data-batch]'));
    var pilihBatch = document.querySelector('[data-batch]');
    var terpilih = pilihBatch.options[pilihBatch.selectedIndex].textContent;
    ok('batch terpilih mengikuti FEFO', terpilih.indexOf('FL-2512B') > 0, terpilih.trim());
    klik('[data-act="simpan-layanan"]');
    var s7 = st();
    ok('pelayanan tercatat', (s7.layanan || []).length === 1);
    ok('booking jadi selesai', s7.booking[0].status === 'selesai');
    var batchFefo = s7.stok.filter(function (x) { return x.batch === 'FL-2512B'; })[0];
    ok('stok batch FEFO berkurang satu', batchFefo.sisa === 3, batchFefo.sisa + ' dari 4');
    ok('mutasi keluar tercatat', s7.mutasi.filter(function (m) { return m.jenis === 'keluar'; }).length === 1);
    var tx = (s7.transaksi || [])[0];
    ok('tagihan terbit otomatis', !!tx && tx.status === 'terbuka', tx ? tx.nomor : '-');
    ok('nilai tagihan dari price list', !!tx && tx.total === parseInt(vFlu.umum.replace(/\D/g, ''), 10),
       tx ? tx.total : '-');

    /* 7. transaksi */
    ganti('#/transaksi');
    ok('tagihan tampil belum lunas', teks().indexOf('Belum lunas') > 0);
    klik('[data-act="form-bayar"]');
    ok('panel pembayaran terbuka', !!document.getElementById('form-bayar'));
    kirim('form-bayar', { tid: st().transaksi[0].id, metode: 'QRIS', tglBayar: hariIni() });
    var tx2 = st().transaksi[0];
    ok('pembayaran dicatat lunas', tx2.status === 'lunas' && tx2.metode === 'QRIS', tx2.metode);
    ok('tanggal bayar tersimpan', tx2.tglBayar === hariIni(), tx2.tglBayar);
    ok('rekap metode pembayaran tampil', teks().indexOf('Metode pembayaran hari ini') > 0 && teks().indexOf('QRIS') > 0);

    /* rekap csv */
    var csvTeks = null, blobAsli = window.Blob;
    window.Blob = function (bagian, opsi) { csvTeks = String(bagian[0]); return new blobAsli(bagian, opsi); };
    window.URL.createObjectURL = function () { return 'blob:uji'; };
    window.URL.revokeObjectURL = function () {};
    klik('[data-act="ekspor-tx"]');
    window.Blob = blobAsli;
    ok('rekap transaksi .csv dibuat', !!csvTeks && csvTeks.indexOf('Nomor;Tanggal;Pasien') > 0,
       (csvTeks || '').trim().split('\r\n').length + ' baris');
    ok('rekap memuat nomor RM pasien', (csvTeks || '').indexOf('RM00001') > 0);

    /* 8. ringkasan memakai angka nyata */
    ganti('#/ringkasan');
    var nilaiStat = [].map.call(document.querySelectorAll('.stat .val'), function (e) { return e.textContent.trim(); });
    ok('ringkasan menghitung booking hari ini', nilaiStat[0] === '2', nilaiStat.join(' · '));
    ok('ringkasan menghitung pasien terdaftar', nilaiStat[1] === '2');
    ok('grafik pendapatan tergambar', !!document.querySelector('#g-omzet svg'));
    ok('kolom pendapatan hari ini ada isinya', document.querySelectorAll('#g-omzet .kolom').length === 1,
       document.querySelectorAll('#g-omzet .kolom').length + ' kolom berisi');
    ok('grafik memakai satu warna seri', [].every.call(document.querySelectorAll('#g-omzet .kolom'), function (k) {
      return k.getAttribute('class') === 'kolom';
    }));
    ok('nilai tertinggi dilabeli langsung', document.querySelectorAll('#g-omzet text.nilai').length === 1,
       document.querySelector('#g-omzet text.nilai').textContent);
    ok('rentang grafik bisa diganti', !!document.querySelector('[data-act="rentang"][data-arg="30"]'));
    klik('[data-act="rentang"][data-arg="7"]');
    ok('rentang 7 hari menggambar 7 titik', document.querySelectorAll('#g-omzet .hit').length === 7,
       document.querySelectorAll('#g-omzet .hit').length + ' titik');
    klik('[data-act="tabel-omzet"]');
    ok('tampilan tabel tersedia sebagai pengganti grafik',
       !document.querySelector('#g-omzet') && document.querySelectorAll('.tbl').length > 0);
    klik('[data-act="tabel-omzet"]');

    ok('peringatan persediaan muncul di ringkasan', teks().indexOf('Perhatian persediaan') > 0 &&
       teks().indexOf('Di bawah stok minimum') > 0);

    /* 9. lencana menu */
    var lencana = [].map.call(document.querySelectorAll('.navitem .jml'), function (e) { return e.textContent; });
    ok('lencana menu menunjukkan antrean & stok', lencana.length >= 2, lencana.join(','));

    /* 10. impor cadangan aplikasi pasien */
    var dataPasien = {
      profil: { nama: 'Ibu Sari', hp: '081299990000' },
      pasien: [{ id: 'x1', nama: 'Citra Ramadhani', tglLahir: geser(-2500), jenisKelamin: 'Perempuan' }],
      alamat: [{ alamat: 'Jl. Contoh No. 1' }],
      booking: [{ kode: 'VK-123456', pasienIds: ['x1'], layanan: 'homecare', tanggal: geser(3),
                  jam: '10:00', dokter: 'umum', vaksinIds: [vFlu.id], status: 'menunggu' }]
    };
    ganti('#/pengaturan');
    window.__imporUji = dataPasien;
    (function () {
      // panggil jalur impor yang sama dengan yang dipakai tombol berkas
      var fr = { result: JSON.stringify(dataPasien) };
      var input = document.getElementById('file-pasien');
      var berkas = new Blob([fr.result], { type: 'application/json' });
      berkas.name = 'cadangan.json';
      var dt = { files: [berkas] };
      Object.defineProperty(input, 'files', { value: dt.files, configurable: true });
      input.dispatchEvent(new Event('change', { bubbles: true }));
    })();
    setTimeout(function () {
      var s10 = st();
      ok('impor menambah pasien dari aplikasi', (s10.pasien || []).length === 3,
         (s10.pasien || []).length + ' pasien');
      ok('impor menambah booking dari aplikasi', (s10.booking || []).length === 3,
         (s10.booking || []).length + ' booking');
      ok('booking impor ditandai sumbernya', (s10.booking || []).some(function (b) { return b.sumber === 'aplikasi pasien'; }));
      selesai();
    }, 400);
    return;
  } catch (e) {
    hasil.push('GAGAL | pengecualian: ' + e.message + ' @ ' + (e.stack || '').split('\n')[1]);
  }
  selesai();

  function selesai() {
    if (galat.length) hasil.push('GAGAL | galat konsol: ' + galat.join(' ; '));
    var out = document.createElement('pre');
    out.id = 'hasil-uji';
    out.textContent = hasil.join('\n');
    document.body.appendChild(out);
  }
})();
</script>
"""


def main():
    with open(BUNDLE, encoding="utf-8") as f:
        html = f.read()
    html = html.replace("</body>", TEST_JS + "\n</body>")
    tmp = os.path.join(tempfile.gettempdir(), "_uji_admin.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html)

    out = subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
         "--allow-file-access-from-files", "--virtual-time-budget=8000",
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
