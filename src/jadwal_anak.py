# -*- coding: utf-8 -*-
"""Jadwal imunisasi anak per dosis: IDAI 2024 dan Buku KIA 2024 (program pemerintah).

Satu dosis = satu baris ceklis. Kolom usia dalam BULAN GENAP yang sudah dijalani
(umur 2 bulan 20 hari dihitung 2), sama dengan cara membaca kolom tabel IDAI:
"2 berarti mulai usia 60 hari sampai 89 hari".

  mulai   usia paling awal dosis diberikan
  tepat   akhir rentang usia tepat (sel putih KIA / sel biru-hijau IDAI)
  boleh   akhir rentang "masih boleh dilengkapi" (sel kuning); None = sama dengan batas
  batas   usia terakhir dosis masih boleh diberikan (catch-up / imunisasi kejar).
          Lewat dari ini dosis ditampilkan "terlewat" dan tidak dihitung kurang.
  kunci   antigen:urutan yang dipenuhi dosis ini. Riwayat disimpan per kunci,
          sehingga dosis yang sama terbaca di kedua jadwal (DPT-HB-Hib 1 di KIA
          memenuhi DTP 1, Hib 1, dan Hepatitis B 1 di IDAI).
  program True bila tersedia gratis di Puskesmas/Posyandu (program pemerintah).
  syarat  '' wajib · 'endemis' hanya daerah endemis JE · 'perempuan' anak perempuan
          · 'rv5' hanya bila memakai Rotateq (RV5) · 'tambahan' di luar jadwal rujukan
  ulang   bulan; dosis berulang (flu tiap 12, tifoid tiap 36) dihitung dari dosis terakhir.

Sumber: Jadwal Imunisasi Anak 0–18 Tahun, Rekomendasi IDAI 2024 (tabel & catatan),
dan Buku KIA 2024 hlm. 124–125 "Pelayanan Imunisasi" + jadwal BIAS sekolah.
Usia 18 tahun = 216 bulan.
"""

T18 = 216  # akhir usia anak


def dosis(id, baris, label, kunci, mulai, tepat, batas, boleh=None, jenis="primer",
          program=False, syarat="", ket="", ulang=0):
    return {
        "id": id, "baris": baris, "label": label, "kunci": kunci if isinstance(kunci, list) else [kunci],
        "mulai": mulai, "tepat": tepat, "boleh": batas if boleh is None else boleh, "batas": batas,
        "jenis": jenis, "program": program, "syarat": syarat, "ket": ket, "ulang": ulang,
    }


