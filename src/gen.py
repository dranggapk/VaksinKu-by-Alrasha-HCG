#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generates the VaksinKu mockup .dc.html artboards."""
import os

# artboards are written next to the build script that calls write()
OUT = os.getcwd()

HEAD = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{
  --teal:#56C3C7; --teal-dark:#2E9BA0; --teal-tint:#E9F9FA; --teal-tint2:#D7F2F3;
  --magenta:#D11972; --magenta-dark:#A81260; --magenta-tint:#FDECF3; --magenta-tint2:#FBD9E7;
  --ink:#262626; --ink-2:#4B4B4B; --ink-3:#606060; --ink-4:#9AA0A6;
  --line:#ECECEC; --bg:#FAFAF9; --card:#FFFFFF;
  --amber:#E8A23A; --amber-tint:#FFF3DF;
  --green:#2E9E5B; --green-tint:#E8F7EE;
}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;}
body{background:#EDEDEC;}
a{color:var(--magenta-dark);text-decoration:none;}
a:hover{color:var(--magenta);}
.frame{
  width:390px;background:var(--bg);
  font-family:'Plus Jakarta Sans',-apple-system,BlinkMacSystemFont,sans-serif;
  color:var(--ink);display:flex;flex-direction:column;position:relative;
  min-height:844px;
}
.disp{font-family:'Baloo 2',ui-rounded,sans-serif;}
img{display:block;max-width:100%;}
.row{display:flex;flex-direction:row;}
.col{display:flex;flex-direction:column;}
.grow{flex-grow:1;}
.pill{border-radius:999px;}
.card{
  background:var(--card);border:1px solid var(--line);border-radius:20px;padding:18px;
  box-shadow:0 1px 2px rgba(38,38,38,0.03),0 10px 24px -16px rgba(38,38,38,0.18);
}
.btn{
  font-family:'Baloo 2',ui-rounded,sans-serif;font-weight:700;font-size:15px;
  border-radius:999px;padding:15px 20px;display:flex;align-items:center;justify-content:center;gap:8px;
  border:none;cursor:pointer;
}
.btn-primary{background:var(--magenta);color:#fff;}
.btn-outline{background:#fff;border:1.6px solid var(--teal);color:var(--teal-dark);}
.btn-outline-mag{background:#fff;border:1.6px solid var(--magenta);color:var(--magenta-dark);}
.chip{
  border-radius:999px;padding:6px 12px;font-size:12px;font-weight:700;
  display:inline-flex;align-items:center;gap:5px;white-space:nowrap;
}
.chip-teal{background:var(--teal-tint);color:var(--teal-dark);}
.chip-mag{background:var(--magenta-tint);color:var(--magenta-dark);}
.chip-amber{background:var(--amber-tint);color:#9C6B0E;}
.chip-green{background:var(--green-tint);color:var(--green);}
.chip-gray{background:#F1F1F0;color:var(--ink-3);}
.input{
  width:100%;border:1.4px solid var(--line);border-radius:14px;padding:14px 14px;
  font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;color:var(--ink);background:#fff;
}
.label{font-size:13.5px;font-weight:700;color:var(--ink);margin-bottom:8px;display:block;}
.req{color:var(--magenta);}
.hint{font-size:12px;color:var(--ink-4);margin:2px 0 10px;line-height:1.5;}
.section{padding:20px;}
.hdr-bar{
  background:var(--teal-dark);color:#fff;padding:18px 20px 20px;display:flex;align-items:center;gap:14px;
}
.hdr-bar .disp{font-size:19px;font-weight:700;}
.iconbtn{
  width:38px;height:38px;border-radius:50%;background:#fff;border:1px solid var(--line);
  display:flex;align-items:center;justify-content:center;flex-shrink:0;
}
.divider{height:1px;background:var(--line);width:100%;}
.navbar{
  margin-top:auto;background:#fff;border-top:1px solid var(--line);
  height:78px;display:flex;align-items:center;justify-content:space-around;padding:0 6px;
  position:sticky;bottom:0;
}
.navitem{display:flex;flex-direction:column;align-items:center;gap:4px;color:var(--ink-4);font-size:10.5px;font-weight:600;width:58px;}
.navitem.active{color:var(--magenta-dark);}
.navfab{
  width:56px;height:56px;border-radius:50%;background:var(--magenta);display:flex;align-items:center;
  justify-content:center;margin-top:-30px;box-shadow:0 8px 18px -6px rgba(209,25,114,0.55);border:5px solid #fff;
}
</style>
</helmet>
"""

TAIL = """
</x-dc>
</body>
</html>
"""

# ---------- icon library (24x24, stroke=currentColor) ----------
def icon(name, size=22, color="currentColor", sw=1.8):
    body = ICONS[name]
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'

ICONS = {
"home": '<path d="M4 11.5 12 4l8 7.5"/><path d="M6 10v9a1 1 0 0 0 1 1h4v-6h2v6h4a1 1 0 0 0 1-1v-9"/>',
"chat": '<path d="M4 5h16a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H9l-5 4V6a1 1 0 0 1 1-1Z"/><path d="M8 10h8M8 13h5"/>',
"plus": '<path d="M12 5v14M5 12h14"/>',
"doc": '<path d="M7 3h7l4 4v14a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1Z"/><path d="M14 3v4h4"/><path d="M9 12h6M9 16h6M9 8h2"/>',
"user": '<circle cx="12" cy="8" r="3.6"/><path d="M5 20c1.2-4 4-6 7-6s5.8 2 7 6"/>',
"bell": '<path d="M6 10a6 6 0 0 1 12 0c0 4 1.4 5.4 2 6H4c.6-.6 2-2 2-6Z"/><path d="M10 19a2 2 0 0 0 4 0"/>',
"coin": '<circle cx="12" cy="12" r="8.4"/><path d="M12 8v8M9.4 10.2c0-1.1 1.1-2 2.6-2s2.6.7 2.6 1.8-1 1.6-2.6 2-2.6.9-2.6 2 1.1 1.8 2.6 1.8 2.6-.7 2.6-1.6"/>',
"calendar": '<rect x="4" y="5.5" width="16" height="15" rx="2.2"/><path d="M8 3.5v4M16 3.5v4M4 10h16"/>',
"pin": '<path d="M12 21s7-6.3 7-11.5A7 7 0 0 0 5 9.5C5 14.7 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.4"/>',
"chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
"chevron": '<path d="M9 5l7 7-7 7"/>',
"check-c": '<circle cx="12" cy="12" r="9"/><path d="M8 12.3l2.6 2.6L16.2 9"/>',
"circle-o": '<circle cx="12" cy="12" r="9"/>',
"download": '<path d="M12 4v11"/><path d="M7.5 11.5 12 16l4.5-4.5"/><path d="M5 19.5h14"/>',
"qr": '<rect x="4" y="4" width="6.5" height="6.5" rx="1"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1"/><path d="M14.2 14.2h2.4v2.4h-2.4zM18 14.2h1.8M14.2 18h1.8M18 18h1.8"/>',
"share": '<circle cx="18" cy="5.5" r="2.4"/><circle cx="6" cy="12" r="2.4"/><circle cx="18" cy="18.5" r="2.4"/><path d="M8.2 10.8 15.8 6.7M8.2 13.2l7.6 4.1"/>',
"house": '<path d="M4 11.5 12 4l8 7.5"/><path d="M6 10v9a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1v-9"/><path d="M10 20v-5h4v5"/>',
"clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/>',
"phone": '<path d="M6.5 3.5h3l1.3 4-2 1.3a12 12 0 0 0 5.4 5.4l1.3-2 4 1.3v3a2 2 0 0 1-2.2 2A17 17 0 0 1 4.5 5.7a2 2 0 0 1 2-2.2Z"/>',
"whatsapp": '<path d="M7 17.5 4.5 20l1-3.6A8 8 0 1 1 12 20a8 8 0 0 1-5-1.7Z"/><path d="M8.8 8.6c.2-.5.6-.5.9-.5h.6c.2 0 .5 0 .7.5s.8 1.9.9 2 .2.3 0 .6-.3.4-.5.6-.4.4-.2.8a6 6 0 0 0 2.8 2.5c.4.2.6.1.8-.1s.8-.9 1-1.2.4-.2.7-.1 1.8.8 2.1 1 .5.3.5.5-.1 1-.6 1.6-1.5 1.2-2.2 1.2c-1.9 0-4.4-1.4-5.9-3.4S8.4 9.3 8.8 8.6Z"/>',
"building": '<rect x="5" y="4" width="14" height="17" rx="1.4"/><path d="M9 8h1.6M13.4 8H15M9 12h1.6M13.4 12h1.6M9 16h1.6M13.4 16h1.6"/>',
"upload": '<path d="M12 16V5"/><path d="M7.5 9.5 12 5l4.5 4.5"/><path d="M5 19.5h14"/>',
"family": '<circle cx="8" cy="7.5" r="2.6"/><circle cx="16" cy="7.5" r="2.6"/><circle cx="12" cy="9.5" r="2"/><path d="M3.5 20c.6-2.7 2.2-4.3 4.5-4.3s3.6 1.3 4 3M12 20c.4-1.7 1.5-3 3-3.4M15.5 15.7c2.3 0 3.9 1.6 4.5 4.3"/>',
"cake": '<path d="M12 3v3M9 3v2M15 3v2"/><path d="M5 20v-7a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v7"/><path d="M4 20h16"/><path d="M5 15c1 1 2 1 3 0s2-1 3 0 2 1 3 0 2-1 3 0 2 1 3 0"/>',
"plane": '<path d="M3 13.5 21 6l-7.5 18-2.5-7L3 13.5Z"/>',
"heart": '<path d="M12 20s-7-4.4-9.3-8.9A5 5 0 0 1 12 6.2a5 5 0 0 1 9.3 4.9C19 15.6 12 20 12 20Z"/>',
"search": '<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.3-4.3"/>',
"gift": '<rect x="4" y="9.5" width="16" height="11" rx="1.4"/><path d="M4 13.5h16"/><path d="M12 9.5V21"/><path d="M8.3 9.5C6 9.5 5.5 5.5 8 5c2 0 3.5 2.6 4 4.5 0.5-1.9 2-4.5 4-4.5 2.5.5 2 4.5-.3 4.5"/>',
}

def logo_full(width=220):
    return f'<img src="vaksinku-logo.png" alt="VaksinKu" style="width:{width}px;">'

def logo_mark(height=24):
    return f'<img src="vaksinku-logo-mark.png" alt="VaksinKu" style="height:{height}px;width:auto;">'

def navbar(active):
    items = [("home","Beranda"), ("chat","Chat"), None, ("doc","Rekam Medis"), ("user","Profil")]
    html = '<div class="navbar">'
    for it in items:
        if it is None:
            html += f'<div class="navfab">{icon("plus", 24, "#fff", 2.4)}</div>'
            continue
        key, label = it
        cls = "navitem active" if key == active else "navitem"
        color = "var(--magenta-dark)" if key == active else "var(--ink-4)"
        html += f'<div class="{cls}">{icon(key, 22, color, 1.8)}<span>{label}</span></div>'
    html += '</div>'
    return html

def write(name, body_html, extra_style=""):
    path = os.path.join(OUT, f"{name}.dc.html")
    content = HEAD + f'<div class="frame">{body_html}</div>' + TAIL
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path, len(content))

print("helper module loaded")
