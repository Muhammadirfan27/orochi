import streamlit as st
import time

# --- 1. KONFIGURASI LAYOUT ---
# 'wide' dan 'collapsed' sidebar memaksimalkan ruang layar
st.set_page_config(page_title="Orochi Pet", page_icon="🐍", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS GAME-STYLE (POU INSPIRED) ---
st.markdown("""
    <style>
    /* Mengisi seluruh latar belakang */
    .stApp { background-color: #0e1117; }
    
    /* Menghapus padding agar benar-benar penuh */
    .block-container { 
        max-width: 100% !important; 
        padding: 0 !important; 
        margin: 0 !important;
    }
    
    /* Layer Game Utama: Orochi di atas, Kontrol di bawah */
    .game-viewport {
        display: flex;
        flex-direction: column;
        height: 100vh;
        justify-content: space-between;
    }
    
    /* Area Orochi */
    .orochi-display {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    .orochi-display img {
        width: 100% !important;
        max-width: 500px !important;
        border-radius: 40px;
    }
    
    /* Area Panel Kontrol bawah */
    .control-panel {
        background: rgba(30, 41, 59, 0.95);
        padding: 20px;
        border-top-left-radius: 40px;
        border-top-right-radius: 40px;
    }
    
    /* Tombol bulat ala Game */
    div.stButton > button {
        width: 100%;
        height: 70px;
        border-radius: 35px;
        background-color: #374151;
        color: white;
        font-weight: bold;
        border: 2px solid #4b5563;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. STATE & FUNGSI ---
if "status" not in st.session_state: st.session_state.status = "diam"

def get_avatar(status):
    images = {
        "tidur": "Orochi_tidur.gif",
        "diam": "Orochi_diam.gif",
        "berfikir": "Orochi_berfikir.gif",
        "bicara": "Orochi_bicara.gif"
    }
    return images.get(status, "Orochi_diam.gif")

# --- 4. RENDER LAYOUT ---
st.markdown("<div class='game-viewport'>", unsafe_allow_html=True)

# Area Karakter
st.markdown("<div class='orochi-display'>", unsafe_allow_html=True)
st.image(get_avatar(st.session_state.status))
st.markdown("</div>", unsafe_allow_html=True)

# Area Panel Bawah
st.markdown("<div class='control-panel'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("❤️"): st.session_state.status = "diam"; st.rerun()
with col2:
    if st.button("💡"): st.session_state.status = "berfikir"; st.rerun()
with col3:
    if st.button("💤"): st.session_state.status = "tidur"; st.rerun()

prompt = st.text_input("", placeholder="Perintah untuk Orochi...")
if prompt:
    st.session_state.status = "bicara"
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Auto Reset status setelah 3 detik
if st.session_state.status in ["berfikir", "bicara"]:
    time.sleep(3)
    st.session_state.status = "diam"
    st.rerun()
