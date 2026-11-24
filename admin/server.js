/* VaksinKu — penghubung dashboard klinik ke server (PostgREST di /api).
 *
 * muat(opsi)            → ambil data satu klinik dari server
 * petakan(data, lama)   → ubah baris server menjadi bentuk data dashboard (admin/app.js)
 * klien(opsi)           → fungsi permintaan bertoken; galat membawa .status dan .pesan
 *
 * Server adalah sumber kebenaran: booking, pasien, stok, pelayanan, dan tagihan dibaca
 * ulang setelah setiap tindakan. Penulisan lewat fungsi database (buat_booking,
 * ubah_status_booking, terima_stok, sesuaikan_stok, catat_pelayanan, terima_pembayaran),
 * yang memeriksa hak petugas, kuota slot, stok, dan harga di sisi server.
 * Hanya data tampilan lokal (stok minimum, alamat & wali pasien) yang tetap di perangkat.
 */
(function (akar, buat) {
  if (typeof module === 'object' && module.exports) module.exports = buat();
  else akar.VaksinKuKlinik = buat();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var LAYANAN_LABEL = { homecare: 'Home Care', klinik: 'On Site Klinik', corporate: 'On Site Corporate' };
  var LAYANAN_KODE = { 'Home Care': 'homecare', 'On Site Klinik': 'klinik', 'On Site Corporate': 'corporate' };
  // status server → status dashboard ('tidak_hadir' bernama 'mangkir' di dashboard)
  var STATUS = { baru: 'baru', terkonfirmasi: 'terkonfirmasi', hadir: 'hadir', selesai: 'selesai', batal: 'batal', tidak_hadir: 'mangkir' };
  var VAKSINATOR = /^Vaksinator: (.*)\n?/;

  function klien(o) {
    var dasar = (o.api || '/api').replace(/\/$/, '');
    var ambil = o.fetch || (typeof fetch !== 'undefined' ? fetch : null);
    return function (metode, jalur, isi, prefer) {
      var kepala = { Authorization: 'Bearer ' + o.token, 'Content-Type': 'application/json' };
      if (prefer) kepala.Prefer = prefer;
      return ambil(dasar + jalur, { method: metode, headers: kepala, body: isi == null ? undefined : JSON.stringify(isi) })
        .then(function (r) {
          return r.text().then(function (t) {
            var d = null;
            try { d = t ? JSON.parse(t) : null; } catch (e) { d = null; }
            if (!r.ok) {
              var e2 = new Error((d && d.message) || 'HTTP ' + r.status);
              e2.status = r.status;
              // pesan berbahasa Indonesia dari fungsi database (mis. "Slot 09:00 penuh")
              e2.pesan = d && d.message && r.status < 500 && r.status !== 401 ? d.message : '';
              throw e2;
            }
            return d;
          });
        }, function () { var e3 = new Error('jaringan'); e3.status = 0; e3.pesan = ''; throw e3; });
    };
  }

  // tanggal kalender WIB dari stempel waktu server
  function tglWIB(ts) {
    if (!ts) return '';
    var d = new Date(ts);
    if (isNaN(d)) return String(ts).slice(0, 10);
    return new Date(d.getTime() + 7 * 36e5).toISOString().slice(0, 10);
  }
  function jamPendek(t) { return String(t || '').slice(0, 5); }
  function tglMundur(n) { return new Date(Date.now() - n * 864e5 + 7 * 36e5).toISOString().slice(0, 10); }

  function muat(o) {
    var minta = klien(o), k = encodeURIComponent(o.klinik);
    return Promise.all([
      minta('GET', '/klinik?select=id,nama,alamat,telepon_wa,jam_buka,jam_tutup,durasi_slot,kapasitas_slot,hari_libur&id=eq.' + k),
      minta('GET', '/booking?select=id,kode,profil_id,layanan,lokasi,tanggal,jam,tarif,status,catatan,bagikan_riwayat,sumber,dibuat_pada,' +
        'booking_item(pasien_id,vaksin_id,harga)&klinik_id=eq.' + k + '&tanggal=gte.' + tglMundur(180) + '&order=tanggal.desc,jam.desc&limit=1000'),
      minta('GET', '/pasien?select=id,nama,tgl_lahir,jenis_kelamin,hp,profil_id,klinik_pendaftar,dibuat_pada,profil(nama,hp)&order=dibuat_pada.desc&limit=1000'),
      minta('GET', '/stok_batch?select=id,vaksin_id,no_batch,kedaluwarsa,jumlah,sisa,dibuat_pada&klinik_id=eq.' + k),
      minta('GET', '/mutasi_stok?select=id,stok_id,jenis,jumlah,keterangan,dibuat_pada&order=dibuat_pada.desc&limit=300'),
      minta('GET', '/layanan?select=id,booking_id,pasien_id,kipi,catatan,dibuat_pada&klinik_id=eq.' + k + '&order=dibuat_pada.desc&limit=1000'),
      minta('GET', '/tagihan?select=id,nomor,layanan_id,item,total,dibayar,status,dibuat_pada,pembayaran(jumlah,metode,dibuat_pada)' +
        '&klinik_id=eq.' + k + '&order=dibuat_pada.desc&limit=1000')
    ]).then(function (r) {
      return { klinik: r[0][0] || null, booking: r[1], pasien: r[2], stok: r[3], mutasi: r[4], layanan: r[5], tagihan: r[6] };
    });
  }

  // lama: state dashboard sebelumnya (untuk data tampilan lokal: stok minimum, alamat/wali pasien)
  function petakan(d, lama) {
    lama = lama || {};
    var ekstra = lama.ekstraPasien || {}, minimum = lama.minimumStok || {};
    var out = {};

    var kl = d.klinik || {};
    out.klinik = { nama: kl.nama || '', alamat: kl.alamat || '', telp: kl.telepon_wa || '' };
    out.jadwal = {
      buka: jamPendek(kl.jam_buka) || '08:00', tutup: jamPendek(kl.jam_tutup) || '16:00',
      durasi: kl.durasi_slot || 30, kapasitas: kl.kapasitas_slot || 3, libur: (kl.hari_libur || [0]).slice()
    };

    out.pasien = (d.pasien || []).map(function (p) {
      var akun = p.profil || null, x = ekstra[p.id] || {};
      return {
        id: p.id, noRM: 'P-' + String(p.id).replace(/-/g, '').slice(0, 6).toUpperCase(),
        nama: p.nama, tglLahir: p.tgl_lahir, jk: p.jenis_kelamin || '',
        hp: p.hp || (akun && akun.hp) || '', wali: x.wali || (akun && akun.nama !== p.nama ? akun.nama : '') || '',
        alamat: x.alamat || '', dibuat: p.dibuat_pada || '', akun: !!p.profil_id, klinikPendaftar: p.klinik_pendaftar || ''
      };
    });

    // pelayanan per (booking, pasien) & tagihan per pelayanan
    var tagihanLayanan = {};
    (d.tagihan || []).forEach(function (t) { tagihanLayanan[t.layanan_id] = t; });
    var dilayani = {};
    (d.layanan || []).forEach(function (l) { dilayani[l.booking_id + '~' + l.pasien_id] = l; });

    // satu baris dashboard per pasien dalam booking (antrean & tagihan dihitung per orang)
    out.booking = [];
    (d.booking || []).forEach(function (b) {
      var perPasien = {}, urut = [];
      (b.booking_item || []).forEach(function (it) {
        if (!perPasien[it.pasien_id]) { perPasien[it.pasien_id] = { vaksinIds: [], harga: {} }; urut.push(it.pasien_id); }
        perPasien[it.pasien_id].vaksinIds.push(it.vaksin_id);
        perPasien[it.pasien_id].harga[it.vaksin_id] = it.harga;
      });
      urut.forEach(function (pid) {
        var l = dilayani[b.id + '~' + pid];
        out.booking.push({
          id: b.id + '~' + pid, srv: b.id, pasienId: pid, kode: b.kode,
          layanan: LAYANAN_LABEL[b.layanan] || b.layanan, lokasi: b.lokasi || '',
          tanggal: b.tanggal, jam: jamPendek(b.jam), dokter: '', dokterTarif: b.tarif,
          vaksinIds: perPasien[pid].vaksinIds, harga: perPasien[pid].harga, catatan: b.catatan || '',
          status: l ? 'selesai' : (STATUS[b.status] || b.status), statusServer: b.status,
          sumber: b.sumber === 'aplikasi' ? 'aplikasi pasien' : b.sumber, akunPasien: !!b.profil_id,
          bagikan: !!b.bagikan_riwayat, dibuat: tglWIB(b.dibuat_pada)
        });
      });
    });

    out.stok = (d.stok || []).map(function (s) {
      return {
        id: s.id, vaksinId: s.vaksin_id, batch: s.no_batch, kedaluwarsa: s.kedaluwarsa,
        jumlahAwal: s.jumlah, sisa: s.sisa, minimum: +minimum[s.id] || 0, dibuat: s.dibuat_pada || ''
      };
    });
    var adaStok = {};
    out.stok.forEach(function (s) { adaStok[s.id] = true; });
    out.mutasi = (d.mutasi || []).filter(function (m) { return adaStok[m.stok_id]; }).map(function (m) {
      var jenis = m.jenis === 'koreksi' ? (m.jumlah > 0 ? 'masuk' : 'keluar') : m.jenis;
      return {
        id: m.id, stokId: m.stok_id, jenis: jenis, jumlah: Math.abs(m.jumlah), tanggal: tglWIB(m.dibuat_pada),
        ket: (m.jenis === 'koreksi' ? 'Koreksi: ' : '') + (m.keterangan || ''), dibuat: m.dibuat_pada || ''
      };
    });

    out.layanan = (d.layanan || []).map(function (l) {
      var t = tagihanLayanan[l.id], m = VAKSINATOR.exec(l.catatan || '');
      return {
        id: l.id, bookingId: l.booking_id + '~' + l.pasien_id, pasienId: l.pasien_id, tanggal: tglWIB(l.dibuat_pada),
        item: (t ? t.item : []).map(function (it) { return { vaksinId: it.vaksin_id, batch: it.no_batch }; }),
        petugas: m ? m[1] : '', kipi: l.kipi || '', catatan: (l.catatan || '').replace(VAKSINATOR, ''), dibuat: l.dibuat_pada || ''
      };
    });
    var layananById = {};
    (d.layanan || []).forEach(function (l) { layananById[l.id] = l; });

    out.transaksi = (d.tagihan || []).map(function (t) {
      var l = layananById[t.layanan_id] || {}, bayar = (t.pembayaran || []).slice().sort(function (a, b) {
        return String(a.dibuat_pada).localeCompare(String(b.dibuat_pada));
      });
      var akhir = bayar[bayar.length - 1] || {};
      return {
        id: t.id, nomor: t.nomor, bookingId: l.booking_id ? l.booking_id + '~' + l.pasien_id : '', pasienId: l.pasien_id || '',
        tanggal: tglWIB(t.dibuat_pada),
        item: (t.item || []).map(function (it) { return { nama: it.nama, harga: it.harga, vaksinId: it.vaksin_id, batch: it.no_batch }; }),
        total: t.total, dibayar: t.dibayar, status: t.status === 'lunas' ? 'lunas' : 'terbuka',
        metode: akhir.metode || '', tglBayar: tglWIB(akhir.dibuat_pada), ket: '', dibuat: t.dibuat_pada || ''
      };
    });
    return out;
  }

  return {
    klien: klien, muat: muat, petakan: petakan, tglWIB: tglWIB,
    LAYANAN_KODE: LAYANAN_KODE, LAYANAN_LABEL: LAYANAN_LABEL, VAKSINATOR: VAKSINATOR
  };
});
