#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import icon, ICONS
from data_katalog import (
    BRAND, PILAR, LAYANAN, TERMASUK, HARGA, HARGA_INTERNASIONAL, PAKET_TRIPLE,
    JADWAL_ANAK, JADWAL_DEWASA, JADWAL_DEWASA_CATATAN, dosis,
    JADWAL_PRANIKAH_VAKSIN, JADWAL_PRANIKAH_WAKTU, JADWAL_LANSIA,
    VAKSIN_INTERNASIONAL_WAJIB, VAKSIN_INTERNASIONAL_TAMBAHAN,
    DOKTER, KLINIK, ALUR_RESERVASI,
)

HERE = os.path.dirname(os.path.abspath(__file__))

def b64(name):
    with open(os.path.join(HERE, name), "rb") as f:
        return base64.b64encode(f.read()).decode()

LOGO_FULL = "data:image/png;base64," + b64("vaksinku-logo.png")
LOGO_MARK = "data:image/png;base64," + b64("vaksinku-logo-mark.png")

def logo_full(width=220):
    return f'<img src="{LOGO_FULL}" alt="VaksinKu" style="width:{width}px;">'

def logo_mark(height=24):
    return f'<img src="{LOGO_MARK}" alt="VaksinKu" style="height:{height}px;width:auto;">'

def navbar(active):
    items = [("home","Beranda","home"), ("chat","Chat","chat"), None, ("doc","Rekam Medis","rekammedis"), ("user","Profil","profile")]
    html = '<div class="navbar">'
    for it in items:
        if it is None:
            html += f'<div class="navfab tap" onclick="showScreen(\'booking\')">{icon("plus", 24, "#fff", 2.4)}</div>'
            continue
        key, label, target = it
        cls = "navitem active tap" if key == active else "navitem tap"
        color = "var(--magenta-dark)" if key == active else "var(--ink-4)"
        html += f'<div class="{cls}" onclick="showScreen(\'{target}\')">{icon(key, 22, color, 1.8)}<span>{label}</span></div>'
    html += '</div>'
    return html

GOOGLE_G = '<svg width="19" height="19" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.4 0 6.4 1.2 8.8 3.5l6.5-6.5C35.3 2.6 30 0 24 0 14.6 0 6.5 5.4 2.6 13.2l7.6 5.9C12.1 13 17.5 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.2-.4-4.7H24v9h12.7c-.5 3-2.2 5.5-4.7 7.2l7.3 5.7c4.3-4 6.8-9.9 6.8-17.2z"/><path fill="#FBBC05" d="M10.2 19.1a14.5 14.5 0 0 0 0 9.8l-7.6 5.9a24 24 0 0 1 0-21.6l7.6 5.9z"/><path fill="#34A853" d="M24 48c6 0 11.3-2 15-5.4l-7.3-5.7c-2 1.4-4.7 2.2-7.7 2.2-6.5 0-12-4.4-13.8-10.3l-7.6 5.9C6.5 42.6 14.6 48 24 48z"/></svg>'

# ---------------------------------------------------------------- SPLASH
splash = f'''
<div id="screen-splash" class="screen active" onclick="showScreen('onboarding')">
<div class="frame tap" style="position:relative;align-items:center;justify-content:center;overflow:hidden;">
  <div style="position:absolute;top:-90px;left:-110px;width:320px;height:320px;border-radius:50%;background:var(--teal-tint2);"></div>
  <div style="position:absolute;bottom:-120px;right:-100px;width:360px;height:360px;border-radius:50%;background:var(--magenta-tint2);"></div>
  <div style="position:relative;display:flex;flex-direction:column;align-items:center;gap:26px;padding:0 40px;">
    {logo_full(260)}
    <div class="disp" style="font-size:26px;font-weight:800;color:var(--ink);text-align:center;line-height:1.25;">#VaksinKeluargaJadiMudah</div>
    <div style="font-size:14px;color:var(--ink-3);text-align:center;line-height:1.6;max-width:270px;">Booking, rekam medis, dan konsultasi vaksinasi keluarga dalam satu aplikasi.</div>
  </div>
  <div style="position:absolute;bottom:34px;display:flex;gap:7px;">
    <div style="width:7px;height:7px;border-radius:50%;background:var(--teal);"></div>
    <div style="width:7px;height:7px;border-radius:50%;background:var(--teal);opacity:.4;"></div>
    <div style="width:7px;height:7px;border-radius:50%;background:var(--magenta);opacity:.4;"></div>
  </div>
</div>
</div>
'''

# ---------------------------------------------------------------- ONBOARDING
def need_card(ic, title, sub, key, selected=False):
    cls = "need-card tap choice" + (" active" if selected else "")
    return f'''<div class="{cls}" data-need="{key}" onclick="pickChoice(this,'need-card')">
      <div class="chk">{icon("check-c",16,"currentColor")}</div>
      <div class="ic-circle">{icon(ic,22,"currentColor")}</div>
      <div><div style="font-weight:700;font-size:14px;">{title}</div><div style="font-size:11.5px;color:var(--ink-3);margin-top:2px;line-height:1.4;">{sub}</div></div>
    </div>'''

illustration = f'''
<div style="height:230px;border-radius:24px;background:linear-gradient(160deg,var(--teal-tint) 0%,var(--magenta-tint) 100%);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;flex-shrink:0;">
  <div style="position:absolute;top:18px;left:18px;width:34px;height:34px;border-radius:50%;background:#fff;opacity:.6;"></div>
  <div style="position:absolute;bottom:22px;right:26px;width:20px;height:20px;border-radius:50%;background:#fff;opacity:.5;"></div>
  <svg width="180" height="150" viewBox="0 0 180 150" fill="none">
    <circle cx="60" cy="46" r="22" fill="#56C3C7"/><circle cx="120" cy="46" r="22" fill="#D11972" opacity="0.85"/><circle cx="90" cy="60" r="17" fill="#2E9BA0"/>
    <path d="M20 140c8-34 30-52 55-52s45 16 52 52" stroke="#56C3C7" stroke-width="6" fill="none" stroke-linecap="round"/>
    <path d="M95 140c6-24 20-36 40-36s32 12 38 36" stroke="#D11972" stroke-width="6" fill="none" stroke-linecap="round" opacity="0.85"/>
  </svg>
</div>'''

onboarding = f'''
<div id="screen-onboarding" class="screen">
<div class="frame">
  <div class="col" style="padding:22px 20px 0;">
    <div class="row" style="justify-content:flex-end;"><span class="tap" style="font-size:13px;font-weight:700;color:var(--ink-3);" onclick="showScreen('login')">Lewati</span></div>
    <div style="height:14px;"></div>
    {illustration}
    <div style="height:22px;"></div>
    <div class="disp" style="font-size:21px;font-weight:800;color:var(--ink);">Pilih kebutuhan vaksinasi Anda</div>
    <div style="font-size:13px;color:var(--ink-3);margin-top:6px;line-height:1.55;">VaksinKu menyesuaikan rekomendasi &amp; paket berdasarkan kebutuhan keluarga Anda.</div>
    <div style="height:18px;"></div>
    <div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;">
      {need_card("cake","Vaksin Anak","Usia 0–5 tahun, jadwal IDAI","anak",True)}
      {need_card("family","Anak Sekolah","Usia 6–18 tahun","sekolah")}
      {need_card("user","Vaksin Dewasa","Rekomendasi PAPDI","dewasa")}
      {need_card("heart","Pranikah","HPV, MMR, tetanus","pranikah")}
      {need_card("heart","Lansia","50 tahun ke atas","lansia")}
      {need_card("plane","Internasional","Haji, umrah, studi (ICV)","internasional")}
    </div>
  </div>
  <div class="grow"></div>
  <div style="padding:18px 20px 26px;display:flex;flex-direction:column;gap:12px;">
    <div class="row" style="justify-content:center;gap:7px;">
      <div style="width:7px;height:7px;border-radius:50%;background:var(--line);"></div>
      <div style="width:18px;height:7px;border-radius:4px;background:var(--magenta);"></div>
      <div style="width:7px;height:7px;border-radius:50%;background:var(--line);"></div>
    </div>
    <button class="btn btn-primary tap" onclick="showScreen('login')">Lanjutkan {icon("chevron",16,"#fff")}</button>
  </div>
</div>
</div>
'''

# ---------------------------------------------------------------- LOGIN
login = f'''
<div id="screen-login" class="screen">
<div class="frame">
  <div class="col grow" style="padding:0 30px;align-items:center;justify-content:center;">
    <div style="display:flex;flex-direction:column;align-items:center;gap:10px;margin-bottom:34px;">{logo_mark(46)}
      <div style="font-size:11.5px;font-weight:700;color:var(--teal-dark);letter-spacing:.02em;text-align:center;">{BRAND["tagline"]}</div>
    </div>
    <div class="disp" style="font-size:21px;font-weight:800;text-align:center;">Masuk untuk mulai vaksinasi</div>
    <div style="font-size:13px;color:var(--ink-3);text-align:center;margin-top:8px;line-height:1.6;">Kelola jadwal, rekam medis, dan keluarga Anda dalam satu akun VaksinKu.</div>
    <div style="height:34px;"></div>
    <div class="col" style="width:100%;gap:12px;">
      <button class="btn tap" style="background:#fff;border:1.4px solid var(--line);color:var(--ink);" onclick="showScreen('home')">{GOOGLE_G} Lanjutkan dengan Google</button>
      <button class="btn btn-primary tap" onclick="showScreen('home')">{icon("phone",17,"#fff")} Lanjutkan dengan Nomor HP</button>
    </div>
    <div style="font-size:11.5px;color:var(--ink-4);text-align:center;margin-top:22px;line-height:1.6;">Dengan melanjutkan, Anda menyetujui Syarat &amp; Ketentuan serta Kebijakan Privasi VaksinKu.</div>
  </div>
  <div class="col" style="align-items:center;gap:6px;padding-bottom:26px;">
    <div style="font-size:12.5px;color:var(--ink-3);">Butuh bantuan? WhatsApp <span style="color:var(--magenta-dark);font-weight:700;">{BRAND["call_center"]}</span></div>
    <div style="font-size:11px;color:var(--ink-4);">Versi 1.0.0 (Prototipe)</div>
  </div>
</div>
</div>
'''

# ---------------------------------------------------------------- HOME
home_header = f'''
<div style="background:linear-gradient(120deg,var(--teal-tint) 0%,var(--magenta-tint) 100%);border-radius:0 0 28px 28px;padding:20px 20px 26px;flex-shrink:0;">
  <div class="row" style="align-items:center;gap:10px;">
    {logo_mark(22)}<div class="grow"></div>
    <div class="chip chip-amber tap" onclick="showScreen('profile')">{icon("coin",14,"#9C6B0E")} 128 Poin</div>
    <div class="iconbtn tap" onclick="toast('Belum ada notifikasi baru')">{icon("bell",18,"var(--ink-2)")}</div>
    <div class="iconbtn tap" onclick="showScreen('rekammedis')">{icon("doc",17,"var(--ink-2)")}</div>
  </div>
  <div style="height:18px;"></div>
  <div class="disp" style="font-size:19px;font-weight:800;">Halo, Keluarga Perdana</div>
  <div style="font-size:12.5px;color:var(--ink-2);margin-top:4px;">Yuk pastikan imunisasi keluarga selalu tepat waktu.</div>
</div>'''

