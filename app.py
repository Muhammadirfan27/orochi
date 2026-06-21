import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz

# --- 1. KONFIGURASI ---
# Gunakan layout="wide" agar lebih fleksibel
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="wide")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. CSS CUSTOM UNTUK TAMPILAN FULLSCREEN ---
# Ini adalah kunci untuk membuat gambar Orochi jadi background sejati
st.markdown("""
    <style>
    /* Mengatur gambar sebagai background utama */
    .stApp {
        background: url('https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/Orochi_diam.jpg') no-repeat center center fixed;
        background-size: cover;
    }

    /* Menghilangkan semua background putih/gelap dari elemen Streamlit */
    .stApp, .block-container {
        background: transparent !important;
    }

    /* Membuat bubble chat menjadi transparan agar Orochi tetap terlihat di baliknya */
    [data-testid="stChatMessageContent"] {
        background: rgba(0, 0, 0, 0.4) !important;
        color: #ffffff !important;
        border-radius: 15px;
    }

    /* Menghilangkan header dan footer agar layar bersih */
    header, footer {
        visibility: hidden;
    }

    /* Memastikan input chat tetap terlihat jelas */
    [data-testid="stChatInput"] {
        background: rgba(0, 0, 0, 0.6) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA CHAT ---
# Inisialisasi pesan
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Halo Irfan, Orochi siap melayani."}]

# Tampilkan riwayat chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input Chat
if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Proses AI
    with st.chat_message("assistant"):
        # Tambahkan konteks lokasi dan profil agar tidak "ngawur"
        sys_prompt = "Kamu adalah Orochi, asisten setia Irfan, Admin Warehouse yang ahli di IoT & MQTT. Lokasi Irfan saat ini adalah Panongan, Tangerang. Jawab dengan singkat, cerdas, dan jangan pernah lupa lokasi atau profil Irfan."
        
        stream = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
