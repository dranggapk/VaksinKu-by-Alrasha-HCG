// Layanan masuk VaksinKu: menukar token Google (ID token) dengan sesi VaksinKu.
//
//   POST /auth/google   {"credential": "<ID token dari Google Identity Services>"}
//     → 200 {"token", "exp", "akun": {"id", "email", "nama", "foto"}}
//   GET  /auth/sehat    → 200 {"ok": true}
//
// Token Google diverifikasi sepenuhnya di sini: tanda tangan RS256 dengan kunci publik
// Google, penerbit, aplikasi tujuan (aud = Client ID VaksinKu), masa berlaku, dan email
// terverifikasi. Sesudah itu akun didaftarkan lewat PostgREST (public.masuk_google) dan
// sesi ditandatangani HS256 dengan PGRST_JWT_SECRET — kunci yang sama dipakai PostgREST
// untuk memeriksa setiap permintaan /api. Tanpa dependensi npm.
import http from 'node:http';
import crypto from 'node:crypto';

const ENV = process.env;
const PORT = Number(ENV.PORT || 8080);
const CLIENT_ID = (ENV.GOOGLE_CLIENT_ID || '').trim();
const JWKS_URL = ENV.GOOGLE_JWKS_URL || 'https://www.googleapis.com/oauth2/v3/certs';
const ISSUERS = (ENV.GOOGLE_ISSUERS || 'accounts.google.com,https://accounts.google.com').split(',');
const API_URL = (ENV.API_URL || 'http://api:3000').replace(/\/$/, '');
const SECRET = ENV.PGRST_JWT_SECRET || '';
const SESI_DETIK = Number(ENV.SESI_DETIK || 7 * 24 * 3600);
const BATAS_PER_MENIT = Number(ENV.BATAS_PER_MENIT || 20);

if (SECRET.length < 32) {
  console.error('PGRST_JWT_SECRET wajib diisi, minimal 32 karakter.');
  process.exit(1);
}

const b64url = (buf) => Buffer.from(buf).toString('base64url');
const json = (o) => b64url(JSON.stringify(o));

function tandaTangan(payload) {
  const kepala = json({ alg: 'HS256', typ: 'JWT' });
  const isi = json(payload);
  const sig = crypto.createHmac('sha256', SECRET).update(`${kepala}.${isi}`).digest('base64url');
  return `${kepala}.${isi}.${sig}`;
}

// ---------------------------------------------------------------- kunci publik Google
let jwks = { kunci: new Map(), sampai: 0 };
async function kunciGoogle(kid) {
  if (Date.now() > jwks.sampai || !jwks.kunci.has(kid)) {
    const r = await fetch(JWKS_URL);
    if (!r.ok) throw new Error(`JWKS ${r.status}`);
    const data = await r.json();
    const umur = Number((/max-age=(\d+)/.exec(r.headers.get('cache-control') || '') || [])[1] || 3600);
    jwks = {
      kunci: new Map(data.keys.map((k) => [k.kid, crypto.createPublicKey({ key: k, format: 'jwk' })])),
      sampai: Date.now() + Math.min(umur, 6 * 3600) * 1000,
    };
  }
  return jwks.kunci.get(kid);
}

async function verifikasiGoogle(token) {
  const bagian = String(token || '').split('.');
  if (bagian.length !== 3) throw new Error('format token');
  const kepala = JSON.parse(Buffer.from(bagian[0], 'base64url'));
  if (kepala.alg !== 'RS256' || !kepala.kid) throw new Error('algoritma token');
  const kunci = await kunciGoogle(kepala.kid);
  if (!kunci) throw new Error('kunci tidak dikenal');
  const sah = crypto.verify('RSA-SHA256', Buffer.from(`${bagian[0]}.${bagian[1]}`),
    kunci, Buffer.from(bagian[2], 'base64url'));
  if (!sah) throw new Error('tanda tangan');
  const d = JSON.parse(Buffer.from(bagian[1], 'base64url'));
  const kini = Math.floor(Date.now() / 1000);
  if (!ISSUERS.includes(d.iss)) throw new Error('penerbit');
  const aud = Array.isArray(d.aud) ? d.aud : [d.aud];
  if (!CLIENT_ID || !aud.includes(CLIENT_ID)) throw new Error('aplikasi tujuan');
  if (!(d.exp > kini - 30)) throw new Error('kedaluwarsa');
  if (d.iat && d.iat > kini + 300) throw new Error('waktu terbit');
  if (!d.sub || !d.email || d.email_verified === false || d.email_verified === 'false') throw new Error('email belum terverifikasi');
  return d;
}

