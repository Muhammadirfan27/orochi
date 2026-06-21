import streamlit as st
from groq import Groq
from datetime import datetime
import pytz

# Konfigurasi halaman
st.set_page_config(page_title="Orochi AI", page_icon="🐍")

# Inisialisasi Groq
# Pastikan di Secrets sudah ada GROQ_API_KEY
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("Orochi AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input user
if prompt := st.chat_input("Apa perintahmu, Komandan?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        tz = pytz.timezone('Asia/Jakarta')
        now = datetime.now(tz)
        waktu = now.strftime("%A, %d %B %Y (Jam %H:%M WIB)")
        
        system_prompt = f"Kamu adalah Orochi, asisten setia Komandan Irfan dari dunia Acma:Game. Waktu sekarang: {waktu}. Gaya chat: santai, WhatsApp style, max 2 emoji."
        
        try:
            stream = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192",
            )
            response = stream.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Waduh, ada kendala: {e}")
