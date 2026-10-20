import streamlit as st
from database import init_db, register_user, verify_user

st.set_page_config(
    page_title="Dela Cruz Store Inventory Management System",
    page_icon="🛒",
    layout="centered"
)

# I-initialize ang database habang naglo-load ang app
init_db()

# Custom CSS para sa nakafix at hindi gumagalaw/nagse-scroll na screen
st.markdown("""
    <style>
    /* Itago ang default Streamlit elements */
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    .stDeployButton {display:none !important;}
    div[data-testid="stDecoration"] {display:none !important;}
    div[data-testid="stHeader"] {display:none !important;}
    div[data-testid="stToolbar"] {display:none !important;}
    
    /* Lock ang buong screen at pigilan ang pag-scroll ng mouse */
    html, body, [data-testid="stAppViewContainer"], .main {
        overflow: hidden !important;
        height: 100vh !important;
        max-height: 100vh !important;
        position: fixed !important;
        width: 100% !important;
    }

    .block-container {
        padding-top: 0.8rem !important;
        padding-bottom: 0.8rem !important;
        max-width: 420px !important;
        width: 100% !important;
        margin: auto !important;
    }

    .stApp {
        background: linear-gradient(135deg, #0056b3 0%, #0080ff 50%, #1a8cff 100%);
        color: white;
    }

    /* Input styling para sakto sa screen */
    input[type="text"], input[type="password"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 6px !important;
        font-size: 13px !important;
        height: 35px !important;
    }
    
    div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border-radius: 6px !important;
    }

    /* Custom Button styling */
    div.stButton > button {
        background-color: #1a6fb3 !important;
        color: white !important;
        border: 1px solid #ffffff !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        padding: 5px 10px !important;
        width: 100%;
        font-size: 13px !important;
    }
    
    div.stButton > button:hover {
        background-color: #004080 !important;
        border-color: #ffffff !important;
    }

    div[data-testid="stCheckbox"] label span {
        color: white !important;
        font-size: 11px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Title Center Aligned
st.markdown("<h1 style='text-align: center; color: white; font-size: 16px; font-weight: bold; margin-bottom: 2px;'>🛒 DELA CRUZ STORE INVENTORY MANAGEMENT SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.3); margin-top: 2px; margin-bottom: 8px;'>", unsafe_allow_html=True)

# Session States
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "login"

if not st.session_state.logged_in:
    
    # 1. REGISTER PAGE
    if st.session_state.page == "register":
        st.markdown("<h3 style='text-align: center; color: white; font-size: 15px; font-weight: bold; margin-bottom: 2px;'>CREATE ACCOUNT</h3>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 30px; margin-bottom: 5px;'>📝</div>", unsafe_allow_html=True)

        reg_user = st.text_input("New Username", key="reg_user")
        reg_pass = st.text_input("New Password", type="password", key="reg_pass")
        reg_pass_conf = st.text_input("Confirm Password", type="password", key="reg_pass_conf")

        st.markdown("<div style='margin-top: 4px;'></div>", unsafe_allow_html=True)
        if st.button("Register", use_container_width=True):
            if reg_user and reg_pass and reg_pass_conf:
                if reg_pass == reg_pass_conf:
                    if register_user(reg_user, reg_pass):
                        st.success("Account created successfully! Please login.")
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        st.error("Username already exists.")
                else:
                    st.warning("Passwords do not match!")
            else:
                st.warning("Please fill in all fields.")
        
        if st.button("Back to Login", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

    # 2. LOGIN PAGE (Fixed & Locked)
    else:
        # LOGO DISPLAY
        try:
            col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
            with col2:
                st.image("ge.png", use_container_width=True)
        except:
            st.markdown("<div style='text-align: center; font-size: 45px; margin-bottom: 5px;'>👤</div>", unsafe_allow_html=True)

        st.markdown("<h3 style='text-align: center; color: white; font-size: 15px; font-weight: bold; margin-top: 2px; margin-bottom: 8px;'>USER LOGIN</h3>", unsafe_allow_html=True)

        username_input = st.text_input("Username", key="user_in")
        
        show_pwd = st.session_state.get("show_pwd_check", False)
        pwd_type = "default" if show_pwd else "password"
        password_input = st.text_input("Password", type=pwd_type, key="pass_in")
        st.checkbox("Show Password", key="show_pwd_check")

        st.markdown("<div style='margin-top: 4px;'></div>", unsafe_allow_html=True)
        
        if st.button("LOGIN", use_container_width=True, key="login_btn"):
            if username_input and password_input:
                if verify_user(username_input, password_input):
                    st.session_state.logged_in = True
                    st.session_state.username = username_input
                    st.rerun()
                else:
                    st.error("Invalid username or password!")
            else:
                st.warning("Please enter both username and password!")

        st.markdown("<div style='margin-top: 4px;'></div>", unsafe_allow_html=True)

        # Bottom Buttons
        b1, b2 = st.columns(2)
        with b1:
            if st.button("Create Account", use_container_width=True):
                st.session_state.page = "register"
                st.rerun()
        with b2:
            if st.button("Forgot Password", use_container_width=True):
                st.info("Coming soon!")

else:
    # --- DASHBOARD / LOGGED IN VIEW ---
    st.markdown(f"<h2 style='text-align: center; color: white;'>Welcome, {st.session_state.username}! 🎉</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #e6f2ff;'>Dito mo ilalagay ang Inventory Dashboard (Add Products, Stocks, Sales, etc.)</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("LOGOUT", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
