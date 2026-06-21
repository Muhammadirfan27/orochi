import streamlit as st
import os
from groq import Groq
from datetime import datetime
import pytz

# Konfigurasi Halaman
st.set_page_config(page_title="Orochi AI", page_icon="🐍")

# 1. PENGAMBILAN API KEY
try:
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        raise ValueError("API Key tidak ditemukan!")
        
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Error Konfigurasi API: {e}")
    st.stop()

st.title("Orochi AI")

# 2. INISIALISASI CHAT & PESAN SAMBUTAN
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_msg = "Hai, aku Orochi, asisten setia Pak Irfan  🤖 Saya disini untuk membantu dan menyediakan informasi yang kamu butuhkan. Semoga hari kamu menyenangkan!"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# 3. TAMPILKAN HISTORY
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. LOGIKA CHAT DENGAN KONTEKS LOKASI
if prompt := st.chat_input("Apa perintahmu, Komandan?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Waktu Jakarta
        tz = pytz.timezone('Asia/Jakarta')
        now = datetime.now(tz)
        waktu = now.strftime("%A, %d %B %Y (Jam %H:%M WIB)")
        
        # Lokasi yang sudah disematkan (Hard-coded context)
        lokasi = "South Tangerang, Banten, Indonesia"
        
        system_prompt = (
            f"Kamu Orochi, asisten setia Komandan Irfan dari dunia Acma:Game. "
            f"IDENTITAS LOKASI: Komandan Irfan saat ini berada di {lokasi}. "
            f"WAKTU SEKARANG: {waktu}. "
            "Gaya bicara: santai, WA style, cerdas, solutif, gunakan maksimal 2 emoji. "
            "Jika ditanya lokasi, jawab dengan data lokasi di atas."
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
