import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz
from streamlit_js_eval import streamlit_js_eval
from elevenlabs.client import ElevenLabs
import base64

# --- INISIALISASI ---
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
eleven_client = ElevenLabs(api_key=st.secrets["ELEVENLABS_API_KEY"])

# --- FUNGSI TTS ELEVENLABS (DENGAN JEDA) ---
def play_audio_stream(text):
    # Memecah teks berdasarkan titik agar Orochi berbicara per kalimat
    sentences = [s.strip() for s in text.replace('!', '.').replace('?', '.').split('.') if len(s.strip()) > 2]
    for sentence in sentences:
        try:
            audio_stream = eleven_client.text_to_speech.convert(
                text=sentence, 
                voice_id="EXAVITQu4vr4xnSDxMaL", 
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128"
            )
            audio_data = b"".join(audio_stream)
            b64 = base64.b64encode(audio_data).decode()
            
            # Putar audio per kalimat
            st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)
            time.sleep(2) # Jeda agar tidak tumpang tindih dan terdengar natural
        except Exception:
            continue

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
    header, footer, #MainMenu, .stAppToolbar, [data-testid="stHeader"], hr {{ visibility: hidden !important; display: none !important; }}
    [data-testid="stAppViewContainer"] {{ background-image: url('{gif_url}') !important; background-size: cover; background-position: center; }}
    [data-testid="stChatMessageContent"] {{ background-color: transparent !important; color: white !important; border: none !important; }}
    .stChatMessage {{ background-color: transparent !important; }}
    .block-container {{ padding-top: 2rem !important; background: transparent !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIKA CHAT & PERSONA ---
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
        
        if any(w in last_msg for w in ["hallo", "halo", "bangun"]):
            konten_bicara = "Halo juga Irfan! Orochi sudah bangun. Ada yang bisa dibantu?"
        elif any(w in last_msg for w in ["bye", "selamat tinggal"]):
            konten_bicara = "Oke Irfan, Orochi istirahat dulu ya. Sampai jumpa!"
        else:
            waktu_jkt = datetime.now(pytz.timezone('Asia/Jakarta'))
            tgl_sekarang = waktu_jkt.strftime("%A, %d %B %Y")
            system_prompt = f"Hari ini {tgl_sekarang}. Jawab RINGKAS."
            
            full_response = ""
            stream = client.chat.completions.create(
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": last_msg}],
                model="llama-3.1-8b-instant", stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            konten_bicara = full_response

        # Update tampilan final
        message_placeholder.markdown(konten_bicara)
        # Putar suara dengan jeda antar kalimat
        play_audio_stream(konten_bicara)
        
        st.session_state.messages.append({"role": "assistant", "content": konten_bicara})
        time.sleep(1)
        st.session_state.status = "tidur" if "Sampai jumpa" in konten_bicara else "diam"
        st.rerun()