async function daftarkan(d) {
  const tokenLayanan = tandaTangan({ role: 'layanan_masuk', exp: Math.floor(Date.now() / 1000) + 60 });
  const r = await fetch(`${API_URL}/rpc/masuk_google`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${tokenLayanan}` },
    body: JSON.stringify({ p_sub: d.sub, p_email: d.email, p_nama: d.name || '', p_foto: d.picture || '' }),
  });
  if (!r.ok) throw new Error(`daftar ${r.status} ${await r.text()}`);
  return r.json();
}

// ---------------------------------------------------------------- batas permintaan
const hitungan = new Map();
function terlaluSering(ip) {
  const menit = Math.floor(Date.now() / 60000);
  const kunci = `${ip}|${menit}`;
  const n = (hitungan.get(kunci) || 0) + 1;
  hitungan.set(kunci, n);
  if (hitungan.size > 5000) for (const k of hitungan.keys()) if (!k.endsWith(`|${menit}`)) hitungan.delete(k);
  return n > BATAS_PER_MENIT;
}

function kirim(res, kode, isi) {
  res.writeHead(kode, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
  res.end(JSON.stringify(isi));
}

function bacaBody(req, maks = 16384) {
  return new Promise((ok, gagal) => {
    let isi = '';
    req.on('data', (c) => { isi += c; if (isi.length > maks) { gagal(new Error('terlalu besar')); req.destroy(); } });
    req.on('end', () => ok(isi));
    req.on('error', gagal);
  });
}

const server = http.createServer(async (req, res) => {
  const jalur = req.url.split('?')[0];
  if (req.method === 'GET' && jalur === '/auth/sehat') return kirim(res, 200, { ok: true, clientId: Boolean(CLIENT_ID) });
  if (req.method !== 'POST' || jalur !== '/auth/google') return kirim(res, 404, { pesan: 'Tidak ditemukan' });

  const ip = String(req.headers['x-forwarded-for'] || req.socket.remoteAddress || '').split(',')[0].trim();
  if (terlaluSering(ip)) return kirim(res, 429, { pesan: 'Terlalu banyak percobaan. Coba lagi sebentar.' });
  if (!CLIENT_ID) return kirim(res, 503, { pesan: 'Masuk dengan Google belum dikonfigurasi.' });

  let credential;
  try { credential = JSON.parse(await bacaBody(req)).credential; } catch { return kirim(res, 400, { pesan: 'Permintaan tidak valid' }); }

  let d;
  try { d = await verifikasiGoogle(credential); } catch (e) {
    console.warn('tolak token:', e.message);
    return kirim(res, 401, { pesan: 'Akun Google tidak dapat diverifikasi.' });
  }
  try {
    const id = await daftarkan(d);
    const exp = Math.floor(Date.now() / 1000) + SESI_DETIK;
    const token = tandaTangan({ sub: id, role: 'authenticated', email: d.email, iat: Math.floor(Date.now() / 1000), exp });
    return kirim(res, 200, { token, exp, akun: { id, email: d.email, nama: d.name || '', foto: d.picture || '' } });
  } catch (e) {
    console.error('gagal daftar:', e.message);
    return kirim(res, 502, { pesan: 'Server VaksinKu sedang bermasalah. Coba lagi.' });
  }
});

server.listen(PORT, () => console.log(`layanan masuk VaksinKu di port ${PORT}`));