booking_card = f'''
<div class="card">
  <div class="row" style="align-items:center;gap:8px;">
    <span class="chip chip-mag">Booking Aktif</span><div class="grow"></div><span style="font-size:11.5px;color:var(--ink-4);">#VK-88213</span>
  </div>
  <div style="height:12px;"></div>
  <div class="row" style="gap:12px;align-items:center;">
    <div style="width:44px;height:44px;border-radius:50%;background:var(--teal-tint);display:flex;align-items:center;justify-content:center;font-weight:800;color:var(--teal-dark);font-family:'Baloo 2';">AP</div>
    <div class="col" style="gap:2px;"><div style="font-weight:700;font-size:14.5px;">Vaksin Influenza — Nadia</div><div style="font-size:12px;color:var(--ink-3);">dr. Dwi Fachri JH, Sp.A</div></div>
  </div>
  <div style="height:14px;"></div>
  <div class="row" style="gap:16px;">
    <div class="row" style="gap:6px;align-items:center;">{icon("calendar",15,"var(--teal-dark)")}<span style="font-size:12px;color:var(--ink-2);">Sab, 12 Sep • 10.00</span></div>
    <div class="row" style="gap:6px;align-items:center;">{icon("house",15,"var(--teal-dark)")}<span style="font-size:12px;color:var(--ink-2);">Home Care</span></div>
  </div>
  <div class="divider" style="margin:14px 0;"></div>
  <div class="row" style="gap:10px;">
    <button class="btn btn-outline tap" style="flex:1;padding:11px;font-size:13px;" onclick="showScreen('booking')">Lihat Detail</button>
    <button class="tap" style="flex:1;background:transparent;border:none;color:var(--magenta-dark);font-weight:700;font-size:13px;font-family:'Baloo 2';" onclick="showScreen('booking')">Reschedule</button>
  </div>
</div>'''

reminder_card = f'''
<div class="card row" style="gap:14px;align-items:flex-start;">
  <div style="width:42px;height:42px;border-radius:14px;background:var(--magenta-tint);display:flex;align-items:center;justify-content:center;flex-shrink:0;">{icon("calendar",20,"var(--magenta-dark)")}</div>
  <div class="col" style="gap:4px;"><div style="font-weight:700;font-size:14px;">Reminder jadwal berikutnya</div><div style="font-size:12.5px;color:var(--ink-2);">Varicella (dosis ke-2) — 3 minggu lagi</div><div style="font-size:11px;color:var(--ink-4);margin-top:2px;">Reminder otomatis H-7, H-1, dan H-1 jam.</div></div>
</div>'''

growth_card = f'''
<div class="card tap" onclick="showScreen('rekammedis')">
  <div class="row" style="align-items:center;"><div style="font-weight:700;font-size:14.5px;">Tumbuh Kembang &amp; Kelengkapan Vaksinasi</div><div class="grow"></div>{icon("chevron",16,"var(--ink-4)")}</div>
  <div style="height:12px;"></div>
  <div class="row" style="gap:8px;">
    <div class="chip chip-teal" style="flex:1;justify-content:center;">Berat 8.5kg · Normal</div>
    <div class="chip chip-teal" style="flex:1;justify-content:center;">Tinggi 68cm · Normal</div>
  </div>
</div>'''

seasonal_banner = f'''
<div class="tap" style="border-radius:20px;padding:20px;background:linear-gradient(135deg,var(--teal-dark) 0%,var(--magenta-dark) 130%);color:#fff;position:relative;overflow:hidden;" onclick="showScreen('paket')">
  <div style="position:absolute;right:-30px;top:-30px;width:130px;height:130px;border-radius:50%;background:rgba(255,255,255,.08);"></div>
  <div style="position:absolute;right:20px;bottom:-40px;width:90px;height:90px;border-radius:50%;background:rgba(255,255,255,.08);"></div>
  <div style="position:relative;">
    <div class="row" style="align-items:center;gap:8px;">
      <span style="background:#fff;color:var(--magenta-dark);border-radius:999px;padding:3px 10px;font-size:10px;font-weight:800;letter-spacing:.03em;">PROMO</span>
      <span style="font-size:11px;opacity:.85;">Haji &amp; Umrah</span>
    </div>
    <div class="disp" style="font-size:17px;font-weight:800;margin-top:8px;">Paket Polio + Meningitis</div>
    <div style="font-size:12.5px;opacity:.9;margin-top:2px;line-height:1.5;">Wajib bagi jamaah haji &amp; umrah. Sudah termasuk e-ICV.</div>
    <div class="row" style="align-items:baseline;gap:10px;margin-top:12px;">
      <span class="disp" style="font-size:22px;font-weight:800;">Rp620.000</span>
      <span style="font-size:12.5px;opacity:.7;text-decoration:line-through;">Rp650.000</span>
    </div>
  </div>
</div>'''

def info_col(ic, label, onclick):
    return f'''<div class="col tap" style="align-items:center;gap:8px;flex:1;" onclick="{onclick}">
      <div style="width:46px;height:46px;border-radius:14px;background:var(--teal-tint);display:flex;align-items:center;justify-content:center;">{icon(ic,21,"var(--teal-dark)")}</div>
      <div style="font-size:11.5px;font-weight:700;text-align:center;line-height:1.3;">{label}</div>
    </div>'''

info_row = f'''<div class="card row" style="gap:8px;">
  {info_col("tag","Daftar Harga","showScreen(&#39;harga&#39;)")}
  {info_col("calendar","Jadwal Vaksin","showScreen(&#39;jadwal&#39;)")}
  {info_col("globe","Vaksin Internasional","showScreen(&#39;paket&#39;)")}
</div>'''

def layanan_col(ic, label, sub):
    return f'''<div class="col tap" style="align-items:center;gap:8px;flex:1;" onclick="showScreen('booking')">
      <div style="width:46px;height:46px;border-radius:14px;background:var(--magenta-tint);display:flex;align-items:center;justify-content:center;">{icon(ic,21,"var(--magenta-dark)")}</div>
      <div style="font-size:11.5px;font-weight:700;text-align:center;line-height:1.3;">{label}</div>
      <div style="font-size:10px;color:var(--ink-4);text-align:center;line-height:1.3;">{sub}</div>
    </div>'''

layanan_row = f'''<div class="card">
  <div class="row" style="align-items:center;margin-bottom:14px;">
    <div style="font-weight:700;font-size:14.5px;">Pilih cara vaksinasi</div>
    <div class="grow"></div>
    <span class="chip chip-teal">3 layanan</span>
  </div>
  <div class="row" style="gap:8px;">
    {layanan_col("house","Home Care","Ke rumah")}
    {layanan_col("pin","On Site Klinik","Di klinik")}
    {layanan_col("building","On Site Corporate","Di kantor")}
  </div>
  <div class="divider" style="margin:14px 0 12px;"></div>
  <div class="row" style="gap:6px;flex-wrap:wrap;">
    <span style="font-size:11px;color:var(--ink-3);font-weight:600;">Sudah termasuk:</span>
    {"".join(f'<span class="chip chip-teal" style="padding:4px 9px;font-size:10.5px;">{t}</span>' for t in TERMASUK)}
  </div>
</div>'''

klinik_card = f'''<div class="card row tap" style="align-items:center;gap:14px;" onclick="showScreen('tentang')">
  <div style="width:42px;height:42px;border-radius:12px;background:var(--teal-tint);display:flex;align-items:center;justify-content:center;flex-shrink:0;">{icon("pin",20,"var(--teal-dark)")}</div>
  <div class="col grow" style="gap:2px;"><div style="font-weight:700;font-size:13.5px;">3 Klinik di Tanjungpinang</div>
  <div style="font-size:11.5px;color:var(--ink-3);">Alrasha HCC · Klinik Utama Alrasha Ibumas · Ibumas</div></div>
  {icon("chevron",16,"var(--ink-4)")}
</div>'''

corp_teaser = f'''
<div class="card row tap" style="align-items:center;gap:14px;background:var(--teal-tint);border-color:transparent;" onclick="showScreen('korporat')">
  <div style="width:42px;height:42px;border-radius:12px;background:#fff;display:flex;align-items:center;justify-content:center;flex-shrink:0;">{icon("building",20,"var(--teal-dark)")}</div>
  <div class="col grow" style="gap:2px;"><div style="font-weight:700;font-size:13.5px;">Mitra Institusi?</div><div style="font-size:11.5px;color:var(--ink-2);">Booking massal vaksinasi sekolah &amp; kantor</div></div>
  <div class="chip chip-mag">Pelajari</div>
</div>'''

home = f'''
<div id="screen-home" class="screen">
<div class="frame">
  {home_header}
  <div class="col" style="padding:18px 20px 12px;gap:14px;">
    {booking_card}{reminder_card}{info_row}{layanan_row}{seasonal_banner}{growth_card}{klinik_card}{corp_teaser}
  </div>
  <div class="grow"></div>
  {navbar("home")}
</div>
</div>
'''

# ---------------------------------------------------------------- BOOKING
BACK_ICON = '<span style="display:inline-flex;transform:scaleX(-1);">' + icon("chevron",20,"#fff",2.2) + '</span>'
booking_hdr = f'''<div class="hdr-bar"><span class="tap" onclick="showScreen('home')">{BACK_ICON}</span><div class="disp">Booking Vaksinasi</div></div>'''

def service_chip(ic, label, key, selected=False):
    cls = "svc-card tap choice" + (" active" if selected else "")
    return f'''<div class="{cls}" data-svc="{key}" onclick="pickChoice(this,'svc-card')">{icon(ic,20,"currentColor")}<span>{label}</span></div>'''

section1 = f'''<div class="section" style="padding-bottom:6px;">
  <span class="label">Pilih Layanan<span class="req">*</span></span>
  <div class="row" style="gap:10px;">{service_chip("doc","Vaksinasi","vaksinasi",True)}{service_chip("chat","Konsultasi","konsultasi")}{service_chip("chart","Cek Tumbuh Kembang","tumbuh")}</div>
</div>'''

section2 = f'''<div class="section" style="padding-top:14px;padding-bottom:6px;">
  <span class="label">Data Pendaftar<span class="req">*</span></span>
  <span class="hint">Data pendaftar akan digunakan sebagai penerima invoice.</span>
  <input class="input" value="Angga Perdana" style="margin-bottom:12px;">
  <div class="row" style="gap:10px;margin-bottom:12px;">
    <div class="gender-opt tap choice" onclick="pickChoice(this,'gender-opt')">Perempuan</div>
    <div class="gender-opt tap choice active" onclick="pickChoice(this,'gender-opt')">Laki-laki</div>
  </div>
  <input class="input" placeholder="Nomor HP aktif">
</div>'''

