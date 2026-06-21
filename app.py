import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz
from streamlit_javascript import st_javascript # WAJIB INSTALL: pip install streamlit-javascript

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. LOGIKA LOKASI (AKTIF) ---
# Menggunakan st_javascript untuk menarik posisi secara real-time
location_js = """
navigator.geolocation.getCurrentPosition(
    (pos) => ({lat: pos.coords.latitude, lon: pos.coords.longitude}),
    (err) => ({error: err.message})
)
"""
# Menjalankan JS untuk mendapatkan data
loc_data = st_javascript(location_js)

# Simpan ke session state
if "lokasi_user" not in st.session_state:
    st.session_state.lokasi_user = "Mencari lokasi..."

if loc_data and 'lat' in loc_data:
    st.session_state.lokasi_user = f"Lat: {loc_data['lat']}, Lon: {loc_data['lon']}"

# --- 3. LOGIKA STATE & PROFIL ---
PROFIL_KOMANDAN = {"Nama": "Irfan", "Pekerjaan": "Admin Warehouse"}
if "status" not in st.session_state: st.session_state.status = "diam"
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Siap Komandan Irfan, Orochi siap melayani."}]

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
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Perintah untuk Orochi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.status = "berfikir"
    st.rerun()

if st.session_state.status == "berfikir":
    st.session_state.status = "bicara"
    
    # AI sekarang tahu lokasi dari variabel st.session_state.lokasi_user
    sys_prompt = f"Kamu Orochi. Lokasi Komandan Irfan saat ini: {st.session_state.lokasi_user}. Jawab cerdas dan akurat."
    
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": sys_prompt}] + st.session_state.messages,
        model="llama-3.1-8b-instant"
    ).choices[0].message.content
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.status = "diam"
    st.rerun()
