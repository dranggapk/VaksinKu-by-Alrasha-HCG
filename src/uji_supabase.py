#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uji aturan akses backend Supabase VaksinKu di PostgreSQL lokal.

Membuat basis data kosong, memasang tiruan skema auth Supabase
(supabase/tests/lokal_supabase_shim.sql), menjalankan semua migrasi
berurutan, mengisi seed.sql, lalu menjalankan skenario uji hak akses.

    python3 uji_supabase.py            # PostgreSQL di 127.0.0.1:54329
    PGURL=postgresql://postgres@host:port python3 uji_supabase.py
"""
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SB = os.path.join(ROOT, "supabase")
PGURL = os.environ.get("PGURL", "postgresql://postgres@127.0.0.1:54329")
DB = "vaksinku_uji"


def psql(db, *args, berkas=None):
    cmd = ["psql", f"{PGURL}/{db}", "-v", "ON_ERROR_STOP=1", "-X", "-q", "-At", *args]
    if berkas:
        cmd += ["-f", berkas]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        nama = os.path.relpath(berkas, ROOT) if berkas else " ".join(args)
        sys.exit(f"GAGAL menjalankan {nama}:\n{r.stderr.strip()}")
    return r.stdout


def main():
    psql("postgres", "-c", f"drop database if exists {DB} with (force)")
    psql("postgres", "-c", f"create database {DB}")

    urutan = [os.path.join(SB, "tests", "lokal_supabase_shim.sql")]
    urutan += sorted(glob.glob(os.path.join(SB, "migrations", "*.sql")))
    urutan += [os.path.join(SB, "seed.sql")]
    for f in urutan:
        psql(DB, berkas=f)
        print("terpasang:", os.path.relpath(f, ROOT))

    keluaran = psql(DB, berkas=os.path.join(SB, "tests", "uji_hak_akses.sql"))
    baris = [b for b in keluaran.splitlines() if b.startswith(("LULUS", "GAGAL"))]
    for b in baris:
        print(b)
    gagal = sum(b.startswith("GAGAL") for b in baris)
    print(f"\n{len(baris) - gagal}/{len(baris)} lulus")
    if gagal or not baris:
        sys.exit(1)


if __name__ == "__main__":
    main()