section3 = f'''<div class="section" style="padding-top:14px;padding-bottom:6px;">
  <span class="label">Layanan Vaksinasi<span class="req">*</span></span>
  <div class="row" style="gap:8px;margin-bottom:10px;">
    <div class="loc-opt tap choice active" onclick="pickChoice(this,'loc-opt')">{icon("house",20,"currentColor")}<span>Home Care</span></div>
    <div class="loc-opt tap choice" onclick="pickChoice(this,'loc-opt')">{icon("pin",20,"currentColor")}<span>On Site Klinik</span></div>
    <div class="loc-opt tap choice" onclick="pickChoice(this,'loc-opt')">{icon("building",20,"currentColor")}<span>On Site Corporate</span></div>
  </div>
  <div class="row" style="align-items:center;gap:10px;background:var(--teal-tint);border-radius:14px;padding:12px 14px;">
    {icon("pin",16,"var(--teal-dark)")}<span class="grow" style="font-size:12.5px;color:var(--ink-2);">Jl. Hang Lekir, Batu 10, Tanjungpinang</span>
    <span class="tap" style="font-size:12px;font-weight:700;color:var(--magenta-dark);" onclick="toast('Ubah alamat akan tersedia di versi lengkap')">Ubah</span>
  </div>
</div>'''

section_dokter = f'''<div class="section" style="padding-top:14px;padding-bottom:6px;">
  <span class="label">Pilih Dokter<span class="req">*</span></span>
  <span class="hint">Harga vaksin menyesuaikan pilihan dokter. Semua vaksinator bersertifikat.</span>
  <div class="row" style="gap:10px;">
    <div class="dok-opt tap choice active" onclick="pickDokter(this,400000)">
      <div class="row" style="align-items:center;gap:8px;"><span class="dok-dot"></span><span style="font-weight:700;font-size:13px;">Dokter Umum</span></div>
      <div style="font-size:11.5px;color:var(--ink-3);margin-top:6px;">Rp400.000</div>
    </div>
    <div class="dok-opt tap choice" onclick="pickDokter(this,450000)">
      <div class="row" style="align-items:center;gap:8px;"><span class="dok-dot"></span><span style="font-weight:700;font-size:13px;">Dokter Spesialis</span></div>
      <div style="font-size:11.5px;color:var(--ink-3);margin-top:6px;">Rp450.000</div>
    </div>
  </div>
</div>'''

section4 = f'''<div class="section" style="padding-top:14px;padding-bottom:6px;">
  <div class="row" style="align-items:center;gap:8px;margin-bottom:2px;"><span class="label" style="margin-bottom:0;">Data Pasien<span class="req">*</span></span><span class="chip chip-teal">Booking untuk keluarga</span></div>
  <span class="hint">Daftar pasien adalah orang yang akan divaksin. Pastikan data sudah benar.</span>
  <div class="col" style="gap:10px;">
    <div class="row tap" style="align-items:center;gap:12px;border:1.4px solid var(--line);border-radius:14px;padding:12px 14px;" onclick="toast('Detail pasien akan tersedia di versi lengkap')">
      <div style="width:34px;height:34px;border-radius:50%;background:var(--teal-tint);display:flex;align-items:center;justify-content:center;font-weight:800;color:var(--teal-dark);font-size:12px;font-family:'Baloo 2';">N</div>
      <div class="col grow" style="gap:1px;"><div style="font-weight:700;font-size:13.5px;">Nadia Perdana</div><div style="font-size:11.5px;color:var(--ink-3);">5 tahun · Influenza (Vaxigrip Tetra)</div></div>
      {icon("chevron",16,"var(--ink-4)")}
    </div>
    <div class="tap" style="border:1.4px dashed var(--teal);border-radius:14px;padding:12px;display:flex;align-items:center;justify-content:center;gap:8px;color:var(--teal-dark);font-weight:700;font-size:13px;" onclick="toast('Tambah pasien akan tersedia di versi lengkap')">{icon("plus",16,"var(--teal-dark)")} Tambah pasien</div>
  </div>
</div>'''

def slot(label, state):
    if state == "full":
        return f'<div class="slot-opt full">{label}</div>'
    cls = "slot-opt tap" + (" active" if state == "selected" else "")
    return f'<div class="{cls}" onclick="pickChoice(this,\'slot-opt\')">{label}</div>'

def date_chip(d, w, active=False):
    cls = "date-opt tap" + (" active" if active else "")
    return (f'<div class="{cls}" onclick="pickChoice(this,\'date-opt\')">'
            f'<div style="font-size:10px;opacity:.8;">{w}</div><div class="disp" style="font-weight:800;font-size:14px;">{d}</div></div>')

date_strip = "".join(date_chip(d, w, active=(d=="12")) for d, w in [("10","Kam"),("11","Jum"),("12","Sab"),("13","Min"),("14","Sen")])

section5 = f'''<div class="section" style="padding-top:14px;padding-bottom:6px;">
  <span class="label">Jadwal Vaksinasi<span class="req">*</span></span>
  <div class="row choice-group" style="gap:8px;margin-bottom:12px;">{date_strip}</div>
  <div class="choice-group">
    <div class="row" style="gap:8px;margin-bottom:8px;">{slot("09.00","available")}{slot("10.00","selected")}{slot("11.00","full")}</div>
    <div class="row" style="gap:8px;">{slot("13.00","available")}{slot("14.00","available")}{slot("15.00","full")}</div>
  </div>
</div>'''

summary = f'''<div class="section" style="padding-top:14px;">
  <div class="card" style="border:1.4px solid var(--teal);background:var(--teal-tint);">
    <div class="row" style="align-items:center;gap:7px;margin-bottom:12px;">{icon("check-c",16,"var(--teal-dark)")}<span style="font-size:12px;font-weight:700;color:var(--teal-dark);">Price list terbuka, tanpa biaya tersembunyi</span></div>
    <div class="row" style="justify-content:space-between;margin-bottom:8px;"><span style="font-size:13px;color:var(--ink-2);">Influenza 4 strain — Vaxigrip Tetra</span><span class="est-line" style="font-size:13px;color:var(--ink);">Rp400.000</span></div>
    <div class="row" style="justify-content:space-between;margin-bottom:8px;"><span style="font-size:13px;color:var(--ink-2);">Jasa dokter &amp; tindakan</span><span style="font-size:13px;color:var(--teal-dark);font-weight:700;">Termasuk</span></div>
    <div class="row" style="justify-content:space-between;margin-bottom:8px;"><span style="font-size:13px;color:var(--ink-2);">Bahan medis habis pakai</span><span style="font-size:13px;color:var(--teal-dark);font-weight:700;">Termasuk</span></div>
    <div class="divider" style="margin:10px 0;"></div>
    <div class="row" style="justify-content:space-between;"><span class="disp" style="font-weight:800;font-size:14px;">Total Estimasi</span><span class="disp est-total" style="font-weight:800;font-size:15px;color:var(--magenta-dark);">Rp400.000</span></div>
    <div style="font-size:11px;color:var(--ink-3);margin-top:8px;line-height:1.5;">Harga sesuai price list VaksinKu. Biaya kunjungan Home Care &amp; On Site dikonfirmasi saat reservasi.</div>
  </div>
</div>'''

payment = f'''<div class="section" style="padding-top:2px;">
  <span class="label">Metode Pembayaran<span class="req">*</span></span>
  <div class="row" style="gap:10px;">
    <div class="pay-opt tap choice" onclick="pickChoice(this,'pay-opt')">Transfer Bank</div>
    <div class="pay-opt tap choice active" onclick="pickChoice(this,'pay-opt')">QRIS</div>
    <div class="pay-opt tap choice" onclick="pickChoice(this,'pay-opt')">E-Wallet</div>
  </div>
</div>'''

booking_footer = f'''<div style="position:sticky;bottom:0;background:#fff;border-top:1px solid var(--line);padding:14px 20px 20px;display:flex;align-items:center;gap:14px;">
  <div class="col" style="gap:1px;"><div style="font-size:10.5px;color:var(--ink-4);">Total estimasi</div><div class="disp est-total" style="font-weight:800;font-size:16px;color:var(--magenta-dark);">Rp400.000</div></div>
  <button class="btn btn-primary grow tap" onclick="confirmBooking()">Konfirmasi Booking</button>
</div>'''

booking = f'''
<div id="screen-booking" class="screen">
<div class="frame">
  {booking_hdr}{section1}{section2}{section3}{section_dokter}{section4}{section5}{summary}{payment}
  <div style="height:8px;"></div>
  {booking_footer}
</div>
</div>
'''

# ---------------------------------------------------------------- REKAM MEDIS
rm_hdr = f'''<div class="hdr-bar"><span class="tap" onclick="showScreen('home')">{BACK_ICON}</span><div class="disp">Rekam Medis</div></div>'''

patient_tabs = f'''<div class="row" style="gap:8px;padding:16px 20px 4px;">
  <div class="patient-tab tap choice active" onclick="pickChoice(this,'patient-tab')">Nadia (5 th)</div>
  <div class="patient-tab tap choice" onclick="pickChoice(this,'patient-tab')">Angga Perdana</div>
  <div class="tap" style="padding:8px 12px;border-radius:999px;border:1.4px dashed var(--teal);color:var(--teal-dark);font-size:12.5px;font-weight:700;" onclick="toast('Tambah pasien akan tersedia di versi lengkap')">{icon("plus",13,"var(--teal-dark)")}</div>
</div>'''

qr = '<svg width="52" height="52" viewBox="0 0 10 10"><rect width="10" height="10" fill="#fff"/>' + "".join(
    f'<rect x="{x}" y="{y}" width="1" height="1" fill="#262626"/>'
    for x, y in [(0,0),(1,0),(2,0),(0,1),(2,1),(0,2),(1,2),(2,2),(4,0),(5,1),(4,3),(7,0),(8,0),(9,0),(7,1),(9,1),(7,2),(8,2),(9,2),(4,5),(5,6),(4,7),(0,7),(1,7),(2,7),(0,8),(2,8),(0,9),(1,9),(2,9),(6,7),(7,7),(8,7),(6,9),(8,9),(7,8),(5,4),(6,5),(8,5)]
) + '</svg>'

vax_card = f'''<div class="card" style="padding:0;overflow:hidden;">
  <div style="background:linear-gradient(120deg,var(--teal) 0%,var(--magenta) 130%);height:8px;"></div>
  <div style="padding:18px;">
    <div class="row" style="align-items:center;"><div class="disp" style="font-weight:800;font-size:14px;">Kartu Vaksinasi Digital</div><div class="grow"></div><span class="chip chip-teal">Aktif</span></div>
    <div class="row" style="align-items:center;gap:14px;margin-top:14px;">
      <div class="col grow" style="gap:3px;"><div style="font-weight:800;font-size:15px;">Nadia Perdana</div><div style="font-size:12px;color:var(--ink-3);">Lahir 12 Mei 2021 · Perempuan</div><div style="font-size:11.5px;color:var(--ink-4);margin-top:4px;">No. Kartu: VK-2026-004821</div></div>
      <div style="border:1px solid var(--line);border-radius:10px;padding:4px;">{qr}</div>
    </div>
    <div style="font-size:11px;color:var(--ink-3);margin-top:12px;line-height:1.5;">Berlaku untuk syarat sekolah &amp; keperluan imigrasi (Umroh/Haji).</div>
    <div class="row" style="gap:10px;margin-top:14px;">
      <button class="btn btn-outline tap" style="flex:1;padding:11px;font-size:13px;" onclick="toast('PDF kartu vaksinasi sedang disiapkan...')">{icon("download",15,"var(--teal-dark)")} Unduh PDF</button>
      <button class="btn btn-outline tap" style="flex:1;padding:11px;font-size:13px;" onclick="toast('Fitur bagikan akan tersedia di versi lengkap')">{icon("share",15,"var(--teal-dark)")} Bagikan</button>
    </div>
  </div>
</div>'''

