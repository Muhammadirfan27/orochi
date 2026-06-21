import streamlit as st
import time
import requests
from groq import Groq
from datetime import datetime
import pytz

# --- KONFIGURASI ---
st.set_page_config(page_title="Orochi AI Pet", page_icon="🐍", layout="wide", initial_sidebar_state="collapsed")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- DATA ---
PROFIL_KOMANDAN = {
    "Nama": "Irfan", "Pekerjaan": "Admin Warehouse",
    "Pendidikan": "Mahasiswa Tingkat Akhir",
    "Alamat": "Jl. Swadaya III, Ciakar, Kec. Panongan, Kabupaten Tangerang, Banten 15710",
    "Keahlian": "Software Developer (PHP, IoT, MQTT)",
    "Hobi": "Esports (Inferno Demons), Anime Kekkaishi"
}

# --- FUNGSI ---
def get_location():
    try:
        res = requests.get("https://ipapi.co/json/", timeout=5).json()
        return f"{res.get('city', 'Tangerang')}, {res.get('region', 'Banten')}"
    except: return "Tangerang, Banten"

# --- STATE ---
if "status" not in st.session_state: st.session_state.status = "diam"
if "last_time" not in st.session_state: st.session_state.last_time = time.time()
if "location" not in st.session_state: st.session_state.location = get_location()
if "messages" not in st.session_state: st.session_state.messages = []

# --- CSS BERSIH (Tanpa Garis/Kotak) ---
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{ padding: 0 !important; }}
    [data-testid="stHeader"] {{ display: none; }}
    .stApp {{
        background-image: url('https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/Orochi_{st.session_state.status}.gif');
        background-size: cover; background-position: center; height: 100vh;
    }}
    /* Teks lokasi saja tanpa kotak */
    .loc-text {{ color: white; font-weight: bold; padding: 10px; text-shadow: 1px 1px 2px black; }}
    </style>
""", unsafe_allow_html=True)

# --- LOGIKA CHAT ---
st.markdown(f"<div class='loc-text'>📍 {st.session_state.location}</div>", unsafe_allow_html=True)

if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.status = "berfikir"
    st.rerun()

if st.session_state.status == "berfikir":
    time.sleep(3)
    st.session_state.status = "bicara"
    
    # KONTEKS WAKTU & LOKASI DITAMBAHKAN DI SINI AGAR AI PINTAR
    tz = pytz.timezone('Asia/Jakarta')
    waktu_sekarang = datetime.now(tz).strftime("%A, %d %B %Y %H:%M")
    memori = "\n".join([f"- {k}: {v}" for k, v in PROFIL_KOMANDAN.items()])
    
    sys_prompt = f"Kamu Orochi. Waktu saat ini: {waktu_sekarang}. Lokasi: {st.session_state.location}. Data: {memori}."
    
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": st.session_state.messages[-1]["content"]}],
        model="llama-3.1-8b-instant"
    ).choices[0].message.content
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    time.sleep(max(2, len(response) / 50))
    st.session_state.status = "diam"
    st.session_state.last_time = time.time()
    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
