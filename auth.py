import streamlit as st
import requests

# Masukkan URL Google Apps Script Anda di sini
SHEET_URL = "URL_WEB_APP_ANDA_DISINI"

def register_user(username, email, password):
    try:
        res = requests.post(SHEET_URL, json={
            "action": "register", 
            "username": username, 
            "email": email, 
            "password": password
        })
        return res.status_code == 200
    except:
        return False

def check_login(username, password):
    try:
        res = requests.post(SHEET_URL, json={
            "action": "login", 
            "username": username, 
            "password": password
        })
        return res.json().get("status") == "success"
    except:
        return False

def render_auth_page():
    # CSS Modern untuk tampilan Card
    st.markdown("""
        <style>
        .auth-card {
            background-color: #1e1e2e;
            padding: 30px;
            border-radius: 15px;
            border: 1px solid #31333F;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            max-width: 400px;
            margin: auto;
        }
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            height: 3em;
            background-color: #ff4b4b;
            color: white;
            font-weight: bold;
            border: none;
        }
        .stButton>button:hover { background-color: #ff2b2b; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>🐍 Orochi AI Access</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Daftar"])
    
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
