// Uji ujung-ke-ujung backend VaksinKu di VPS: PostgreSQL + PostgREST + layanan masuk.
//
// Membuat database baru, memasang deploy/backend/db/00_auth.sql, migrasi
// supabase/migrations, 50_masuk_google.sql, dan seed; lalu menjalankan PostgREST dan
// layanan masuk (deploy/backend/auth/server.mjs) dengan server kunci Google tiruan,
// sehingga token Google sah, palsu, kedaluwarsa, dan untuk aplikasi lain bisa diuji.
//
//   node src/uji_backend.mjs
//   PGURL=postgresql://postgres@127.0.0.1:54329 POSTGREST=/jalur/postgrest node src/uji_backend.mjs
import { spawn, execFileSync } from 'node:child_process';
import crypto from 'node:crypto';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const PGURL = process.env.PGURL || 'postgresql://postgres@127.0.0.1:54329';
const POSTGREST = process.env.POSTGREST || 'postgrest';
const DB = 'vaksinku_e2e';
const PORT_API = 3101, PORT_AUTH = 8181, PORT_JWKS = 8282, PORT_WEB = 8099;
const CADDY = process.env.CADDY || '';   // bila diisi: uji juga lewat deploy/web/Caddyfile
const CLIENT_ID = 'uji-vaksinku.apps.googleusercontent.com';
const SECRET = crypto.randomBytes(48).toString('base64');
const PW_AUTH = crypto.randomBytes(18).toString('hex');

const hasil = [];
const ok = (nama, syarat, detail = '') => hasil.push(`${syarat ? 'LULUS' : 'GAGAL'} | ${nama}${detail ? ' | ' + detail : ''}`);

function psql(db, ...args) {
  return execFileSync('psql', [`${PGURL}/${db}`, '-v', 'ON_ERROR_STOP=1', '-X', '-q', '-At', ...args], { encoding: 'utf8' });
}

// ---------------------------------------------------------------- database
psql('postgres', '-c', `drop database if exists ${DB} with (force)`);
psql('postgres', '-c', `create database ${DB}`);
const berkas = [
  'deploy/backend/db/00_auth.sql',
  ...fs.readdirSync(path.join(ROOT, 'supabase/migrations')).filter((f) => f.endsWith('.sql')).sort().map((f) => `supabase/migrations/${f}`),
  'deploy/backend/db/50_masuk_google.sql',
  'supabase/seed.sql',
];
for (const f of berkas) psql(DB, '-f', path.join(ROOT, f));
psql(DB, '-c', `alter role authenticator with login password '${PW_AUTH}'`);

// ---------------------------------------------------------------- Google tiruan
const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const palsu = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const jwk = { ...publicKey.export({ format: 'jwk' }), kid: 'kunci-uji', alg: 'RS256', use: 'sig' };
const jwks = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'application/json', 'Cache-Control': 'public, max-age=60' });
  res.end(JSON.stringify({ keys: [jwk] }));
}).listen(PORT_JWKS);

const b64 = (o) => Buffer.from(JSON.stringify(o)).toString('base64url');
function tokenGoogle(ubah = {}, kunci = privateKey, kepala = {}) {
  const kini = Math.floor(Date.now() / 1000);
  const isi = { iss: 'https://accounts.google.com', aud: CLIENT_ID, sub: '1001', email: 'sari@gmail.com',
    email_verified: true, name: 'Ibu Sari', picture: 'https://contoh/foto.jpg', iat: kini, exp: kini + 600, ...ubah };
  const h = b64({ alg: 'RS256', kid: 'kunci-uji', typ: 'JWT', ...kepala });
  const p = b64(isi);
  const sig = crypto.sign('RSA-SHA256', Buffer.from(`${h}.${p}`), kunci).toString('base64url');
  return `${h}.${p}.${sig}`;
}

