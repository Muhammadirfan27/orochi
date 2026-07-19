import streamlit as st
import requests

def render_auth_page():
    # CSS yang lebih rapi untuk menghindari konflik elemen
    st.markdown("""
        <style>
        .login-box {
            max-width: 400px;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            color: #333;
        }
        .header-text { text-align: center; color: #333; margin-bottom: 30px; font-weight: 600; }
        .stButton>button {
            width: 100%;
            border-radius: 6px;
            height: 2.5em;
            margin-bottom: 10px;
            font-weight: bold;
        }
        .btn-google {
            width: 100%;
            background-color: #db4437;
            color: white;
            padding: 10px;
            border-radius: 6px;
            text-align: center;
            font-weight: bold;
            display: block;
            text-decoration: none;
            margin-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Container utama agar form terpusat
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h2 class="header-text">Login ke akun Anda</h2>', unsafe_allow_html=True)
        
        # Input form dengan label yang jelas
        email = st.text_input("Email", placeholder="Masukkan email anda")
        password = st.text_input("Password", type="password", placeholder="Masukkan password")
        
        # Tombol utama
        if st.button("Login", type="primary", use_container_width=True):
            st.info("Logika login di sini")
        if st.button("Register", use_container_width=True):
            st.info("Logika register di sini")
            
        st.markdown('<p style="text-align:center; color:#888; margin: 20px 0;">— atau —</p>', unsafe_allow_html=True)
        
        # Tombol Google
        st.markdown('<a href="#" class="btn-google">G | Login dengan Google</a>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
