#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild catalog page 5 (Jadwal Vaksin Anak) from the two scroll captures and
correct the duplicated bullet in the "0 BULAN (LAHIR)" box: the second entry
reads "Hep B 0" but should read "Polio 0".

The replacement text is rendered on a 4x canvas and downsampled, which matches
how the original page was produced (large render, then downscaled), so stroke
weight and antialiasing match the surrounding text.
"""
import os
from PIL import Image, ImageDraw, ImageFont

UP = "/root/.claude/uploads/057c0866-d1f0-5e2b-a03b-cc71ca25427e"
HERE = os.path.dirname(os.path.abspath(__file__))

# --- page 5 spans the end of capture A and the first rows of capture B -------
A = Image.open(f"{UP}/df7cb266-image.jpg").convert("RGB")   # pages 1-5
B = Image.open(f"{UP}/d042473c-image.jpg").convert("RGB")   # page 5 footer, pages 6-9

PAGE_TOP = 6509        # first white row of page 5 in A
OVERLAP = 7916         # A_y = B_y + OVERLAP (found by correlating the captures)
FOOTER_END_B = 120     # first grey row after page 5's teal footer, in B

part_a = A.crop((0, PAGE_TOP, A.width, A.height))
part_b = B.crop((0, A.height - OVERLAP, B.width, FOOTER_END_B))
page = Image.new("RGB", (A.width, part_a.height + part_b.height))
page.paste(part_a, (0, 0))
page.paste(part_b, (0, part_a.height))

# --- patch the second bullet -------------------------------------------------
# Region and type parameters were fitted against the identical line above it.
REGION = (250, 6993, 330, 7015)   # in capture-A coordinates
FONT = os.path.join(HERE, "fonts", "poppins500.ttf")
SIZE_SS, DX_SS, DY_SS, S = 66, 21, -2, 4   # supersampled type metrics
BG = (253, 245, 232)              # cream fill inside the box
INK = (24, 19, 16)
KEEP_TOP_ROWS = 1                 # leave line 1's "p" descender untouched

x0, y0, x1, y1 = REGION
w, h = x1 - x0, y1 - y0

big = Image.new("RGB", (w * S, h * S), BG)
ImageDraw.Draw(big).text((DX_SS, DY_SS), "Polio 0",
                         font=ImageFont.truetype(FONT, SIZE_SS), fill=INK)
tile = big.resize((w, h), Image.LANCZOS)

page.paste(tile.crop((0, KEEP_TOP_ROWS, w, h)),
           (x0, y0 - PAGE_TOP + KEEP_TOP_ROWS))

# --- remove the gallery-app overlay that the screenshot captured -------------
# ("5/16" page pill and the scroll chevron sit on empty white page margin)
overlay_draw = ImageDraw.Draw(page)
for rect in [(838, 0, 978, 47), (972, 0, page.width, 82)]:
    overlay_draw.rectangle(rect, fill=(252, 252, 252))

out = os.path.join(HERE, "Katalog-VaksinKu-Hal5-Jadwal-Vaksin-Anak-revisi.png")
page.save(out)
print("wrote", out, page.size)

# side-by-side detail for checking
before = A.crop((215, 6940, 420, 7035)).resize((205 * 4, 95 * 4), Image.LANCZOS)
after = page.crop((215, 6940 - PAGE_TOP, 420, 7035 - PAGE_TOP)).resize((205 * 4, 95 * 4), Image.LANCZOS)
cmp = Image.new("RGB", (before.width, before.height * 2 + 20), (255, 255, 255))
cmp.paste(before, (0, 0)); cmp.paste(after, (0, before.height + 20))
cmp.save(os.path.join(HERE, "cek_sebelum_sesudah.png"))
print("wrote comparison")