def vax_chip(label, state):
    m = {"done": ("var(--green-tint)","var(--green)","check-c"), "soon": ("var(--amber-tint)","#9C6B0E","clock"), "todo": ("#F1F1F0","var(--ink-3)","circle-o")}
    bg,color,ic = m[state]
    return f'<div style="background:{bg};border-radius:12px;padding:8px 10px;display:flex;align-items:center;gap:6px;"><span style="color:{color};">{icon(ic,14,color)}</span><span style="font-size:11.5px;font-weight:700;color:{color};">{label}</span></div>'

idl_card = f'''<div class="card">
  <div class="row" style="align-items:center;"><div style="font-weight:700;font-size:14.5px;">Status Kelengkapan Imunisasi (IDL)</div></div>
  <div class="row" style="align-items:center;gap:10px;margin-top:12px;">
    <div style="flex:1;height:8px;border-radius:6px;background:#F1F1F0;overflow:hidden;"><div style="width:67%;height:100%;background:var(--teal);"></div></div>
    <span style="font-size:12.5px;font-weight:800;color:var(--teal-dark);">67%</span>
  </div>
  <div style="height:12px;"></div>
  <div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;">
    {vax_chip("HB0","done")}{vax_chip("BCG","done")}{vax_chip("Polio 1","done")}{vax_chip("DPT-HB-Hib 1","soon")}{vax_chip("Campak","todo")}{vax_chip("Polio 2","todo")}
  </div>
</div>'''

chart_svg = '''<svg width="100%" height="150" viewBox="0 0 320 150" preserveAspectRatio="none">
  <polygon points="0,150 0,90 320,40 320,150" fill="#E9F9FA"/>
  <polyline points="0,120 60,105 120,88 180,70 240,55 320,42" fill="none" stroke="#BFE9EA" stroke-width="2"/>
  <polyline points="0,138 60,128 120,116 180,102 240,90 320,78" fill="none" stroke="#BFE9EA" stroke-width="2"/>
  <polyline points="0,108 60,86 120,66 180,50 240,36 320,26" fill="none" stroke="#F6D3E4" stroke-width="2"/>
  <polyline points="0,130 60,112 120,94 180,80 240,64 320,52" fill="none" stroke="#56C3C7" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="0" cy="130" r="4" fill="#2E9BA0"/><circle cx="60" cy="112" r="4" fill="#2E9BA0"/>
  <circle cx="120" cy="94" r="4" fill="#2E9BA0"/><circle cx="180" cy="80" r="4" fill="#2E9BA0"/>
  <circle cx="240" cy="64" r="4" fill="#2E9BA0"/><circle cx="320" cy="52" r="5" fill="#D11972"/>
</svg>'''

growth_card = f'''<div class="card">
  <div class="row" style="align-items:center;"><div style="font-weight:700;font-size:14.5px;">Grafik Tumbuh Kembang</div><div class="grow"></div>
    <span class="row" style="gap:5px;align-items:center;font-size:11px;color:var(--ink-3);"><span style="width:8px;height:8px;border-radius:50%;background:var(--teal-dark);display:inline-block;"></span>Berat badan</span>
  </div>
  <div style="margin-top:10px;">{chart_svg}</div>
  <div class="row" style="gap:8px;margin-top:14px;">
    <div class="chip chip-teal" style="flex:1;justify-content:center;">Berat 12.4kg</div><div class="chip chip-teal" style="flex:1;justify-content:center;">Tinggi 92cm</div><div class="chip chip-teal" style="flex:1;justify-content:center;">Kepala 47cm</div>
  </div>
  <button class="btn btn-outline tap" style="width:100%;margin-top:14px;padding:12px;font-size:13px;" onclick="toast('Form update pertumbuhan akan tersedia di versi lengkap')">Update Data Pertumbuhan</button>
</div>'''

def history_row(date, title, sub):
    return f'''<div class="row tap" style="align-items:center;gap:12px;padding:12px 0;" onclick="toast('Detail riwayat akan tersedia di versi lengkap')">
      <div style="width:40px;height:40px;border-radius:12px;background:var(--magenta-tint);display:flex;align-items:center;justify-content:center;flex-shrink:0;">{icon("doc",18,"var(--magenta-dark)")}</div>
      <div class="col grow" style="gap:1px;"><div style="font-weight:700;font-size:13px;">{title}</div><div style="font-size:11.5px;color:var(--ink-3);">{sub}</div></div>
      <div class="col" style="align-items:flex-end;gap:2px;"><span style="font-size:11px;color:var(--ink-4);">{date}</span>{icon("chevron",14,"var(--ink-4)")}</div>
    </div>'''

history_card = f'''<div class="card">
  <div style="font-weight:700;font-size:14.5px;margin-bottom:4px;">Riwayat Vaksinasi</div><div class="divider"></div>
  {history_row("2 Sep 2026","Varicella 1 (Varivax)","dr. Dwi Fachri JH, Sp.A · Home Care")}<div class="divider"></div>
  {history_row("14 Jul 2026","Tifoid (Typhim Vi)","dr. Dwi Fachri JH, Sp.A · Klinik Utama Alrasha Ibumas")}<div class="divider"></div>
  {history_row("2 Mar 2026","Combo DPT 3 (Pentabio)","Tim Dokter Umum · Klinik Alrasha HCC")}
</div>'''

rekammedis = f'''
<div id="screen-rekammedis" class="screen">
<div class="frame">
  {rm_hdr}{patient_tabs}
  <div class="col" style="padding:10px 20px 12px;gap:14px;">{vax_card}{idl_card}{growth_card}{history_card}</div>
  <div class="grow"></div>
  {navbar("doc")}
</div>
</div>
'''

# ---------------------------------------------------------------- CHAT
chat_hdr = f'''<div style="padding:20px 20px 14px;flex-shrink:0;"><div class="disp" style="font-size:20px;font-weight:800;">Chat</div><div style="font-size:12.5px;color:var(--ink-3);margin-top:2px;">Konsultasi dokter &amp; bantuan CS</div></div>'''

chat_info = f'''<div style="margin:0 20px 14px;background:var(--teal-tint);border-radius:14px;padding:12px 14px;display:flex;align-items:center;gap:10px;">
  {icon("clock",16,"var(--teal-dark)")}<span style="font-size:11.5px;color:var(--teal-dark);font-weight:600;line-height:1.4;">Dokter online: Senin–Jumat 09.00–17.00 · Sabtu 09.00–12.00</span>
</div>'''

def chat_row(initials, bg, name, preview, time, badge=None, unread=False, icon_name=None):
    avatar = f'<div style="width:46px;height:46px;border-radius:50%;background:{bg};display:flex;align-items:center;justify-content:center;flex-shrink:0;">'
    avatar += (icon(icon_name, 20, "#fff") if icon_name else f'<span class="disp" style="color:#fff;font-weight:800;font-size:14px;">{initials}</span>') + '</div>'
    badge_html = f'<span class="chip chip-mag" style="padding:3px 8px;font-size:9.5px;">{badge}</span>' if badge else ""
    dot = '<div style="width:9px;height:9px;border-radius:50%;background:var(--magenta);margin-top:6px;"></div>' if unread else '<div style="width:9px;height:9px;"></div>'
    return f'''<div class="row tap" style="align-items:center;gap:12px;padding:14px 20px;border-bottom:1px solid var(--line);" onclick="toast('Percakapan lengkap akan tersedia di versi lengkap')">
      {avatar}
      <div class="col grow" style="gap:3px;min-width:0;"><div class="row" style="align-items:center;gap:8px;"><span style="font-weight:700;font-size:13.5px;">{name}</span>{badge_html}</div>
      <div style="font-size:12px;color:var(--ink-3);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{preview}</div></div>
      <div class="col" style="align-items:flex-end;gap:6px;"><span style="font-size:10.5px;color:var(--ink-4);">{time}</span>{dot}</div>
    </div>'''

chat_rows = (chat_row("DF", "var(--teal)", DOKTER[0][0], "Baik, jadwal vaksin Influenza Nadia kita lanjutkan minggu depan ya Bu.", "09.42", unread=True)
    + chat_row(None, "var(--magenta)", f"CS VaksinKu · {BRAND['call_center']}", "Halo! Ada yang bisa dibantu terkait reservasi Anda?", "Kemarin", badge="24 JAM", icon_name="whatsapp")
    + chat_row("AP", "#8FB8BC", DOKTER[1][0], "Untuk vaksin meningitis umrah, idealnya 4 minggu sebelum berangkat.", "2 hari lalu")
    + chat_row("LA", "#C7CBCF", DOKTER[2][0], "Terima kasih atas kunjungannya!", "5 hari lalu"))

chat = f'''
<div id="screen-chat" class="screen">
<div class="frame">
  {chat_hdr}{chat_info}
  <div class="col">{chat_rows}</div>
  <div class="grow"></div>
  {navbar("chat")}
</div>
</div>
'''

# ---------------------------------------------------------------- PROFILE
profile_header = f'''<div style="background:linear-gradient(120deg,var(--teal-tint) 0%,var(--magenta-tint) 100%);border-radius:0 0 28px 28px;padding:24px 20px 22px;flex-shrink:0;">
  <div class="row" style="align-items:center;gap:14px;">
    <div style="width:60px;height:60px;border-radius:50%;background:linear-gradient(135deg,var(--teal),var(--magenta));display:flex;align-items:center;justify-content:center;">
      <div style="width:54px;height:54px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;"><span class="disp" style="font-weight:800;font-size:18px;color:var(--ink-2);">AP</span></div>
    </div>
    <div class="col" style="gap:3px;"><div class="disp" style="font-weight:800;font-size:17px;">Angga Perdana</div><div style="font-size:12px;color:var(--ink-3);">dr.angga.pk@gmail.com</div>
    <div class="tap" style="font-size:12px;font-weight:700;color:var(--magenta-dark);margin-top:2px;" onclick="toast('Edit profil akan tersedia di versi lengkap')">Edit Profil ›</div></div>
  </div>
</div>'''

poin_card = f'''<div class="card tap" style="background:var(--amber-tint);border-color:transparent;" onclick="toast('Riwayat &amp; penukaran poin akan tersedia di versi lengkap')">
  <div class="row" style="align-items:center;gap:12px;">
    <div style="width:42px;height:42px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;">{icon("coin",22,"#C8890F")}</div>
    <div class="col grow" style="gap:1px;"><div class="disp" style="font-weight:800;font-size:16px;">128 Poin Sehat</div><div style="font-size:11.5px;color:#8A6A21;">Setara Rp12.800 potongan booking</div></div>
    {icon("chevron",16,"#8A6A21")}
  </div>
  <div class="divider" style="margin:14px 0;background:rgba(0,0,0,0.06);"></div>
  <div class="row" style="gap:8px;flex-wrap:wrap;">
    <span class="chip" style="background:#fff;color:#8A6A21;">+10 tiap booking</span><span class="chip" style="background:#fff;color:#8A6A21;">+25 ajak keluarga</span><span class="chip" style="background:#fff;color:#8A6A21;">+15 isi ulasan</span>
  </div>
</div>'''

