import streamlit as st
import os
from groq import Groq
from datetime import datetime
import pytz
import streamlit.components.v1 as components
import requests

# 1. Konfigurasi
st.set_page_config(page_title="Orochi AI", page_icon="🐍")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("Orochi AI")

# 2. Skrip JS untuk Koordinat
gps_js = """
<script>
async function getGPS() {
    navigator.geolocation.getCurrentPosition(
        (pos) => {
            const coords = {lat: pos.coords.latitude, lon: pos.coords.longitude};
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: coords}, '*');
        },
        (err) => console.log(err),
        {enableHighAccuracy: true, timeout: 10000}
    );
}
getGPS();
</script>
"""
components.html(gps_js, height=0)

# 3. Fungsi Mendapatkan Alamat Detail (Reverse Geocoding)
def get_address(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        response = requests.get(url, headers={'User-Agent': 'OrochiAI/1.0'})
        data = response.json()
        return data.get("display_name", "Alamat tidak ditemukan")
    except:
        return "Gagal mengambil detail alamat"

# 4. State Management
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_msg = "Hai Komandan! Sistem sudah aktif dan terhubung ke peta. Apa perintahmu?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Logika Chat
if prompt := st.chat_input("Apa perintahmu, Komandan?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Cek lokasi dari browser
    # Catatan: Di Streamlit, kita harus menangkap nilai dari components.html
    # Untuk versi sederhana ini, kita asumsi data koordinat masuk ke session
    
    with st.chat_message("assistant"):
        # Jika ada koordinat di session, ambil alamatnya
        alamat_detail = "Sedang dipetakan..."
        if "coords" in st.session_state and st.session_state.coords:
            lat = st.session_state.coords['lat']
            lon = st.session_state.coords['lon']
            alamat_detail = get_address(lat, lon)
        
        system_prompt = (
            f"Kamu Orochi, asisten Komandan Irfan. "
            f"ALAMAT LOKASI ANDA SEKARANG: {alamat_detail}. "
            "Gaya bicara: santai, WA style, sangat akurat, informatif."
        )
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )
        response = chat_completion.choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
