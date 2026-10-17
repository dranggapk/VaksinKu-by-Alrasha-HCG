#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merakit paket pemasangan VaksinKu untuk VPS: dist/vaksinku-vps.tar.gz.

Isi paket diekstrak ke /opt sehingga menjadi /opt/vaksinku:

    vaksinku/docker-compose.yml, pasang.sh, atur-google.sh, cadangkan.sh
    vaksinku/web/Caddyfile
    vaksinku/auth/server.mjs
    vaksinku/db/init/   00_auth → migrasi tabel, keamanan, fungsi → masuk_google → seed → peran
    vaksinku/situs/     index.html (aplikasi) + privasi.html

.env (rahasia) dan data/ (isi database) tidak pernah ada di paket, jadi ekstrak ulang
untuk pembaruan tidak menimpanya.

    python3 buat_paket_vps.py      # jalankan build_bundle.py dulu bila aplikasi berubah
"""
import glob
import io
import os
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEP = os.path.join(ROOT, "deploy")
KELUAR = os.path.join(ROOT, "dist", "vaksinku-vps.tar.gz")


def isi_paket():
    migrasi = sorted(glob.glob(os.path.join(ROOT, "supabase", "migrations", "*.sql")))
    nama_migrasi = ["10_skema.sql", "20_keamanan.sql", "30_fungsi.sql", "40_petugas.sql"]
    assert len(migrasi) == len(nama_migrasi), "jumlah migrasi berubah — perbarui nama_migrasi"
    berkas = [
        ("docker-compose.yml", os.path.join(DEP, "docker-compose.yml"), 0o644),
        ("pasang.sh", os.path.join(DEP, "pasang.sh"), 0o755),
        ("atur-google.sh", os.path.join(DEP, "atur-google.sh"), 0o755),
        ("cadangkan.sh", os.path.join(DEP, "cadangkan.sh"), 0o755),
        ("perbarui-situs.sh", os.path.join(DEP, "perbarui-situs.sh"), 0o755),
        ("perbarui-backend.sh", os.path.join(DEP, "perbarui-backend.sh"), 0o755),
        ("jadikan-admin.sh", os.path.join(DEP, "jadikan-admin.sh"), 0o755),
        ("web/Caddyfile", os.path.join(DEP, "web", "Caddyfile"), 0o644),
        ("auth/server.mjs", os.path.join(DEP, "backend", "auth", "server.mjs"), 0o644),
        ("db/init/00_auth.sql", os.path.join(DEP, "backend", "db", "00_auth.sql"), 0o644),
    ]
    berkas += [("db/init/" + n, f, 0o644) for n, f in zip(nama_migrasi, migrasi)]
    berkas += [
        ("db/init/50_masuk_google.sql", os.path.join(DEP, "backend", "db", "50_masuk_google.sql"), 0o644),
        ("db/init/60_seed.sql", os.path.join(ROOT, "supabase", "seed.sql"), 0o644),
        ("db/init/90_peran.sh", os.path.join(DEP, "backend", "db", "90_peran.sh"), 0o755),
        ("situs/index.html", os.path.join(ROOT, "VaksinKu-App.html"), 0o644),
        ("situs/privasi.html", os.path.join(ROOT, "situs", "privasi.html"), 0o644),
        ("situs/klinik.html", os.path.join(ROOT, "VaksinKu-Dashboard.html"), 0o644),
    ]
    return berkas


def main():
    os.makedirs(os.path.dirname(KELUAR), exist_ok=True)
    with tarfile.open(KELUAR, "w:gz") as tar:
        for nama, sumber, mode in isi_paket():
            with open(sumber, "rb") as f:
                data = f.read()
            info = tarfile.TarInfo("vaksinku/" + nama)
            info.size, info.mode, info.uid, info.gid = len(data), mode, 0, 0
            info.mtime = int(os.path.getmtime(sumber))
            tar.addfile(info, io.BytesIO(data))
            print("  %-28s %7.1f KB" % (nama, len(data) / 1024))
    print("wrote %s — %.0f KB" % (KELUAR, os.path.getsize(KELUAR) / 1024))


if __name__ == "__main__":
    main()
