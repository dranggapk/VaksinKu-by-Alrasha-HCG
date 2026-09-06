import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from gen import icon, logo_full, logo_mark, navbar, write

header = f'''
<div style="background:linear-gradient(120deg,var(--teal-tint) 0%,var(--magenta-tint) 100%);border-radius:0 0 28px 28px;padding:24px 20px 22px;">
  <div class="row" style="align-items:center;gap:14px;">
    <div style="width:60px;height:60px;border-radius:50%;background:linear-gradient(135deg,var(--teal),var(--magenta));display:flex;align-items:center;justify-content:center;">
      <div style="width:54px;height:54px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;">
        <span class="disp" style="font-weight:800;font-size:18px;color:var(--ink-2);">AP</span>
      </div>
    </div>
    <div class="col" style="gap:3px;">
      <div class="disp" style="font-weight:800;font-size:17px;">Angga Perdana</div>
      <div style="font-size:12px;color:var(--ink-3);">dr.angga.pk@gmail.com</div>
      <div style="font-size:12px;font-weight:700;color:var(--magenta-dark);margin-top:2px;">Edit Profil ›</div>
    </div>
  </div>
</div>
'''

poin_card = f'''
<div class="card" style="background:var(--amber-tint);border-color:transparent;">
  <div class="row" style="align-items:center;gap:12px;">
    <div style="width:42px;height:42px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;">{icon("coin",22,"#C8890F")}</div>
    <div class="col grow" style="gap:1px;">
      <div class="disp" style="font-weight:800;font-size:16px;">128 Poin Sehat</div>
      <div style="font-size:11.5px;color:#8A6A21;">Setara Rp12.800 potongan booking</div>
    </div>
    {icon("chevron",16,"#8A6A21")}
  </div>
  <div class="divider" style="margin:14px 0;background:rgba(0,0,0,0.06);"></div>
  <div class="row" style="gap:8px;flex-wrap:wrap;">
    <span class="chip" style="background:#fff;color:#8A6A21;">+10 tiap booking</span>
    <span class="chip" style="background:#fff;color:#8A6A21;">+25 ajak keluarga</span>
    <span class="chip" style="background:#fff;color:#8A6A21;">+15 isi ulasan</span>
  </div>
</div>
'''

def row(ic, label, sub=None, mag=False):
    iconbg = "var(--magenta-tint)" if mag else "var(--teal-tint)"
    iconcolor = "var(--magenta-dark)" if mag else "var(--teal-dark)"
    sub_html = f'<div style="font-size:11.5px;color:var(--ink-3);">{sub}</div>' if sub else ""
    return f'''
    <div class="row" style="align-items:center;gap:14px;padding:15px 4px;">
      <div style="width:38px;height:38px;border-radius:11px;background:{iconbg};display:flex;align-items:center;justify-content:center;flex-shrink:0;">{icon(ic,18,iconcolor)}</div>
      <div class="col grow" style="gap:1px;">
        <div style="font-weight:700;font-size:13.5px;">{label}</div>
        {sub_html}
      </div>
      {icon("chevron",16,"var(--ink-4)")}
    </div>'''

menu_card = f'''
<div class="card" style="padding:8px 16px;">
  {row("doc","Rekam Medis")}<div class="divider"></div>
  {row("family","Daftar Pasien","Keluarga & anggota terdaftar")}<div class="divider"></div>
  {row("pin","Daftar Alamat")}<div class="divider"></div>
  {row("chart","Riwayat Transaksi & Invoice")}<div class="divider"></div>
  {row("building","Mitra Institusi","Mode Admin Sekolah / Kantor",mag=True)}<div class="divider"></div>
  {row("doc","Syarat & Ketentuan")}<div class="divider"></div>
  {row("whatsapp","Bantuan","WhatsApp CS VaksinKu")}
</div>
'''

body = f'''
{header}
<div class="col" style="padding:18px 20px 16px;gap:14px;">
  {poin_card}
  {menu_card}
  <div style="text-align:center;font-size:11px;color:var(--ink-4);padding:6px 0 2px;">Versi 1.0.0 (Konsep)</div>
</div>
<div class="grow"></div>
{navbar("user")}
'''
write("Profile", body)
