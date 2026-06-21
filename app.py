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
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ngobrol santai sama Orochi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    prompt_lower = prompt.lower()
    
    # LOGIKA BARU: Jika sedang tidur, bangunkan dulu untuk semua jenis input
    if st.session_state.status == "tidur":
        if "bye" not in prompt_lower: # Kalau user ngetik apa saja selain bye
            st.session_state.status = "bicara"
            st.session_state.messages.append({"role": "assistant", "content": "Eh, Irfan! Orochi bangun. Ada apa nih?"})
        else:
            # Kalau sedang tidur tapi disuruh bye lagi
            st.session_state.messages.append({"role": "assistant", "content": "Iya, aku kan udah tidur, Irfan..."})
            
    # LOGIKA BIASA: Jika tidak tidur, cek perintah khusus
    elif "bye" in prompt_lower or "selamat tinggal" in prompt_lower:
        st.session_state.status = "bicara"
        st.session_state.messages.append({"role": "assistant", "content": "Oke Irfan, Orochi istirahat dulu ya. Sampai jumpa!"})
    elif "hallo" in prompt_lower or "halo" in prompt_lower or "hai" in prompt_lower or "bangun" in prompt_lower:
        st.session_state.status = "bicara"
        st.session_state.messages.append({"role": "assistant", "content": "Halo juga Irfan! Orochi sudah bangun. Ada yang bisa dibantu?"})
    else:
        st.session_state.status = "berfikir"
    
    st.rerun()

# --- SISANYA SAMA SEPERTI KODE SEBELUMNYA ---
if st.session_state.status == "berfikir":
    time.sleep(1) 
    st.session_state.status = "bicara"
    st.rerun()

if st.session_state.status == "bicara":
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        last_msg = st.session_state.messages[-1]
        
        # Cek apakah pesan terakhir adalah respon sapaan/bye yang kita buat manual
        if last_msg.get("role") == "assistant" and (
            "Orochi bangun" in last_msg["content"] or 
            "Halo" in last_msg["content"] or 
            "Sampai jumpa" in last_msg["content"] or
            "tidur" in last_msg["content"]
        ):
            # Efek ketik untuk respon manual
            text = last_msg["content"]
            full_response = ""
            for char in text:
                full_response += char
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.08)
            message_placeholder.markdown(full_response)
        else:
            # Respon AI biasa
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
        if "Sampai jumpa" in last_msg["content"]:
            st.session_state.status = "tidur"
        else:
            st.session_state.status = "diam"
        st.rerun()
            
        st.rerun()
