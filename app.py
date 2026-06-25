import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz
from streamlit_js_eval import streamlit_js_eval

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
    st.session_state.lokasi = f"Lat: {loc['coords']['latitude']}, Lon: {loc['coords']['longitude']}"
else:
    st.session_state.lokasi = "Panongan, Tangerang"

# --- 4. CSS ---
gif_url = f"https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/templates/Orochi_{st.session_state.status}.gif"

st.markdown(f"""
    <style>
    header, footer, [data-testid="stHeader"] {{ visibility: hidden !important; }}
    [data-testid="stAppViewContainer"] {{
        background-image: url('{gif_url}') !important;
        background-size: cover !important; background-attachment: fixed !important;
    }}
    [data-testid="stChatMessageContent"] {{ background-color: rgba(0,0,0,0.5) !important; color: white !important; border-radius: 15px; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIKA CHAT ---
def get_avatar(role):
    return "templates/Orochi.png" if role == "assistant" else None

# Tampilkan history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=get_avatar(msg["role"])):
        st.markdown(msg["content"])

# Input User
if prompt := st.chat_input("Ngobrol santai sama Orochi..."):
    if st.session_state.status == "tidur" and not any(w in prompt.lower() for w in ["hallo", "halo", "bangun"]):
        st.warning("Orochi masih tidur. Bilang 'bangun' dulu ya.")
        st.stop()
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.status = "berfikir"
    st.rerun()

# --- 6. LOGIKA AI & TRANSISI ---
if st.session_state.status == "berfikir":
    with st.chat_message("assistant", avatar=get_avatar("assistant")):
        message_placeholder = st.empty()
        
        # Waktu & Konteks
        waktu_jkt = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%A, %d %B %Y %H:%M")
        
        # System Persona
        system_prompt = f"""Kamu adalah Orochi, AI asisten pribadi Irfan. 
        Lokasi saat ini: {st.session_state.lokasi}. Waktu saat ini: {waktu_jkt}.
        Kepribadian: Cerdas, santai, setia, dan sedikit misterius.
        Aturan: Jawab dengan sangat ringkas, gunakan bahasa Indonesia yang luwes, jangan bertele-tele."""

        # Mengambil 10 pesan terakhir untuk memori (Kecerdasan Konteks)
        context = st.session_state.messages[-10:]
        
        try:
            stream = client.chat.completions.create(
                messages=[{"role": "system", "content": system_prompt}] + context,
                model="llama-3.1-8b-instant",
                stream=True
            )
            
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            # Transisi status
            if any(w in full_response.lower() for w in ["istirahat", "tidur", "sampai jumpa"]):
                st.session_state.status = "tidur"
            else:
                st.session_state.status = "diam"
            st.rerun()
            
        except Exception as e:
            st.error("Orochi sedang kehilangan sinyal...")
            st.session_state.status = "diam"
