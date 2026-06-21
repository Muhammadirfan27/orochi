import streamlit as st
import time

# --- 1. LAYOUT WIDE ---
st.set_page_config(page_title="Orochi World", page_icon="🐍", layout="wide")

# --- 2. CSS BACKGROUND ANIMASI ---
st.markdown("""
    <style>
    /* Mengatur GIF menjadi Background */
    .stApp {
        background-image: url('https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/Orochi_diam.gif');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    
    /* Memberi efek transparan pada container agar background Orochi terlihat */
    .main .block-container {
        background-color: rgba(0, 0, 0, 0.6); /* Hitam transparan */
        border-radius: 30px;
        padding: 40px;
        color: white;
    }
    
    /* Tombol supaya lebih kontras di atas background */
    div.stButton > button {
        background-color: rgba(255, 255, 255, 0.2);
        color: white;
        border: 1px solid white;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA STATE ---
if "status" not in st.session_state: st.session_state.status = "diam"

# --- 4. TAMPILAN ---
st.markdown("<h1 style='text-align: center;'>Orochi Realm</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>Status: {st.session_state.status.upper()}</p>", unsafe_allow_html=True)

# Tombol kontrol di depan background
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Diam"): st.session_state.status = "diam"; st.rerun()
with col2:
    if st.button("Berfikir"): st.session_state.status = "berfikir"; st.rerun()
with col3:
    if st.button("Tidur"): st.session_state.status = "tidur"; st.rerun()

# --- 5. CHAT AREA ---
prompt = st.text_input("Perintah:")
if prompt:
    st.write(f"Orochi: Memproses '{prompt}'...")
    time.sleep(2)
