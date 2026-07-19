import streamlit as st

def render_auth_page():
    # CSS Khusus untuk meniru gaya referensi Anda
    st.markdown("""
        <style>
        .login-box {
            max-width: 350px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            color: #555;
            font-family: sans-serif;
        }
        .logo-circle {
            width: 80px; height: 80px; background: #f39c12; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            margin: 0 auto 15px; color: white; font-size: 30px; font-weight: bold;
            border: 3px solid #eee;
        }
        .btn-full { width: 100%; border: none; padding: 10px; color: white; margin-bottom: 5px; cursor: pointer; border-radius: 2px; }
        .btn-login { background-color: #2980b9; }
        .btn-register { background-color: #bdc3c7; }
        .divider { text-align: center; margin: 15px 0; border-bottom: 1px solid #ddd; line-height: 0.1em; color: #777; }
        .divider span { background: #fff; padding: 0 10px; }
        .social-btn { display: block; width: 100%; padding: 10px; color: white; text-decoration: none; margin-bottom: 5px; text-align: left; padding-left: 20px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="logo-circle">{J}</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; color:#555;">Login ke akun Anda</h2>', unsafe_allow_html=True)
    
    # Input field
    st.text_input("Email", placeholder="Email", key="email")
    st.text_input("Password", type="password", placeholder="Password", key="pass")
    
    col1, col2 = st.columns([1, 1])
    with col1: st.checkbox("Biarkan tetap masuk")
    with col2: st.markdown("[Lupa Password?](#)")
    
    # Tombol Utama
    if st.button("Login", type="primary", use_container_width=True): pass
    if st.button("Register", use_container_width=True): pass
    
    # Divider
    st.markdown('<p class="divider"><span>atau</span></p>', unsafe_allow_html=True)
    
    # Social Buttons
    st.markdown('<a href="#" class="social-btn" style="background:#3b5998;">f | Login dengan Facebook</a>', unsafe_allow_html=True)
    st.markdown('<a href="#" class="social-btn" style="background:#db4437;">G | Login dengan Google</a>', unsafe_allow_html=True)
    st.markdown('<a href="#" class="social-btn" style="background:#8e44ad;">Y | Login dengan Yahoo</a>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
