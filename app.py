import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz
from streamlit_js_eval import streamlit_js_eval

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. STATE MANAGEMENT ---
if "status" not in st.session_state: st.session_state.status = "diam"
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Orochi aktif, Komandan."}]

# --- 3. LOKASI ---
loc = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition((pos) => {window.parent.postMessage({lat: pos.coords.latitude, lon: pos.coords.longitude}, "*")})', want_output=True, key='loc')
if loc:
    st.session_state.lokasi_tersimpan = f"Lat: {loc['coords']['latitude']}, Lon: {loc['coords']['longitude']}"
else:
    if "lokasi_tersimpan" not in st.session_state: st.session_state.lokasi_tersimpan = "Panongan, Tangerang"

# --- 4. CSS DENGAN PATH TEMPLATES & CACHE-BUSTER ---
# Menambahkan timestamp (?t=...) agar browser memaksa memuat GIF baru
gif_url = f"https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/templates/Orochi_{st.session_state.status}.gif?t={time.time()}"

st.markdown(f"""
    <style>
    /* Sembunyikan elemen bawaan tapi jaga iframe tetap ada */
    header, footer, #MainMenu, .stAppToolbar, [data-testid="stHeader"], hr {{
        visibility: hidden !important; display: none !important;
    }}
    
    iframe {{ 
        width: 1px !important; height: 1px !important; opacity: 0 !important; 
        position: absolute !important; pointer-events: none !important; 
    }}

    /* Background Orochi yang dipaksa muncul */
    [data-testid="stAppViewContainer"] {{
        background-image: url('{gif_url}') !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stChatMessageContent"] {{ background: rgba(0, 0, 0, 0.6) !important; color: white !important; border-radius: 15px; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIKA CHAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.status = "diam" # Default ke diam setelah chat
    st.rerun()

# PROACTIVE NOTIFICATION
if "last_toast" not in st.session_state: st.session_state.last_toast = time.time()
if time.time() - st.session_state.last_toast > 1800:
    st.toast("Orochi: Saya tetap siaga memantau koordinat Komandan.")
    st.session_state.last_toast = time.time()
