import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz
from streamlit_js_eval import streamlit_js_eval

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. FITUR LOKASI ---
loc = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition((pos) => {window.parent.postMessage({lat: pos.coords.latitude, lon: pos.coords.longitude}, "*")})', want_output=True, key='loc')

if "lokasi_tersimpan" not in st.session_state:
    st.session_state.lokasi_tersimpan = "Panongan, Tangerang"
if loc:
    st.session_state.lokasi_tersimpan = f"Lat: {loc['coords']['latitude']}, Lon: {loc['coords']['longitude']}"

# --- 3. DYNAMIC PERSONALITY ENGINE ---
def get_orochi_mood():
    h = datetime.now(pytz.timezone('Asia/Jakarta')).hour
    if 0 <= h < 5: return "tidur"
    return "diam" 

st.session_state.status = get_orochi_mood()

# --- 4. CSS BACKGROUND (DENGAN FORMAT YANG TERBUKTI BERHASIL) ---
gif_url = f"https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/Orochi_{st.session_state.status}.gif"

st.markdown("""
    <style>
    header, footer, #MainMenu, .stAppToolbar, [data-testid="stHeader"], hr {
        visibility: hidden !important;
        display: none !important;
    }
    
    iframe {
        width: 1px !important;
        height: 1px !important;
        opacity: 0 !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        pointer-events: none !important;
    }

    [data-testid="stAppViewContainer"] {
        background-image: url('""" + gif_url + """');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    .block-container { padding-top: 0rem !important; }
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIKA CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"Orochi aktif. Komandan Irfan terpantau di {st.session_state.lokasi_tersimpan}."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner("Orochi sedang menganalisis situasi..."):
        sys_prompt = f"Nama: Orochi. Komandan: Irfan. Lokasi: {st.session_state.lokasi_tersimpan}. Jawab cerdas & berwibawa."
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages,
            model="llama-3.1-8b-instant"
        ).choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# --- 6. PROACTIVE NOTIFICATION ---
if "last_toast" not in st.session_state: st.session_state.last_toast = time.time()
if time.time() - st.session_state.last_toast > 1800:
    st.toast("Orochi: Saya tetap siaga memantau koordinat Komandan.")
    st.session_state.last_toast = time.time()
