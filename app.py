import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz
from streamlit_js_eval import streamlit_js_eval

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. FITUR 1: BRIDGE LOKASI (REAL-TIME) ---
# Meminta lokasi dan otomatis mengirimkannya ke variabel loc
loc = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition((pos) => {window.parent.postMessage({lat: pos.coords.latitude, lon: pos.coords.longitude}, "*")})', want_output=True, key='loc')

# --- 3. FITUR 2: MEMORI PERSISTEN ---
if "lokasi_tersimpan" not in st.session_state:
    st.session_state.lokasi_tersimpan = "Lokasi tersembunyi"
if loc:
    st.session_state.lokasi_tersimpan = f"Lat: {loc['coords']['latitude']}, Lon: {loc['coords']['longitude']}"

# --- 4. FITUR 3: DYNAMIC PERSONALITY ENGINE ---
def get_orochi_mood():
    h = datetime.now(pytz.timezone('Asia/Jakarta')).hour
    if 0 <= h < 5: return "tidur"
    if 5 <= h < 11: return "pagi"
    return "aktif"

mood = get_orochi_mood()

# --- 5. LOGIKA CHAT DENGAN SENSORY FEEDBACK ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"Orochi aktif. Komandan Irfan terpantau di {st.session_state.lokasi_tersimpan}."}]

# Tampilan Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input Chat
if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # FITUR 4: SENSORY FEEDBACK (Spinner saat berfikir)
    with st.spinner("Orochi sedang menganalisis situasi..."):
        sys_prompt = f"""Kamu Orochi, asisten setia Komandan Irfan. 
        Mood saat ini: {mood}. 
        Lokasi Komandan: {st.session_state.lokasi_tersimpan}. 
        Aturan: Jawab cerdas, berwibawa, dan sesuaikan gaya bicara dengan mood."""
        
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages,
            model="llama-3.1-8b-instant"
        ).choices[0].message.content
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# FITUR 5: NOTIFIKASI PROAKTIF
if "last_toast" not in st.session_state: st.session_state.last_toast = time.time()
if time.time() - st.session_state.last_toast > 1800: # Toast tiap 30 menit
    st.toast("Orochi: Saya tetap siaga memantau koordinat Komandan.")
    st.session_state.last_toast = time.time()
