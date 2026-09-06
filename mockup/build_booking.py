import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from gen import icon, logo_full, logo_mark, navbar, write

hdr = f'''
<div class="hdr-bar">
  {icon("chevron",20,"#fff")}
  <div class="disp">Booking Vaksinasi</div>
</div>
'''

def service_chip(ic, label, selected=False):
    border = "1.6px solid var(--magenta)" if selected else "1.4px solid var(--line)"
    bg = "var(--magenta-tint)" if selected else "#fff"
    color = "var(--magenta-dark)" if selected else "var(--ink-2)"
    iconcolor = "var(--magenta-dark)" if selected else "var(--teal-dark)"
    return f'''<div style="flex:1;border:{border};background:{bg};border-radius:16px;padding:14px 8px;display:flex;flex-direction:column;align-items:center;gap:6px;">
      {icon(ic,20,iconcolor)}<span style="font-size:11.5px;font-weight:700;color:{color};text-align:center;">{label}</span>
    </div>'''

section1 = f'''
<div class="section" style="padding-bottom:6px;">
  <span class="label">Pilih Layanan<span class="req">*</span></span>
  <div class="row" style="gap:10px;">
    {service_chip("doc","Vaksinasi",True)}
    {service_chip("chat","Konsultasi")}
    {service_chip("chart","Cek Tumbuh Kembang")}
  </div>
</div>
'''

section2 = f'''
<div class="section" style="padding-top:14px;padding-bottom:6px;">
  <span class="label">Data Pendaftar<span class="req">*</span></span>
  <span class="hint">Data pendaftar akan digunakan sebagai penerima invoice.</span>
  <input class="input" value="Angga Perdana" style="margin-bottom:12px;" readonly>
  <div class="row" style="gap:10px;margin-bottom:12px;">
    <div style="flex:1;text-align:center;padding:12px;border-radius:14px;border:1.4px solid var(--line);font-size:13px;color:var(--ink-3);font-weight:600;">Perempuan</div>
    <div style="flex:1;text-align:center;padding:12px;border-radius:14px;border:1.6px solid var(--magenta);background:var(--magenta-tint);font-size:13px;color:var(--magenta-dark);font-weight:700;">Laki-laki</div>
  </div>
  <input class="input" placeholder="Nomor HP aktif">
</div>
'''

section3 = f'''
<div class="section" style="padding-top:14px;padding-bottom:6px;">
  <span class="label">Lokasi Layanan<span class="req">*</span></span>
  <div class="row" style="gap:10px;margin-bottom:10px;">
    <div style="flex:1;border:1.6px solid var(--magenta);background:var(--magenta-tint);border-radius:16px;padding:14px;display:flex;flex-direction:column;align-items:center;gap:6px;">
      {icon("house",20,"var(--magenta-dark)")}<span style="font-size:12.5px;font-weight:700;color:var(--magenta-dark);">Di Rumah</span>
    </div>
    <div style="flex:1;border:1.4px solid var(--line);border-radius:16px;padding:14px;display:flex;flex-direction:column;align-items:center;gap:6px;">
      {icon("pin",20,"var(--teal-dark)")}<span style="font-size:12.5px;font-weight:700;color:var(--ink-2);">Klinik Terdekat</span>
    </div>
  </div>
  <div class="row" style="align-items:center;gap:10px;background:var(--teal-tint);border-radius:14px;padding:12px 14px;">
    {icon("pin",16,"var(--teal-dark)")}
    <span class="grow" style="font-size:12.5px;color:var(--ink-2);">Jl. Gurame No. 5, Lengkong, Kota Bandung</span>
    <span style="font-size:12px;font-weight:700;color:var(--magenta-dark);">Ubah</span>
  </div>
</div>
'''

section4 = f'''
<div class="section" style="padding-top:14px;padding-bottom:6px;">
  <div class="row" style="align-items:center;gap:8px;margin-bottom:2px;">
    <span class="label" style="margin-bottom:0;">Data Pasien<span class="req">*</span></span>
    <span class="chip chip-teal">Booking untuk keluarga</span>
  </div>
  <span class="hint">Daftar pasien adalah orang yang akan divaksin. Pastikan data sudah benar.</span>
  <div class="col" style="gap:10px;">
    <div class="row" style="align-items:center;gap:12px;border:1.4px solid var(--line);border-radius:14px;padding:12px 14px;">
      <div style="width:34px;height:34px;border-radius:50%;background:var(--teal-tint);display:flex;align-items:center;justify-content:center;font-weight:800;color:var(--teal-dark);font-size:12px;font-family:'Baloo 2';">N</div>
      <div class="col grow" style="gap:1px;">
        <div style="font-weight:700;font-size:13.5px;">Nadia Perdana</div>
        <div style="font-size:11.5px;color:var(--ink-3);">5 tahun · Vaksin Influenza</div>
      </div>
      {icon("chevron",16,"var(--ink-4)")}
    </div>
    <div style="border:1.4px dashed var(--teal);border-radius:14px;padding:12px;display:flex;align-items:center;justify-content:center;gap:8px;color:var(--teal-dark);font-weight:700;font-size:13px;">
      {icon("plus",16,"var(--teal-dark)")} Tambah pasien
    </div>
  </div>
</div>
'''

