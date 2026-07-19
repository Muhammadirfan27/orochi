import streamlit as st
import time
import requests
from groq import Groq
from datetime import datetime
import pytz
from streamlit_js_eval import streamlit_js_eval
from elevenlabs.client import ElevenLabs
import base64

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
eleven_client = ElevenLabs(api_key=st.secrets["ELEVENLABS_API_KEY"])

# --- FUNGSI GOOGLE SHEETS ---
def simpan_ke_sheet(nama, email):
    # GANTI URL_WEB_APP_ANDA_DISINI dengan URL dari Deployment Apps Script Anda
    url = "https://script.google.com/macros/s/AKfycbxpYgB0dgiGjOhRiktL0mYo7RQaQZ9jxSH4XoRDy1wn1PLkh3lShqRBAaIpjsIm0T3-/exec" 
    data = {"name": nama, "email": email}
    try:
        requests.post(url, json=data)
    except:
        pass

# --- FUNGSI TTS ELEVENLABS ---
def play_chunk(text):
    try:
        audio_stream = eleven_client.text_to_speech.convert(
            text=text, voice_id="EXAVITQu4vr4xnSDxMaL", 
            model_id="eleven_multilingual_v2", output_format="mp3_44100_128"
        )
        audio_data = b"".join(audio_stream)
        b64 = base64.b64encode(audio_data).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)
    except Exception: pass

# --- 2. INITIAL STATE & LOGIN ---
if "status" not in st.session_state: st.session_state.status = "diam"
if "messages" not in st.session_state: st.session_state.messages = []
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_name" not in st.session_state: st.session_state.user_name = ""

# FORM LOGIN
if not st.session_state.logged_in:
    st.title("Orochi AI Login")
    name_input = st.text_input("Nama Anda:")
    email_input = st.text_input("Email Anda:")
    if st.button("Masuk"):
        if name_input and email_input:
            st.session_state.user_name = name_input
            st.session_state.logged_in = True
            simpan_ke_sheet(name_input, email_input)
            st.rerun()
    st.stop()

# --- 3. LOKASI ---
loc = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition((pos) => {window.parent.postMessage({lat: pos.coords.latitude, lon: pos.coords.longitude}, "*")})', want_output=True, key='loc')
if loc: st.session_state.lokasi_tersimpan = f"Lat: {loc['coords']['latitude']}, Lon: {loc['coords']['longitude']}"

# --- 4. CSS ---
gif_url = f"https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/templates/Orochi_{st.session_state.status}.gif"
st.markdown(f"""
    <style>
    header, footer, #MainMenu, .stAppToolbar, [data-testid="stHeader"], hr, .stMarkdown hr, div.stMarkdown > hr {{
        visibility: hidden !important; display: none !important;
    }}
    [data-testid="stAppViewContainer"] {{ background-image: url('{gif_url}') !important; background-size: cover; background-position: center; }}
    [data-testid="stChatMessageContent"] {{ background-color: transparent !important; color: white !important; border: none !important; }}
    .stChatMessage {{ background-color: transparent !important; }}
    .block-container {{ padding-top: 2rem !important; background: transparent !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIKA CHAT & PERSONA ---
def get_avatar(role): return "templates/Orochi.png" if role == "assistant" else None

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=get_avatar(msg["role"])): st.markdown(msg["content"])

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
        
        if any(w in last_user_msg for w in ["hallo", "halo", "bangun"]):
            konten_bicara = f"Halo {st.session_state.user_name}! Saya Orochi, asisten pribadi ciptaan Irfan. Ada yang bisa dibantu?"
        elif any(w in last_user_msg for w in ["bye", "selamat tinggal"]):
            konten_bicara = f"Baik {st.session_state.user_name}, saya istirahat dulu ya. Sampai jumpa!"
        else:
            waktu_jkt = datetime.now(pytz.timezone('Asia/Jakarta'))
            tgl_sekarang = waktu_jkt.strftime("%A, %d %B %Y")
            system_prompt = (
                f"Hari ini adalah {tgl_sekarang}. IDENTITAS KAMU: Nama kamu Orochi, AI ciptaan Irfan. "
                f"Pengguna saat ini adalah {st.session_state.user_name}. "
                "WAJIB menggunakan bahasa Indonesia yang baik dan benar. Jangan gunakan bahasa Inggris. "
                "Jika ditanya tentang Pancasila, WAJIB menjawab dengan teks resmi: "
                "1. Ketuhanan Yang Maha Esa. 2. Kemanusiaan yang adil dan beradab. 3. Persatuan Indonesia. "
                "4. Kerakyatan yang dipimpin oleh hikmat kebijaksanaan dalam permusyawaratan/perwakilan. "
                "5. Keadilan sosial bagi seluruh rakyat Indonesia."
            )
            
            full_response = ""
            try:
                stream = client.chat.completions.create(
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": last_user_msg}],
                    model="llama-3.1-8b-instant", stream=True
                )
                for chunk in stream:
                    if chunk.choices[0].delta.content: full_response += chunk.choices[0].delta.content
                konten_bicara = full_response
            except: konten_bicara = "Maaf, ada kendala teknis."

        sentences = [s.strip() for s in konten_bicara.replace('!', '.').replace('?', '.').split('.') if s.strip()]
        displayed_text = ""
        for sentence in sentences:
            play_chunk(sentence)
            for char in sentence + ". ":
                displayed_text += char
                message_placeholder.markdown(displayed_text + "▌")
                time.sleep(0.08)
        
        message_placeholder.markdown(displayed_text)
        st.session_state.messages.append({"role": "assistant", "content": konten_bicara})
        time.sleep(1)
        st.session_state.status = "tidur" if "Sampai jumpa" in konten_bicara else "diam"
        st.rerun()
