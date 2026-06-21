import streamlit as st
import time
import requests
from groq import Groq
from datetime import datetime
import pytz

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="Orochi Virtual Pet", page_icon="🐍", layout="wide")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. DATA PROFIL ---
PROFIL_KOMANDAN = {
    "Nama": "Irfan",
    "Pekerjaan": "Admin Warehouse",
    "Lokasi": "Panongan, Tangerang",
    "Keahlian": "Software Developer (PHP, IoT, MQTT)"
}

# --- 3. FUNGSI ---
def get_avatar(status):
    images = {
        "tidur": "Orochi_tidur.gif",
        "diam": "Orochi_diam.gif",
        "berfikir": "Orochi_berfikir.gif",
        "bicara": "Orochi_bicara.gif"
    }
    return images.get(status, "Orochi_diam.gif")

# --- 4. INISIALISASI STATE ---
if "energy" not in st.session_state: st.session_state.energy = 50
if "orochi_awake" not in st.session_state: st.session_state.orochi_awake = False
if "status" not in st.session_state: st.session_state.status = "tidur"
if "last_activity" not in st.session_state: st.session_state.last_activity = time.time()
if "messages" not in st.session_state: st.session_state.messages = []

# --- 5. LOGIKA AUTO-TIDUR (10 Detik) ---
if st.session_state.orochi_awake and time.time() - st.session_state.last_activity > 10 and st.session_state.status == "diam":
    st.session_state.status = "tidur"

# --- 6. TAMPILAN BERSIH ---
st.markdown("<style>div[data-testid='stImage'] {display: flex; justify-content: center;}</style>", unsafe_allow_html=True)
st.image(get_avatar(st.session_state.status), width=350)

# --- 7. LOGIKA INTERAKSI ---
if not st.session_state.orochi_awake:
    if st.button("Bangunkan Orochi"):
        st.session_state.orochi_awake = True
        st.session_state.status = "diam"
        st.session_state.last_activity = time.time()
        st.rerun()
else:
    col_stat1, col_stat2 = st.columns(2)
    col_stat1.metric("Energi", f"{st.session_state.energy}%")
    col_stat2.write(f"Lokasi: {PROFIL_KOMANDAN['Lokasi']}")

    c1, c2, c3 = st.columns(3)
    if c1.button("Sentuh Orochi"):
        st.session_state.status = "diam"
        st.session_state.energy = min(100, st.session_state.energy + 10)
        st.session_state.last_activity = time.time()
        st.rerun()
    if c2.button("Beri Perintah"):
        st.session_state.status = "berfikir"
        st.rerun()
    if c3.button("Tidurkan"):
        st.session_state.status = "tidur"
        st.session_state.orochi_awake = False
        st.rerun()

    # Chat & Logika Bicara
    if st.session_state.status in ["berfikir", "bicara"]:
        prompt = st.chat_input("Apa perintahmu, Komandan?")
        
        if st.session_state.status == "berfikir" and prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.status = "bicara"
            
            # Panggil AI dengan Konteks Waktu
            tz = pytz.timezone('Asia/Jakarta')
            waktu = datetime.now(tz).strftime("%A, %d %B %Y %H:%M")
            memori = f"Nama: {PROFIL_KOMANDAN['Nama']}. Keahlian: {PROFIL_KOMANDAN['Keahlian']}."
            
            # Berfikir 1 Detik
            time.sleep(1)
            
            sys_prompt = f"Kamu Orochi. Waktu sekarang: {waktu}. Info user: {memori}"
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant"
            ).choices[0].message.content
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Durasi Bicara sesuai panjang teks
            time.sleep(max(2, len(response) / 50))
            st.session_state.status = "diam"
            st.session_state.last_activity = time.time()
            st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
