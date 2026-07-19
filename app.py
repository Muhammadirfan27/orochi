import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz
from streamlit_js_eval import streamlit_js_eval
from gtts import gTTS
import base64

# --- FUNGSI TTS ---
def play_audio(text):
    try:
        # Menggunakan gTTS untuk generate suara
        tts = gTTS(text=text, lang='id')
        tts.save("response.mp3")
        with open("response.mp3", "rb") as audio_file:
            audio_bytes = audio_file.read()
        b64 = base64.b64encode(audio_bytes).decode()
        # Menggunakan autostart agar langsung berbunyi setelah teks tampil
        audio_html = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    except Exception:
        pass

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. INITIAL STATE ---
if "status" not in st.session_state: st.session_state.status = "diam"
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Halo Irfan! Orochi di sini. Ada yang bisa kubantu?"}]

# --- 3. LOKASI ---
loc = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition((pos) => {window.parent.postMessage({lat: pos.coords.latitude, lon: pos.coords.longitude}, "*")})', want_output=True, key='loc')
if loc:
    st.session_state.lokasi_tersimpan = f"Lat: {loc['coords']['latitude']}, Lon: {loc['coords']['longitude']}"

# --- 4. CSS ---
gif_url = f"https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/templates/Orochi_{st.session_state.status}.gif"
st.markdown(f"""
    <style>
    header, footer, .stAppToolbar {{ visibility: hidden !important; }}
    [data-testid="stAppViewContainer"] {{ background-image: url('{gif_url}') !important; background-size: cover; }}
    [data-testid="stChatMessageContent"] {{ background-color: transparent !important; color: white !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIKA CHAT ---
def get_avatar(role):
    return "templates/Orochi.png" if role == "assistant" else None

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=get_avatar(msg["role"])):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ngobrol santai sama Orochi..."):
    if st.session_state.status == "tidur" and not any(w in prompt.lower() for w in ["hallo", "halo", "bangun"]):
        st.warning("Orochi masih tidur, Irfan.")
        st.stop()
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.status = "bicara" if any(w in prompt.lower() for w in ["bye", "selamat tinggal"]) else "berfikir"
    st.rerun()

if st.session_state.status == "berfikir":
    time.sleep(1) 
    st.session_state.status = "bicara"
    st.rerun()

if st.session_state.status == "bicara":
    with st.chat_message("assistant", avatar=get_avatar("assistant")):
        message_placeholder = st.empty()
        last_msg = st.session_state.messages[-1]["content"].lower()
        
        # Penentuan Konten
        if any(w in last_msg for w in ["hallo", "halo", "bangun"]):
            konten_bicara = "Halo juga Irfan! Orochi sudah bangun. Ada yang bisa dibantu?"
        elif any(w in last_msg for w in ["bye", "selamat tinggal"]):
            konten_bicara = "Oke Irfan, Orochi istirahat dulu ya. Sampai jumpa!"
        else:
            # Generate Jawaban
            stream = client.chat.completions.create(
                messages=[{"role": "user", "content": last_msg}],
                model="llama-3.1-8b-instant", stream=True
            )
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            konten_bicara = full_response

        # Tampilkan teks utuh tanpa kursor
        message_placeholder.markdown(konten_bicara)
        
        # Baru setelah teks tampil penuh, panggil suara
        play_audio(konten_bicara)
        
        st.session_state.messages.append({"role": "assistant", "content": konten_bicara})
        time.sleep(1)
        st.session_state.status = "tidur" if "Sampai jumpa" in konten_bicara else "diam"
        st.rerun()
