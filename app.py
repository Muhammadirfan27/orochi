import streamlit as st
import os
from groq import Groq
from datetime import datetime
import pytz

# Konfigurasi Halaman
st.set_page_config(page_title="Orochi AI", page_icon="🐍")

# 1. PENGAMBILAN API KEY
try:
    if "GROQ_API_KEY" not in st.secrets:
        raise ValueError("API Key belum ditemukan di Secrets!")
    api_key = st.secrets["GROQ_API_KEY"]
except ValueError as e:
    st.error(f"Error Konfigurasi API: {e}")
    st.stop()

# Cari API key di environment
if not api_key:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        st.error("API Key tidak ditemukan!")
        st.stop()

client = Groq(api_key=api_key)

st.title("Orochi AI")

# 2. INISIALISASI CHAT HISTORY
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. TAMPILKAN HISTORY CHAT
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(message["content"], unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(message["content"], unsafe_allow_html=True)

# 4. PROSES CHAT
if prompt := st.text_input("Apa perintahmu, Komandan?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.markdown("<hr>", unsafe_allow_html=True):
        st.markdown(prompt, unsafe_allow_html=True)

    with st.markdown("<hr>", unsafe_allow_html=True):
        with st.markdown("<strong>Orochi</strong>", unsafe_allow_html=True):
            with st.markdown("<strong>Waktu:</strong>", unsafe_allow_html=True):
                st.markdown("", unsafe_allow_html=True)

            tz = pytz.timezone('Asia/Jakarta')
            now = datetime.now(tz)
            waktu = now.strftime("%A, %d %B %Y (Jam %H:%M WIB)")

            system_prompt = (
                f"Kamu Orochi, asisten setia Pak Irfan, Aku dirancang untuk membantumu. "
                f"Waktu sekarang: {waktu}. "
                "Gaya bicara: santai, WA style, jangan kaku, solutif, gunakan maksimal 2 emoji."
            )

            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.1-8b-instant", 
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error API: {e}")
                if "401" in str(e):
                    st.warning("Pesan 401: Kunci API salah. Pastikan kuncinya benar di Settings > Secrets.")