# ------------------------------------------------------------------- IDAI 2024
IDAI = [
    dosis("hb0", "Hepatitis B", "Hepatitis B 0", "hepb:0", 0, 0, 1, program=True,
          ket="Segera setelah lahir, sebelum 24 jam (didahului vitamin K1)"),
    dosis("hb1", "Hepatitis B", "Hepatitis B 1", "hepb:1", 2, 2, T18, program=True, ket="Biasanya dalam vaksin kombinasi"),
    dosis("hb2", "Hepatitis B", "Hepatitis B 2", "hepb:2", 3, 3, T18, program=True),
    dosis("hb3", "Hepatitis B", "Hepatitis B 3", "hepb:3", 4, 4, T18, program=True),
    dosis("hb4", "Hepatitis B", "Hepatitis B 4", "hepb:4", 18, 18, T18, jenis="booster", program=True),

    dosis("p0", "Polio", "Polio 0 (tetes)", "polio:0", 0, 1, T18, program=True, ket="bOPV saat lahir / pulang dari RS"),
    dosis("p1", "Polio", "Polio 1", "polio:1", 2, 2, T18, program=True),
    dosis("p2", "Polio", "Polio 2", "polio:2", 3, 3, T18, program=True),
    dosis("p3", "Polio", "Polio 3", "polio:3", 4, 4, T18, program=True),
    dosis("p4", "Polio", "Polio 4", "polio:4", 18, 18, T18, jenis="booster"),
    dosis("ipv1", "Polio suntik (IPV)", "IPV 1", "ipv:1", 4, 4, T18, program=True, ket="Minimal 2× IPV sesuai panduan Kemenkes"),
    dosis("ipv2", "Polio suntik (IPV)", "IPV 2", "ipv:2", 9, 9, T18, program=True),

    dosis("bcg", "BCG", "BCG", "bcg:1", 0, 0, 14, program=True,
          ket="Lahir s.d. sebelum 1 bulan. Usia ≥3 bulan: uji tuberkulin dulu"),

    dosis("dtp1", "DTP", "DTP 1", "dtp:1", 2, 2, 83, program=True),
    dosis("dtp2", "DTP", "DTP 2", "dtp:2", 3, 3, 83, program=True),
    dosis("dtp3", "DTP", "DTP 3", "dtp:3", 4, 4, 83, program=True),
    dosis("dtp4", "DTP", "DTP 4", "dtp:4", 18, 18, 59, jenis="booster", program=True),
    dosis("dtp5", "DTP", "DTP 5", "dtp:5", 60, 95, 119, jenis="booster", program=True, ket="Usia 5–7 tahun"),
    dosis("td1", "DTP", "Td / Tdap", "td:1", 120, T18, T18, jenis="booster", program=True, ket="Usia 10–18 tahun"),

    dosis("hib1", "Hib", "Hib 1", "hib:1", 2, 2, 59, program=True),
    dosis("hib2", "Hib", "Hib 2", "hib:2", 3, 3, 59, program=True),
    dosis("hib3", "Hib", "Hib 3", "hib:3", 4, 4, 59, program=True),
    dosis("hib4", "Hib", "Hib 4", "hib:4", 18, 18, 59, jenis="booster", program=True),

    dosis("pcv1", "PCV", "PCV 1", "pcv:1", 2, 2, 59, program=True),
    dosis("pcv2", "PCV", "PCV 2", "pcv:2", 4, 4, 59, program=True),
    dosis("pcv3", "PCV", "PCV 3", "pcv:3", 6, 6, 59, program=True),
    dosis("pcv4", "PCV", "PCV 4", "pcv:4", 12, 14, 59, jenis="booster",
          ket="Jumlah dosis kejar bergantung usia mulai — konsultasikan dengan dokter"),

    dosis("rv1", "Rotavirus", "Rotavirus 1", "rv:1", 2, 2, 2, program=True, ket="Dosis pertama usia 6–12 minggu"),
    dosis("rv2", "Rotavirus", "Rotavirus 2", "rv:2", 4, 4, 5, program=True, ket="Rotarix (RV1) selesai di dosis ini, paling lambat 24 minggu"),
    dosis("rv3", "Rotavirus", "Rotavirus 3", "rv:3", 6, 6, 7, program=True, syarat="rv5",
          ket="Hanya untuk Rotateq (RV5), paling lambat 32 minggu"),

    dosis("flu1", "Influenza", "Influenza 1", "flu:1", 6, 6, T18),
    dosis("flu2", "Influenza", "Influenza 2", "flu:2", 7, 7, T18, ket="4 minggu setelah dosis 1 (seri pertama usia <9 tahun)"),
    dosis("flu", "Influenza", "Influenza tahunan", "flu:t", 18, T18, T18, jenis="booster", ulang=12, ket="Diulang setiap tahun 1 dosis"),

    dosis("mr1", "MR / MMR", "MR 1", "mr:1", 9, 9, T18, program=True),
    dosis("mr2", "MR / MMR", "MR / MMR 2", "mr:2", 15, 18, T18, program=True),
    dosis("mr3", "MR / MMR", "MR / MMR 3", "mr:3", 60, 83, T18, jenis="booster", program=True, ket="Usia 5–7 tahun"),

    dosis("je1", "JE", "Japanese Encephalitis 1", "je:1", 9, 9, T18, syarat="endemis", program=True,
          ket="Untuk yang tinggal di / akan ke daerah endemis ≥1 bulan"),
    dosis("je2", "JE", "Japanese Encephalitis 2", "je:2", 24, 24, T18, jenis="booster", syarat="endemis"),

    dosis("var1", "Varisela", "Varisela 1", "var:1", 12, 15, T18),
    dosis("var2", "Varisela", "Varisela 2", "var:2", 14, 18, T18, ket="6 minggu–3 bulan setelah dosis 1"),

    dosis("hepa1", "Hepatitis A", "Hepatitis A 1", "hepa:1", 12, 23, T18),
    dosis("hepa2", "Hepatitis A", "Hepatitis A 2", "hepa:2", 18, 23, T18, ket="6–18 bulan setelah dosis 1"),

    dosis("tif1", "Tifoid", "Tifoid 1", "tif:1", 24, 24, T18),
    dosis("tif", "Tifoid", "Tifoid ulangan", "tif:t", 60, T18, T18, jenis="booster", ulang=36, ket="Diulang setiap 3 tahun"),

    dosis("dbd1", "Dengue", "Dengue 1", "dbd:1", 72, T18, T18, ket="Usia 6–45 tahun"),
    dosis("dbd2", "Dengue", "Dengue 2", "dbd:2", 75, T18, T18, ket="3 bulan setelah dosis 1"),

    dosis("hpv1", "HPV", "HPV 1", "hpv:1", 108, 179, T18, syarat="perempuan", program=True,
          ket="Usia 9–14 tahun: 2 dosis. Mulai usia ≥15 tahun: 3 dosis"),
    dosis("hpv2", "HPV", "HPV 2", "hpv:2", 114, 179, T18, syarat="perempuan", program=True, ket="6–12 bulan setelah dosis 1"),

    dosis("hfmd1", "Flu Singapura (EV71)", "Flu Singapura 1", "hfmd:1", 6, 6, 71, syarat="tambahan",
          ket="Tidak termasuk jadwal IDAI 2024 — vaksin tambahan"),
    dosis("hfmd2", "Flu Singapura (EV71)", "Flu Singapura 2", "hfmd:2", 7, 7, 71, syarat="tambahan"),
]

