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
if "last_interaction" not in st.session_state: st.session_state.last_interaction = time.time()
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Orochi aktif, Komandan."}]

# --- 3. LOGIKA LOKASI & MOOD ---
loc = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition((pos) => {window.parent.postMessage({lat: pos.coords.latitude, lon: pos.coords.longitude}, "*")})', want_output=True, key='loc')
if loc: st.session_state.lokasi_tersimpan = f"Lat: {loc['coords']['latitude']}, Lon: {loc['coords']['longitude']}"

# Update Mood
if time.time() - st.session_state.last_interaction > 5 and st.session_state.status not in ["berfikir", "bicara"]:
    st.session_state.status = "tidur"

# --- 4. CSS DENGAN ID UNIK (AGAR GAMBAR MUNCUL) ---
# Menambahkan timestamp (?t=...) pada URL agar browser tidak pakai cache lama
gif_url = f"https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/templates/Orochi_{st.session_state.status}.gif?t={time.time()}"

st.markdown(f"""
    <style>
    /* Fokus menyembunyikan header saja, jangan menyembunyikan iframe lokasi */
    header, [data-testid="stHeader"] {{ visibility: hidden !important; display: none !important; }}
    
    /* Background Orochi */
    [data-testid="stAppViewContainer"] {{
        background-image: url('{gif_url}') !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    
    /* Bubble chat */
    [data-testid="stChatMessageContent"] {{ background: rgba(0, 0, 0, 0.6) !important; color: white !important; border-radius: 15px; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIKA CHAT & STATE MACHINE ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.status = "berfikir"
    st.session_state.last_interaction = time.time()
    st.rerun()

if st.session_state.status == "berfikir":
    time.sleep(1)
    st.session_state.status = "bicara"
    st.rerun()

if st.session_state.status == "bicara":
    sys_prompt = f"Nama: Orochi. Komandan: Irfan. Lokasi: {st.session_state.lokasi_tersimpan}. Jawab cerdas & berwibawa."
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages,
        model="llama-3.1-8b-instant"
    ).choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.status = "diam"
    st.session_state.last_interaction = time.time()
    st.rerun()
