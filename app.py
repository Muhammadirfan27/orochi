import streamlit as st
import time

# --- 1. KONFIGURASI LAYOUT ---
st.set_page_config(page_title="Orochi", page_icon="🐍", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS ABSOLUTE POSITIONING (FULLSCREEN & NYATU) ---
st.markdown("""
    <style>
    /* Hilangkan semua padding bawaan Streamlit */
    [data-testid="stAppViewContainer"] { padding: 0 !important; }
    [data-testid="stHeader"] { display: none; }
    
    .orochi-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        width: 100vw;
        background-color: #0e1117;
    }
    
    /* Orochi tidak akan terpotong */
    .orochi-img {
        max-width: 90vw;
        max-height: 60vh;
        border-radius: 40px;
        margin-bottom: 20px;
    }
    
    /* Kontrol menyatu tepat di bawah Orochi */
    .controls {
        display: flex;
        gap: 15px;
        margin-bottom: 20px;
    }
    
    .input-box {
        width: 80vw;
        max-width: 500px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA STATE ---
if "status" not in st.session_state: st.session_state.status = "diam"

def get_avatar(status):
    images = {"tidur": "Orochi_tidur.gif", "diam": "Orochi_diam.gif", "berfikir": "Orochi_berfikir.gif", "bicara": "Orochi_bicara.gif"}
    return images.get(status, "Orochi_diam.gif")

# --- 4. RENDER LAYOUT ---
st.markdown("<div class='orochi-wrapper'>", unsafe_allow_html=True)

# Orochi
st.image(get_avatar(st.session_state.status), use_container_width=False, output_format="GIF")
# Tambahkan class CSS manual via st.markdown karena st.image terbatas
st.markdown(f"<style>.stImage img {{ max-width: 80vw !important; max-height: 50vh !important; border-radius: 30px; }}</style>", unsafe_allow_html=True)

# Kontrol menyatu
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("❤️"): st.session_state.status = "diam"; st.rerun()
with col2:
    if st.button("💡"): st.session_state.status = "berfikir"; st.rerun()
with col3:
    if st.button("💤"): st.session_state.status = "tidur"; st.rerun()

# Perintah menyatu
prompt = st.text_input("", placeholder="Perintah untuk Orochi...")
if prompt:
    st.session_state.status = "bicara"
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Auto Reset
if st.session_state.status in ["berfikir", "bicara"]:
    time.sleep(3)
    st.session_state.status = "diam"
    st.rerun()
