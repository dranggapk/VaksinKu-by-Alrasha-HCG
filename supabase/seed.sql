-- Dibuat oleh src/buat_seed_supabase.py dari src/data_katalog.py — jangan disunting manual.
-- Aman dijalankan ulang: baris yang sudah ada diperbarui.

insert into public.kota (id, nama) values
  ('bandung', 'Kota Bandung'),
  ('tanjungpinang', 'Kota Tanjungpinang')
on conflict (id) do update set nama = excluded.nama;

insert into public.klinik (id, kota_id, nama, alamat) values
  ('jasmine-mq', 'bandung', 'Klinik Utama Jasmine MQ Medika', ''),
  ('alrasha-hcc', 'tanjungpinang', 'Klinik Alrasha Health Care Center', 'Jl. Hang Lekir, Batu 10, No. 21–22, Tanjungpinang'),
  ('alrasha-ibumas', 'tanjungpinang', 'Klinik Utama Alrasha Ibumas', 'Jl. Hang Lekir, Batu 10, No. 18–20, Tanjungpinang')
on conflict (id) do update set kota_id = excluded.kota_id, nama = excluded.nama, alamat = excluded.alamat;

insert into public.vaksin (id, kategori, sediaan, merek, antigen) values
  ('v1-0', 'BCG (TBC)', 'BCG Private', 'BCG Biofarma', '{bcg}'),
  ('v1-1', 'BCG (TBC)', 'BCG Group (min 3 orang)', 'BCG Biofarma', '{bcg}'),
  ('v2-2', 'Polio', 'Polio Oral', 'Polio Tetes', '{polio}'),
  ('v2-3', 'Polio', 'Polio IPV', 'Polio Injeksi (IPV)', '{ipv}'),
  ('v3-4', 'DPT / DPT Combo', 'DPaT + IPV + HIB + HB', 'Infanrix Hexa', '{dtp,hib,hepb,ipv}'),
  ('v3-5', 'DPT / DPT Combo', 'DPaT + IPV + HIB + HB', 'Hexaxim', '{dtp,hib,hepb,ipv}'),
  ('v3-6', 'DPT / DPT Combo', 'DPaT + HIB + HB', 'Pentabio', '{dtp,hib,hepb}'),
  ('v4-7', 'Rotavirus (diare)', 'Rotateq (pentavalen)', 'Rotateq', '{rv}'),
  ('v4-8', 'Rotavirus (diare)', 'Rotarix (monovalen)', 'Rotarix susp', '{rv}'),
  ('v5-9', 'Meningitis', 'Menivax', 'Menivax', '{}'),
  ('v6-10', 'Pneumococcus', 'PCV (20) – pneumonia / IPD', 'Prevenar 20', '{pcv}'),
  ('v7-11', 'Influenza', '4 strain', 'Vaxigrip Tetra', '{flu}'),
  ('v7-12', 'Influenza', 'Flubio', 'Flubio', '{flu}'),
  ('v8-13', 'Typhoid (Tipes)', 'Typhim Vi', 'Typhim', '{tif}'),
  ('v9-14', 'Tetanus', 'Tdap', 'Adacel', '{td}'),
  ('v10-15', 'Campak + Rubella', 'Campak + Rubella', 'MR Group', '{mr}'),
  ('v10-16', 'Campak + Rubella', 'Campak + Rubella', 'MR Private', '{mr}'),
  ('v10-17', 'Campak + Rubella', 'Measles, Mumps, Rubella', 'MMR', '{mr}'),
  ('v11-18', 'Varicella', 'Varicella', 'Varicella', '{var}'),
  ('v11-19', 'Varicella', 'Varicella', 'Varivax', '{var}'),
  ('v12-20', 'Hepatitis B', 'Engerix-B Anak', 'Engerix-B Anak', '{hepb}'),
  ('v12-21', 'Hepatitis B', 'Engerix-B Dewasa', 'Engerix-B Dewasa', '{hepb}'),
  ('v13-22', 'Hepatitis A', 'Avaxim Anak', 'Avaxim Anak', '{hepa}'),
  ('v13-23', 'Hepatitis A', 'Avaxim Dewasa', 'Avaxim Dewasa', '{hepa}'),
  ('v14-24', 'HPV (Kanker Serviks)', 'HPV 2 valen', 'Gardasil', '{hpv}'),
  ('v14-25', 'HPV (Kanker Serviks)', 'HPV 9 valen', 'Gardasil 9', '{hpv}'),
  ('v15-26', 'Demam Berdarah', 'Qdenga', 'Qdenga', '{dbd}'),
  ('v16-27', 'Japanese Encephalitis', 'Imojev', 'Imojev', '{je}'),
  ('v17-28', 'Flu Singapura', 'Inlive VACC', 'Inlive VACC', '{hfmd}')
on conflict (id) do update set kategori = excluded.kategori, sediaan = excluded.sediaan,
  merek = excluded.merek, antigen = excluded.antigen;

