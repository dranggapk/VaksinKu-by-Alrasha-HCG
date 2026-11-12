// Pakai: node mockup/build_panduan.js <root-repo> <keluaran.html> <fonts.css>
// Membuat mockup tiga alternatif fitur "Panduan Vaksinasi di Indonesia".
// Memakai CSS, font, dan ikon asli aplikasi supaya tampilannya identik.
var fs = require('fs'), path = require('path');
var ROOT = process.argv[2], OUT = process.argv[3];
var src = fs.readFileSync(path.join(ROOT, 'app/app.js'), 'utf8');
eval(src.slice(src.indexOf('  var ICON = {'), src.indexOf('  /* ============================ util')));
function h(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }
var css = fs.readFileSync(path.join(ROOT, 'app/styles.css'), 'utf8');
var fonts = fs.readFileSync(process.argv[4], 'utf8');

function hp(judul, isi, nav) {
  return '<div class="hp"><div class="statusbar"><span>09.41</span><span>●●● 4G ▮</span></div>' + isi + (nav === false ? '' : navbar()) + '</div>';
}
function navbar() {
  var it = [['beranda', 'Beranda'], ['konsultasi', 'Konsultasi'], null, ['rekam', 'Rekam Medis'], ['profil', 'Profil']];
  return '<nav class="navbar">' + it.map(function (x) {
    if (!x) return '<button class="navfab">' + ic('plus', 24, 2.4) + '</button>';
    return '<button class="navitem">' + icm(x[0], 26) + '<span>' + x[1] + '</span></button>';
  }).join('') + '</nav>';
}
function topbar(j, s, back, extra) {
  return '<div class="topbar">' + (back ? '<button class="backbtn">' + ic('back', 20, 2.2) + '</button>' : '') +
    '<div class="grow"><h1>' + j + '</h1>' + (s ? '<div class="sub">' + s + '</div>' : '') + '</div>' + (extra || '') + '</div>';
}
function cari(ph) {
  return '<div style="position:relative;"><input class="input" placeholder="' + ph + '" style="padding-left:38px;">' +
    '<span style="position:absolute;left:12px;top:12px;color:var(--ink-4);">' + ic('search', 18) + '</span></div>';
}
var JADWAL = [
  ['pasien', 'Anak · IDAI 2024', '0–18 tahun'], ['rekam', 'Anak · Buku KIA', 'Program pemerintah'],
  ['profil', 'Dewasa · PAPDI 2025', '19 tahun ke atas'], ['pengingat', 'Ibu Hamil · POGI', 'Flu, Tdap, RSV'],
  ['tentang', 'Pra Nikah', 'Calon pengantin'], ['jadwal', 'Lansia', '60 tahun ke atas'],
  ['internasional', 'Internasional', 'Haji, umrah, perjalanan']
];
var VAKSIN = [['Hepatitis B', 'Hati', 4], ['Polio', 'Kelumpuhan', 2], ['BCG', 'TBC', 1], ['DTP Combo', 'Difteri, tetanus, pertusis', 4],
  ['Tdap / Td', 'Usia 7 tahun ke atas', 3], ['PCV', 'Pneumonia, IPD', 3], ['Rotavirus', 'Diare berat', 2], ['Influenza', 'Flu musiman', 5]];
function ikonV(n) { return /combo|\+/i.test(n) ? 'suntik-combo' : 'suntik'; }

/* ---------------- Alternatif A: Ensiklopedia kartu + akordeon ---------------- */
var aHome = topbar('Panduan Vaksinasi', 'Di Indonesia · 22 jenis vaksin', true) +
  '<div class="scroll pad stack g14">' + cari('Cari vaksin atau penyakit…') +
  '<div class="stack g8"><div class="row mid between"><div class="sect-title">Jadwal vaksinasi</div><span class="tiny muted">7 jadwal</span></div>' +
  '<div class="mk-grid3">' + JADWAL.slice(0, 6).map(function (j) {
    return '<div class="mk-tile">' + ikonKotak(j[0], '', 44) + '<b>' + j[1] + '</b><span>' + j[2] + '</span></div>';
  }).join('') + '</div></div>' +
  '<div class="stack g8"><div class="sect-title">Jenis vaksin</div>' +
  '<div class="mk-grid2">' + VAKSIN.slice(0, 6).map(function (v) {
    return '<div class="card mk-vk">' + ikonKotak(ikonV(v[0]), '', 38) + '<div><b>' + v[0] + '</b><span>' + v[1] + '</span></div>' +
      '<span class="chip teal" style="font-size:10px;">' + v[2] + ' merek</span></div>';
  }).join('') + '</div></div></div>';

