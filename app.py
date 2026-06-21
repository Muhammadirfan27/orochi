import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. CSS "CLEAN FULLSCREEN" ---
# Menggunakan background-image langsung pada .stApp dengan CSS yang lebih bersih
st.markdown("""
    <style>
    /* Paksa background agar selalu tampil dan tidak terhalang */
    .stApp {
        background: url('https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/Orochi_diam.jpg') no-repeat center center fixed !important;
        background-size: cover !important;
    }
    
    /* Buat semua kontainer transparan agar gambar terlihat */
    .stApp, .block-container, [data-testid="stMainBlockContainer"] {
        background: transparent !important;
    }

    /* Styling chat agar menyatu namun tetap terbaca */
    [data-testid="stChatMessageContent"] {
        background: rgba(0, 0, 0, 0.6) !important;
        color: #ffffff !important;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Sembunyikan elemen yang tidak perlu */
    header, footer, #MainMenu { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA PROFIL & KONTEKS ---
PROFIL = "Nama: Irfan. Pekerjaan: Admin Warehouse. Lokasi: Panongan, Tangerang. Keahlian: IoT & MQTT."

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Halo Irfan, Orochi siap melayani."}]

# --- 4. LOGIKA CHAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Menyertakan profil dan lokasi di SETIAP pesan agar AI tidak lupa
        sys_prompt = f"Kamu adalah Orochi, asisten setia. Profil Komandan: {PROFIL}. Jika ditanya lokasi, jawab dengan lokasi yang tepat di profil. Jawab dengan cerdas dan profesional."
        
        try:
            stream = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages,
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error("Gagal terhubung ke pusat data Orochi. Cek API Key Anda.")
