import streamlit as st
import time
import requests
from groq import Groq
from datetime import datetime
import pytz

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="Orochi AI Pet", page_icon="🐍", layout="wide", initial_sidebar_state="collapsed")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. DATA PROFIL ---
PROFIL_KOMANDAN = {
    "Nama": "Irfan", "Pekerjaan": "Admin Warehouse",
    "Pendidikan": "Mahasiswa Tingkat Akhir",
    "Alamat": "Jl. Swadaya III, Ciakar, Kec. Panongan, Kabupaten Tangerang, Banten 15710",
    "Keahlian": "Software Developer (PHP, IoT, MQTT)",
    "Hobi": "Esports (Inferno Demons), Anime Kekkaishi"
}

# --- 3. FUNGSI ---
def get_location():
    try:
        res = requests.get("https://ipapi.co/json/", timeout=5).json()
        return f"{res.get('city', 'Tangerang')}, {res.get('region', 'Banten')}"
    except: return "Tangerang, Banten"

# --- 4. STATE ---
if "status" not in st.session_state: st.session_state.status = "diam"
if "last_time" not in st.session_state: st.session_state.last_time = time.time()
if "location" not in st.session_state: st.session_state.location = get_location()
if "messages" not in st.session_state: st.session_state.messages = []

# --- 5. LOGIKA AUTO-TIDUR ---
if time.time() - st.session_state.last_time > 10 and st.session_state.status == "diam":
    st.session_state.status = "tidur"

# --- 6. CSS (Garis & Status dihapus) ---
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{ padding: 0 !important; }}
    [data-testid="stHeader"] {{ display: none; }}
    .stApp {{
        background-image: url('https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/Orochi_{st.session_state.status}.gif');
        background-size: cover; background-position: center; height: 100vh;
    }}
    .chat-box {{ background: rgba(0,0,0,0.7); padding: 20px; border-radius: 20px; color: white; margin-top: 50vh; }}
    </style>
""", unsafe_allow_html=True)

# --- 7. LOGIKA CHAT & ANIMASI ---
st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
# Menampilkan lokasi saja, tanpa garis dan status
st.markdown(f"📍 {st.session_state.location}")

# Proses Input
if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.status = "diam"
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.status = "berfikir"
    st.rerun()

# Logika Transisi Animasi
if st.session_state.status == "berfikir":
    time.sleep(3)
    st.session_state.status = "bicara"
    
    memori = "\n".join([f"- {k}: {v}" for k, v in PROFIL_KOMANDAN.items()])
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": f"Kamu Orochi. Data: {memori}"}, {"role": "user", "content": st.session_state.messages[-1]["content"]}],
        model="llama-3.1-8b-instant"
    ).choices[0].message.content
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    duration = max(2, len(response) / 50)
    time.sleep(duration)
    
    st.session_state.status = "diam"
    st.session_state.last_time = time.time()
    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

st.markdown("</div>", unsafe_allow_html=True)