def prow(ic, label, sub=None, mag=False, onclick="toast('Fitur ini akan tersedia di versi lengkap')"):
    iconbg = "var(--magenta-tint)" if mag else "var(--teal-tint)"
    iconcolor = "var(--magenta-dark)" if mag else "var(--teal-dark)"
    sub_html = f'<div style="font-size:11.5px;color:var(--ink-3);">{sub}</div>' if sub else ""
    return f'''<div class="row tap" style="align-items:center;gap:14px;padding:15px 4px;" onclick="{onclick}">
      <div style="width:38px;height:38px;border-radius:11px;background:{iconbg};display:flex;align-items:center;justify-content:center;flex-shrink:0;">{icon(ic,18,iconcolor)}</div>
      <div class="col grow" style="gap:1px;"><div style="font-weight:700;font-size:13.5px;">{label}</div>{sub_html}</div>
      {icon("chevron",16,"var(--ink-4)")}
    </div>'''

menu_card = f'''<div class="card" style="padding:8px 16px;">
  {prow("doc","Rekam Medis",onclick="showScreen('rekammedis')")}<div class="divider"></div>
  {prow("family","Daftar Pasien","Keluarga &amp; anggota terdaftar")}<div class="divider"></div>
  {prow("tag","Daftar Harga Vaksinasi","Price list terbuka",onclick="showScreen('harga')")}<div class="divider"></div>
  {prow("calendar","Jadwal Vaksin","Anak, dewasa, pranikah, lansia",onclick="showScreen('jadwal')")}<div class="divider"></div>
  {prow("globe","Vaksin Internasional","Haji, umrah, studi &amp; e-ICV",onclick="showScreen('paket')")}<div class="divider"></div>
  {prow("pin","Lokasi Klinik","3 klinik di Tanjungpinang",onclick="showScreen('tentang')")}<div class="divider"></div>
  {prow("chart","Riwayat Transaksi &amp; Invoice")}<div class="divider"></div>
  {prow("building","Mitra Institusi","Mode Admin Sekolah / Kantor",mag=True,onclick="showScreen('korporat')")}<div class="divider"></div>
  {prow("whatsapp","Bantuan","Call Center " + BRAND["call_center"])}
</div>'''

profile = f'''
<div id="screen-profile" class="screen">
<div class="frame">
  {profile_header}
  <div class="col" style="padding:18px 20px 16px;gap:14px;">{poin_card}{menu_card}
    <div style="text-align:center;font-size:11px;color:var(--ink-4);padding:6px 0 2px;">Versi 1.0.0 (Prototipe)</div>
  </div>
  <div class="grow"></div>
  {navbar("user")}
</div>
</div>
'''

# ---------------------------------------------------------------- KORPORAT
korp_hdr = f'''<div class="hdr-bar" style="flex-direction:column;align-items:flex-start;gap:10px;background:var(--ink);flex-shrink:0;">
  <div class="row" style="align-items:center;gap:14px;width:100%;">
    <span class="tap" onclick="showScreen('profile')">{BACK_ICON}</span>
    <div class="col" style="gap:1px;"><div class="disp" style="font-size:18px;font-weight:700;">Dashboard Vaksinasi Sekolah</div><div style="font-size:11.5px;opacity:.75;">SDN Melati 02 · Tahun Ajaran 2026/2027</div></div>
  </div>
</div>'''

korp_tabs = f'''<div class="row" style="padding:14px 20px 0;gap:22px;border-bottom:1px solid var(--line);flex-shrink:0;">
  <div class="tap" style="padding-bottom:12px;border-bottom:2.4px solid var(--magenta);color:var(--magenta-dark);font-weight:700;font-size:13px;">Ringkasan</div>
  <div class="tap" style="padding-bottom:12px;color:var(--ink-3);font-weight:600;font-size:13px;" onclick="toast('Daftar peserta akan tersedia di versi lengkap')">Peserta</div>
  <div class="tap" style="padding-bottom:12px;color:var(--ink-3);font-weight:600;font-size:13px;" onclick="toast('Laporan akan tersedia di versi lengkap')">Laporan</div>
</div>'''

def kstat(value, label, color="var(--ink)"):
    return f'''<div class="card" style="flex:1;padding:14px;text-align:center;"><div class="disp" style="font-size:21px;font-weight:800;color:{color};">{value}</div><div style="font-size:10.5px;color:var(--ink-3);margin-top:4px;line-height:1.3;">{label}</div></div>'''

korp_stats = f'''<div class="row" style="gap:10px;padding:16px 20px 0;">{kstat("320","Total Peserta")}{kstat("248","Sudah Divaksin","var(--teal-dark)")}{kstat("77%","Coverage","var(--magenta-dark)")}</div>'''

korp_bulk = f'''<div style="padding:16px 20px 0;"><button class="btn btn-primary tap" style="width:100%;" onclick="toast('Booking massal akan tersedia di versi lengkap')">{icon("plus",16,"#fff")} Booking Massal (Bulk)</button></div>'''

def coverage_row(cls, pct, color):
    return f'''<div class="col" style="gap:6px;"><div class="row" style="justify-content:space-between;"><span style="font-size:12.5px;font-weight:700;">{cls}</span><span style="font-size:12px;font-weight:700;color:{color};">{pct}%</span></div>
    <div style="height:7px;border-radius:5px;background:#F1F1F0;overflow:hidden;"><div style="width:{pct}%;height:100%;background:{color};"></div></div></div>'''

coverage_card = f'''<div class="card"><div style="font-weight:700;font-size:14.5px;margin-bottom:14px;">Cakupan per Kelas</div>
  <div class="col" style="gap:14px;">{coverage_row("Kelas 1A","92","var(--teal-dark)")}{coverage_row("Kelas 1B","65","#C8890F")}{coverage_row("Kelas 2A","100","var(--teal-dark)")}{coverage_row("Kelas 2B","58","#C8890F")}</div>
</div>'''

report_card = f'''<div class="card">
  <div class="row" style="align-items:center;gap:12px;"><div style="width:40px;height:40px;border-radius:12px;background:var(--teal-tint);display:flex;align-items:center;justify-content:center;">{icon("upload",19,"var(--teal-dark)")}</div>
  <div class="col grow" style="gap:1px;"><div style="font-weight:700;font-size:13.5px;">Laporan &amp; Kepatuhan</div><div style="font-size:11.5px;color:var(--ink-3);">Format sesuai standar BIAS</div></div></div>
  <button class="btn btn-outline tap" style="width:100%;margin-top:14px;padding:12px;font-size:13px;" onclick="toast('Laporan sedang disiapkan...')">{icon("download",15,"var(--teal-dark)")} Unduh Laporan untuk Dinas Kesehatan</button>
</div>'''

invoice_card = f'''<div class="card">
  <div class="row" style="align-items:center;"><div style="font-weight:700;font-size:14.5px;">Invoice &amp; Termin</div><div class="grow"></div><span class="chip chip-amber">Jatuh Tempo 15 Sep</span></div>
  <div class="row" style="align-items:center;margin-top:12px;"><div class="col" style="gap:2px;"><div style="font-size:12px;color:var(--ink-3);">INV-2026-0142</div><div class="disp" style="font-weight:800;font-size:17px;">Rp48.000.000</div></div>
  <div class="grow"></div><button class="btn btn-outline-mag tap" style="padding:10px 16px;font-size:12.5px;" onclick="toast('Detail invoice akan tersedia di versi lengkap')">Lihat Invoice</button></div>
</div>'''

korporat = f'''
<div id="screen-korporat" class="screen">
<div class="frame">
  {korp_hdr}{korp_tabs}{korp_stats}{korp_bulk}
  <div class="col" style="padding:16px 20px 24px;gap:14px;">{coverage_card}{report_card}{invoice_card}</div>
</div>
</div>
'''

# ---------------------------------------------------------------- DAFTAR HARGA
def harga_group(nama, baris):
    rows = ""
    for _, _, sediaan, merk, spes, umum in baris:
        sub = f'<div style="font-size:10.5px;color:var(--ink-4);margin-top:1px;">{merk}</div>' if merk != sediaan else ""
        spes_html = ('<span class="p-spes" style="color:var(--ink-4);">Hubungi CS</span>' if spes == "—"
                     else f'<span class="p-spes">Rp{spes}</span>')
        rows += f'''<div class="row" style="align-items:flex-start;gap:10px;padding:10px 0;border-top:1px solid var(--line);">
          <div class="col grow" style="min-width:0;"><div style="font-size:12.5px;font-weight:600;">{sediaan}</div>{sub}</div>
          <div class="disp" style="font-size:13px;font-weight:800;color:var(--magenta-dark);white-space:nowrap;">
            <span class="p-umum">Rp{umum}</span>{spes_html}
          </div>
        </div>'''
    return f'''<div class="card" style="padding:16px 18px;">
      <div class="row" style="align-items:center;gap:8px;">
        <div style="width:30px;height:30px;border-radius:9px;background:var(--teal-tint);display:flex;align-items:center;justify-content:center;flex-shrink:0;">{icon("syringe",16,"var(--teal-dark)")}</div>
        <div style="font-weight:700;font-size:14px;">{nama}</div>
      </div>
      <div style="margin-top:6px;">{rows}</div>
    </div>'''

_urut, _grup = [], {}
for row in HARGA:
    nama = row[1]
    if nama not in _grup:
        _grup[nama] = []
        _urut.append(nama)
    _grup[nama].append(row)
harga_groups = "".join(harga_group(n, _grup[n]) for n in _urut)

harga = f'''
<div id="screen-harga" class="screen">
<div class="frame">
  <div class="hdr-bar"><span class="tap" onclick="showScreen('home')">{BACK_ICON}</span><div class="disp">Daftar Harga Vaksinasi</div></div>
  <div style="padding:16px 20px 0;">
    <div class="row" style="align-items:center;gap:8px;background:var(--teal-tint);border-radius:14px;padding:12px 14px;">
      {icon("check-c",16,"var(--teal-dark)")}
      <span style="font-size:11.5px;color:var(--teal-dark);font-weight:600;line-height:1.45;">Harga sudah termasuk jasa dokter, vaksin, bahan habis pakai &amp; administrasi.</span>
    </div>
  </div>
  <div style="padding:14px 20px 0;position:sticky;top:0;background:var(--bg);z-index:5;">
    <div class="row" style="gap:8px;">
      <div class="tarif-opt tap choice active" onclick="setTarif(this,'umum')">Dokter Umum</div>
      <div class="tarif-opt tap choice" onclick="setTarif(this,'spes')">Dokter Spesialis</div>
    </div>
  </div>
  <div id="harga-wrap" class="umum col" style="padding:14px 20px 24px;gap:12px;">
    {harga_groups}
    <div style="font-size:11px;color:var(--ink-4);line-height:1.5;padding:0 4px;">Harga dapat berubah sewaktu-waktu. Konfirmasi terakhir saat reservasi melalui call center {BRAND["call_center"]}.</div>
  </div>
</div>
</div>
'''

# ---------------------------------------------------------------- JADWAL VAKSIN
def anak_step(usia, badge, isi, last=False):
    badge_html = f'<span class="chip chip-mag" style="padding:3px 9px;font-size:9.5px;">{badge}</span>' if badge else ""
    line = "" if last else '<div style="position:absolute;left:7px;top:22px;bottom:-14px;width:2px;background:var(--line);"></div>'
    items = "".join(f'<div style="font-size:12px;color:var(--ink-2);line-height:1.6;">{i}</div>' for i in isi)
    return f'''<div style="position:relative;padding-left:26px;padding-bottom:14px;">
      {line}
      <div style="position:absolute;left:0;top:5px;width:16px;height:16px;border-radius:50%;background:#fff;border:3px solid var(--teal);"></div>
      <div class="row" style="align-items:center;gap:8px;margin-bottom:4px;"><span class="disp" style="font-weight:800;font-size:13.5px;">{usia}</span>{badge_html}</div>
      {items}
    </div>'''

