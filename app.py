import streamlit as st
import os
from groq import Groq
from datetime import datetime
import pytz

# Konfigurasi Halaman
st.set_page_config(page_title="Orochi AI", page_icon="🐍")

# 1. PENGAMBILAN API KEY DENGAN LOGIKA CADANGAN
# Mencoba mengambil dari Streamlit Secrets, jika gagal ambil dari environment variable
try:
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        api_key = os.environ.get("GROQ_API_KEY")
        
    if not api_key:
        raise ValueError("API Key tidak ditemukan!")
        
    # Inisialisasi client
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Error Konfigurasi API: {e}")
    st.info("Pastikan GROQ_API_KEY sudah diisi di Settings > Secrets pada dashboard Streamlit.")
    st.stop()

st.title("Orochi AI")

# Inisialisasi history chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan history chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Chat
if prompt := st.chat_input("Apa perintahmu, Komandan?"):
    # Simpan chat user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate jawaban
    with st.chat_message("assistant"):
        tz = pytz.timezone('Asia/Jakarta')
        now = datetime.now(tz)
        waktu = now.strftime("%A, %d %B %Y (Jam %H:%M WIB)")
        
        system_prompt = f"Kamu Orochi, asisten setia Komandan Irfan dari dunia Acma:Game. Waktu sekarang: {waktu}. Gaya: santai, WA style, max 2 emoji."
        
        try:
            chat_completion = # Ganti model lama dengan yang terbaru
model="llama-3.1-8b-instant"(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192",
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error API: {e}")
            if "401" in str(e):
                st.warning("Pesan 401 berarti kunci API salah atau tidak terbaca. Coba buat kunci baru di console.groq.com dan update di Secrets!")
