import streamlit as st
import time

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Orochi Virtual Pet", page_icon="🐍")
st.markdown("""
    <style>
    /* Transisi halus agar GIF tidak patah saat berganti */
    .stImage img { 
        transition: all 0.3s ease-in-out;
        border-radius: 20px;
    }
    div[data-testid="stImage"] {
        display: flex;
        justify-content: center;
        min-height: 350px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. INISIALISASI STATE ---
if "energy" not in st.session_state: st.session_state.energy = 50
if "orochi_awake" not in st.session_state: st.session_state.orochi_awake = False
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "status" not in st.session_state: st.session_state.status = "tidur"

PROFIL_KOMANDAN = {
    "Nama": "Irfan",
    "Pekerjaan": "Admin Warehouse",
    "Lokasi": "Panongan, Tangerang",
    "Keahlian": "Software Developer (PHP, IoT, MQTT)"
}

# Fungsi untuk memetakan status ke file GIF
def get_avatar(status):
    # Pastikan file-file ini ada dengan format .gif
    images = {
        "tidur": "Orochi_tidur.gif",
        "diam": "Orochi_diam.gif",
        "berfikir": "Orochi_berfikir.gif",
        "bicara": "Orochi_bicara.gif"
    }
    return images.get(status, "Orochi_diam.gif")

# --- 3. LOGIKA UI - HEADER & STATUS ---
st.title(f"Orochi AI - {PROFIL_KOMANDAN['Lokasi']}")

if st.session_state.orochi_awake:
    col_stat1, col_stat2 = st.columns(2)
    col_stat1.metric("Energi", f"{st.session_state.energy}%")
    col_stat2.write(f"Lokasi: {PROFIL_KOMANDAN['Lokasi']}")

# Menampilkan Avatar (GIF)
st.image(get_avatar(st.session_state.status), width=350)

# --- 4. LOGIKA INTERAKSI & CHAT (Game Loop) ---
if not st.session_state.orochi_awake:
    if st.button("Bangunkan Orochi"):
        st.session_state.orochi_awake = True
        st.session_state.status = "diam"
        st.rerun()

elif not st.session_state.logged_in:
    st.success("Sistem Online. Silakan Login:")
    if st.button("Login"):
        st.session_state.logged_in = True
        st.rerun()

else:
    # Mode Interaksi
    col1, col2, col3 = st.columns(3)
    if col1.button("Sentuh Orochi"):
        st.session_state.status = "diam"
        st.session_state.energy = min(100, st.session_state.energy + 10)
        st.toast("Orochi merasa senang!")
        st.rerun()
    if col2.button("Beri Perintah"):
        st.session_state.status = "berfikir"
        st.rerun()
    if col3.button("Tidurkan"):
        st.session_state.status = "tidur"
        st.rerun()

    # Chat Logic
    if st.session_state.status in ["berfikir", "bicara"]:
        prompt = st.text_input("Apa perintahmu?")
        if prompt:
            st.session_state.status = "bicara"
            response = f"Siap, Komandan {PROFIL_KOMANDAN['Nama']}. Sedang memproses: {prompt}"
            st.write(response)
            if st.button("Selesai"):
                st.session_state.status = "diam"
                st.rerun()
        
        # Auto-reset ke diam setelah 5 detik agar animasi tidak stuck
        time.sleep(5)
        st.session_state.status = "diam"
        st.rerun()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.orochi_awake = False
        st.session_state.status = "tidur"
        st.rerun()
