import streamlit as st
import os
from groq import Groq
from datetime import datetime
import pytz

# 1. Konfigurasi
st.set_page_config(page_title="Orochi AI", page_icon="🐍")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("Orochi AI")

# 2. PROFIL KOMANDAN (MEMORI PERMANEN)
# Semua informasi penting tersimpan di sini
PROFIL_KOMANDAN = {
    "Nama": "Irfan",
    "Pekerjaan": "Admin Warehouse",
    "Pendidikan": "Mahasiswa Tingkat Akhir",
    "Alamat": "Jl. Swadaya III, Ciakar, Kec. Panongan, Kabupaten Tangerang, Banten 15710, Perum Golden Residence",
    "Keahlian": "Software Developer (PHP, IoT, MQTT)",
    "Hobi": "Esports (Inferno Demons), Anime Kekkaishi"
}

# 3. INISIALISASI STATE
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_msg = "Hai Komandan Irfan! Orochi sudah mengingat semua data Anda. Siap membantu hari ini?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# 4. TAMPILKAN HISTORY
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. LOGIKA CHAT DENGAN MEMORI
if prompt := st.chat_input("Apa perintahmu, Komandan?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        tz = pytz.timezone('Asia/Jakarta')
        now = datetime.now(tz)
        waktu = now.strftime("%A, %d %B %Y (Jam %H:%M WIB)")
        
        # Mengonstruksi konteks memori
        memori_string = "\n".join([f"- {k}: {v}" for k, v in PROFIL_KOMANDAN.items()])
        
        system_prompt = (
            f"Kamu adalah Orochi, asisten setia Komandan Irfan. "
            f"WAKTU SAAT INI: {waktu}. "
            f"DATA MEMORI PERMANEN KOMANDAN:\n{memori_string}\n"
            "INSTRUKSI:\n"
            "1. Selalu gunakan data di atas untuk menjawab setiap pertanyaan tentang identitas atau lokasi Komandan.\n"
            "2. Jangan pernah berhalusinasi atau menebak-nebak jika data sudah ada di atas.\n"
            "3. Gaya bicara: santai, WA style, cerdas, dan setia."
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
            st.error(f"Error: {e}")
