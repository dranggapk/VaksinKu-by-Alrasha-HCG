import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from gen import icon, logo_full, logo_mark, navbar, write

hdr = f'''
<div class="hdr-bar">
  {icon("chevron",20,"#fff")}
  <div class="disp">Rekam Medis</div>
</div>
'''

patient_tabs = f'''
<div class="row" style="gap:8px;padding:16px 20px 4px;">
  <div style="padding:8px 14px;border-radius:999px;background:var(--magenta);color:#fff;font-size:12.5px;font-weight:700;">Nadia (5 th)</div>
  <div style="padding:8px 14px;border-radius:999px;border:1.4px solid var(--line);color:var(--ink-2);font-size:12.5px;font-weight:700;">Angga Perdana</div>
  <div style="padding:8px 12px;border-radius:999px;border:1.4px dashed var(--teal);color:var(--teal-dark);font-size:12.5px;font-weight:700;">{icon("plus",13,"var(--teal-dark)")}</div>
</div>
'''

qr = '<svg width="52" height="52" viewBox="0 0 10 10"><rect width="10" height="10" fill="#fff"/>' + "".join(
    f'<rect x="{x}" y="{y}" width="1" height="1" fill="#262626"/>'
    for x, y in [(0,0),(1,0),(2,0),(0,1),(2,1),(0,2),(1,2),(2,2),(4,0),(5,1),(4,3),(7,0),(8,0),(9,0),(7,1),(9,1),(7,2),(8,2),(9,2),(4,5),(5,6),(4,7),(0,7),(1,7),(2,7),(0,8),(2,8),(0,9),(1,9),(2,9),(6,7),(7,7),(8,7),(6,9),(8,9),(7,8),(5,4),(6,5),(8,5)]
) + '</svg>'

vax_card = f'''
<div class="card" style="padding:0;overflow:hidden;">
  <div style="background:linear-gradient(120deg,var(--teal) 0%,var(--magenta) 130%);height:8px;"></div>
  <div style="padding:18px;">
    <div class="row" style="align-items:center;">
      <div class="disp" style="font-weight:800;font-size:14px;">Kartu Vaksinasi Digital</div>
      <div class="grow"></div>
      <span class="chip chip-teal">Aktif</span>
    </div>
    <div class="row" style="align-items:center;gap:14px;margin-top:14px;">
      <div class="col grow" style="gap:3px;">
        <div style="font-weight:800;font-size:15px;">Nadia Perdana</div>
        <div style="font-size:12px;color:var(--ink-3);">Lahir 12 Mei 2021 · Perempuan</div>
        <div style="font-size:11.5px;color:var(--ink-4);margin-top:4px;">No. Kartu: VK-2026-004821</div>
      </div>
      <div style="border:1px solid var(--line);border-radius:10px;padding:4px;">{qr}</div>
    </div>
    <div style="font-size:11px;color:var(--ink-3);margin-top:12px;line-height:1.5;">Berlaku untuk syarat sekolah &amp; keperluan imigrasi (Umroh/Haji).</div>
    <div class="row" style="gap:10px;margin-top:14px;">
      <button class="btn btn-outline" style="flex:1;padding:11px;font-size:13px;">{icon("download",15,"var(--teal-dark)")} Unduh PDF</button>
      <button class="btn btn-outline" style="flex:1;padding:11px;font-size:13px;">{icon("share",15,"var(--teal-dark)")} Bagikan</button>
    </div>
  </div>
</div>
'''

def vax_chip(label, state):
    m = {
      "done": ("var(--green-tint)","var(--green)","check-c"),
      "soon": ("var(--amber-tint)","#9C6B0E","clock"),
      "todo": ("#F1F1F0","var(--ink-3)","circle-o"),
    }
    bg,color,ic = m[state]
    return f'<div style="background:{bg};border-radius:12px;padding:8px 10px;display:flex;align-items:center;gap:6px;"><span style="color:{color};">{icon(ic,14,color)}</span><span style="font-size:11.5px;font-weight:700;color:{color};">{label}</span></div>'

idl_card = f'''
<div class="card">
  <div class="row" style="align-items:center;">
    <div style="font-weight:700;font-size:14.5px;">Status Kelengkapan Imunisasi (IDL)</div>
  </div>
  <div class="row" style="align-items:center;gap:10px;margin-top:12px;">
    <div style="flex:1;height:8px;border-radius:6px;background:#F1F1F0;overflow:hidden;">
      <div style="width:67%;height:100%;background:var(--teal);"></div>
    </div>
    <span style="font-size:12.5px;font-weight:800;color:var(--teal-dark);">67%</span>
  </div>
  <div style="height:12px;"></div>
  <div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;">
    {vax_chip("HB0","done")}{vax_chip("BCG","done")}
    {vax_chip("Polio 1","done")}{vax_chip("DPT-HB-Hib 1","soon")}
    {vax_chip("Campak","todo")}{vax_chip("Polio 2","todo")}
  </div>
</div>
'''

