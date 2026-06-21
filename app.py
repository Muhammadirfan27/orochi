import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz
from streamlit_js_eval import streamlit_js_eval

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. FITUR 1: BRIDGE LOKASI (REAL-TIME) ---
loc = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition((pos) => {window.parent.postMessage({lat: pos.coords.latitude, lon: pos.coords.longitude}, "*")})', want_output=True, key='loc')

# --- 3. FITUR 2: MEMORI PERSISTEN ---
if "lokasi_tersimpan" not in st.session_state:
    st.session_state.lokasi_tersimpan = "Panongan, Tangerang"
if loc:
    st.session_state.lokasi_tersimpan = f"Lat: {loc['coords']['latitude']}, Lon: {loc['coords']['longitude']}"

# --- 4. FITUR 3: DYNAMIC PERSONALITY ENGINE ---
def get_orochi_mood():
    h = datetime.now(pytz.timezone('Asia/Jakarta')).hour
    if 0 <= h < 5: return "tidur"
    if 5 <= h < 11: return "diam" # Gunakan 'diam' jika GIF itu yang ada
    return "diam"

st.session_state.status = get_orochi_mood()

# --- 5. CSS BACKGROUND GIF (YANG DITUNGGU-TUNGGU) ---
gif_url = f"https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/Orochi_{st.session_state.status}.gif"

st.markdown("""
    <style>
    /* Sembunyikan elemen bawaan Streamlit yang memunculkan garis */
    header, footer, #MainMenu, .stAppToolbar, [data-testid="stHeader"], hr {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* Hapus garis yang dihasilkan oleh iframe komponen JS */
    iframe {
        display: none !important;
    }

    /* Pastikan tidak ada padding di bagian atas */
    .block-container { 
        padding-top: 0rem !important; 
    }
    </style>
""", unsafe_allow_html=True)

# --- 6. LOGIKA CHAT & SENSORY FEEDBACK ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"Orochi aktif. Komandan Irfan terpantau di {st.session_state.lokasi_tersimpan}."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # FITUR 4: SENSORY FEEDBACK (Spinner)
    with st.spinner("Orochi sedang menganalisis situasi..."):
        sys_prompt = f"Nama: Orochi. Komandan: Irfan. Lokasi: {st.session_state.lokasi_tersimpan}. Jawab cerdas & berwibawa."
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages,
            model="llama-3.1-8b-instant"
        ).choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# FITUR 5: PROACTIVE NOTIFICATION
if "last_toast" not in st.session_state: st.session_state.last_toast = time.time()
if time.time() - st.session_state.last_toast > 1800:
    st.toast("Orochi: Saya tetap siaga memantau koordinat Komandan.")
    st.session_state.last_toast = time.time()
