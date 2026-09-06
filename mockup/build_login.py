import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from gen import icon, logo_full, logo_mark, navbar, write

google_g = '''<svg width="19" height="19" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.4 0 6.4 1.2 8.8 3.5l6.5-6.5C35.3 2.6 30 0 24 0 14.6 0 6.5 5.4 2.6 13.2l7.6 5.9C12.1 13 17.5 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.2-.4-4.7H24v9h12.7c-.5 3-2.2 5.5-4.7 7.2l7.3 5.7c4.3-4 6.8-9.9 6.8-17.2z"/><path fill="#FBBC05" d="M10.2 19.1a14.5 14.5 0 0 0 0 9.8l-7.6 5.9a24 24 0 0 1 0-21.6l7.6 5.9z"/><path fill="#34A853" d="M24 48c6 0 11.3-2 15-5.4l-7.3-5.7c-2 1.4-4.7 2.2-7.7 2.2-6.5 0-12-4.4-13.8-10.3l-7.6 5.9C6.5 42.6 14.6 48 24 48z"/></svg>'''

body = f'''
<div class="col grow" style="padding:0 30px;align-items:center;justify-content:center;min-height:844px;">
  <div style="display:flex;flex-direction:column;align-items:center;gap:8px;margin-bottom:38px;">
    {logo_mark(46)}
  </div>
  <div class="disp" style="font-size:21px;font-weight:800;text-align:center;">Masuk untuk mulai vaksinasi</div>
  <div style="font-size:13px;color:var(--ink-3);text-align:center;margin-top:8px;line-height:1.6;">
    Kelola jadwal, rekam medis, dan keluarga Anda dalam satu akun VaksinKu.
  </div>
  <div style="height:34px;"></div>
  <div class="col" style="width:100%;gap:12px;">
    <button class="btn" style="background:#fff;border:1.4px solid var(--line);color:var(--ink);">
      {google_g} Lanjutkan dengan Google
    </button>
    <button class="btn btn-primary">
      {icon("phone",17,"#fff")} Lanjutkan dengan Nomor HP
    </button>
  </div>
  <div style="font-size:11.5px;color:var(--ink-4);text-align:center;margin-top:22px;line-height:1.6;">
    Dengan melanjutkan, Anda menyetujui Syarat &amp; Ketentuan serta Kebijakan Privasi VaksinKu.
  </div>
</div>
<div class="col" style="align-items:center;gap:6px;padding-bottom:26px;">
  <div style="font-size:12.5px;color:var(--ink-3);">Butuh bantuan? WhatsApp <span style="color:var(--magenta-dark);font-weight:700;">[Nomor CS VaksinKu]</span></div>
  <div style="font-size:11px;color:var(--ink-4);">Versi 1.0.0 (Konsep)</div>
</div>
'''
write("Login", body)
