#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Isi katalog resmi VaksinKu by Alrasha Health Care Group — sumber tunggal untuk
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

# Masuk dengan Google. Client ID dibuat di Google Cloud Console (Credentials →
# OAuth client ID → Web application) dengan Authorized JavaScript origin
# https://vaksinku.app. Client ID bukan rahasia; boleh juga diisi lewat
# variabel lingkungan VAKSINKU_GOOGLE_CLIENT_ID saat build.
GOOGLE = {
    "client_id": "969970859602-3le4bln2e58lcd3d84n6q08uo55jli6h.apps.googleusercontent.com",
    "situs": "https://vaksinku.app",
}

# Tiga pilar positioning (slide "Kenapa harus di VaksinKu")
PILAR = [
    ("shield", "Aman", [
        "Vaksin terjamin keasliannya dari produsen skala nasional dan internasional",
        "Sistem <b>Cold Chain</b> sesuai standar untuk menjaga kualitas vaksin",
        "Dikerjakan oleh dokter vaksinator kompeten dan bersertifikat",
    ]),
    ("check-c", "Lengkap", [
        "Menyediakan berbagai jenis vaksin dasar dan tambahan untuk segala usia",
        "Fleksibilitas memilih dokter umum atau dokter spesialis",
        "Tersedia layanan Home Care, On Site Corporate, dan On Site Klinik",
    ]),
    ("coin", "Terjangkau", [
        "Harga lebih murah dibanding vaksinasi di rumah sakit",
        "Price list sudah termasuk jasa dokter, vaksin, bahan habis pakai, dan administrasi",
        "Ada berbagai paket vaksinasi yang lebih terjangkau",
    ]),
]

