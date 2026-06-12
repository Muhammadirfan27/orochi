import streamlit as st
import google.generativeai as genai
from datetime import datetime
import pytz

# Konfigurasi halaman
st.set_page_config(page_title="Orochi AI", page_icon="🐍")

# Konfigurasi API
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Menggunakan gemini-1.5-pro yang lebih stabil
  
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error konfigurasi API: {e}")

# Fungsi Waktu Jakarta
def get_jakarta_time():
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.now(tz)
    hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    return now.strftime(f"{hari[now.weekday()]}, %d %B %Y (Jam %H:%M WIB)")

# Instruksi Orochi
system_instruction = f"""
Kamu adalah Orochi, AI asisten masa depan yang cerdas, setia, dan ekspresif dari dunia Acma:Game.
SAAT INI ADALAH: {get_jakarta_time()}.
Gunakan gaya bahasa santai seperti chat WhatsApp, panggil user "Komandan Irfan", dan gunakan maksimal 2 emoji per balasan.
"""

# Tampilan Chat
st.title("Orochi AI")
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan riwayat chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Chat
if prompt := st.chat_input("Apa perintahmu, Komandan?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            full_prompt = system_instruction + "\nUser: " + prompt
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Waduh Komandan, ada kendala teknis (Model/API): {e}")
