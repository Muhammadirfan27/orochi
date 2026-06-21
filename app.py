import streamlit as st
import os
from groq import Groq
from datetime import datetime
import pytz

# Konfigurasi Halaman
st.set_page_config(page_title="Orochi AI", page_icon="🐍")

# 1. SETUP CLIENT
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("Orochi AI")

# 2. INISIALISASI CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_msg = "Hai Komandan! Orochi siap membantu. Ada yang bisa saya bantu hari ini?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# Tampilkan history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. PROSES CHAT
if prompt := st.chat_input("Apa perintahmu, Komandan?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        tz = pytz.timezone('Asia/Jakarta')
        now = datetime.now(tz)
        waktu = now.strftime("%A, %d %B %Y (Jam %H:%M WIB)")
        
        # Lokasi yang benar dan akurat
        lokasi_akurat = "South Tangerang, Banten, Indonesia"
        
        system_prompt = (
            f"Kamu Orochi, asisten setia Komandan Irfan. "
            f"LOKASI SAAT INI: {lokasi_akurat}. "
            f"WAKTU SAAT INI: {waktu}. "
            "Gaya bicara: santai, WA style, cerdas, solutif. "
            "Jika ditanya lokasi, jawab dengan: 'Komandan Irfan saat ini berada di South Tangerang, Banten, Indonesia'."
        )
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )
        response = chat_completion.choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
