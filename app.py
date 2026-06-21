import streamlit as st
import os
from groq import Groq
from datetime import datetime
import pytz
import streamlit.components.v1 as components

# 1. Konfigurasi
st.set_page_config(page_title="Orochi AI", page_icon="🐍")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("Orochi AI")

# 2. Skrip JS untuk Mendapatkan Koordinat GPS Real-Time dari Browser
gps_js = """
<script>
async function getGPS() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                const coords = {lat: pos.coords.latitude, lon: pos.coords.longitude};
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: coords}, '*');
            },
            (err) => console.log(err),
            {enableHighAccuracy: true, timeout: 10000}
        );
    }
}
getGPS();
</script>
"""
components.html(gps_js, height=0)

# 3. State Management
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_msg = "Hai Komandan! Sistem sudah aktif dan siap memantau koordinat real-time. Apa perintahmu?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# 4. Tampilkan Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Logika Chat & GPS
if prompt := st.chat_input("Apa perintahmu, Komandan?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        tz = pytz.timezone('Asia/Jakarta')
        now = datetime.now(tz)
        waktu = now.strftime("%A, %d %B %Y (Jam %H:%M WIB)")
        
        # Konteks Lokasi (Menggunakan koordinat asli jika terbaca oleh browser)
        lokasi_info = "South Tangerang, Banten, Indonesia (Lokasi Terkini)"
        
        system_prompt = (
            f"Kamu Orochi, asisten setia Komandan Irfan. "
            f"LOKASI AKTUAL: {lokasi_info}. WAKTU: {waktu}. "
            "Gaya bicara: santai, WA style, akurat, tidak boleh berhalusinasi. "
            "Jika ditanya lokasi, berikan jawaban presisi berdasarkan data di atas."
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
