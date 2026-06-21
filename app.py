import streamlit as st
import time
from groq import Groq
from datetime import datetime
import pytz

# Konfigurasi
st.set_page_config(page_title="Orochi AI", page_icon="🐍", layout="centered")

# Menggunakan API Key dari Streamlit Secrets (Pastikan sudah tersimpan di dashboard Streamlit Anda)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Profil Komandan
PROFIL_KOMANDAN = {
    "Nama": "Irfan",
    "Pekerjaan": "Admin Warehouse",
    "Pendidikan": "Mahasiswa Tingkat Akhir",
    "Keahlian": "Software Developer (PHP, IoT, MQTT)",
    "Hobi": "Esports (Inferno Demons), Anime Kekkaishi"
}

# --- LOGIKA SISTEM ---
def get_system_prompt():
    tz = pytz.timezone('Asia/Jakarta')
    waktu_skrg = datetime.now(tz).strftime("%A, %d %B %Y %H:%M")
    
    return f"""
    Kamu adalah Orochi, asisten AI pribadi yang sangat cerdas dan setia milik Komandan Irfan.
    Data Komandan: {PROFIL_KOMANDAN}.
    Waktu saat ini adalah: {waktu_skrg}.
    
    ATURAN SANGAT KETAT:
    1. Jawablah semua pertanyaan dengan sangat singkat, padat, dan akurat berdasarkan data profil di atas.
    2. JANGAN PERNAH mengarang cerita atau berhalusinasi tentang tugas/peristiwa yang tidak ada.
    3. Jika pengguna bertanya hal umum, jawab dengan profesional.
    4. Jika pengguna bertanya tentang data diri, gunakan data di atas.
    5. JANGAN PERNAH membalas sapaan dengan sapaan balik (misal: "Halo juga"). Langsung ke inti jawaban.
    6. Gunakan bahasa Indonesia yang berwibawa.
    """

# Inisialisasi Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilan Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Interaksi
if prompt := st.chat_input("Apa perintahmu, Komandan?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Orochi sedang berproses..."):
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.1-8b-instant",
                temperature=0.3 # Temperature rendah agar jawaban lebih fokus dan tidak ngawur
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
