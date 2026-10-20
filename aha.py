import streamlit as st

st.set_page_config(
    page_title="Dela Cruz Store Inventory System",
    page_icon="🛒",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0056b3 0%, #4da6ff 100%);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🛒 DELA CRUZ STORE INVENTORY MANAGEMENT SYSTEM</h1>", unsafe_allow_html=True)
st.write("---")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.subheader("👤 USER LOGIN")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("LOGIN", use_container_width=True):
            if username and password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.warning("Please enter both username and password!")
else:
    st.title(f"Welcome, {st.session_state.username}! 🎉")
    st.info("Naka-login ka na sa iyong Inventory Dashboard!")
    
    if st.button("LOGOUT"):
        st.session_state.logged_in = False
        st.rerun()import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Sizzling Sisig - User Login",
    page_icon="🍽️",
    layout="wide"
)

# Custom CSS para TULUYANNG MAWALA ang Streamlit Header, Footer, at Deploy/Share buttons
st.markdown("""
    <style>
    /* Itago ang Streamlit Header sa itaas */
    header {visibility: hidden;}
    
    /* Itago ang "Made with Streamlit" footer sa ibaba */
    footer {visibility: hidden;}
    
    /* Itago ang hamburger menu (tatlong guhit sa kanang taas) at share button */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Background color ng buong app */
    .stApp {
        background-color: #f7ebe8;
    }
    
    .login-card {
        background-color: white;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }
    .brand-section {
        background-color: #fcf1ef;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        height: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Session State para sa Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.2, 1.2], gap="large")

    with col_left:
        st.markdown("""
            <div class='brand-section'>
                <h1 style='color: #6b1d1f; font-family: sans-serif; font-weight: 800; letter-spacing: 2px;'>SIZZLING<br>SISIG</h1>
                <p style='color: #8c5859; font-weight: 600; letter-spacing: 3px; font-size: 12px;'>HOT • FRESH • DELICIOUS</p>
                <hr style='border: 1px solid #e0b8b5; width: 50%; margin: 20px auto;'>
                <p style='color: #555555; font-size: 14px;'>Welcome to Sizzling Sisig!<br>Manage sales and inventory easily.</p>
                <br>
                <p style='color: #6b1d1f; font-weight: bold; font-size: 13px; letter-spacing: 1px;'>PURE HEAT, PURE EAT</p>
            </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #5c181a; text-align: center; font-weight: bold;'>User Login</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #888888; text-align: center; font-size: 13px;'>Please log in to access your dashboard.</p>", unsafe_allow_html=True)
        
        username_input = st.text_input("Username", placeholder="Enter username")
        password_input = st.text_input("Password", type="password", placeholder="Enter password")
        
        st.markdown("<p style='text-align: right; font-size: 12px;'><a href='#' style='color: #8c3a3c; text-decoration: none;'>Forgot Password?</a></p>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            login_clicked = st.button("LOGIN", use_container_width=True)
        with c2:
            clear_clicked = st.button("CLEAR", use_container_width=True)
            
        if login_clicked:
            if username_input and password_input:
                st.session_state.logged_in = True
                st.session_state.username = username_input
                st.rerun()
            else:
                st.warning("Please enter username and password.")
                
        st.markdown("<p style='text-align: center; font-size: 13px; color: #666; margin-top: 20px;'>Don't have an account? <span style='color: #8c3a3c; font-weight: bold;'>Sign Up</span></p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.title(f"Welcome to Dashboard, {st.session_state.username}! 🎉")
    if st.button("LOGOUT"):
        st.session_state.logged_in = False
        st.rerun()
