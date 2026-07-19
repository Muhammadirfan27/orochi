import streamlit as st
import time
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

# --- FUNGSI TTS ELEVENLABS (DENGAN JEDA) ---
def play_chunk(text):
    """Mengubah teks menjadi audio per potongan dan memutarnya"""
    try:
        audio_stream = eleven_client.text_to_speech.convert(
            text=text,
            voice_id="EXAVITQu4vr4xnSDxMaL", 
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        audio_data = b"".join(audio_stream)
        b64 = base64.b64encode(audio_data).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)
    except Exception:
        pass

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
    header, footer, #MainMenu, .stAppToolbar, [data-testid="stHeader"], hr, .stMarkdown hr, div.stMarkdown > hr {{
        visibility: hidden !important; display: none !important;
    }}
    iframe {{ width: 1px !important; height: 1px !important; opacity: 0 !important; position: absolute !important; pointer-events: none !important; }}
    [data-testid="stAppViewContainer"] {{
        background-image: url('{gif_url}') !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        will-change: background-image;
        backface-visibility: hidden;
    }}
    [data-testid="stChatMessageContent"] {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: white !important;
    }}
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
    prompt_lower = prompt.lower()
    if st.session_state.status == "tidur":
        if any(word in prompt_lower for word in ["hallo", "halo", "hai", "bangun"]):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.status = "bicara"
        else:
            st.warning("Orochi masih tidur, Irfan. Bilang 'hallo' atau 'bangun' dulu ya.")
            st.stop()
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        if any(word in prompt_lower for word in ["bye", "selamat tinggal"]):
            st.session_state.status = "bicara"
        else:
            st.session_state.status = "berfikir"
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
            konten_bicara = "Halo juga Irfan! Orochi sudah bangun. Ada yang bisa dibantu?"
        elif any(w in last_user_msg for w in ["bye", "selamat tinggal"]):
            konten_bicara = "Oke Irfan, Orochi istirahat dulu ya. Sampai jumpa!"
        else:
            waktu_jkt = datetime.now(pytz.timezone('Asia/Jakarta'))
            nama_hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
            tgl_sekarang = waktu_jkt.strftime(f"{nama_hari[waktu_jkt.weekday()]}, %d %B %Y")
            
            system_prompt = (
                f"Hari ini adalah {tgl_sekarang}. WAJIB menggunakan bahasa Indonesia yang baik. "
                "Jangan gunakan bahasa Inggris sama sekali. Jika ditanya tentang Pancasila, "
                "WAJIB menjawab dengan teks resmi: 1. Ketuhanan Yang Maha Esa. "
                "2. Kemanusiaan yang adil dan beradab. 3. Persatuan Indonesia. "
                "4. Kerakyatan yang dipimpin oleh hikmat kebijaksanaan dalam permusyawaratan/perwakilan. "
                "5. Keadilan sosial bagi seluruh rakyat Indonesia. Jawab dengan ringkas."
            )
            
            full_response = ""
            try:
                stream = client.chat.completions.create(
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": last_user_msg}],
                    model="llama-3.1-8b-instant",
                    stream=True
                )
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                konten_bicara = full_response
            except Exception:
                konten_bicara = "Maaf, Orochi lagi ada kendala teknis."

        # --- EFEK KETIK & SUARA SINKRON ---
        sentences = [s.strip() for s in konten_bicara.replace('!', '.').replace('?', '.').split('.') if s.strip()]
        displayed_text = ""
        for sentence in sentences:
            play_chunk(sentence) # Suara per kalimat
            for char in sentence + ". ":
                displayed_text += char
                message_placeholder.markdown(displayed_text + "▌")
                time.sleep(0.08) # Kecepatan ketikan agar sinkron dengan suara
        
        message_placeholder.markdown(displayed_text)
        st.session_state.messages.append({"role": "assistant", "content": konten_bicara})
        
        time.sleep(1)
        st.session_state.status = "tidur" if "Sampai jumpa" in konten_bicara else "diam"
        st.rerun()
