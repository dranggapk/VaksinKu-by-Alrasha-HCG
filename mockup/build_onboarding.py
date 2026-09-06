import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from gen import icon, logo_full, logo_mark, navbar, write

def need_card(ic, title, sub, selected=False):
    border = "1.6px solid var(--magenta)" if selected else "1.4px solid var(--line)"
    bg = "var(--magenta-tint)" if selected else "#fff"
    iconbg = "var(--magenta)" if selected else "var(--teal-tint)"
    iconcolor = "#fff" if selected else "var(--teal-dark)"
    check = f'<div style="position:absolute;top:10px;right:10px;">{icon("check-c",16,"var(--magenta)")}</div>' if selected else ""
    return f'''
    <div style="position:relative;border:{border};background:{bg};border-radius:18px;padding:16px 14px;display:flex;flex-direction:column;gap:10px;">
      {check}
      <div style="width:42px;height:42px;border-radius:50%;background:{iconbg};display:flex;align-items:center;justify-content:center;">
        {icon(ic,22,iconcolor)}
      </div>
      <div>
        <div style="font-weight:700;font-size:14px;">{title}</div>
        <div style="font-size:11.5px;color:var(--ink-3);margin-top:2px;line-height:1.4;">{sub}</div>
      </div>
    </div>'''

illustration = f'''
<div style="height:230px;border-radius:24px;background:linear-gradient(160deg,var(--teal-tint) 0%,var(--magenta-tint) 100%);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;">
  <div style="position:absolute;top:18px;left:18px;width:34px;height:34px;border-radius:50%;background:#fff;opacity:.6;"></div>
  <div style="position:absolute;bottom:22px;right:26px;width:20px;height:20px;border-radius:50%;background:#fff;opacity:.5;"></div>
  <svg width="180" height="150" viewBox="0 0 180 150" fill="none">
    <circle cx="60" cy="46" r="22" fill="#56C3C7"/>
    <circle cx="120" cy="46" r="22" fill="#D11972" opacity="0.85"/>
    <circle cx="90" cy="60" r="17" fill="#2E9BA0"/>
    <path d="M20 140c8-34 30-52 55-52s45 16 52 52" stroke="#56C3C7" stroke-width="6" fill="none" stroke-linecap="round"/>
    <path d="M95 140c6-24 20-36 40-36s32 12 38 36" stroke="#D11972" stroke-width="6" fill="none" stroke-linecap="round" opacity="0.85"/>
  </svg>
</div>
'''

body = f'''
<div class="col" style="padding:22px 20px 0;">
  <div class="row" style="justify-content:flex-end;">
    <span style="font-size:13px;font-weight:700;color:var(--ink-3);">Lewati</span>
  </div>
  <div style="height:14px;"></div>
  {illustration}
  <div style="height:22px;"></div>
  <div class="disp" style="font-size:21px;font-weight:800;color:var(--ink);">Pilih kebutuhan vaksinasi Anda</div>
  <div style="font-size:13px;color:var(--ink-3);margin-top:6px;line-height:1.55;">
    VaksinKu menyesuaikan rekomendasi &amp; paket berdasarkan kebutuhan keluarga Anda.
  </div>
  <div style="height:18px;"></div>
  <div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;">
    {need_card("family","Vaksin Anak","Imunisasi dasar &amp; lanjutan",True)}
    {need_card("user","Vaksin Dewasa","HPV, flu, tifoid, dll")}
    {need_card("plane","Umroh &amp; Haji","Meningitis wajib jamaah")}
    {need_card("heart","Lansia","Influenza, pneumonia")}
  </div>
</div>
<div class="grow"></div>
<div style="padding:18px 20px 26px;display:flex;flex-direction:column;gap:12px;">
  <div class="row" style="justify-content:center;gap:7px;">
    <div style="width:7px;height:7px;border-radius:50%;background:var(--line);"></div>
    <div style="width:18px;height:7px;border-radius:4px;background:var(--magenta);"></div>
    <div style="width:7px;height:7px;border-radius:50%;background:var(--line);"></div>
  </div>
  <button class="btn btn-primary">Lanjutkan {icon("chevron",16,"#fff")}</button>
</div>
'''
write("Onboarding", body)
