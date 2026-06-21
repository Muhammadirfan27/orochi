import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. CSS FULLSCREEN PRESISI ---
st.markdown("""
    <style>
    /* Paksa background agar menutupi seluruh layar */
    .stApp {
        background: url('https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/Orochi_diam.jpg') no-repeat center center fixed !important;
        background-size: cover !important;
    }
    
    /* Hilangkan semua pembatas hitam */
    .main, .block-container {
        background: transparent !important;
        padding-top: 1rem !important; /* Jarak atas disesuaikan agar pas */
    }

    /* Chat bubble transparan agar gambar Orochi terlihat di belakangnya */
    [data-testid="stChatMessageContent"] {
        background: rgba(0, 0, 0, 0.4) !important;
        color: white !important;
        border-radius: 10px;
        border: none !important;
    }

    /* Hilangkan header agar tampilan clean */
    header { visibility: hidden !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA & KONTEKS ---
PROFIL = "Nama: Irfan. Pekerjaan: Admin Warehouse. Lokasi: Panongan, Tangerang. Keahlian: IoT & MQTT."

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Halo Irfan, Orochi siap melayani."}]

# --- 4. ENGINE CHAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Sistem prompt yang memaksa AI selalu tahu lokasi Anda
        sys_prompt = f"Kamu adalah Orochi, asisten setia Irfan. Profil Irfan: {PROFIL}. Lokasi Irfan saat ini: Panongan, Tangerang. Jawab dengan cerdas, berwibawa, dan jangan pernah lupa lokasi ini."
        
        stream = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
