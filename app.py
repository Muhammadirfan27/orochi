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

# --- AVATAR KUSTOM (PERBAIKAN) ---
def get_avatar(role):
    if role == "assistant":
        # Gunakan path relatif atau URL yang bisa diakses web
        # Pastikan file ada di folder tersebut dan bisa diakses publik
        return "templates/Orochi.png" 
    return None

# 1. Tampilkan riwayat chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=get_avatar(msg["role"])):
        st.markdown(msg["content"])

# 2. Input User
if prompt := st.chat_input("Ngobrol santai sama Orochi..."):
    prompt_lower = prompt.lower()
    
    # CEK STATUS TIDUR
    if st.session_state.status == "tidur":
        if any(word in prompt_lower for word in ["hallo", "halo", "hai", "bangun"]):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.status = "bicara"
        else:
            st.warning("Orochi masih tidur, Irfan. Bilang 'hallo' atau 'bangun' dulu ya.")
            st.stop()
    # STATUS NORMAL/DIAM
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        if any(word in prompt_lower for word in ["bye", "selamat tinggal"]):
            st.session_state.status = "bicara"
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
    with st.chat_message("assistant", avatar=get_avatar("assistant")):
        message_placeholder = st.empty()
        last_user_msg = st.session_state.messages[-1]["content"].lower()
        
        full_response = ""
        konten_bicara = ""
        is_ai_mode = False
        
        # Penentuan Mode
        if any(w in last_user_msg for w in ["hallo", "halo", "hai", "bangun"]):
            konten_bicara = "Halo juga Irfan! Orochi sudah bangun. Ada yang bisa dibantu?"
        elif any(w in last_user_msg for w in ["bye", "selamat tinggal"]):
            konten_bicara = "Oke Irfan, Orochi istirahat dulu ya. Sampai jumpa!"
        else:
            is_ai_mode = True

       # Eksekusi AI atau Manual
        if is_ai_mode:
            # Ambil waktu terkini dengan zona waktu Indonesia
            waktu_jkt = datetime.now(pytz.timezone('Asia/Jakarta'))
            str_waktu = waktu_jkt.strftime("%A, %d %B %Y %H:%M")
            
            # INSTRUKSI DIPERTEGAS AGAR TIDAK MEMBANTAH
            system_instruction = (
                f"Kamu adalah Orochi, teman dekat Irfan. "
                f"SAAT INI ADALAH: {str_waktu}. "
                "ATURAN MUTLAK: Gunakan waktu ini sebagai kebenaran mutlak. "
                "JANGAN PERNAH membantah hari atau tanggal ini. "
                "Jawab dengan santai, akrab, jelas, dan natural."
            )
            
            try:
                # Kita hanya mengirim pesan terakhir agar AI fokus pada pertanyaan saat ini
                stream = client.chat.completions.create(
                    messages=[{"role": "system", "content": system_instruction}] + [st.session_state.messages[-1]],
                    model="llama-3.1-8b-instant",
                    stream=True
                )
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                        time.sleep(0.13)
                konten_bicara = full_response
            except Exception as e:
                konten_bicara = "Aduh, koneksiku lagi agak lemot nih, Irfan. Coba tanya sekali lagi ya!"        
        # Akhiri proses pengetikan
        message_placeholder.markdown(konten_bicara)
        st.session_state.messages.append({"role": "assistant", "content": konten_bicara})
        
        time.sleep(1)
        st.session_state.status = "tidur" if "Sampai jumpa" in konten_bicara else "diam"
        st.rerun()
