import joblib

# Memuat vectorizer
try:
    vectorizer = joblib.load('registry/vectorizer_v1.pkl')
    print("✅ Berhasil memuat Vectorizer")
    print("Jumlah fitur kata:", len(vectorizer.get_feature_names_out()))
    print("Contoh fitur (n-gram):", vectorizer.get_feature_names_out()[:10])

    print("-" * 30)

    # Memuat matrix
    matrix = joblib.load('registry/matrix_v1.pkl')
    print("✅ Berhasil memuat Matrix")
    print("Bentuk matrix (Baris Data x Fitur):", matrix.shape)
except Exception as e:
    print(f"❌ Gagal membaca file: {e}")