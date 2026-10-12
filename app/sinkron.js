/* VaksinKu · sinkronisasi data pasien dengan server (PostgREST di vaksinku.app/api).
 *
 * Yang disinkronkan: profil (nama, HP), anggota keluarga (tabel pasien), dan riwayat
 * dosis. Foto label vaksin tetap di perangkat. Catatan dosis dari klinik (terverifikasi,
 * dengan No. Batch) hanya diterima dari server dan tidak pernah dikirim balik.
 *
 * Penggabungan tiga arah per baris, dengan S.sinkron.dikenal[sid] = sidik baris saat
 * sinkron terakhir:
 *   - ada di sini & di server: yang berubah sejak sinkron terakhir menang; bila keduanya
 *     berubah, perubahan di perangkat ini yang dipakai
 *   - hanya di sini:   dikenal → sudah dihapus di perangkat lain → hapus di sini
 *                      belum dikenal → baru → kirim
 *   - hanya di server: dikenal → dihapus di sini → hapus di server
 *                      belum dikenal → dari perangkat lain → ambil
 * Modul ini tidak menyentuh tampilan; dipakai app.js dan diuji langsung terhadap
 * PostgREST oleh src/uji_backend.mjs. */
(function (akar, buat) {
  var modul = buat();
  if (typeof module === 'object' && module.exports) module.exports = modul;
  else akar.VaksinKuSinkron = modul;
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  function uuid() {
    var c = typeof crypto !== 'undefined' ? crypto : null;
    if (c && c.randomUUID) return c.randomUUID();
    var b = new Uint8Array(16);
    if (c && c.getRandomValues) c.getRandomValues(b);
    else for (var i = 0; i < 16; i++) b[i] = Math.floor(Math.random() * 256);
    b[6] = (b[6] & 15) | 64; b[8] = (b[8] & 63) | 128;
    var h = Array.prototype.map.call(b, function (x) { return (x + 256).toString(16).slice(1); }).join('');
    return h.slice(0, 8) + '-' + h.slice(8, 12) + '-' + h.slice(12, 16) + '-' + h.slice(16, 20) + '-' + h.slice(20);
  }

  // JSON dengan kunci objek terurut, agar sidik baris tidak bergantung urutan kunci.
  function sidik(v) {
    if (Array.isArray(v)) return '[' + v.map(sidik).join(',') + ']';
    if (v && typeof v === 'object') {
      return '{' + Object.keys(v).sort().map(function (k) { return JSON.stringify(k) + ':' + sidik(v[k]); }).join(',') + '}';
    }
    return JSON.stringify(v === undefined ? null : v);
  }

  var JK = ['', 'Perempuan', 'Laki-laki'];
  function teks(v) { return v == null ? '' : String(v); }

  // ------------------------------------------------------------ bentuk baris server
  function barisPasien(p) {
    var kondisi = {};
    Object.keys(p.kondisi || {}).sort().forEach(function (k) { if (p.kondisi[k]) kondisi[k] = true; });
    return {
      nama: teks(p.nama).trim(),
      tgl_lahir: teks(p.tglLahir || p.tgl_lahir),
      jenis_kelamin: JK.indexOf(p.jenisKelamin) >= 0 ? p.jenisKelamin : (JK.indexOf(p.jenis_kelamin) >= 0 ? p.jenis_kelamin : ''),
      hubungan: teks(p.hubungan),
      jadwal_anak: (p.jadwalAnak || p.jadwal_anak) === 'kia' ? 'kia' : 'idai',
      endemis: !!p.endemis,
      rv: ['rv1', 'rv5'].indexOf(p.rv) >= 0 ? p.rv : '',
      kondisi: kondisi
    };
  }
  function keLokalPasien(b, lama) {
    var p = lama || { id: 'srv-' + b.id };
    p.sid = b.id;
    p.nama = b.nama; p.tglLahir = b.tgl_lahir; p.jenisKelamin = b.jenis_kelamin; p.hubungan = b.hubungan;
    p.jadwalAnak = b.jadwal_anak; p.endemis = !!b.endemis; p.rv = b.rv || '';
    p.kondisi = b.kondisi || {};
    return p;
  }
  function barisRiwayat(r) {
    return {
      kunci: (r.kunci || []).slice(),
      label: teks(r.label),
      tanggal: teks(r.tanggal),
      tempat: teks(r.tempat),
      faskes: teks(r.faskes),
      merek: teks(r.merek),
      no_batch: teks(r.batch != null ? r.batch : r.no_batch)
    };
  }
  function keLokalRiwayat(b, pasienLokalId, lama) {
    var r = lama || { id: 'srv-' + b.id };
    r.sid = b.id; r.pasienId = pasienLokalId;
    r.kunci = (b.kunci || []).slice(); r.label = b.label; r.tanggal = b.tanggal;
    r.tempat = b.tempat; r.faskes = b.faskes; r.merek = b.merek; r.batch = b.no_batch;
    if (b.sumber === 'klinik') {
      r.sumber = 'klinik'; r.diverifikasi = !!b.diverifikasi; r.klinikId = b.klinik_id || '';
    } else if (!r.sumber || r.sumber === 'klinik') {
      r.sumber = 'jadwal';
    }
    return r;
  }

  // ------------------------------------------------------------ HTTP
  function klien(o) {
    var dasar = (o.api || '/api').replace(/\/$/, '');
    var ambil = o.fetch || (typeof fetch !== 'undefined' ? fetch : null);
    return function (metode, jalur, isi, prefer) {
      var kepala = { Authorization: 'Bearer ' + o.token, 'Content-Type': 'application/json' };
      if (prefer) kepala.Prefer = prefer;
      return ambil(dasar + jalur, { method: metode, headers: kepala, body: isi == null ? undefined : JSON.stringify(isi) })
        .then(function (r) {
          return r.text().then(function (t) {
            if (!r.ok) {
              var e = new Error('HTTP ' + r.status + ' ' + metode + ' ' + jalur.split('?')[0] + ': ' + t.slice(0, 160));
              e.status = r.status; throw e;
            }
            return t ? JSON.parse(t) : null;
          });
        });
    };
  }
  function daftarId(ids) { return 'in.(' + ids.join(',') + ')'; }

  // ------------------------------------------------------------ rencana penggabungan
  // lokal: [{sid?, baris, rec}], server: [{id, baris, mentah}], dikenal: {sid: sidik}
  function rencanakan(lokal, server, dikenal) {
    var hasil = { kirim: [], hapusServer: [], ambil: [], hapusLokal: [], tetap: [] };
    var diServer = {};
    server.forEach(function (s) { diServer[s.id] = s; });
    var diLokal = {};
    lokal.forEach(function (l) {
      if (!l.sid) { hasil.kirim.push(l); return; }
      diLokal[l.sid] = l;
      var s = diServer[l.sid], jejak = dikenal[l.sid];
      if (!s) {
        if (jejak) hasil.hapusLokal.push(l); else hasil.kirim.push(l);
        return;
      }
      var sl = sidik(l.baris), ss = sidik(s.baris);
      if (sl === ss) hasil.tetap.push(l);
      else if (jejak && sl === jejak) hasil.ambil.push({ lokal: l, server: s });   // hanya server berubah
      else hasil.kirim.push(l);                                                  // perangkat ini berubah
    });
    server.forEach(function (s) {
      if (diLokal[s.id]) return;
      if (dikenal[s.id]) hasil.hapusServer.push(s); else hasil.ambil.push({ lokal: null, server: s });
    });
    return hasil;
  }

  // ------------------------------------------------------------ sinkron
  function sinkron(S, o) {
    var minta = klien(o);
    var akun = o.akunId;
    var st = S.sinkron = S.sinkron || {};
    st.dikenal = st.dikenal || {};
    var ringkas = { dikirim: 0, diterima: 0, dihapus: 0 };
    var kolomP = 'id,nama,tgl_lahir,jenis_kelamin,hubungan,jadwal_anak,endemis,rv,kondisi';
    var kolomR = 'id,pasien_id,kunci,label,tanggal,tempat,faskes,merek,no_batch,sumber,diverifikasi,klinik_id';

    S.profil = S.profil || {};
    st.profil = st.profil && typeof st.profil === 'object' ? st.profil : {};

    return Promise.resolve()
      // ---------------- profil: per kolom; isian kosong di sini tidak menimpa server
      .then(function () { return minta('GET', '/profil?select=nama,hp&id=eq.' + akun); })
      .then(function (baris) {
        var srv = baris[0] || { nama: '', hp: '' }, ubah = {};
        ['nama', 'hp'].forEach(function (k) {
          var l = teks(S.profil[k]).trim(), sv = teks(srv[k]).trim();
          if (l === sv) { st.profil[k] = l; return; }
          if (!l || st.profil[k] === l) { S.profil[k] = sv; st.profil[k] = sv; if (sv) ringkas.diterima++; return; }
          ubah[k] = l;
        });
        if (!Object.keys(ubah).length) return;
        return minta('PATCH', '/profil?id=eq.' + akun, ubah, 'return=minimal').then(function () {
          Object.keys(ubah).forEach(function (k) { st.profil[k] = ubah[k]; });
          ringkas.dikirim++;
        });
      })
      // ---------------- anggota keluarga
      .then(function () { return minta('GET', '/pasien?select=' + kolomP + '&profil_id=eq.' + akun); })
      .then(function (srvP) {
        var lokal = S.pasien.filter(function (p) { return p.nama && (p.tglLahir || p.tgl_lahir); })
          .map(function (p) { return { sid: p.sid, baris: barisPasien(p), rec: p }; });
        var server = srvP.map(function (b) { return { id: b.id, baris: barisPasien(b), mentah: b }; });
        var r = rencanakan(lokal, server, st.dikenal);
        var tugas = [];

        r.kirim.forEach(function (l) { if (!l.rec.sid) l.rec.sid = uuid(); l.sid = l.rec.sid; });
        if (r.kirim.length) {
          var isi = r.kirim.map(function (l) {
            var b = Object.assign({ id: l.sid, profil_id: akun }, l.baris); return b;
          });
          tugas.push(minta('POST', '/pasien', isi, 'resolution=merge-duplicates,return=minimal').then(function () {
            r.kirim.forEach(function (l) { st.dikenal[l.sid] = sidik(l.baris); });
            ringkas.dikirim += r.kirim.length;
          }));
        }
        if (r.hapusServer.length) {
          tugas.push(minta('DELETE', '/pasien?id=' + daftarId(r.hapusServer.map(function (s) { return s.id; })), null, 'return=minimal')
            .then(function () { r.hapusServer.forEach(function (s) { delete st.dikenal[s.id]; }); ringkas.dihapus += r.hapusServer.length; }));
        }
        r.ambil.forEach(function (a) {
          var p = keLokalPasien(a.server.mentah, a.lokal && a.lokal.rec);
          if (!a.lokal) S.pasien.push(p);
          st.dikenal[a.server.id] = sidik(a.server.baris);
          ringkas.diterima++;
        });
        if (r.hapusLokal.length) {
          var buang = r.hapusLokal.map(function (l) { return l.rec.id; });
          S.pasien = S.pasien.filter(function (p) { return buang.indexOf(p.id) < 0; });
          S.riwayat = S.riwayat.filter(function (x) { return buang.indexOf(x.pasienId) < 0; });
          r.hapusLokal.forEach(function (l) { delete st.dikenal[l.sid]; });
          ringkas.dihapus += r.hapusLokal.length;
        }
        r.tetap.forEach(function (l) { st.dikenal[l.sid] = sidik(l.baris); });
        return Promise.all(tugas);
      })
      // ---------------- riwayat dosis
      .then(function () { return minta('GET', '/riwayat_dosis?select=' + kolomR); })
      .then(function (srvR) {
        var lokalPasien = {}, sidKeLokal = {};
        S.pasien.forEach(function (p) { if (p.sid && st.dikenal[p.sid]) { lokalPasien[p.id] = p.sid; sidKeLokal[p.sid] = p.id; } });
        srvR = srvR.filter(function (b) { return sidKeLokal[b.pasien_id]; });

        // catatan klinik: server selalu benar, tidak dikirim balik
        var klinikSrv = srvR.filter(function (b) { return b.sumber === 'klinik'; });
        var adaKlinik = {};
        klinikSrv.forEach(function (b) {
          adaKlinik[b.id] = true;
          var lama = S.riwayat.filter(function (x) { return x.sid === b.id; })[0];
          var r0 = keLokalRiwayat(b, sidKeLokal[b.pasien_id], lama);
          if (!lama) { S.riwayat.push(r0); ringkas.diterima++; }
        });
        S.riwayat = S.riwayat.filter(function (x) { return x.sumber !== 'klinik' || !x.sid || adaKlinik[x.sid] || !lokalPasien[x.pasienId]; });

        var lokal = S.riwayat.filter(function (x) {
          return x.sumber !== 'klinik' && lokalPasien[x.pasienId] && x.tanggal;
        }).map(function (x) { return { sid: x.sid, baris: barisRiwayat(x), rec: x }; });
        var server = srvR.filter(function (b) { return b.sumber !== 'klinik'; })
          .map(function (b) { return { id: b.id, baris: barisRiwayat(b), mentah: b }; });
        var r = rencanakan(lokal, server, st.dikenal);
        var tugas = [];

        r.kirim.forEach(function (l) { if (!l.rec.sid) l.rec.sid = uuid(); l.sid = l.rec.sid; });
        if (r.kirim.length) {
          var isi = r.kirim.map(function (l) {
            return Object.assign({ id: l.sid, pasien_id: lokalPasien[l.rec.pasienId], sumber: 'pasien' }, l.baris);
          });
          tugas.push(minta('POST', '/riwayat_dosis', isi, 'resolution=merge-duplicates,return=minimal').then(function () {
            r.kirim.forEach(function (l) { st.dikenal[l.sid] = sidik(l.baris); });
            ringkas.dikirim += r.kirim.length;
          }));
        }
        if (r.hapusServer.length) {
          tugas.push(minta('DELETE', '/riwayat_dosis?id=' + daftarId(r.hapusServer.map(function (s) { return s.id; })), null, 'return=minimal')
            .then(function () { r.hapusServer.forEach(function (s) { delete st.dikenal[s.id]; }); ringkas.dihapus += r.hapusServer.length; }));
        }
        r.ambil.forEach(function (a) {
          var x = keLokalRiwayat(a.server.mentah, sidKeLokal[a.server.mentah.pasien_id], a.lokal && a.lokal.rec);
          if (!a.lokal) S.riwayat.push(x);
          st.dikenal[a.server.id] = sidik(a.server.baris);
          ringkas.diterima++;
        });
        if (r.hapusLokal.length) {
          var buang = r.hapusLokal.map(function (l) { return l.rec; });
          S.riwayat = S.riwayat.filter(function (x) { return buang.indexOf(x) < 0; });
          r.hapusLokal.forEach(function (l) { delete st.dikenal[l.sid]; });
          ringkas.dihapus += r.hapusLokal.length;
        }
        r.tetap.forEach(function (l) { st.dikenal[l.sid] = sidik(l.baris); });
        return Promise.all(tugas);
      })
      .then(function () {
        st.akunId = akun;
        st.terakhir = new Date().toISOString();
        st.galat = '';
        return ringkas;
      });
  }

  return { sinkron: sinkron, rencanakan: rencanakan, barisPasien: barisPasien, barisRiwayat: barisRiwayat, sidik: sidik, uuid: uuid };
});
