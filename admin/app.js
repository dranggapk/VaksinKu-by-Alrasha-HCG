/* VaksinKu by Alrasha Ibumas — Dashboard Manajemen klinik.
   Booking, pendaftaran, penjadwalan, pelayanan, persediaan, dan transaksi.
   Data disimpan lokal di perangkat (localStorage). Tanpa server. */
(function () {
  'use strict';

  var K = window.KATALOG;

  /* ============================ ikon ============================ */
  var ICON = {
    grid: '<rect x="3.5" y="3.5" width="7" height="7" rx="1.6"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.6"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.6"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.6"/>',
    calendar: '<rect x="4" y="5.5" width="16" height="15" rx="2.2"/><path d="M8 3.5v4M16 3.5v4M4 10h16"/>',
    userplus: '<circle cx="10" cy="8" r="3.4"/><path d="M3.6 20c1.1-3.7 3.6-5.6 6.4-5.6 1 0 2 .25 2.9.72"/><path d="M17.5 14.5v6M14.5 17.5h6"/>',
    clock: '<circle cx="12" cy="12" r="8.6"/><path d="M12 7.2v5l3.2 2"/>',
    syringe: '<path d="M13.5 4.5 19.5 10.5"/><path d="M16.5 3 21 7.5"/><path d="M15 7 7.5 14.5 6 19.5l5-1.5L18.5 10.5 15 7Z"/><path d="M10.5 9.5 12.5 11.5M8.5 11.5l2 2"/><path d="M6 19.5 3.5 22"/>',
    box: '<path d="M3.6 7.5 12 3.5l8.4 4v9L12 20.5l-8.4-4v-9Z"/><path d="M3.6 7.5 12 11.5l8.4-4M12 11.5v9"/>',
    receipt: '<path d="M6 3.5h12v17l-2.4-1.6-2.4 1.6-2.4-1.6-2.4 1.6L6 20.5v-17Z"/><path d="M9.2 8h5.6M9.2 12h5.6"/>',
    gear: '<circle cx="12" cy="12" r="3.2"/><path d="M12 3.2v2.4M12 18.4v2.4M20.8 12h-2.4M5.6 12H3.2M18.2 5.8l-1.7 1.7M7.5 16.5l-1.7 1.7M18.2 18.2l-1.7-1.7M7.5 7.5 5.8 5.8"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    close: '<path d="M6 6l12 12M18 6 6 18"/>',
    check: '<path d="M5 12.5l4.5 4.5L19 7"/>',
    chevron: '<path d="M9 5l7 7-7 7"/>',
    back: '<path d="M15 5l-7 7 7 7"/>',
    search: '<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.3-4.3"/>',
    edit: '<path d="M4 20h4L19 9l-4-4L4 16v4Z"/><path d="M14 6l4 4"/>',
    trash: '<path d="M5 7h14M10 7V5h4v2M6.5 7l.8 12a1 1 0 0 0 1 1h7.4a1 1 0 0 0 1-1l.8-12"/><path d="M10 11v6M14 11v6"/>',
    download: '<path d="M12 4v11"/><path d="M7.5 11.5 12 16l4.5-4.5"/><path d="M5 19.5h14"/>',
    upload: '<path d="M12 16V5"/><path d="M7.5 9.5 12 5l4.5 4.5"/><path d="M5 19.5h14"/>',
    warn: '<path d="M12 4.2 21 19.5H3L12 4.2Z"/><path d="M12 10v4.2M12 17v.4"/>',
    info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.6v.6"/>',
    user: '<circle cx="12" cy="8" r="3.6"/><path d="M5 20c1.2-4 4-6 7-6s5.8 2 7 6"/>',
    money: '<rect x="2.8" y="6" width="18.4" height="12" rx="2.2"/><circle cx="12" cy="12" r="2.8"/><path d="M6.2 9.6v4.8M17.8 9.6v4.8"/>'
  };
  function ic(name, size, sw) {
    return '<svg width="' + (size || 18) + '" height="' + (size || 18) + '" viewBox="0 0 24 24" fill="none" ' +
      'stroke="currentColor" stroke-width="' + (sw || 1.8) + '" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
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
  function rpk(n) {
    n = Number(n || 0);
    if (n >= 1e9) return 'Rp' + (n / 1e9).toFixed(n % 1e9 ? 1 : 0).replace('.', ',') + ' M';
    if (n >= 1e6) return 'Rp' + (n / 1e6).toFixed(n % 1e6 ? 1 : 0).replace('.', ',') + ' jt';
    if (n >= 1e3) return 'Rp' + Math.round(n / 1e3) + ' rb';
    return rp(n);
  }
  function angka(s) { return parseInt(String(s).replace(/\D/g, ''), 10) || 0; }
  function salin(v) { return JSON.parse(JSON.stringify(v)); }
  var BULAN = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'];
  var BLN3 = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'];
  var HARI = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'];
  function tgl(iso, bentuk) {
    if (!iso) return '-';
    var p = String(iso).slice(0, 10).split('-');
    if (p.length < 3) return iso;
    var d = new Date(+p[0], +p[1] - 1, +p[2]);
    if (bentuk === 'panjang') return HARI[d.getDay()] + ', ' + (+p[2]) + ' ' + BULAN[+p[1] - 1] + ' ' + p[0];
    if (bentuk === 'pendek') return (+p[2]) + ' ' + BLN3[+p[1] - 1];
    return (+p[2]) + ' ' + BLN3[+p[1] - 1] + ' ' + p[0];
  }
  function hariIni() {
    var d = new Date();
    return new Date(d.getTime() - d.getTimezoneOffset() * 6e4).toISOString().slice(0, 10);
  }
  function geserHari(iso, n) {
    var p = iso.split('-'), d = new Date(+p[0], +p[1] - 1, +p[2] + n);
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  }
  function selisihHari(iso) {
    if (!iso) return null;
    var a = new Date(hariIni()), b = new Date(String(iso).slice(0, 10));
    return Math.round((b - a) / 864e5);
  }
  function umurTeks(lahir) {
    if (!lahir) return '-';
    var l = new Date(lahir), n = new Date();
    var bln = (n.getFullYear() - l.getFullYear()) * 12 + (n.getMonth() - l.getMonth());
    if (n.getDate() < l.getDate()) bln--;
    if (bln < 0) return '-';
    if (bln < 24) return bln + ' bulan';
    var th = Math.floor(bln / 12), sisa = bln % 12;
    return th + ' tahun' + (sisa ? ' ' + sisa + ' bln' : '');
  }
  function inisial(nama) {
    var p = String(nama || '?').trim().split(/\s+/);
    return ((p[0] || '?')[0] + (p.length > 1 ? p[p.length - 1][0] : '')).toUpperCase();
  }

  /* ============================ state ============================ */
  var KEY = 'vaksinku.admin.v1';
  var kosong = {
    versi: 1,
    klinik: { nama: K.klinik[0][0], alamat: K.klinik[0][1], telp: K.brand.callCenter },
    jadwal: { buka: '08:00', tutup: '16:00', durasi: 30, kapasitas: 3, libur: [0] },
    pasien: [], booking: [], layanan: [], stok: [], mutasi: [], transaksi: [],
    urut: { rm: 0, booking: 0, invoice: 0 },
    ui: { tanggalJadwal: '', filterBooking: 'semua', cariPasien: '', cariBooking: '', rentangOmzet: 14 }
  };
  var S, storageOk = true;

  function baca() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return salin(kosong);
      var d = JSON.parse(raw);
      for (var k in kosong) {
        if (!(k in d) || d[k] == null) { d[k] = salin(kosong[k]); continue; }
        var b = kosong[k];
        if (b && typeof b === 'object' && !(b instanceof Array) && typeof d[k] === 'object') {
          for (var sk in b) if (!(sk in d[k])) d[k][sk] = salin(b[sk]);
        }
      }
      return d;
    } catch (e) { storageOk = false; return salin(kosong); }
  }
  function simpan() {
    try { localStorage.setItem(KEY, JSON.stringify(S)); }
    catch (e) { storageOk = false; }
  }
  S = baca();

  function nomorRM() {
    S.urut.rm++;
    return 'RM' + String(S.urut.rm).padStart(5, '0');
  }
  function nomorBooking() {
    S.urut.booking++;
    return 'BK-' + hariIni().replace(/-/g, '').slice(2) + '-' + String(S.urut.booking).padStart(3, '0');
  }
  function nomorInvoice() {
    S.urut.invoice++;
    return 'INV/' + new Date().getFullYear() + '/' + String(S.urut.invoice).padStart(4, '0');
  }

  /* ============================ katalog ============================ */
  function vaksinById(id) {
    for (var i = 0; i < K.harga.length; i++) if (K.harga[i].id === id) return K.harga[i];
    return null;
  }
  function vaksinNama(id) {
    var v = vaksinById(id);
    return v ? v.kategori + ' — ' + v.merk : '(vaksin tidak dikenal)';
  }
  function hargaVaksin(id, dokter) {
    var v = vaksinById(id);
    if (!v) return 0;
    var s = dokter === 'spesialis' ? v.spesialis : v.umum;
    return s ? angka(s) : 0;
  }
  var STATUS = {
    baru: { label: 'Baru', chip: 'grey' },
    terkonfirmasi: { label: 'Terkonfirmasi', chip: 'teal' },
    hadir: { label: 'Hadir', chip: 'mag' },
    selesai: { label: 'Selesai', chip: 'green' },
    batal: { label: 'Batal', chip: 'danger' },
    mangkir: { label: 'Tidak hadir', chip: 'amber' }
  };

  /* ============================ turunan ============================ */
  function pasienById(id) {
    for (var i = 0; i < S.pasien.length; i++) if (S.pasien[i].id === id) return S.pasien[i];
    return null;
  }
  function namaPasien(id) {
    var p = pasienById(id);
    return p ? p.nama : '(pasien terhapus)';
  }
  function bookingById(id) {
    for (var i = 0; i < S.booking.length; i++) if (S.booking[i].id === id) return S.booking[i];
    return null;
  }
  function totalBooking(b) {
    var t = 0;
    (b.vaksinIds || []).forEach(function (id) { t += hargaVaksin(id, b.dokterTarif); });
    return t;
  }
  function bookingTanggal(iso) {
    return S.booking.filter(function (b) {
      return b.tanggal === iso && b.status !== 'batal';
    });
  }
  function slotJam() {
    var j = S.jadwal, out = [];
    function menit(t) { var p = String(t).split(':'); return (+p[0]) * 60 + (+p[1] || 0); }
    var a = menit(j.buka), z = menit(j.tutup), d = Math.max(5, +j.durasi || 30);
    for (var m = a; m + d <= z; m += d) {
      out.push(String(Math.floor(m / 60)).padStart(2, '0') + ':' + String(m % 60).padStart(2, '0'));
    }
    return out;
  }
  function hariLibur(iso) {
    var p = iso.split('-'), d = new Date(+p[0], +p[1] - 1, +p[2]);
    return (S.jadwal.libur || []).indexOf(d.getDay()) >= 0;
  }
  function isiSlot(iso, jam) {
    return bookingTanggal(iso).filter(function (b) { return b.jam === jam; }).length;
  }

  /* ---- persediaan ---- */
  function batchVaksin(vaksinId) {
    return S.stok.filter(function (s) { return s.vaksinId === vaksinId && s.sisa > 0; })
      .sort(function (a, b) { return String(a.kedaluwarsa).localeCompare(String(b.kedaluwarsa)); });
  }
  function sisaVaksin(vaksinId) {
    return S.stok.filter(function (s) { return s.vaksinId === vaksinId; })
      .reduce(function (n, s) { return n + (+s.sisa || 0); }, 0);
  }
  function stokRingkas() {
    var peta = {}, urut = [];
    S.stok.forEach(function (s) {
      if (!peta[s.vaksinId]) { peta[s.vaksinId] = { vaksinId: s.vaksinId, sisa: 0, minimum: 0, batch: [] }; urut.push(s.vaksinId); }
      var g = peta[s.vaksinId];
      g.sisa += (+s.sisa || 0);
      g.minimum = Math.max(g.minimum, +s.minimum || 0);
      g.batch.push(s);
    });
    return urut.map(function (id) {
      var g = peta[id];
      g.batch.sort(function (a, b) { return String(a.kedaluwarsa).localeCompare(String(b.kedaluwarsa)); });
      g.nama = vaksinNama(id);
      g.kritis = g.minimum > 0 && g.sisa <= g.minimum;
      g.habis = g.sisa === 0;
      var dekat = g.batch.filter(function (b) {
        var d = selisihHari(b.kedaluwarsa);
        return b.sisa > 0 && d !== null && d <= 90;
      });
      g.dekatTempo = dekat.length;
      g.lewatTempo = g.batch.filter(function (b) {
        var d = selisihHari(b.kedaluwarsa);
        return b.sisa > 0 && d !== null && d < 0;
      }).length;
      return g;
    }).sort(function (a, b) { return a.nama.localeCompare(b.nama); });
  }
  function peringatanStok() {
    return stokRingkas().filter(function (g) { return g.habis || g.kritis || g.dekatTempo; });
  }

  /* ---- transaksi ---- */
  function belumBayar() {
    return S.transaksi.filter(function (t) { return t.status !== 'lunas'; });
  }
  function omzetHarian(n) {
    var out = [];
    for (var i = n - 1; i >= 0; i--) {
      var d = geserHari(hariIni(), -i), jumlah = 0;
      S.transaksi.forEach(function (t) {
        if (t.status === 'lunas' && String(t.tglBayar || '').slice(0, 10) === d) jumlah += t.total;
      });
      out.push({ tanggal: d, nilai: jumlah });
    }
    return out;
  }

  /* ============================ grafik kolom ============================ */
  /* Satu seri = satu warna (sequential), tanpa legenda; nilai hanya dilabeli
     pada kolom tertinggi, sisanya lewat sumbu, tooltip, dan tampilan tabel. */
  function sumbuRapi(maks) {
    if (maks <= 0) return [0, 1];
    var pangkat = Math.pow(10, Math.floor(Math.log(maks) / Math.LN10));
    var langkah = pangkat;
    [1, 2, 2.5, 5, 10].some(function (f) {
      if (maks / (pangkat * f) <= 2) { langkah = pangkat * f; return true; }
      return false;
    });
    var atas = Math.ceil(maks / langkah) * langkah;
    return [0, atas / 2, atas];
  }
  /* Grafik digambar ulang sesuai lebar wadahnya (lihat pasangGrafik) agar
     1 unit viewBox = 1 piksel: ukuran teks dan tebal kolom tetap apa adanya
     di layar lebar maupun sempit. */
  var GRAFIK = {};
  function grafikKolom(id, data, opt) {
    GRAFIK[id] = { data: data, opt: opt || {} };
    return '<div class="chart" id="' + id + '" data-grafik="' + id + '" style="min-height:' + TINGGI_GRAFIK + 'px;"></div>';
  }
  var TINGGI_GRAFIK = 230;
  function svgKolom(W, data, opt) {
    var H = TINGGI_GRAFIK, kiri = 62, kanan = 12, atas = 22, bawah = 32;
    var pw = Math.max(80, W - kiri - kanan), ph = H - atas - bawah;
    var maks = data.reduce(function (m, d) { return Math.max(m, d.nilai); }, 0);
    var tick = sumbuRapi(maks), skala = tick[2] || 1;
    var band = pw / Math.max(1, data.length);
    var lebar = Math.min(24, Math.max(5, band - 10));
    var iMaks = -1;
    data.forEach(function (d, i) { if (d.nilai > 0 && (iMaks < 0 || d.nilai > data[iMaks].nilai)) iMaks = i; });
    // label sumbu-x dijarangkan bila bandnya terlalu sempit untuk teks
    var lompat = Math.max(1, opt.tiapN || 1, Math.ceil(42 / band));

    var svg = '<svg viewBox="0 0 ' + W + ' ' + H + '" width="' + W + '" height="' + H +
      '" role="img" aria-label="' + h(opt.alt || 'Grafik') + '">';
    tick.forEach(function (t) {
      var y = atas + ph - (t / skala) * ph;
      svg += '<line class="sumbu" x1="' + kiri + '" y1="' + y.toFixed(1) + '" x2="' + (W - kanan) + '" y2="' + y.toFixed(1) + '"/>' +
        '<text x="' + (kiri - 9) + '" y="' + (y + 3.5).toFixed(1) + '" text-anchor="end">' + h(opt.tick ? opt.tick(t) : t) + '</text>';
    });
    data.forEach(function (d, i) {
      var x = kiri + band * i + (band - lebar) / 2;
      var tinggi = skala ? (d.nilai / skala) * ph : 0;
      var y = atas + ph - tinggi;
      if (tinggi > 0) {
        var r = Math.min(4, lebar / 2, tinggi);
        svg += '<path class="kolom" d="M' + x.toFixed(1) + ' ' + (atas + ph) +
          ' V' + (y + r).toFixed(1) + ' a' + r + ' ' + r + ' 0 0 1 ' + r + ' -' + r +
          ' h' + (lebar - 2 * r).toFixed(1) + ' a' + r + ' ' + r + ' 0 0 1 ' + r + ' ' + r +
          ' V' + (atas + ph) + ' Z"/>';
      }
      // area sentuh selebar band, jadi kolom tipis pun mudah dibidik
      svg += '<rect class="hit" data-i="' + i + '" x="' + (kiri + band * i).toFixed(1) + '" y="' + atas +
        '" width="' + band.toFixed(1) + '" height="' + ph + '"><title>' +
        h(d.label + ': ' + (opt.nilaiTeks ? opt.nilaiTeks(d.nilai) : d.nilai)) + '</title></rect>';
      if (i === iMaks) {
        svg += '<text class="nilai" x="' + (x + lebar / 2).toFixed(1) + '" y="' + (y - 7).toFixed(1) + '" text-anchor="middle">' +
          h(opt.nilaiTeks ? opt.nilaiTeks(d.nilai) : d.nilai) + '</text>';
      }
      if (i % lompat === 0 || i === data.length - 1) {
        svg += '<text x="' + (kiri + band * i + band / 2).toFixed(1) + '" y="' + (H - 11) + '" text-anchor="middle">' + h(d.label) + '</text>';
      }
    });
    svg += '<line class="sumbu" x1="' + kiri + '" y1="' + (atas + ph) + '" x2="' + (W - kanan) + '" y2="' + (atas + ph) + '"/></svg>';
    return svg;
  }
  function tabelNilai(data, kolomNilai, format) {
    return '<div class="tabel-gulir"><table class="tbl"><thead><tr><th>Tanggal</th><th class="num">' +
      h(kolomNilai) + '</th></tr></thead><tbody>' +
      data.map(function (d) {
        return '<tr><td>' + h(d.penuh || d.label) + '</td><td class="num">' + h(format(d.nilai)) + '</td></tr>';
      }).join('') + '</tbody></table></div>';
  }

  /* ============================ kerangka ============================ */
  var MENU = [
    ['Operasional', [
      ['ringkasan', 'grid', 'Ringkasan'],
      ['booking', 'calendar', 'Booking'],
      ['pendaftaran', 'userplus', 'Pendaftaran'],
      ['penjadwalan', 'clock', 'Penjadwalan'],
      ['pelayanan', 'syringe', 'Pelayanan']
    ]],
    ['Penunjang', [
      ['persediaan', 'box', 'Persediaan'],
      ['transaksi', 'receipt', 'Transaksi'],
      ['pengaturan', 'gear', 'Pengaturan']
    ]]
  ];
  var JUDUL = {
    ringkasan: ['Ringkasan', 'Gambaran operasional klinik hari ini'],
    booking: ['Booking', 'Reservasi masuk, konfirmasi, dan penjadwalan ulang'],
    pendaftaran: ['Pendaftaran Pasien', 'Data induk pasien dan nomor rekam medis'],
    penjadwalan: ['Penjadwalan', 'Slot layanan, kapasitas, dan beban per hari'],
    pelayanan: ['Pelayanan', 'Antrean hari ini, pencatatan vaksinasi, dan KIPI'],
    persediaan: ['Persediaan Vaksin', 'Stok per batch, kedaluwarsa, dan mutasi'],
    transaksi: ['Transaksi', 'Tagihan, pembayaran, dan rekap pendapatan'],
    pengaturan: ['Pengaturan', 'Identitas klinik, jam layanan, dan data aplikasi']
  };

  var route = 'ringkasan', panel = null, formErr = {}, app = document.getElementById('app');

  function bacaRoute() {
    var r = (location.hash || '#/ringkasan').replace(/^#\//, '').split('/')[0];
    route = JUDUL[r] ? r : 'ringkasan';
  }
  function lencana(nama) {
    if (nama === 'booking') {
      var n = S.booking.filter(function (b) { return b.status === 'baru'; }).length;
      return n ? { teks: n, warn: true } : null;
    }
    if (nama === 'pelayanan') {
      var a = antreanHariIni().length;
      return a ? { teks: a } : null;
    }
    if (nama === 'persediaan') {
      var p = peringatanStok().length;
      return p ? { teks: p, warn: true } : null;
    }
    if (nama === 'transaksi') {
      var t = belumBayar().length;
      return t ? { teks: t } : null;
    }
    return null;
  }
  function sidebar() {
    var out = '<aside class="sidebar"><div class="merk">' +
      '<img src="' + K.logoMark + '" alt="VaksinKu">' +
      '<div><div class="t">Dashboard</div></div></div>';
    MENU.forEach(function (sec) {
      out += '<div class="navsec">' + h(sec[0]) + '</div>';
      sec[1].forEach(function (it) {
        var l = lencana(it[0]);
        out += '<button class="navitem' + (route === it[0] ? ' on' : '') + '" data-act="go" data-arg="' + it[0] + '">' +
          ic(it[1], 18) + '<span>' + h(it[2]) + '</span>' +
          (l ? '<span class="jml' + (l.warn ? ' warn' : '') + '">' + h(String(l.teks)) + '</span>' : '') +
          '</button>';
      });
    });
    out += '<div class="kaki">' + h(S.klinik.nama) + '<br>Data tersimpan di perangkat ini</div></aside>';
    return out;
  }
  function render() {
    var isi;
    switch (route) {
      case 'booking': isi = scBooking(); break;
      case 'pendaftaran': isi = scPendaftaran(); break;
      case 'penjadwalan': isi = scPenjadwalan(); break;
      case 'pelayanan': isi = scPelayanan(); break;
      case 'persediaan': isi = scPersediaan(); break;
      case 'transaksi': isi = scTransaksi(); break;
      case 'pengaturan': isi = scPengaturan(); break;
      default: isi = scRingkasan();
    }
    var j = JUDUL[route];
    app.innerHTML = '<div class="shell">' + sidebar() +
      '<main class="utama"><header class="topbar">' +
      '<div class="grow"><h1>' + h(j[0]) + '</h1><div class="sub">' + h(j[1]) + '</div></div>' +
      (isi.aksi || '') + '</header>' +
      '<div class="isi">' + isi.body + '</div></main>' +
      (panel ? panelHTML() : '') + '</div>';
    pasangGrafik();
  }
  function toast(pesan) {
    var el = document.createElement('div');
    el.className = 'toast';
    el.innerHTML = '<div>' + h(pesan) + '</div>';
    document.body.appendChild(el);
    requestAnimationFrame(function () { el.firstChild.classList.add('on'); });
    setTimeout(function () {
      el.firstChild.classList.remove('on');
      setTimeout(function () { el.remove(); }, 240);
    }, 2600);
  }
  function konfirmasi(p) { return window.confirm(p); }
  function kosongPesan(teks, tombol) {
    return '<div class="kosong">' + h(teks) + (tombol ? '<div style="margin-top:14px;">' + tombol + '</div>' : '') + '</div>';
  }
  function statTile(label, nilai, sub) {
    return '<div class="stat"><div class="lbl2">' + h(label) + '</div>' +
      '<div class="val">' + h(String(nilai)) + '</div>' +
      (sub ? '<div class="sub2">' + h(sub) + '</div>' : '') + '</div>';
  }
  function chipStatus(st) {
    var s = STATUS[st] || { label: st, chip: 'grey' };
    return '<span class="chip ' + s.chip + '">' + h(s.label) + '</span>';
  }

  /* tooltip grafik dipasang setelah render */
  function pasangGrafik() {
    [].forEach.call(document.querySelectorAll('[data-grafik]'), function (box) {
      var g = GRAFIK[box.getAttribute('data-grafik')];
      if (!g) return;
      var W = Math.round(box.clientWidth) || 720;
      box.innerHTML = svgKolom(W, g.data, g.opt);
      var tip = null;
      [].forEach.call(box.querySelectorAll('.hit'), function (hit) {
        function tampil() {
          var d = g.data[+hit.getAttribute('data-i')];
          if (!d) return;
          if (!tip) { tip = document.createElement('div'); tip.className = 'tip'; box.appendChild(tip); }
          tip.innerHTML = '<b>' + h(g.opt.nilaiTeks ? g.opt.nilaiTeks(d.nilai) : String(d.nilai)) + '</b>' +
            h(d.penuh || d.label);
          var rb = box.getBoundingClientRect(), rh = hit.getBoundingClientRect();
          tip.style.left = (rh.left - rb.left + rh.width / 2) + 'px';
          tip.style.top = (rh.top - rb.top - 6) + 'px';
        }
        function sembunyi() { if (tip) { tip.remove(); tip = null; } }
        hit.setAttribute('tabindex', '0');
        hit.addEventListener('mouseenter', tampil);
        hit.addEventListener('mouseleave', sembunyi);
        hit.addEventListener('focus', tampil);
        hit.addEventListener('blur', sembunyi);
      });
    });
  }

  /* ============================ layar: ringkasan ============================ */
  function antreanHariIni() {
    return S.booking.filter(function (b) {
      return b.tanggal === hariIni() && ['terkonfirmasi', 'hadir', 'baru'].indexOf(b.status) >= 0;
    }).sort(function (a, b) { return String(a.jam).localeCompare(String(b.jam)); });
  }
  function scRingkasan() {
    var hari = hariIni();
    var bookingHari = bookingTanggal(hari);
    var selesaiHari = S.booking.filter(function (b) { return b.tanggal === hari && b.status === 'selesai'; });
    var bulan = hari.slice(0, 7);
    var omzetBulan = S.transaksi.reduce(function (n, t) {
      return n + (t.status === 'lunas' && String(t.tglBayar || '').slice(0, 7) === bulan ? t.total : 0);
    }, 0);
    var tunggak = belumBayar().reduce(function (n, t) { return n + (t.total - (t.dibayar || 0)); }, 0);

    var body = '<div class="lebar stack g18">';
    body += '<div class="grid g-4">' +
      statTile('Booking hari ini', bookingHari.length, selesaiHari.length + ' sudah selesai') +
      statTile('Pasien terdaftar', S.pasien.length, 'Total data induk') +
      statTile('Pendapatan bulan ini', rpk(omzetBulan), tgl(hari, 'panjang').split(', ')[1]) +
      statTile('Tagihan belum lunas', rpk(tunggak), belumBayar().length + ' tagihan') +
      '</div>';

    /* grafik pendapatan */
    var n = +S.ui.rentangOmzet || 14;
    var data = omzetHarian(n).map(function (d) {
      return { label: tgl(d.tanggal, 'pendek'), penuh: tgl(d.tanggal, 'panjang'), nilai: d.nilai };
    });
    var totalPeriode = data.reduce(function (a, d) { return a + d.nilai; }, 0);
    body += '<section class="kartu stack g14">' +
      '<div class="row mid between wrap g12">' +
      '<div><div class="judul-sec">Pendapatan harian</div>' +
      '<div class="hint">Transaksi berstatus lunas, berdasarkan tanggal pembayaran. Total ' + n + ' hari: ' + h(rp(totalPeriode)) + '.</div></div>' +
      '<div class="row g8">' +
      [7, 14, 30].map(function (x) {
        return '<button class="pill' + (n === x ? ' on' : '') + '" data-act="rentang" data-arg="' + x + '">' + x + ' hari</button>';
      }).join('') +
      '<button class="pill' + (S.ui.tabelOmzet ? ' on' : '') + '" data-act="tabel-omzet">Tabel</button></div></div>' +
      (S.ui.tabelOmzet
        ? tabelNilai(data, 'Pendapatan', rp)
        : (totalPeriode
          ? grafikKolom('g-omzet', data, {
            alt: 'Pendapatan harian ' + n + ' hari terakhir',
            tick: rpk, nilaiTeks: rp, tiapN: n > 14 ? 5 : (n > 7 ? 2 : 1)
          })
          : kosongPesan('Belum ada pembayaran lunas pada ' + n + ' hari terakhir.'))) +
      '</section>';

    body += '<div class="grid g-23">';
    /* antrean hari ini */
    var antre = antreanHariIni();
    body += '<section class="kartu stack g12"><div class="row mid between">' +
      '<div class="judul-sec">Antrean hari ini</div>' +
      '<button class="linkbtn" data-act="go" data-arg="pelayanan">Buka pelayanan</button></div>';
    if (!antre.length) {
      body += kosongPesan('Tidak ada booking terjadwal hari ini.');
    } else {
      body += '<div class="stack g8">' + antre.slice(0, 6).map(function (b, i) {
        return '<div class="antre"><div class="nomor">' + (i + 1) + '</div>' +
          '<div class="grow"><div style="font-weight:700;">' + h(namaPasien(b.pasienId)) + '</div>' +
          '<div class="tiny muted">' + h(b.jam) + ' · ' + h((b.vaksinIds || []).map(function (v) {
            return (vaksinById(v) || {}).kategori || '-';
          }).join(', ') || 'Vaksin belum dipilih') + '</div></div>' +
          chipStatus(b.status) + '</div>';
      }).join('') + '</div>';
      if (antre.length > 6) body += '<div class="tiny muted">+' + (antre.length - 6) + ' lagi di layar Pelayanan.</div>';
    }
    body += '</section>';

    /* peringatan stok */
    var waspada = peringatanStok();
    body += '<section class="kartu stack g12"><div class="row mid between">' +
      '<div class="judul-sec">Perhatian persediaan</div>' +
      '<button class="linkbtn" data-act="go" data-arg="persediaan">Kelola</button></div>';
    if (!waspada.length) {
      body += kosongPesan(S.stok.length ? 'Semua stok aman.' : 'Belum ada data stok.');
    } else {
      body += '<div class="stack g12">' + waspada.slice(0, 6).map(function (g) {
        var sebab = g.habis ? ['Stok habis', 'danger'] : (g.lewatTempo ? ['Ada batch kedaluwarsa', 'danger'] :
          (g.kritis ? ['Di bawah stok minimum', 'amber'] : ['Mendekati kedaluwarsa', 'amber']));
        var persen = g.minimum ? Math.min(100, Math.round(g.sisa / (g.minimum * 2) * 100)) : (g.sisa ? 100 : 0);
        var kelasMeter = g.habis ? 'bad' : (g.kritis ? 'warn' : '');
        return '<div class="stack g6"><div class="row mid between g8">' +
          '<span class="small" style="font-weight:700;">' + h(g.nama) + '</span>' +
          '<span class="chip ' + sebab[1] + '">' + ic('warn', 12) + ' ' + h(sebab[0]) + '</span></div>' +
          '<div class="meter ' + kelasMeter + '"><i style="width:' + persen + '%;"></i></div>' +
          '<div class="tiny muted">Sisa ' + g.sisa + ' dosis' + (g.minimum ? ' · minimum ' + g.minimum : '') + '</div></div>';
      }).join('') + '</div>';
    }
    body += '</section></div>';

    if (!S.pasien.length && !S.stok.length) {
      body += '<section class="kartu stack g12"><div class="judul-sec">Mulai dari mana?</div>' +
        '<div class="hint">Dashboard ini kosong sampai Anda mengisinya. Urutan yang disarankan: daftarkan pasien, ' +
        'masukkan stok vaksin, lalu buat booking. Semua angka di layar ini dihitung dari data itu.</div>' +
        '<div class="row g8 wrap">' +
        '<button class="btn primary sm" data-act="go" data-arg="pendaftaran">' + ic('userplus', 15) + ' Daftarkan pasien</button>' +
        '<button class="btn outline sm" data-act="go" data-arg="persediaan">' + ic('box', 15) + ' Isi persediaan</button>' +
        '<button class="btn outline sm" data-act="contoh">Muat data contoh</button></div></section>';
    }
    body += '</div>';
    return { body: body };
  }

  /* ============================ layar: pendaftaran ============================ */
  function scPendaftaran() {
    var q = (S.ui.cariPasien || '').toLowerCase();
    var daftar = S.pasien.filter(function (p) {
      return !q || (p.nama + ' ' + p.noRM + ' ' + (p.hp || '')).toLowerCase().indexOf(q) >= 0;
    }).slice().sort(function (a, b) { return b.dibuat.localeCompare(a.dibuat); });

    var body = '<div class="lebar stack g14">';
    body += '<div class="row mid g12 wrap">' +
      '<div style="position:relative;flex:1;min-width:220px;">' +
      '<input class="input" id="cari-pasien" placeholder="Cari nama, nomor RM, atau nomor HP..." value="' + h(S.ui.cariPasien || '') + '" style="padding-left:34px;">' +
      '<span style="position:absolute;left:11px;top:10px;color:var(--ink-4);">' + ic('search', 17) + '</span></div>' +
      '<span class="small muted">' + daftar.length + ' dari ' + S.pasien.length + ' pasien</span></div>';

    body += '<section class="kartu rapat"><div class="tabel-gulir"><table class="tbl"><thead><tr>' +
      '<th>No. RM</th><th>Nama</th><th>Usia</th><th>Jenis kelamin</th><th>Kontak</th><th class="num">Riwayat</th><th></th>' +
      '</tr></thead><tbody>';
    if (!daftar.length) {
      body += '<tr><td colspan="7">' + kosongPesan(
        S.pasien.length ? 'Tidak ada pasien yang cocok dengan pencarian.' : 'Belum ada pasien terdaftar.',
        '<button class="btn primary sm" data-act="form-pasien">' + ic('plus', 15) + ' Daftarkan pasien</button>') + '</td></tr>';
    } else {
      daftar.forEach(function (p) {
        var jml = S.layanan.filter(function (l) { return l.pasienId === p.id; }).length;
        body += '<tr><td style="font-variant-numeric:tabular-nums;font-weight:700;">' + h(p.noRM) + '</td>' +
          '<td><div class="row mid g10"><span class="nomor" style="width:30px;height:30px;font-size:12px;border-radius:9px;">' + h(inisial(p.nama)) + '</span>' +
          '<span style="font-weight:600;">' + h(p.nama) + '</span></div></td>' +
          '<td class="small muted">' + h(umurTeks(p.tglLahir)) + '</td>' +
          '<td class="small muted">' + h(p.jk || '-') + '</td>' +
          '<td class="small muted">' + h(p.hp || '-') + '</td>' +
          '<td class="num small muted">' + jml + ' vaksinasi</td>' +
          '<td class="kanan"><button class="linkbtn" data-act="form-pasien" data-arg="' + p.id + '">Ubah</button></td></tr>';
      });
    }
    body += '</tbody></table></div></section>';
    body += '<div class="hint">Nomor rekam medis dibuat otomatis dan berurutan. Pasien yang sudah pernah ' +
      'dilayani tidak bisa dihapus agar riwayat vaksinasi dan tagihannya tetap utuh.</div>';
    body += '</div>';
    return {
      body: body,
      aksi: '<button class="btn primary" data-act="form-pasien">' + ic('plus', 16) + ' Pasien baru</button>'
    };
  }

  /* ============================ layar: booking ============================ */
  function scBooking() {
    var f = S.ui.filterBooking || 'semua';
    var q = (S.ui.cariBooking || '').toLowerCase();
    var daftar = S.booking.filter(function (b) {
      if (f === 'hari-ini' && b.tanggal !== hariIni()) return false;
      if (f === 'mendatang' && !(b.tanggal >= hariIni() && ['baru', 'terkonfirmasi'].indexOf(b.status) >= 0)) return false;
      if (STATUS[f] && b.status !== f) return false;
      if (q && (b.kode + ' ' + namaPasien(b.pasienId)).toLowerCase().indexOf(q) < 0) return false;
      return true;
    }).slice().sort(function (a, b) {
      return (b.tanggal + b.jam).localeCompare(a.tanggal + a.jam);
    });

    var tapis = [['semua', 'Semua'], ['hari-ini', 'Hari ini'], ['mendatang', 'Mendatang'],
      ['baru', 'Baru'], ['terkonfirmasi', 'Terkonfirmasi'], ['selesai', 'Selesai'], ['batal', 'Batal']];

    var body = '<div class="lebar stack g14">';
    body += '<div class="row mid g10 wrap">' + tapis.map(function (t) {
      var jml = t[0] === 'semua' ? S.booking.length : S.booking.filter(function (b) {
        if (t[0] === 'hari-ini') return b.tanggal === hariIni();
        if (t[0] === 'mendatang') return b.tanggal >= hariIni() && ['baru', 'terkonfirmasi'].indexOf(b.status) >= 0;
        return b.status === t[0];
      }).length;
      return '<button class="pill' + (f === t[0] ? ' on' : '') + '" data-act="filter-booking" data-arg="' + t[0] + '">' +
        h(t[1]) + ' · ' + jml + '</button>';
    }).join('') + '</div>';

    body += '<div style="position:relative;max-width:360px;">' +
      '<input class="input" id="cari-booking" placeholder="Cari kode booking atau nama pasien..." value="' + h(S.ui.cariBooking || '') + '" style="padding-left:34px;">' +
      '<span style="position:absolute;left:11px;top:10px;color:var(--ink-4);">' + ic('search', 17) + '</span></div>';

    body += '<section class="kartu rapat"><div class="tabel-gulir"><table class="tbl"><thead><tr>' +
      '<th>Kode</th><th>Pasien</th><th>Jadwal</th><th>Layanan</th><th>Vaksin</th><th class="num">Tagihan</th><th>Status</th><th></th>' +
      '</tr></thead><tbody>';
    if (!daftar.length) {
      body += '<tr><td colspan="8">' + kosongPesan(
        S.booking.length ? 'Tidak ada booking pada filter ini.' : 'Belum ada booking.',
        '<button class="btn primary sm" data-act="form-booking">' + ic('plus', 15) + ' Buat booking</button>') + '</td></tr>';
    } else {
      daftar.forEach(function (b) {
        body += '<tr><td style="font-variant-numeric:tabular-nums;font-weight:700;">' + h(b.kode) + '</td>' +
          '<td style="font-weight:600;">' + h(namaPasien(b.pasienId)) + '</td>' +
          '<td class="small"><div>' + h(tgl(b.tanggal)) + '</div><div class="muted">' + h(b.jam || '-') + '</div></td>' +
          '<td class="small muted">' + h(b.layanan || '-') + '</td>' +
          '<td class="small muted">' + h((b.vaksinIds || []).map(function (v) {
            return (vaksinById(v) || {}).kategori || '-';
          }).join(', ') || '-') + '</td>' +
          '<td class="num">' + h(rp(totalBooking(b))) + '</td>' +
          '<td>' + chipStatus(b.status) + '</td>' +
          '<td class="kanan"><button class="linkbtn" data-act="buka-booking" data-arg="' + b.id + '">Detail</button></td></tr>';
      });
    }
    body += '</tbody></table></div></section>';
    body += '<div class="hint">Booking dari aplikasi pasien tiba lewat WhatsApp, lalu dicatat di sini oleh petugas — ' +
      'belum ada sambungan otomatis karena dashboard ini berjalan tanpa server. Cadangan .json dari aplikasi pasien ' +
      'bisa diimpor lewat Pengaturan.</div>';
    body += '</div>';
    return {
      body: body,
      aksi: '<button class="btn primary" data-act="form-booking">' + ic('plus', 16) + ' Booking baru</button>'
    };
  }

  /* ============================ layar: penjadwalan ============================ */
  function scPenjadwalan() {
    var iso = S.ui.tanggalJadwal || hariIni();
    var slots = slotJam(), libur = hariLibur(iso), kap = Math.max(1, +S.jadwal.kapasitas || 1);
    var isiHari = bookingTanggal(iso);
    var terpakai = isiHari.length, daya = libur ? 0 : slots.length * kap;

    var body = '<div class="lebar stack g18">';
    body += '<section class="kartu stack g14">' +
      '<div class="row mid between wrap g12">' +
      '<div class="row mid g8">' +
      '<button class="ikonbtn" data-act="geser-hari" data-arg="-1" aria-label="Hari sebelumnya">' + ic('back', 16) + '</button>' +
      '<input class="input" type="date" id="tgl-jadwal" value="' + h(iso) + '" style="width:168px;">' +
      '<button class="ikonbtn" data-act="geser-hari" data-arg="1" aria-label="Hari berikutnya">' + ic('chevron', 16) + '</button>' +
      '<button class="btn outline sm" data-act="jadwal-hari-ini">Hari ini</button></div>' +
      '<div class="row mid g10">' +
      (libur ? '<span class="chip danger">' + ic('warn', 12) + ' Hari libur</span>'
        : '<span class="chip ' + (terpakai >= daya ? 'danger' : (terpakai / (daya || 1) > .7 ? 'amber' : 'teal')) + '">' +
          terpakai + ' / ' + daya + ' kapasitas terpakai</span>') +
      '</div></div>' +
      '<div class="judul-sec">' + h(tgl(iso, 'panjang')) + '</div>';

    if (libur) {
      body += kosongPesan('Hari ini ditandai libur pada pengaturan jam layanan, jadi tidak ada slot yang dibuka.');
      // booking yang sudah terlanjur ada tetap ditampilkan — jangan sampai hilang
      // dari pandangan hanya karena harinya kemudian ditandai libur
      if (isiHari.length) {
        body += '<div class="kartu" style="background:var(--danger-tint);border-color:transparent;">' +
          '<div class="small" style="font-weight:700;color:var(--danger);">' + isiHari.length +
          ' booking masih terjadwal pada hari libur ini</div>' +
          '<div class="tiny" style="color:var(--danger);margin-top:4px;">Jadwalkan ulang atau batalkan lewat detail masing-masing.</div>' +
          '<div class="stack g6" style="margin-top:12px;">' + isiHari.map(function (b) {
            return '<button class="row mid g10" style="background:#fff;border:1px solid var(--line);border-radius:10px;padding:9px 11px;width:100%;text-align:left;cursor:pointer;" ' +
              'data-act="buka-booking" data-arg="' + b.id + '">' +
              '<span class="small" style="font-weight:700;width:52px;">' + h(b.jam || '-') + '</span>' +
              '<span class="small grow">' + h(namaPasien(b.pasienId)) + '</span>' + chipStatus(b.status) + '</button>';
          }).join('') + '</div></div>';
      }
    } else if (!slots.length) {
      body += kosongPesan('Jam buka dan tutup belum menghasilkan satu slot pun — periksa pengaturan.');
    } else {
      body += '<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(148px,1fr));">' +
        slots.map(function (jam) {
          var isiJ = isiHari.filter(function (b) { return b.jam === jam; });
          var kelas = isiJ.length >= kap ? ' penuh' : (isiJ.length / kap >= .67 ? ' ramai' : '');
          return '<div class="slot' + kelas + '"><div class="row mid between">' +
            '<span class="jam">' + h(jam) + '</span>' +
            '<span class="tiny" style="font-weight:700;">' + isiJ.length + '/' + kap + '</span></div>' +
            (isiJ.length
              ? '<div class="stack g4">' + isiJ.map(function (b) {
                return '<button class="tiny" style="background:none;border:0;padding:0;text-align:left;cursor:pointer;color:var(--ink-2);" ' +
                  'data-act="buka-booking" data-arg="' + b.id + '">· ' + h(namaPasien(b.pasienId)) + '</button>';
              }).join('') + '</div>'
              : '<div class="tiny muted">kosong</div>') +
            '</div>';
        }).join('') + '</div>';
    }
    body += '</section>';

    /* beban 14 hari ke depan */
    var depan = [];
    for (var i = 0; i < 14; i++) {
      var d = geserHari(hariIni(), i);
      depan.push({ label: tgl(d, 'pendek'), penuh: tgl(d, 'panjang'), nilai: bookingTanggal(d).length });
    }
    var adaBeban = depan.some(function (d) { return d.nilai > 0; });
    body += '<section class="kartu stack g14">' +
      '<div><div class="judul-sec">Beban 14 hari ke depan</div>' +
      '<div class="hint">Jumlah booking per hari (di luar yang dibatalkan). Kapasitas harian saat ini ' + daya + ' kunjungan.</div></div>' +
      (adaBeban
        ? grafikKolom('g-beban', depan, { alt: 'Jumlah booking per hari, 14 hari ke depan', tiapN: 2 })
        : kosongPesan('Belum ada booking terjadwal dalam 14 hari ke depan.')) +
      '</section>';

    body += '</div>';
    return {
      body: body,
      aksi: '<button class="btn primary" data-act="form-booking">' + ic('plus', 16) + ' Booking baru</button>'
    };
  }

  /* ============================ layar: pelayanan ============================ */
  function scPelayanan() {
    var hari = hariIni();
    var antre = antreanHariIni();
    var selesai = S.booking.filter(function (b) { return b.tanggal === hari && b.status === 'selesai'; });

    var body = '<div class="lebar stack g18">';
    body += '<div class="grid g-3">' +
      statTile('Menunggu', antre.filter(function (b) { return b.status !== 'hadir'; }).length, 'Belum check-in') +
      statTile('Sedang dilayani', antre.filter(function (b) { return b.status === 'hadir'; }).length, 'Sudah check-in') +
      statTile('Selesai hari ini', selesai.length, 'Tercatat di rekam medis') +
      '</div>';

    body += '<section class="kartu stack g12"><div class="judul-sec">Antrean ' + h(tgl(hari, 'panjang')) + '</div>';
    if (!antre.length) {
      body += kosongPesan('Tidak ada pasien yang dijadwalkan hari ini.',
        '<button class="btn outline sm" data-act="go" data-arg="booking">Lihat semua booking</button>');
    } else {
      body += '<div class="stack g10">' + antre.map(function (b, i) {
        var hadir = b.status === 'hadir';
        return '<div class="antre' + (hadir ? ' aktif' : '') + '">' +
          '<div class="nomor">' + (i + 1) + '</div>' +
          '<div class="grow"><div class="row mid g8"><span style="font-weight:700;">' + h(namaPasien(b.pasienId)) + '</span>' +
          chipStatus(b.status) + '</div>' +
          '<div class="tiny muted" style="margin-top:2px;">' + h(b.jam) + ' · ' + h(b.kode) + ' · ' +
          h((b.vaksinIds || []).map(vaksinNama).join(', ') || 'vaksin belum dipilih') + '</div></div>' +
          '<div class="row g8">' +
          (hadir
            ? '<button class="btn teal sm" data-act="form-layanan" data-arg="' + b.id + '">' + ic('syringe', 15) + ' Catat vaksinasi</button>'
            : '<button class="btn outline sm" data-act="checkin" data-arg="' + b.id + '">Check-in</button>') +
          '<button class="btn outline sm" data-act="buka-booking" data-arg="' + b.id + '">Detail</button>' +
          '</div></div>';
      }).join('') + '</div>';
    }
    body += '</section>';

    /* riwayat pelayanan terakhir */
    var riwayat = S.layanan.slice().sort(function (a, b) { return b.dibuat.localeCompare(a.dibuat); }).slice(0, 12);
    body += '<section class="kartu rapat"><div style="padding:18px 18px 0;"><div class="judul-sec">Pelayanan terakhir</div></div>' +
      '<div class="tabel-gulir" style="margin-top:12px;"><table class="tbl"><thead><tr>' +
      '<th>Tanggal</th><th>Pasien</th><th>Vaksin &amp; batch</th><th>Petugas</th><th>KIPI</th></tr></thead><tbody>';
    if (!riwayat.length) {
      body += '<tr><td colspan="5">' + kosongPesan('Belum ada vaksinasi yang dicatat.') + '</td></tr>';
    } else {
      riwayat.forEach(function (l) {
        body += '<tr><td class="small">' + h(tgl(l.tanggal)) + '</td>' +
          '<td style="font-weight:600;">' + h(namaPasien(l.pasienId)) + '</td>' +
          '<td class="small muted">' + h(l.item.map(function (it) {
            return (vaksinById(it.vaksinId) || {}).kategori + ' (' + (it.batch || 'tanpa batch') + ')';
          }).join(', ')) + '</td>' +
          '<td class="small muted">' + h(l.petugas || '-') + '</td>' +
          '<td class="small">' + (l.kipi ? '<span class="chip amber">' + h(l.kipi) + '</span>' : '<span class="muted">—</span>') + '</td></tr>';
      });
    }
    body += '</tbody></table></div></section>';
    body += '</div>';
    return { body: body };
  }

  /* ============================ layar: persediaan ============================ */
  function scPersediaan() {
    var ringkas = stokRingkas();
    var totalDosis = ringkas.reduce(function (n, g) { return n + g.sisa; }, 0);
    var waspada = peringatanStok();
    var kedaluwarsa = S.stok.filter(function (s) {
      var d = selisihHari(s.kedaluwarsa);
      return s.sisa > 0 && d !== null && d < 0;
    });

    var body = '<div class="lebar stack g18">';
    body += '<div class="grid g-4">' +
      statTile('Jenis vaksin', ringkas.length, 'Punya catatan stok') +
      statTile('Total dosis', totalDosis, 'Siap pakai') +
      statTile('Perlu perhatian', waspada.length, 'Habis, minim, atau mendekati tempo') +
      statTile('Kedaluwarsa', kedaluwarsa.length, 'Batch yang harus ditarik') +
      '</div>';

    body += '<section class="kartu stack g14"><div class="judul-sec">Stok per jenis vaksin</div>';
    if (!ringkas.length) {
      body += kosongPesan('Belum ada stok tercatat.',
        '<button class="btn primary sm" data-act="form-stok">' + ic('plus', 15) + ' Catat stok masuk</button>');
    } else {
      body += '<div class="stack g14">' + ringkas.map(function (g) {
        // bar mengukur jumlah terhadap stok minimum; soal kedaluwarsa ditandai chip
        var kelas = g.habis ? 'bad' : (g.kritis ? 'warn' : '');
        var persen = g.minimum ? Math.min(100, Math.round(g.sisa / (g.minimum * 2) * 100)) : (g.sisa ? 100 : 0);
        return '<div class="stack g6">' +
          '<div class="row mid between g8 wrap"><span class="small" style="font-weight:700;">' + h(g.nama) + '</span>' +
          '<span class="row mid g8">' +
          (g.habis ? '<span class="chip danger">' + ic('warn', 12) + ' Habis</span>' : '') +
          (g.lewatTempo ? '<span class="chip danger">' + ic('warn', 12) + ' ' + g.lewatTempo + ' batch kedaluwarsa</span>' : '') +
          (!g.habis && g.kritis ? '<span class="chip amber">' + ic('warn', 12) + ' Di bawah minimum</span>' : '') +
          (g.dekatTempo && !g.lewatTempo ? '<span class="chip amber">' + g.dekatTempo + ' batch < 90 hari</span>' : '') +
          '<span class="small" style="font-weight:700;font-variant-numeric:tabular-nums;">' + g.sisa + ' dosis</span></span></div>' +
          '<div class="meter ' + kelas + '"><i style="width:' + persen + '%;"></i></div>' +
          '<div class="tiny muted">' + g.batch.filter(function (b) { return b.sisa > 0; }).map(function (b) {
            var d = selisihHari(b.kedaluwarsa);
            return 'Batch ' + b.batch + ': ' + b.sisa + ' dosis, ED ' + tgl(b.kedaluwarsa) +
              (d !== null && d < 0 ? ' (lewat)' : (d !== null && d <= 90 ? ' (' + d + ' hari lagi)' : ''));
          }).join(' · ') + (g.minimum ? ' · minimum ' + g.minimum + ' dosis' : '') + '</div></div>';
      }).join('') + '</div>';
    }
    body += '</section>';

    body += '<section class="kartu rapat"><div style="padding:18px 18px 0;" class="row mid between">' +
      '<div class="judul-sec">Daftar batch</div>' +
      '<button class="btn outline sm" data-act="form-stok">' + ic('plus', 15) + ' Stok masuk</button></div>' +
      '<div class="tabel-gulir" style="margin-top:12px;"><table class="tbl"><thead><tr>' +
      '<th>Vaksin</th><th>Batch</th><th>Kedaluwarsa</th><th class="num">Masuk</th><th class="num">Sisa</th><th class="num">Minimum</th><th></th>' +
      '</tr></thead><tbody>';
    if (!S.stok.length) {
      body += '<tr><td colspan="7">' + kosongPesan('Belum ada batch tercatat.') + '</td></tr>';
    } else {
      S.stok.slice().sort(function (a, b) {
        return (vaksinNama(a.vaksinId) + a.kedaluwarsa).localeCompare(vaksinNama(b.vaksinId) + b.kedaluwarsa);
      }).forEach(function (s) {
        var d = selisihHari(s.kedaluwarsa);
        body += '<tr><td class="small" style="font-weight:600;">' + h(vaksinNama(s.vaksinId)) + '</td>' +
          '<td class="small" style="font-variant-numeric:tabular-nums;">' + h(s.batch) + '</td>' +
          '<td class="small">' + h(tgl(s.kedaluwarsa)) +
          (d !== null && d < 0 ? ' <span class="chip danger">lewat</span>' : (d !== null && d <= 90 ? ' <span class="chip amber">' + d + ' hari</span>' : '')) + '</td>' +
          '<td class="num small muted">' + s.jumlahAwal + '</td>' +
          '<td class="num" style="font-weight:700;">' + s.sisa + '</td>' +
          '<td class="num small muted">' + (s.minimum || '-') + '</td>' +
          '<td class="kanan"><button class="linkbtn" data-act="form-penyesuaian" data-arg="' + s.id + '">Sesuaikan</button></td></tr>';
      });
    }
    body += '</tbody></table></div></section>';

    /* mutasi terakhir */
    var mutasi = S.mutasi.slice().sort(function (a, b) { return b.dibuat.localeCompare(a.dibuat); }).slice(0, 15);
    if (mutasi.length) {
      body += '<section class="kartu rapat"><div style="padding:18px 18px 0;"><div class="judul-sec">Mutasi terakhir</div></div>' +
        '<div class="tabel-gulir" style="margin-top:12px;"><table class="tbl"><thead><tr>' +
        '<th>Tanggal</th><th>Vaksin</th><th>Batch</th><th>Jenis</th><th class="num">Jumlah</th><th>Keterangan</th>' +
        '</tr></thead><tbody>' + mutasi.map(function (m) {
          var s = S.stok.filter(function (x) { return x.id === m.stokId; })[0] || {};
          var warna = m.jenis === 'masuk' ? 'green' : (m.jenis === 'buang' ? 'danger' : 'grey');
          return '<tr><td class="small">' + h(tgl(m.tanggal)) + '</td>' +
            '<td class="small">' + h(vaksinNama(s.vaksinId)) + '</td>' +
            '<td class="small" style="font-variant-numeric:tabular-nums;">' + h(s.batch || '-') + '</td>' +
            '<td><span class="chip ' + warna + '">' + h(m.jenis) + '</span></td>' +
            '<td class="num" style="font-weight:700;">' + (m.jenis === 'masuk' ? '+' : '−') + Math.abs(m.jumlah) + '</td>' +
            '<td class="small muted">' + h(m.ket || '-') + '</td></tr>';
        }).join('') + '</tbody></table></div></section>';
    }
    body += '</div>';
    return {
      body: body,
      aksi: '<button class="btn primary" data-act="form-stok">' + ic('plus', 16) + ' Stok masuk</button>'
    };
  }

  /* ============================ layar: transaksi ============================ */
  function scTransaksi() {
    var hari = hariIni();
    var hariIniTx = S.transaksi.filter(function (t) { return t.status === 'lunas' && String(t.tglBayar || '').slice(0, 10) === hari; });
    var omzetHari = hariIniTx.reduce(function (n, t) { return n + t.total; }, 0);
    var tunggak = belumBayar().reduce(function (n, t) { return n + (t.total - (t.dibayar || 0)); }, 0);
    var metode = {};
    hariIniTx.forEach(function (t) { metode[t.metode || 'lain'] = (metode[t.metode || 'lain'] || 0) + t.total; });

    var body = '<div class="lebar stack g18">';
    body += '<div class="grid g-3">' +
      statTile('Pendapatan hari ini', rp(omzetHari), hariIniTx.length + ' transaksi lunas') +
      statTile('Belum lunas', rp(tunggak), belumBayar().length + ' tagihan terbuka') +
      statTile('Total tagihan', S.transaksi.length, 'Sejak dashboard dipakai') +
      '</div>';

    if (Object.keys(metode).length) {
      body += '<section class="kartu stack g10"><div class="judul-sec">Metode pembayaran hari ini</div>' +
        '<div class="tabel-gulir"><table class="tbl"><thead><tr><th>Metode</th><th class="num">Jumlah</th></tr></thead><tbody>' +
        Object.keys(metode).map(function (m) {
          return '<tr><td style="font-weight:600;">' + h(m) + '</td><td class="num">' + h(rp(metode[m])) + '</td></tr>';
        }).join('') + '</tbody></table></div></section>';
    }

    body += '<section class="kartu rapat"><div class="tabel-gulir"><table class="tbl"><thead><tr>' +
      '<th>Nomor</th><th>Tanggal</th><th>Pasien</th><th>Rincian</th><th class="num">Total</th><th>Status</th><th></th>' +
      '</tr></thead><tbody>';
    var daftar = S.transaksi.slice().sort(function (a, b) { return b.dibuat.localeCompare(a.dibuat); });
    if (!daftar.length) {
      body += '<tr><td colspan="7">' + kosongPesan('Belum ada tagihan. Tagihan terbit otomatis saat vaksinasi dicatat selesai di layar Pelayanan.') + '</td></tr>';
    } else {
      daftar.forEach(function (t) {
        body += '<tr><td style="font-variant-numeric:tabular-nums;font-weight:700;">' + h(t.nomor) + '</td>' +
          '<td class="small">' + h(tgl(t.tanggal)) + '</td>' +
          '<td style="font-weight:600;">' + h(namaPasien(t.pasienId)) + '</td>' +
          '<td class="small muted">' + h(t.item.map(function (i) { return i.nama; }).join(', ')) + '</td>' +
          '<td class="num" style="font-weight:700;">' + h(rp(t.total)) + '</td>' +
          '<td>' + (t.status === 'lunas'
            ? '<span class="chip green">Lunas · ' + h(t.metode || '-') + '</span>'
            : '<span class="chip amber">Belum lunas</span>') + '</td>' +
          '<td class="kanan">' + (t.status === 'lunas'
            ? '<span class="tiny muted">' + h(tgl(t.tglBayar)) + '</span>'
            : '<button class="linkbtn" data-act="form-bayar" data-arg="' + t.id + '">Terima bayar</button>') + '</td></tr>';
      });
    }
    body += '</tbody></table></div></section>';
    body += '<div class="hint">Tagihan memakai harga dari price list resmi pada saat vaksinasi dicatat. ' +
      'Dashboard ini tidak terhubung ke mesin EDC atau payment gateway — pembayaran dicatat manual oleh kasir.</div>';
    body += '</div>';
    return {
      body: body,
      aksi: S.transaksi.length ? '<button class="btn outline" data-act="ekspor-tx">' + ic('download', 16) + ' Rekap .csv</button>' : ''
    };
  }

  /* ============================ layar: pengaturan ============================ */
  function scPengaturan() {
    var body = '<div class="lebar grid g-2">';
    body += '<section class="kartu stack g12"><div class="judul-sec">Identitas klinik</div>' +
      '<div><label class="lbl">Nama klinik</label>' +
      '<select class="input" data-field="klinik.nama">' + K.klinik.map(function (k) {
        return '<option value="' + h(k[0]) + '"' + (S.klinik.nama === k[0] ? ' selected' : '') + '>' + h(k[0]) + '</option>';
      }).join('') + '</select></div>' +
      '<div><label class="lbl">Alamat</label>' +
      '<input class="input" data-field="klinik.alamat" value="' + h(S.klinik.alamat) + '"></div>' +
      '<div><label class="lbl">Telepon</label>' +
      '<input class="input" data-field="klinik.telp" value="' + h(S.klinik.telp) + '"></div></section>';

    body += '<section class="kartu stack g12"><div class="judul-sec">Jam layanan &amp; kapasitas</div>' +
      '<div class="hint">Slot dibentuk dari jam buka sampai tutup sesuai durasi. Kapasitas membatasi jumlah booking per slot.</div>' +
      '<div class="grid g-2">' +
      '<div><label class="lbl">Jam buka</label><input class="input" type="time" data-field="jadwal.buka" value="' + h(S.jadwal.buka) + '"></div>' +
      '<div><label class="lbl">Jam tutup</label><input class="input" type="time" data-field="jadwal.tutup" value="' + h(S.jadwal.tutup) + '"></div>' +
      '<div><label class="lbl">Durasi slot (menit)</label><input class="input" type="number" min="5" step="5" data-field="jadwal.durasi" value="' + h(S.jadwal.durasi) + '"></div>' +
      '<div><label class="lbl">Kapasitas per slot</label><input class="input" type="number" min="1" data-field="jadwal.kapasitas" value="' + h(S.jadwal.kapasitas) + '"></div>' +
      '</div>' +
      '<div><label class="lbl">Hari libur</label><div class="row g6 wrap">' +
      HARI.map(function (nm, i) {
        var on = (S.jadwal.libur || []).indexOf(i) >= 0;
        return '<button class="pill' + (on ? ' on' : '') + '" data-act="toggle-libur" data-arg="' + i + '">' + h(nm.slice(0, 3)) + '</button>';
      }).join('') + '</div></div>' +
      '<div class="tiny muted">' + slotJam().length + ' slot per hari buka · kapasitas harian ' +
      (slotJam().length * Math.max(1, +S.jadwal.kapasitas || 1)) + ' kunjungan.</div></section>';

    body += '<section class="kartu stack g12"><div class="judul-sec">Data aplikasi</div>' +
      '<div class="hint">Seluruh data dashboard tersimpan di browser perangkat ini, bukan di server. ' +
      'Cadangkan sebelum berganti perangkat atau membersihkan data browser.</div>' +
      '<div class="row g8 wrap">' +
      '<button class="btn outline sm" data-act="ekspor">' + ic('download', 15) + ' Cadangkan (.json)</button>' +
      '<button class="btn outline sm" data-act="impor">' + ic('upload', 15) + ' Pulihkan cadangan</button>' +
      (S.pasien.length ? '' : '<button class="btn outline sm" data-act="contoh">Muat data contoh</button>') +
      '<button class="btn danger sm" data-act="reset">Hapus semua data</button></div>' +
      '<input type="file" id="file-impor" accept="application/json,.json" class="hide"></section>';

    body += '<section class="kartu stack g12"><div class="judul-sec">Impor dari aplikasi pasien</div>' +
      '<div class="hint">Aplikasi pasien (VaksinKu-App.html) bisa mencadangkan datanya sebagai berkas .json. ' +
      'Berkas itu dapat diimpor di sini: pasien dan reservasinya ditambahkan ke dashboard tanpa menimpa data yang sudah ada. ' +
      'Ini satu-satunya jalur otomatis yang mungkin tanpa server.</div>' +
      '<button class="btn teal sm" data-act="impor-pasien">' + ic('upload', 15) + ' Impor cadangan aplikasi pasien</button>' +
      '<input type="file" id="file-pasien" accept="application/json,.json" class="hide"></section>';

    if (!storageOk) {
      body += '<section class="kartu" style="background:var(--danger-tint);border-color:transparent;">' +
        '<div class="small" style="color:var(--danger);line-height:1.6;">Penyimpanan browser tidak aktif, jadi data hanya ' +
        'bertahan selama halaman terbuka. Buka berkas ini langsung di browser (bukan mode privat).</div></section>';
    }
    body += '</div>';
    return { body: body };
  }

  /* ============================ panel ============================ */
  function bukaPanel(jenis, arg, awal) {
    panel = { jenis: jenis, arg: arg || '', d: awal || {} };
    formErr = {};
    render();
  }
  function tutupPanel() { panel = null; formErr = {}; render(); }
  function pd() { return panel.d; }

  function panelHTML() {
    var p = { judul: '', badan: '', kaki: '' };
    switch (panel.jenis) {
      case 'pasien': p = pnPasien(); break;
      case 'booking': p = pnBooking(); break;
      case 'detail-booking': p = pnDetailBooking(); break;
      case 'layanan': p = pnLayanan(); break;
      case 'stok': p = pnStok(); break;
      case 'penyesuaian': p = pnPenyesuaian(); break;
      case 'bayar': p = pnBayar(); break;
    }
    return '<div class="tirai" data-act="tutup-panel"><div class="panel" data-stop>' +
      '<div class="kepala"><div class="grow"><h2>' + h(p.judul) + '</h2>' +
      (p.sub ? '<div class="tiny muted">' + h(p.sub) + '</div>' : '') + '</div>' +
      '<button class="ikonbtn" data-act="tutup-panel" aria-label="Tutup">' + ic('close', 16) + '</button></div>' +
      '<div class="badan">' + p.badan + '</div>' +
      (p.kaki ? '<div class="kaki">' + p.kaki + '</div>' : '') + '</div></div>';
  }
  function medan(nama, label, isi, galat, hint) {
    return '<div><label class="lbl">' + h(label) + '</label>' + isi +
      (hint ? '<div class="hint" style="margin-top:5px;">' + h(hint) + '</div>' : '') +
      (galat ? '<div class="errmsg">' + h(galat) + '</div>' : '') + '</div>';
  }

  function pnPasien() {
    var p = pasienById(panel.arg) || { id: '', nama: '', tglLahir: '', jk: '', hp: '', alamat: '', wali: '' };
    var badan = '<form id="form-pasien" class="stack g14">' +
      medan('nama', 'Nama lengkap *',
        '<input class="input' + (formErr.nama ? ' err' : '') + '" name="nama" value="' + h(p.nama) + '" placeholder="Nama sesuai identitas">', formErr.nama) +
      medan('tglLahir', 'Tanggal lahir *',
        '<input class="input' + (formErr.tglLahir ? ' err' : '') + '" type="date" name="tglLahir" max="' + hariIni() + '" value="' + h(p.tglLahir) + '">',
        formErr.tglLahir, 'Dipakai menghitung usia dan memilih jadwal vaksin yang sesuai.') +
      medan('jk', 'Jenis kelamin',
        '<select class="input" name="jk">' + ['', 'Perempuan', 'Laki-laki'].map(function (o) {
          return '<option value="' + o + '"' + (p.jk === o ? ' selected' : '') + '>' + (o || 'Pilih...') + '</option>';
        }).join('') + '</select>') +
      medan('hp', 'Nomor HP / WhatsApp',
        '<input class="input' + (formErr.hp ? ' err' : '') + '" type="tel" name="hp" value="' + h(p.hp) + '" placeholder="08xxxxxxxxxx">', formErr.hp) +
      medan('wali', 'Nama wali / penanggung jawab',
        '<input class="input" name="wali" value="' + h(p.wali) + '" placeholder="Diisi bila pasien anak-anak">') +
      medan('alamat', 'Alamat',
        '<textarea class="input" name="alamat" rows="2" placeholder="Alamat tempat tinggal">' + h(p.alamat) + '</textarea>') +
      '<input type="hidden" name="pid" value="' + h(p.id) + '"></form>';
    if (p.id) {
      badan += '<div class="divider" style="margin:18px 0;"></div>' +
        '<div class="stack g8"><div class="judul-sec">Riwayat vaksinasi</div>' +
        (function () {
          var r = S.layanan.filter(function (l) { return l.pasienId === p.id; })
            .sort(function (a, b) { return b.tanggal.localeCompare(a.tanggal); });
          if (!r.length) return '<div class="hint">Belum ada vaksinasi tercatat untuk pasien ini.</div>';
          return '<div class="stack g6">' + r.map(function (l) {
            return '<div class="row mid g8 small"><span class="muted" style="width:92px;">' + h(tgl(l.tanggal)) + '</span>' +
              '<span>' + h(l.item.map(function (i) { return (vaksinById(i.vaksinId) || {}).kategori; }).join(', ')) + '</span></div>';
          }).join('') + '</div>';
        })() + '</div>';
    }
    return {
      judul: p.id ? 'Ubah Data Pasien' : 'Pendaftaran Pasien Baru',
      sub: p.id ? p.noRM : 'Nomor rekam medis dibuat otomatis',
      badan: badan,
      kaki: '<button class="btn outline" data-act="tutup-panel">Batal</button>' +
        '<button class="btn primary" data-act="kirim-form" data-arg="form-pasien">' + (p.id ? 'Simpan perubahan' : 'Daftarkan') + '</button>'
    };
  }

  function pnBooking() {
    var d = pd();
    if (!d.siap) {
      d.siap = true;
      d.pasienId = d.pasienId || '';
      d.tanggal = d.tanggal || hariIni();
      d.jam = d.jam || '';
      d.layanan = d.layanan || 'On Site Klinik';
      d.dokter = d.dokter || K.dokter[0][0];
      d.dokterTarif = d.dokterTarif || 'umum';
      d.vaksinIds = d.vaksinIds || [];
    }
    var slots = slotJam(), kap = Math.max(1, +S.jadwal.kapasitas || 1);
    var libur = hariLibur(d.tanggal);
    var total = d.vaksinIds.reduce(function (n, id) { return n + hargaVaksin(id, d.dokterTarif); }, 0);

    var badan = '<div class="stack g14">' +
      medan('pasienId', 'Pasien *',
        '<select class="input' + (formErr.pasienId ? ' err' : '') + '" data-pd="pasienId">' +
        '<option value="">Pilih pasien terdaftar...</option>' +
        S.pasien.slice().sort(function (a, b) { return a.nama.localeCompare(b.nama); }).map(function (p) {
          return '<option value="' + p.id + '"' + (d.pasienId === p.id ? ' selected' : '') + '>' +
            h(p.nama + ' · ' + p.noRM) + '</option>';
        }).join('') + '</select>', formErr.pasienId,
        S.pasien.length ? '' : 'Belum ada pasien. Daftarkan dulu lewat menu Pendaftaran.') +
      medan('layanan', 'Jenis layanan',
        '<select class="input" data-pd="layanan">' + K.layanan.map(function (l) {
          return '<option value="' + h(l[1]) + '"' + (d.layanan === l[1] ? ' selected' : '') + '>' + h(l[1]) + '</option>';
        }).join('') + '</select>') +
      medan('tanggal', 'Tanggal *',
        '<input class="input' + (formErr.tanggal ? ' err' : '') + '" type="date" min="' + hariIni() + '" data-pd="tanggal" value="' + h(d.tanggal) + '">',
        formErr.tanggal, libur ? '' : slots.length + ' slot tersedia pada hari ini.');

    if (libur) {
      badan += '<div class="kartu" style="background:var(--danger-tint);border-color:transparent;padding:12px 14px;">' +
        '<div class="small" style="color:var(--danger);">Tanggal ini ditandai hari libur. Ubah tanggal, atau sesuaikan hari libur di Pengaturan.</div></div>';
    } else {
      badan += '<div><label class="lbl">Jam *</label><div class="row g6 wrap">' +
        slots.map(function (jam) {
          var isiJ = isiSlot(d.tanggal, jam), penuh = isiJ >= kap;
          return '<button class="pill' + (d.jam === jam ? ' on' : '') + '"' + (penuh && d.jam !== jam ? ' disabled' : '') +
            ' data-act="pd-jam" data-arg="' + jam + '" title="' + isiJ + ' dari ' + kap + ' terisi">' +
            h(jam) + ' <span style="opacity:.6;font-weight:600;">' + isiJ + '/' + kap + '</span></button>';
        }).join('') + '</div>' +
        (formErr.jam ? '<div class="errmsg">' + h(formErr.jam) + '</div>' : '') +
        '<div class="hint" style="margin-top:6px;">Slot yang sudah penuh tidak bisa dipilih.</div></div>';
    }

    badan += medan('dokter', 'Dokter / vaksinator',
      '<select class="input" data-pd="dokter">' + K.dokter.map(function (dk) {
        return '<option value="' + h(dk[0]) + '"' + (d.dokter === dk[0] ? ' selected' : '') + '>' + h(dk[0]) + '</option>';
      }).join('') + '</select>') +
      '<div><label class="lbl">Tarif</label><div class="row g6">' +
      [['umum', 'Dokter umum'], ['spesialis', 'Dokter spesialis']].map(function (t) {
        return '<button class="pill' + (d.dokterTarif === t[0] ? ' on' : '') + '" data-act="pd-tarif" data-arg="' + t[0] + '">' + h(t[1]) + '</button>';
      }).join('') + '</div></div>';

    badan += '<div><label class="lbl">Vaksin *</label>' +
      (formErr.vaksinIds ? '<div class="errmsg" style="margin:0 0 6px;">' + h(formErr.vaksinIds) + '</div>' : '') +
      '<select class="input" data-act="pd-tambah-vaksin"><option value="">Tambahkan vaksin...</option>' +
      K.harga.filter(function (v) { return d.vaksinIds.indexOf(v.id) < 0; }).map(function (v) {
        var sisa = sisaVaksin(v.id);
        return '<option value="' + v.id + '">' + h(v.kategori + ' — ' + v.merk) +
          (sisa ? ' (stok ' + sisa + ')' : ' (stok kosong)') + '</option>';
      }).join('') + '</select>';
    if (d.vaksinIds.length) {
      badan += '<div class="stack g6" style="margin-top:10px;">' + d.vaksinIds.map(function (id) {
        var harga = hargaVaksin(id, d.dokterTarif), sisa = sisaVaksin(id);
        return '<div class="row mid g8" style="border:1px solid var(--line);border-radius:10px;padding:9px 11px;">' +
          '<div class="grow"><div class="small" style="font-weight:600;">' + h(vaksinNama(id)) + '</div>' +
          '<div class="tiny ' + (sisa ? 'muted' : '') + '" style="' + (sisa ? '' : 'color:var(--danger);') + '">' +
          (sisa ? 'Stok ' + sisa + ' dosis' : 'Stok kosong — isi persediaan sebelum pelayanan') + '</div></div>' +
          '<span class="small" style="font-weight:700;">' + h(harga ? rp(harga) : 'Hubungi CS') + '</span>' +
          '<button class="ikonbtn" data-act="pd-hapus-vaksin" data-arg="' + id + '" aria-label="Hapus">' + ic('close', 14) + '</button></div>';
      }).join('') + '</div>' +
        '<div class="row mid between" style="margin-top:12px;padding-top:12px;border-top:1px solid var(--line);">' +
        '<span class="small" style="font-weight:700;">Estimasi tagihan</span>' +
        '<span class="disp" style="font-size:18px;font-weight:800;">' + h(rp(total)) + '</span></div>';
    }
    badan += '</div>' +
      medan('catatan', 'Catatan', '<textarea class="input" data-pd="catatan" rows="2" placeholder="Permintaan khusus, kondisi pasien, dll.">' + h(d.catatan || '') + '</textarea>') +
      '</div>';

    return {
      judul: 'Booking Baru', sub: 'Dicatat petugas dari WhatsApp, telepon, atau pasien datang langsung',
      badan: badan,
      kaki: '<button class="btn outline" data-act="tutup-panel">Batal</button>' +
        '<button class="btn primary" data-act="simpan-booking">Simpan booking</button>'
    };
  }

  function pnDetailBooking() {
    var b = bookingById(panel.arg);
    if (!b) return { judul: 'Booking', badan: kosongPesan('Booking tidak ditemukan.') };
    var tx = S.transaksi.filter(function (t) { return t.bookingId === b.id; })[0];
    var baris = function (l, v) {
      return '<div class="row between g12" style="padding:9px 0;border-bottom:1px solid var(--line);">' +
        '<span class="small muted">' + h(l) + '</span><span class="small kanan" style="font-weight:600;">' + v + '</span></div>';
    };
    var badan = '<div class="stack g14">' +
      '<div class="row mid g10">' + chipStatus(b.status) +
      '<span class="tiny muted">Dibuat ' + h(tgl(b.dibuat)) + '</span></div>' +
      '<div>' +
      baris('Pasien', h(namaPasien(b.pasienId))) +
      baris('Jadwal', h(tgl(b.tanggal, 'panjang') + ' · ' + (b.jam || '-'))) +
      baris('Layanan', h(b.layanan || '-')) +
      baris('Dokter', h(b.dokter || '-') + ' <span class="muted">(' + h(b.dokterTarif) + ')</span>') +
      baris('Vaksin', (b.vaksinIds || []).map(function (v) { return h(vaksinNama(v)); }).join('<br>') || '-') +
      baris('Estimasi tagihan', h(rp(totalBooking(b)))) +
      (b.catatan ? baris('Catatan', h(b.catatan)) : '') +
      (tx ? baris('Tagihan', h(tx.nomor) + ' · ' + (tx.status === 'lunas' ? 'lunas' : 'belum lunas')) : '') +
      '</div>';

    var aksi = [];
    if (b.status === 'baru') aksi.push(['ubah-status/terkonfirmasi', 'Konfirmasi booking', 'teal']);
    if (['baru', 'terkonfirmasi'].indexOf(b.status) >= 0) {
      aksi.push(['ubah-status/hadir', 'Tandai pasien hadir', 'outline']);
      aksi.push(['ubah-status/mangkir', 'Tandai tidak hadir', 'outline']);
      aksi.push(['ubah-status/batal', 'Batalkan booking', 'danger']);
    }
    if (b.status === 'hadir') aksi.push(['layani/' + b.id, 'Catat vaksinasi', 'primary']);
    if (aksi.length) {
      badan += '<div class="stack g8"><div class="judul-sec">Tindakan</div>' +
        aksi.map(function (a) {
          return '<button class="btn ' + a[2] + ' block" data-act="aksi-booking" data-arg="' + a[0] + '">' + h(a[1]) + '</button>';
        }).join('') + '</div>';
    }
    badan += '</div>';
    return { judul: b.kode, sub: namaPasien(b.pasienId), badan: badan };
  }

  function pnLayanan() {
    var b = bookingById(panel.arg);
    if (!b) return { judul: 'Pelayanan', badan: kosongPesan('Booking tidak ditemukan.') };
    var d = pd();
    if (!d.siap) {
      d.siap = true;
      d.pilih = {};
      (b.vaksinIds || []).forEach(function (id) {
        var bt = batchVaksin(id);
        d.pilih[id] = bt.length ? bt[0].id : '';   // FEFO: kedaluwarsa terdekat lebih dulu
      });
      d.petugas = b.dokter || K.dokter[0][0];
      d.kipi = '';
      d.catatan = '';
    }
    var badan = '<div class="stack g14">' +
      '<div class="kartu" style="background:var(--teal-tint);border-color:transparent;padding:12px 14px;">' +
      '<div class="small" style="font-weight:700;color:var(--teal-deep);">' + h(namaPasien(b.pasienId)) + '</div>' +
      '<div class="tiny" style="color:var(--teal-deep);">' + h(b.kode + ' · ' + tgl(b.tanggal) + ' ' + (b.jam || '')) + '</div></div>';

    badan += '<div class="stack g10"><div class="judul-sec">Vaksin &amp; batch</div>' +
      '<div class="hint">Batch terpilih otomatis mengikuti kedaluwarsa terdekat (FEFO). Stok berkurang saat pelayanan disimpan.</div>';
    if (!(b.vaksinIds || []).length) {
      badan += '<div class="errmsg">Booking ini belum punya vaksin. Tambahkan dulu lewat booking baru.</div>';
    }
    (b.vaksinIds || []).forEach(function (id) {
      var bt = batchVaksin(id);
      badan += '<div class="stack g6" style="border:1px solid var(--line);border-radius:11px;padding:12px;">' +
        '<div class="small" style="font-weight:700;">' + h(vaksinNama(id)) + '</div>' +
        (bt.length
          ? '<select class="input" data-batch="' + id + '">' + bt.map(function (s) {
            var sh = selisihHari(s.kedaluwarsa);
            return '<option value="' + s.id + '"' + (d.pilih[id] === s.id ? ' selected' : '') + '>' +
              h('Batch ' + s.batch + ' · sisa ' + s.sisa + ' · ED ' + tgl(s.kedaluwarsa)) +
              (sh !== null && sh < 0 ? ' (KEDALUWARSA)' : '') + '</option>';
          }).join('') + '</select>'
          : '<div class="errmsg">Tidak ada batch tersisa untuk vaksin ini. Catat stok masuk dulu di menu Persediaan.</div>') +
        '</div>';
    });
    badan += '</div>';

    badan += medan('petugas', 'Petugas vaksinator',
      '<select class="input" data-pd="petugas">' + K.dokter.map(function (dk) {
        return '<option value="' + h(dk[0]) + '"' + (d.petugas === dk[0] ? ' selected' : '') + '>' + h(dk[0]) + '</option>';
      }).join('') + '</select>') +
      medan('kipi', 'Kejadian ikutan pasca imunisasi (KIPI)',
        '<input class="input" data-pd="kipi" value="' + h(d.kipi) + '" placeholder="Kosongkan bila tidak ada">',
        '', 'Catat bila ada reaksi yang teramati saat observasi, misalnya demam atau bengkak di bekas suntikan.') +
      medan('catatan', 'Catatan pelayanan',
        '<textarea class="input" data-pd="catatan" rows="2">' + h(d.catatan) + '</textarea>');

    var total = (b.vaksinIds || []).reduce(function (n, id) { return n + hargaVaksin(id, b.dokterTarif); }, 0);
    badan += '<div class="kartu" style="padding:14px;"><div class="row mid between">' +
      '<span class="small" style="font-weight:700;">Tagihan yang akan terbit</span>' +
      '<span class="disp" style="font-size:18px;font-weight:800;">' + h(rp(total)) + '</span></div>' +
      '<div class="hint" style="margin-top:6px;">Tagihan terbit berstatus belum lunas; pembayaran dicatat di menu Transaksi.</div></div>';
    badan += '</div>';

    return {
      judul: 'Catat Vaksinasi', sub: b.kode,
      badan: badan,
      kaki: '<button class="btn outline" data-act="tutup-panel">Batal</button>' +
        '<button class="btn primary" data-act="simpan-layanan">' + ic('check', 15) + ' Selesai &amp; kurangi stok</button>'
    };
  }

  function pnStok() {
    var badan = '<form id="form-stok" class="stack g14">' +
      medan('vaksinId', 'Vaksin *',
        '<select class="input' + (formErr.vaksinId ? ' err' : '') + '" name="vaksinId"><option value="">Pilih vaksin...</option>' +
        K.harga.map(function (v) {
          return '<option value="' + v.id + '">' + h(v.kategori + ' — ' + v.merk) + '</option>';
        }).join('') + '</select>', formErr.vaksinId) +
      medan('batch', 'Nomor batch *',
        '<input class="input' + (formErr.batch ? ' err' : '') + '" name="batch" placeholder="Sesuai kemasan vaksin">', formErr.batch) +
      medan('kedaluwarsa', 'Tanggal kedaluwarsa *',
        '<input class="input' + (formErr.kedaluwarsa ? ' err' : '') + '" type="date" name="kedaluwarsa">', formErr.kedaluwarsa) +
      medan('jumlah', 'Jumlah dosis masuk *',
        '<input class="input' + (formErr.jumlah ? ' err' : '') + '" type="number" min="1" name="jumlah" placeholder="0">', formErr.jumlah) +
      medan('minimum', 'Stok minimum',
        '<input class="input" type="number" min="0" name="minimum" placeholder="0">', '',
        'Dipakai sebagai ambang peringatan. Kosongkan bila belum ditentukan.') +
      medan('ket', 'Keterangan', '<input class="input" name="ket" placeholder="Nomor surat jalan, distributor, dll.">') +
      '</form>';
    return {
      judul: 'Stok Masuk', sub: 'Penerimaan vaksin per batch',
      badan: badan,
      kaki: '<button class="btn outline" data-act="tutup-panel">Batal</button>' +
        '<button class="btn primary" data-act="kirim-form" data-arg="form-stok">Simpan penerimaan</button>'
    };
  }

  function pnPenyesuaian() {
    var s = S.stok.filter(function (x) { return x.id === panel.arg; })[0];
    if (!s) return { judul: 'Penyesuaian', badan: kosongPesan('Batch tidak ditemukan.') };
    var badan = '<div class="kartu" style="padding:12px 14px;margin-bottom:16px;">' +
      '<div class="small" style="font-weight:700;">' + h(vaksinNama(s.vaksinId)) + '</div>' +
      '<div class="tiny muted">Batch ' + h(s.batch) + ' · sisa ' + s.sisa + ' dari ' + s.jumlahAwal + ' dosis · ED ' + h(tgl(s.kedaluwarsa)) + '</div></div>' +
      '<form id="form-penyesuaian" class="stack g14">' +
      '<div><label class="lbl">Jenis penyesuaian</label><div class="row g6 wrap">' +
      [['buang', 'Pembuangan / rusak'], ['koreksi', 'Koreksi hitung'], ['masuk', 'Tambahan masuk']].map(function (t, i) {
        return '<label class="pill' + (i === 0 ? ' on' : '') + '" data-pilih-jenis="' + t[0] + '">' +
          '<input type="radio" name="jenis" value="' + t[0] + '"' + (i === 0 ? ' checked' : '') + ' class="hide">' + h(t[1]) + '</label>';
      }).join('') + '</div></div>' +
      medan('jumlah', 'Jumlah dosis *',
        '<input class="input' + (formErr.jumlah ? ' err' : '') + '" type="number" min="1" name="jumlah">', formErr.jumlah,
        'Untuk pembuangan dan koreksi, jumlah ini dikurangkan dari sisa batch.') +
      medan('minimum', 'Stok minimum',
        '<input class="input" type="number" min="0" name="minimum" value="' + h(s.minimum || '') + '">') +
      medan('ket', 'Alasan *',
        '<input class="input' + (formErr.ket ? ' err' : '') + '" name="ket" placeholder="Vial pecah, rantai dingin putus, salah hitung...">', formErr.ket) +
      '<input type="hidden" name="sid" value="' + h(s.id) + '"></form>';
    return {
      judul: 'Penyesuaian Stok', sub: 'Batch ' + s.batch,
      badan: badan,
      kaki: '<button class="btn outline" data-act="tutup-panel">Batal</button>' +
        '<button class="btn primary" data-act="kirim-form" data-arg="form-penyesuaian">Simpan penyesuaian</button>'
    };
  }

  function pnBayar() {
    var t = S.transaksi.filter(function (x) { return x.id === panel.arg; })[0];
    if (!t) return { judul: 'Pembayaran', badan: kosongPesan('Tagihan tidak ditemukan.') };
    var badan = '<div class="stack g14">' +
      '<div class="kartu" style="padding:14px;">' +
      '<div class="tiny muted">' + h(t.nomor) + ' · ' + h(namaPasien(t.pasienId)) + '</div>' +
      '<div class="hero" style="font-size:34px;margin-top:6px;">' + h(rp(t.total)) + '</div></div>' +
      '<div class="stack g8"><div class="judul-sec">Rincian</div>' +
      t.item.map(function (i) {
        return '<div class="row between g10 small"><span>' + h(i.nama) + '</span>' +
          '<span style="font-weight:700;font-variant-numeric:tabular-nums;">' + h(rp(i.harga)) + '</span></div>';
      }).join('') + '</div>' +
      '<form id="form-bayar" class="stack g14">' +
      '<div><label class="lbl">Metode pembayaran *</label><div class="row g6 wrap">' +
      ['Tunai', 'Transfer', 'QRIS', 'Kartu debit/kredit', 'Asuransi'].map(function (m, i) {
        return '<label class="pill' + (i === 0 ? ' on' : '') + '" data-pilih-metode="' + h(m) + '">' +
          '<input type="radio" name="metode" value="' + h(m) + '"' + (i === 0 ? ' checked' : '') + ' class="hide">' + h(m) + '</label>';
      }).join('') + '</div></div>' +
      medan('tglBayar', 'Tanggal pembayaran',
        '<input class="input" type="date" name="tglBayar" value="' + h(hariIni()) + '" max="' + h(hariIni()) + '">') +
      medan('ket', 'Catatan', '<input class="input" name="ket" placeholder="Nomor referensi, nama penjamin, dll.">') +
      '<input type="hidden" name="tid" value="' + h(t.id) + '"></form></div>';
    return {
      judul: 'Terima Pembayaran', sub: t.nomor,
      badan: badan,
      kaki: '<button class="btn outline" data-act="tutup-panel">Batal</button>' +
        '<button class="btn primary" data-act="kirim-form" data-arg="form-bayar">' + ic('check', 15) + ' Tandai lunas</button>'
    };
  }

  /* ============================ aksi ============================ */
  function buatTransaksi(b, item) {
    var total = item.reduce(function (n, i) { return n + i.harga; }, 0);
    var t = {
      id: uid(), nomor: nomorInvoice(), bookingId: b.id, pasienId: b.pasienId,
      tanggal: b.tanggal, item: item, total: total, dibayar: 0,
      status: 'terbuka', metode: '', tglBayar: '', ket: '', dibuat: new Date().toISOString()
    };
    S.transaksi.push(t);
    return t;
  }
  function kurangiStok(stokId, jumlah, ket, ref) {
    var s = S.stok.filter(function (x) { return x.id === stokId; })[0];
    if (!s) return false;
    s.sisa = Math.max(0, s.sisa - jumlah);
    S.mutasi.push({
      id: uid(), stokId: stokId, jenis: 'keluar', jumlah: jumlah,
      tanggal: hariIni(), ket: ket, ref: ref || '', dibuat: new Date().toISOString()
    });
    return true;
  }
  function unduhBerkas(nama, isi, tipe) {
    var blob = new Blob([isi], { type: tipe || 'application/json' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = nama;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
  }
  function csvTransaksi() {
    function sel(v) {
      var t = String(v == null ? '' : v);
      return /[";\n]/.test(t) ? '"' + t.replace(/"/g, '""') + '"' : t;
    }
    var baris = [['Nomor', 'Tanggal', 'Pasien', 'No. RM', 'Rincian', 'Total', 'Status', 'Metode', 'Tanggal bayar']];
    S.transaksi.slice().sort(function (a, b) { return a.dibuat.localeCompare(b.dibuat); }).forEach(function (t) {
      var p = pasienById(t.pasienId) || {};
      baris.push([t.nomor, t.tanggal, p.nama || '-', p.noRM || '-',
        t.item.map(function (i) { return i.nama; }).join(' | '), t.total,
        t.status === 'lunas' ? 'Lunas' : 'Belum lunas', t.metode || '-', t.tglBayar || '-']);
    });
    return '﻿' + baris.map(function (r) { return r.map(sel).join(';'); }).join('\r\n');
  }

  document.addEventListener('click', function (ev) {
    var el = ev.target.closest('[data-act]');
    if (!el) return;
    var act = el.getAttribute('data-act'), arg = el.getAttribute('data-arg') || '';
    if (act === 'tutup-panel' && ev.target.closest('[data-stop]') && el.classList.contains('tirai')) return;

    switch (act) {
      case 'go': location.hash = '#/' + arg; return;
      case 'tutup-panel': tutupPanel(); return;
      case 'rentang': S.ui.rentangOmzet = +arg; simpan(); render(); return;
      case 'tabel-omzet': S.ui.tabelOmzet = !S.ui.tabelOmzet; simpan(); render(); return;
      case 'filter-booking': S.ui.filterBooking = arg; simpan(); render(); return;
      case 'geser-hari': S.ui.tanggalJadwal = geserHari(S.ui.tanggalJadwal || hariIni(), +arg); simpan(); render(); return;
      case 'jadwal-hari-ini': S.ui.tanggalJadwal = hariIni(); simpan(); render(); return;
      case 'toggle-libur': {
        var lb = S.jadwal.libur, i = lb.indexOf(+arg);
        if (i >= 0) lb.splice(i, 1); else lb.push(+arg);
        simpan(); render(); return;
      }
      case 'form-pasien': bukaPanel('pasien', arg); return;
      case 'form-booking': bukaPanel('booking', '', {}); return;
      case 'buka-booking': bukaPanel('detail-booking', arg); return;
      case 'form-layanan': bukaPanel('layanan', arg, {}); return;
      case 'form-stok': bukaPanel('stok'); return;
      case 'form-penyesuaian': bukaPanel('penyesuaian', arg); return;
      case 'form-bayar': bukaPanel('bayar', arg); return;
      case 'checkin': {
        var bc = bookingById(arg);
        if (bc) { bc.status = 'hadir'; simpan(); render(); toast(namaPasien(bc.pasienId) + ' ditandai hadir.'); }
        return;
      }
      case 'aksi-booking': {
        var bagian = arg.split('/'), bb = bookingById(bagian[1] || panel.arg);
        if (!bb) return;
        if (bagian[0] === 'layani') { bukaPanel('layanan', bb.id, {}); return; }
        var st = bagian[1];
        bb = bookingById(panel.arg);
        if (!bb) return;
        if (st === 'batal' && !konfirmasi('Batalkan booking ' + bb.kode + '?')) return;
        bb.status = st;
        simpan(); render();
        toast('Status ' + bb.kode + ' menjadi ' + (STATUS[st] || {}).label + '.');
        return;
      }
      case 'pd-jam': pd().jam = arg; render(); return;
      case 'pd-tarif': pd().dokterTarif = arg; render(); return;
      case 'pd-hapus-vaksin': {
        var vi = pd().vaksinIds.indexOf(arg);
        if (vi >= 0) pd().vaksinIds.splice(vi, 1);
        render(); return;
      }
      case 'simpan-booking': simpanBooking(); return;
      case 'simpan-layanan': simpanLayanan(); return;
      case 'kirim-form': {
        var f = document.getElementById(arg);
        if (f) f.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
        return;
      }
      case 'ekspor': unduhBerkas('vaksinku-dashboard-' + hariIni() + '.json', JSON.stringify(S, null, 2));
        toast('Cadangan diunduh.'); return;
      case 'ekspor-tx': unduhBerkas('rekap-transaksi-' + hariIni() + '.csv', csvTransaksi(), 'text/csv;charset=utf-8');
        toast('Rekap transaksi diunduh.'); return;
      case 'impor': document.getElementById('file-impor').click(); return;
      case 'impor-pasien': document.getElementById('file-pasien').click(); return;
      case 'contoh': muatContoh(); return;
      case 'reset': {
        if (!konfirmasi('Hapus seluruh data dashboard? Tindakan ini tidak bisa dibatalkan.')) return;
        S = salin(kosong); simpan(); location.hash = '#/ringkasan'; render();
        toast('Semua data dihapus.'); return;
      }
    }
  });

  /* pilihan radio bergaya pill */
  document.addEventListener('change', function (ev) {
    var t = ev.target;
    if (t.type === 'radio' && t.closest('.panel')) {
      var grup = t.closest('.panel').querySelectorAll('[name="' + t.name + '"]');
      [].forEach.call(grup, function (r) {
        var lab = r.closest('.pill');
        if (lab) lab.classList.toggle('on', r.checked);
      });
      return;
    }
    if (t.id === 'file-impor' && t.files.length) { bacaCadangan(t.files[0], false); return; }
    if (t.id === 'file-pasien' && t.files.length) { bacaCadangan(t.files[0], true); return; }
  });

  document.addEventListener('input', function (ev) {
    var el = ev.target;
    if (el.id === 'cari-pasien') { S.ui.cariPasien = el.value; simpan(); render(); fokusLagi('cari-pasien'); return; }
    if (el.id === 'cari-booking') { S.ui.cariBooking = el.value; simpan(); render(); fokusLagi('cari-booking'); return; }
    if (el.id === 'tgl-jadwal') { S.ui.tanggalJadwal = el.value; simpan(); render(); return; }
    var pdf = el.getAttribute('data-pd');
    if (pdf && panel) {
      pd()[pdf] = el.value;
      if (pdf === 'tanggal') { pd().jam = ''; render(); }
      return;
    }
    var bt = el.getAttribute('data-batch');
    if (bt && panel) { pd().pilih[bt] = el.value; return; }
    if (el.getAttribute('data-act') === 'pd-tambah-vaksin' && el.value) {
      if (pd().vaksinIds.indexOf(el.value) < 0) pd().vaksinIds.push(el.value);
      render(); return;
    }
    var f = el.getAttribute('data-field');
    if (f) {
      var bagian = f.split('.');
      S[bagian[0]][bagian[1]] = bagian[0] === 'jadwal' && ['durasi', 'kapasitas'].indexOf(bagian[1]) >= 0
        ? (parseInt(el.value, 10) || 0) : el.value;
      simpan();
      if (bagian[0] === 'jadwal') { render(); }
      return;
    }
  });
  function fokusLagi(id) {
    var el = document.getElementById(id);
    if (el) { el.focus(); el.setSelectionRange(el.value.length, el.value.length); }
  }

  document.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var f = ev.target, formId = f.getAttribute('id');
    var get = function (n) { return (f.elements[n] ? String(f.elements[n].value) : '').trim(); };
    formErr = {};

    if (formId === 'form-pasien') {
      if (!get('nama')) formErr.nama = 'Nama wajib diisi.';
      if (!get('tglLahir')) formErr.tglLahir = 'Tanggal lahir wajib diisi.';
      else if (get('tglLahir') > hariIni()) formErr.tglLahir = 'Tanggal lahir tidak boleh di masa depan.';
      var hp = get('hp').replace(/\D/g, '');
      if (get('hp') && (hp.length < 9 || hp.length > 15)) formErr.hp = 'Nomor HP tidak valid — isi 9–15 digit.';
      if (Object.keys(formErr).length) { render(); return; }
      var pid = get('pid');
      if (pid) {
        var pp = pasienById(pid);
        if (pp) {
          pp.nama = get('nama'); pp.tglLahir = get('tglLahir'); pp.jk = get('jk');
          pp.hp = get('hp'); pp.wali = get('wali'); pp.alamat = get('alamat');
        }
        simpan(); tutupPanel(); toast('Data pasien diperbarui.');
      } else {
        S.pasien.push({
          id: uid(), noRM: nomorRM(), nama: get('nama'), tglLahir: get('tglLahir'), jk: get('jk'),
          hp: get('hp'), wali: get('wali'), alamat: get('alamat'), dibuat: new Date().toISOString()
        });
        simpan(); tutupPanel(); toast(get('nama') + ' terdaftar.');
      }
      return;
    }

    if (formId === 'form-stok') {
      if (!get('vaksinId')) formErr.vaksinId = 'Pilih vaksin.';
      if (!get('batch')) formErr.batch = 'Nomor batch wajib diisi.';
      if (!get('kedaluwarsa')) formErr.kedaluwarsa = 'Tanggal kedaluwarsa wajib diisi.';
      else if (get('kedaluwarsa') <= hariIni()) formErr.kedaluwarsa = 'Batch yang sudah kedaluwarsa tidak boleh diterima.';
      var jml = parseInt(get('jumlah'), 10);
      if (!jml || jml < 1) formErr.jumlah = 'Jumlah dosis minimal 1.';
      if (Object.keys(formErr).length) { render(); return; }
      var sudahAda = S.stok.filter(function (s) {
        return s.vaksinId === get('vaksinId') && s.batch === get('batch');
      })[0];
      if (sudahAda) {
        sudahAda.jumlahAwal += jml;
        sudahAda.sisa += jml;
        if (get('minimum')) sudahAda.minimum = parseInt(get('minimum'), 10) || 0;
        S.mutasi.push({ id: uid(), stokId: sudahAda.id, jenis: 'masuk', jumlah: jml, tanggal: hariIni(), ket: get('ket'), dibuat: new Date().toISOString() });
      } else {
        var baruStok = {
          id: uid(), vaksinId: get('vaksinId'), batch: get('batch'), kedaluwarsa: get('kedaluwarsa'),
          jumlahAwal: jml, sisa: jml, minimum: parseInt(get('minimum'), 10) || 0, dibuat: new Date().toISOString()
        };
        S.stok.push(baruStok);
        S.mutasi.push({ id: uid(), stokId: baruStok.id, jenis: 'masuk', jumlah: jml, tanggal: hariIni(), ket: get('ket'), dibuat: new Date().toISOString() });
      }
      simpan(); tutupPanel(); toast(jml + ' dosis masuk ke persediaan.');
      return;
    }

    if (formId === 'form-penyesuaian') {
      var s2 = S.stok.filter(function (x) { return x.id === get('sid'); })[0];
      var jp = parseInt(get('jumlah'), 10);
      var jenis = get('jenis') || 'buang';
      if (!jp || jp < 1) formErr.jumlah = 'Jumlah minimal 1.';
      else if (jenis !== 'masuk' && s2 && jp > s2.sisa) formErr.jumlah = 'Melebihi sisa batch (' + s2.sisa + ' dosis).';
      if (!get('ket')) formErr.ket = 'Alasan wajib diisi agar mutasi bisa ditelusuri.';
      if (Object.keys(formErr).length) { render(); return; }
      if (jenis === 'masuk') { s2.sisa += jp; s2.jumlahAwal += jp; }
      else s2.sisa -= jp;
      if (get('minimum') !== '') s2.minimum = parseInt(get('minimum'), 10) || 0;
      S.mutasi.push({
        id: uid(), stokId: s2.id, jenis: jenis === 'masuk' ? 'masuk' : (jenis === 'buang' ? 'buang' : 'keluar'),
        jumlah: jp, tanggal: hariIni(), ket: get('ket'), dibuat: new Date().toISOString()
      });
      simpan(); tutupPanel(); toast('Penyesuaian stok tercatat.');
      return;
    }

    if (formId === 'form-bayar') {
      var tx = S.transaksi.filter(function (x) { return x.id === get('tid'); })[0];
      if (!tx) { tutupPanel(); return; }
      tx.status = 'lunas';
      tx.dibayar = tx.total;
      tx.metode = get('metode') || 'Tunai';
      tx.tglBayar = get('tglBayar') || hariIni();
      tx.ket = get('ket');
      simpan(); tutupPanel(); toast('Pembayaran ' + tx.nomor + ' dicatat lunas.');
      return;
    }
  });

  function simpanBooking() {
    var d = pd();
    formErr = {};
    if (!d.pasienId) formErr.pasienId = 'Pilih pasien.';
    if (!d.tanggal) formErr.tanggal = 'Tanggal wajib diisi.';
    else if (hariLibur(d.tanggal)) formErr.tanggal = 'Tanggal ini hari libur.';
    if (!d.jam) formErr.jam = 'Pilih slot jam.';
    else if (isiSlot(d.tanggal, d.jam) >= Math.max(1, +S.jadwal.kapasitas || 1)) formErr.jam = 'Slot sudah penuh.';
    if (!d.vaksinIds.length) formErr.vaksinIds = 'Pilih minimal satu vaksin.';
    if (Object.keys(formErr).length) { render(); return; }
    var b = {
      id: uid(), kode: nomorBooking(), pasienId: d.pasienId, layanan: d.layanan,
      tanggal: d.tanggal, jam: d.jam, dokter: d.dokter, dokterTarif: d.dokterTarif,
      vaksinIds: d.vaksinIds.slice(), catatan: d.catatan || '', status: 'terkonfirmasi',
      sumber: 'petugas', dibuat: hariIni()
    };
    S.booking.push(b);
    simpan(); tutupPanel();
    toast('Booking ' + b.kode + ' dibuat untuk ' + namaPasien(b.pasienId) + '.');
  }

  function simpanLayanan() {
    var b = bookingById(panel.arg), d = pd();
    if (!b) { tutupPanel(); return; }
    if (!(b.vaksinIds || []).length) { toast('Booking ini belum punya vaksin.'); return; }
    var kurang = (b.vaksinIds || []).filter(function (id) { return !d.pilih[id]; });
    if (kurang.length) {
      toast('Stok belum tersedia untuk ' + (vaksinById(kurang[0]) || {}).kategori + '.');
      return;
    }
    var item = [], catatan = [];
    b.vaksinIds.forEach(function (id) {
      var stokId = d.pilih[id];
      var s = S.stok.filter(function (x) { return x.id === stokId; })[0];
      kurangiStok(stokId, 1, 'Pelayanan ' + b.kode, b.id);
      item.push({ nama: vaksinNama(id), harga: hargaVaksin(id, b.dokterTarif), vaksinId: id });
      catatan.push({ vaksinId: id, stokId: stokId, batch: s ? s.batch : '' });
    });
    S.layanan.push({
      id: uid(), bookingId: b.id, pasienId: b.pasienId, tanggal: hariIni(),
      item: catatan, petugas: d.petugas, kipi: d.kipi || '', catatan: d.catatan || '',
      dibuat: new Date().toISOString()
    });
    b.status = 'selesai';
    var tx = buatTransaksi(b, item);
    simpan(); tutupPanel();
    toast('Vaksinasi tercatat. Tagihan ' + tx.nomor + ' terbit ' + rp(tx.total) + '.');
  }

  function bacaCadangan(berkas, dariPasien) {
    var fr = new FileReader();
    fr.onload = function () {
      try {
        var data = JSON.parse(fr.result);
        if (!data || typeof data !== 'object') throw new Error('bukan JSON objek');
        if (dariPasien) imporDariAplikasiPasien(data);
        else {
          if (!('booking' in data) || !('pasien' in data)) throw new Error('bukan cadangan dashboard');
          for (var k in kosong) if (!(k in data)) data[k] = salin(kosong[k]);
          S = data; simpan(); render(); toast('Cadangan dashboard dipulihkan.');
        }
      } catch (e) { toast('Berkas tidak dikenali: ' + e.message + '.'); }
    };
    fr.readAsText(berkas);
  }
  function imporDariAplikasiPasien(data) {
    if (!(data.pasien instanceof Array)) throw new Error('bukan cadangan aplikasi pasien');
    var petaPasien = {}, pBaru = 0, bBaru = 0;
    data.pasien.forEach(function (p) {
      var ada = S.pasien.filter(function (x) {
        return x.nama.toLowerCase() === String(p.nama || '').toLowerCase() && x.tglLahir === p.tglLahir;
      })[0];
      if (ada) { petaPasien[p.id] = ada.id; return; }
      var baru = {
        id: uid(), noRM: nomorRM(), nama: p.nama, tglLahir: p.tglLahir,
        jk: p.jenisKelamin || '', hp: (data.profil || {}).hp || '', wali: (data.profil || {}).nama || '',
        alamat: ((data.alamat || [])[0] || {}).alamat || '', dibuat: new Date().toISOString()
      };
      S.pasien.push(baru);
      petaPasien[p.id] = baru.id;
      pBaru++;
    });
    (data.booking || []).forEach(function (b) {
      if (S.booking.some(function (x) { return x.asal === b.kode; })) return;
      var pid = petaPasien[(b.pasienIds || [])[0]];
      if (!pid) return;
      S.booking.push({
        id: uid(), kode: nomorBooking(), pasienId: pid,
        layanan: b.layanan === 'homecare' ? 'Home Care' : (b.layanan === 'corporate' ? 'On Site Corporate' : 'On Site Klinik'),
        tanggal: b.tanggal, jam: b.jam, dokter: b.dokter === 'spesialis' ? K.dokter[0][0] : K.dokter[3][0],
        dokterTarif: b.dokter === 'spesialis' ? 'spesialis' : 'umum',
        vaksinIds: (b.vaksinIds || []).slice(), catatan: b.catatan || '',
        status: b.status === 'selesai' ? 'selesai' : 'baru', sumber: 'aplikasi pasien',
        asal: b.kode, dibuat: hariIni()
      });
      bBaru++;
    });
    simpan(); render();
    toast(pBaru + ' pasien dan ' + bBaru + ' booking diimpor dari aplikasi pasien.');
  }

  /* ============================ data contoh ============================ */
  function muatContoh() {
    if (!konfirmasi('Muat data contoh? Data dashboard yang ada sekarang akan diganti.')) return;
    S = salin(kosong);
    // klinik contoh dibuat buka pada hari data ini dimuat, agar antrean hari ini
    // tidak bentrok dengan hari libur bawaan
    var wdIni = new Date(hariIni() + 'T00:00:00').getDay();
    S.jadwal.libur = S.jadwal.libur.filter(function (d) { return d !== wdIni; });
    var nama = [['Nadia Putri', '2021-05-12', 'Perempuan'], ['Bayu Pratama', '1992-02-08', 'Laki-laki'],
      ['Siti Rahmawati', '1988-11-30', 'Perempuan'], ['Ahmad Fauzi', '2019-07-21', 'Laki-laki'],
      ['Dewi Anggraini', '1965-03-14', 'Perempuan']];
    nama.forEach(function (n) {
      S.pasien.push({
        id: uid(), noRM: nomorRM(), nama: n[0], tglLahir: n[1], jk: n[2],
        hp: '0812xxxxxxx', wali: '', alamat: 'Tanjungpinang', dibuat: new Date().toISOString()
      });
    });
    var vFlu = K.harga.filter(function (v) { return v.kategori.indexOf('Influenza') === 0 && v.umum; })[0];
    var vHepB = K.harga.filter(function (v) { return v.kategori.indexOf('Hepatitis B') === 0 && v.umum; })[0];
    [[vFlu, 'FL-2608A', 60], [vHepB, 'HB-2611C', 24]].forEach(function (x) {
      if (!x[0]) return;
      var s = {
        id: uid(), vaksinId: x[0].id, batch: x[1], kedaluwarsa: geserHari(hariIni(), 240),
        jumlahAwal: x[2], sisa: x[2], minimum: 10, dibuat: new Date().toISOString()
      };
      S.stok.push(s);
      S.mutasi.push({ id: uid(), stokId: s.id, jenis: 'masuk', jumlah: x[2], tanggal: geserHari(hariIni(), -20), ket: 'Penerimaan awal', dibuat: new Date().toISOString() });
    });
    // satu batch tipis agar peringatan stok terlihat
    if (vHepB) {
      var tipis = {
        id: uid(), vaksinId: vHepB.id, batch: 'HB-2509B', kedaluwarsa: geserHari(hariIni(), 45),
        jumlahAwal: 20, sisa: 6, minimum: 10, dibuat: new Date().toISOString()
      };
      S.stok.push(tipis);
    }
    var slots = slotJam();
    S.pasien.slice(0, 4).forEach(function (p, i) {
      var tgl2 = i < 2 ? hariIni() : geserHari(hariIni(), i);
      S.booking.push({
        id: uid(), kode: nomorBooking(), pasienId: p.id, layanan: i % 2 ? 'Home Care' : 'On Site Klinik',
        tanggal: tgl2, jam: slots[Math.min(slots.length - 1, i)] || '09:00',
        dokter: K.dokter[3][0], dokterTarif: 'umum',
        vaksinIds: [(vFlu || {}).id].filter(Boolean), catatan: '',
        status: i === 0 ? 'hadir' : (i === 3 ? 'baru' : 'terkonfirmasi'), sumber: 'petugas', dibuat: hariIni()
      });
    });
    // satu pelayanan selesai berikut tagihannya, agar grafik pendapatan ada isinya
    var pLama = S.pasien[4], sFlu = S.stok[0];
    if (pLama && sFlu && vFlu) {
      var bLama = {
        id: uid(), kode: nomorBooking(), pasienId: pLama.id, layanan: 'On Site Klinik',
        tanggal: geserHari(hariIni(), -2), jam: '09:00', dokter: K.dokter[3][0], dokterTarif: 'umum',
        vaksinIds: [vFlu.id], catatan: '', status: 'selesai', sumber: 'petugas', dibuat: geserHari(hariIni(), -2)
      };
      S.booking.push(bLama);
      sFlu.sisa -= 1;
      S.mutasi.push({ id: uid(), stokId: sFlu.id, jenis: 'keluar', jumlah: 1, tanggal: geserHari(hariIni(), -2), ket: 'Pelayanan ' + bLama.kode, dibuat: new Date().toISOString() });
      S.layanan.push({
        id: uid(), bookingId: bLama.id, pasienId: pLama.id, tanggal: geserHari(hariIni(), -2),
        item: [{ vaksinId: vFlu.id, stokId: sFlu.id, batch: sFlu.batch }],
        petugas: K.dokter[3][0], kipi: '', catatan: '', dibuat: new Date().toISOString()
      });
      var txLama = buatTransaksi(bLama, [{ nama: vaksinNama(vFlu.id), harga: angka(vFlu.umum), vaksinId: vFlu.id }]);
      txLama.status = 'lunas'; txLama.dibayar = txLama.total;
      txLama.metode = 'Tunai'; txLama.tglBayar = geserHari(hariIni(), -2);
    }
    simpan(); location.hash = '#/ringkasan'; render();
    toast('Data contoh dimuat. Hapus kapan saja lewat Pengaturan.');
  }

  /* ============================ init ============================ */
  window.addEventListener('hashchange', function () {
    bacaRoute(); panel = null; formErr = {};
    render();
    var sc = document.querySelector('.isi');
    if (sc) sc.scrollTop = 0;
  });
  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape' && panel) tutupPanel();
  });
  bacaRoute();
  render();
})();
