import streamlit as st
import time

# --- 1. SETTING LAYOUT ---
st.set_page_config(page_title="Orochi Realm", page_icon="🐍", layout="centered")

# --- 2. CSS RESPONSIVE (HP & LAPTOP FRIENDLY) ---
st.markdown("""
    <style>
    /* Mengatur kontainer utama agar tidak terlalu lebar di laptop */
    .block-container { max-width: 600px !important; padding: 1rem !important; }

    /* Membuat Orochi menjadi Background Animasi */
    .stApp {
        background-image: url('https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/Orochi_diam.gif');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

    /* Container untuk elemen di atas background */
    .main-box {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 20px;
        border-radius: 25px;
        color: white;
        text-align: center;
    }

    /* Responsif untuk HP (Layar Kecil) */
    @media (max-width: 600px) {
        .main-box { padding: 10px; }
        h1 { font-size: 24px; }
    }

    /* Styling Tombol */
    div.stButton > button {
        width: 100%;
        background-color: rgba(255,255,255,0.1);
        border: 1px solid white;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA STATE ---
if "status" not in st.session_state: st.session_state.status = "diam"

# --- 4. TAMPILAN ---
st.markdown("<div class='main-box'>", unsafe_allow_html=True)
st.title("Orochi Realm")
st.write(f"Status: **{st.session_state.status.upper()}**")

# Tombol Kontrol
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Diam"): st.session_state.status = "diam"; st.rerun()
with col2:
    if st.button("Berfikir"): st.session_state.status = "berfikir"; st.rerun()
with col3:
    if st.button("Tidur"): st.session_state.status = "tidur"; st.rerun()

# Input Perintah
prompt = st.text_input("Perintah:")
if prompt:
    st.write(f"Orochi: Memproses '{prompt}'...")
    time.sleep(2)
    st.session_state.status = "diam"
st.markdown("</div>", unsafe_allow_html=True)