insert into public.harga_klinik (klinik_id, vaksin_id, harga_umum, harga_spesialis) values
  ('alrasha-hcc', 'v1-0', 465000, 550000),
  ('alrasha-hcc', 'v1-1', 235000, 285000),
  ('alrasha-hcc', 'v2-2', 130000, 200000),
  ('alrasha-hcc', 'v2-3', 305000, 355000),
  ('alrasha-hcc', 'v3-4', 1000000, 1095000),
  ('alrasha-hcc', 'v3-5', 950000, 1050000),
  ('alrasha-hcc', 'v3-6', 360000, 400000),
  ('alrasha-hcc', 'v4-7', 475000, 525000),
  ('alrasha-hcc', 'v4-8', 495000, 550000),
  ('alrasha-hcc', 'v5-9', 345000, null),
  ('alrasha-hcc', 'v6-10', 1100000, 1200000),
  ('alrasha-hcc', 'v7-11', 400000, 450000),
  ('alrasha-hcc', 'v7-12', 325000, 375000),
  ('alrasha-hcc', 'v8-13', 425000, 450000),
  ('alrasha-hcc', 'v9-14', 525000, 575000),
  ('alrasha-hcc', 'v10-15', 375000, 450000),
  ('alrasha-hcc', 'v10-16', 900000, 975000),
  ('alrasha-hcc', 'v10-17', 575000, 690000),
  ('alrasha-hcc', 'v11-18', 600000, 650000),
  ('alrasha-hcc', 'v11-19', 750000, 805000),
  ('alrasha-hcc', 'v12-20', 300000, 350000),
  ('alrasha-hcc', 'v12-21', 325000, 375000),
  ('alrasha-hcc', 'v13-22', 500000, 550000),
  ('alrasha-hcc', 'v13-23', 565000, 600000),
  ('alrasha-hcc', 'v14-24', 1250000, 1300000),
  ('alrasha-hcc', 'v14-25', 2350000, 2400000),
  ('alrasha-hcc', 'v15-26', 650000, 700000),
  ('alrasha-hcc', 'v16-27', 550000, 600000),
  ('alrasha-hcc', 'v17-28', 1075000, 1125000),
  ('alrasha-ibumas', 'v1-0', 465000, 550000),
  ('alrasha-ibumas', 'v1-1', 235000, 285000),
  ('alrasha-ibumas', 'v2-2', 130000, 200000),
  ('alrasha-ibumas', 'v2-3', 305000, 355000),
  ('alrasha-ibumas', 'v3-4', 1000000, 1095000),
  ('alrasha-ibumas', 'v3-5', 950000, 1050000),
  ('alrasha-ibumas', 'v3-6', 360000, 400000),
  ('alrasha-ibumas', 'v4-7', 475000, 525000),
  ('alrasha-ibumas', 'v4-8', 495000, 550000),
  ('alrasha-ibumas', 'v5-9', 345000, null),
  ('alrasha-ibumas', 'v6-10', 1100000, 1200000),
  ('alrasha-ibumas', 'v7-11', 400000, 450000),
  ('alrasha-ibumas', 'v7-12', 325000, 375000),
  ('alrasha-ibumas', 'v8-13', 425000, 450000),
  ('alrasha-ibumas', 'v9-14', 525000, 575000),
  ('alrasha-ibumas', 'v10-15', 375000, 450000),
  ('alrasha-ibumas', 'v10-16', 900000, 975000),
  ('alrasha-ibumas', 'v10-17', 575000, 690000),
  ('alrasha-ibumas', 'v11-18', 600000, 650000),
  ('alrasha-ibumas', 'v11-19', 750000, 805000),
  ('alrasha-ibumas', 'v12-20', 300000, 350000),
  ('alrasha-ibumas', 'v12-21', 325000, 375000),
  ('alrasha-ibumas', 'v13-22', 500000, 550000),
  ('alrasha-ibumas', 'v13-23', 565000, 600000),
  ('alrasha-ibumas', 'v14-24', 1250000, 1300000),
  ('alrasha-ibumas', 'v14-25', 2350000, 2400000),
  ('alrasha-ibumas', 'v15-26', 650000, 700000),
  ('alrasha-ibumas', 'v16-27', 550000, 600000),
  ('alrasha-ibumas', 'v17-28', 1075000, 1125000)
on conflict (klinik_id, vaksin_id) do update set harga_umum = excluded.harga_umum,
  harga_spesialis = excluded.harga_spesialis;

insert into public.dokter (klinik_id, nama, spesialisasi, inisial)
select v.* from (values
  ('alrasha-hcc', 'dr. Dwi Fachri JH, Sp.A', 'Dokter Spesialis Anak', 'DF'),
  ('alrasha-hcc', 'dr. Augustine PA, Sp.PD, FINASIM', 'Dokter Spesialis Penyakit Dalam', 'AP'),
  ('alrasha-hcc', 'dr. Leo Andreas, Sp.PD', 'Dokter Spesialis Penyakit Dalam', 'LA'),
  ('alrasha-hcc', 'Tim Dokter Umum', 'Dokter Umum vaksinator bersertifikat', 'DU'),
  ('alrasha-ibumas', 'dr. Dwi Fachri JH, Sp.A', 'Dokter Spesialis Anak', 'DF'),
  ('alrasha-ibumas', 'dr. Augustine PA, Sp.PD, FINASIM', 'Dokter Spesialis Penyakit Dalam', 'AP'),
  ('alrasha-ibumas', 'dr. Leo Andreas, Sp.PD', 'Dokter Spesialis Penyakit Dalam', 'LA'),
  ('alrasha-ibumas', 'Tim Dokter Umum', 'Dokter Umum vaksinator bersertifikat', 'DU')
) as v(klinik_id, nama, spesialisasi, inisial)
where not exists (select 1 from public.dokter d where d.klinik_id = v.klinik_id and d.nama = v.nama);
