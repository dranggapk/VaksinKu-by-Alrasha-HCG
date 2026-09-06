/* VaksinKu by Alrasha Ibumas — aplikasi vaksinasi keluarga.
   Data disimpan lokal di perangkat (localStorage). Tanpa server. */
(function () {
  'use strict';

  var K = window.KATALOG;
  var WA = '62' + K.brand.callCenter.replace(/\D/g, '').replace(/^0/, '');

  /* ============================ ikon ============================ */
  var ICON = {
    home: '<path d="M4 11.5 12 4l8 7.5"/><path d="M6 10v9a1 1 0 0 0 1 1h4v-6h2v6h4a1 1 0 0 0 1-1v-9"/>',
    calendar: '<rect x="4" y="5.5" width="16" height="15" rx="2.2"/><path d="M8 3.5v4M16 3.5v4M4 10h16"/>',
    doc: '<path d="M7 3h7l4 4v14a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1Z"/><path d="M14 3v4h4"/><path d="M9 12h6M9 16h6"/>',
    user: '<circle cx="12" cy="8" r="3.6"/><path d="M5 20c1.2-4 4-6 7-6s5.8 2 7 6"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    back: '<path d="M15 5l-7 7 7 7"/>',
    chevron: '<path d="M9 5l7 7-7 7"/>',
    check: '<path d="M5 12.5l4.5 4.5L19 7"/>',
    checkc: '<circle cx="12" cy="12" r="9"/><path d="M8 12.3l2.6 2.6L16.2 9"/>',
    circle: '<circle cx="12" cy="12" r="9"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/>',
    pin: '<path d="M12 21s7-6.3 7-11.5A7 7 0 0 0 5 9.5C5 14.7 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.4"/>',
    house: '<path d="M4 11.5 12 4l8 7.5"/><path d="M6 10v9a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1v-9"/>',
    building: '<rect x="5" y="4" width="14" height="17" rx="1.4"/><path d="M9 8h1.6M13.4 8H15M9 12h1.6M13.4 12h1.6M9 16h1.6M13.4 16h1.6"/>',
    syringe: '<path d="M13.5 4.5 19.5 10.5"/><path d="M16.5 3 21 7.5"/><path d="M15 7 7.5 14.5 6 19.5l5-1.5L18.5 10.5 15 7Z"/><path d="M10.5 9.5 12.5 11.5M8.5 11.5l2 2"/><path d="M6 19.5 3.5 22"/>',
    tag: '<path d="M11.4 3.6H20v8.6l-8.7 8.7a1.4 1.4 0 0 1-2 0l-6.6-6.6a1.4 1.4 0 0 1 0-2l8.7-8.7Z"/><circle cx="16.2" cy="7.8" r="1.4"/>',
    globe: '<circle cx="12" cy="12" r="8.6"/><path d="M3.6 12h16.8"/><path d="M12 3.4c2.2 2.4 3.4 5.4 3.4 8.6S14.2 18.2 12 20.6c-2.2-2.4-3.4-5.4-3.4-8.6S9.8 5.8 12 3.4Z"/>',
    wa: '<path d="M7 17.5 4.5 20l1-3.6A8 8 0 1 1 12 20a8 8 0 0 1-5-1.7Z"/><path d="M8.8 8.6c.2-.5.6-.5.9-.5h.6c.2 0 .5 0 .7.5s.8 1.9.9 2 .2.3 0 .6-.3.4-.5.6-.4.4-.2.8a6 6 0 0 0 2.8 2.5c.4.2.6.1.8-.1s.8-.9 1-1.2.4-.2.7-.1 1.8.8 2.1 1 .5.3.5.5-.1 1-.6 1.6-1.5 1.2-2.2 1.2c-1.9 0-4.4-1.4-5.9-3.4S8.4 9.3 8.8 8.6Z"/>',
    family: '<circle cx="8" cy="7.5" r="2.6"/><circle cx="16" cy="7.5" r="2.6"/><circle cx="12" cy="9.5" r="2"/><path d="M3.5 20c.6-2.7 2.2-4.3 4.5-4.3s3.6 1.3 4 3M12 20c.4-1.7 1.5-3 3-3.4M15.5 15.7c2.3 0 3.9 1.6 4.5 4.3"/>',
    chart: '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    trash: '<path d="M5 7h14M10 7V5h4v2M6.5 7l.8 12a1 1 0 0 0 1 1h7.4a1 1 0 0 0 1-1l.8-12"/><path d="M10 11v6M14 11v6"/>',
    edit: '<path d="M4 20h4L19 9l-4-4L4 16v4Z"/><path d="M14 6l4 4"/>',
    download: '<path d="M12 4v11"/><path d="M7.5 11.5 12 16l4.5-4.5"/><path d="M5 19.5h14"/>',
    upload: '<path d="M12 16V5"/><path d="M7.5 9.5 12 5l4.5 4.5"/><path d="M5 19.5h14"/>',
    shield: '<path d="M12 3.5 5 6v6c0 4.2 2.9 7.5 7 8.5 4.1-1 7-4.3 7-8.5V6l-7-2.5Z"/><path d="M9 12.2l2.2 2.2L15.2 10"/>',
    coin: '<circle cx="12" cy="12" r="8.4"/><path d="M12 8v8M9.4 10.2c0-1.1 1.1-2 2.6-2s2.6.7 2.6 1.8-1 1.6-2.6 2-2.6.9-2.6 2 1.1 1.8 2.6 1.8 2.6-.7 2.6-1.6"/>',
    search: '<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.3-4.3"/>',
    info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.6v.6"/>',
    bell: '<path d="M6 10a6 6 0 0 1 12 0c0 4 1.4 5.4 2 6H4c.6-.6 2-2 2-6Z"/><path d="M10 19a2 2 0 0 0 4 0"/>'
  };
  function ic(name, size, sw) {
    return '<svg width="' + (size || 20) + '" height="' + (size || 20) + '" viewBox="0 0 24 24" fill="none" ' +
      'stroke="currentColor" stroke-width="' + (sw || 1.8) + '" stroke-linecap="round" stroke-linejoin="round">' +
      (ICON[name] || '') + '</svg>';
  }

  /* ============================ util ============================ */
  function h(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function uid() { return Date.now().toString(36) + Math.random().toString(36).slice(2, 7); }
  function rp(n) { return 'Rp' + Number(n || 0).toLocaleString('id-ID'); }
  function angka(s) { return parseInt(String(s).replace(/\./g, ''), 10) || 0; }
  var BULAN = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'];
  var HARI = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'];
  function tgl(iso, panjang) {
    if (!iso) return '-';
    var d = new Date(iso + 'T00:00:00');
    if (isNaN(d)) return '-';
    var s = d.getDate() + ' ' + BULAN[d.getMonth()] + ' ' + d.getFullYear();
    return panjang ? HARI[d.getDay()] + ', ' + s : s;
  }
  function hariIni() { var d = new Date(); return new Date(d.getTime() - d.getTimezoneOffset() * 6e4).toISOString().slice(0, 10); }
  function umurBulan(lahir, sampai) {
    if (!lahir) return null;
    var a = new Date(lahir + 'T00:00:00'), b = sampai ? new Date(sampai + 'T00:00:00') : new Date();
    if (isNaN(a) || isNaN(b)) return null;
    var m = (b.getFullYear() - a.getFullYear()) * 12 + (b.getMonth() - a.getMonth());
    if (b.getDate() < a.getDate()) m--;
    return Math.max(0, m);
  }
  function umurTeks(bulan) {
    if (bulan == null) return 'usia belum diisi';
    if (bulan < 24) return bulan + ' bulan';
    var t = Math.floor(bulan / 12), s = bulan % 12;
    return t + ' tahun' + (s ? ' ' + s + ' bulan' : '');
  }
  function inisial(nama) {
    var p = String(nama || '?').trim().split(/\s+/);
    return ((p[0] || '?')[0] + (p.length > 1 ? p[p.length - 1][0] : '')).toUpperCase();
  }
  function selisihHari(iso) {
    var d = new Date(iso + 'T00:00:00'), n = new Date(hariIni() + 'T00:00:00');
    return Math.round((d - n) / 864e5);
  }

  /* ============================ state ============================ */
  var KEY = 'vaksinku.v1';
  var kosong = {
    versi: 1, profil: { nama: '', hp: '', jenisKelamin: '' },
    pasien: [], alamat: [], booking: [], riwayat: [], pertumbuhan: [],
    poin: 0, draft: null, ui: { pasienAktif: '' }
  };
  var S, storageOk = true;

  function baca() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return JSON.parse(JSON.stringify(kosong));
      var d = JSON.parse(raw);
      for (var k in kosong) if (!(k in d)) d[k] = JSON.parse(JSON.stringify(kosong[k]));
      return d;
    } catch (e) { storageOk = false; return JSON.parse(JSON.stringify(kosong)); }
  }
  function simpan() {
    try { localStorage.setItem(KEY, JSON.stringify(S)); }
    catch (e) { storageOk = false; }
  }
  S = baca();

  /* ============================ katalog ============================ */
  function vaksinById(id) {
    for (var i = 0; i < K.harga.length; i++) if (K.harga[i].id === id) return K.harga[i];
    return null;
  }
  function hargaVaksin(v, dokter) {
    var s = dokter === 'spesialis' ? v.spesialis : v.umum;
    return s ? angka(s) : 0;
  }
  function bracketDewasa(tahun) {
    for (var i = 0; i < K.jadwalDewasa.length; i++) {
      var b = K.jadwalDewasa[i];
      if (tahun >= b.minTahun && tahun <= b.maxTahun) return b;
    }
    return null;
  }

  /* ============================ riwayat & jadwal ============================ */
  function riwayatPasien(id) {
    return S.riwayat.filter(function (r) { return r.pasienId === id; })
      .sort(function (a, b) { return b.tanggal.localeCompare(a.tanggal); });
  }
  function sudah(pasienId, label) {
    return S.riwayat.some(function (r) { return r.pasienId === pasienId && r.label === label; });
  }
  function jadwalPasien(p) {
    var bln = umurBulan(p.tglLahir);
    if (bln == null) return null;
    var tahun = Math.floor(bln / 12);
    if (tahun >= 19) {
      var b = bracketDewasa(tahun);
      if (!b) return null;
      return {
        tipe: 'dewasa', judul: b.usia, catatan: K.catatanDewasa,
        langkah: [{
          usia: b.usia, jatuhTempo: true,
          items: b.items.map(function (it) {
            return { label: it.nama, ket: it.dosis, selesai: sudah(p.id, it.nama) };
          })
        }]
      };
    }
    return {
      tipe: 'anak', judul: 'Jadwal IDAI 2024', catatan: '',
      langkah: K.jadwalAnak.map(function (st) {
        return {
          usia: st.usia, badge: st.badge, usiaBulan: st.usiaBulan,
          jatuhTempo: st.usiaBulan <= bln,
          berikutnya: st.usiaBulan > bln,
          items: st.items.map(function (lb) {
            return { label: lb, selesai: sudah(p.id, lb) };
          })
        };
      })
    };
  }
  function ringkasJadwal(p) {
    var j = jadwalPasien(p);
    if (!j) return null;
    var total = 0, selesai = 0, belum = [];
    j.langkah.forEach(function (st) {
      if (!st.jatuhTempo) return;
      st.items.forEach(function (it) {
        total++;
        if (it.selesai) selesai++; else belum.push({ usia: st.usia, label: it.label });
      });
    });
    return { total: total, selesai: selesai, belum: belum, persen: total ? Math.round(selesai / total * 100) : 0, jadwal: j };
  }

  /* ============================ booking ============================ */
  function draft() {
    if (!S.draft) {
      S.draft = {
        layanan: '', klinikIdx: 0, alamatId: '', institusi: '', institusiAlamat: '',
        pasienIds: [], vaksinIds: [], dokter: 'umum', tanggal: '', jam: '', catatan: ''
      };
    }
    return S.draft;
  }
  function hitungBiaya(d) {
    var rincian = [], tanpaHarga = [], subtotal = 0;
    d.vaksinIds.forEach(function (id) {
      var v = vaksinById(id); if (!v) return;
      var hrg = hargaVaksin(v, d.dokter);
      if (hrg) { rincian.push({ nama: v.kategori + ' — ' + v.merk, harga: hrg }); subtotal += hrg; }
      else { tanpaHarga.push(v.kategori + ' — ' + v.merk); }
    });
    var jml = Math.max(1, d.pasienIds.length);
    return { rincian: rincian, tanpaHarga: tanpaHarga, perPasien: subtotal, jumlahPasien: jml, total: subtotal * jml };
  }
  function lokasiTeks(d) {
    if (d.layanan === 'klinik') { var kl = K.klinik[d.klinikIdx]; return kl ? kl[0] + ' — ' + kl[1] : ''; }
    if (d.layanan === 'homecare') {
      var a = S.alamat.filter(function (x) { return x.id === d.alamatId; })[0];
      return a ? a.label + ' — ' + a.alamat + ', ' + a.kecamatan : '';
    }
    if (d.layanan === 'corporate') return d.institusi + (d.institusiAlamat ? ' — ' + d.institusiAlamat : '');
    return '';
  }
  var LAYANAN_NAMA = { homecare: 'Home Care', klinik: 'On Site Klinik', corporate: 'On Site Corporate' };

  function validasiBooking(d) {
    var e = {};
    if (!d.layanan) e.layanan = 'Pilih jenis layanan.';
    if (d.layanan === 'homecare' && !d.alamatId) e.lokasi = 'Pilih atau tambahkan alamat vaksinasi.';
    if (d.layanan === 'klinik' && K.klinik[d.klinikIdx] == null) e.lokasi = 'Pilih klinik.';
    if (d.layanan === 'corporate' && !String(d.institusi).trim()) e.lokasi = 'Isi nama institusi/perusahaan.';
    if (!d.pasienIds.length) e.pasien = 'Pilih minimal satu pasien.';
    if (!d.vaksinIds.length) e.vaksin = 'Pilih minimal satu vaksin.';
    if (!d.tanggal) e.jadwal = 'Pilih tanggal vaksinasi.';
    else if (selisihHari(d.tanggal) < 0) e.jadwal = 'Tanggal tidak boleh di masa lalu.';
    else if (!d.jam) e.jadwal = 'Pilih jam vaksinasi.';
    if (!String(S.profil.nama).trim()) e.profil = 'Lengkapi nama pendaftar di Profil.';
    if (!String(S.profil.hp).trim()) e.profil = 'Lengkapi nomor HP pendaftar di Profil.';
    return e;
  }
  function buatBooking() {
    var d = draft(), b = hitungBiaya(d);
    var kode = 'VK-' + String(Date.now()).slice(-6);
    var rec = {
      id: uid(), kode: kode, dibuat: new Date().toISOString(), status: 'menunggu',
      layanan: d.layanan, lokasi: lokasiTeks(d), pasienIds: d.pasienIds.slice(),
      vaksinIds: d.vaksinIds.slice(), dokter: d.dokter, tanggal: d.tanggal, jam: d.jam,
      catatan: d.catatan, rincian: b.rincian, tanpaHarga: b.tanpaHarga,
      perPasien: b.perPasien, total: b.total,
      pendaftar: { nama: S.profil.nama, hp: S.profil.hp }
    };
    S.booking.unshift(rec);
    S.draft = null;
    simpan();
    return rec;
  }
  function namaPasien(id) {
    var p = S.pasien.filter(function (x) { return x.id === id; })[0];
    return p ? p.nama : '(pasien dihapus)';
  }
  function pesanWA(b) {
    var L = [];
    L.push('Halo VaksinKu, saya ingin reservasi vaksinasi.');
    L.push('');
    L.push('Kode: ' + b.kode);
    L.push('Pendaftar: ' + b.pendaftar.nama + ' (' + b.pendaftar.hp + ')');
    L.push('Layanan: ' + LAYANAN_NAMA[b.layanan]);
    L.push('Lokasi: ' + b.lokasi);
    L.push('Jadwal: ' + tgl(b.tanggal, true) + ', pukul ' + b.jam);
    L.push('Dokter: ' + (b.dokter === 'spesialis' ? 'Dokter Spesialis' : 'Dokter Umum'));
    L.push('');
    L.push('Pasien (' + b.pasienIds.length + '):');
    b.pasienIds.forEach(function (id, i) {
      var p = S.pasien.filter(function (x) { return x.id === id; })[0];
      L.push('  ' + (i + 1) + '. ' + namaPasien(id) + (p && p.tglLahir ? ' (' + umurTeks(umurBulan(p.tglLahir)) + ')' : ''));
    });
    L.push('');
    L.push('Vaksin:');
    b.rincian.forEach(function (r) { L.push('  - ' + r.nama + ' — ' + rp(r.harga)); });
    b.tanpaHarga.forEach(function (n) { L.push('  - ' + n + ' — harga dikonfirmasi'); });
    L.push('');
    L.push('Estimasi total: ' + rp(b.total) + ' (' + rp(b.perPasien) + ' x ' + b.pasienIds.length + ' pasien)');
    if (b.catatan) { L.push(''); L.push('Catatan: ' + b.catatan); }
    return L.join('\n');
  }
  function kirimWA(b) {
    window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(pesanWA(b)), '_blank');
  }

  /* ============================ shell ============================ */
  var route = { name: 'beranda', param: '' };
  var app = document.getElementById('app');

  function go(hash) { location.hash = '#/' + hash; }
  function bacaRoute() {
    var p = (location.hash || '#/beranda').replace(/^#\//, '').split('/');
    route = { name: p[0] || 'beranda', param: p[1] || '' };
  }
  function topbar(judul, sub, kembali, aksi) {
    return '<div class="topbar">' +
      (kembali ? '<button class="backbtn" data-act="go" data-arg="' + h(kembali) + '" aria-label="Kembali">' + ic('back', 20, 2.2) + '</button>' : '') +
      '<div class="grow"><h1>' + h(judul) + '</h1>' + (sub ? '<div class="sub">' + h(sub) + '</div>' : '') + '</div>' +
      (aksi || '') + '</div>';
  }
  function navbar(aktif) {
    var items = [['beranda', 'home', 'Beranda'], ['jadwal', 'calendar', 'Jadwal'], null,
      ['rekam', 'doc', 'Rekam Medis'], ['profil', 'user', 'Profil']];
    return '<nav class="navbar">' + items.map(function (it) {
      if (!it) return '<button class="navfab" data-act="go" data-arg="booking" aria-label="Booking vaksinasi">' + ic('plus', 24, 2.4) + '</button>';
      return '<button class="navitem' + (aktif === it[0] ? ' on' : '') + '" data-act="go" data-arg="' + it[0] + '">' +
        ic(it[1], 21) + '<span>' + it[2] + '</span></button>';
    }).join('') + '</nav>';
  }
  function toast(msg) {
    var el = document.createElement('div');
    el.className = 'toast';
    el.innerHTML = '<div>' + h(msg) + '</div>';
    document.querySelector('.device').appendChild(el);
    requestAnimationFrame(function () { el.firstChild.classList.add('on'); });
    setTimeout(function () {
      el.firstChild.classList.remove('on');
      setTimeout(function () { el.remove(); }, 260);
    }, 2400);
  }
  function empty(icon, judul, teks, tombol) {
    return '<div class="empty"><div class="icon-sq">' + ic(icon, 26) + '</div>' +
      '<div class="disp" style="font-size:16px;font-weight:800;">' + h(judul) + '</div>' +
      '<div class="small muted" style="margin-top:6px;">' + h(teks) + '</div>' +
      (tombol ? '<div style="margin-top:16px;">' + tombol + '</div>' : '') + '</div>';
  }

  /* ============================ layar: beranda ============================ */
  function scBeranda() {
    var belumSiap = !S.profil.nama || !S.pasien.length;
    var aktif = S.booking.filter(function (b) { return b.status === 'menunggu'; });
    var body = '';

    body += '<div class="hero">' +
      '<div class="row mid g10"><img src="' + K.logoMark + '" alt="VaksinKu" style="height:22px;width:auto;">' +
      '<div class="grow"></div>' +
      '<span class="chip amber">' + ic('coin', 14) + ' ' + S.poin + ' Poin</span></div>' +
      '<div style="height:14px;"></div>' +
      '<div class="disp" style="font-size:18px;font-weight:800;">Halo' + (S.profil.nama ? ', ' + h(S.profil.nama.split(' ')[0]) : '') + '</div>' +
      '<div class="small" style="color:var(--ink-2);margin-top:2px;">' + h(K.brand.tagline) + '</div>' +
      '</div>';

    body += '<div class="pad stack g14">';

    if (belumSiap) {
      body += '<div class="card tint stack g10">' +
        '<div class="row mid g10"><div class="icon-sq" style="background:#fff;">' + ic('user', 19) + '</div>' +
        '<div class="grow"><div style="font-weight:700;">Lengkapi data dulu, yuk</div>' +
        '<div class="tiny muted">' + (!S.profil.nama ? 'Isi nama & nomor HP pendaftar' : 'Tambahkan anggota keluarga yang akan divaksin') + '</div></div></div>' +
        '<button class="btn primary sm" data-act="go" data-arg="' + (!S.profil.nama ? 'profil' : 'pasien') + '">' +
        (!S.profil.nama ? 'Lengkapi Profil' : 'Tambah Pasien') + '</button></div>';
    }

    if (aktif.length) {
      aktif.slice(0, 2).forEach(function (b) {
        var sisa = selisihHari(b.tanggal);
        body += '<div class="card stack g12 tap" data-act="go" data-arg="booking-detail/' + b.id + '">' +
          '<div class="row mid g8"><span class="chip mag">Menunggu konfirmasi</span><div class="grow"></div>' +
          '<span class="tiny muted">' + h(b.kode) + '</span></div>' +
          '<div><div style="font-weight:700;font-size:14.5px;">' + h(b.rincian.map(function (r) { return r.nama.split(' — ')[0]; }).join(', ') || 'Vaksinasi') + '</div>' +
          '<div class="small muted">' + h(b.pasienIds.map(namaPasien).join(', ')) + '</div></div>' +
          '<div class="row g14 small" style="color:var(--ink-2);">' +
          '<span class="row mid g6">' + ic('calendar', 15) + tgl(b.tanggal) + ' · ' + h(b.jam) + '</span>' +
          '<span class="row mid g6">' + ic('house', 15) + h(LAYANAN_NAMA[b.layanan]) + '</span></div>' +
          (sisa >= 0 ? '<div class="chip teal">' + (sisa === 0 ? 'Hari ini' : sisa + ' hari lagi') + '</div>' : '') +
          '</div>';
      });
    } else {
      body += '<div class="card stack g12 center">' +
        '<div class="icon-sq mag" style="margin:0 auto;">' + ic('syringe', 20) + '</div>' +
        '<div><div style="font-weight:700;">Belum ada reservasi aktif</div>' +
        '<div class="small muted" style="margin-top:4px;">Atur jadwal vaksinasi keluarga Anda sekarang.</div></div>' +
        '<button class="btn primary" data-act="go" data-arg="booking">' + ic('plus', 17, 2.2) + ' Booking Vaksinasi</button></div>';
    }

    // pengingat dari jadwal pasien
    var pengingat = [];
    S.pasien.forEach(function (p) {
      var r = ringkasJadwal(p);
      if (r && r.belum.length) pengingat.push({ p: p, jml: r.belum.length, contoh: r.belum[0].label });
    });
    if (pengingat.length) {
      body += '<div class="card warn stack g10">' +
        '<div class="row mid g10"><div class="icon-sq amber" style="background:#fff;">' + ic('bell', 19) + '</div>' +
        '<div class="grow"><div style="font-weight:700;">Vaksin yang belum lengkap</div>' +
        '<div class="tiny" style="color:var(--amber);">Berdasarkan usia dan riwayat masing-masing pasien</div></div></div>' +
        pengingat.slice(0, 3).map(function (x) {
          return '<button class="rowlink" data-act="pasien-jadwal" data-arg="' + x.p.id + '">' +
            '<div class="avatar" style="width:32px;height:32px;font-size:12px;">' + h(inisial(x.p.nama)) + '</div>' +
            '<div class="grow"><div class="small" style="font-weight:700;">' + h(x.p.nama) + '</div>' +
            '<div class="tiny muted">' + x.jml + ' vaksin tertunda · ' + h(x.contoh) + '</div></div>' +
            '<span style="color:var(--ink-4);">' + ic('chevron', 15) + '</span></button>';
        }).join('') + '</div>';
    }

    body += '<div class="card row g8">' +
      pintasan('tag', 'Daftar Harga', 'harga') +
      pintasan('calendar', 'Jadwal Vaksin', 'jadwal') +
      pintasan('globe', 'Internasional', 'internasional') +
      '</div>';

    body += '<div class="card stack g12">' +
      '<div class="row mid"><div class="sect-title">Pilih cara vaksinasi</div><div class="grow"></div><span class="chip teal">3 layanan</span></div>' +
      '<div class="row g8">' +
      layananPintasan('house', 'Home Care', 'homecare') +
      layananPintasan('pin', 'On Site Klinik', 'klinik') +
      layananPintasan('building', 'On Site Corporate', 'corporate') +
      '</div>' +
      '<div class="divider"></div>' +
      '<div class="row wrap g6 mid"><span class="tiny muted" style="font-weight:600;">Sudah termasuk:</span>' +
      K.termasuk.map(function (t) { return '<span class="chip teal" style="padding:4px 9px;font-size:10.5px;">' + h(t) + '</span>'; }).join('') +
      '</div></div>';

    var promo = K.hargaInternasional.filter(function (x) { return x.coret; })[0];
    if (promo) {
      body += '<div class="card tap stack g6" style="background:linear-gradient(135deg,var(--teal-dark),var(--magenta-dark));border-color:transparent;color:#fff;" data-act="go" data-arg="internasional">' +
        '<div class="row mid g8"><span class="chip" style="background:#fff;color:var(--magenta-dark);padding:3px 10px;font-size:10px;">PROMO</span>' +
        '<span class="tiny" style="opacity:.85;">Haji &amp; Umrah</span></div>' +
        '<div class="disp" style="font-size:16px;font-weight:800;">Paket ' + h(promo.nama) + '</div>' +
        '<div class="row mid g10" style="align-items:baseline;"><span class="disp" style="font-size:21px;font-weight:800;">' + rp(angka(promo.harga)) + '</span>' +
        '<span class="small" style="opacity:.75;text-decoration:line-through;">' + rp(angka(promo.coret)) + '</span></div></div>';
    }

    body += '<button class="card rowlink" data-act="go" data-arg="tentang" style="padding:16px;">' +
      '<div class="icon-sq">' + ic('pin', 19) + '</div>' +
      '<div class="grow"><div style="font-weight:700;font-size:13.5px;">' + K.klinik.length + ' klinik di Tanjungpinang</div>' +
      '<div class="tiny muted">Alamat, dokter, dan alur reservasi</div></div>' +
      '<span style="color:var(--ink-4);">' + ic('chevron', 16) + '</span></button>';

    body += '</div>';
    return { body: body, nav: 'beranda' };
  }
  function pintasan(icon, label, target) {
    return '<button class="stack mid g8 tap" style="flex:1;background:none;border:0;padding:4px 0;cursor:pointer;" data-act="go" data-arg="' + target + '">' +
      '<div class="icon-sq" style="width:44px;height:44px;border-radius:13px;">' + ic(icon, 20) + '</div>' +
      '<span class="tiny" style="font-weight:700;text-align:center;line-height:1.3;">' + h(label) + '</span></button>';
  }
  function layananPintasan(icon, label, jenis) {
    return '<button class="stack mid g8 tap" style="flex:1;background:none;border:0;padding:4px 0;cursor:pointer;" data-act="mulai-booking" data-arg="' + jenis + '">' +
      '<div class="icon-sq mag" style="width:44px;height:44px;border-radius:13px;">' + ic(icon, 20) + '</div>' +
      '<span class="tiny" style="font-weight:700;text-align:center;line-height:1.3;">' + h(label) + '</span></button>';
  }

  /* ============================ layar: booking ============================ */
  var errB = {};
  function scBooking() {
    var d = draft(), b = hitungBiaya(d);
    var body = topbar('Booking Vaksinasi', 'Isi data, kirim ke CS untuk dikonfirmasi', 'beranda');
    body += '<div class="pad stack g18">';

    if (errB.profil) body += '<div class="card" style="background:var(--danger-tint);border-color:transparent;"><div class="small" style="color:var(--danger);font-weight:700;">' + h(errB.profil) + '</div>' +
      '<button class="btn sm outline" style="margin-top:10px;" data-act="go" data-arg="profil">Buka Profil</button></div>';

    // 1 layanan
    body += '<div class="stack g8"><label class="lbl">1. Jenis layanan<span class="req">*</span></label>' +
      '<div class="row g8">' +
      ['homecare|house|Home Care', 'klinik|pin|On Site Klinik', 'corporate|building|On Site Corporate'].map(function (s) {
        var p = s.split('|');
        return '<button class="opt' + (d.layanan === p[0] ? ' on' : '') + '" data-act="set-layanan" data-arg="' + p[0] + '">' + ic(p[1], 20) + '<span>' + p[2] + '</span></button>';
      }).join('') + '</div>' +
      (errB.layanan ? '<div class="errmsg">' + h(errB.layanan) + '</div>' : '') + '</div>';

    // 2 lokasi
    body += '<div class="stack g8"><label class="lbl">2. Lokasi vaksinasi<span class="req">*</span></label>';
    if (!d.layanan) {
      body += '<div class="card flat small muted" style="border-style:dashed;">Pilih jenis layanan dulu untuk menentukan lokasi.</div>';
    } else {
      if (d.layanan === 'klinik') {
        body += K.klinik.map(function (kl, i) {
          return '<button class="checkrow' + (d.klinikIdx === i ? ' on' : '') + '" data-act="set-klinik" data-arg="' + i + '">' +
            '<div class="box">' + (d.klinikIdx === i ? ic('check', 14, 3) : '') + '</div>' +
            '<div class="grow"><div class="small" style="font-weight:700;">' + h(kl[0]) + '</div>' +
            '<div class="tiny muted">' + h(kl[1]) + '</div></div></button>';
        }).join('');
      } else if (d.layanan === 'homecare') {
        body += S.alamat.map(function (a) {
          return '<button class="checkrow' + (d.alamatId === a.id ? ' on' : '') + '" data-act="set-alamat" data-arg="' + a.id + '">' +
            '<div class="box">' + (d.alamatId === a.id ? ic('check', 14, 3) : '') + '</div>' +
            '<div class="grow"><div class="small" style="font-weight:700;">' + h(a.label) + '</div>' +
            '<div class="tiny muted">' + h(a.alamat + ', ' + a.kecamatan) + '</div></div></button>';
        }).join('');
        body += '<button class="btn outline sm" data-act="go" data-arg="alamat-form">' + ic('plus', 15, 2.2) + ' Tambah alamat</button>';
      } else {
        body += '<input class="input" data-field="institusi" placeholder="Nama institusi / perusahaan" value="' + h(d.institusi) + '" style="margin-bottom:8px;">' +
          '<input class="input" data-field="institusiAlamat" placeholder="Alamat lokasi kegiatan" value="' + h(d.institusiAlamat) + '">' +
          '<div class="hint" style="margin-top:8px;">Untuk vaksinasi massal, jumlah peserta dan jadwal akan dikonfirmasi tim kami.</div>';
      }
    }
    body += (errB.lokasi ? '<div class="errmsg">' + h(errB.lokasi) + '</div>' : '') + '</div>';

    // 3 pasien
    body += '<div class="stack g8"><label class="lbl">3. Pasien yang divaksin<span class="req">*</span></label>';
    if (!S.pasien.length) {
      body += '<div class="card flat stack g10" style="border-style:dashed;">' +
        '<div class="small muted">Belum ada data pasien.</div>' +
        '<button class="btn outline sm" data-act="go" data-arg="pasien-form">' + ic('plus', 15, 2.2) + ' Tambah pasien</button></div>';
    } else {
      body += S.pasien.map(function (p) {
        var on = d.pasienIds.indexOf(p.id) >= 0;
        return '<button class="checkrow' + (on ? ' on' : '') + '" data-act="toggle-pasien" data-arg="' + p.id + '">' +
          '<div class="box">' + (on ? ic('check', 14, 3) : '') + '</div>' +
          '<div class="avatar" style="width:32px;height:32px;font-size:12px;">' + h(inisial(p.nama)) + '</div>' +
          '<div class="grow"><div class="small" style="font-weight:700;">' + h(p.nama) + '</div>' +
          '<div class="tiny muted">' + h(umurTeks(umurBulan(p.tglLahir))) + (p.hubungan ? ' · ' + h(p.hubungan) : '') + '</div></div></button>';
      }).join('');
      body += '<button class="btn outline sm" data-act="go" data-arg="pasien-form">' + ic('plus', 15, 2.2) + ' Tambah pasien</button>';
    }
    body += (errB.pasien ? '<div class="errmsg">' + h(errB.pasien) + '</div>' : '') + '</div>';

    // 4 dokter
    body += '<div class="stack g8"><label class="lbl">4. Pilihan dokter<span class="req">*</span></label>' +
      '<div class="hint">Harga vaksin menyesuaikan pilihan dokter. Semua vaksinator bersertifikat.</div>' +
      '<div class="row g8">' +
      '<button class="opt' + (d.dokter === 'umum' ? ' on' : '') + '" data-act="set-dokter" data-arg="umum"><span>Dokter Umum</span></button>' +
      '<button class="opt' + (d.dokter === 'spesialis' ? ' on' : '') + '" data-act="set-dokter" data-arg="spesialis"><span>Dokter Spesialis</span></button>' +
      '</div></div>';

    // 5 vaksin
    body += '<div class="stack g8"><label class="lbl">5. Vaksin yang dipilih<span class="req">*</span></label>' +
      '<div class="hint">Harga berlaku per pasien. Tim kami akan menyesuaikan jika hasil skrining berbeda.</div>' +
      '<button class="btn outline" data-act="buka-vaksin">' + ic('search', 16) + ' Pilih vaksin dari daftar harga</button>';
    if (d.vaksinIds.length) {
      body += '<div class="stack g8" style="margin-top:4px;">' + d.vaksinIds.map(function (id) {
        var v = vaksinById(id); if (!v) return '';
        var hrg = hargaVaksin(v, d.dokter);
        return '<div class="row mid g10 card flat" style="padding:11px 13px;">' +
          '<div class="grow"><div class="small" style="font-weight:700;">' + h(v.kategori) + '</div>' +
          '<div class="tiny muted">' + h(v.sediaan === v.merk ? v.merk : v.sediaan + ' · ' + v.merk) + '</div></div>' +
          '<div class="disp nowrap" style="font-weight:800;color:var(--magenta-dark);">' + (hrg ? rp(hrg) : 'Hubungi CS') + '</div>' +
          '<button class="linkbtn" data-act="hapus-vaksin" data-arg="' + id + '" aria-label="Hapus" style="color:var(--ink-4);">' + ic('trash', 16) + '</button></div>';
      }).join('') + '</div>';
    }
    body += (errB.vaksin ? '<div class="errmsg">' + h(errB.vaksin) + '</div>' : '') + '</div>';

    // 6 jadwal
    var min = hariIni();
    body += '<div class="stack g8"><label class="lbl">6. Jadwal vaksinasi<span class="req">*</span></label>' +
      '<input type="date" class="input" data-field="tanggal" min="' + min + '" value="' + h(d.tanggal) + '">' +
      '<div class="row wrap g8" style="margin-top:4px;">' + jamSlot(d) + '</div>' +
      '<div class="hint" style="margin-top:6px;">Ketersediaan slot final dikonfirmasi oleh tim CS.</div>' +
      (errB.jadwal ? '<div class="errmsg">' + h(errB.jadwal) + '</div>' : '') + '</div>';

    // 7 catatan
    body += '<div class="stack g8"><label class="lbl">7. Catatan (opsional)</label>' +
      '<textarea class="input" data-field="catatan" placeholder="Riwayat alergi, kondisi khusus, patokan lokasi...">' + h(d.catatan) + '</textarea></div>';

    // ringkasan
    body += '<div class="card tint stack g10">' +
      '<div class="row mid g8">' + ic('checkc', 16) + '<span class="small" style="font-weight:700;color:var(--teal-dark);">Price list terbuka, tanpa biaya tersembunyi</span></div>';
    if (b.rincian.length) {
      body += b.rincian.map(function (r) {
        return '<div class="row between small"><span style="color:var(--ink-2);">' + h(r.nama) + '</span><span>' + rp(r.harga) + '</span></div>';
      }).join('');
      body += '<div class="row between small"><span style="color:var(--ink-2);">Jasa dokter, tindakan &amp; BHP</span><span style="color:var(--teal-dark);font-weight:700;">Termasuk</span></div>';
      body += '<div class="divider"></div>';
      body += '<div class="row between small"><span style="color:var(--ink-2);">Per pasien</span><span>' + rp(b.perPasien) + '</span></div>';
      body += '<div class="row between small"><span style="color:var(--ink-2);">Jumlah pasien</span><span>' + b.jumlahPasien + ' orang</span></div>';
    } else {
      body += '<div class="small muted">Pilih vaksin untuk melihat estimasi biaya.</div>';
    }
    if (b.tanpaHarga.length) {
      body += '<div class="tiny" style="color:var(--amber);">' + h(b.tanpaHarga.join(', ')) + ': harga dikonfirmasi CS, belum masuk total.</div>';
    }
    body += '<div class="divider"></div>' +
      '<div class="row between mid"><span class="disp" style="font-weight:800;">Total estimasi</span>' +
      '<span class="disp" style="font-weight:800;font-size:16px;color:var(--magenta-dark);">' + rp(b.total) + '</span></div>' +
      '<div class="tiny muted">Biaya kunjungan Home Care / On Site dikonfirmasi saat reservasi.</div></div>';

    body += '</div>';

    var foot = '<div class="sticky-foot">' +
      '<div class="stack" style="gap:1px;"><span class="tiny muted">Total estimasi</span>' +
      '<span class="disp" style="font-weight:800;font-size:15px;color:var(--magenta-dark);">' + rp(b.total) + '</span></div>' +
      '<button class="btn primary grow" data-act="kirim-booking">Buat Reservasi</button></div>';

    return { body: body, foot: foot };
  }
  function jamSlot(d) {
    var out = '', jams = ['08:00', '09:00', '10:00', '11:00', '13:00', '14:00', '15:00', '16:00'];
    var now = new Date(), sekarang = now.getHours() * 60 + now.getMinutes();
    jams.forEach(function (j) {
      var lewat = d.tanggal === hariIni() && (parseInt(j, 10) * 60) <= sekarang;
      out += '<button class="pill' + (d.jam === j ? ' on' : '') + '" data-act="set-jam" data-arg="' + j + '"' + (lewat ? ' disabled' : '') + '>' + j + '</button>';
    });
    return out;
  }

  /* --------- sheet pilih vaksin --------- */
  var cariVaksin = '';
  function sheetVaksin() {
    var d = draft();
    var q = cariVaksin.toLowerCase();
    var list = K.harga.filter(function (v) {
      return !q || (v.kategori + ' ' + v.sediaan + ' ' + v.merk).toLowerCase().indexOf(q) >= 0;
    });
    var html = '<div class="sheet" data-act="tutup-sheet"><div data-stop="1">' +
      '<div class="row mid between" style="margin-bottom:12px;"><div class="sect-title">Pilih vaksin</div>' +
      '<button class="linkbtn" data-act="tutup-sheet">Selesai</button></div>' +
      '<input class="input" id="cari-vaksin" placeholder="Cari vaksin, contoh: influenza" value="' + h(cariVaksin) + '" style="margin-bottom:12px;">' +
      '<div class="stack g8">';
    if (!list.length) html += '<div class="small muted center" style="padding:20px 0;">Vaksin tidak ditemukan.</div>';
    list.forEach(function (v) {
      var on = d.vaksinIds.indexOf(v.id) >= 0;
      var hrg = hargaVaksin(v, d.dokter);
      html += '<button class="checkrow' + (on ? ' on' : '') + '" data-act="toggle-vaksin" data-arg="' + v.id + '">' +
        '<div class="box">' + (on ? ic('check', 14, 3) : '') + '</div>' +
        '<div class="grow"><div class="small" style="font-weight:700;">' + h(v.kategori) + '</div>' +
        '<div class="tiny muted">' + h(v.sediaan === v.merk ? v.merk : v.sediaan + ' · ' + v.merk) + '</div></div>' +
        '<div class="disp nowrap small" style="font-weight:800;color:var(--magenta-dark);">' + (hrg ? rp(hrg) : 'Hubungi CS') + '</div></button>';
    });
    return html + '</div></div></div>';
  }

  /* ============================ layar: detail booking ============================ */
  function scBookingDetail(id) {
    var b = S.booking.filter(function (x) { return x.id === id; })[0];
    if (!b) return { body: topbar('Reservasi', '', 'beranda') + empty('doc', 'Reservasi tidak ditemukan', 'Data mungkin sudah dihapus.') };
    var st = { menunggu: ['mag', 'Menunggu konfirmasi'], selesai: ['green', 'Selesai'], batal: ['grey', 'Dibatalkan'] }[b.status];
    var body = topbar('Detail Reservasi', b.kode, 'beranda');
    body += '<div class="pad stack g14">';
    body += '<div class="card stack g12">' +
      '<div class="row mid"><span class="chip ' + st[0] + '">' + st[1] + '</span><div class="grow"></div>' +
      '<span class="tiny muted">' + tgl(b.dibuat.slice(0, 10)) + '</span></div>' +
      baris('calendar', 'Jadwal', tgl(b.tanggal, true) + ' · pukul ' + b.jam) +
      baris('house', 'Layanan', LAYANAN_NAMA[b.layanan]) +
      baris('pin', 'Lokasi', b.lokasi || '-') +
      baris('user', 'Dokter', b.dokter === 'spesialis' ? 'Dokter Spesialis' : 'Dokter Umum') +
      baris('family', 'Pasien', b.pasienIds.map(namaPasien).join(', ')) +
      (b.catatan ? baris('doc', 'Catatan', b.catatan) : '') +
      '</div>';

    body += '<div class="card stack g10"><div class="sect-title">Rincian biaya</div>' +
      b.rincian.map(function (r) {
        return '<div class="row between small"><span style="color:var(--ink-2);">' + h(r.nama) + '</span><span>' + rp(r.harga) + '</span></div>';
      }).join('') +
      (b.tanpaHarga.length ? '<div class="tiny" style="color:var(--amber);">' + h(b.tanpaHarga.join(', ')) + ': harga dikonfirmasi CS.</div>' : '') +
      '<div class="divider"></div>' +
      '<div class="row between small"><span style="color:var(--ink-2);">' + rp(b.perPasien) + ' × ' + b.pasienIds.length + ' pasien</span><span></span></div>' +
      '<div class="row between mid"><span class="disp" style="font-weight:800;">Total estimasi</span>' +
      '<span class="disp" style="font-weight:800;font-size:16px;color:var(--magenta-dark);">' + rp(b.total) + '</span></div></div>';

    body += '<div class="card warn stack g8"><div class="row mid g8">' + ic('info', 16) + '<span class="small" style="font-weight:700;color:var(--amber);">Reservasi belum terjadwal otomatis</span></div>' +
      '<div class="tiny" style="color:#8A6A21;line-height:1.6;">Aplikasi ini menyimpan data di perangkat Anda. Kirim ringkasan ke WhatsApp CS ' + h(K.brand.callCenter) + ' agar jadwal dikonfirmasi petugas.</div></div>';

    if (b.status === 'menunggu') {
      body += '<button class="btn teal" data-act="wa-booking" data-arg="' + b.id + '">' + ic('wa', 17) + ' Kirim ke WhatsApp CS</button>';
      body += '<button class="btn outline" data-act="selesai-booking" data-arg="' + b.id + '">' + ic('checkc', 16) + ' Tandai vaksinasi selesai</button>';
      body += '<button class="btn danger" data-act="batal-booking" data-arg="' + b.id + '">Batalkan reservasi</button>';
    } else if (b.status === 'selesai') {
      body += '<div class="card tint small" style="color:var(--teal-dark);">Vaksin dari reservasi ini sudah tercatat di Rekam Medis pasien.</div>';
      body += '<button class="btn outline" data-act="go" data-arg="rekam">Lihat rekam medis</button>';
    }
    body += '<button class="btn ghost" data-act="hapus-booking" data-arg="' + b.id + '">Hapus dari daftar</button>';
    body += '</div>';
    return { body: body };
  }
  function baris(icon, label, isi) {
    return '<div class="row g12" style="align-items:flex-start;"><div class="icon-sq" style="width:32px;height:32px;border-radius:9px;">' + ic(icon, 16) + '</div>' +
      '<div class="grow"><div class="tiny muted">' + h(label) + '</div>' +
      '<div class="small" style="font-weight:600;line-height:1.5;">' + h(isi) + '</div></div></div>';
  }

  /* ============================ layar: jadwal ============================ */
  function pasienAktif() {
    var id = S.ui.pasienAktif;
    var p = S.pasien.filter(function (x) { return x.id === id; })[0];
    return p || S.pasien[0] || null;
  }
  function scJadwal() {
    var body = topbar('Jadwal Vaksin', 'Sesuai usia & riwayat pasien');
    var p = pasienAktif();
    if (!p) {
      body += empty('family', 'Belum ada pasien', 'Tambahkan anggota keluarga untuk melihat jadwal vaksin yang sesuai usianya.',
        '<button class="btn primary" data-act="go" data-arg="pasien-form">Tambah pasien</button>');
      body += '<div class="pad">' + kartuJadwalUmum() + '</div>';
      return { body: body, nav: 'jadwal' };
    }
    body += '<div class="pad stack g14">' + pilihPasien(p);
    var r = ringkasJadwal(p);
    if (!r) {
      body += '<div class="card small muted">Tanggal lahir pasien belum diisi, jadi jadwal belum bisa dihitung. ' +
        '<button class="linkbtn" data-act="go" data-arg="pasien-form/' + p.id + '">Lengkapi data pasien</button></div>';
    } else {
      body += '<div class="card stack g10">' +
        '<div class="row mid"><div><div class="sect-title">Kelengkapan sesuai usia</div>' +
        '<div class="tiny muted">' + h(r.jadwal.tipe === 'anak' ? 'Jadwal IDAI 2024' : 'Rekomendasi PAPDI 2025 · ' + r.jadwal.judul) + '</div></div>' +
        '<div class="grow"></div><div class="disp" style="font-size:20px;font-weight:800;color:var(--teal-dark);">' + r.persen + '%</div></div>' +
        '<div class="bar"><i style="width:' + r.persen + '%"></i></div>' +
        '<div class="tiny muted">' + r.selesai + ' dari ' + r.total + ' vaksin yang sudah jatuh tempo telah dicatat.</div></div>';

      body += '<div class="card stack g12"><div class="sect-title">Ceklis vaksin</div>' +
        '<div class="tiny muted" style="margin-top:-6px;">Ketuk item untuk menandai sudah divaksin.</div>';
      r.jadwal.langkah.forEach(function (st, i) {
        var last = i === r.jadwal.langkah.length - 1;
        body += '<div class="timeline">' +
          (last ? '' : '<div class="lnk"></div>') +
          '<div class="dot' + (st.jatuhTempo ? (st.items.every(function (x) { return x.selesai; }) ? ' done' : ' due') : '') + '"></div>' +
          '<div class="row mid g8" style="margin-bottom:6px;"><span class="disp" style="font-weight:800;font-size:13.5px;">' + h(st.usia) + '</span>' +
          (st.badge ? '<span class="chip mag" style="padding:2px 8px;font-size:9.5px;">' + h(st.badge) + '</span>' : '') +
          (st.berikutnya ? '<span class="chip grey" style="padding:2px 8px;font-size:9.5px;">akan datang</span>' : '') + '</div>' +
          '<div class="stack g6" style="padding-bottom:14px;">' +
          st.items.map(function (it) {
            return '<button class="checkrow' + (it.selesai ? ' done' : '') + '" style="padding:9px 11px;" data-act="toggle-riwayat" data-arg="' + p.id + '|' + encodeURIComponent(it.label) + '">' +
              '<div class="box" style="width:19px;height:19px;border-radius:6px;">' + (it.selesai ? ic('check', 12, 3) : '') + '</div>' +
              '<div class="grow"><span class="small" style="font-weight:600;">' + h(it.label) + '</span>' +
              (it.ket ? '<div class="tiny muted">' + h(it.ket) + '</div>' : '') + '</div></button>';
          }).join('') + '</div></div>';
      });
      body += '</div>';
      if (r.jadwal.catatan) body += '<div class="card warn tiny" style="color:#8A6A21;line-height:1.6;">' + h(r.jadwal.catatan) + '</div>';
    }
    body += kartuJadwalUmum() + '</div>';
    return { body: body, nav: 'jadwal' };
  }
  function pilihPasien(aktif) {
    return '<div class="tabs">' + S.pasien.map(function (p) {
      return '<button class="pill' + (p.id === aktif.id ? ' on' : '') + '" data-act="pilih-pasien" data-arg="' + p.id + '">' + h(p.nama.split(' ')[0]) + '</button>';
    }).join('') + '<button class="pill" data-act="go" data-arg="pasien-form">+ Pasien</button></div>';
  }
  function kartuJadwalUmum() {
    return '<div class="card stack g12"><div class="sect-title">Jadwal rujukan lain</div>' +
      '<button class="rowlink" data-act="go" data-arg="jadwal-info/pranikah"><div class="icon-sq mag">' + ic('family', 18) + '</div>' +
      '<div class="grow"><div class="small" style="font-weight:700;">Vaksin Pranikah</div><div class="tiny muted">HPV, MMR, Tetanus &amp; jadwalnya</div></div>' + ic('chevron', 15) + '</button>' +
      '<div class="divider"></div>' +
      '<button class="rowlink" data-act="go" data-arg="jadwal-info/lansia"><div class="icon-sq mag">' + ic('shield', 18) + '</div>' +
      '<div class="grow"><div class="small" style="font-weight:700;">Vaksin Lansia</div><div class="tiny muted">50 tahun ke atas</div></div>' + ic('chevron', 15) + '</button>' +
      '<div class="divider"></div>' +
      '<button class="rowlink" data-act="go" data-arg="internasional"><div class="icon-sq mag">' + ic('globe', 18) + '</div>' +
      '<div class="grow"><div class="small" style="font-weight:700;">Vaksin Internasional</div><div class="tiny muted">Haji, umrah, studi &amp; e-ICV</div></div>' + ic('chevron', 15) + '</button></div>';
  }
  function scJadwalInfo(jenis) {
    var body, isi = '';
    if (jenis === 'pranikah') {
      body = topbar('Vaksin Pranikah', 'Persiapan sebelum menikah', 'jadwal');
      isi += '<div class="card stack g10"><div class="sect-title">Vaksin yang dianjurkan</div>' +
        K.pranikahVaksin.map(function (v) {
          return '<div class="row g12" style="align-items:flex-start;"><div class="icon-sq mag" style="width:32px;height:32px;border-radius:9px;">' + ic('syringe', 16) + '</div>' +
            '<div class="grow"><div class="small" style="font-weight:700;">' + h(v[0]) + '</div>' +
            '<div class="tiny muted">' + h(v[1] + ' · ' + v[2]) + '</div></div></div>';
        }).join('') + '</div>';
      isi += '<div class="card stack g10"><div class="sect-title">Jadwal pemberian</div>' +
        '<div class="tiny muted" style="margin-top:-6px;">Dihitung mundur dari tanggal pernikahan.</div>' +
        K.pranikahWaktu.map(function (w) {
          return '<div class="row g12" style="align-items:flex-start;"><span class="chip mag" style="width:84px;justify-content:center;">' + h(w[0]) + '</span>' +
            '<div class="grow small" style="color:var(--ink-2);">' + w[1].map(h).join('<br>') + '</div></div>';
        }).join('') + '</div>';
    } else {
      body = topbar('Vaksin Lansia', '50 tahun ke atas', 'jadwal');
      isi += K.lansia.map(function (v) {
        return '<div class="card stack g8"><div class="row mid g10">' + ic('checkc', 18) + '<span style="font-weight:700;">' + h(v[0]) + '</span></div>' +
          '<span class="chip teal">' + h(v[1]) + '</span>' +
          '<div class="small" style="color:var(--ink-2);line-height:1.6;">' + h(v[2]) + '</div></div>';
      }).join('');
    }
    isi += '<button class="btn primary" data-act="go" data-arg="booking">' + ic('plus', 16, 2.2) + ' Booking vaksinasi</button>';
    return { body: body + '<div class="pad stack g14">' + isi + '</div>' };
  }

  /* ============================ layar: rekam medis ============================ */
  function scRekam() {
    var body = topbar('Rekam Medis', 'Riwayat & tumbuh kembang');
    var p = pasienAktif();
    if (!p) {
      body += empty('doc', 'Belum ada rekam medis', 'Tambahkan pasien lalu catat vaksinasi dan pertumbuhannya di sini.',
        '<button class="btn primary" data-act="go" data-arg="pasien-form">Tambah pasien</button>');
      return { body: body, nav: 'rekam' };
    }
    var riw = riwayatPasien(p.id), r = ringkasJadwal(p);
    var tumbuh = S.pertumbuhan.filter(function (x) { return x.pasienId === p.id; })
      .sort(function (a, b) { return a.tanggal.localeCompare(b.tanggal); });

    body += '<div class="pad stack g14">' + pilihPasien(p);

    body += '<div class="card stack g12">' +
      '<div class="row mid g12"><div class="avatar" style="width:46px;height:46px;font-size:15px;">' + h(inisial(p.nama)) + '</div>' +
      '<div class="grow"><div style="font-weight:800;font-size:15px;">' + h(p.nama) + '</div>' +
      '<div class="tiny muted">' + h(umurTeks(umurBulan(p.tglLahir))) + (p.tglLahir ? ' · lahir ' + tgl(p.tglLahir) : '') + '</div></div>' +
      '<button class="linkbtn" data-act="go" data-arg="pasien-form/' + p.id + '">' + ic('edit', 17) + '</button></div>' +
      (r ? '<div class="divider"></div><div class="row between mid"><span class="small muted">Kelengkapan sesuai usia</span>' +
        '<span class="chip teal">' + r.selesai + '/' + r.total + ' · ' + r.persen + '%</span></div>' : '') +
      '</div>';

    body += '<div class="card stack g10"><div class="row mid"><div class="sect-title">Riwayat vaksinasi</div>' +
      '<div class="grow"></div><span class="chip grey">' + riw.length + '</span></div>';
    if (!riw.length) {
      body += '<div class="small muted">Belum ada catatan. Tandai vaksin di halaman Jadwal, atau selesaikan reservasi untuk mencatat otomatis.</div>' +
        '<button class="btn outline sm" data-act="go" data-arg="jadwal">Buka jadwal vaksin</button>';
    } else {
      body += riw.map(function (x) {
        return '<div class="row g12" style="align-items:flex-start;padding:8px 0;border-top:1px solid var(--line);">' +
          '<div class="icon-sq" style="width:32px;height:32px;border-radius:9px;background:var(--green-tint);color:var(--green);">' + ic('checkc', 16) + '</div>' +
          '<div class="grow"><div class="small" style="font-weight:700;">' + h(x.label) + '</div>' +
          '<div class="tiny muted">' + tgl(x.tanggal) + ' · ' + h(x.sumber === 'booking' ? 'dari reservasi' : 'dicatat manual') + '</div></div>' +
          '<button class="linkbtn" data-act="hapus-riwayat" data-arg="' + x.id + '" style="color:var(--ink-4);">' + ic('trash', 15) + '</button></div>';
      }).join('');
    }
    body += '</div>';

    body += '<div class="card stack g12"><div class="row mid"><div class="sect-title">Tumbuh kembang</div><div class="grow"></div>' +
      '<button class="linkbtn" data-act="go" data-arg="tumbuh-form/' + p.id + '">+ Catat</button></div>';
    if (tumbuh.length < 1) {
      body += '<div class="small muted">Belum ada data. Catat berat, tinggi, dan lingkar kepala untuk melihat grafiknya.</div>';
    } else {
      var akhir = tumbuh[tumbuh.length - 1];
      body += '<div class="row g8">' +
        statKecil('Berat', akhir.berat ? akhir.berat + ' kg' : '-') +
        statKecil('Tinggi', akhir.tinggi ? akhir.tinggi + ' cm' : '-') +
        statKecil('Lingkar kepala', akhir.kepala ? akhir.kepala + ' cm' : '-') + '</div>';
      body += '<div class="tiny muted">Pengukuran terakhir ' + tgl(akhir.tanggal) + '</div>';
      body += grafik(tumbuh, p);
      body += '<div class="stack g6">' + tumbuh.slice().reverse().map(function (t) {
        return '<div class="row between small" style="padding:6px 0;border-top:1px solid var(--line);">' +
          '<span style="color:var(--ink-2);">' + tgl(t.tanggal) + '</span>' +
          '<span class="nowrap">' + (t.berat ? t.berat + ' kg' : '') + (t.tinggi ? ' · ' + t.tinggi + ' cm' : '') +
          ' <button class="linkbtn" data-act="hapus-tumbuh" data-arg="' + t.id + '" style="color:var(--ink-4);">' + ic('trash', 14) + '</button></span></div>';
      }).join('') + '</div>';
    }
    body += '</div>';

    body += '</div>';
    return { body: body, nav: 'rekam' };
  }
  function statKecil(label, nilai) {
    return '<div class="card flat" style="flex:1;padding:11px;text-align:center;border-radius:13px;">' +
      '<div class="disp" style="font-size:15px;font-weight:800;">' + h(nilai) + '</div>' +
      '<div class="tiny muted" style="margin-top:2px;">' + h(label) + '</div></div>';
  }
  function grafik(data, p) {
    var pts = data.filter(function (d) { return d.berat; }).map(function (d) {
      return { x: umurBulan(p.tglLahir, d.tanggal) || 0, y: parseFloat(d.berat) };
    });
    if (pts.length < 2) return '<div class="tiny muted">Grafik muncul setelah ada minimal dua pengukuran berat badan.</div>';
    var W = 300, H = 150, pad = 30;
    var xs = pts.map(function (p) { return p.x; }), ys = pts.map(function (p) { return p.y; });
    var x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs);
    var y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
    if (x1 === x0) x1 = x0 + 1;
    if (y1 === y0) { y0 = Math.max(0, y0 - 1); y1 = y1 + 1; }
    var sx = function (v) { return pad + (v - x0) / (x1 - x0) * (W - pad - 8); };
    var sy = function (v) { return H - 24 - (v - y0) / (y1 - y0) * (H - 24 - 10); };
    var d = pts.map(function (p, i) { return (i ? 'L' : 'M') + sx(p.x).toFixed(1) + ' ' + sy(p.y).toFixed(1); }).join(' ');
    var dots = pts.map(function (p) { return '<circle cx="' + sx(p.x).toFixed(1) + '" cy="' + sy(p.y).toFixed(1) + '" r="3.4" fill="#2E9BA0"/>'; }).join('');
    return '<div style="overflow-x:auto;"><svg viewBox="0 0 ' + W + ' ' + H + '" width="100%" height="150" role="img" aria-label="Grafik berat badan">' +
      '<line x1="' + pad + '" y1="' + (H - 24) + '" x2="' + (W - 8) + '" y2="' + (H - 24) + '" stroke="#ECECEC" stroke-width="1"/>' +
      '<line x1="' + pad + '" y1="10" x2="' + pad + '" y2="' + (H - 24) + '" stroke="#ECECEC" stroke-width="1"/>' +
      '<path d="' + d + '" fill="none" stroke="#56C3C7" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>' + dots +
      '<text x="' + pad + '" y="' + (H - 8) + '" fill="#9AA0A6" font-size="9" font-family="sans-serif">' + x0 + ' bln</text>' +
      '<text x="' + (W - 8) + '" y="' + (H - 8) + '" fill="#9AA0A6" font-size="9" font-family="sans-serif" text-anchor="end">' + x1 + ' bln</text>' +
      '<text x="2" y="14" fill="#9AA0A6" font-size="9" font-family="sans-serif">' + y1 + ' kg</text>' +
      '<text x="2" y="' + (H - 26) + '" fill="#9AA0A6" font-size="9" font-family="sans-serif">' + y0 + ' kg</text>' +
      '</svg></div><div class="tiny muted">Grafik berat badan anak terhadap usia (data Anda sendiri).</div>';
  }

  /* ============================ layar: harga ============================ */
  var tarif = 'umum', cariHarga = '';
  function scHarga() {
    var body = topbar('Daftar Harga Vaksinasi', 'Price list terbuka', 'beranda');
    body += '<div class="pad stack g12">' +
      '<div class="card tint row mid g8" style="padding:12px 14px;">' + ic('checkc', 16) +
      '<span class="tiny" style="color:var(--teal-dark);font-weight:600;line-height:1.5;">Harga sudah termasuk jasa dokter, vaksin, bahan habis pakai &amp; administrasi.</span></div>' +
      '<div class="row g8">' +
      '<button class="pill' + (tarif === 'umum' ? ' teal-on' : '') + '" style="flex:1;text-align:center;" data-act="set-tarif" data-arg="umum">Dokter Umum</button>' +
      '<button class="pill' + (tarif === 'spesialis' ? ' teal-on' : '') + '" style="flex:1;text-align:center;" data-act="set-tarif" data-arg="spesialis">Dokter Spesialis</button></div>' +
      '<input class="input" id="cari-harga" placeholder="Cari vaksin..." value="' + h(cariHarga) + '">';

    var q = cariHarga.toLowerCase();
    var grup = {}, urut = [];
    K.harga.forEach(function (v) {
      if (q && (v.kategori + ' ' + v.sediaan + ' ' + v.merk).toLowerCase().indexOf(q) < 0) return;
      if (!grup[v.kategori]) { grup[v.kategori] = []; urut.push(v.kategori); }
      grup[v.kategori].push(v);
    });
    if (!urut.length) body += '<div class="small muted center" style="padding:24px 0;">Vaksin tidak ditemukan.</div>';
    urut.forEach(function (nama) {
      body += '<div class="card stack g6" style="padding:14px 16px;">' +
        '<div class="row mid g8"><div class="icon-sq" style="width:30px;height:30px;border-radius:9px;">' + ic('syringe', 16) + '</div>' +
        '<span style="font-weight:700;font-size:13.5px;">' + h(nama) + '</span></div>' +
        '<table class="price">' + grup[nama].map(function (v) {
          var hrg = tarif === 'spesialis' ? v.spesialis : v.umum;
          return '<tr><td><div style="font-weight:600;">' + h(v.sediaan) + '</div>' +
            (v.merk !== v.sediaan ? '<div class="tiny muted">' + h(v.merk) + '</div>' : '') + '</td>' +
            '<td class="p">' + (hrg ? rp(angka(hrg)) : '<span class="muted" style="font-weight:600;">Hubungi CS</span>') + '</td></tr>';
        }).join('') + '</table></div>';
    });
    body += '<div class="tiny muted" style="padding:0 4px;">Harga dapat berubah sewaktu-waktu. Konfirmasi terakhir saat reservasi melalui ' + h(K.brand.callCenter) + '.</div>';
    body += '<button class="btn primary" data-act="go" data-arg="booking">' + ic('plus', 16, 2.2) + ' Booking vaksinasi</button>';
    body += '</div>';
    return { body: body };
  }

  /* ============================ layar: internasional ============================ */
  function scInternasional() {
    var body = topbar('Vaksin Internasional', 'Haji, umrah, studi & liburan', 'beranda');
    body += '<div class="pad stack g14">' +
      '<div class="small muted" style="line-height:1.6;">Bagi jamaah <b>haji &amp; umrah</b> wajib vaksin Meningitis dan Polio. WHO merekomendasikan vaksinasi tambahan Influenza dan Pneumonia.</div>';
    body += '<div class="card stack g10"><div class="row mid g8"><div class="sect-title">Vaksin wajib</div><span class="chip teal">Regulasi Arab Saudi</span></div>' +
      K.internasionalWajib.map(function (v) {
        return '<div class="row g12" style="align-items:flex-start;padding-top:10px;border-top:1px solid var(--line);">' +
          '<div class="icon-sq" style="width:32px;height:32px;border-radius:9px;">' + ic('shield', 16) + '</div>' +
          '<div class="grow"><div class="small" style="font-weight:700;">' + h(v[0]) + '</div>' +
          '<div class="tiny muted" style="line-height:1.55;">' + h(v[1]) + '</div></div></div>';
      }).join('') + '</div>';
    body += '<div class="card stack g10"><div class="row mid g8"><div class="sect-title">Vaksin tambahan</div><span class="chip amber">Rekomendasi WHO</span></div>' +
      K.internasionalTambahan.map(function (v) {
        return '<div class="row g12" style="align-items:flex-start;padding-top:10px;border-top:1px solid var(--line);">' +
          '<div class="icon-sq mag" style="width:32px;height:32px;border-radius:9px;">' + ic('plus', 16) + '</div>' +
          '<div class="grow"><div class="small" style="font-weight:700;">' + h(v[0]) + '</div>' +
          '<div class="tiny muted" style="line-height:1.55;">' + h(v[1]) + '</div></div></div>';
      }).join('') + '</div>';
    body += '<div class="sect-title" style="padding-top:2px;">Harga</div>';
    K.hargaInternasional.forEach(function (x) {
      body += '<div class="card row mid g12" style="padding:15px 16px;">' +
        '<div class="grow"><div class="row mid g7"><span style="font-weight:700;font-size:13px;">' + h(x.nama) + '</span>' +
        (x.coret ? '<span class="chip mag" style="padding:2px 8px;font-size:9.5px;margin-left:7px;">PROMO</span>' : '') + '</div>' +
        (x.coret ? '<div class="tiny muted" style="text-decoration:line-through;">' + rp(angka(x.coret)) + '</div>' : '') + '</div>' +
        '<div class="disp nowrap" style="font-size:16px;font-weight:800;color:var(--magenta-dark);">' + rp(angka(x.harga)) + '</div></div>';
    });
    var pt = K.paketTriple;
    body += '<div class="card stack g10" style="border:1.6px solid var(--magenta);">' +
      '<div class="row mid g8"><span class="disp" style="font-size:15px;font-weight:800;">' + h(pt.nama) + '</span>' +
      '<span class="chip mag" style="padding:2px 8px;font-size:9.5px;">HEMAT</span></div>' +
      pt.isi.map(function (i) { return '<div class="row mid g8">' + ic('checkc', 15) + '<span class="small" style="color:var(--ink-2);">' + h(i) + '</span></div>'; }).join('') +
      '<div class="divider"></div>' +
      '<div class="row mid g10" style="align-items:baseline;"><span class="disp" style="font-size:21px;font-weight:800;color:var(--magenta-dark);">' + rp(angka(pt.harga)) + '</span>' +
      '<span class="small muted" style="text-decoration:line-through;">' + rp(angka(pt.coret)) + '</span></div></div>';
    body += '<div class="card tint row mid g12"><div class="icon-sq" style="background:#fff;">' + ic('doc', 19) + '</div>' +
      '<div class="grow"><div class="small" style="font-weight:700;">Buku Kuning Elektronik (e-ICV)</div>' +
      '<div class="tiny" style="color:var(--ink-2);">Diterbitkan di klinik setelah vaksinasi.</div></div></div>';
    body += '<button class="btn primary" data-act="go" data-arg="booking">' + ic('plus', 16, 2.2) + ' Booking vaksin internasional</button>';
    body += '</div>';
    return { body: body };
  }

  /* ============================ layar: tentang ============================ */
  function scTentang() {
    var body = topbar('Tentang & Lokasi', K.brand.group, 'beranda');
    body += '<div class="pad stack g14">' +
      '<div class="stack mid g10 center" style="padding:4px 0;"><img src="' + K.logoMark + '" alt="VaksinKu" style="height:30px;width:auto;">' +
      '<div class="small" style="font-weight:700;color:var(--teal-dark);">' + h(K.brand.tagline) + '</div></div>';
    K.pilar.forEach(function (p) {
      body += '<div class="card stack g10"><div class="row mid g10"><div class="icon-sq">' + ic(p[0] === 'shield' ? 'shield' : p[0] === 'coin' ? 'coin' : 'checkc', 18) + '</div>' +
        '<span class="disp" style="font-weight:800;font-size:15px;">' + h(p[1]) + '</span></div>' +
        p[2].map(function (t) {
          return '<div class="row g8" style="align-items:flex-start;">' + ic('checkc', 14) +
            '<span class="small" style="color:var(--ink-2);line-height:1.55;">' + t + '</span></div>';
        }).join('') + '</div>';
    });
    body += '<div class="sect-title" style="padding-top:4px;">Kemudahan dari VaksinKu</div>';
    K.layanan.forEach(function (l) {
      body += '<div class="card stack g8"><div class="row mid g10"><div class="icon-sq mag">' + ic(l[0], 18) + '</div>' +
        '<div><div class="disp" style="font-weight:800;font-size:14.5px;">' + h(l[1]) + '</div>' +
        '<div class="tiny muted">' + h(l[2]) + '</div></div></div>' +
        '<div class="small" style="color:var(--ink-2);line-height:1.6;">' + h(l[3]) + '</div>' +
        '<span class="chip teal">' + h(l[4]) + '</span></div>';
    });
    body += '<div class="card stack g4"><div class="sect-title" style="margin-bottom:6px;">Alur reservasi</div>' +
      K.alurReservasi.map(function (s, i) {
        return '<div class="row g12" style="align-items:flex-start;padding:6px 0;">' +
          '<div class="disp" style="width:24px;height:24px;border-radius:50%;background:var(--teal);color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;flex-shrink:0;">' + (i + 1) + '</div>' +
          '<span class="small" style="color:var(--ink-2);line-height:1.55;padding-top:2px;">' + h(s) + '</span></div>';
      }).join('') + '</div>';
    body += '<div class="card stack g4"><div class="sect-title" style="margin-bottom:6px;">Dokter vaksinasi</div>' +
      K.dokter.map(function (d) {
        return '<div class="row mid g12" style="padding:9px 0;border-top:1px solid var(--line);">' +
          '<div class="avatar" style="width:36px;height:36px;font-size:12px;">' + h(d[2]) + '</div>' +
          '<div class="grow"><div class="small" style="font-weight:700;">' + h(d[0]) + '</div>' +
          '<div class="tiny muted">' + h(d[1]) + '</div></div></div>';
      }).join('') + '</div>';
    body += '<div class="card stack g4"><div class="sect-title" style="margin-bottom:6px;">Lokasi klinik</div>' +
      K.klinik.map(function (kl) {
        return '<div class="row g12" style="align-items:flex-start;padding:10px 0;border-top:1px solid var(--line);">' +
          '<div class="icon-sq mag" style="width:32px;height:32px;border-radius:9px;">' + ic('pin', 16) + '</div>' +
          '<div class="grow"><div class="small" style="font-weight:700;">' + h(kl[0]) + '</div>' +
          '<div class="tiny muted" style="line-height:1.5;">' + h(kl[1]) + '</div></div></div>';
      }).join('') + '</div>';
    body += '<div class="card stack g12" style="background:var(--teal-dark);border-color:transparent;color:#fff;">' +
      '<div class="row mid g12"><div class="icon-sq" style="background:rgba(255,255,255,.16);color:#fff;border-radius:50%;">' + ic('wa', 19) + '</div>' +
      '<div class="grow"><div class="tiny" style="opacity:.85;">' + h(K.brand.callCenterLabel) + '</div>' +
      '<div class="disp" style="font-weight:800;font-size:18px;">' + h(K.brand.callCenter) + '</div></div></div>' +
      '<button class="btn" style="background:#fff;color:var(--teal-deep);" data-act="wa-umum">' + ic('wa', 17) + ' Hubungi via WhatsApp</button>' +
      '<div class="row g16 wrap tiny" style="opacity:.9;"><span>' + h(K.brand.instagram) + '</span><span>' + h(K.brand.website) + '</span></div></div>';
    body += '</div>';
    return { body: body };
  }

  /* ============================ layar: profil ============================ */
  function scProfil() {
    var body = topbar('Profil', 'Data pendaftar & pengaturan');
    body += '<div class="pad stack g14">';
    body += '<div class="card stack g10"><div class="sect-title">Data pendaftar</div>' +
      '<div class="hint">Dipakai sebagai penerima invoice dan kontak yang dihubungi CS.</div>' +
      '<div><label class="lbl">Nama lengkap<span class="req">*</span></label>' +
      '<input class="input" data-field="profil.nama" value="' + h(S.profil.nama) + '" placeholder="Nama sesuai identitas"></div>' +
      '<div><label class="lbl">Nomor HP / WhatsApp<span class="req">*</span></label>' +
      '<input class="input" type="tel" inputmode="tel" data-field="profil.hp" value="' + h(S.profil.hp) + '" placeholder="08xxxxxxxxxx"></div>' +
      '<div><label class="lbl">Jenis kelamin</label>' +
      '<div class="row g8">' +
      '<button class="opt' + (S.profil.jenisKelamin === 'Perempuan' ? ' on' : '') + '" data-act="set-jk" data-arg="Perempuan">Perempuan</button>' +
      '<button class="opt' + (S.profil.jenisKelamin === 'Laki-laki' ? ' on' : '') + '" data-act="set-jk" data-arg="Laki-laki">Laki-laki</button></div></div></div>';

    body += '<div class="card row mid g12" style="background:var(--amber-tint);border-color:transparent;">' +
      '<div class="icon-sq amber" style="background:#fff;">' + ic('coin', 20) + '</div>' +
      '<div class="grow"><div class="disp" style="font-weight:800;font-size:16px;">' + S.poin + ' Poin Sehat</div>' +
      '<div class="tiny" style="color:#8A6A21;">+10 poin setiap vaksinasi selesai</div></div></div>';

    body += '<div class="card stack g4">' +
      menuRow('family', 'Daftar Pasien', S.pasien.length + ' orang terdaftar', 'pasien') +
      '<div class="divider"></div>' +
      menuRow('pin', 'Daftar Alamat', S.alamat.length + ' alamat tersimpan', 'alamat') +
      '<div class="divider"></div>' +
      menuRow('doc', 'Riwayat Reservasi', S.booking.length + ' reservasi', 'riwayat-booking') +
      '<div class="divider"></div>' +
      menuRow('tag', 'Daftar Harga', 'Price list lengkap', 'harga') +
      '<div class="divider"></div>' +
      menuRow('info', 'Tentang & Lokasi', 'Klinik, dokter, kontak', 'tentang') +
      '</div>';

    body += '<div class="card stack g10"><div class="sect-title">Data aplikasi</div>' +
      '<div class="hint">Semua data tersimpan di perangkat ini saja — tidak dikirim ke server mana pun. Cadangkan sebelum ganti perangkat atau membersihkan browser.</div>' +
      '<button class="btn outline sm" data-act="ekspor">' + ic('download', 16) + ' Cadangkan data (.json)</button>' +
      '<button class="btn outline sm" data-act="impor">' + ic('upload', 16) + ' Pulihkan dari cadangan</button>' +
      (S.pasien.length ? '' : '<button class="btn outline sm" data-act="contoh">Muat data contoh</button>') +
      '<button class="btn danger sm" data-act="reset">Hapus semua data</button>' +
      '<input type="file" id="file-impor" accept="application/json,.json" class="hide"></div>';

    if (!storageOk) {
      body += '<div class="card" style="background:var(--danger-tint);border-color:transparent;">' +
        '<div class="small" style="color:var(--danger);line-height:1.6;">Penyimpanan browser tidak aktif, jadi data hanya bertahan selama halaman terbuka. ' +
        'Buka file ini langsung di browser (bukan mode privat) agar data tersimpan.</div></div>';
    }
    body += '<div class="tiny muted center">VaksinKu ' + h(K.brand.group) + ' · versi 1.0</div>';
    body += '</div>';
    return { body: body, nav: 'profil' };
  }
  function menuRow(icon, judul, sub, target) {
    return '<button class="rowlink" data-act="go" data-arg="' + target + '">' +
      '<div class="icon-sq" style="width:34px;height:34px;border-radius:10px;">' + ic(icon, 17) + '</div>' +
      '<div class="grow"><div class="small" style="font-weight:700;">' + h(judul) + '</div>' +
      '<div class="tiny muted">' + h(sub) + '</div></div>' +
      '<span style="color:var(--ink-4);">' + ic('chevron', 15) + '</span></button>';
  }

  /* ============================ layar: daftar pasien / alamat / riwayat ============================ */
  function scPasien() {
    var body = topbar('Daftar Pasien', 'Anggota keluarga yang divaksin', 'profil');
    body += '<div class="pad stack g12">';
    if (!S.pasien.length) {
      body += empty('family', 'Belum ada pasien', 'Tambahkan anggota keluarga beserta tanggal lahirnya agar jadwal vaksin bisa dihitung otomatis.', '');
    } else {
      S.pasien.forEach(function (p) {
        var r = ringkasJadwal(p);
        body += '<div class="card row mid g12">' +
          '<div class="avatar">' + h(inisial(p.nama)) + '</div>' +
          '<div class="grow"><div style="font-weight:700;font-size:13.5px;">' + h(p.nama) + '</div>' +
          '<div class="tiny muted">' + h(umurTeks(umurBulan(p.tglLahir))) + (p.hubungan ? ' · ' + h(p.hubungan) : '') + '</div>' +
          (r ? '<div class="tiny" style="color:var(--teal-dark);margin-top:2px;">Kelengkapan ' + r.persen + '%</div>' : '') + '</div>' +
          '<button class="linkbtn" data-act="go" data-arg="pasien-form/' + p.id + '" style="color:var(--ink-4);">' + ic('edit', 17) + '</button></div>';
      });
    }
    body += '<button class="btn primary" data-act="go" data-arg="pasien-form">' + ic('plus', 16, 2.2) + ' Tambah pasien</button></div>';
    return { body: body };
  }
  var formErr = {};
  function scPasienForm(id) {
    var p = S.pasien.filter(function (x) { return x.id === id; })[0] ||
      { id: '', nama: '', tglLahir: '', jenisKelamin: '', hubungan: '' };
    var body = topbar(id ? 'Ubah Pasien' : 'Tambah Pasien', '', 'pasien');
    body += '<div class="pad stack g14"><form id="form-pasien" class="stack g14">' +
      '<div><label class="lbl">Nama lengkap<span class="req">*</span></label>' +
      '<input class="input' + (formErr.nama ? ' err' : '') + '" name="nama" value="' + h(p.nama) + '" placeholder="Nama pasien">' +
      (formErr.nama ? '<div class="errmsg">' + h(formErr.nama) + '</div>' : '') + '</div>' +
      '<div><label class="lbl">Tanggal lahir<span class="req">*</span></label>' +
      '<input class="input' + (formErr.tglLahir ? ' err' : '') + '" type="date" name="tglLahir" max="' + hariIni() + '" value="' + h(p.tglLahir) + '">' +
      '<div class="hint" style="margin-top:6px;">Dipakai untuk menghitung jadwal vaksin sesuai usia.</div>' +
      (formErr.tglLahir ? '<div class="errmsg">' + h(formErr.tglLahir) + '</div>' : '') + '</div>' +
      '<div><label class="lbl">Jenis kelamin</label>' +
      '<select class="input" name="jenisKelamin">' +
      ['', 'Perempuan', 'Laki-laki'].map(function (o) {
        return '<option value="' + o + '"' + (p.jenisKelamin === o ? ' selected' : '') + '>' + (o || 'Pilih...') + '</option>';
      }).join('') + '</select></div>' +
      '<div><label class="lbl">Hubungan keluarga</label>' +
      '<input class="input" name="hubungan" value="' + h(p.hubungan) + '" placeholder="Anak, istri, orang tua..."></div>' +
      '<input type="hidden" name="pid" value="' + h(p.id) + '">' +
      '<button type="submit" class="btn primary">' + (id ? 'Simpan perubahan' : 'Simpan pasien') + '</button>' +
      (id ? '<button type="button" class="btn danger" data-act="hapus-pasien" data-arg="' + id + '">Hapus pasien</button>' : '') +
      '</form></div>';
    return { body: body };
  }
  function scAlamat() {
    var body = topbar('Daftar Alamat', 'Untuk layanan Home Care', 'profil');
    body += '<div class="pad stack g12">';
    if (!S.alamat.length) body += empty('pin', 'Belum ada alamat', 'Tambahkan alamat rumah agar bisa memilih layanan Home Care saat reservasi.', '');
    S.alamat.forEach(function (a) {
      body += '<div class="card row mid g12"><div class="icon-sq">' + ic('pin', 18) + '</div>' +
        '<div class="grow"><div style="font-weight:700;font-size:13.5px;">' + h(a.label) + '</div>' +
        '<div class="tiny muted" style="line-height:1.5;">' + h(a.alamat + ', ' + a.kecamatan) + (a.patokan ? ' (' + h(a.patokan) + ')' : '') + '</div></div>' +
        '<button class="linkbtn" data-act="hapus-alamat" data-arg="' + a.id + '" style="color:var(--ink-4);">' + ic('trash', 16) + '</button></div>';
    });
    body += '<button class="btn primary" data-act="go" data-arg="alamat-form">' + ic('plus', 16, 2.2) + ' Tambah alamat</button></div>';
    return { body: body };
  }
  function scAlamatForm() {
    var body = topbar('Tambah Alamat', '', 'alamat');
    body += '<div class="pad stack g14"><form id="form-alamat" class="stack g14">' +
      '<div><label class="lbl">Label<span class="req">*</span></label>' +
      '<input class="input' + (formErr.label ? ' err' : '') + '" name="label" placeholder="Rumah, kantor, rumah orang tua...">' +
      (formErr.label ? '<div class="errmsg">' + h(formErr.label) + '</div>' : '') + '</div>' +
      '<div><label class="lbl">Kecamatan / kota<span class="req">*</span></label>' +
      '<input class="input' + (formErr.kecamatan ? ' err' : '') + '" name="kecamatan" placeholder="Tanjungpinang Kota, Kepulauan Riau">' +
      (formErr.kecamatan ? '<div class="errmsg">' + h(formErr.kecamatan) + '</div>' : '') + '</div>' +
      '<div><label class="lbl">Alamat lengkap<span class="req">*</span></label>' +
      '<textarea class="input' + (formErr.alamat ? ' err' : '') + '" name="alamat" placeholder="Nama jalan, nomor rumah, RT/RW"></textarea>' +
      (formErr.alamat ? '<div class="errmsg">' + h(formErr.alamat) + '</div>' : '') + '</div>' +
      '<div><label class="lbl">Patokan (opsional)</label>' +
      '<input class="input" name="patokan" placeholder="Depan masjid, sebelah minimarket..."></div>' +
      '<button type="submit" class="btn primary">Simpan alamat</button></form></div>';
    return { body: body };
  }
  function scTumbuhForm(pasienId) {
    var p = S.pasien.filter(function (x) { return x.id === pasienId; })[0];
    if (!p) return { body: topbar('Catat Pertumbuhan', '', 'rekam') + empty('chart', 'Pasien tidak ditemukan', '') };
    var body = topbar('Catat Pertumbuhan', p.nama, 'rekam');
    body += '<div class="pad stack g14"><form id="form-tumbuh" class="stack g14">' +
      '<input type="hidden" name="pasienId" value="' + h(pasienId) + '">' +
      '<div><label class="lbl">Tanggal pengukuran<span class="req">*</span></label>' +
      '<input class="input" type="date" name="tanggal" max="' + hariIni() + '" value="' + hariIni() + '"></div>' +
      '<div><label class="lbl">Berat badan (kg)</label>' +
      '<input class="input" type="number" step="0.1" min="0" name="berat" inputmode="decimal" placeholder="contoh: 12.4"></div>' +
      '<div><label class="lbl">Tinggi badan (cm)</label>' +
      '<input class="input" type="number" step="0.1" min="0" name="tinggi" inputmode="decimal" placeholder="contoh: 92"></div>' +
      '<div><label class="lbl">Lingkar kepala (cm)</label>' +
      '<input class="input" type="number" step="0.1" min="0" name="kepala" inputmode="decimal" placeholder="contoh: 47"></div>' +
      (formErr.tumbuh ? '<div class="errmsg">' + h(formErr.tumbuh) + '</div>' : '') +
      '<button type="submit" class="btn primary">Simpan pengukuran</button></form></div>';
    return { body: body };
  }
  function scRiwayatBooking() {
    var body = topbar('Riwayat Reservasi', S.booking.length + ' reservasi', 'profil');
    body += '<div class="pad stack g12">';
    if (!S.booking.length) body += empty('doc', 'Belum ada reservasi', 'Reservasi yang Anda buat akan tersimpan di sini.',
      '<button class="btn primary" data-act="go" data-arg="booking">Buat reservasi</button>');
    S.booking.forEach(function (b) {
      var st = { menunggu: ['mag', 'Menunggu'], selesai: ['green', 'Selesai'], batal: ['grey', 'Batal'] }[b.status];
      body += '<button class="card row mid g12 tap" style="text-align:left;width:100%;border-width:1px;" data-act="go" data-arg="booking-detail/' + b.id + '">' +
        '<div class="stack grow g4"><div class="row mid g8"><span class="chip ' + st[0] + '">' + st[1] + '</span>' +
        '<span class="tiny muted">' + h(b.kode) + '</span></div>' +
        '<div class="small" style="font-weight:700;">' + h(b.pasienIds.map(namaPasien).join(', ')) + '</div>' +
        '<div class="tiny muted">' + tgl(b.tanggal) + ' · ' + h(b.jam) + ' · ' + rp(b.total) + '</div></div>' +
        '<span style="color:var(--ink-4);">' + ic('chevron', 16) + '</span></button>';
    });
    body += '</div>';
    return { body: body };
  }

  /* ============================ render ============================ */
  var sheetHTML = '';
  function render() {
    var r;
    switch (route.name) {
      case 'booking': r = scBooking(); break;
      case 'booking-detail': r = scBookingDetail(route.param); break;
      case 'jadwal': r = scJadwal(); break;
      case 'jadwal-info': r = scJadwalInfo(route.param); break;
      case 'rekam': r = scRekam(); break;
      case 'harga': r = scHarga(); break;
      case 'internasional': r = scInternasional(); break;
      case 'tentang': r = scTentang(); break;
      case 'profil': r = scProfil(); break;
      case 'pasien': r = scPasien(); break;
      case 'pasien-form': r = scPasienForm(route.param); break;
      case 'alamat': r = scAlamat(); break;
      case 'alamat-form': r = scAlamatForm(); break;
      case 'tumbuh-form': r = scTumbuhForm(route.param); break;
      case 'riwayat-booking': r = scRiwayatBooking(); break;
      default: r = scBeranda();
    }
    app.innerHTML = '<div class="device">' +
      '<div class="scroll" id="scroll">' + r.body + '</div>' +
      (r.foot || '') + (r.nav ? navbar(r.nav) : '') + sheetHTML + '</div>';
    var s = document.getElementById('cari-vaksin');
    if (s) { s.focus(); s.setSelectionRange(s.value.length, s.value.length); }
  }

  /* ============================ aksi ============================ */
  function konfirmasi(pesan) { return window.confirm(pesan); }

  document.addEventListener('click', function (ev) {
    var el = ev.target.closest('[data-act]');
    if (!el) return;
    var act = el.getAttribute('data-act'), arg = el.getAttribute('data-arg') || '';
    if (act === 'tutup-sheet' && ev.target.closest('[data-stop]')) return;
    var d = draft();

    switch (act) {
      case 'go': location.hash = '#/' + arg; return;
      case 'mulai-booking': d.layanan = arg; simpan(); location.hash = '#/booking'; return;
      case 'pilih-pasien': S.ui.pasienAktif = arg; simpan(); render(); return;
      case 'pasien-jadwal': S.ui.pasienAktif = arg; simpan(); location.hash = '#/jadwal'; return;
      case 'set-layanan': d.layanan = arg; simpan(); render(); return;
      case 'set-klinik': d.klinikIdx = parseInt(arg, 10); simpan(); render(); return;
      case 'set-alamat': d.alamatId = arg; simpan(); render(); return;
      case 'set-dokter': d.dokter = arg; simpan(); render(); return;
      case 'set-jam': d.jam = arg; simpan(); render(); return;
      case 'set-jk': S.profil.jenisKelamin = arg; simpan(); render(); return;
      case 'set-tarif': tarif = arg; render(); return;
      case 'toggle-pasien': {
        var i = d.pasienIds.indexOf(arg);
        if (i >= 0) d.pasienIds.splice(i, 1); else d.pasienIds.push(arg);
        simpan(); render(); return;
      }
      case 'buka-vaksin': cariVaksin = ''; sheetHTML = sheetVaksin(); render(); return;
      case 'tutup-sheet': sheetHTML = ''; render(); return;
      case 'toggle-vaksin': {
        var j = d.vaksinIds.indexOf(arg);
        if (j >= 0) d.vaksinIds.splice(j, 1); else d.vaksinIds.push(arg);
        simpan(); sheetHTML = sheetVaksin(); render(); return;
      }
      case 'hapus-vaksin': {
        var k = d.vaksinIds.indexOf(arg);
        if (k >= 0) d.vaksinIds.splice(k, 1);
        simpan(); render(); return;
      }
      case 'kirim-booking': {
        errB = validasiBooking(d);
        if (Object.keys(errB).length) {
          render();
          var bad = document.querySelector('.errmsg');
          if (bad) bad.scrollIntoView({ block: 'center', behavior: 'smooth' });
          toast('Lengkapi bagian yang ditandai merah.');
          return;
        }
        var rec = buatBooking();
        errB = {};
        location.hash = '#/booking-detail/' + rec.id;
        setTimeout(function () { toast('Reservasi ' + rec.kode + ' tersimpan. Kirim ke CS untuk konfirmasi.'); }, 60);
        return;
      }
      case 'wa-booking': {
        var b1 = S.booking.filter(function (x) { return x.id === arg; })[0];
        if (b1) kirimWA(b1);
        return;
      }
      case 'wa-umum':
        window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent('Halo VaksinKu, saya ingin bertanya tentang layanan vaksinasi.'), '_blank');
        return;
      case 'selesai-booking': {
        var b2 = S.booking.filter(function (x) { return x.id === arg; })[0];
        if (!b2 || b2.status !== 'menunggu') return;
        if (!konfirmasi('Tandai vaksinasi ini sudah selesai? Vaksin akan dicatat di rekam medis pasien.')) return;
        b2.status = 'selesai';
        b2.pasienIds.forEach(function (pid) {
          b2.rincian.concat(b2.tanpaHarga.map(function (n) { return { nama: n }; })).forEach(function (r) {
            S.riwayat.push({ id: uid(), pasienId: pid, label: r.nama, tanggal: b2.tanggal, sumber: 'booking', bookingId: b2.id });
          });
        });
        S.poin += 10;
        simpan(); render(); toast('Tercatat di rekam medis. +10 Poin Sehat.');
        return;
      }
      case 'batal-booking': {
        var b3 = S.booking.filter(function (x) { return x.id === arg; })[0];
        if (!b3 || !konfirmasi('Batalkan reservasi ' + b3.kode + '?')) return;
        b3.status = 'batal'; simpan(); render(); toast('Reservasi dibatalkan.');
        return;
      }
      case 'hapus-booking': {
        if (!konfirmasi('Hapus reservasi ini dari daftar?')) return;
        S.booking = S.booking.filter(function (x) { return x.id !== arg; });
        simpan(); location.hash = '#/riwayat-booking'; toast('Reservasi dihapus.');
        return;
      }
      case 'toggle-riwayat': {
        var parts = arg.split('|'), pid = parts[0], label = decodeURIComponent(parts[1]);
        var ada = S.riwayat.filter(function (r) { return r.pasienId === pid && r.label === label; })[0];
        if (ada) S.riwayat = S.riwayat.filter(function (r) { return r !== ada; });
        else S.riwayat.push({ id: uid(), pasienId: pid, label: label, tanggal: hariIni(), sumber: 'jadwal' });
        simpan(); render();
        return;
      }
      case 'hapus-riwayat':
        S.riwayat = S.riwayat.filter(function (r) { return r.id !== arg; });
        simpan(); render(); toast('Catatan dihapus.');
        return;
      case 'hapus-pasien': {
        if (!konfirmasi('Hapus pasien ini beserta riwayat vaksin dan data pertumbuhannya?')) return;
        S.pasien = S.pasien.filter(function (p) { return p.id !== arg; });
        S.riwayat = S.riwayat.filter(function (r) { return r.pasienId !== arg; });
        S.pertumbuhan = S.pertumbuhan.filter(function (t) { return t.pasienId !== arg; });
        if (S.ui.pasienAktif === arg) S.ui.pasienAktif = '';
        var dd = draft(); dd.pasienIds = dd.pasienIds.filter(function (x) { return x !== arg; });
        simpan(); location.hash = '#/pasien'; toast('Pasien dihapus.');
        return;
      }
      case 'hapus-alamat': {
        if (!konfirmasi('Hapus alamat ini?')) return;
        S.alamat = S.alamat.filter(function (a) { return a.id !== arg; });
        if (draft().alamatId === arg) draft().alamatId = '';
        simpan(); render(); toast('Alamat dihapus.');
        return;
      }
      case 'hapus-tumbuh':
        S.pertumbuhan = S.pertumbuhan.filter(function (t) { return t.id !== arg; });
        simpan(); render(); toast('Data pengukuran dihapus.');
        return;
      case 'ekspor': {
        var blob = new Blob([JSON.stringify(S, null, 2)], { type: 'application/json' });
        var a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'vaksinku-cadangan-' + hariIni() + '.json';
        document.body.appendChild(a); a.click(); a.remove();
        setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
        toast('Cadangan diunduh.');
        return;
      }
      case 'impor': document.getElementById('file-impor').click(); return;
      case 'contoh': muatContoh(); return;
      case 'reset': {
        if (!konfirmasi('Hapus SEMUA data di aplikasi ini? Tindakan ini tidak bisa dibatalkan.')) return;
        S = JSON.parse(JSON.stringify(kosong));
        simpan(); location.hash = '#/beranda'; render(); toast('Semua data dihapus.');
        return;
      }
    }
  });

  document.addEventListener('input', function (ev) {
    var el = ev.target;
    if (el.id === 'cari-vaksin') { cariVaksin = el.value; sheetHTML = sheetVaksin(); render(); return; }
    if (el.id === 'cari-harga') {
      cariHarga = el.value;
      var pos = el.selectionStart; render();
      var n = document.getElementById('cari-harga');
      if (n) { n.focus(); n.setSelectionRange(pos, pos); }
      return;
    }
    var f = el.getAttribute('data-field');
    if (!f) return;
    if (f.indexOf('profil.') === 0) S.profil[f.split('.')[1]] = el.value;
    else draft()[f] = el.value;
    simpan();
    if (f === 'tanggal') render();
  });

  document.addEventListener('change', function (ev) {
    if (ev.target.id !== 'file-impor' || !ev.target.files.length) return;
    var fr = new FileReader();
    fr.onload = function () {
      try {
        var data = JSON.parse(fr.result);
        if (!data || typeof data !== 'object' || !('pasien' in data)) throw new Error('bukan cadangan VaksinKu');
        for (var k in kosong) if (!(k in data)) data[k] = JSON.parse(JSON.stringify(kosong[k]));
        S = data; simpan(); render(); toast('Data berhasil dipulihkan.');
      } catch (e) { toast('Berkas tidak dikenali sebagai cadangan VaksinKu.'); }
    };
    fr.readAsText(ev.target.files[0]);
  });

  document.addEventListener('submit', function (ev) {
    ev.preventDefault();
    // catatan: pakai getAttribute('id') — properti f.id bisa tertutup oleh
    // kontrol form yang bernama sama (named property access pada <form>).
    var f = ev.target, formId = f.getAttribute('id');
    var get = function (n) { return (f.elements[n] ? f.elements[n].value : '').trim(); };
    formErr = {};
    if (formId === 'form-pasien') {
      if (!get('nama')) formErr.nama = 'Nama pasien wajib diisi.';
      if (!get('tglLahir')) formErr.tglLahir = 'Tanggal lahir wajib diisi.';
      else if (get('tglLahir') > hariIni()) formErr.tglLahir = 'Tanggal lahir tidak boleh di masa depan.';
      if (Object.keys(formErr).length) { render(); return; }
      var id = get('pid');
      if (id) {
        S.pasien.forEach(function (p) {
          if (p.id !== id) return;
          p.nama = get('nama'); p.tglLahir = get('tglLahir');
          p.jenisKelamin = get('jenisKelamin'); p.hubungan = get('hubungan');
        });
      } else {
        var baru = { id: uid(), nama: get('nama'), tglLahir: get('tglLahir'), jenisKelamin: get('jenisKelamin'), hubungan: get('hubungan') };
        S.pasien.push(baru);
        if (!S.ui.pasienAktif) S.ui.pasienAktif = baru.id;
      }
      simpan(); location.hash = '#/pasien'; toast(id ? 'Data pasien diperbarui.' : 'Pasien ditambahkan.');
      return;
    }
    if (formId === 'form-alamat') {
      if (!get('label')) formErr.label = 'Label wajib diisi.';
      if (!get('kecamatan')) formErr.kecamatan = 'Kecamatan/kota wajib diisi.';
      if (!get('alamat')) formErr.alamat = 'Alamat lengkap wajib diisi.';
      if (Object.keys(formErr).length) { render(); return; }
      var a = { id: uid(), label: get('label'), kecamatan: get('kecamatan'), alamat: get('alamat'), patokan: get('patokan') };
      S.alamat.push(a);
      draft().alamatId = a.id;
      simpan(); location.hash = '#/alamat'; toast('Alamat ditambahkan.');
      return;
    }
    if (formId === 'form-tumbuh') {
      if (!get('berat') && !get('tinggi') && !get('kepala')) {
        formErr.tumbuh = 'Isi minimal salah satu: berat, tinggi, atau lingkar kepala.';
        render(); return;
      }
      S.pertumbuhan.push({
        id: uid(), pasienId: get('pasienId'), tanggal: get('tanggal') || hariIni(),
        berat: get('berat'), tinggi: get('tinggi'), kepala: get('kepala')
      });
      simpan(); location.hash = '#/rekam'; toast('Pengukuran tersimpan.');
      return;
    }
  });

  /* ============================ data contoh ============================ */
  function muatContoh() {
    if (!konfirmasi('Muat data contoh untuk mencoba aplikasi? Data yang ada sekarang akan diganti.')) return;
    var thn = new Date().getFullYear();
    S = JSON.parse(JSON.stringify(kosong));
    S.profil = { nama: 'Contoh Pengguna', hp: '0812xxxxxxx', jenisKelamin: 'Perempuan' };
    var anak = { id: uid(), nama: 'Nadia Contoh', tglLahir: (thn - 5) + '-05-12', jenisKelamin: 'Perempuan', hubungan: 'Anak' };
    var ayah = { id: uid(), nama: 'Bayu Contoh', tglLahir: (thn - 34) + '-02-08', jenisKelamin: 'Laki-laki', hubungan: 'Ayah' };
    S.pasien = [anak, ayah];
    S.ui.pasienAktif = anak.id;
    S.alamat = [{ id: uid(), label: 'Rumah', kecamatan: 'Tanjungpinang Kota, Kepulauan Riau', alamat: 'Jl. Contoh No. 10', patokan: '' }];
    ['Hep B 0', 'Polio 0', 'BCG', 'Combo DPT 1', 'PCV 1', 'Rotavirus 1', 'Combo DPT 2'].forEach(function (lb, i) {
      S.riwayat.push({ id: uid(), pasienId: anak.id, label: lb, tanggal: (thn - 5) + '-0' + Math.min(9, 5 + i) + '-20', sumber: 'jadwal' });
    });
    S.pertumbuhan = [
      { id: uid(), pasienId: anak.id, tanggal: (thn - 1) + '-06-10', berat: '15.2', tinggi: '102', kepala: '49' },
      { id: uid(), pasienId: anak.id, tanggal: thn + '-01-15', berat: '16.8', tinggi: '106', kepala: '49.5' },
      { id: uid(), pasienId: anak.id, tanggal: hariIni(), berat: '17.9', tinggi: '109', kepala: '50' }
    ];
    simpan(); location.hash = '#/beranda'; render();
    toast('Data contoh dimuat. Hapus kapan saja lewat Profil.');
  }

  /* ============================ init ============================ */
  window.addEventListener('hashchange', function () {
    bacaRoute(); sheetHTML = ''; formErr = {};
    if (route.name !== 'booking') errB = {};
    render();
    var sc = document.getElementById('scroll');
    if (sc) sc.scrollTop = 0;
  });
  bacaRoute();
  render();
})();