var aDetail = topbar('Vaksin Hepatitis B', 'Panduan Vaksinasi', true) +
  '<div class="scroll stack" style="padding-bottom:84px;">' +
  '<div class="mk-hero">' + ikonKotak('suntik', '', 56) + '<div><div class="disp" style="font-size:20px;font-weight:800;">Hepatitis B</div>' +
  '<div class="small">Mencegah infeksi virus Hepatitis B penyebab sirosis &amp; kanker hati</div>' +
  '<div class="row g6" style="margin-top:8px;"><span class="chip green">Gratis di Puskesmas</span><span class="chip teal">Anak &amp; dewasa</span></div></div></div>' +
  '<div class="pad stack g10">' +
  '<div class="card stack g8"><div class="row mid between"><b>Merek tersedia</b><span class="tiny muted">4 merek</span></div>' +
  [['Engerix-B', 'GSK · Inggris', 'Anak & dewasa'], ['Vecon', 'Bio Farma · Indonesia', 'Anak & dewasa'], ['Twinrix', 'GSK · Inggris', 'Kombinasi Hep A + Hep B']].map(function (m) {
    return '<div class="row mid g10 mk-merek">' + ikonKotak('suntik', '', 32) + '<div class="grow"><b>' + m[0] + '</b><div class="tiny muted">' + m[1] + ' · ' + m[2] + '</div></div><span class="tiny" style="color:var(--teal-dark);font-weight:700;">Tersedia</span></div>';
  }).join('') + '</div>' +
  ['Manfaat', 'Jadwal pemberian', 'Siapa yang tidak boleh', 'Reaksi setelah vaksin', 'Pertanyaan umum'].map(function (s, i) {
    return '<div class="card mk-acc' + (i === 1 ? ' buka' : '') + '"><div class="row mid between"><b>' + s + '</b>' + ic('chevron', 16) + '</div>' +
      (i === 1 ? '<div class="mk-tl">' + [['Lahir (<24 jam)', 'Dosis 0 · di rumah sakit'], ['2 · 3 · 4 bulan', 'Dosis 1–3, lewat vaksin kombinasi'], ['18 bulan', 'Booster']].map(function (t) {
        return '<div><i></i><b>' + t[0] + '</b><span>' + t[1] + '</span></div>'; }).join('') +
        '<div class="tiny muted" style="margin-top:6px;">Dewasa: 3 dosis, jadwal 0–1–6 bulan</div></div>' : '') + '</div>';
  }).join('') + '</div></div>' +
  '<div class="mk-cta"><div><div class="tiny muted">Mulai dari · Klinik Alrasha HCC</div><b class="disp" style="font-size:16px;color:var(--magenta-dark);">Rp350.000</b></div><button class="btn primary sm">Booking vaksin ini</button></div>';

