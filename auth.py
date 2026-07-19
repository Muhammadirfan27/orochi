import streamlit as st
import requests

SHEET_URL = "URL_WEB_APP_ANDA_DISINI"

def register_user(username, email, password):
    try:
        res = requests.post(SHEET_URL, json={"action": "register", "username": username, "email": email, "password": password})
        return res.status_code == 200
    except: return False

def check_login(username, password):
    try:
        res = requests.post(SHEET_URL, json={"action": "login", "username": username, "password": password})
        return res.json().get("status") == "success"
    except: return False

def render_auth_page():
    # CSS Elegan dengan Efek Glassmorphism
    st.markdown("""
        <style>
        .main-container {
            max-width: 400px;
            margin: 50px auto;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            padding: 40px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            text-align: center;
        }
        h2 { color: #ffffff; margin-bottom: 20px !important; }
        .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 20px; }
        .stTabs [data-baseweb="tab"] { color: #888; font-weight: bold; }
        .stTabs [aria-selected="true"] { color: #ff4b4b !important; }
        .stButton>button {
            width: 100%;
            border-radius: 50px;
            height: 3em;
            background: linear-gradient(90deg, #ff4b4b, #ff7b7b);
            color: white;
            font-weight: bold;
            border: none;
            margin-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("<h2>🐍 Orochi AI</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Daftar"])
    
    with tab1:
        user_l = st.text_input("Username", key="u1")
        pass_l = st.text_input("Password", type="password", key="p1")
        if st.button("Masuk"):
            if check_login(user_l, pass_l):
                st.session_state.logged_in = True
                st.session_state.user_name = user_l
                st.rerun()
            else: st.error("Username atau Password salah!")
            
    with tab2:
        user_r = st.text_input("Username", key="u2")
        email_r = st.text_input("Gmail", key="e2")
        pass_r = st.text_input("Password", type="password", key="p2")
        if st.button("Daftar"):
            if register_user(user_r, email_r, pass_r):
                st.success("Akun berhasil! Silakan Login.")
            else: st.error("Gagal mendaftar.")
    
    st.markdown('</div>', unsafe_allow_html=True)
