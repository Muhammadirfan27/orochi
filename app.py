import streamlit as st
import time
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
    return f"Orochi_{status}.gif" # Pastikan file tersedia di folder/github

def get_greeting():
    hour = datetime.now(pytz.timezone('Asia/Jakarta')).hour
    if 5 <= hour < 12: return "Selamat Pagi, Komandan Irfan!"
    if 12 <= hour < 15: return "Selamat Siang, Komandan Irfan!"
    if 15 <= hour < 18: return "Selamat Sore, Komandan Irfan!"
    return "Selamat Malam, Komandan Irfan!"

# --- 4. INISIALISASI STATE ---
if "energy" not in st.session_state: st.session_state.energy = 50
if "orochi_awake" not in st.session_state: st.session_state.orochi_awake = False
if "status" not in st.session_state: st.session_state.status = "tidur"
if "messages" not in st.session_state: 
    st.session_state.messages = [{"role": "assistant", "content": get_greeting()}]

# --- 5. TAMPILAN BERSIH ---
st.markdown("<style>div[data-testid='stImage'] {display: flex; justify-content: center;}</style>", unsafe_allow_html=True)
st.image(get_avatar(st.session_state.status), width=350)

# --- 6. LOGIKA INTERAKSI ---
if not st.session_state.orochi_awake:
    if st.button("Bangunkan Orochi"):
        st.session_state.orochi_awake = True
        st.session_state.status = "diam"
        st.rerun()
else:
    # Status Bar
    col_stat1, col_stat2 = st.columns(2)
    col_stat1.metric("Energi", f"{st.session_state.energy}%")
    col_stat2.write(f"Lokasi: {PROFIL_KOMANDAN['Lokasi']}")

    c1, c2, c3 = st.columns(3)
    if c1.button("Sentuh Orochi"):
        st.session_state.status = "diam"
        st.session_state.energy = min(100, st.session_state.energy + 10)
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
            
            # Berfikir 1 Detik
            time.sleep(1)
            
            # Panggil AI
            tz = pytz.timezone('Asia/Jakarta')
            waktu = datetime.now(tz).strftime("%H:%M")
            sys_prompt = f"Kamu Orochi. Waktu sekarang: {waktu}. User: {PROFIL_KOMANDAN['Nama']}."
            
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant"
            ).choices[0].message.content
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            time.sleep(max(2, len(response) / 50))
            st.session_state.status = "diam"
            st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
