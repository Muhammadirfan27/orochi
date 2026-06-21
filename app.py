import streamlit as st
import time

# --- 1. SETTING LAYOUT ---
st.set_page_config(page_title="Orochi Realm", page_icon="🐍", layout="centered")

# --- 2. CSS RESPONSIVE & CLEAN UI ---
st.markdown("""
    <style>
    /* Background polos gelap ala aplikasi game */
    .stApp { background-color: #0e1117; }
    
    /* Mengatur kontainer agar proporsional */
    .block-container { 
        max-width: 600px !important; 
        padding: 2rem !important; 
    }
    
    /* Styling Orochi agar selalu utuh dan berada di tengah */
    .orochi-box {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .stImage img { 
        border-radius: 30px !important;
        width: 100% !important;
    }
    
    /* Tombol Game Style */
    div.stButton > button {
        width: 100%;
        background-color: #1f2937;
        color: white;
        border: 1px solid #4b5563;
        border-radius: 15px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA STATE ---
if "status" not in st.session_state: st.session_state.status = "diam"

# Fungsi untuk memanggil file GIF
def get_avatar(status):
    images = {
        "tidur": "Orochi_tidur.gif",
        "diam": "Orochi_diam.gif",
        "berfikir": "Orochi_berfikir.gif",
        "bicara": "Orochi_bicara.gif"
    }
    return images.get(status, "Orochi_diam.gif")

# --- 4. TAMPILAN UTAMA ---
st.markdown("<h1 style='text-align: center; color: white;'>Orochi Realm</h1>", unsafe_allow_html=True)

# Area Gambar Orochi (Terbungkus rapi agar tidak terpotong)
st.markdown("<div class='orochi-box'>", unsafe_allow_html=True)
st.image(get_avatar(st.session_state.status))
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center; color: #9ca3af;'>Status: {st.session_state.status.upper()}</p>", unsafe_allow_html=True)

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
    st.session_state.status = "bicara"
    st.write(f"💬 Orochi: Memproses '{prompt}'...")
    time.sleep(3)
    st.session_state.status = "diam"
    st.rerun()