// ---------------------------------------------------------------- layanan
const proses = [];
function jalankan(cmd, args, env) {
  const p = spawn(cmd, args, { env: { ...process.env, ...env }, stdio: ['ignore', 'pipe', 'pipe'] });
  let log = '';
  p.stdout.on('data', (d) => { log += d; });
  p.stderr.on('data', (d) => { log += d; });
  p.log = () => log;
  proses.push(p);
  return p;
}
const u = new URL(PGURL);
const api = jalankan(POSTGREST, [], {
  PGRST_DB_URI: `postgres://authenticator:${PW_AUTH}@${u.hostname}:${u.port}/${DB}`,
  PGRST_DB_SCHEMAS: 'public', PGRST_DB_ANON_ROLE: 'anon', PGRST_JWT_SECRET: SECRET,
  PGRST_SERVER_PORT: String(PORT_API), PGRST_OPENAPI_MODE: 'disabled', PGRST_DB_CHANNEL_ENABLED: 'false',
});
const auth = jalankan('node', [path.join(ROOT, 'deploy/backend/auth/server.mjs')], {
  PORT: String(PORT_AUTH), GOOGLE_CLIENT_ID: CLIENT_ID, GOOGLE_JWKS_URL: `http://127.0.0.1:${PORT_JWKS}/certs`,
  API_URL: `http://127.0.0.1:${PORT_API}`, PGRST_JWT_SECRET: SECRET, BATAS_PER_MENIT: '100',
});

let web = null;
if (CADDY) {
  const tmp = fs.mkdtempSync('/tmp/vaksinku-web-');
  fs.writeFileSync(path.join(tmp, 'index.html'), '<title>VaksinKu</title>');
  const cf = fs.readFileSync(path.join(ROOT, 'deploy/web/Caddyfile'), 'utf8')
    .replace(':80 {', `:${PORT_WEB} {`).replace('root * /srv', `root * ${tmp}`)
    .replace('auth:8080', `127.0.0.1:${PORT_AUTH}`).replace('api:3000', `127.0.0.1:${PORT_API}`);
  fs.writeFileSync(path.join(tmp, 'Caddyfile'), cf);
  web = jalankan(CADDY, ['run', '--config', path.join(tmp, 'Caddyfile'), '--adapter', 'caddyfile'], {});
}

async function tunggu(url) {
  for (let i = 0; i < 100; i++) {
    try { const r = await fetch(url); if (r.status < 500) return; } catch { /* belum menyala */ }
    await new Promise((r) => setTimeout(r, 100));
  }
  throw new Error(`tidak menyala: ${url}\n${api.log()}\n${auth.log()}`);
}

const API = `http://127.0.0.1:${PORT_API}`;
const AUTH = `http://127.0.0.1:${PORT_AUTH}`;
async function masuk(credential) {
  const r = await fetch(`${AUTH}/auth/google`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ credential }) });
  return { status: r.status, data: await r.json().catch(() => ({})) };
}
async function panggil(jalur, token, opsi = {}) {
  const headers = { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}), ...(opsi.headers || {}) };
  const r = await fetch(`${API}${jalur}`, { ...opsi, headers });
  const teks = await r.text();
  let data; try { data = JSON.parse(teks); } catch { data = teks; }
  return { status: r.status, data };
}
function hariKerja() {
  const t = new Date(Date.now() + 7 * 864e5);
  while (t.getUTCDay() === 0) t.setUTCDate(t.getUTCDate() + 1);
  return t.toISOString().slice(0, 10);
}

