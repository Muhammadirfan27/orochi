import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz
from streamlit_js_eval import streamlit_js_eval
from elevenlabs.client import ElevenLabs
import base64
from auth import render_auth_page # Mengimpor fungsi login/daftar

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
eleven_client = ElevenLabs(api_key=st.secrets["ELEVENLABS_API_KEY"])

# --- INISIALISASI SESSION STATE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "status" not in st.session_state: st.session_state.status = "diam"
if "messages" not in st.session_state: st.session_state.messages = []

# --- 2. LOGIKA LOGIN (Memanggil file auth.py) ---
if not st.session_state.logged_in:
    render_auth_page()
    st.stop() # Hentikan eksekusi jika belum login

# --- KODE OROCHI (Berjalan HANYA setelah login berhasil) ---
if not st.session_state.messages:
    st.session_state.messages = [{"role": "assistant", "content": f"Halo {st.session_state.user_name}! Orochi di sini. Ada yang bisa kubantu?"}]

# --- 3. LOKASI ---
loc = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition((pos) => {window.parent.postMessage({lat: pos.coords.latitude, lon: pos.coords.longitude}, "*")})', want_output=True, key='loc')
if loc:
    st.session_state.lokasi_tersimpan = f"Lat: {loc['coords']['latitude']}, Lon: {loc['coords']['longitude']}"

# --- 4. CSS ---
gif_url = f"https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/templates/Orochi_{st.session_state.status}.gif"
st.markdown(f"""
    <style>
    header, footer, #MainMenu, .stAppToolbar, [data-testid="stHeader"], hr, .stMarkdown hr, div.stMarkdown > hr {{
        visibility: hidden !important; display: none !important;
    }}
    [data-testid="stAppViewContainer"] {{ background-image: url('{gif_url}') !important; background-size: cover !important; background-position: center !important; background-attachment: fixed !important; }}
    [data-testid="stChatMessageContent"] {{ background-color: transparent !important; color: white !important; border: none !important; }}
    .stChatMessage {{ background-color: transparent !important; }}
    .block-container {{ padding-top: 2rem !important; background: transparent !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIKA CHAT ---
def get_avatar(role):
    return "templates/Orochi.png" if role == "assistant" else None

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=get_avatar(msg["role"])):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ngobrol santai sama Orochi..."):
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
        last_user_msg = st.session_state.messages[-1]["content"].lower()
        
        # Penentuan Konten
        if any(w in last_user_msg for w in ["hallo", "halo", "hai", "bangun"]):
            konten_bicara = f"Halo juga {st.session_state.user_name}! Orochi sudah bangun."
        elif any(w in last_user_msg for w in ["bye", "selamat tinggal"]):
            konten_bicara = f"Oke {st.session_state.user_name}, Orochi istirahat dulu ya. Sampai jumpa!"
        else:
            system_prompt = f"Kamu adalah Orochi, AI ciptaan Irfan. Pengguna saat ini adalah {st.session_state.user_name}. Gunakan bahasa Indonesia ringkas."
            full_response = ""
            try:
                stream = client.chat.completions.create(
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": last_user_msg}],
                    model="llama-3.1-8b-instant", stream=True
                )
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                konten_bicara = full_response
            except: konten_bicara = "Maaf, ada kendala teknis."

        # Sinkronisasi TTS dan Teks
        def play_chunk(text):
            try:
                audio = eleven_client.text_to_speech.convert(text=text, voice_id="EXAVITQu4vr4xnSDxMaL", model_id="eleven_multilingual_v2", output_format="mp3_44100_128")
                b64 = base64.b64encode(b"".join(audio)).decode()
                st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)
            except: pass

        sentences = [s.strip() for s in konten_bicara.replace('!', '.').replace('?', '.').split('.') if s.strip()]
        displayed_text = ""
        for sentence in sentences:
            play_chunk(sentence)
            for char in sentence + ". ":
                displayed_text += char
                message_placeholder.markdown(displayed_text + "▌")
                time.sleep(0.05)
        
        message_placeholder.markdown(displayed_text)
        st.session_state.messages.append({"role": "assistant", "content": konten_bicara})
        time.sleep(1)
        st.session_state.status = "tidur" if "Sampai jumpa" in konten_bicara else "diam"
        st.rerun()
