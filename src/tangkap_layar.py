#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tangkap layar aplikasi VaksinKu dengan data contoh, untuk pemeriksaan visual.

Data disuntikkan ke localStorage sebelum skrip aplikasi dijalankan, sehingga
aplikasi langsung boot dengan isi yang diinginkan tanpa perlu memuat ulang.

    python3 tangkap_layar.py [nama-layar ...]
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUNDLE = os.path.join(ROOT, "VaksinKu-App.html")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
KELUAR = os.path.join(tempfile.gettempdir(), "vaksinku-layar")

LAYAR = {
    "beranda": "#/beranda", "booking": "#/booking", "jadwal": "#/jadwal",
    "rekam": "#/rekam", "harga": "#/harga", "profil": "#/profil",
    "tentang": "#/tentang", "internasional": "#/internasional",
    "chat": "#/chat", "chat-baru": "#/chat-baru", "chat-detail": "#/chat-detail/k1",
    "booking-detail": "#/booking-detail/b1",
    "notifikasi": "#/notifikasi",
}

TANDA_APP = "<script>/*APP-MULAI*/"


def contoh_state():
    """Satu keluarga dengan riwayat vaksin, reservasi, dan konsultasi."""
    anak, ayah = "p1", "p2"
    riwayat = [
        {"id": "r%d" % i, "pasienId": anak, "label": lb, "tanggal": "2021-%02d-20" % bln, "sumber": "jadwal"}
        for i, (lb, bln) in enumerate([("Hep B 0", 5), ("Polio 0", 5), ("BCG", 6), ("Combo DPT 1", 7),
                                       ("PCV 1", 7), ("Rotavirus 1", 7), ("Combo DPT 2", 8)])
    ]
    tanya = ("Anak saya demam 38°C sejak semalam setelah vaksin DPT kemarin sore. "
             "Apakah perlu dibawa ke klinik atau cukup diobservasi di rumah?")
    jawab = ("Demam ringan pasca vaksin DPT wajar dan biasanya reda dalam 1-2 hari. "
             "Cukupi cairan, kompres hangat, boleh parasetamol sesuai berat badan. "
             "Bila demam di atas 39°C, kejang, atau bengkak besar di bekas suntikan, segera bawa ke klinik ya Bu.")
    return {
        "versi": 1,
        "profil": {"nama": "Sari Contoh", "hp": "0812xxxxxxx", "jenisKelamin": "Perempuan"},
        "pasien": [
            {"id": anak, "nama": "Nadia Contoh", "tglLahir": "2021-05-12",
             "jenisKelamin": "Perempuan", "hubungan": "Anak"},
            {"id": ayah, "nama": "Bayu Contoh", "tglLahir": "1992-02-08",
             "jenisKelamin": "Laki-laki", "hubungan": "Ayah"},
        ],
        "alamat": [{"id": "a1", "label": "Rumah", "kecamatan": "Tanjungpinang Kota, Kepulauan Riau",
                    "alamat": "Jl. Contoh No. 10", "patokan": ""}],
        "booking": [{
            "id": "b1", "kode": "VK-880231", "dibuat": "2026-09-04T09:00:00.000Z", "status": "menunggu",
            "layanan": "homecare", "lokasi": "Rumah — Jl. Contoh No. 10, Tanjungpinang Kota",
            "pasienIds": [anak], "vaksinIds": ["v7-11"], "dokter": "umum",
            "tanggal": "2026-09-12", "jam": "10:00", "catatan": "",
            "rincian": [{"nama": "Influenza — Vaxigrip Tetra", "harga": 400000}], "tanpaHarga": [],
            "perPasien": 400000, "total": 400000,
            "pendaftar": {"nama": "Sari Contoh", "hp": "0812xxxxxxx"},
        }],
        "riwayat": riwayat,
        "pertumbuhan": [
            {"id": "t1", "pasienId": anak, "tanggal": "2025-06-10", "berat": "15.2", "tinggi": "102", "kepala": "49"},
            {"id": "t2", "pasienId": anak, "tanggal": "2026-01-15", "berat": "16.8", "tinggi": "106", "kepala": "49.5"},
            {"id": "t3", "pasienId": anak, "tanggal": "2026-09-01", "berat": "17.9", "tinggi": "109", "kepala": "50"},
        ],
        "konsultasi": [{
            "id": "k1", "kode": "KS-471967", "status": "dijawab", "dibuat": "2026-09-05T08:10:00.000Z",
            "pasienId": anak, "topik": "Efek samping (KIPI)", "dokter": "dr. Dwi Fachri JH, Sp.A",
            "pertanyaan": tanya,
            "konteks": ["Usia: 5 tahun 3 bulan", "Kelengkapan vaksin sesuai usia: 21% (7/33)",
                        "Vaksin terakhir: Combo DPT 2 (20 Agustus 2021)",
                        "Pengukuran 1 September 2026: BB 17.9 kg, TB 109 cm"],
            "pendaftar": {"nama": "Sari Contoh", "hp": "0812xxxxxxx"},
            "pesan": [
                {"id": "m1", "dari": "saya", "teks": tanya, "waktu": "2026-09-05T08:10:00.000Z"},
                {"id": "m2", "dari": "dokter", "teks": jawab, "waktu": "2026-09-05T09:40:00.000Z"},
            ],
        }],
        "poin": 10, "draft": None, "draftKonsul": None, "ui": {"pasienAktif": anak},
    }


def seed_js(tujuan):
    return ("<script>try{localStorage.setItem('vaksinku.v1'," +
            json.dumps(json.dumps(contoh_state(), ensure_ascii=False)) +
            ");}catch(e){}location.hash=" + json.dumps(tujuan) + ";</script>\n")


def main():
    pilih = sys.argv[1:] or list(LAYAR)
    os.makedirs(KELUAR, exist_ok=True)
    with open(BUNDLE, encoding="utf-8") as f:
        html = f.read()
    if TANDA_APP not in html:
        print("penanda skrip aplikasi tidak ditemukan — jalankan build_bundle.py dulu")
        return 1
    for nama in pilih:
        if nama not in LAYAR:
            print("layar tidak dikenal:", nama)
            continue
        doc = html.replace(TANDA_APP, seed_js(LAYAR[nama]) + TANDA_APP)
        tmp = os.path.join(tempfile.gettempdir(), "_layar_%s.html" % nama)
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(doc)
        png = os.path.join(KELUAR, nama + ".png")
        if os.path.exists(png):
            os.remove(png)
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--allow-file-access-from-files",
             "--hide-scrollbars", "--window-size=470,930", "--virtual-time-budget=4000",
             "--screenshot=" + png, "file://" + tmp],
            capture_output=True, timeout=90)
        print(("  ok " if os.path.exists(png) else "  XX ") + png)
    return 0


if __name__ == "__main__":
    sys.exit(main())
