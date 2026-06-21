import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. DATA PROFIL ---
PROFIL_KOMANDAN = {
    "Nama": "Irfan",
    "Pekerjaan": "Admin Warehouse",
    "Keahlian": "Software Developer (PHP, IoT, MQTT)",
    "Hobi": "Esports (Inferno Demons), Anime Kekkaishi",
    "Lokasi": "Tangerang, Banten, Indonesia"
}

# --- 3. LOGIKA STATE & SAPAAN ---
def get_sapaan():
    tz = pytz.timezone('Asia/Jakarta')
    h = datetime.now(tz).hour
    s = "Pagi" if 5<=h<11 else "Siang" if 11<=h<15 else "Sore" if 15<=h<19 else "Malam"
    return f"Selamat {s}, Komandan Irfan."

if "status" not in st.session_state: st.session_state.status = "diam"
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"{get_sapaan()} Ada yang bisa saya bantu?"}]

# --- 4. CSS DYNAMIC BACKGROUND ---
gif_url = f"https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/Orochi_{st.session_state.status}.gif"

st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url('{gif_url}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .stApp {{ background: transparent !important; }}
    [data-testid="stChatMessageContent"] {{ 
        background: rgba(0, 0, 0, 0.7) !important; 
        color: white !important;
        border-radius: 15px;
    }}
    header, footer {{ visibility: hidden; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIKA CHAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.status = "berfikir"
    st.rerun()

if st.session_state.status == "berfikir":
    st.session_state.status = "bicara"
    st.rerun()

if st.session_state.status == "bicara":
    tz = pytz.timezone('Asia/Jakarta')
    waktu = datetime.now(tz).strftime("%A, %d %B %Y %H:%M")
    
    sys_prompt = f"""Kamu Orochi, asisten setia Komandan Irfan. 
    Profil Komandan: {PROFIL_KOMANDAN}. 
    Waktu sekarang: {waktu}. 
    Aturan: Kamu harus tetap sopan namun berwibawa. Ingat bahwa lokasi Komandan adalah {PROFIL_KOMANDAN['Lokasi']}. 
    Berikan jawaban yang cerdas dan langsung pada intinya."""
    
    chat_history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "system", "content": sys_prompt}] + chat_history,
        model="llama-3.1-8b-instant",
        temperature=0.3
    )
    response = chat_completion.choices[0].message.content
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    time.sleep(max(2, len(response) / 40))
    st.session_state.status = "diam"
    st.rerun()
