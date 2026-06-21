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
    "Hobi": "Esports (Inferno Demons), Anime Kekkaishi"
}

# --- 3. LOGIKA STATE ---
if "status" not in st.session_state: st.session_state.status = "diam"
if "last_activity" not in st.session_state: st.session_state.last_activity = time.time()
if "messages" not in st.session_state:
    tz = pytz.timezone('Asia/Jakarta')
    h = datetime.now(tz).hour
    s = "Pagi" if 5<=h<11 else "Siang" if 11<=h<15 else "Sore" if 15<=h<19 else "Malam"
    st.session_state.messages = [{"role": "assistant", "content": f"Selamat {s}, Komandan Irfan. Ada yang bisa saya bantu?"}]

# Auto-Tidur 10 Detik
if time.time() - st.session_state.last_activity > 10 and st.session_state.status == "diam":
    st.session_state.status = "tidur"

# --- 4. CSS DYNAMIC BACKGROUND ---
gif_url = f"https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/Orochi_{st.session_state.status}.gif"

st.markdown(f"""
    <style>
    /* Mengatur gambar sebagai background halaman yang responsif */
    [data-testid="stAppViewContainer"] {{
        background-image: url('{gif_url}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    .stApp {{ background: transparent !important; }}
    
    /* Bubble chat transparan agar menyatu dengan background */
    [data-testid="stChatMessageContent"] {{ 
        background: rgba(0, 0, 0, 0.7) !important; 
        color: white !important;
        border-radius: 15px;
    }}
    
    /* Menghilangkan elemen yang menghalangi background */
    header, footer {{ visibility: hidden; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIKA CHAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.last_activity = time.time()
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.status = "berfikir"
    st.rerun()

if st.session_state.status == "berfikir":
    time.sleep(1)
    st.session_state.status = "bicara"
    
    tz = pytz.timezone('Asia/Jakarta')
    waktu = datetime.now(tz).strftime("%A, %d %B %Y %H:%M")
    sys_prompt = f"Kamu Orochi, asisten setia Komandan Irfan. Profil: {PROFIL_KOMANDAN}. Waktu: {waktu}. Aturan: Jangan balas sapaan, langsung jawab cerdas & berwibawa."
    
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
    st.session_state.last_activity = time.time()
    st.rerun()