/* ---------------- Alternatif B: Daftar per tahap usia + tab di profil ---------------- */
var bHome = topbar('Panduan Vaksinasi', 'Pilih tahap usia atau cari vaksin', true) +
  '<div class="scroll pad stack g12">' + cari('Cari: hepatitis, HPV, flu…') +
  '<div class="row g6"><span class="mk-pill on">Tahap usia</span><span class="mk-pill">Jenis vaksin</span><span class="mk-pill">Penyakit</span></div>' +
  [['pasien', 'Bayi & Anak', '0–18 tahun', 'IDAI 2024', 'Buku KIA'], ['profil', 'Dewasa', '19–59 tahun', 'PAPDI 2025'],
   ['pengingat', 'Ibu Hamil', 'Per kehamilan', 'POGI'], ['tentang', 'Pra Nikah', 'Calon pengantin', 'PAPDI'],
   ['jadwal', 'Lansia', '60 tahun ke atas', 'PAPDI 2025'], ['internasional', 'Perjalanan', 'Haji, umrah, luar negeri', 'Kemenkes · WHO']].map(function (t) {
    return '<div class="card row mid g12" style="padding:12px 14px;">' + ikonKotak(t[0], '', 46) +
      '<div class="grow"><b>' + t[1] + '</b><div class="tiny muted">' + t[2] + '</div>' +
      '<div class="row g4" style="margin-top:5px;">' + t.slice(3).map(function (c) { return '<span class="chip teal" style="font-size:10px;padding:2px 8px;">' + c + '</span>'; }).join('') + '</div></div>' +
      '<span style="color:var(--ink-4);">' + ic('chevron', 16) + '</span></div>';
  }).join('') + '</div>';

var bDetail = '<div class="topbar">' + '<button class="backbtn">' + ic('back', 20, 2.2) + '</button><div class="grow"><h1>Hepatitis B</h1><div class="sub">Mencegah infeksi hati kronis</div></div></div>' +
  '<div style="background:var(--teal-dark);padding:0 18px 0;"><div class="mk-seg">' + ['Ringkasan', 'Merek', 'Jadwal', 'Keamanan', 'Tanya-jawab'].map(function (t, i) {
    return '<span' + (i === 0 ? ' class="on"' : '') + '>' + t + '</span>'; }).join('') + '</div></div>' +
  '<div class="scroll pad stack g12" style="padding-bottom:84px;">' +
  '<div class="mk-fakta">' + [['Mulai usia', 'Lahir (<24 jam)'], ['Jumlah dosis', 'Anak 4 · Dewasa 3'], ['Cara', 'Suntik otot'], ['Booster', '18 bulan']].map(function (f) {
    return '<div><span>' + f[0] + '</span><b>' + f[1] + '</b></div>'; }).join('') + '</div>' +
  '<div class="card stack g6"><b>Kenapa penting?</b><div class="small" style="color:var(--ink-2);line-height:1.6;">Virus Hepatitis B menular lewat darah dan cairan tubuh, termasuk dari ibu ke bayi saat lahir. Infeksi yang menahun dapat merusak hati hingga sirosis dan kanker hati.</div></div>' +
  '<div class="card row mid g10" style="background:var(--green-tint);border-color:transparent;">' + icm('rekam', 28) +
  '<div class="grow small"><b>Termasuk program pemerintah.</b> Dosis anak tersedia gratis di Puskesmas &amp; Posyandu.</div></div>' +
  '<div class="card stack g6"><b>Jadwal anak Anda</b><div class="row mid between small"><span>Nadia · 5 tahun</span><span class="chip green">Lengkap 4/4</span></div>' +
  '<div class="row mid between small"><span>Bayi Rafa · 2 bulan</span><span class="chip amber">Dosis 1 jatuh tempo</span></div></div></div>' +
  '<div class="mk-cta"><div><div class="tiny muted">Klinik Alrasha HCC · Tanjungpinang</div><b class="disp" style="font-size:16px;color:var(--magenta-dark);">Rp350.000</b></div><button class="btn primary sm">Booking</button></div>';