# --------------------------------------------------------------- Buku KIA 2024
# Warna tabel KIA: putih = usia tepat, kuning = masih boleh dilengkapi (bayi &
# baduta), merah muda = imunisasi kejar, abu-abu = tidak boleh diberikan.
KIA = [
    dosis("k-hb0", "", "Hepatitis B (<24 jam)", "hepb:0", 0, 0, 0, program=True, ket="0–24 jam setelah lahir"),
    dosis("k-bcg", "", "BCG", "bcg:1", 0, 1, 11, program=True),
    dosis("k-p1", "", "Polio tetes 1", "polio:0", 0, 1, 59, boleh=11, program=True),
    dosis("k-dpt1", "", "DPT-HB-Hib 1", ["dtp:1", "hib:1", "hepb:1"], 2, 2, 59, boleh=11, program=True),
    dosis("k-p2", "", "Polio tetes 2", "polio:1", 2, 2, 59, boleh=11, program=True),
    dosis("k-rv1", "", "Rotavirus (RV) 1", "rv:1", 2, 2, 4, program=True),
    dosis("k-pcv1", "", "PCV 1", "pcv:1", 2, 2, 59, boleh=11, program=True),
    dosis("k-dpt2", "", "DPT-HB-Hib 2", ["dtp:2", "hib:2", "hepb:2"], 3, 3, 59, boleh=11, program=True),
    dosis("k-p3", "", "Polio tetes 3", "polio:2", 3, 3, 59, boleh=11, program=True),
    dosis("k-rv2", "", "Rotavirus (RV) 2", "rv:2", 3, 3, 5, program=True),
    dosis("k-pcv2", "", "PCV 2", "pcv:2", 3, 3, 59, boleh=11, program=True),
    dosis("k-dpt3", "", "DPT-HB-Hib 3", ["dtp:3", "hib:3", "hepb:3"], 4, 4, 59, boleh=11, program=True),
    dosis("k-p4", "", "Polio tetes 4", "polio:3", 4, 4, 59, boleh=11, program=True),
    dosis("k-ipv1", "", "Polio suntik (IPV) 1", "ipv:1", 4, 4, 59, boleh=11, program=True),
    dosis("k-rv3", "", "Rotavirus (RV) 3", "rv:3", 4, 4, 6, program=True, ket="Paling lambat usia 6 bulan 29 hari"),
    dosis("k-mr1", "", "Campak-Rubella (MR)", "mr:1", 9, 9, 59, boleh=11, program=True),
    dosis("k-ipv2", "", "Polio suntik (IPV) 2", "ipv:2", 9, 9, 59, boleh=11, program=True),
    dosis("k-je", "", "Japanese Encephalitis (JE)", "je:1", 10, 10, 59, boleh=11, program=True, syarat="endemis",
          ket="Hanya di daerah endemis"),
    dosis("k-pcv3", "", "PCV 3", "pcv:3", 12, 12, 59, boleh=23, program=True),
    dosis("k-dpt4", "", "DPT-HB-Hib lanjutan", ["dtp:4", "hib:4", "hepb:4"], 18, 18, 59, boleh=23, jenis="booster", program=True),
    dosis("k-mr2", "", "Campak-Rubella lanjutan", "mr:2", 18, 18, 59, boleh=23, jenis="booster", program=True),
    # BIAS (Bulan Imunisasi Anak Sekolah) — kelas 1 ≈ 7 thn, kelas 2 ≈ 8, kelas 5 ≈ 11, kelas 6 ≈ 12
    dosis("k-bias-mr", "", "MR (BIAS kelas 1)", "mr:3", 84, 95, 179, jenis="booster", program=True),
    dosis("k-bias-dt", "", "DT (BIAS kelas 1)", "dtp:5", 84, 95, 179, jenis="booster", program=True),
    dosis("k-bias-td1", "", "Td (BIAS kelas 2)", "td:1", 96, 107, 179, jenis="booster", program=True),
    dosis("k-bias-td2", "", "Td (BIAS kelas 5)", "td:2", 132, 143, T18, jenis="booster", program=True),
    dosis("k-bias-hpv1", "", "HPV 1 (BIAS kelas 5)", "hpv:1", 132, 143, T18, program=True, syarat="perempuan"),
    dosis("k-bias-hpv2", "", "HPV 2 (BIAS kelas 6)", "hpv:2", 144, 155, T18, program=True, syarat="perempuan"),
]

