import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from gen import icon, logo_full, logo_mark, navbar, write

header = f'''
<div style="background:linear-gradient(120deg,var(--teal-tint) 0%,var(--magenta-tint) 100%);border-radius:0 0 28px 28px;padding:20px 20px 26px;">
  <div class="row" style="align-items:center;gap:10px;">
    {logo_mark(22)}
    <div class="grow"></div>
    <div class="chip chip-amber">{icon("coin",14,"#9C6B0E")} 128 Poin</div>
    <div class="iconbtn">{icon("bell",18,"var(--ink-2)")}</div>
    <div class="iconbtn">{icon("doc",17,"var(--ink-2)")}</div>
  </div>
  <div style="height:18px;"></div>
  <div class="disp" style="font-size:19px;font-weight:800;">Halo, Keluarga Perdana</div>
  <div style="font-size:12.5px;color:var(--ink-2);margin-top:4px;">Yuk pastikan imunisasi keluarga selalu tepat waktu.</div>
</div>
'''

booking_card = f'''
<div class="card">
  <div class="row" style="align-items:center;gap:8px;">
    <span class="chip chip-mag">Booking Aktif</span>
    <div class="grow"></div>
    <span style="font-size:11.5px;color:var(--ink-4);">#VK-88213</span>
  </div>
  <div style="height:12px;"></div>
  <div class="row" style="gap:12px;align-items:center;">
    <div style="width:44px;height:44px;border-radius:50%;background:var(--teal-tint);display:flex;align-items:center;justify-content:center;font-weight:800;color:var(--teal-dark);font-family:'Baloo 2';">AP</div>
    <div class="col" style="gap:2px;">
      <div style="font-weight:700;font-size:14.5px;">Vaksin Influenza — Nadia</div>
      <div style="font-size:12px;color:var(--ink-3);">dr. Melati Anggraini, Sp.A</div>
    </div>
  </div>
  <div style="height:14px;"></div>
  <div class="row" style="gap:16px;">
    <div class="row" style="gap:6px;align-items:center;">{icon("calendar",15,"var(--teal-dark)")}<span style="font-size:12px;color:var(--ink-2);">Sab, 12 Sep • 10.00</span></div>
    <div class="row" style="gap:6px;align-items:center;">{icon("house",15,"var(--teal-dark)")}<span style="font-size:12px;color:var(--ink-2);">Di Rumah</span></div>
  </div>
  <div class="divider" style="margin:14px 0;"></div>
  <div class="row" style="gap:10px;">
    <button class="btn btn-outline" style="flex:1;padding:11px;font-size:13px;">Lihat Detail</button>
    <button style="flex:1;background:transparent;border:none;color:var(--magenta-dark);font-weight:700;font-size:13px;font-family:'Baloo 2';">Reschedule</button>
  </div>
</div>
'''

reminder_card = f'''
<div class="card row" style="gap:14px;align-items:flex-start;">
  <div style="width:42px;height:42px;border-radius:14px;background:var(--magenta-tint);display:flex;align-items:center;justify-content:center;flex-shrink:0;">
    {icon("calendar",20,"var(--magenta-dark)")}
  </div>
  <div class="col" style="gap:4px;">
    <div style="font-weight:700;font-size:14px;">Reminder jadwal berikutnya</div>
    <div style="font-size:12.5px;color:var(--ink-2);">Varicella (dosis ke-2) — 3 minggu lagi</div>
    <div style="font-size:11px;color:var(--ink-4);margin-top:2px;">Reminder otomatis H-7, H-1, dan H-1 jam.</div>
  </div>
</div>
'''

growth_card = f'''
<div class="card">
  <div class="row" style="align-items:center;">
    <div style="font-weight:700;font-size:14.5px;">Tumbuh Kembang &amp; Kelengkapan Vaksinasi</div>
    <div class="grow"></div>
    {icon("chevron",16,"var(--ink-4)")}
  </div>
  <div style="height:12px;"></div>
  <div class="row" style="gap:8px;">
    <div class="chip chip-teal" style="flex:1;justify-content:center;">Berat 8.5kg · Normal</div>
    <div class="chip chip-teal" style="flex:1;justify-content:center;">Tinggi 68cm · Normal</div>
  </div>
</div>
'''

seasonal_banner = f'''
<div style="border-radius:20px;padding:20px;background:linear-gradient(135deg,var(--teal-dark) 0%,var(--magenta-dark) 130%);color:#fff;position:relative;overflow:hidden;">
  <div style="position:absolute;right:-30px;top:-30px;width:130px;height:130px;border-radius:50%;background:rgba(255,255,255,.08);"></div>
  <div style="position:absolute;right:20px;bottom:-40px;width:90px;height:90px;border-radius:50%;background:rgba(255,255,255,.08);"></div>
  <div style="position:relative;">
    <div class="disp" style="font-size:17px;font-weight:800;">Musim Umroh &amp; Haji</div>
    <div style="font-size:12.5px;opacity:.9;margin-top:4px;line-height:1.5;">Vaksin Meningitis wajib jamaah, siap sebelum berangkat.</div>
    <div class="row" style="gap:8px;margin-top:12px;flex-wrap:wrap;">
      <span style="background:rgba(255,255,255,.18);border-radius:999px;padding:5px 11px;font-size:11px;font-weight:700;">Meningitis</span>
      <span style="background:rgba(255,255,255,.18);border-radius:999px;padding:5px 11px;font-size:11px;font-weight:700;">Influenza</span>
      <span style="background:rgba(255,255,255,.18);border-radius:999px;padding:5px 11px;font-size:11px;font-weight:700;">Tifoid</span>
    </div>
  </div>
</div>
'''

def info_col(ic, label):
    return f'''
    <div class="col" style="align-items:center;gap:8px;flex:1;">
      <div style="width:46px;height:46px;border-radius:14px;background:var(--teal-tint);display:flex;align-items:center;justify-content:center;">
        {icon(ic,21,"var(--teal-dark)")}
      </div>
      <div style="font-size:11.5px;font-weight:700;text-align:center;line-height:1.3;">{label}</div>
    </div>'''

info_row = f'''
<div class="card row" style="gap:8px;">
  {info_col("doc","Price List")}
  {info_col("gift","Paket Vaksinasi")}
  {info_col("search","Artikel Edukasi")}
</div>
'''

corp_teaser = f'''
<div class="card row" style="align-items:center;gap:14px;background:var(--teal-tint);border-color:transparent;">
  <div style="width:42px;height:42px;border-radius:12px;background:#fff;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
    {icon("building",20,"var(--teal-dark)")}
  </div>
  <div class="col grow" style="gap:2px;">
    <div style="font-weight:700;font-size:13.5px;">Mitra Institusi?</div>
    <div style="font-size:11.5px;color:var(--ink-2);">Booking massal vaksinasi sekolah &amp; kantor</div>
  </div>
  <div class="chip chip-mag">Pelajari</div>
</div>
'''

body = f'''
{header}
<div class="col" style="padding:18px 20px 12px;gap:14px;">
  {booking_card}
  {reminder_card}
  {growth_card}
  {seasonal_banner}
  {info_row}
  {corp_teaser}
</div>
<div class="grow"></div>
{navbar("home")}
'''
write("Main", body)
