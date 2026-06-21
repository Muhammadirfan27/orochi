import streamlit as st
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
        return f"{response.get('city', 'Tangerang')}, {response.get('region', 'Banten')}"
    except:
        return "Panongan, Tangerang"

def get_avatar_url(status):
    # Menggunakan f-string untuk mengambil file yang sesuai di GitHub
    return f"https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/Orochi_{status}.gif"

# --- 4. INISIALISASI STATE ---
if "status" not in st.session_state: st.session_state.status = "diam"
if "energy" not in st.session_state: st.session_state.energy = 60
if "last_activity" not in st.session_state: st.session_state.last_activity = time.time()
if "location" not in st.session_state: st.session_state.location = get_location()
if "messages" not in st.session_state: 
    st.session_state.messages = [{"role": "assistant", "content": "Hai Komandan Irfan! Orochi standby."}]

# --- 5. LOGIKA AUTO-TIDUR ---
if time.time() - st.session_state.last_activity > 10 and st.session_state.status == "diam":
    st.session_state.status = "tidur"

# --- 6. CSS (Tanpa Garis/Kotak, Tampilan Bersih) ---
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{ padding: 0 !important; }}
    [data-testid="stHeader"] {{ display: none; }}
    .stApp {{
        background-image: url('{get_avatar_url(st.session_state.status)}');
        background-size: cover; background-position: center; height: 100vh;
    }}
    .info-loc {{ color: white; font-weight: bold; padding: 10px; text-shadow: 1px 1px 2px black; }}
    </style>
""", unsafe_allow_html=True)

# --- 7. TAMPILAN & LOGIKA CHAT ---
st.markdown(f"<div class='info-loc'>📍 {st.session_state.location} | ⚡ Energi: {st.session_state.energy}%</div>", unsafe_allow_html=True)

# Input Chat
if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.status = "berfikir"
    st.session_state.last_activity = time.time()
    st.rerun()

# Logika Transisi Animasi & AI
if st.session_state.status == "berfikir":
    time.sleep(3) # Jeda Berfikir
    st.session_state.status = "bicara"
    
    # Memori & Prompt AI dengan Konteks Waktu
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.now(tz).strftime("%A, %d %B %Y %H:%M")
    memori = "\n".join([f"- {k}: {v}" for k, v in PROFIL_KOMANDAN.items()])
    system_prompt = f"Kamu Orochi, asisten setia Irfan. Waktu: {now}. Lokasi: {st.session_state.location}. Data: {memori}."
    
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": st.session_state.messages[-1]["content"]}],
        model="llama-3.1-8b-instant"
    ).choices[0].message.content
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Durasi bicara menyesuaikan panjang teks
    time.sleep(max(2, len(response) / 50))
    st.session_state.status = "diam"
    st.session_state.last_activity = time.time()
    st.rerun()

# Tampilkan Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