/* ---------------- Alternatif C: Lembar ringkas dari mana saja + halaman panduan ---------------- */
var cHome = topbar('Daftar Harga', 'Klinik Alrasha HCC · Dokter Umum', true) +
  '<div class="scroll pad stack g10" style="filter:brightness(.62);">' +
  [['Hepatitis B', 'Engerix-B Anak', 'Rp350.000'], ['Polio', 'Polio Injeksi (IPV)', 'Rp305.000'], ['DPT / DPT Combo', 'Infanrix Hexa', 'Rp1.000.000']].map(function (r) { var n = r[0];
    return '<div class="card stack g6"><div class="row mid g10">' + ikonKotak(ikonV(n), '', 38) + '<b>' + n + '</b><span class="tiny" style="margin-left:auto;color:var(--teal-dark);font-weight:700;">ⓘ Panduan</span></div>' +
      '<div class="row between small"><span>' + r[1] + '</span><b style="color:var(--magenta-dark);">' + r[2] + '</b></div></div>';
  }).join('') + '</div>' +
  '<div class="mk-sheet"><div class="mk-grip"></div><div class="row mid g12">' + ikonKotak('suntik', '', 52) +
  '<div class="grow"><div class="disp" style="font-size:19px;font-weight:800;">Hepatitis B</div><div class="tiny muted">Mencegah infeksi hati kronis, sirosis &amp; kanker hati</div></div></div>' +
  '<div class="mk-fakta" style="margin-top:12px;">' + [['Mulai', 'Lahir'], ['Dosis', '4 (anak)'], ['Gratis', 'Puskesmas']].map(function (f) {
    return '<div><span>' + f[0] + '</span><b>' + f[1] + '</b></div>'; }).join('') + '</div>' +
  '<div class="small" style="color:var(--ink-2);line-height:1.6;margin-top:10px;">Merek: Engerix-B, Vecon, Euvax B, Twinrix (kombinasi Hep A + B). Reaksi umumnya ringan: demam, nyeri di bekas suntikan.</div>' +
  '<div class="row g8" style="margin-top:12px;"><button class="btn outline sm grow">Baca panduan lengkap</button><button class="btn primary sm grow">Booking</button></div></div>';

var cDetail = topbar('Panduan Vaksinasi', 'Hepatitis B', true) +
  '<div class="scroll stack" style="padding-bottom:20px;">' +
  '<div class="mk-chipnav">' + ['Hepatitis B', 'Polio', 'BCG', 'DTP Combo', 'Tdap', 'PCV'].map(function (n, i) {
    return '<span class="mk-pill' + (i === 0 ? ' on' : '') + '">' + n + '</span>'; }).join('') + '</div>' +
  '<div class="pad stack g14" style="padding-top:6px;">' +
  '<div class="stack g6"><div class="mk-h">Ada merek apa saja?</div><div class="mk-merk3">' +
  [['Engerix-B', 'GSK'], ['Vecon', 'Bio Farma'], ['Euvax B', 'Sanofi'], ['Twinrix', 'GSK · Hep A+B']].map(function (m) {
    return '<div>' + icm('suntik', 30) + '<b>' + m[0] + '</b><span>' + m[1] + '</span></div>'; }).join('') + '</div></div>' +
  '<div class="stack g6"><div class="mk-h">Jadwal pemberian</div><table class="mk-tbl"><tr><th></th><th>IDAI</th><th>Buku KIA</th></tr>' +
  [['Dosis 0', 'Lahir', '0–24 jam'], ['Dosis 1', '2 bln', '2 bln'], ['Dosis 2', '3 bln', '3 bln'], ['Dosis 3', '4 bln', '4 bln'], ['Booster', '18 bln', '18 bln']].map(function (r) {
    return '<tr><td>' + r[0] + '</td><td>' + r[1] + '</td><td>' + r[2] + '</td></tr>'; }).join('') + '</table></div>' +
  '<div class="stack g6"><div class="mk-h">Siapa yang tidak boleh?</div><div class="small" style="color:var(--ink-2);line-height:1.6;">• Alergi berat pada komponen vaksin atau pada dosis sebelumnya<br>• Sedang demam tinggi atau infeksi akut — ditunda dulu</div></div>' +
  '<div class="stack g6"><div class="mk-h">Tanya-jawab</div><div class="card small" style="padding:12px 14px;"><b>Perlu cek darah dulu sebelum vaksin?</b><div class="muted" style="margin-top:4px;">Tidak wajib. Vaksin tetap dapat diberikan tanpa pemeriksaan serologi.</div></div></div>' +
  '<div class="tiny muted" style="border-top:1px solid var(--line);padding-top:10px;">Informasi ini tidak menggantikan anjuran dokter.</div></div></div>';

