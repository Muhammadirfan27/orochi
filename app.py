import streamlit as st
import time

# --- 1. KONFIGURASI LAYOUT ---
# Layout 'wide' untuk memastikan konten memenuhi layar
st.set_page_config(page_title="Orochi Pet", page_icon="🐍", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS GAME-STYLE (FULLSCREEN & RESPONSIVE) ---
st.markdown("""
    <style>
    /* Mengisi seluruh layar dengan warna latar game */
    .stApp { background-color: #0e1117; }
    
    /* Mengatur kontainer utama agar tidak terpotong */
    .block-container { 
        max-width: 100% !important; 
        padding: 0 !important; 
        margin: 0 !important;
    }
    
    /* Layer Game Utama */
    .game-layer {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        height: 95vh;
        width: 100vw;
    }
    
    /* Orochi Display */
    .orochi-box {
        flex-grow: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        padding: 20px;
    }
    .stImage img { 
        border-radius: 40px; 
        max-width: 600px !important;
        width: 100% !important;
    }
    
    /* Control Panel (Tombol & Input) */
    .control-panel {
        width: 100%;
        padding: 20px;
        background: rgba(31, 41, 55, 0.9);
        border-top-left-radius: 30px;
        border-top-right-radius: 30px;
    }
    
    /* Styling Tombol */
    div.stButton > button {
        width: 100%;
        height: 60px;
        font-size: 20px;
        border-radius: 15px;
        background-color: #374151;
        color: white;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. INISIALISASI STATE ---
if "status" not in st.session_state: st.session_state.status = "diam"
if "energy" not in st.session_state: st.session_state.energy = 60

# --- 4. FUNGSI AVATAR ---
def get_avatar(status):
    images = {
        "tidur": "Orochi_tidur.gif",
        "diam": "Orochi_diam.gif",
        "berfikir": "Orochi_berfikir.gif",
        "bicara": "Orochi_bicara.gif"
    }
    return images.get(status, "Orochi_diam.gif")

# --- 5. TAMPILAN GAME (LAYOUT FULL) ---
st.markdown("<div class='game-layer'>", unsafe_allow_html=True)

# Area Gambar
st.markdown("<div class='orochi-box'>", unsafe_allow_html=True)
st.image(get_avatar(st.session_state.status))
st.markdown("</div>", unsafe_allow_html=True)

# Area Kontrol
st.markdown("<div class='control-panel'>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: white;'>⚡ Energi: {st.session_state.energy}% | Status: {st.session_state.status.upper()}</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("❤️"): 
        st.session_state.status = "diam"; st.session_state.energy = min(100, st.session_state.energy + 5); st.rerun()
with col2:
    if st.button("💡"): st.session_state.status = "berfikir"; st.rerun()
with col3:
    if st.button("💤"): st.session_state.status = "tidur"; st.rerun()

prompt = st.text_input("", placeholder="Tulis perintah untuk Orochi...")
if prompt:
    st.session_state.status = "bicara"
    st.write(f"💬 Orochi: Memproses '{prompt}'...")
    time.sleep(3)
    st.session_state.status = "diam"
    st.rerun()

st.markdown("</div></div>", unsafe_allow_html=True)

# Auto-reset animasi agar tidak stuck
if st.session_state.status in ["berfikir", "bicara"]:
    time.sleep(3)
    st.session_state.status = "diam"
    st.rerun()
