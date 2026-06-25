import streamlit as st
import time
from groq import Groq
from datetime import datetime, timedelta
import pytz
from streamlit_js_eval import streamlit_js_eval

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. INITIAL STATE ---
if "status" not in st.session_state: st.session_state.status = "diam"
if "last_active" not in st.session_state: st.session_state.last_active = datetime.now()
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Halo Irfan! Orochi di sini. Ada yang bisa kubantu?"}]

# --- 3. FITUR AUTO-TIDUR (Jika diam > 5 menit) ---
if (datetime.now() - st.session_state.last_active).total_seconds() > 300 and st.session_state.status != "tidur":
    st.session_state.status = "tidur"

# --- 4. CSS ---
gif_url = f"https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/templates/Orochi_{st.session_state.status}.gif"

st.markdown(f"""
    <style>
    header, footer, #MainMenu, [data-testid="stHeader"] {{ visibility: hidden !important; }}
    [data-testid="stAppViewContainer"] {{
        background-image: url('{gif_url}') !important;
        background-size: cover !important; background-attachment: fixed !important;
    }}
    [data-testid="stChatMessageContent"] {{ background-color: rgba(0,0,0,0.3) !important; color: white !important; border-radius: 15px; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIKA CHAT ---
def get_avatar(): return "templates/Orochi.png"

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=get_avatar() if msg["role"]=="assistant" else None):
        st.markdown(msg["content"])

# --- 6. INPUT CHAT ---
if prompt := st.chat_input("Ngobrol santai sama Orochi..."):
    st.session_state.last_active = datetime.now()
    
    if st.session_state.status == "tidur" and not any(w in prompt.lower() for w in ["hallo", "halo", "bangun"]):
        st.warning("Orochi masih tidur, Irfan. Bilang 'hallo' atau 'bangun' dulu.")
        st.stop()
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.status = "berfikir"
    st.rerun()

# --- 7. LOGIKA PROSES ---
if st.session_state.status == "berfikir":
    time.sleep(1)
    st.session_state.status = "bicara"
    st.rerun()

if st.session_state.status == "bicara":
    with st.chat_message("assistant", avatar=get_avatar()):
        message_placeholder = st.empty()
        last_user = st.session_state.messages[-1]["content"].lower()
        
        # Logika Penentuan Respons
        if any(w in last_user for w in ["hallo", "halo", "hai", "bangun"]):
            konten = "Halo Irfan! Orochi sudah bangun. Siap menemani hari ini."
        elif any(w in last_user for w in ["bye", "selamat tinggal"]):
            konten = "Oke Irfan, Orochi istirahat dulu ya. Sampai jumpa!"
        else:
            # Mengirim konteks chat terakhir (5 pesan terakhir agar ringan)
            context = st.session_state.messages[-6:-1]
            try:
                stream = client.chat.completions.create(
                    messages=[{"role": "system", "content": "Kamu adalah Orochi, asisten AI pribadi Irfan. Singkat, padat, dan ramah."}] + context + [{"role": "user", "content": last_user}],
                    model="llama-3.1-8b-instant",
                    stream=True
                )
                full = ""
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full += chunk.choices[0].delta.content
                        message_placeholder.markdown(full + "▌")
                konten = full
            except Exception:
                konten = "Maaf, koneksi ke server sedang ada kendala."
        
        message_placeholder.markdown(konten)
        st.session_state.messages.append({"role": "assistant", "content": konten})
        
        # Transisi Status
        st.session_state.status = "tidur" if "Sampai jumpa" in konten else "diam"
        st.rerun()