anak_steps = "".join(
    anak_step(u, b, i, last=(idx == len(JADWAL_ANAK) - 1))
    for idx, (u, b, i) in enumerate(JADWAL_ANAK)
)

def dewasa_group(usia, keys, active=False):
    rows = ""
    for k in keys:
        nama, ds = dosis(k)
        rows += f'''<div class="row" style="align-items:flex-start;gap:12px;padding:9px 0;border-top:1px solid var(--line);">
          <div style="font-size:12.5px;font-weight:700;width:120px;flex-shrink:0;">{nama}</div>
          <div style="font-size:11.5px;color:var(--ink-3);line-height:1.5;">{ds}</div>
        </div>'''
    cls = "usia-pane" + (" active" if active else "")
    return f'<div class="{cls}" data-usia="{usia}"><div class="card" style="padding:14px 18px;">{rows}</div></div>'

dewasa_tabs = "".join(
    f'<div class="usia-opt tap choice{" active" if i == 0 else ""}" onclick="pickUsia(this,{i})">{u}</div>'
    for i, (u, _) in enumerate(JADWAL_DEWASA)
)
dewasa_panes = "".join(dewasa_group(u, k, active=(i == 0)) for i, (u, k) in enumerate(JADWAL_DEWASA))

pranikah_cards = "".join(
    f'''<div class="row" style="align-items:flex-start;gap:12px;padding:11px 0;border-top:1px solid var(--line);">
      <div style="width:34px;height:34px;border-radius:10px;background:var(--magenta-tint);display:flex;align-items:center;justify-content:center;flex-shrink:0;">{icon("syringe",16,"var(--magenta-dark)")}</div>
      <div class="col grow" style="gap:2px;"><div style="font-weight:700;font-size:13px;">{n}</div>
      <div style="font-size:11.5px;color:var(--ink-3);line-height:1.5;">{d} · {ket}</div></div>
    </div>''' for n, d, ket in JADWAL_PRANIKAH_VAKSIN
)
pranikah_timeline = "".join(
    f'''<div class="row" style="align-items:flex-start;gap:12px;padding:10px 0;border-top:1px solid var(--line);">
      <div class="chip chip-mag" style="width:82px;justify-content:center;flex-shrink:0;">{w}</div>
      <div class="col" style="gap:2px;">{"".join(f'<div style="font-size:12px;color:var(--ink-2);line-height:1.55;">{i}</div>' for i in isi)}</div>
    </div>''' for w, isi in JADWAL_PRANIKAH_WAKTU
)

lansia_cards = "".join(
    f'''<div class="card">
      <div class="row" style="align-items:center;gap:10px;">{icon("check-c",18,"var(--green)")}<div style="font-weight:700;font-size:14px;">{n}</div></div>
      <div class="chip chip-teal" style="margin-top:10px;">{d}</div>
      <div style="font-size:12px;color:var(--ink-2);line-height:1.6;margin-top:10px;">{ket}</div>
    </div>''' for n, d, ket in JADWAL_LANSIA
)

jadwal = f'''
<div id="screen-jadwal" class="screen">
<div class="frame">
  <div class="hdr-bar"><span class="tap" onclick="showScreen('home')">{BACK_ICON}</span><div class="disp">Jadwal Vaksin</div></div>
  <div class="row" style="gap:8px;padding:16px 20px 6px;overflow-x:auto;">
    <div class="jad-opt tap choice active" onclick="pickJadwal(this,'anak')">Anak</div>
    <div class="jad-opt tap choice" onclick="pickJadwal(this,'dewasa')">Dewasa</div>
    <div class="jad-opt tap choice" onclick="pickJadwal(this,'pranikah')">Pranikah</div>
    <div class="jad-opt tap choice" onclick="pickJadwal(this,'lansia')">Lansia</div>
  </div>

  <div class="jad-pane active" data-jad="anak">
    <div class="col" style="padding:12px 20px 24px;gap:12px;">
      <div style="font-size:12px;color:var(--ink-3);line-height:1.55;">Sesuai jadwal imunisasi anak <b>IDAI terbaru 2024</b>. Ceklis otomatis mengikuti rekam medis pasien.</div>
      <div class="card">{anak_steps}</div>
    </div>
  </div>

  <div class="jad-pane" data-jad="dewasa">
    <div class="col" style="padding:12px 20px 24px;gap:12px;">
      <div style="font-size:12px;color:var(--ink-3);line-height:1.55;">Sesuai rekomendasi <b>PAPDI 2025</b> — Perhimpunan Dokter Spesialis Penyakit Dalam Indonesia.</div>
      <div class="row" style="gap:8px;overflow-x:auto;padding-bottom:2px;">{dewasa_tabs}</div>
      {dewasa_panes}
      <div class="row" style="align-items:flex-start;gap:8px;background:var(--amber-tint);border-radius:12px;padding:11px 13px;">
        {icon("bell",15,"#9C6B0E")}<span style="font-size:11px;color:#8A6A21;line-height:1.5;">{JADWAL_DEWASA_CATATAN}</span>
      </div>
    </div>
  </div>

  <div class="jad-pane" data-jad="pranikah">
    <div class="col" style="padding:12px 20px 24px;gap:12px;">
      <div class="card" style="padding:14px 18px;">
        <div style="font-weight:700;font-size:14px;">Vaksin pranikah terdiri dari</div>
        {pranikah_cards}
      </div>
      <div class="card" style="padding:14px 18px;">
        <div style="font-weight:700;font-size:14px;">Jadwal pemberian</div>
        <div style="font-size:11.5px;color:var(--ink-4);margin-top:2px;margin-bottom:4px;">Dihitung mundur dari tanggal pernikahan.</div>
        {pranikah_timeline}
      </div>
      <div style="background:var(--magenta);color:#fff;border-radius:14px;padding:13px 16px;text-align:center;font-weight:700;font-size:13px;font-family:'Baloo 2';">Lengkapi vaksin pranikah sebelum menikah!</div>
    </div>
  </div>

  <div class="jad-pane" data-jad="lansia">
    <div class="col" style="padding:12px 20px 24px;gap:12px;">
      <div style="font-size:12px;color:var(--ink-3);line-height:1.55;">Lansia usia <b>50 tahun ke atas</b> juga membutuhkan vaksinasi.</div>
      {lansia_cards}
      <div style="background:var(--magenta-tint);border-radius:14px;padding:13px 16px;text-align:center;font-weight:700;font-size:13px;color:var(--magenta-dark);font-family:'Baloo 2';">Lindungi orang tua yang disayangi dengan vaksin!</div>
    </div>
  </div>
</div>
</div>
'''

# ---------------------------------------------------------------- VAKSIN INTERNASIONAL
intl_wajib = "".join(
    f'''<div class="row" style="align-items:flex-start;gap:12px;padding:12px 0;border-top:1px solid var(--line);">
      <div style="width:34px;height:34px;border-radius:10px;background:var(--teal-tint);display:flex;align-items:center;justify-content:center;flex-shrink:0;">{icon("shield",17,"var(--teal-dark)")}</div>
      <div class="col grow" style="gap:3px;"><div style="font-weight:700;font-size:13px;">{n}</div>
      <div style="font-size:11.5px;color:var(--ink-3);line-height:1.55;">{k}</div></div>
    </div>''' for n, k in VAKSIN_INTERNASIONAL_WAJIB
)
intl_tambahan = "".join(
    f'''<div class="row" style="align-items:flex-start;gap:12px;padding:12px 0;border-top:1px solid var(--line);">
      <div style="width:34px;height:34px;border-radius:10px;background:var(--magenta-tint);display:flex;align-items:center;justify-content:center;flex-shrink:0;">{icon("plus",17,"var(--magenta-dark)")}</div>
      <div class="col grow" style="gap:3px;"><div style="font-weight:700;font-size:13px;">{n}</div>
      <div style="font-size:11.5px;color:var(--ink-3);line-height:1.55;">{k}</div></div>
    </div>''' for n, k in VAKSIN_INTERNASIONAL_TAMBAHAN
)

def intl_price(nama, harga, coret):
    coret_html = f'<div style="font-size:11px;color:var(--ink-4);text-decoration:line-through;">Rp{coret}</div>' if coret else ""
    promo = '<span class="chip chip-mag" style="padding:3px 8px;font-size:9.5px;">PROMO</span>' if coret else ""
    return f'''<div class="card row" style="align-items:center;gap:12px;padding:15px 18px;">
      <div class="col grow" style="gap:3px;"><div class="row" style="align-items:center;gap:7px;"><span style="font-weight:700;font-size:13px;">{nama}</span>{promo}</div>{coret_html}</div>
      <div class="disp" style="font-size:17px;font-weight:800;color:var(--magenta-dark);white-space:nowrap;">Rp{harga}</div>
    </div>'''

paket_triple = f'''<div class="card" style="border:1.6px solid var(--magenta);padding:18px;">
  <div class="row" style="align-items:center;gap:8px;">
    <div class="disp" style="font-weight:800;font-size:15px;">{PAKET_TRIPLE["nama"]}</div>
    <span class="chip chip-mag" style="padding:3px 8px;font-size:9.5px;">HEMAT</span>
  </div>
  <div class="col" style="gap:7px;margin-top:12px;">
    {"".join(f'<div class="row" style="align-items:center;gap:8px;">{icon("check-c",15,"var(--teal-dark)")}<span style="font-size:12.5px;color:var(--ink-2);">{i}</span></div>' for i in PAKET_TRIPLE["isi"])}
  </div>
  <div class="divider" style="margin:14px 0;"></div>
  <div class="row" style="align-items:baseline;gap:10px;">
    <span class="disp" style="font-size:22px;font-weight:800;color:var(--magenta-dark);">Rp{PAKET_TRIPLE["harga"]}</span>
    <span style="font-size:12.5px;color:var(--ink-4);text-decoration:line-through;">Rp{PAKET_TRIPLE["coret"]}</span>
  </div>
</div>'''

