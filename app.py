import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz

# Konfigurasi Halaman
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")

# Inisialisasi Groq (Pastikan sudah diset di Secrets)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Profil Komandan
PROFIL = {
    "Nama": "Irfan",
    "Pekerjaan": "Admin Warehouse",
    "Keahlian": "Software Developer (PHP, IoT, MQTT)",
    "Hobi": "Esports (Inferno Demons), Anime Kekkaishi"
}

# Inisialisasi State
if "status" not in st.session_state: st.session_state.status = "diam"
if "last_activity" not in st.session_state: st.session_state.last_activity = time.time()
if "messages" not in st.session_state:
    tz = pytz.timezone('Asia/Jakarta')
    h = datetime.now(tz).hour
    sapaan = "Pagi" if 5<=h<11 else "Siang" if 11<=h<15 else "Sore" if 15<=h<19 else "Malam"
    st.session_state.messages = [{"role": "assistant", "content": f"Selamat {sapaan}, Komandan Irfan. Apa yang bisa saya bantu?"}]

# CSS Responsive
st.markdown("""
    <style>
    .orochi-img { width: 100%; max-width: 350px; display: block; margin: auto; border-radius: 20px; }
    /* Menghilangkan elemen default Streamlit yang mengganggu */
    [data-testid="stChatMessageContent"] { background: transparent !important; }
    </style>
""", unsafe_allow_html=True)

# Logika Auto-Tidur
if time.time() - st.session_state.last_activity > 10 and st.session_state.status == "diam":
    st.session_state.status = "tidur"

# Render GIF
gif_url = f"https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/Orochi_{st.session_state.status}.gif"
st.markdown(f'<img src="{gif_url}" class="orochi-img">', unsafe_allow_html=True)

# Tampilkan Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Apa perintahmu, Komandan?"):
    st.session_state.last_activity = time.time()
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.status = "berfikir"
    st.rerun()

# State Machine
if st.session_state.status == "berfikir":
    time.sleep(1) # Durasi berfikir 1 detik
    st.session_state.status = "bicara"
    
    # Konteks Waktu & Profil
    tz = pytz.timezone('Asia/Jakarta')
    waktu = datetime.now(tz).strftime("%A, %d %B %Y %H:%M")
    sys_prompt = f"Kamu Orochi. Waktu: {waktu}. Komandan: {PROFIL}. Aturan: Jangan sapa balik. Langsung jawab fokus ke tugas/pertanyaan."
    
    # Request ke AI
    chat_completion = client.chat.completions.create(
        messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": st.session_state.messages[-1]["content"]}],
        model="llama-3.1-8b-instant"
    )
    response = chat_completion.choices[0].message.content
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Bicara sesuai panjang teks
    time.sleep(max(2, len(response) / 40))
    st.session_state.status = "diam"
    st.session_state.last_activity = time.time()
    st.rerun()
