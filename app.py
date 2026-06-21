import streamlit as st
import os
import time
import requests
from groq import Groq
from datetime import datetime
import pytz

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="Orochi AI Pet", page_icon="🐍", layout="wide", initial_sidebar_state="collapsed")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. DATA PROFIL KOMANDAN (MEMORI PERMANEN) ---
PROFIL_KOMANDAN = {
    "Nama": "Irfan",
    "Pekerjaan": "Admin Warehouse",
    "Pendidikan": "Mahasiswa Tingkat Akhir",
    "Alamat": "Jl. Swadaya III, Ciakar, Kec. Panongan, Kabupaten Tangerang, Banten 15710, Perum Golden Residence",
    "Keahlian": "Software Developer (PHP, IoT, MQTT)",
    "Hobi": "Esports (Inferno Demons), Anime Kekkaishi"
}

# --- 3. FUNGSI PENDUKUNG ---
def get_location():
    try:
        response = requests.get("https://ipapi.co/json/", timeout=5).json()
        return f"{response.get('city', 'Unknown')}, {response.get('region', 'Unknown')}"
    except:
        return "Panongan, Tangerang"

def get_avatar(status):
    images = {
        "tidur": "Orochi_tidur.gif",
        "diam": "Orochi_diam.gif",
        "berfikir": "Orochi_berfikir.gif",
        "bicara": "Orochi_bicara.gif"
    }
    return images.get(status, "Orochi_diam.gif")

# --- 4. INISIALISASI STATE ---
if "status" not in st.session_state: st.session_state.status = "diam"
if "energy" not in st.session_state: st.session_state.energy = 60
if "location" not in st.session_state: st.session_state.location = get_location()
if "messages" not in st.session_state: 
    st.session_state.messages = [{"role": "assistant", "content": "Hai Komandan Irfan! Orochi standby di posisi."}]

# --- 5. CSS FULLSCREEN OVERLAY ---
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{ padding: 0 !important; }}
    [data-testid="stHeader"] {{ display: none; }}
    .stApp {{
        background-image: url('https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/{get_avatar(st.session_state.status)}');
        background-size: cover;
        background-position: center;
        height: 100vh;
    }}
    .overlay-container {{
        position: absolute;
        bottom: 0;
        width: 100%;
        padding: 20px;
        background: linear-gradient(to top, rgba(0,0,0,0.9), transparent);
        color: white;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 6. TAMPILAN & LOGIKA CHAT ---
st.markdown("<div class='overlay-container'>", unsafe_allow_html=True)

# Info Bar
st.markdown(f"📍 {st.session_state.location} | ⚡ Energi: {st.session_state.energy}%")

# Tombol Kontrol
col1, col2, col3 = st.columns(3)
if col1.button("❤️"): st.session_state.status = "diam"; st.rerun()
if col2.button("💡"): st.session_state.status = "berfikir"; st.rerun()
if col3.button("💤"): st.session_state.status = "tidur"; st.rerun()

# Chat Area
if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.status = "bicara"
    
    # Memori & Prompt AI
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.now(tz).strftime("%A, %d %B %Y %H:%M")
    memori = "\n".join([f"- {k}: {v}" for k, v in PROFIL_KOMANDAN.items()])
    
    system_prompt = f"Kamu Orochi, asisten setia Komandan Irfan. Lokasi terkini: {st.session_state.location}. Waktu: {now}. Data: {memori}."
    
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant"
    ).choices[0].message.content
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Tampilkan Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

st.markdown("</div>", unsafe_allow_html=True)

# Reset Status Animasi
if st.session_state.status in ["berfikir", "bicara"]:
    time.sleep(3)
    st.session_state.status = "diam"
    st.rerun()