paket = f'''
<div id="screen-paket" class="screen">
<div class="frame">
  <div class="hdr-bar"><span class="tap" onclick="showScreen('home')">{BACK_ICON}</span><div class="disp">Vaksin Internasional</div></div>
  <div class="col" style="padding:16px 20px 24px;gap:14px;">
    <div style="font-size:12px;color:var(--ink-3);line-height:1.6;">Bagi jamaah <b>haji &amp; umrah</b> wajib vaksin Meningitis dan Polio. WHO merekomendasikan vaksinasi tambahan Influenza dan Pneumonia.</div>

    <div class="card" style="padding:14px 18px;">
      <div class="row" style="align-items:center;gap:8px;"><div style="font-weight:700;font-size:14px;">Vaksin wajib</div><span class="chip chip-teal">Regulasi Arab Saudi</span></div>
      {intl_wajib}
    </div>

    <div class="card" style="padding:14px 18px;">
      <div class="row" style="align-items:center;gap:8px;"><div style="font-weight:700;font-size:14px;">Vaksin tambahan</div><span class="chip chip-amber">Rekomendasi WHO</span></div>
      {intl_tambahan}
    </div>

    <div class="disp" style="font-size:15px;font-weight:800;padding-top:4px;">Harga vaksinasi internasional</div>
    {"".join(intl_price(n, h, c) for n, h, c in HARGA_INTERNASIONAL)}
    {paket_triple}

    <div class="card row" style="align-items:center;gap:14px;background:var(--teal-tint);border-color:transparent;">
      <div style="width:42px;height:42px;border-radius:12px;background:#fff;display:flex;align-items:center;justify-content:center;flex-shrink:0;">{icon("qr",20,"var(--teal-dark)")}</div>
      <div class="col grow" style="gap:2px;"><div style="font-weight:700;font-size:13.5px;">Buku Kuning Elektronik (e-ICV)</div>
      <div style="font-size:11.5px;color:var(--ink-2);">Diterbitkan langsung di klinik setelah vaksinasi.</div></div>
    </div>

    <button class="btn btn-primary tap" onclick="showScreen('booking')">{icon("plus",16,"#fff")} Booking Vaksin Internasional</button>
  </div>
</div>
</div>
'''

# ---------------------------------------------------------------- TENTANG & LOKASI
pilar_cards = "".join(
    f'''<div class="card">
      <div class="row" style="align-items:center;gap:10px;">
        <div style="width:34px;height:34px;border-radius:10px;background:var(--teal-tint);display:flex;align-items:center;justify-content:center;">{icon(ic,18,"var(--teal-dark)")}</div>
        <div class="disp" style="font-weight:800;font-size:15px;">{judul}</div>
      </div>
      <div class="col" style="gap:8px;margin-top:12px;">
        {"".join(f'<div class="row" style="align-items:flex-start;gap:8px;">{icon("check-c",14,"var(--teal-dark)")}<span style="font-size:12px;color:var(--ink-2);line-height:1.55;">{p}</span></div>' for p in poin)}
      </div>
    </div>''' for ic, judul, poin in PILAR
)

layanan_cards = "".join(
    f'''<div class="card">
      <div class="row" style="align-items:center;gap:10px;">
        <div style="width:36px;height:36px;border-radius:11px;background:var(--magenta-tint);display:flex;align-items:center;justify-content:center;">{icon(ic,18,"var(--magenta-dark)")}</div>
        <div class="col"><div class="disp" style="font-weight:800;font-size:14.5px;">{nama}</div>
        <div style="font-size:11.5px;color:var(--ink-3);">{ringkas}</div></div>
      </div>
      <div style="font-size:12px;color:var(--ink-2);line-height:1.6;margin-top:11px;">{detail}</div>
      <div class="chip chip-teal" style="margin-top:10px;">{tagline}</div>
    </div>''' for ic, nama, ringkas, detail, tagline in LAYANAN
)

alur_steps = "".join(
    f'''<div class="row" style="align-items:flex-start;gap:12px;padding:9px 0;">
      <div class="disp" style="width:24px;height:24px;border-radius:50%;background:var(--teal);color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;flex-shrink:0;">{i+1}</div>
      <span style="font-size:12px;color:var(--ink-2);line-height:1.55;padding-top:3px;">{s}</span>
    </div>''' for i, s in enumerate(ALUR_RESERVASI)
)

dokter_rows = "".join(
    f'''<div class="row" style="align-items:center;gap:12px;padding:11px 0;border-top:1px solid var(--line);">
      <div style="width:40px;height:40px;border-radius:50%;background:var(--teal-tint);display:flex;align-items:center;justify-content:center;flex-shrink:0;">
        <span class="disp" style="font-weight:800;font-size:13px;color:var(--teal-dark);">{ini}</span></div>
      <div class="col grow" style="gap:1px;"><div style="font-weight:700;font-size:13px;">{nama}</div>
      <div style="font-size:11.5px;color:var(--ink-3);">{spes}</div></div>
    </div>''' for nama, spes, ini in DOKTER
)

klinik_rows = "".join(
    f'''<div class="row tap" style="align-items:flex-start;gap:12px;padding:12px 0;border-top:1px solid var(--line);" onclick="toast('Peta lokasi akan tersedia di versi lengkap')">
      <div style="width:34px;height:34px;border-radius:10px;background:var(--magenta-tint);display:flex;align-items:center;justify-content:center;flex-shrink:0;">{icon("pin",16,"var(--magenta-dark)")}</div>
      <div class="col grow" style="gap:2px;"><div style="font-weight:700;font-size:13px;">{nama}</div>
      <div style="font-size:11.5px;color:var(--ink-3);line-height:1.5;">{alamat}</div></div>
      {icon("chevron",15,"var(--ink-4)")}
    </div>''' for nama, alamat in KLINIK
)

tentang = f'''
<div id="screen-tentang" class="screen">
<div class="frame">
  <div class="hdr-bar"><span class="tap" onclick="showScreen('home')">{BACK_ICON}</span><div class="disp">Tentang &amp; Lokasi</div></div>
  <div class="col" style="padding:18px 20px 24px;gap:14px;">
    <div class="col" style="align-items:center;gap:10px;padding:6px 0 4px;">
      {logo_mark(30)}
      <div style="font-size:12px;font-weight:700;color:var(--teal-dark);text-align:center;">{BRAND["tagline"]}</div>
      <div style="font-size:11.5px;color:var(--ink-3);text-align:center;line-height:1.6;">Layanan vaksinasi dari {BRAND["group"]} untuk segala usia.</div>
    </div>

    {pilar_cards}

    <div class="disp" style="font-size:15px;font-weight:800;padding-top:6px;">Kemudahan dari VaksinKu</div>
    {layanan_cards}

    <div class="card" style="padding:14px 18px;">
      <div style="font-weight:700;font-size:14px;margin-bottom:2px;">Alur reservasi</div>
      {alur_steps}
    </div>

    <div class="card" style="padding:14px 18px;">
      <div style="font-weight:700;font-size:14px;">Dokter vaksinasi</div>
      <div style="font-size:11.5px;color:var(--ink-4);margin-top:2px;margin-bottom:2px;">{BRAND["group"]}</div>
      {dokter_rows}
    </div>

    <div class="card" style="padding:14px 18px;">
      <div style="font-weight:700;font-size:14px;">Lokasi klinik</div>
      <div style="font-size:11.5px;color:var(--ink-4);margin-top:2px;margin-bottom:2px;">Tanjungpinang, Kepulauan Riau</div>
      {klinik_rows}
    </div>

    <div class="card" style="background:var(--teal-dark);border-color:transparent;color:#fff;">
      <div class="row" style="align-items:center;gap:12px;">
        <div style="width:42px;height:42px;border-radius:50%;background:rgba(255,255,255,.16);display:flex;align-items:center;justify-content:center;flex-shrink:0;">{icon("whatsapp",20,"#fff")}</div>
        <div class="col grow" style="gap:2px;"><div style="font-size:11px;opacity:.85;">{BRAND["call_center_label"]}</div>
        <div class="disp" style="font-weight:800;font-size:18px;">{BRAND["call_center"]}</div></div>
      </div>
      <div class="divider" style="margin:14px 0;background:rgba(255,255,255,.18);"></div>
      <div class="row" style="gap:16px;flex-wrap:wrap;">
        <span style="font-size:11.5px;opacity:.9;">{BRAND["instagram"]}</span>
        <span style="font-size:11.5px;opacity:.9;">{BRAND["website"]}</span>
      </div>
    </div>
  </div>
</div>
</div>
'''

# ---------------------------------------------------------------- QUICK NAV
quicknav_items = [
    ("splash","1 · Splash"), ("onboarding","2 · Onboarding"), ("login","3 · Login"),
    ("home","4 · Beranda"), ("booking","5 · Booking"), ("rekammedis","6 · Rekam Medis"),
    ("chat","7 · Chat"), ("profile","8 · Profil"), ("korporat","9 · Korporat"),
    ("harga","10 · Daftar Harga"), ("jadwal","11 · Jadwal Vaksin"),
    ("paket","12 · Vaksin Internasional"), ("tentang","13 · Tentang & Lokasi"),
]
quicknav_html = "".join(
    f'<div class="qn-pill{" active" if k=="splash" else ""}" data-target="{k}" onclick="showScreen(\'{k}\')">{label}</div>'
    for k, label in quicknav_items
)

