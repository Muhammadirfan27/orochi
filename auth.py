import streamlit as st
import requests

SHEET_URL = "URL_WEB_APP_ANDA_DISINI"

def register_user(username, email, password):
    # Mengirim data pendaftaran ke Google Sheets
    res = requests.post(SHEET_URL, json={
        "action": "register", 
        "username": username, 
        "email": email, 
        "password": password
    })
    return res.status_code == 200

def check_login(username, password):
    # Mengecek username dan password
    res = requests.post(SHEET_URL, json={
        "action": "login", 
        "username": username, 
        "password": password
    })
    return res.json().get("status") == "success"

def render_auth_page():
    st.title("🐍 Orochi AI Access")
    tab1, tab2 = st.tabs(["Login", "Daftar"])
    
    with tab1:
        user_l = st.text_input("Username (Login):")
        pass_l = st.text_input("Password (Login):", type="password")
        if st.button("Masuk"):
            if check_login(user_l, pass_l):
                st.session_state.logged_in = True
                st.session_state.user_name = user_l
                st.rerun()
            else: st.error("Username atau Password salah!")
            
    with tab2:
        user_r = st.text_input("Username (Daftar):")
        email_r = st.text_input("Gmail (Daftar):")
        pass_r = st.text_input("Password (Daftar):", type="password")
        if st.button("Daftar"):
            if register_user(user_r, email_r, pass_r):
                st.success("Akun berhasil dibuat! Silakan pindah ke tab Login.")
            else: st.error("Gagal mendaftar.")
