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
    /* 1. Sembunyikan elemen default */
    header, footer, #MainMenu, .stAppToolbar, [data-testid="stHeader"], hr {{
        visibility: hidden !important; display: none !important;
    }}
    iframe {{ width: 1px !important; height: 1px !important; opacity: 0 !important; position: absolute !important; pointer-events: none !important; }}
    
    /* 2. Set Background */
    [data-testid="stAppViewContainer"] {{
        background-image: url('{gif_url}') !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        will-change: background-image;
        backface-visibility: hidden;
    }}
    
    /* 3. Menghilangkan Kotak Chat */
    [data-testid="stChatMessageContent"] {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: white !important;
    }}
    
    .stChatMessage {{
        background-color: transparent !important;
    }}

    /* 4. Menghilangkan background container utama */
    .block-container {{ 
        padding-top: 2rem !important; 
        background: transparent !important; 
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIKA CHAT & PERSONA ---
# 1. Tampilkan riwayat chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 2. Input User
if prompt := st.chat_input("Ngobrol santai sama Orochi..."):
    prompt_lower = prompt.lower()
    
    # CEK STATUS TIDUR
    if st.session_state.status == "tidur":
        # Hanya respon jika ingin bangun
        if any(word in prompt_lower for word in ["hallo", "halo", "hai", "bangun"]):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.status = "bicara"
            st.session_state.messages.append({"role": "assistant", "content": "Halo juga Irfan! Orochi sudah bangun. Ada yang bisa dibantu?"})
        else:
            # Abaikan input lain saat tidur
            st.warning("Orochi masih tidur, Irfan. Bilang 'hallo' atau 'bangun' dulu ya.")
            st.stop()
            
    # STATUS NORMAL/DIAM
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        if any(word in prompt_lower for word in ["bye", "selamat tinggal"]):
            st.session_state.status = "bicara"
            st.session_state.messages.append({"role": "assistant", "content": "Oke Irfan, Orochi istirahat dulu ya. Sampai jumpa!"})
        else:
            st.session_state.status = "berfikir"
    
    st.rerun()

# 3. Logika Transisi Status
if st.session_state.status == "berfikir":
    time.sleep(1) 
    st.session_state.status = "bicara"
    st.rerun()

# 4. Mode Bicara
if st.session_state.status == "bicara":
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        last_msg = st.session_state.messages[-1]
        
        # Pengecekan apakah ini respon manual (Sapaan/Bye)
        is_manual_response = any(phrase in last_msg["content"] for phrase in ["Halo", "Sampai jumpa", "Orochi sudah bangun"])
        
        if is_manual_response:
            # Efek ketik manual
            full_response = ""
            for char in last_msg["content"]:
                full_response += char
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.08)
            message_placeholder.markdown(full_response)
        else:
            # Efek ketik AI Streaming
            full_response = ""
            stream = client.chat.completions.create(
                messages=[{"role": "system", "content": "Kamu Orochi, teman dekat Irfan. Jawab santai, akrab, jelas, dan natural."}] + st.session_state.messages[:-1],
                model="llama-3.1-8b-instant",
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.13)
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        time.sleep(1)
        
        # Penentuan status akhir
        if "Sampai jumpa" in last_msg["content"]:
            st.session_state.status = "tidur"
        else:
            st.session_state.status = "diam"
        st.rerun()
            
        st.rerun()
