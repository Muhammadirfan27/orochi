
import streamlit as st
import requests

SHEET_URL = "URL_WEB_APP_ANDA_DISINI"

def register_user(name, email):
    res = requests.post(SHEET_URL, json={"action": "register", "name": name, "email": email})
    return res.status_code == 200

def check_login(name, email):
    res = requests.post(SHEET_URL, json={"action": "login", "name": name, "email": email})
    return res.json().get("status") == "success"

def render_auth_page():
    st.title("🐍 Orochi AI Access")
    tab1, tab2 = st.tabs(["Login", "Daftar"])
    
    with tab1:
        name_l = st.text_input("Nama (Login):", key="n1")
        email_l = st.text_input("Email (Login):", key="e1")
        if st.button("Masuk"):
            if check_login(name_l, email_l):
                st.session_state.logged_in = True
                st.session_state.user_name = name_l
                st.rerun()
            else: st.error("Data tidak ditemukan!")
            
    with tab2:
        name_r = st.text_input("Nama (Daftar):", key="n2")
        email_r = st.text_input("Email (Daftar):", key="e2")
        if st.button("Daftar"):
            if register_user(name_r, email_r):
                st.success("Berhasil daftar! Silakan Login.")
            else: st.error("Gagal.")