var extra = '.hp{width:360px;height:760px;border-radius:34px;overflow:hidden;background:var(--bg);display:flex;flex-direction:column;position:relative;' +
  'box-shadow:0 30px 50px -25px rgba(20,20,20,.45),0 0 0 10px #17191c,0 0 0 12px #2a2d31;}' +
  '.statusbar{display:flex;justify-content:space-between;padding:8px 22px 6px;font-size:11px;font-weight:700;background:var(--teal-dark);color:#fff;}' +
  '.hp .scroll{flex:1;overflow:hidden;}' +
  '.mk-grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;}' +
  '.mk-tile{background:#fff;border:1px solid var(--line);border-radius:16px;padding:10px 6px;display:flex;flex-direction:column;align-items:center;gap:5px;text-align:center;}' +
  '.mk-tile b{font-size:10.5px;line-height:1.25;} .mk-tile span{font-size:9.5px;color:var(--ink-3);line-height:1.2;}' +
  '.mk-grid2{display:grid;grid-template-columns:1fr 1fr;gap:8px;}' +
  '.mk-vk{padding:10px;display:flex;flex-direction:column;gap:6px;} .mk-vk b{font-size:12.5px;display:block;} .mk-vk span{font-size:10.5px;color:var(--ink-3);}' +
  '.mk-vk .chip{align-self:flex-start;}' +
  '.mk-hero{display:flex;gap:14px;align-items:flex-start;padding:18px;background:linear-gradient(120deg,var(--teal-tint) 0%,var(--magenta-tint) 100%);}' +
  '.mk-merek{padding:6px 0;border-top:1px solid var(--line);} .mk-merek b{font-size:12.5px;}' +
  '.mk-acc{padding:13px 14px;} .mk-acc b{font-size:13px;} .mk-acc.buka svg{transform:rotate(90deg);}' +
  '.mk-tl{margin-top:10px;border-left:2px solid var(--teal-tint2);padding-left:14px;display:flex;flex-direction:column;gap:8px;}' +
  '.mk-tl div{position:relative;font-size:12px;} .mk-tl i{position:absolute;left:-20px;top:4px;width:10px;height:10px;border-radius:50%;background:var(--teal);}' +
  '.mk-tl b{display:block;} .mk-tl span{color:var(--ink-3);font-size:11px;}' +
  '.mk-cta{position:absolute;left:0;right:0;bottom:62px;background:#fff;border-top:1px solid var(--line);padding:10px 18px;display:flex;align-items:center;justify-content:space-between;}' +
  '.mk-seg{display:flex;gap:16px;overflow:hidden;} .mk-seg span{color:rgba(255,255,255,.75);font-size:12.5px;font-weight:700;padding:10px 0;white-space:nowrap;border-bottom:3px solid transparent;}' +
  '.mk-seg span.on{color:#fff;border-bottom-color:#fff;}' +
  '.mk-fakta{display:grid;grid-template-columns:1fr 1fr;gap:8px;} .mk-sheet .mk-fakta{grid-template-columns:repeat(3,1fr);}' +
  '.mk-fakta div{background:var(--teal-tint);border-radius:12px;padding:9px 11px;} .mk-fakta span{display:block;font-size:10px;color:var(--teal-dark);font-weight:700;} .mk-fakta b{font-size:12.5px;}' +
  '.mk-sheet{position:absolute;left:0;right:0;bottom:62px;background:#fff;border-radius:22px 22px 0 0;padding:10px 18px 18px;box-shadow:0 -10px 30px rgba(0,0,0,.18);}' +
  '.mk-grip{width:40px;height:4px;border-radius:4px;background:var(--line-2);margin:0 auto 12px;}' +
  '.mk-chipnav{flex-shrink:0;display:flex;gap:6px;overflow:hidden;padding:12px 18px 6px;} .mk-pill{display:inline-block;border:1.4px solid var(--line-2);background:#fff;border-radius:999px;padding:7px 12px;font-size:11.5px;font-weight:700;white-space:nowrap;color:var(--ink-2);} .mk-pill.on{background:var(--teal-dark);border-color:var(--teal-dark);color:#fff;}' +
  '.mk-h{font-family:var(--disp);font-size:15px;font-weight:800;}' +
  '.mk-merk3{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;} .mk-merk3 div{background:#fff;border:1px solid var(--line);border-radius:12px;padding:8px 4px;display:flex;flex-direction:column;align-items:center;text-align:center;}' +
  '.mk-merk3 b{font-size:10.5px;} .mk-merk3 span{font-size:9px;color:var(--ink-3);}' +
  '.mk-tbl{width:100%;border-collapse:collapse;font-size:12px;background:#fff;border-radius:12px;overflow:hidden;} .mk-tbl th{background:var(--teal-dark);color:#fff;padding:7px;font-size:11px;}' +
  '.mk-tbl td{padding:7px;border-top:1px solid var(--line);text-align:center;} .mk-tbl td:first-child{text-align:left;font-weight:700;}' +
  '.alt{display:flex;flex-direction:column;gap:18px;} .alt h2{font-family:var(--disp);margin:0;font-size:24px;} .alt p{margin:0;font-size:14px;color:var(--ink-2);max-width:760px;line-height:1.55;}' +
  '.pasang{display:flex;gap:40px;} .label{font-size:12px;font-weight:700;color:var(--ink-3);margin-bottom:12px;text-transform:uppercase;letter-spacing:.06em;}';

