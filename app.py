import streamlit as st
import os
from groq import Groq
from datetime import datetime
import pytz
from streamlit_geolocation import streamlit_geolocation

# Konfigurasi Halaman
st.set_page_config(page_title="Orochi AI", page_icon="🐍")

# 1. SETUP CLIENT
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("Orochi AI")

# 2. DETEKSI LOKASI OTOMATIS
st.write("Mendeteksi lokasi Komandan...")
location = streamlit_geolocation()

# Format lokasi untuk AI
if location['latitude'] is not None:
    lokasi_info = f"Latitude: {location['latitude']}, Longitude: {location['longitude']}"
else:
    lokasi_info = "Lokasi tidak terdeteksi (Pastikan GPS/Izin Lokasi Aktif)"

# 3. CHAT LOGIC
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_msg = "Hai Komandan! Orochi siap membantu. Saya sudah mengaktifkan sensor lokasi untuk mendeteksi posisi Anda saat ini."
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Apa perintahmu, Komandan?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        tz = pytz.timezone('Asia/Jakarta')
        now = datetime.now(tz)
        
        system_prompt = (
            f"Kamu Orochi, asisten setia Komandan Irfan. "
            f"DATA GPS REAL-TIME: {lokasi_info}. "
            "Gaya bicara: santai, WA style, cerdas. Jika ditanya lokasi, gunakan data GPS ini."
        )
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )
        response = chat_completion.choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
