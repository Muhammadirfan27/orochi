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
st.session_state.lokasi_tersimpan = "Panongan, Tangerang"
if loc:
    st.session_state.lokasi_tersimpan = f"Lat: {loc['coords']['latitude']}, Lon: {loc['coords']['longitude']}"

# --- 4. CSS DENGAN PATH YANG BENAR & CHAT TRANSPARAN ---
gif_url = f"https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/templates/Orochi_{st.session_state.status}.gif"

st.markdown(f"""
    <style>
    /* Sembunyikan elemen default */
    header, footer, #MainMenu, .stAppToolbar, [data-testid="stHeader"], hr {{
        visibility: hidden !important; display: none !important;
    }}
    iframe {{ width: 1px !important; height: 1px !important; opacity: 0 !important; position: absolute !important; pointer-events: none !important; }}
    
    /* Set Background */
    [data-testid="stAppViewContainer"] {{
        background-image: url('{gif_url}') !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    
    /* MENGHILANGKAN KOTAK CHAT */
    [data-testid="stChatMessageContent"] {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: white !important; /* Agar teks tetap terlihat jelas */
    }}
    
    .stChatMessage {{
        background-color: transparent !important;
    }}

    /* Menghilangkan background container utama chat */
    .block-container {{ 
        padding-top: 2rem !important; 
        background: transparent !important; 
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIKA CHAT & PERSONA ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ngobrol santai sama Orochi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Jeda 3 detik sebelum berubah status ke mode berfikir
    time.sleep(3)
    
    # Update status ke berfikir dan refresh halaman
    st.session_state.status = "berfikir"
    st.rerun()

# Logika AI berjalan jika status saat ini 'berfikir'
if st.session_state.status == "berfikir":
    with st.spinner("Orochi lagi mikir..."):
        # PERSONA: Teman akrab, santai, sopan, dan pintar
        sys_prompt = (
            "Kamu adalah Orochi, teman dekat Irfan. "
            "Gunakan bahasa yang super santai, akrab, dan asik tapi sopan. "
            "JANGAN gunakan bahasa formal, kaku, atau gaya militer. "
            "Anggap saja kalian lagi nongkrong bareng. "
            "Jawabannya harus natural, singkat, dan seru tapi harus jelas."
        )
        
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages,
            model="llama-3.1-8b-instant"
        ).choices[0].message.content
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Kembali ke mode diam setelah selesai
        st.session_state.status = "diam"
        st.rerun()
