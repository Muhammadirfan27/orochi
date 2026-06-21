import streamlit as st

# 1. Konfigurasi Halaman & CSS Animasi
st.set_page_config(page_title="Orochi Virtual Pet", page_icon="🐍")
st.markdown("""
    <style>
    /* Transisi halus agar gambar tidak patah-patah */
    .stImage img { 
        transition: opacity 0.5s ease-in-out; 
    }
    </style>
""", unsafe_allow_html=True)

# 2. Inisialisasi State
if "energy" not in st.session_state: st.session_state.energy = 50
if "orochi_awake" not in st.session_state: st.session_state.orochi_awake = False
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "status" not in st.session_state: st.session_state.status = "tidur"

# Data Profil, Lokasi, dan Memori
PROFIL_KOMANDAN = {
    "Nama": "Irfan",
    "Pekerjaan": "Admin Warehouse",
    "Lokasi": "Panongan, Tangerang",
    "Keahlian": "Software Developer (PHP, IoT, MQTT)"
}

# Fungsi untuk memetakan status ke file gambar
def get_avatar(status):
    images = {
        "tidur": "Orochi_tidur.png",
        "diam": "Orochi_diam.png",
        "berfikir": "Orochi_berfikir.png",
        "bicara": "Orochi_bicara.png"
    }
    return images.get(status, "Orochi_diam.png")

# 3. LOGIKA UI - Header & Status
st.title(f"Orochi AI - {PROFIL_KOMANDAN['Lokasi']}")

if st.session_state.orochi_awake:
    col_stat1, col_stat2 = st.columns(2)
    col_stat1.metric("Energi", f"{st.session_state.energy}%")
    col_stat2.write(f"Lokasi: {PROFIL_KOMANDAN['Lokasi']}")

# Menampilkan Avatar
placeholder = st.empty()
placeholder.image(get_avatar(st.session_state.status), width=300)

# 4. LOGIKA INTERAKSI & CHAT (Game Loop)
if not st.session_state.orochi_awake:
    if st.button("Bangunkan Orochi"):
        st.session_state.orochi_awake = True
        st.session_state.status = "diam"
        st.rerun()

elif not st.session_state.logged_in:
    st.success("Selamat datang, Komandan! Silakan Login:")
    if st.button("Login"):
        st.session_state.logged_in = True
        st.rerun()

else:
    # Mode Interaksi (Gameplay ala Pou)
    col1, col2, col3 = st.columns(3)
    if col1.button("Sentuh Orochi"):
        st.session_state.status = "diam"
        st.session_state.energy = min(100, st.session_state.energy + 10)
        st.rerun()
    if col2.button("Beri Perintah"):
        st.session_state.status = "berfikir"
        st.rerun()
    if col3.button("Tidurkan"):
        st.session_state.status = "tidur"
        st.rerun()

    # Chat Logic (saat sedang berfikir atau bicara)
    if st.session_state.status in ["berfikir", "bicara"]:
        prompt = st.text_input("Apa perintahmu?")
        if prompt:
            st.session_state.status = "bicara"
            response = f"Siap, Komandan {PROFIL_KOMANDAN['Nama']} di {PROFIL_KOMANDAN['Lokasi']}. Saya sedang memproses: {prompt}"
            st.write(response)
            if st.button("Selesai"):
                st.session_state.status = "diam"
                st.rerun()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.orochi_awake = False
        st.session_state.status = "tidur"
        st.rerun()
