import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz
from streamlit_js_eval import streamlit_js_eval

# --- KONFIGURASI ---
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- CSS FULL-SCREEN & PEMBERSIH GARIS ---
# Menghapus garis dengan CSS yang lebih spesifik
st.markdown("""
    <style>
    /* Paksa background full */
    [data-testid="stAppViewContainer"] {
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    
    /* Hapus elemen bawaan yang sering memunculkan garis */
    header, footer, #MainMenu, .stAppToolbar, [data-testid="stHeader"] {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* Hilangkan garis pemisah (hr) dan border input */
    hr { display: none !important; }
    .stChatInputContainer { border: none !important; }
    
    /* Pastikan tidak ada margin atas */
    .block-container { padding-top: 0rem !important; }
    </style>
""", unsafe_allow_html=True)

# --- FITUR LOKASI & MEMORI ---
loc = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition((pos) => {window.parent.postMessage({lat: pos.coords.latitude, lon: pos.coords.longitude}, "*")})', want_output=True, key='loc')

if "lokasi_tersimpan" not in st.session_state: st.session_state.lokasi_tersimpan = "Mendeteksi..."
if loc: st.session_state.lokasi_tersimpan = f"Lat: {loc['coords']['latitude']}, Lon: {loc['coords']['longitude']}"

# --- LOGIKA CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"Orochi aktif. Komandan Irfan terpantau di {st.session_state.lokasi_tersimpan}."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Orochi memproses..."):
        # Penjelasan sistem yang menyertakan lokasi
        sys_prompt = f"Nama: Orochi. Komandan: Irfan. Lokasi Terdeteksi: {st.session_state.lokasi_tersimpan}."
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages,
            model="llama-3.1-8b-instant"
        ).choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# --- NOTIFIKASI PROAKTIF ---
if time.time() % 3600 < 5: # Simulasi notifikasi per jam
    st.toast("Orochi: Saya tetap siaga memantau koordinat Komandan.")