function blok(huruf, nama, desk, s1, l1, s2, l2) {
  return '<section class="alt"><div><h2>Alternatif ' + huruf + ' · ' + nama + '</h2><p>' + desk + '</p></div>' +
    '<div class="pasang"><div><div class="label">' + l1 + '</div>' + s1 + '</div><div><div class="label">' + l2 + '</div>' + s2 + '</div></div></section>';
}
var html = '<!doctype html><html lang="id"><head><meta charset="utf-8"><title>Mockup Panduan Vaksinasi</title><style>' + fonts + '</style><style>' + css + extra +
  'body{background:#F1EFEA;padding:40px 48px;margin:0;} .wrap{display:flex;flex-direction:column;gap:64px;}</style></head><body><div class="wrap">' +
  '<div><h1 class="disp" style="margin:0;font-size:32px;">Panduan Vaksinasi di Indonesia — 3 alternatif desain</h1>' +
  '<p style="margin:6px 0 0;color:var(--ink-2);">Contoh isi: Vaksin Hepatitis B. Semua alternatif dibuka dengan mengetuk nama vaksin di mana pun (Daftar Harga, Jadwal, Rekam Medis, Booking) dan dari menu Profil → Panduan Vaksinasi.</p></div>' +
  blok('A', 'Ensiklopedia kartu', 'Beranda panduan berupa ubin jadwal (IDAI, KIA, PAPDI, POGI, Pra Nikah, Lansia, Internasional) dan kartu jenis vaksin. Profil vaksin: kepala berwarna, daftar merek, lalu bagian-bagian yang bisa dibuka-tutup. Tombol booking dengan harga klinik terpilih menempel di bawah.',
    hp('', aHome), 'Beranda panduan', hp('', aDetail), 'Profil vaksin') +
  blok('B', 'Per tahap usia + tab', 'Beranda panduan dikelompokkan menurut tahap hidup — orang tua langsung menemukan yang relevan. Profil vaksin memakai tab (Ringkasan · Merek · Jadwal · Keamanan · Tanya-jawab), dibuka dengan fakta singkat dan status vaksin anggota keluarga sendiri.',
    hp('', bHome), 'Beranda panduan', hp('', bDetail), 'Profil vaksin · tab Ringkasan') +
  blok('C', 'Lembar ringkas + halaman baca', 'Mengetuk nama vaksin di mana pun memunculkan lembar ringkas dari bawah tanpa meninggalkan layar; "Baca panduan lengkap" membuka halaman baca satu gulir dengan pindah cepat antar-vaksin dan tabel IDAI vs Buku KIA berdampingan.',
    hp('', cHome), 'Ketuk nama vaksin di Daftar Harga', hp('', cDetail), 'Halaman panduan lengkap') +
  '</div></body></html>';
fs.writeFileSync(OUT, html);
console.log('ok', OUT);