# simple SVG growth chart
chart_svg = f'''
<svg width="100%" height="150" viewBox="0 0 320 150" preserveAspectRatio="none">
  <polygon points="0,150 0,90 320,40 320,150" fill="#E9F9FA"/>
  <polyline points="0,120 60,105 120,88 180,70 240,55 320,42" fill="none" stroke="#BFE9EA" stroke-width="2"/>
  <polyline points="0,138 60,128 120,116 180,102 240,90 320,78" fill="none" stroke="#BFE9EA" stroke-width="2"/>
  <polyline points="0,108 60,86 120,66 180,50 240,36 320,26" fill="none" stroke="#F6D3E4" stroke-width="2"/>
  <polyline points="0,130 60,112 120,94 180,80 240,64 320,52" fill="none" stroke="#56C3C7" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="0" cy="130" r="4" fill="#2E9BA0"/><circle cx="60" cy="112" r="4" fill="#2E9BA0"/>
  <circle cx="120" cy="94" r="4" fill="#2E9BA0"/><circle cx="180" cy="80" r="4" fill="#2E9BA0"/>
  <circle cx="240" cy="64" r="4" fill="#2E9BA0"/><circle cx="320" cy="52" r="5" fill="#D11972"/>
</svg>
'''

growth_card = f'''
<div class="card">
  <div class="row" style="align-items:center;">
    <div style="font-weight:700;font-size:14.5px;">Grafik Tumbuh Kembang</div>
    <div class="grow"></div>
    <span class="row" style="gap:5px;align-items:center;font-size:11px;color:var(--ink-3);"><span style="width:8px;height:8px;border-radius:50%;background:var(--teal-dark);display:inline-block;"></span>Berat badan</span>
  </div>
  <div style="margin-top:10px;">{chart_svg}</div>
  <div class="row" style="gap:8px;margin-top:14px;">
    <div class="chip chip-teal" style="flex:1;justify-content:center;">Berat 12.4kg</div>
    <div class="chip chip-teal" style="flex:1;justify-content:center;">Tinggi 92cm</div>
    <div class="chip chip-teal" style="flex:1;justify-content:center;">Kepala 47cm</div>
  </div>
  <button class="btn btn-outline" style="width:100%;margin-top:14px;padding:12px;font-size:13px;">Update Data Pertumbuhan</button>
</div>
'''

def history_row(date, title, sub):
    return f'''<div class="row" style="align-items:center;gap:12px;padding:12px 0;">
      <div style="width:40px;height:40px;border-radius:12px;background:var(--magenta-tint);display:flex;align-items:center;justify-content:center;flex-shrink:0;">{icon("doc",18,"var(--magenta-dark)")}</div>
      <div class="col grow" style="gap:1px;">
        <div style="font-weight:700;font-size:13px;">{title}</div>
        <div style="font-size:11.5px;color:var(--ink-3);">{sub}</div>
      </div>
      <div class="col" style="align-items:flex-end;gap:2px;">
        <span style="font-size:11px;color:var(--ink-4);">{date}</span>
        {icon("chevron",14,"var(--ink-4)")}
      </div>
    </div>'''

history_card = f'''
<div class="card">
  <div style="font-weight:700;font-size:14.5px;margin-bottom:4px;">Riwayat Vaksinasi</div>
  <div class="divider"></div>
  {history_row("2 Sep 2026","Vaksin Varicella (dosis 1)","dr. Melati Anggraini · Di Rumah")}
  <div class="divider"></div>
  {history_row("14 Jul 2026","Vaksin Tifoid","dr. Melati Anggraini · Klinik Sunter")}
  <div class="divider"></div>
  {history_row("2 Mar 2026","Vaksin DPT-HB-Hib 3","dr. Bagas Wirawan · Di Rumah")}
</div>
'''

body = f'''
{hdr}
{patient_tabs}
<div class="col" style="padding:10px 20px 12px;gap:14px;">
  {vax_card}
  {idl_card}
  {growth_card}
  {history_card}
</div>
<div class="grow"></div>
{navbar("doc")}
'''
write("RekamMedis", body)
