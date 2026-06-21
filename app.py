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
    /* Hapus header, footer, dan menu default */
    header, footer, #MainMenu, .stAppToolbar, [data-testid="stHeader"], hr {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* JANGAN sembunyikan iframe dengan display: none */
    /* Karena jika disembunyikan, fungsi lokasi JS akan mati */
    /* Cukup buat ukurannya menjadi sangat kecil agar tidak terlihat */
    iframe {
        width: 1px !important;
        height: 1px !important;
        opacity: 0 !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        pointer-events: none !important;
    }

    /* Pastikan background full screen */
    [data-testid="stAppViewContainer"] {
        background-image: url('""" + gif_url + """');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    .block-container { padding-top: 0rem !important; }
    </style>
""", unsafe_allow_html=True)

# --- 6. LOGIKA CHAT & SENSORY FEEDBACK ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Orochi aktif, Komandan."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Deteksi Idle (Mode Tidur) ---
if "last_interaction" not in st.session_state: st.session_state.last_interaction = time.time()
if time.time() - st.session_state.last_interaction > 5: # Jika lebih dari 5 detik tidak ada chat
    st.session_state.status = "tidur" 
else:
    st.session_state.status = "diam"

if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.last_interaction = time.time()
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Mode Berpikir
    st.session_state.status = "berfikir"
    st.rerun() # Paksa rerun untuk update GIF ke mode berfikir

# --- Proses Respon (Jika user baru saja chat) ---
if st.session_state.status == "berfikir":
    # Jeda 1 detik untuk menunjukkan Orochi sedang berpikir
    time.sleep(1)
    
    # Mode Bicara
    st.session_state.status = "bicara"
    
    sys_prompt = f"Nama: Orochi. Komandan: Irfan. Lokasi: {st.session_state.lokasi_tersimpan}. Jawab cerdas & berwibawa."
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages,
        model="llama-3.1-8b-instant"
    ).choices[0].message.content
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.status = "diam"
    st.session_state.last_interaction = time.time()
    st.rerun()
