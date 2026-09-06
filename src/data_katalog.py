#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Isi katalog resmi VaksinKu by Alrasha Ibumas — sumber tunggal untuk
harga, jadwal vaksin, layanan, dokter, dan lokasi klinik di dalam prototipe."""

# ---------------------------------------------------------------- identitas
BRAND = {
    "tagline": "Tempatnya Vaksinasi Aman · Lengkap · Terjangkau",
    "call_center": "0811-7744-74",
    "call_center_label": "Call Center & Booking · Fast Respon Service",
    "instagram": "@alrashaibumasgroup",
    "website": "www.alrashaibumas.com",
    "group": "Alrasha Ibumas Group",
}

# Tiga pilar positioning (slide "Kenapa harus di VaksinKu")
PILAR = [
    ("shield", "Aman", [
        "Vaksin terjamin keasliannya, didapat dari produsen skala nasional dan internasional",
        "Sistem <b>Cold Chain</b> yang menjamin penyimpanan, pengiriman, dan monitoring sesuai standar",
        "Dokter vaksinator kompeten dan bersertifikat",
    ]),
    ("check-c", "Lengkap", [
        "Menyediakan berbagai jenis vaksin dasar dan tambahan untuk segala usia",
        "Fleksibilitas memilih dokter umum atau dokter spesialis",
        "Tersedia layanan Home Care, On Site Corporate, dan On Site Klinik",
    ]),
    ("coin", "Terjangkau", [
        "Harga lebih murah dibanding vaksinasi di rumah sakit",
        "Price list terbuka, termasuk jasa dokter, vaksin, bahan habis pakai, dan administrasi",
        "Tersedia paket vaksinasi yang lebih terjangkau",
    ]),
]

# ---------------------------------------------------------------- layanan
LAYANAN = [
    ("house", "Home Care", "Layanan vaksinasi langsung ke rumah",
     "Cocok untuk anak-anak, lansia, pasien pasca tindakan medis, atau yang ingin kenyamanan di rumah.",
     "Aman, praktis, dan tetap diawasi tenaga medis berpengalaman"),
    ("building", "On Site Corporate", "Vaksinasi di lingkungan kantor/perusahaan",
     "Ideal untuk menjaga kesehatan tim kerja tanpa harus keluar kantor.",
     "Efisien, hemat waktu, bisa massal, dengan tim medis berpengalaman"),
    ("pin", "On Site Klinik", "Vaksinasi langsung di klinik",
     "Fasilitas nyaman dengan tenaga medis profesional.",
     "Proses cepat, bisa booking jadwal, konsultasi langsung dengan dokter"),
]

TERMASUK = ["Konsultasi Dokter", "Tindakan Dokter", "Vaksin", "Bahan Medis Habis Pakai"]

# Segmen layanan vaksinasi (slide "Layanan Vaksinasi di VaksinKu")
SEGMEN = [
    ("cake", "anak-02", "Vaksinasi Anak", "Usia 0–2 tahun"),
    ("cake", "anak-25", "Vaksinasi Anak", "Usia 2–5 tahun"),
    ("family", "anak-sekolah", "Anak Usia Sekolah", "6–18 tahun"),
    ("user", "dewasa", "Vaksinasi Dewasa", "19 tahun ke atas"),
    ("heart", "pranikah", "Vaksinasi Pranikah", "Persiapan menikah"),
    ("heart", "lansia", "Vaksinasi Lansia", "50 tahun ke atas"),
    ("plane", "internasional", "Vaksinasi Internasional", "Haji, umrah, studi & liburan (ICV)"),
]

# ---------------------------------------------------------------- harga
# (no, vaksin, sediaan, merk/produk, harga dokter spesialis, harga dokter umum)
HARGA = [
    ("1", "BCG (TBC)", "BCG Private", "BCG Biofarma", "550.000", "465.000"),
    ("1", "BCG (TBC)", "BCG Group (min 3 orang)", "BCG Biofarma", "285.000", "235.000"),
    ("2", "Polio", "Polio Oral", "Polio Tetes", "200.000", "130.000"),
    ("2", "Polio", "Polio IPV", "Polio Injeksi (IPV)", "355.000", "305.000"),
    ("3", "DPT / DPT Combo", "DPaT + IPV + HIB + HB", "Infanrix Hexa", "1.095.000", "1.000.000"),
    ("3", "DPT / DPT Combo", "DPaT + IPV + HIB + HB", "Hexaxim", "1.050.000", "950.000"),
    ("3", "DPT / DPT Combo", "DPaT + HIB + HB", "Pentabio", "400.000", "360.000"),
    ("4", "Rotavirus (diare)", "Rotateq (pentavalen)", "Rotateq", "525.000", "475.000"),
    ("4", "Rotavirus (diare)", "Rotarix (monovalen)", "Rotarix susp", "550.000", "495.000"),
    ("5", "Meningitis", "Menivax", "Menivax", "—", "345.000"),
    ("6", "Pneumococcus", "PCV (20) – pneumonia / IPD", "Prevenar 20", "1.200.000", "1.100.000"),
    ("7", "Influenza", "4 strain", "Vaxigrip Tetra", "450.000", "400.000"),
    ("7", "Influenza", "Flubio", "Flubio", "375.000", "325.000"),
    ("8", "Typhoid (Tipes)", "Typhim Vi", "Typhim", "450.000", "425.000"),
    ("9", "Tetanus", "Tdap", "Adacel", "575.000", "525.000"),
    ("10", "Campak + Rubella", "Campak + Rubella", "MR Group", "450.000", "375.000"),
    ("10", "Campak + Rubella", "Campak + Rubella", "MR Private", "975.000", "900.000"),
    ("10", "Campak + Rubella", "Measles, Mumps, Rubella", "MMR", "690.000", "575.000"),
    ("11", "Varicella", "Varicella", "Varicella", "650.000", "600.000"),
    ("11", "Varicella", "Varicella", "Varivax", "805.000", "750.000"),
    ("12", "Hepatitis B", "Engerix-B Anak", "Engerix-B Anak", "350.000", "300.000"),
    ("12", "Hepatitis B", "Engerix-B Dewasa", "Engerix-B Dewasa", "375.000", "325.000"),
    ("13", "Hepatitis A", "Avaxim Anak", "Avaxim Anak", "550.000", "500.000"),
    ("13", "Hepatitis A", "Avaxim Dewasa", "Avaxim Dewasa", "600.000", "565.000"),
    ("14", "HPV (Kanker Serviks)", "HPV 2 valen", "Gardasil", "1.300.000", "1.250.000"),
    ("14", "HPV (Kanker Serviks)", "HPV 9 valen", "Gardasil 9", "2.400.000", "2.350.000"),
    ("15", "Demam Berdarah", "Qdenga", "Qdenga", "700.000", "650.000"),
    ("16", "Japanese Encephalitis", "Imojev", "Imojev", "600.000", "550.000"),
    ("17", "Flu Singapura", "Inlive VACC", "Inlive VACC", "1.125.000", "1.075.000"),
]

# Harga vaksinasi internasional & paket promo
HARGA_INTERNASIONAL = [
    ("Polio (IPV)", "305.000", None),
    ("Meningitis", "345.000", None),
    ("Polio + Meningitis", "620.000", "650.000"),
]
PAKET_TRIPLE = {
    "nama": "Paket Triple",
    "isi": ["Polio (IPV)", "Meningitis (Menivax)", "Influenza (Vaxigrip)"],
    "harga": "1.000.000",
    "coret": "1.050.000",
}

# ---------------------------------------------------------------- jadwal anak
# Jadwal Vaksin Anak sesuai IDAI terbaru 2024
JADWAL_ANAK = [
    ("0 bulan", "Lahir", ["Hep B 0"]),
    ("1 bulan", None, ["BCG"]),
    ("2 bulan", None, ["Combo DPT 1", "PCV 1", "Rotavirus 1"]),
    ("3 bulan", None, ["Combo DPT 2"]),
    ("4 bulan", None, ["Combo DPT 3", "PCV 2", "Rotavirus 2"]),
    ("6 bulan", None, ["PCV 3", "Rotavirus 3", "Influenza (Flu) 1", "HFMD (Flu Singapura) 1"]),
    ("7 bulan", None, ["Influenza (Flu) 2", "HFMD (Flu Singapura) 2"]),
    ("9 bulan", None, ["MR 1", "Japanese Encephalitis (JE) 1"]),
    ("12 bulan", None, ["PCV 4", "Varicella 1", "Hepatitis A 1"]),
    ("14 bulan", None, ["Varicella 2"]),
    ("18 bulan", None, ["Combo DPT 4", "MMR 1", "Hepatitis A 2"]),
    ("24 bulan", None, ["Japanese Encephalitis (JE) 2", "Tifoid (Tipes) 1", "Influenza (Flu) tiap 1 tahun"]),
    ("3–4 tahun", None, ["Influenza (Flu) tiap 1 tahun"]),
    ("5 tahun", None, ["Combo DPT 5", "MMR 2", "Influenza (Flu) tiap 1 tahun", "Tifoid (Tipes) tiap 3 tahun"]),
    ("6 tahun", None, ["Influenza (Flu) tiap 1 tahun", "Demam Berdarah (DBD) 1"]),
    ("6 tahun 3 bulan", None, ["Demam Berdarah (DBD) 2"]),
    ("7–8 tahun", None, ["Influenza (Flu) tiap 1 tahun", "Tifoid (Tipes) tiap 3 tahun"]),
    ("9 tahun", None, ["HPV 1", "Influenza (Flu) tiap 1 tahun"]),
    ("10 tahun", None, ["DPT 6 dalam bentuk Tdap", "Influenza (Flu) tiap 1 tahun"]),
    ("11–18 tahun", "Lengkap!", ["Influenza (Flu) tiap 1 tahun", "Tifoid (Tipes) tiap 3 tahun"]),
]

# ---------------------------------------------------------------- jadwal dewasa
# Sesuai rekomendasi PAPDI 2025. Vaksin teratas = prioritas bila belum lengkap.
_DOSIS = {
    "flu": ("Flu", "1 dosis setiap tahun"),
    "pcv": ("Pneumonia PCV20", "1 dosis"),
    "dbd": ("DBD", "2 dosis, jarak 3 bulan"),
    "hpv": ("HPV 9 (wanita)", "3 dosis (0–2–6 bulan)"),
    "tifoid": ("Tifoid / tipes", "1 dosis setiap 3 tahun"),
    "hepa": ("Hepatitis A", "2 dosis, jarak 6 bulan"),
    "hepb": ("Hepatitis B", "3 dosis (0–1–6 bulan)"),
    "varicella": ("Varicella", "2 dosis, jarak 1 bulan (bagi yang belum pernah cacar air)"),
    "mmr": ("MMR (wanita)", "2 dosis, jarak 1 bulan (persiapan pranikah)"),
    "tdap": ("Tetanus Tdap (wanita)", "1 dosis (persiapan pranikah)"),
    "zoster": ("Zoster / Cacar Api", "2 dosis, jarak 2 bulan (belum maupun sudah pernah cacar api)"),
    "rsv": ("RSV", "1 dosis"),
}

JADWAL_DEWASA = [
    ("19 – 21 tahun", ["flu", "pcv", "dbd", "hpv", "tifoid", "hepa", "hepb", "varicella"]),
    ("22 – 26 tahun", ["flu", "pcv", "dbd", "hpv", "tifoid", "hepa", "hepb", "varicella", "mmr", "tdap"]),
    ("27 – 45 tahun", ["flu", "pcv", "dbd", "hpv", "tifoid", "hepa", "hepb", "varicella", "mmr", "tdap"]),
    ("46 – 49 tahun", ["flu", "pcv", "tifoid", "hepa", "hepb", "varicella"]),
    ("50 – 59 tahun", ["flu", "pcv", "zoster", "tifoid", "hepa", "hepb", "varicella"]),
    ("60 tahun ke atas", ["flu", "pcv", "zoster", "rsv", "tifoid", "hepa", "hepb", "varicella"]),
]
JADWAL_DEWASA_CATATAN = "Vaksin teratas adalah vaksin prioritas bila belum lengkap. Usia 60 tahun ke atas tidak ada batas usia maksimal."


def dosis(key):
    return _DOSIS[key]


# ---------------------------------------------------------------- pranikah
JADWAL_PRANIKAH_VAKSIN = [
    ("Vaksin HPV", "3 dosis", "Mencegah kanker serviks"),
    ("Vaksin MMR", "2 dosis", "Mencegah Rubella pada kehamilan"),
    ("Vaksin Tetanus", "1 dosis", "Mencegah infeksi tetanus saat persalinan"),
]
JADWAL_PRANIKAH_WAKTU = [
    ("H-7 bulan", ["Vaksin HPV ke-1", "Vaksin MMR ke-1"]),
    ("H-5 bulan", ["Vaksin HPV ke-2", "Vaksin MMR ke-2"]),
    ("H-1 bulan", ["Vaksin HPV ke-3", "Vaksin Tetanus"]),
]

# ---------------------------------------------------------------- lansia
JADWAL_LANSIA = [
    ("Vaksin Flu", "1 dosis setiap tahun",
     "Mencegah influenza. Influenza pada lansia lebih berat gejalanya dan dapat menimbulkan komplikasi lanjut."),
    ("Vaksin Pneumonia", "1 dosis untuk seumur hidup",
     "Mencegah pneumonia / radang paru-paru, penyebab kematian tertinggi akibat infeksi pada lansia."),
]

# ---------------------------------------------------------------- internasional
VAKSIN_INTERNASIONAL_WAJIB = [
    ("Meningitis Polisakarida",
     "Memberikan perlindungan terhadap penyakit meningitis, berlaku selama 2 tahun. Bisa digunakan untuk anak usia di atas 2 tahun."),
    ("Inactivated Polio Vaccine (IPV)",
     "Mencegah penyakit polio. Diberikan minimal satu dosis dalam 12 bulan sebelum keberangkatan dan tidak kurang dari 4 minggu sebelum kedatangan di Arab Saudi."),
]
VAKSIN_INTERNASIONAL_TAMBAHAN = [
    ("Influenza", "WHO merekomendasikan melengkapi vaksinasi yang berhubungan dengan pernapasan."),
    ("Pneumonia", "WHO merekomendasikan melengkapi vaksinasi yang berhubungan dengan pernapasan."),
]

# ---------------------------------------------------------------- dokter
DOKTER = [
    ("dr. Dwi Fachri JH, Sp.A", "Dokter Spesialis Anak", "DF"),
    ("dr. Augustine PA, Sp.PD, FINASIM", "Dokter Spesialis Penyakit Dalam", "AP"),
    ("dr. Leo Andreas, Sp.PD", "Dokter Spesialis Penyakit Dalam", "LA"),
    ("Tim Dokter Umum", "Dokter Umum vaksinator bersertifikat", "DU"),
]

# ---------------------------------------------------------------- klinik
KLINIK = [
    ("Klinik Alrasha Health Care Center", "Jl. Hang Lekir, Batu 10, No. 21–22, Tanjungpinang"),
    ("Klinik Utama Alrasha Ibumas", "Jl. Hang Lekir, Batu 10, No. 18–20, Tanjungpinang"),
    ("Klinik Ibumas", "Jl. D.I. Panjaitan No. 4, Tanjungpinang"),
]

# ---------------------------------------------------------------- alur reservasi
ALUR_RESERVASI = [
    "Booking via Call Center atau langsung di klinik",
    "Konsultasi kebutuhan vaksin: di klinik, home care, atau on site perusahaan",
    "Menjadwalkan janji vaksin",
    "Datang ke klinik sesuai jadwal yang sudah ditentukan",
    "Konsultasi dokter dan tindakan vaksinasi",
    "Melakukan pembayaran",
    "Pengambilan obat pendukung (jika dibutuhkan)",
    "Penerbitan e-ICV khusus vaksin internasional",
]
