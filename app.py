import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz
import streamlit.components.v1 as components

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. LOKASI ENGINE (HTML5 MURNI - TANPA PIP INSTALL) ---
# Menggunakan JavaScript untuk mengirim data ke Streamlit melalui query parameter/callback
location_tracker = """
<script>
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition((pos) => {
                window.parent.postMessage({type: 'loc', lat: pos.coords.latitude, lon: pos.coords.longitude}, '*');
            });
        }
    }
    getLocation();
</script>
"""
components.html(location_tracker, height=0)

# --- 3. LOGIKA STATE ---
if "status" not in st.session_state: st.session_state.status = "diam"
if "lokasi_user" not in st.session_state: st.session_state.lokasi_user = "Lokasi belum diizinkan"

# --- 4. CSS DYNAMIC ---
gif_url = f"https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/Orochi_{st.session_state.status}.gif"
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url('{gif_url}'); background-size: cover;
        background-position: center; background-attachment: fixed;
    }}
    .stApp {{ background: transparent !important; }}
    [data-testid="stChatMessageContent"] {{ 
        background: rgba(0, 0, 0, 0.6) !important; color: white !important; border-radius: 15px;
    }}
    header, footer {{ visibility: hidden; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIKA CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Siap Komandan, Orochi aktif."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.status = "berfikir"
    st.rerun()

if st.session_state.status == "berfikir":
    st.session_state.status = "bicara"
    sys_prompt = f"Kamu Orochi. Asisten Irfan. Lokasi Terakhir: {st.session_state.lokasi_user}. Jawab cerdas & berwibawa."
    
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages,
        model="llama-3.1-8b-instant"
    ).choices[0].message.content
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.status = "diam"
    st.rerun()
