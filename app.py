import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. CSS RESPONSIVE & LAYOUT ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    /* Memastikan GIF responsif di HP dan Laptop */
    .orochi-img { 
        width: 100%; 
        max-width: 400px; 
        display: block; 
        margin: auto; 
        border-radius: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. INISIALISASI STATE ---
if "status" not in st.session_state: st.session_state.status = "diam"
if "last_activity" not in st.session_state: st.session_state.last_activity = time.time()
if "messages" not in st.session_state: st.session_state.messages = [{"role": "assistant", "content": "Ada yang bisa saya bantu, Komandan?"}]

# --- 4. LOGIKA AUTO-TIDUR (10 DETIK) ---
if time.time() - st.session_state.last_activity > 10 and st.session_state.status == "diam":
    st.session_state.status = "tidur"

# --- 5. TAMPILAN GIF ---
gif_url = f"https://raw.githubusercontent.com/Muhammadirfan27/orochi/main/Orochi_{st.session_state.status}.gif"
st.markdown(f'<img src="{gif_url}" class="orochi-img">', unsafe_allow_html=True)

# --- 6. LOGIKA CHAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Apa perintahmu, Komandan?"):
    st.session_state.last_activity = time.time()
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.status = "berfikir"
    st.rerun()

# --- 7. STATE MACHINE (BERFIKIR -> BICARA -> DIAM) ---
if st.session_state.status == "berfikir":
    time.sleep(3) # Jeda 3 detik
    st.session_state.status = "bicara"
    
    # Panggilan AI
    memori = "Nama: Irfan, Pekerjaan: Admin Warehouse, Keahlian: Software Developer (PHP, IoT, MQTT)"
    system_prompt = f"Kamu Orochi. Data: {memori}. Instruksi: Jangan balas sapaan, langsung jawab dengan berwibawa."
    
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": st.session_state.messages[-1]["content"]}],
        model="llama-3.1-8b-instant"
    ).choices[0].message.content
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Durasi bicara sesuai panjang teks (minimal 3 detik)
    durasi_bicara = max(3, len(response) / 40)
    time.sleep(durasi_bicara)
    
    st.session_state.status = "diam"
    st.session_state.last_activity = time.time()
    st.rerun()
