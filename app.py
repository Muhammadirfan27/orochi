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
    if 5 <= hour < 11: return "Selamat pagi, Komandan Irfan!"
    if 11 <= hour < 15: return "Selamat siang, Komandan Irfan!"
    if 15 <= hour < 19: return "Selamat sore, Komandan Irfan!"
    return "Selamat malam, Komandan Irfan!"

# 4. INISIALISASI STATE
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Menggunakan sapaan dinamis berdasarkan waktu
    welcome_msg = get_sapaan()
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# 5. TAMPILKAN CHAT
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. LOGIKA CHAT
if prompt := st.chat_input("Apa perintahmu, Komandan?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        memori_string = "\n".join([f"- {k}: {v}" for k, v in PROFIL_KOMANDAN.items()])
        
        system_prompt = (
            f"Kamu Orochi, asisten setia Komandan Irfan. "
            f"DATA MEMORI PERMANEN:\n{memori_string}\n"
            "Gaya bicara: santai, WA style, cerdas, setia. Wajib gunakan data di atas untuk menjawab."
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