# ---------------------------------------------------------------- layanan
LAYANAN = [
    ("house", "Home Care", "Layanan vaksinasi langsung ke rumah",
     "Cocok untuk anak-anak, lansia, pasien pasca tindakan medis, atau yang ingin kenyamanan di rumah.",
     "Aman, praktis, dan tetap diawasi tenaga medis berpengalaman"),
    ("building", "On Site Corporate", "Vaksinasi di lingkungan kantor/perusahaan",
     "Ideal untuk menjaga kesehatan tim kerja tanpa harus keluar kantor/perusahaan.",
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
    ("heart", "hamil", "Vaksinasi Ibu Hamil", "Selama kehamilan"),
    ("heart", "lansia", "Vaksinasi Lansia", "50 tahun ke atas"),
    ("plane", "internasional", "Vaksinasi Internasional", "Haji, umrah, studi & liburan (ICV)"),
]

# ---------------------------------------------------------------- harga
# Katalog VaksinKu 2026 (Daftar Harga Vaksinasi).
# (id, no, vaksin, sediaan, merk/produk, harga dokter spesialis, harga dokter umum)
# id tetap untuk selamanya: dipakai reservasi, riwayat, dan price list di server.
# Produk baru mendapat id baru (nomor urut setelah id terbesar), jangan memakai ulang.
HARGA = [
    ("v1-0", "1", "BCG (TBC)", "BCG Private", "BCG Biofarma", "550.000", "465.000"),
    ("v1-1", "1", "BCG (TBC)", "BCG Group (min 3 orang)", "BCG Biofarma", "285.000", "235.000"),
    ("v2-2", "2", "Polio", "Polio Oral", "Polio Tetes", "200.000", "130.000"),
    ("v2-3", "2", "Polio", "Polio IPV", "Polio Injeksi (IPV)", "395.000", "320.000"),
    ("v3-4", "3", "DPT / DPT Combo", "DPaT + IPV + HIB + HB", "Infanrix Hexa", "1.150.000", "1.060.000"),
    ("v3-5", "3", "DPT / DPT Combo", "DPaT + IPV + HIB + HB", "Hexaxim", "1.200.000", "1.100.000"),
    ("v3-6", "3", "DPT / DPT Combo", "DPaT + HIB + HB", "Pentabio", "400.000", "360.000"),
    ("v4-7", "4", "Rotavirus (diare)", "Rotateq (pentavalen)", "Rotateq", "525.000", "475.000"),
    ("v4-8", "4", "Rotavirus (diare)", "Rotarix (monovalen)", "Rotarix susp", "635.000", "575.000"),
    ("v5-9", "5", "Meningitis", "Menivax", "Menivax", "—", "365.000"),
    ("v6-10", "6", "Pneumococcus", "PCV (20) – pneumonia / IPD", "Prevenar 20", "1.300.000", "1.150.000"),
    ("v7-11", "7", "Influenza", "3 strain", "Vaxigrip TIV", "400.000", "350.000"),
    ("v7-12", "7", "Influenza", "3 strain", "Flubio", "385.000", "345.000"),
    ("v8-13", "8", "Typhoid (Tipes)", "Typhim Vi", "Typhim", "500.000", "450.000"),
    ("v9-14", "9", "Tetanus", "Tdap", "Adacel", "575.000", "525.000"),
    ("v10-15", "10", "Campak + Rubella", "Campak + Rubella", "MR Group (3 orang)", "450.000", "375.000"),
    ("v10-29", "10", "Campak + Rubella", "Campak + Rubella", "MR Group (2 orang)", "675.000", "625.000"),
    ("v10-16", "10", "Campak + Rubella", "Campak + Rubella", "MR Private", "1.300.000", "1.200.000"),
    ("v10-17", "10", "Campak + Rubella", "Measles, Mumps, Rubella", "MMR", "690.000", "575.000"),
    ("v11-18", "11", "Varicella", "Varicella", "Varicella", "730.000", "675.000"),
    ("v11-19", "11", "Varicella", "Varicella", "Varivax", "805.000", "750.000"),
    ("v12-20", "12", "Hepatitis B", "Engerix-B Anak", "Engerix-B Anak", "350.000", "300.000"),
    ("v12-21", "12", "Hepatitis B", "Engerix-B Dewasa", "Engerix-B Dewasa", "375.000", "325.000"),
    ("v13-22", "13", "Hepatitis A", "Avaxim Anak", "Avaxim Anak", "575.000", "525.000"),
    ("v13-23", "13", "Hepatitis A", "Avaxim Dewasa", "Avaxim Dewasa", "610.000", "565.000"),
    ("v14-24", "14", "HPV (Kanker Serviks)", "HPV 4 valen", "HPV 4", "700.000", "650.000"),
    ("v14-25", "14", "HPV (Kanker Serviks)", "HPV 9 valen", "Gardasil 9", "2.400.000", "2.350.000"),
    ("v15-26", "15", "Demam Berdarah", "Qdenga", "Qdenga", "700.000", "650.000"),
    ("v16-27", "16", "Japanese Encephalitis", "Imojev", "Imojev", "680.000", "610.000"),
    ("v17-28", "17", "Flu Singapura", "Inlive VACC", "Inlive VACC", "1.125.000", "1.075.000"),
    ("v18-30", "18", "Yellow Fever", "Yellow Fever", "Stamaril", "600.000", "550.000"),
    ("v19-31", "19", "Hepatitis A + B", "Twinrix", "Twinrix", "850.000", "750.000"),
    ("v20-32", "20", "Meningitis Konjugat", "MenQuadfi", "MenQuadfi", "975.000", "900.000"),
]

# Harga vaksinasi internasional & paket (halaman "Daftar Harga Vaksinasi Internasional")
HARGA_INTERNASIONAL = [
    ("Polio (IPV)", "320.000", None),
    ("Meningitis", "365.000", None),
]
PAKET_INTERNASIONAL = [
    {"nama": "Bundling Apotek Mini", "isi": ["Polio (IPV)", "Meningitis (Menivax)", "Apotek Mini Marwa"],
     "harga": "590.000", "coret": "775.000"},
    {"nama": "Paket Triple", "isi": ["Polio (IPV)", "Meningitis (Menivax)", "Influenza (Vaxigrip / Flubio)"],
     "harga": "800.000", "coret": "1.350.000"},
]
PAKET_TRIPLE = PAKET_INTERNASIONAL[1]   # nama lama, dipakai mockup statis (build_app.py)

# ---------------------------------------------------------------- jadwal anak
# Jadwal Vaksin Anak sesuai IDAI terbaru 2024
JADWAL_ANAK = [
    ("0 bulan", "Lahir", ["Hep B 0", "Polio 0"]),
    ("1 bulan", None, ["BCG"]),
    ("2 bulan", None, ["Combo DTP 1 (DPT 1, Polio 1, Hep B 1, Hib 1)", "PCV 1", "Rotavirus 1"]),
    ("3 bulan", None, ["Combo DTP 2 (DPT 2, Polio 2, Hep B 2, Hib 2)"]),
    ("4 bulan", None, ["Combo DTP 3 (DPT 3, Polio 3, Hep B 3, Hib 3)", "PCV 2", "Rotavirus 2"]),
    ("6 bulan", None, ["PCV 3", "Rotavirus 3", "Influenza (Flu) 1", "HFMD (Flu Singapura) 1"]),
    ("7 bulan", None, ["Influenza (Flu) 2", "HFMD (Flu Singapura) 2"]),
    ("9 bulan", None, ["MR 1", "Japanese Encephalitis (JE) 1"]),
    ("12 bulan", None, ["PCV 4", "Varicella 1", "Hepatitis A 1"]),
    ("14 bulan", None, ["Varicella 2"]),
    ("18 bulan", None, ["Combo DTP 4 (DPT 4, Polio 4, Hep B 4, Hib 4)", "MMR 1", "Hepatitis A 2"]),
    ("24 bulan", None, ["Japanese Encephalitis (JE) 2", "Tifoid (Tipes) 1", "Influenza (Flu) tiap 1 tahun"]),
    ("3–4 tahun", None, ["Influenza (Flu) tiap 1 tahun"]),
    ("5 tahun", None, ["Combo DTP 5 (DTaP-IPV)", "MMR 2", "Influenza (Flu) tiap 1 tahun", "Tifoid (Tipes) tiap 3 tahun"]),
    ("6 tahun", None, ["Influenza (Flu) tiap 1 tahun", "Demam Berdarah (DBD) 1"]),
    ("6 tahun 3 bulan", None, ["Demam Berdarah (DBD) 2"]),
    ("7–8 tahun", None, ["Influenza (Flu) tiap 1 tahun", "Tifoid (Tipes) tiap 3 tahun"]),
    ("9 tahun", None, ["HPV 1", "Influenza (Flu) tiap 1 tahun"]),
    ("9,5 tahun", None, ["HPV 2"]),
    ("10 tahun", None, ["DTP 6 (Tdap)", "Influenza (Flu) tiap 1 tahun"]),
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
    ("46 – 49 tahun", ["flu", "pcv", "tifoid", "hepa", "hepb", "varicella", "mmr", "tdap"]),
    ("50 – 59 tahun", ["flu", "pcv", "zoster", "tifoid", "hepa", "hepb", "varicella"]),
    ("60 tahun ke atas", ["flu", "pcv", "zoster", "rsv", "tifoid", "hepa", "hepb", "varicella"]),
]
JADWAL_DEWASA_CATATAN = "Vaksin teratas adalah vaksin prioritas bila belum lengkap. Usia 60 tahun ke atas tidak ada batas usia maksimal."


def dosis(key):
    return _DOSIS[key]


# ---------------------------------------------------------------- pranikah
JADWAL_PRANIKAH_VAKSIN = [
    ("Vaksin HPV", "3 dosis", "Mencegah kanker serviks"),
    ("Vaksin MMR", "2 dosis", "Mencegah campak, gondongan, dan rubella"),
    ("Vaksin Tetanus", "1 dosis", "Mencegah infeksi tetanus saat persalinan"),
    ("Vaksin Influenza", "1 dosis setiap tahun", "Mencegah flu dan komplikasinya"),
    ("Vaksin Hepatitis B", "3 dosis", "Mencegah infeksi hepatitis B yang dapat menular pada ibu dan bayi"),
]
# Dihitung dari tanggal pernikahan
JADWAL_PRANIKAH_WAKTU = [
    ("H-7 bulan", ["Vaksin HPV ke-1", "Vaksin MMR ke-1", "Vaksin Hepatitis B ke-1"]),
    ("H-5 bulan", ["Vaksin HPV ke-2", "Vaksin MMR ke-2", "Vaksin Hepatitis B ke-2"]),
    ("H-1 bulan", ["Vaksin HPV ke-3", "Vaksin Tetanus", "Vaksin Hepatitis B ke-3", "Vaksin Influenza"]),
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
    ("dr. Andrea Hertanto, Sp.DVE", "Dokter Spesialis Kulit & Kelamin", "AH"),
    ("dr. Hariadi Putra, Sp.OG", "Dokter Spesialis Obstetri & Ginekologi", "HP"),
]
# urutan tampil di klinik: spesialis dulu, lalu tim dokter umum (indeks DOKTER tetap)
DOKTER_ALRASHA = [0, 1, 2, 4, 5, 3]

# ---------------------------------------------------------------- klinik
# Mitra VaksinKu per kota. Harga dan ketersediaan vaksin bergantung pada klinik
# yang dipilih pengguna. "harga" menunjuk price list yang dipakai klinik itu:
# "alrasha" = price list katalog di atas (HARGA, HARGA_INTERNASIONAL, PAKET_INTERNASIONAL);
# None = price list belum diterima, harga dikonfirmasi klinik saat reservasi.
# "alamat" kosong = belum diterima; aplikasi menulis "alamat menyusul".
MITRA = [
    {"id": "bandung", "kota": "Kota Bandung", "klinik": [
        {"id": "jasmine-mq", "nama": "Klinik Utama Jasmine MQ Medika", "alamat": "", "harga": None, "dokter": []},
    ]},
    {"id": "tanjungpinang", "kota": "Kota Tanjungpinang", "klinik": [
        {"id": "alrasha-hcc", "nama": "Klinik Pratama Alrasha HCC",
         "alamat": "Jl. Hang Lekir No. 18–22, Batu IX, Kec. Tanjungpinang Timur, Kota Tanjungpinang",
         "harga": "alrasha", "dokter": DOKTER_ALRASHA},
        {"id": "alrasha-ibumas", "nama": "Klinik Utama Alrasha Ibumas",
         "alamat": "Jl. Hang Lekir No. 18–22, Batu IX, Kec. Tanjungpinang Timur, Kota Tanjungpinang",
         "harga": "alrasha", "dokter": DOKTER_ALRASHA},
    ]},
]

# Daftar datar (nama, alamat) untuk dashboard klinik: satu dashboard per klinik mitra.
KLINIK = [(k["nama"], k["alamat"] or "Alamat menyusul")
          for kota in sorted(MITRA, key=lambda m: m["id"] != "tanjungpinang") for k in kota["klinik"]]

# ---------------------------------------------------------------- alur reservasi
ALUR_RESERVASI = [
    "Booking via Call Center atau langsung di klinik",
    "Konsultasi kebutuhan vaksin: di klinik, home care, atau on site perusahaan",
    "Menjadwalkan janji vaksin",
    "Datang ke klinik sesuai jadwal yang sudah ditentukan",
    "Konsultasi dokter dan tindakan vaksinasi",
    "Melakukan pembayaran",
    "Penerbitan e-ICV (International Certificate of Vaccination) khusus vaksin internasional",
]
