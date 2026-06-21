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
    "Lokasi": "Panongan, Tangerang"
}

# --- 3. CSS "PURE FULLSCREEN" (REVISI BERSIH) ---
st.markdown("""
    <style>
    /* Mengatur background gif untuk seluruh halaman */
    [data-testid="stAppViewContainer"] {
        background-image: url('https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/Orochi_diam.gif');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Menghilangkan semua warna background default Streamlit */
    .stApp, .block-container, [data-testid="stMainBlockContainer"] {
        background: transparent !important;
    }

    /* Membuat chat bubble lebih minimalis dan transparan */
    [data-testid="stChatMessageContent"] {
        background: rgba(0, 0, 0, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #ffffff !important;
    }

    /* Menghilangkan header, footer, dan margin atas */
    header, footer, [data-testid="stHeader"] {
        visibility: hidden;
        height: 0;
    }
    
    .block-container {
        padding-top: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. INISIALISASI & LOGIKA ---
if "messages" not in st.session_state:
    tz = pytz.timezone('Asia/Jakarta')
    h = datetime.now(tz).hour
    s = "Pagi" if 5<=h<11 else "Siang" if 11<=h<15 else "Sore" if 15<=h<19 else "Malam"
    st.session_state.messages = [{"role": "assistant", "content": f"Selamat {s}, Komandan Irfan. Ada yang bisa saya bantu?"}]

# --- 5. LOGIKA CHAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Mode Berfikir & Respon
    with st.chat_message("assistant"):
        tz = pytz.timezone('Asia/Jakarta')
        waktu = datetime.now(tz).strftime("%A, %d %B %Y %H:%M")
        
        sys_prompt = f"""Kamu Orochi, asisten setia Komandan Irfan. 
        Profil Komandan: {PROFIL_KOMANDAN}. 
        Waktu sekarang: {waktu}. 
        Aturan: Berikan jawaban yang cerdas, berwibawa, singkat, dan ingat bahwa lokasi Komandan adalah {PROFIL_KOMANDAN['Lokasi']}. 
        Jangan gunakan sapaan berulang, langsung jawab inti pertanyaan."""
        
        chat_history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}] + chat_history,
            model="llama-3.1-8b-instant",
            temperature=0.3
        )
        response = chat_completion.choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