# ---------------------------------------------------------------- SHELL
STYLE = '''
:root{
  --teal:#56C3C7; --teal-dark:#2E9BA0; --teal-tint:#E9F9FA; --teal-tint2:#D7F2F3;
  --magenta:#D11972; --magenta-dark:#A81260; --magenta-tint:#FDECF3; --magenta-tint2:#FBD9E7;
  --ink:#262626; --ink-2:#4B4B4B; --ink-3:#606060; --ink-4:#9AA0A6;
  --line:#ECECEC; --bg:#FAFAF9; --card:#FFFFFF;
  --amber:#E8A23A; --amber-tint:#FFF3DF;
  --green:#2E9E5B; --green-tint:#E8F7EE;
  --stage-bg-1:#F1EFEA; --stage-bg-2:#E7EAE6;
}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;}
body{
  background:radial-gradient(1100px 700px at 20% 0%, var(--stage-bg-1), var(--stage-bg-2));
  min-height:100vh;font-family:'Plus Jakarta Sans',-apple-system,BlinkMacSystemFont,sans-serif;color:var(--ink);
}
a{color:var(--magenta-dark);text-decoration:none;}
a:hover{color:var(--magenta);}
img{display:block;max-width:100%;}
.stage{display:flex;flex-direction:column;align-items:center;padding:40px 20px 60px;gap:22px;}
.stage-label{font-size:11.5px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--ink-4);}
.qn-row{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;max-width:640px;}
.qn-pill{
  font-family:'Plus Jakarta Sans',sans-serif;font-size:12px;font-weight:700;color:var(--ink-2);
  background:#fff;border:1.4px solid var(--line);border-radius:999px;padding:8px 14px;cursor:pointer;
  transition:all .15s;
}
.qn-pill:hover{border-color:var(--teal);}
.qn-pill.active{background:var(--ink);color:#fff;border-color:var(--ink);}
.phone-bezel{
  width:426px;padding:14px;border-radius:52px;background:linear-gradient(160deg,#22252A,#111214);
  box-shadow:0 40px 70px -25px rgba(20,20,20,.5),0 12px 30px -14px rgba(20,20,20,.35);
}
.phone-mask{
  width:398px;height:862px;border-radius:38px;overflow:hidden;position:relative;background:var(--bg);
}
.disp{font-family:'Baloo 2',ui-rounded,sans-serif;}
.row{display:flex;flex-direction:row;}
.col{display:flex;flex-direction:column;}
.grow{flex-grow:1;}
.tap{cursor:pointer;}
.screen{
  position:absolute;inset:0;overflow-y:auto;-webkit-overflow-scrolling:touch;display:none;
  scrollbar-width:none;
}
.screen::-webkit-scrollbar{display:none;}
.screen.active{display:block;}
.frame{
  width:100%;min-height:100%;background:var(--bg);font-family:'Plus Jakarta Sans',-apple-system,sans-serif;
  color:var(--ink);display:flex;flex-direction:column;position:relative;
}
.card{
  background:var(--card);border:1px solid var(--line);border-radius:20px;padding:18px;
  box-shadow:0 1px 2px rgba(38,38,38,0.03),0 10px 24px -16px rgba(38,38,38,0.18);
}
.btn{
  font-family:'Baloo 2',ui-rounded,sans-serif;font-weight:700;font-size:15px;border-radius:999px;padding:15px 20px;
  display:flex;align-items:center;justify-content:center;gap:8px;border:none;cursor:pointer;
}
.btn-primary{background:var(--magenta);color:#fff;}
.btn-outline{background:#fff;border:1.6px solid var(--teal);color:var(--teal-dark);}
.btn-outline-mag{background:#fff;border:1.6px solid var(--magenta);color:var(--magenta-dark);}
.chip{border-radius:999px;padding:6px 12px;font-size:12px;font-weight:700;display:inline-flex;align-items:center;gap:5px;white-space:nowrap;}
.chip-teal{background:var(--teal-tint);color:var(--teal-dark);}
.chip-mag{background:var(--magenta-tint);color:var(--magenta-dark);}
.chip-amber{background:var(--amber-tint);color:#9C6B0E;}
.input{width:100%;border:1.4px solid var(--line);border-radius:14px;padding:14px 14px;font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;color:var(--ink);background:#fff;}
.input:focus{outline:2px solid var(--teal);outline-offset:1px;}
.label{font-size:13.5px;font-weight:700;color:var(--ink);margin-bottom:8px;display:block;}
.req{color:var(--magenta);}
.hint{font-size:12px;color:var(--ink-4);margin:2px 0 10px;line-height:1.5;}
.section{padding:20px;}
.hdr-bar{background:var(--teal-dark);color:#fff;padding:18px 20px 20px;display:flex;align-items:center;gap:14px;}
.hdr-bar .disp{font-size:19px;font-weight:700;}
.iconbtn{width:38px;height:38px;border-radius:50%;background:#fff;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.divider{height:1px;background:var(--line);width:100%;}
.navbar{margin-top:auto;background:#fff;border-top:1px solid var(--line);height:78px;display:flex;align-items:center;justify-content:space-around;padding:0 6px;position:sticky;bottom:0;}
.navitem{display:flex;flex-direction:column;align-items:center;gap:4px;color:var(--ink-4);font-size:10.5px;font-weight:600;width:58px;}
.navitem.active{color:var(--magenta-dark);}
.navfab{width:56px;height:56px;border-radius:50%;background:var(--magenta);display:flex;align-items:center;justify-content:center;margin-top:-30px;box-shadow:0 8px 18px -6px rgba(209,25,114,0.55);border:5px solid #fff;}

/* ---- interactive choice states ---- */
.choice{transition:border-color .15s,background-color .15s,color .15s;}
.svc-card{flex:1;border:1.4px solid var(--line);background:#fff;border-radius:16px;padding:14px 8px;display:flex;flex-direction:column;align-items:center;gap:6px;color:var(--ink-2);font-size:11.5px;font-weight:700;text-align:center;}
.svc-card svg{color:var(--teal-dark);}
.svc-card.active{border-color:var(--magenta);background:var(--magenta-tint);color:var(--magenta-dark);}
.svc-card.active svg{color:var(--magenta-dark);}
.gender-opt{flex:1;text-align:center;padding:12px;border-radius:14px;border:1.4px solid var(--line);font-size:13px;color:var(--ink-3);font-weight:600;}
.gender-opt.active{border:1.6px solid var(--magenta);background:var(--magenta-tint);color:var(--magenta-dark);font-weight:700;}
.loc-opt{flex:1;border:1.4px solid var(--line);border-radius:16px;padding:14px;display:flex;flex-direction:column;align-items:center;gap:6px;color:var(--ink-2);font-size:12.5px;font-weight:700;}
.loc-opt svg{color:var(--teal-dark);}
.loc-opt.active{border:1.6px solid var(--magenta);background:var(--magenta-tint);color:var(--magenta-dark);}
.loc-opt.active svg{color:var(--magenta-dark);}
.slot-opt{flex:1;text-align:center;padding:10px 4px;border-radius:12px;border:1.4px solid var(--line);color:var(--ink-2);font-size:12px;font-weight:700;background:#fff;}
.slot-opt.active{background:var(--magenta);border-color:var(--magenta);color:#fff;}
.slot-opt.full{background:#F5F5F4;color:var(--ink-4);text-decoration:line-through;cursor:not-allowed;}
.date-opt{flex:1;text-align:center;padding:10px 2px;border-radius:12px;border:1.4px solid var(--line);color:var(--ink-2);background:#fff;}
.date-opt.active{background:var(--magenta);border-color:var(--magenta);color:#fff;}
.pay-opt{flex:1;text-align:center;padding:12px 4px;border-radius:14px;border:1.4px solid var(--line);font-size:12px;font-weight:700;color:var(--ink-2);}
.pay-opt.active{border:1.6px solid var(--magenta);background:var(--magenta-tint);color:var(--magenta-dark);}
.patient-tab{padding:8px 14px;border-radius:999px;border:1.4px solid var(--line);color:var(--ink-2);font-size:12.5px;font-weight:700;}
.patient-tab.active{background:var(--magenta);color:#fff;border-color:var(--magenta);}
.need-card{position:relative;border:1.4px solid var(--line);background:#fff;border-radius:18px;padding:16px 14px;display:flex;flex-direction:column;gap:10px;color:var(--ink-2);}
.need-card .ic-circle{width:42px;height:42px;border-radius:50%;background:var(--teal-tint);color:var(--teal-dark);display:flex;align-items:center;justify-content:center;}
.need-card .chk{position:absolute;top:10px;right:10px;display:none;color:var(--magenta);}
.need-card.active{border:1.6px solid var(--magenta);background:var(--magenta-tint);}
.need-card.active .ic-circle{background:var(--magenta);color:#fff;}
.need-card.active .chk{display:flex;}
.dok-opt{flex:1;border:1.4px solid var(--line);border-radius:16px;padding:13px 14px;background:#fff;}
.dok-opt .dok-dot{width:15px;height:15px;border-radius:50%;border:2px solid var(--ink-4);display:inline-block;flex-shrink:0;}
.dok-opt.active{border:1.6px solid var(--magenta);background:var(--magenta-tint);}
.dok-opt.active .dok-dot{border-color:var(--magenta);background:radial-gradient(circle,var(--magenta) 45%,#fff 48%);}

/* ---- tarif toggle on the price list ---- */
.tarif-opt{flex:1;text-align:center;padding:11px 8px;border-radius:999px;border:1.4px solid var(--line);background:#fff;font-size:12.5px;font-weight:700;color:var(--ink-2);}
.tarif-opt.active{background:var(--teal-dark);border-color:var(--teal-dark);color:#fff;}
#harga-wrap.umum .p-spes{display:none;}
#harga-wrap.spes .p-umum{display:none;}

/* ---- jadwal tabs ---- */
.jad-opt{padding:9px 16px;border-radius:999px;border:1.4px solid var(--line);background:#fff;font-size:12.5px;font-weight:700;color:var(--ink-2);white-space:nowrap;}
.jad-opt.active{background:var(--magenta);border-color:var(--magenta);color:#fff;}
.jad-pane{display:none;}
.jad-pane.active{display:block;}
.usia-opt{padding:8px 13px;border-radius:999px;border:1.4px solid var(--line);background:#fff;font-size:11.5px;font-weight:700;color:var(--ink-2);white-space:nowrap;}
.usia-opt.active{background:var(--teal-dark);border-color:var(--teal-dark);color:#fff;}
.usia-pane{display:none;}
.usia-pane.active{display:block;}

/* ---- toast ---- */
#toast-host{position:absolute;left:0;right:0;bottom:96px;display:flex;flex-direction:column;align-items:center;gap:8px;pointer-events:none;z-index:50;}
.toast-pill{
  background:var(--ink);color:#fff;font-size:12.5px;font-weight:600;padding:11px 18px;border-radius:999px;
  box-shadow:0 10px 24px -10px rgba(0,0,0,.4);opacity:0;transform:translateY(8px);transition:opacity .25s,transform .25s;
  max-width:300px;text-align:center;
}
.toast-pill.show{opacity:1;transform:translateY(0);}
'''

SCRIPT = '''
function showScreen(id){
  document.querySelectorAll(".screen").forEach(function(s){ s.classList.remove("active"); });
  var el = document.getElementById("screen-" + id);
  if(el){ el.classList.add("active"); el.scrollTop = 0; }
  document.querySelectorAll(".qn-pill").forEach(function(p){ p.classList.toggle("active", p.dataset.target === id); });
}
function pickChoice(el, cls){
  var scope = el.closest(".choice-group") || el.parentElement;
  scope.querySelectorAll("." + cls).forEach(function(s){ s.classList.remove("active"); });
  el.classList.add("active");
}
function toast(msg){
  var host = document.getElementById("toast-host");
  if(!host) return;
  var t = document.createElement("div");
  t.className = "toast-pill";
  t.textContent = msg;
  host.appendChild(t);
  requestAnimationFrame(function(){ t.classList.add("show"); });
  setTimeout(function(){
    t.classList.remove("show");
    setTimeout(function(){ t.remove(); }, 300);
  }, 2200);
}
function confirmBooking(){
  toast("Booking berhasil dikonfirmasi! Menuju beranda...");
  setTimeout(function(){ showScreen("home"); }, 1300);
}
function setTarif(el, mode){
  pickChoice(el, "tarif-opt");
  var wrap = document.getElementById("harga-wrap");
  if(wrap){ wrap.className = wrap.className.replace(/\\b(umum|spes)\\b/, mode); }
}
function pickJadwal(el, key){
  pickChoice(el, "jad-opt");
  document.querySelectorAll(".jad-pane").forEach(function(p){
    p.classList.toggle("active", p.dataset.jad === key);
  });
}
function pickUsia(el, idx){
  pickChoice(el, "usia-opt");
  document.querySelectorAll(".usia-pane").forEach(function(p, i){
    p.classList.toggle("active", i === idx);
  });
}
function pickDokter(el, harga){
  pickChoice(el, "dok-opt");
  var teks = "Rp" + harga.toLocaleString("id-ID");
  document.querySelectorAll(".est-line, .est-total").forEach(function(n){ n.textContent = teks; });
}
setTimeout(function(){
  var splash = document.getElementById("screen-splash");
  if(splash && splash.classList.contains("active")){ showScreen("onboarding"); }
}, 3200);
'''

HTML = f'''<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VaksinKu App</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{STYLE}</style>
</head>
<body>
<div class="stage">
  <div class="col" style="align-items:center;gap:10px;">
    <div class="stage-label">Prototipe interaktif · navigasi cepat</div>
    <div class="qn-row">{quicknav_html}</div>
  </div>
  <div class="phone-bezel">
    <div class="phone-mask">
      {splash}
      {onboarding}
      {login}
      {home}
      {booking}
      {rekammedis}
      {chat}
      {profile}
      {korporat}
      {harga}
      {jadwal}
      {paket}
      {tentang}
      <div id="toast-host"></div>
    </div>
  </div>
</div>
<script>{SCRIPT}</script>
</body>
</html>
'''

OUT_PATH = os.path.join(HERE, "vaksinku-app.html")
with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", OUT_PATH, len(HTML))