# Kolom tabel ceklis KIA (bulan), meniru tabel di Buku KIA hlm. 125.
KIA_KOLOM = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 18, 23, 59]

# Riwayat dari versi lama aplikasi (dicatat per label) → kunci dosis.
LABEL_LAMA = {
    "Hep B 0": ["hepb:0"], "Polio 0": ["polio:0"], "BCG": ["bcg:1"],
    "Combo DPT 1": ["dtp:1", "hib:1", "hepb:1", "ipv:1"], "Combo DPT 2": ["dtp:2", "hib:2", "hepb:2", "ipv:2"],
    "Combo DPT 3": ["dtp:3", "hib:3", "hepb:3"], "Combo DPT 4": ["dtp:4", "hib:4", "hepb:4"],
    "Combo DPT 5": ["dtp:5"], "DPT 6 dalam bentuk Tdap": ["td:1"],
    "PCV 1": ["pcv:1"], "PCV 2": ["pcv:2"], "PCV 3": ["pcv:3"], "PCV 4": ["pcv:4"],
    "Rotavirus 1": ["rv:1"], "Rotavirus 2": ["rv:2"], "Rotavirus 3": ["rv:3"],
    "Influenza (Flu) 1": ["flu:1"], "Influenza (Flu) 2": ["flu:2"],
    "HFMD (Flu Singapura) 1": ["hfmd:1"], "HFMD (Flu Singapura) 2": ["hfmd:2"],
    "MR 1": ["mr:1"], "MMR 1": ["mr:2"], "MMR 2": ["mr:3"],
    "Japanese Encephalitis (JE) 1": ["je:1"], "Japanese Encephalitis (JE) 2": ["je:2"],
    "Varicella 1": ["var:1"], "Varicella 2": ["var:2"], "Hepatitis A 1": ["hepa:1"], "Hepatitis A 2": ["hepa:2"],
    "Tifoid (Tipes) 1": ["tif:1"], "Demam Berdarah (DBD) 1": ["dbd:1"], "Demam Berdarah (DBD) 2": ["dbd:2"],
    "HPV 1": ["hpv:1"],
}
