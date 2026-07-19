import streamlit as st

def render_auth_page():
    # CSS untuk memaksa tampilan bersih dengan latar putih
    st.markdown("""
        <style>
        /* Paksa area utama menjadi putih agar mirip referensi */
        .block-container { background-color: #ffffff !important; padding: 2rem; border-radius: 10px; max-width: 400px; margin: auto; }
        
        /* Styling logo bulat */
        .logo-circle {
            width: 90px; height: 90px; background: #e67e22; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            margin: 0 auto 15px; color: white; font-size: 35px; font-weight: bold;
            border: 2px solid #ccc;
        }
        
        /* Tombol-tombol */
        div.stButton > button { width: 100%; border: none; padding: 10px; color: white; font-weight: bold; border-radius: 2px; }
        .btn-login { background-color: #2980b9 !important; }
        .btn-register { background-color: #bdc3c7 !important; }
        
        /* Pemisah 'atau' */
        .divider { text-align: center; margin: 20px 0; border-bottom: 1px solid #ddd; line-height: 0.1em; color: #777; }
        .divider span { background: #fff; padding: 0 10px; }
        
        /* Tombol Sosial */
        .soc-fb { background: #3b5998 !important; }
        .soc-go { background: #dd4b39 !important; }
        .soc-ya { background: #8e44ad !important; }
        </style>
    """, unsafe_allow_html=True)

    # Rendering elemen
    st.markdown('<div class="logo-circle">{J}</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; color:#333;">Login ke akun Anda</h2>', unsafe_allow_html=True)
    
    st.text_input("Email", placeholder="Email", key="email")
    st.text_input("Password", type="password", placeholder="Password", key="pass")
    
    col1, col2 = st.columns([1, 1])
    with col1: st.checkbox("Biarkan tetap masuk")
    with col2: st.markdown("[Lupa Password?](#)")
    
    # Tombol dengan class kustom
    st.markdown('<div class="btn-login">', unsafe_allow_html=True)
    if st.button("Login", key="btn1"): pass
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="btn-register">', unsafe_allow_html=True)
    if st.button("Register", key="btn2"): pass
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<p class="divider"><span>atau</span></p>', unsafe_allow_html=True)
    
    # Tombol Sosial
    st.markdown('<div class="soc-fb"><button class="stButton" style="width:100%; color:white; border:none; padding:10px;">f | Login dengan Facebook</button></div>', unsafe_allow_html=True)
    st.markdown('<div class="soc-go"><button class="stButton" style="width:100%; color:white; border:none; padding:10px;">G | Login dengan Google</button></div>', unsafe_allow_html=True)
    st.markdown('<div class="soc-ya"><button class="stButton" style="width:100%; color:white; border:none; padding:10px;">Y | Login dengan Yahoo</button></div>', unsafe_allow_html=True)
