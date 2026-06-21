import streamlit as st
from groq import Groq
from datetime import datetime
import pytz

# Konfigurasi
st.set_page_config(page_title="Orochi AI", page_icon="🐍")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("Orochi AI")

# Profil
PROFIL_KOMANDAN = {
    "Nama": "Irfan",
    "Pekerjaan": "Admin Warehouse",
    "Pendidikan": "Mahasiswa Tingkat Akhir",
    "Alamat": "Jl. Swadaya III, Ciakar, Kec. Panongan, Kabupaten Tangerang, Banten 15710, Perum Golden Residence",
    "Keahlian": "Software Developer (PHP, IoT, MQTT)",
    "Hobi": "Esports (Inferno Demons), Anime Kekkaishi"
}

# Fungsi Sapaan Akurat
def get_sapaan():
    tz = pytz.timezone('Asia/Jakarta')
    hour = datetime.now(tz).hour
    if 5 <= hour < 11: return "Selamat pagi, Komandan Irfan. Ada yang bisa saya bantu?"
    if 11 <= hour < 15: return "Selamat siang, Komandan Irfan. Ada yang bisa saya bantu?"
    if 15 <= hour < 19: return "Selamat sore, Komandan Irfan. Ada yang bisa saya bantu?"
    return "Selamat malam, Komandan Irfan. Ada yang bisa saya bantu?"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": get_sapaan()}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Apa perintahmu, Komandan?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        memori_string = "\n".join([f"- {k}: {v}" for k, v in PROFIL_KOMANDAN.items()])
        
        # Instruksi SUPER KETAT
        system_prompt = (
            f"Kamu Orochi, asisten profesional Komandan Irfan. DATA MEMORI: {memori_string}. "
            "INSTRUKSI UTAMA: "
            "1. JANGAN PERNAH membalas sapaan pengguna dengan sapaan balik (misal: jika pengguna bilang 'siang', jangan balas 'siang juga'). "
            "2. Langsung tanyakan kebutuhan pengguna atau jawab pertanyaan mereka dengan sopan, akurat, dan berwibawa. "
            "3. Gunakan memori yang disediakan untuk data pribadi. "
            "4. Jangan gunakan kata sapaan pagi/siang/sore di dalam chat setelah sapaan pembuka."
        )
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )
        response = chat_completion.choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
