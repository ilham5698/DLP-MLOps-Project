import pandas as pd
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader
import docx

REGISTRY_PATH = "registry"
if not os.path.exists(REGISTRY_PATH):
    os.makedirs(REGISTRY_PATH)

def baca_file_apapun(file):
    """Mengekstrak teks dari PDF, DOCX, atau TXT"""
    teks = ""
    try:
        if file.name.endswith(".pdf"):
            reader = PdfReader(file)
            for page in reader.pages:
                teks += page.extract_text() + "\n"
        elif file.name.endswith(".docx"):
            doc = docx.Document(file)
            for para in doc.paragraphs:
                teks += para.text + "\n"
        else:
            teks = file.read().decode("utf-8")
        return teks
    except Exception as e:
        return ""

def cek_kebocoran(teks_input):
    """Proses perbandingan teks dengan database rahasia"""
    if not os.path.exists("dataset_rahasia.csv"):
        return 0.0, "Database Tidak Ditemukan", "Error"
    
    df = pd.read_csv("dataset_rahasia.csv")
    list_rahasia = df['Isi'].astype(str).tolist()
    
    model_file = os.path.join(REGISTRY_PATH, "vectorizer_v1.pkl")
    matrix_file = os.path.join(REGISTRY_PATH, "matrix_v1.pkl")

    if os.path.exists(model_file) and os.path.exists(matrix_file):
        vectorizer = joblib.load(model_file)
        tfidf_matrix = joblib.load(matrix_file)
    else:
        # Latih model jika belum ada
        vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(3, 3))
        tfidf_matrix = vectorizer.fit_transform(list_rahasia)
        joblib.dump(vectorizer, model_file)
        joblib.dump(tfidf_matrix, matrix_file)

    tfidf_input = vectorizer.transform([teks_input.lower()])
    sim = cosine_similarity(tfidf_input, tfidf_matrix)
    
    skor = float(sim.max())
    idx = sim.argmax()
    kategori = df.iloc[idx]['Kategori']
    
    return skor, kategori, "Sukses"