def slot(label, state):
    styles = {
      "selected": ("var(--magenta)","#fff","1.6px solid var(--magenta)"),
      "available": ("#fff","var(--ink-2)","1.4px solid var(--line)"),
      "full": ("#F5F5F4","var(--ink-4)","1.4px solid var(--line)"),
    }
    bg,color,border = styles[state]
    deco = "text-decoration:line-through;" if state=="full" else ""
    return f'<div style="flex:1;text-align:center;padding:10px 4px;border-radius:12px;background:{bg};border:{border};color:{color};font-size:12px;font-weight:700;{deco}">{label}</div>'

def date_chip(d, w):
    active = d == "12"
    bg = "var(--magenta)" if active else "#fff"
    border = "var(--magenta)" if active else "var(--line)"
    color = "#fff" if active else "var(--ink-2)"
    return (f'<div style="flex:1;text-align:center;padding:10px 2px;border-radius:12px;'
            f'background:{bg};border:1.4px solid {border};color:{color};">'
            f'<div style="font-size:10px;opacity:.8;">{w}</div>'
            f'<div class="disp" style="font-weight:800;font-size:14px;">{d}</div></div>')

date_strip = "".join(date_chip(d, w) for d, w in [("10","Kam"),("11","Jum"),("12","Sab"),("13","Min"),("14","Sen")])

section5 = f'''
<div class="section" style="padding-top:14px;padding-bottom:6px;">
  <span class="label">Jadwal Vaksinasi<span class="req">*</span></span>
  <div class="row" style="gap:8px;margin-bottom:12px;">
    {date_strip}
  </div>
  <div class="row" style="gap:8px;margin-bottom:8px;">
    {slot("09.00","available")}{slot("10.00","selected")}{slot("11.00","full")}
  </div>
  <div class="row" style="gap:8px;">
    {slot("13.00","available")}{slot("14.00","available")}{slot("15.00","full")}
  </div>
</div>
'''

summary = f'''
<div class="section" style="padding-top:14px;">
  <div class="card" style="border:1.4px solid var(--teal);background:var(--teal-tint);">
    <div class="row" style="align-items:center;gap:7px;margin-bottom:12px;">
      {icon("check-c",16,"var(--teal-dark)")}
      <span style="font-size:12px;font-weight:700;color:var(--teal-dark);">Transparan, tanpa biaya tersembunyi</span>
    </div>
    <div class="row" style="justify-content:space-between;margin-bottom:8px;">
      <span style="font-size:13px;color:var(--ink-2);">Vaksin Influenza x1</span>
      <span style="font-size:13px;color:var(--ink);">Rp350.000</span>
    </div>
    <div class="row" style="justify-content:space-between;margin-bottom:8px;">
      <span style="font-size:13px;color:var(--ink-2);">Biaya layanan ke rumah</span>
      <span style="font-size:13px;color:var(--ink);">Rp75.000</span>
    </div>
    <div class="divider" style="margin:10px 0;"></div>
    <div class="row" style="justify-content:space-between;">
      <span style="font-weight:800;font-size:14px;" class="disp">Total Estimasi</span>
      <span style="font-weight:800;font-size:15px;color:var(--magenta-dark);" class="disp">Rp425.000</span>
    </div>
    <div style="font-size:11px;color:var(--ink-3);margin-top:8px;line-height:1.5;">Estimasi dapat menyesuaikan hasil skrining kesehatan di lokasi.</div>
  </div>
</div>
'''

payment = f'''
<div class="section" style="padding-top:2px;">
  <span class="label">Metode Pembayaran<span class="req">*</span></span>
  <div class="row" style="gap:10px;">
    <div style="flex:1;text-align:center;padding:12px 4px;border-radius:14px;border:1.4px solid var(--line);font-size:12px;font-weight:700;color:var(--ink-2);">Transfer Bank</div>
    <div style="flex:1;text-align:center;padding:12px 4px;border-radius:14px;border:1.6px solid var(--magenta);background:var(--magenta-tint);font-size:12px;font-weight:700;color:var(--magenta-dark);">QRIS</div>
    <div style="flex:1;text-align:center;padding:12px 4px;border-radius:14px;border:1.4px solid var(--line);font-size:12px;font-weight:700;color:var(--ink-2);">E-Wallet</div>
  </div>
</div>
'''

footer = f'''
<div style="position:sticky;bottom:0;background:#fff;border-top:1px solid var(--line);padding:14px 20px 20px;display:flex;align-items:center;gap:14px;">
  <div class="col" style="gap:1px;">
    <div style="font-size:10.5px;color:var(--ink-4);">Total estimasi</div>
    <div class="disp" style="font-weight:800;font-size:16px;color:var(--magenta-dark);">Rp425.000</div>
  </div>
  <button class="btn btn-primary grow">Konfirmasi Booking</button>
</div>
'''

body = f'''
{hdr}
{section1}
{section2}
{section3}
{section4}
{section5}
{summary}
{payment}
<div style="height:8px;"></div>
{footer}
'''
write("Booking", body)
