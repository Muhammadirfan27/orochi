import streamlit as st
from datetime import datetime
import pytz

# 1. Konfigurasi Halaman & CSS Animasi
st.set_page_config(page_title="Orochi AI", page_icon="🐍")
st.markdown("""
    <style>
    /* Membuat gambar tampak halus saat berganti (efek animasi) */
    .stImage img {
        transition: opacity 0.5s ease-in-out;
        opacity: 1;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Inisialisasi State
if "orochi_awake" not in st.session_state: st.session_state.orochi_awake = False
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "menu" not in st.session_state: st.session_state.menu = None

# Fungsi untuk Update Gambar
def update_orochi_avatar(status):
    images = {
        "tidur": "Orochi_tidur.png",
        "diam": "Orochi_diam.png",
        "berfikir": "Orochi_berfikir.png",
        "bicara": "Orochi_bicara.png"
    }
    # Membersihkan placeholder dan menampilkan gambar baru
    placeholder.empty()
    placeholder.image(images.get(status, "Orochi_diam.png"), width=300)

# PROFIL
PROFIL_KOMANDAN = {
    "Nama": "Irfan",
    "Pekerjaan": "Admin Warehouse",
    "Pendidikan": "Mahasiswa Tingkat Akhir",
    "Alamat": "Jl. Swadaya III, Ciakar, Kec. Panongan, Kabupaten Tangerang, Banten 15710, Perum Golden Residence",
    "Keahlian": "Software Developer (PHP, IoT, MQTT)",
    "Hobi": "Esports (Inferno Demons), Anime Kekkaishi"
}

# 3. LOGIKA UI
placeholder = st.empty() 

if not st.session_state.orochi_awake:
    placeholder.image("Orochi_tidur.png", width=300)
    st.title("Orochi AI")
    if st.button("Bangunkan Orochi"):
        st.session_state.orochi_awake = True
        st.rerun()

elif not st.session_state.logged_in:
    placeholder.image("Orochi_diam.png", width=300)
    st.success("Selamat datang di Orochi! Silakan pilih menu:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"): st.session_state.menu = "login"
    with col2:
        if st.button("Daftar"): st.session_state.menu = "register"
    
    if st.session_state.menu == "login":
        st.text_input("Username:")
        if st.button("Konfirmasi Login"):
            st.session_state.logged_in = True
            st.rerun()

# 4. SISTEM CHAT
else:
    st.title("Orochi AI - Online")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Halo, Komandan Irfan. Ada yang bisa saya bantu hari ini?"}]
        placeholder.image("Orochi_diam.png", width=300)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Apa perintahmu?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Transisi ke Berfikir
        update_orochi_avatar("berfikir")
        
        with st.chat_message("assistant"):
            # Simulasi proses
            response = "Saya sedang memproses data Komandan Irfan mengenai permintaan Anda."
            
            # Transisi ke Bicara
            update_orochi_avatar("bicara")
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Kembali ke posisi diam
            update_orochi_avatar("diam")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.orochi_awake = False
        st.rerun()
