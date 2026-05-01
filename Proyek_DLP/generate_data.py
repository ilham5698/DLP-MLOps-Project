import pandas as pd
import random
import string

categories = ["IT Security", "Keuangan", "HRD", "Strategi"]
data_rows = []

for i in range(5000):
    kat = random.choice(categories)
    if kat == "IT Security":
        isi = f"Server IP {random.randint(1,255)}.{random.randint(1,255)} API: {''.join(random.choices(string.ascii_uppercase, k=10))}"
    elif kat == "Keuangan":
        isi = f"Transfer Rp {random.randint(1,100)*1000000} ke Rekening {random.randint(10000000,99999999)}"
    elif kat == "HRD":
        isi = f"Data Gaji NIK {random.randint(1000,9999)} atas nama Karyawan-{random.randint(1,100)}"
    else:
        isi = f"Rencana Proyek Rahasia Strategis Kode-{random.randint(100,999)}"
    data_rows.append({"Kategori": kat, "Isi": isi})

pd.DataFrame(data_rows).to_csv("dataset_rahasia.csv", index=False)
print("✅ Dataset Berhasil Dibuat!")