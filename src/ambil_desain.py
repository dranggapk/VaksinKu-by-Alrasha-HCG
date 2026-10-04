#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ambil isi kanvas Claude Design ke folder design/.

Kanvas "VaksinKu App Mockup" menyimpan seluruh rancangannya di dalam satu blok
state (script id="appifact-doc") pada halaman artifact-nya. Skrip ini membongkar
blok itu menjadi berkas-berkas biasa: satu .dc.html per artboard, canvas.json
untuk tata letak, dan logo sebagai PNG.

    python3 ambil_desain.py <berkas-halaman-artifact.html>

Berkas halaman artifact didapat dengan membaca artifact-nya (Artifact → read),
yang menyimpan salinan HTML lengkapnya ke disk.
"""
import base64
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TUJUAN = os.path.join(ROOT, "design")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    sumber = sys.argv[1]
    with open(sumber, encoding="utf-8", errors="replace") as f:
        halaman = f.read()

    cocok = re.search(r'<script[^>]*id="appifact-doc"[^>]*>([\s\S]*?)</script>', halaman)
    if not cocok:
        print("blok state kanvas tidak ditemukan — pastikan ini halaman kanvas Claude Design")
        return 1
    doc = json.loads(cocok.group(1).strip())
    berkas = doc["content"]["files"]

    os.makedirs(TUJUAN, exist_ok=True)
    print("judul kanvas:", doc.get("title"))
    for nama, isi in berkas.items():
        jalur = os.path.join(TUJUAN, nama)
        if nama.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
            # gambar disimpan di state sebagai base64 polos
            with open(jalur, "wb") as f:
                f.write(base64.b64decode(isi))
        else:
            with open(jalur, "w", encoding="utf-8") as f:
                f.write(isi)
        print("  %-26s %7d bita" % (nama, os.path.getsize(jalur)))

    catatan = doc.get("comments") or []
    if catatan:
        print("\n%d komentar di kanvas (tidak ikut diekspor)" % len(catatan))
    return 0


if __name__ == "__main__":
    sys.exit(main())
