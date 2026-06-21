import streamlit as st
import time

# --- 1. LAYOUT & CSS ---
st.set_page_config(page_title="Orochi Realm", page_icon="🐍", layout="centered")

st.markdown("""
    <style>
    /* Background polos agar bersih */
    .stApp { background-color: #0e1117; }
    
    /* Container Orochi agar tetap utuh dan tidak terpotong */
    .orochi-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-top: 20px;
    }
    
    /* Memastikan gambar Orochi selalu tampil penuh */
    .orochi-img {
        width: 100%;
        max-width: 500px;
        height: auto;
        border-radius: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. LOGIKA STATE ---
if "status" not in st.session_state: st.session_state.status = "diam"

# --- 3. TAMPILAN ---
st.title("Orochi Realm")

# Menampilkan Orochi sebagai elemen gambar, bukan background CSS
# Ini menjamin Orochi TIDAK akan terpotong
st.markdown("<div class='orochi-container'>", unsafe_allow_html=True)
st.image(f"{st.session_state.status.capitalize()}.gif", use_container_width=False) 
st.markdown("</div>", unsafe_allow_html=True)

# Tombol Kontrol
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Diam"): st.session_state.status = "diam"; st.rerun()
with col2:
    if st.button("Berfikir"): st.session_state.status = "berfikir"; st.rerun()
with col3:
    if st.button("Tidur"): st.session_state.status = "tidur"; st.rerun()

prompt = st.text_input("Perintah:")
if prompt:
    st.write(f"Orochi: Memproses '{prompt}'...")
    time.sleep(2)
    st.session_state.status = "diam"; st.rerun()
