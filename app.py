import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. CSS FULLSCREEN (DIPERBAIKI) ---
st.markdown("""
    <style>
    /* Mengatur kontainer agar bisa menampung gambar sebagai background */
    .stApp {
        background-color: #0e1117; /* Fallback warna gelap */
    }
    
    /* Memastikan gambar background menutupi seluruh layar */
    .bg-orochi {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        object-fit: cover;
        z-index: -1;
    }

    /* Membuat chat bubble transparan agar terlihat menyatu */
    [data-testid="stChatMessageContent"] {
        background: rgba(0, 0, 0, 0.6) !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. RENDER BACKGROUND ---
# Menggunakan HTML tag img langsung agar lebih stabil daripada background-image CSS
st.markdown(
    '<img src="https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/Orochi_diam.jpg" class="bg-orochi">', 
    unsafe_allow_html=True
)

# --- 4. DATA PROFIL & LOGIKA ---
PROFIL_KOMANDAN = {
    "Nama": "Irfan",
    "Pekerjaan": "Admin Warehouse",
    "Keahlian": "Software Developer (PHP, IoT, MQTT)",
    "Hobi": "Esports (Inferno Demons), Anime Kekkaishi",
    "Lokasi": "Panongan, Tangerang"
}

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Halo Irfan, Orochi siap melayani."}]

# --- 5. LOGIKA CHAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Menyertakan lokasi secara eksplisit dalam sistem prompt agar selalu diingat
        sys_prompt = (f"Kamu Orochi, asisten setia Irfan. "
                      f"Profil: {PROFIL_KOMANDAN}. "
                      f"PENTING: Lokasi Irfan saat ini adalah {PROFIL_KOMANDAN['Lokasi']}. "
                      "Jawablah dengan cerdas, singkat, dan berwibawa.")
        
        stream = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
