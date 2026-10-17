#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Membuat supabase/seed.sql dari katalog yang sama dengan aplikasi.

Kota, klinik mitra, produk vaksin (id sama dengan aplikasi), price list per
klinik, dan dokter — semuanya dari src/data_katalog.py, sehingga harga tidak
pernah diketik dua kali.

    python3 buat_seed_supabase.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import data_katalog as D  # noqa: E402
from build_bundle import ANTIGEN_KATEGORI, ANTIGEN_SEDIAAN  # noqa: E402


def q(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, list):
        return "'{" + ",".join(v) + "}'"
    return "'" + str(v).replace("'", "''") + "'"


def rupiah(s):
    s = (s or "").strip()
    return None if s in ("", "—") else int(s.replace(".", ""))


def main():
    out = ["-- Dibuat oleh src/buat_seed_supabase.py dari src/data_katalog.py — jangan disunting manual.",
           "-- Aman dijalankan ulang: baris yang sudah ada diperbarui.", ""]

    out.append("insert into public.kota (id, nama) values")
    out.append(",\n".join("  (%s, %s)" % (q(m["id"]), q(m["kota"])) for m in D.MITRA))
    out.append("on conflict (id) do update set nama = excluded.nama;\n")

    baris = []
    for m in D.MITRA:
        for k in m["klinik"]:
            baris.append("  (%s, %s, %s, %s)" % (q(k["id"]), q(m["id"]), q(k["nama"]), q(k["alamat"])))
    out.append("insert into public.klinik (id, kota_id, nama, alamat) values")
    out.append(",\n".join(baris))
    out.append("on conflict (id) do update set kota_id = excluded.kota_id, nama = excluded.nama, alamat = excluded.alamat;\n")

    vaksin = []
    for i, (no, kategori, sediaan, merk, spes, umum) in enumerate(D.HARGA):
        vid = "v%d-%d" % (int(no), i)
        antigen = ANTIGEN_SEDIAAN.get(sediaan, ANTIGEN_KATEGORI.get(kategori, []))
        vaksin.append((vid, kategori, sediaan, merk, antigen, rupiah(umum), rupiah(spes)))
    out.append("insert into public.vaksin (id, kategori, sediaan, merek, antigen) values")
    out.append(",\n".join("  (%s, %s, %s, %s, %s)" % (q(v[0]), q(v[1]), q(v[2]), q(v[3]), q(v[4])) for v in vaksin))
    out.append("on conflict (id) do update set kategori = excluded.kategori, sediaan = excluded.sediaan,\n"
               "  merek = excluded.merek, antigen = excluded.antigen;\n")

    # Price list katalog berlaku untuk klinik yang "harga": "alrasha"; klinik tanpa
    # price list tidak mendapat baris (harga dikonfirmasi klinik).
    hk = []
    for m in D.MITRA:
        for k in m["klinik"]:
            if k["harga"] != "alrasha":
                continue
            for v in vaksin:
                hk.append("  (%s, %s, %s, %s)" % (q(k["id"]), q(v[0]), q(v[5]), q(v[6])))
    out.append("insert into public.harga_klinik (klinik_id, vaksin_id, harga_umum, harga_spesialis) values")
    out.append(",\n".join(hk))
    out.append("on conflict (klinik_id, vaksin_id) do update set harga_umum = excluded.harga_umum,\n"
               "  harga_spesialis = excluded.harga_spesialis;\n")

    dk = []
    for m in D.MITRA:
        for k in m["klinik"]:
            for i in k["dokter"]:
                nama, spes, inisial = D.DOKTER[i]
                dk.append("  (%s, %s, %s, %s)" % (q(k["id"]), q(nama), q(spes), q(inisial)))
    if dk:
        out.append("insert into public.dokter (klinik_id, nama, spesialisasi, inisial)")
        out.append("select v.* from (values\n" + ",\n".join(dk) + "\n) as v(klinik_id, nama, spesialisasi, inisial)")
        out.append("where not exists (select 1 from public.dokter d where d.klinik_id = v.klinik_id and d.nama = v.nama);\n")

    path = os.path.join(ROOT, "supabase", "seed.sql")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("wrote %s — %d klinik, %d vaksin, %d harga, %d dokter" % (
        path, sum(len(m["klinik"]) for m in D.MITRA), len(vaksin), len(hk), len(dk)))


if __name__ == "__main__":
    main()
