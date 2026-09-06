import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from gen import icon, logo_full, logo_mark, navbar, write

hdr = f'''
<div style="padding:20px 20px 14px;">
  <div class="disp" style="font-size:20px;font-weight:800;">Chat</div>
  <div style="font-size:12.5px;color:var(--ink-3);margin-top:2px;">Konsultasi dokter &amp; bantuan CS</div>
</div>
'''

info_strip = f'''
<div style="margin:0 20px 14px;background:var(--teal-tint);border-radius:14px;padding:12px 14px;display:flex;align-items:center;gap:10px;">
  {icon("clock",16,"var(--teal-dark)")}
  <span style="font-size:11.5px;color:var(--teal-dark);font-weight:600;line-height:1.4;">Dokter online: Senin–Jumat 09.00–17.00 · Sabtu 09.00–12.00</span>
</div>
'''

def chat_row(initials, bg, name, preview, time, badge=None, unread=False, icon_name=None):
    avatar = f'<div style="width:46px;height:46px;border-radius:50%;background:{bg};display:flex;align-items:center;justify-content:center;flex-shrink:0;">'
    if icon_name:
        avatar += icon(icon_name, 20, "#fff")
    else:
        avatar += f'<span class="disp" style="color:#fff;font-weight:800;font-size:14px;">{initials}</span>'
    avatar += '</div>'
    badge_html = f'<span class="chip chip-mag" style="padding:3px 8px;font-size:9.5px;">{badge}</span>' if badge else ""
    dot = '<div style="width:9px;height:9px;border-radius:50%;background:var(--magenta);margin-top:6px;"></div>' if unread else '<div style="width:9px;height:9px;"></div>'
    return f'''
    <div class="row" style="align-items:center;gap:12px;padding:14px 20px;border-bottom:1px solid var(--line);">
      {avatar}
      <div class="col grow" style="gap:3px;min-width:0;">
        <div class="row" style="align-items:center;gap:8px;">
          <span style="font-weight:700;font-size:13.5px;">{name}</span>{badge_html}
        </div>
        <div style="font-size:12px;color:var(--ink-3);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{preview}</div>
      </div>
      <div class="col" style="align-items:flex-end;gap:6px;">
        <span style="font-size:10.5px;color:var(--ink-4);">{time}</span>
        {dot}
      </div>
    </div>'''

rows = (
    chat_row("M", "var(--teal)", "dr. Melati Anggraini, Sp.A", "Baik, silakan lanjutkan jadwal vaksin minggu depan ya Bu.", "09.42", unread=True)
    + chat_row(None, "var(--magenta)", "CS VaksinKu", "Halo! Ada yang bisa dibantu terkait booking Anda?", "Kemarin", badge="24 JAM", icon_name="whatsapp")
    + chat_row("B", "#C7CBCF", "dr. Bagas Wirawan, Sp.PD", "Terima kasih atas kunjungannya!", "2 hari lalu")
)

body = f'''
{hdr}
{info_strip}
<div class="col">
  {rows}
</div>
<div class="grow"></div>
{navbar("chat")}
'''
write("Chat", body)
