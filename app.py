import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz
from streamlit_js_eval import streamlit_js_eval

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. FITUR 1: BRIDGE LOKASI REAL-TIME ---
# Meminta lokasi tanpa tombol, langsung saat app dimuat
loc = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition((pos) => {window.parent.postMessage({lat: pos.coords.latitude, lon: pos.coords.longitude}, "*")})', want_output=True, key='loc')

# --- 3. FITUR 2: MEMORI PERSISTEN ---
if "lokasi_tersimpan" not in st.session_state: st.session_state.lokasi_tersimpan = "Panongan, Tangerang"
if loc: st.session_state.lokasi_tersimpan = f"Lat: {loc['coords']['latitude']}, Lon: {loc['coords']['longitude']}"

# --- 4. FITUR 3: DYNAMIC PERSONALITY ENGINE ---
def get_orochi_mood():
    h = datetime.now(pytz.timezone('Asia/Jakarta')).hour
    if h < 5: return "tidur"
    if h < 11: return "diam" # Mode Pagi
    return "diam"

st.session_state.status = get_orochi_mood()

# --- 5. LOGIKA CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"Komandan Irfan, Orochi aktif di {st.session_state.lokasi_tersimpan}."}]

# --- [CSS DAN LOGIKA CHAT TETAP SEPERTI SEBELUMNYA] ---
# (Pastikan Anda menggunakan CSS yang sudah kita perbaiki tadi)

if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # FITUR 4: SENSORY FEEDBACK (Simulasi)
    with st.spinner("Orochi sedang memproses..."):
        sys_prompt = f"Nama: Orochi. Komandan: Irfan. Lokasi: {st.session_state.lokasi_tersimpan}. Berikan jawaban yang disesuaikan dengan profil dan lokasi."
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages,
            model="llama-3.1-8b-instant"
        ).choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# FITUR 5: PROACTIVE NOTIFICATION
if "last_check" not in st.session_state: st.session_state.last_check = time.time()
if time.time() - st.session_state.last_check > 3600: # Cek tiap 1 jam
    st.toast("Orochi: Komandan, saya tetap siaga mengawasi koordinat Anda.")
    st.session_state.last_check = time.time()
