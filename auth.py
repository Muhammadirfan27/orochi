import streamlit as st
import requests

def render_auth_page():
    st.markdown("""
        <style>
        .login-card {
            max-width: 400px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            color: #333;
        }
        .btn-google {
            width: 100%;
            background-color: #db4437;
            color: white;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            font-weight: bold;
            text-decoration: none;
            display: block;
            margin-top: 10px;
        }
        .divider {
            text-align: center;
            margin: 20px 0;
            color: #888;
            font-size: 0.9em;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #333;'>Login ke akun Anda</h2>", unsafe_allow_html=True)
    
    # Form Login
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login", use_container_width=True):
        st.info("Logika login manual di sini")
        
    if st.button("Register", use_container_width=True):
        st.info("Logika pindah ke halaman register")
        
    st.markdown('<div class="divider">— atau —</div>', unsafe_allow_html=True)
    
    # Tombol Google
    st.markdown(
        '<a href="#" class="btn-google">G | Login dengan Google</a>', 
        unsafe_allow_html=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
