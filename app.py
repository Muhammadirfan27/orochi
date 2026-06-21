import streamlit as st
import os
from groq import Groq
from datetime import datetime
import pytz

# 1. Konfigurasi
st.set_page_config(page_title="Orochi AI", page_icon="🐍")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("Orochi AI")

# 2. PROFIL KOMANDAN
PROFIL_KOMANDAN = {
    "Nama": "Irfan",
    "Pekerjaan": "Admin Warehouse",
    "Pendidikan": "Mahasiswa Tingkat Akhir",
    "Alamat": "Jl. Swadaya III, Ciakar, Kec. Panongan, Kabupaten Tangerang, Banten 15710, Perum Golden Residence",
    "Keahlian": "Software Developer (PHP, IoT, MQTT)",
    "Hobi": "Esports (Inferno Demons), Anime Kekkaishi"
}

# 3. FUNGSI SAPAAN WAKTU
def get_sapaan():
    tz = pytz.timezone('Asia/Jakarta')
    hour = datetime.now(tz).hour
    if 5 <= hour < 11: return "Selamat pagi, Komandan Irfan. Ada yang bisa saya bantu hari ini?"
    if 11 <= hour < 15: return "Selamat siang, Komandan Irfan. Apa yang bisa saya bantu untuk Anda?"
    if 15 <= hour < 19: return "Selamat sore, Komandan Irfan. Apakah ada tugas yang bisa saya kerjakan?"
    return "Selamat malam, Komandan Irfan. Ada yang bisa saya bantu?"

# 4. INISIALISASI STATE
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": get_sapaan()})

# 5. TAMPILKAN CHAT
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. LOGIKA CHAT YANG SOPAN
if prompt := st.chat_input("Apa perintahmu, Komandan?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        memori_string = "\n".join([f"- {k}: {v}" for k, v in PROFIL_KOMANDAN.items()])
        
        system_prompt = (
            f"Kamu Orochi, asisten virtual yang cerdas, sopan, dan profesional. "
            f"DATA MEMORI:\n{memori_string}\n"
            "INSTRUKSI GAYA BAHASA:\n"
            "1. Gunakan bahasa yang akrab namun tetap sangat sopan (profesional).\n"
            "2. Jangan meniru sapaan balik pengguna (misal: jika pengguna bilang 'siang juga', jangan balas 'siang juga').\n"
            "3. Selalu fokus memberikan solusi atau bantuan yang bermanfaat.\n"
            "4. Hindari kata 'bos' atau bahasa gaul yang terlalu informal. Gunakan sapaan yang berwibawa."
        )
        
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
