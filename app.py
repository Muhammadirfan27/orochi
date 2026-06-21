import streamlit as st
import time

st.set_page_config(page_title="Orochi Pet", page_icon="🐍", layout="centered")

# CSS untuk membuat tampilan game-like
st.markdown("""
    <style>
    /* Fokuskan tampilan Orochi */
    .stApp { background-color: #0e1117; }
    
    /* Center the main container */
    .block-container { max-width: 500px; padding-top: 2rem; }
    
    /* Animasi Orochi */
    .stImage img { 
        border: 4px solid #333; 
        border-radius: 50px; 
        background-color: #1a1a1a;
    }
    
    /* Gaya Tombol ala Game */
    div.stButton > button {
        width: 100%;
        border-radius: 20px;
        background-color: #2e3b4e;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# State Management
if "status" not in st.session_state: st.session_state.status = "diam"
if "energy" not in st.session_state: st.session_state.energy = 60

# Header minimalis
st.markdown("<h2 style='text-align: center; color: white;'>Orochi Pet</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>Energi: {st.session_state.energy}% | Lokasi: Panongan</p>", unsafe_allow_html=True)

# Menampilkan Orochi di tengah (Fokus Utama)
def get_avatar(status):
    images = {"tidur": "Orochi_tidur.gif", "diam": "Orochi_diam.gif", "berfikir": "Orochi_berfikir.gif", "bicara": "Orochi_bicara.gif"}
    return images.get(status, "Orochi_diam.gif")

st.image(get_avatar(st.session_state.status), use_container_width=True)

# Area Interaksi (Dibuat lebih ringkas)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("❤️"):
        st.session_state.status = "diam"
        st.toast("Orochi senang!")
with col2:
    if st.button("💡"):
        st.session_state.status = "berfikir"
        st.rerun()
with col3:
    if st.button("💤"):
        st.session_state.status = "tidur"
        st.rerun()

# Input Perintah
prompt = st.text_input("", placeholder="Tulis perintah untuk Orochi...")
if prompt:
    st.session_state.status = "bicara"
    st.write(f"💬 Orochi: Memproses '{prompt}'...")
    time.sleep(2)
    st.session_state.status = "diam"
    st.rerun()

# Auto Reset
if st.session_state.status in ["berfikir", "bicara"]:
    time.sleep(3)
    st.session_state.status = "diam"
    st.rerun()
