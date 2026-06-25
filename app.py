import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz
from streamlit_js_eval import streamlit_js_eval

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")
# Pastikan API key sudah diatur di Streamlit Secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. INITIAL STATE ---
if "status" not in st.session_state: st.session_state.status = "diam"
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Halo Irfan! Orochi di sini. Ada yang bisa kubantu?"}]

# --- 3. LOKASI ---
loc = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition((pos) => {window.parent.postMessage({lat: pos.coords.latitude, lon: pos.coords.longitude}, "*")})', want_output=True, key='loc')
st.session_state.lokasi_tersimpan = "Panongan, Tangerang"
if loc:
    st.session_state.lokasi_tersimpan = f"Lat: {loc['coords']['latitude']}, Lon: {loc['coords']['longitude']}"

# --- 4. CSS ---
gif_url = f"https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/templates/Orochi_{st.session_state.status}.gif"

st.markdown(f"""
    <style>
    header, footer, #MainMenu, .stAppToolbar, [data-testid="stHeader"], hr {{
        visibility: hidden !important; display: none !important;
    }}
    [data-testid="stAppViewContainer"] {{
        background-image: url('{gif_url}') !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    [data-testid="stChatMessageContent"] {{ background-color: transparent !important; color: white !important; }}
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
        
        if any(w in last_user_msg for w in ["hallo", "halo", "hai", "bangun"]):
            konten_bicara = "Halo juga Irfan! Orochi sudah bangun. Ada yang bisa dibantu?"
        elif any(w in last_user_msg for w in ["bye", "selamat tinggal"]):
            konten_bicara = "Oke Irfan, Orochi istirahat dulu ya. Sampai jumpa!"
        else:
            waktu_jkt = datetime.now(pytz.timezone('Asia/Jakarta'))
            tgl_sekarang = waktu_jkt.strftime("%A, %d %B %Y")
            
            system_prompt = (
                f"Hari ini adalah {tgl_sekarang}. Jawab dengan sangat ringkas."
            )
            
            full_response = ""
            try:
                stream = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": last_user_msg}
                    ],
                    model="llama-3.1-8b-instant",
                    stream=True
                )
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                konten_bicara = full_response
            except Exception as e:
                konten_bicara = "Maaf, Orochi sedang ada gangguan teknis. Bisa ulangi pertanyaannya?"

        message_placeholder.markdown(konten_bicara)
        st.session_state.messages.append({"role": "assistant", "content": konten_bicara})
        
        # Logika transisi status
        if "Sampai jumpa" in konten_bicara:
            st.session_state.status = "tidur"
        else:
            st.session_state.status = "diam"
        st.rerun()
