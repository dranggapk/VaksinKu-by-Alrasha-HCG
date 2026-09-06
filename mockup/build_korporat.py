import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from gen import icon, logo_full, logo_mark, navbar, write

hdr = f'''
<div class="hdr-bar" style="flex-direction:column;align-items:flex-start;gap:10px;background:var(--ink);">
  <div class="row" style="align-items:center;gap:14px;width:100%;">
    {icon("chevron",20,"#fff")}
    <div class="col" style="gap:1px;">
      <div class="disp" style="font-size:18px;font-weight:700;">Dashboard Vaksinasi Sekolah</div>
      <div style="font-size:11.5px;opacity:.75;">SDN Melati 02 · Tahun Ajaran 2026/2027</div>
    </div>
  </div>
</div>
'''

tabs = f'''
<div class="row" style="padding:14px 20px 0;gap:22px;border-bottom:1px solid var(--line);">
  <div style="padding-bottom:12px;border-bottom:2.4px solid var(--magenta);color:var(--magenta-dark);font-weight:700;font-size:13px;">Ringkasan</div>
  <div style="padding-bottom:12px;color:var(--ink-3);font-weight:600;font-size:13px;">Peserta</div>
  <div style="padding-bottom:12px;color:var(--ink-3);font-weight:600;font-size:13px;">Laporan</div>
</div>
'''

def stat(value, label, color="var(--ink)"):
    return f'''<div class="card" style="flex:1;padding:14px;text-align:center;">
      <div class="disp" style="font-size:21px;font-weight:800;color:{color};">{value}</div>
      <div style="font-size:10.5px;color:var(--ink-3);margin-top:4px;line-height:1.3;">{label}</div>
    </div>'''

stats = f'''
<div class="row" style="gap:10px;padding:16px 20px 0;">
  {stat("320","Total Peserta")}
  {stat("248","Sudah Divaksin","var(--teal-dark)")}
  {stat("77%","Coverage","var(--magenta-dark)")}
</div>
'''

bulk_btn = f'''
<div style="padding:16px 20px 0;">
  <button class="btn btn-primary" style="width:100%;">{icon("plus",16,"#fff")} Booking Massal (Bulk)</button>
</div>
'''

def coverage_row(cls, pct, color):
    return f'''<div class="col" style="gap:6px;">
      <div class="row" style="justify-content:space-between;">
        <span style="font-size:12.5px;font-weight:700;">{cls}</span>
        <span style="font-size:12px;font-weight:700;color:{color};">{pct}%</span>
      </div>
      <div style="height:7px;border-radius:5px;background:#F1F1F0;overflow:hidden;">
        <div style="width:{pct}%;height:100%;background:{color};"></div>
      </div>
    </div>'''

coverage_card = f'''
<div class="card">
  <div style="font-weight:700;font-size:14.5px;margin-bottom:14px;">Cakupan per Kelas</div>
  <div class="col" style="gap:14px;">
    {coverage_row("Kelas 1A","92","var(--teal-dark)")}
    {coverage_row("Kelas 1B","65","#C8890F")}
    {coverage_row("Kelas 2A","100","var(--teal-dark)")}
    {coverage_row("Kelas 2B","58","#C8890F")}
  </div>
</div>
'''

report_card = f'''
<div class="card">
  <div class="row" style="align-items:center;gap:12px;">
    <div style="width:40px;height:40px;border-radius:12px;background:var(--teal-tint);display:flex;align-items:center;justify-content:center;">{icon("upload",19,"var(--teal-dark)")}</div>
    <div class="col grow" style="gap:1px;">
      <div style="font-weight:700;font-size:13.5px;">Laporan &amp; Kepatuhan</div>
      <div style="font-size:11.5px;color:var(--ink-3);">Format sesuai standar BIAS</div>
    </div>
  </div>
  <button class="btn btn-outline" style="width:100%;margin-top:14px;padding:12px;font-size:13px;">{icon("download",15,"var(--teal-dark)")} Unduh Laporan untuk Dinas Kesehatan</button>
</div>
'''

invoice_card = f'''
<div class="card">
  <div class="row" style="align-items:center;">
    <div style="font-weight:700;font-size:14.5px;">Invoice &amp; Termin</div>
    <div class="grow"></div>
    <span class="chip chip-amber">Jatuh Tempo 15 Sep</span>
  </div>
  <div class="row" style="align-items:center;margin-top:12px;">
    <div class="col" style="gap:2px;">
      <div style="font-size:12px;color:var(--ink-3);">INV-2026-0142</div>
      <div class="disp" style="font-weight:800;font-size:17px;">Rp48.000.000</div>
    </div>
    <div class="grow"></div>
    <button class="btn btn-outline-mag" style="padding:10px 16px;font-size:12.5px;">Lihat Invoice</button>
  </div>
</div>
'''

body = f'''
{hdr}
{tabs}
{stats}
{bulk_btn}
<div class="col" style="padding:16px 20px 24px;gap:14px;">
  {coverage_card}
  {report_card}
  {invoice_card}
</div>
'''
write("Korporat", body)
