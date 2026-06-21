import streamlit as st
import time

# --- 1. KONFIGURASI LAYOUT WIDE ---
st.set_page_config(page_title="Orochi Pet", page_icon="🐍", layout="wide")

# --- 2. CSS FULL-SCREEN & GAME-STYLE ---
st.markdown("""
    <style>
    /* Mengisi seluruh lebar layar */
    .block-container {
        max-width: 100% !important;
        padding-top: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    /* Orochi Full-size */
    .stImage {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .stImage img { 
        width: 100% !important;
        max-width: 700px !important; /* Ukuran pas untuk fokus visual */
        border-radius: 40px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    
    /* Tombol Game */
    div.stButton > button {
        width: 100%;
        height: 80px;
        font-size: 30px;
        border-radius: 20px;
        background-color: #1f2937;
        color: white;
        border: none;
    }
    div.stButton > button:hover { background-color: #374151; }
    
    /* Text Input */
    .stTextInput input {
        height: 50px;
        font-size: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. INISIALISASI STATE ---
if "status" not in st.session_state: st.session_state.status = "diam"
if "energy" not in st.session_state: st.session_state.energy = 60

# --- 4. LOGIKA AVATAR ---
def get_avatar(status):
    images = {
        "tidur": "Orochi_tidur.gif",
        "diam": "Orochi_diam.gif",
        "berfikir": "Orochi_berfikir.gif",
        "bicara": "Orochi_bicara.gif"
    }
    return images.get(status, "Orochi_diam.gif")

# --- 5. UI UTAMA ---
st.markdown("<h1 style='text-align: center; color: white;'>Orochi Pet</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 20px;'>⚡ Energi: {st.session_state.energy}% | 📍 Panongan, Tangerang</p>", unsafe_allow_html=True)

# Menampilkan Orochi (Pusat perhatian)
st.image(get_avatar(st.session_state.status))

# --- 6. INTERAKSI GAME ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("❤️"):
        st.session_state.status = "diam"
        st.toast("Orochi merasa senang!")
        st.rerun()
with col2:
    if st.button("💡"):
        st.session_state.status = "berfikir"
        st.rerun()
with col3:
    if st.button("💤"):
        st.session_state.status = "tidur"
        st.rerun()

# --- 7. CHAT LOGIC ---
prompt = st.text_input("", placeholder="Tulis perintah untuk Orochi...")
if prompt:
    st.session_state.status = "bicara"
    st.write(f"💬 **Orochi**: Memproses '{prompt}'...")
    time.sleep(3)
    st.session_state.status = "diam"
    st.rerun()

# Auto-reset animasi
if st.session_state.status in ["berfikir", "bicara"]:
    time.sleep(3)
    st.session_state.status = "diam"
    st.rerun()