try {
  await tunggu(`${API}/klinik`);
  await tunggu(`${AUTH}/auth/sehat`);

  if (web) {
    const WEB = `http://127.0.0.1:${PORT_WEB}`;
    await tunggu(`${WEB}/`);
    const halaman = await fetch(`${WEB}/`);
    ok('web: halaman aplikasi tersaji, tanpa header Server', halaman.status === 200 && !halaman.headers.get('server') &&
      halaman.headers.get('cache-control') === 'no-cache', String(halaman.status));
    const lw = await fetch(`${WEB}/auth/google`, { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ credential: tokenGoogle({ sub: '3003', email: 'lewat-web@gmail.com' }) }) });
    const dw = await lw.json();
    ok('web: /auth/google diteruskan ke layanan masuk', lw.status === 200 && !!dw.token, String(lw.status));
    const pw = await fetch(`${WEB}/api/profil?select=nama`, { headers: { Authorization: `Bearer ${dw.token}` } });
    ok('web: /api/ diteruskan ke PostgREST (awalan dibuang)', pw.status === 200 && (await pw.json()).length === 1, String(pw.status));
    const besar = await fetch(`${WEB}/auth/google`, { method: 'POST', body: 'x'.repeat(40000) });
    ok('web: permintaan masuk terlalu besar ditolak', besar.status === 413 || besar.status === 400, String(besar.status));
  }

  // ---- katalog terbuka
  const kl = await panggil('/klinik?select=id&order=id');
  ok('anon: daftar klinik terbuka lewat API', kl.status === 200 && kl.data.length === 3, JSON.stringify(kl.data));
  const ps0 = await panggil('/pasien');
  ok('anon: data pasien tertutup', ps0.status === 401 || ps0.status === 403, String(ps0.status));

  // ---- penolakan token Google
  const tolak = [
    ['token untuk aplikasi lain', tokenGoogle({ aud: 'aplikasi-lain.apps.googleusercontent.com' })],
    ['token kedaluwarsa', tokenGoogle({ exp: Math.floor(Date.now() / 1000) - 3600 })],
    ['tanda tangan palsu', tokenGoogle({}, palsu.privateKey)],
    ['penerbit bukan Google', tokenGoogle({ iss: 'https://penipu.example' })],
    ['email belum terverifikasi', tokenGoogle({ email_verified: false })],
    ['algoritma none', `${b64({ alg: 'none', kid: 'kunci-uji' })}.${b64({ iss: 'accounts.google.com', aud: CLIENT_ID, sub: '1', email: 'x@y', exp: 9e9 })}.`],
    ['bukan token', 'abc'],
  ];
  for (const [nama, t] of tolak) {
    const r = await masuk(t);
    ok(`masuk: ${nama} ditolak`, r.status === 401 && !r.data.token, String(r.status));
  }

  // ---- masuk sah
  const a = await masuk(tokenGoogle());
  ok('masuk: token Google sah → sesi VaksinKu', a.status === 200 && !!a.data.token && /^[0-9a-f-]{36}$/.test(a.data.akun?.id || ''),
    `${a.status} ${a.data.akun?.email}`);
  const a2 = await masuk(tokenGoogle({ name: 'Ibu Sari W.' }));
  ok('masuk ulang: akun sama, tidak dobel', a2.data.akun?.id === a.data.akun?.id);
  const jumlahAkun = psql(DB, '-c', 'select count(*) from auth.users where google_sub = \'1001\'').trim();
  ok('masuk ulang: satu baris auth.users', jumlahAkun === '1', jumlahAkun);
  const S = a2.data.token;

  // ---- sesi dipakai ke API
  const prof = await panggil('/profil?select=id,nama', S);
  ok('sesi: profil dibuat otomatis dari akun Google', prof.status === 200 && prof.data.length === 1 && prof.data[0].nama === 'Ibu Sari',
    JSON.stringify(prof.data));
  const ubah = await panggil(`/profil?id=eq.${a.data.akun.id}`, S, { method: 'PATCH', body: JSON.stringify({ hp: '081234567890' }), headers: { Prefer: 'return=representation' } });
  ok('sesi: pemilik mengisi nomor HP di profil', ubah.status === 200 && ubah.data[0]?.hp === '081234567890', String(ubah.status));
  const anak = await panggil('/pasien', S, { method: 'POST', headers: { Prefer: 'return=representation' },
    body: JSON.stringify({ profil_id: a.data.akun.id, nama: 'Nadia', tgl_lahir: '2021-05-12', jenis_kelamin: 'Perempuan', hubungan: 'Anak' }) });
  ok('sesi: menambah anggota keluarga', anak.status === 201, `${anak.status} ${JSON.stringify(anak.data).slice(0, 80)}`);
  const pasienId = anak.data[0]?.id;

  const bk = await panggil('/rpc/buat_booking', S, { method: 'POST', body: JSON.stringify({
    p_klinik: 'alrasha-hcc', p_layanan: 'klinik', p_lokasi: '', p_tanggal: hariKerja(), p_jam: '09:00', p_tarif: 'umum',
    p_catatan: '', p_bagikan_riwayat: false, p_item: [{ pasien_id: pasienId, vaksin_id: 'v7-11' }] }) });
  ok('sesi: booking lewat API dengan harga dari server', bk.status === 200 && /^VK-/.test(bk.data.kode || ''), `${bk.status} ${bk.data.kode || JSON.stringify(bk.data).slice(0, 80)}`);

  // ---- pemisahan antar akun
  const b = await masuk(tokenGoogle({ sub: '2002', email: 'budi@gmail.com', name: 'Pak Budi' }));
  const psB = await panggil('/pasien?select=id', b.data.token);
  ok('akun lain: tidak melihat pasien Ibu Sari', psB.status === 200 && psB.data.length === 0, JSON.stringify(psB.data));
  const bkB = await panggil('/booking?select=id', b.data.token);
  ok('akun lain: tidak melihat booking Ibu Sari', bkB.status === 200 && bkB.data.length === 0);
  const curi = await panggil('/pasien', b.data.token, { method: 'POST',
    body: JSON.stringify({ profil_id: a.data.akun.id, nama: 'Titipan', tgl_lahir: '2020-01-01' }) });
  ok('akun lain: tidak bisa menambah pasien atas nama Ibu Sari', curi.status === 403 || curi.status === 401, String(curi.status));

  // ---- pemalsuan sesi & peran
  const rpc = await panggil('/rpc/masuk_google', S, { method: 'POST', body: JSON.stringify({ p_sub: '9', p_email: 'x@y', p_nama: '', p_foto: '' }) });
  ok('pengguna tidak bisa memanggil pendaftaran akun langsung', rpc.status === 401 || rpc.status === 403 || rpc.status === 404, String(rpc.status));
  const isiS = JSON.parse(Buffer.from(S.split('.')[1], 'base64url'));
  const palsuS = [S.split('.')[0], b64({ ...isiS, sub: b.data.akun.id }), S.split('.')[2]].join('.');
  const r1 = await panggil('/pasien', palsuS);
  ok('sesi yang diubah isinya ditolak', r1.status === 401, String(r1.status));
  const kepalaHS = b64({ alg: 'HS256', typ: 'JWT' });
  const isiLayanan = b64({ role: 'layanan_masuk', exp: 9e9 });
  const kunciLain = crypto.createHmac('sha256', 'kunci-tebakan-yang-salah-xxxxxxxxxxxx').update(`${kepalaHS}.${isiLayanan}`).digest('base64url');
  const r2 = await panggil('/rpc/masuk_google', `${kepalaHS}.${isiLayanan}.${kunciLain}`, { method: 'POST', body: '{}' });
  ok('peran layanan dengan kunci tebakan ditolak', r2.status === 401, String(r2.status));
  const sr = await panggil('/pasien', [kepalaHS, b64({ role: 'service_role', exp: 9e9 }), 'x'].join('.'));
  ok('peran service_role tidak bisa dipakai lewat API', sr.status === 401, String(sr.status));
} catch (e) {
  ok('uji berjalan tanpa galat', false, e.message);
} finally {
  for (const p of proses) p.kill();
  jwks.close();
}

for (const h of hasil) console.log(h);
const gagal = hasil.filter((h) => h.startsWith('GAGAL')).length;
console.log(`\n${hasil.length - gagal}/${hasil.length} lulus`);
if (gagal) { console.log('\n--- log auth ---\n' + auth.log()); process.exit(1); }
