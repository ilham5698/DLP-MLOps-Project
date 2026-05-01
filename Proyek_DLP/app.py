import streamlit as st
import pandas as pd
import os
import datetime
from dlp_otak import cek_kebocoran, baca_file_apapun

# --- CONFIG ---
st.set_page_config(page_title="🛡️ SOC DLP CENTER", layout="wide")

# --- UI STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    h1, h2, h3 { color: #58a6ff !important; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 15px; }
    .stButton>button { background: linear-gradient(to right, #1f6feb, #58a6ff); color: white; border: none; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE USER & LOG ---
USERS = {"admin": "admin123", "user": "user123"}

def tulis_log(user, kategori, skor, status):
    log_file = "monitoring_log.csv"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_baru = pd.DataFrame([[timestamp, user, kategori, skor, status]], 
                           columns=['Timestamp', 'User', 'Kategori', 'Skor', 'Status'])
    if not os.path.isfile(log_file):
        df_baru.to_csv(log_file, index=False)
    else:
        df_baru.to_csv(log_file, mode='a', header=False, index=False)

# --- SESSION LOGIN ---
if "auth" not in st.session_state: st.session_state["auth"] = False

if not st.session_state["auth"]:
    st.markdown("<h1 style='text-align: center;'>🔐 SOC TERMINAL LOGIN</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        u = st.text_input("Username")
        p = st.text_input("Access Key", type="password")
        if st.button("LOGIN"):
            if u in USERS and USERS[u] == p:
                st.session_state.update({"auth": True, "user": u})
                st.rerun()
            else: st.error("Invalid Credentials")
    st.stop()

# --- SIDEBAR ---
st.sidebar.markdown(f"### 🟢 Operator: `{st.session_state['user']}`")
if st.sidebar.button("LOGOUT"):
    st.session_state["auth"] = False
    st.rerun()

# --- MAIN INTERFACE ---
st.title("🛡️ DLP COMMAND CENTER")
tab1, tab2 = st.tabs(["🔍 THREAT SCANNER", "📊 SECURITY ANALYTICS"])

with tab1:
    col_a, col_b = st.columns([2,1])
    with col_a:
        msg = st.text_area("Input Message Context:", height=100)
        file = st.file_uploader("Evidence Attachment:", type=["pdf", "docx", "txt"])
    with col_b:
        st.info("Sistem akan menggabungkan teks dan lampiran untuk dianalisis AI.")
        thr = st.slider("Sensitivity Threshold", 0.1, 1.0, 0.4)

    if st.button("🚀 EXECUTE SECURITY SCAN"):
        content = msg
        if file:
            content += "\n" + baca_file_apapun(file)
        
        if not content.strip():
            st.warning("No data to scan.")
        else:
            with st.spinner("Analyzing Pipeline..."):
                skor, kat, stat = cek_kebocoran(content)
                hasil = "BAHAYA" if skor > thr else "AMAN"
                kat_log = kat if hasil == "BAHAYA" else "Aman"
                
                tulis_log(st.session_state["user"], kat_log, skor, hasil)
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    color = "#ff7b72" if hasil == "BAHAYA" else "#56d364"
                    st.markdown(f"<div style='border:2px solid {color}; border-radius:10px; text-align:center;'><h2 style='color:{color};'>{hasil}</h2></div>", unsafe_allow_html=True)
                with c2: st.metric("Detection Category", kat_log)
                with c3: st.metric("Risk Level", f"{skor:.2%}")

with tab2:
    if st.session_state["user"] == "admin":
        if os.path.exists("monitoring_log.csv"):
            df = pd.read_csv("monitoring_log.csv")
            st.markdown("### 📈 Real-time Traffic")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Events", len(df))
            col2.metric("Threats Detected", len(df[df['Status'] == 'BAHAYA']))
            col3.metric("Safety Rate", f"{(len(df[df['Status'] == 'AMAN'])/len(df) if len(df)>0 else 0):.1%}")
            
            st.bar_chart(df['Kategori'].value_counts())
            st.markdown("### 📑 Detailed Audit Logs")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Audit log is empty. Start scanning first.")
    else:
        st.error("Admin privileges required for Analytics Dashboard.")