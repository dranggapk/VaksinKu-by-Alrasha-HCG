import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from gen import icon, logo_full, logo_mark, navbar, write

# ---------------- 1. SPLASH ----------------
body = f'''
<div style="position:relative;flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;overflow:hidden;min-height:844px;">
  <div style="position:absolute;top:-90px;left:-110px;width:320px;height:320px;border-radius:50%;background:var(--teal-tint2);filter:blur(2px);"></div>
  <div style="position:absolute;bottom:-120px;right:-100px;width:360px;height:360px;border-radius:50%;background:var(--magenta-tint2);filter:blur(2px);"></div>
  <div style="position:relative;display:flex;flex-direction:column;align-items:center;gap:26px;padding:0 40px;">
    {logo_full(260)}
    <div class="disp" style="font-size:26px;font-weight:800;color:var(--ink);text-align:center;line-height:1.25;">
      #VaksinKeluargaJadiMudah
    </div>
    <div style="font-size:14px;color:var(--ink-3);text-align:center;line-height:1.6;max-width:270px;">
      Booking, rekam medis, dan konsultasi vaksinasi keluarga dalam satu aplikasi.
    </div>
  </div>
  <div style="position:absolute;bottom:34px;display:flex;gap:7px;">
    <div style="width:7px;height:7px;border-radius:50%;background:var(--teal);"></div>
    <div style="width:7px;height:7px;border-radius:50%;background:var(--teal);opacity:.4;"></div>
    <div style="width:7px;height:7px;border-radius:50%;background:var(--magenta);opacity:.4;"></div>
  </div>
</div>
'''
write("Splash", body)
