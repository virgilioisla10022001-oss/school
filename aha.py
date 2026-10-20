import streamlit as st
from database import init_db, register_user, verify_user

st.set_page_config(
    page_title="Dela Cruz Store Inventory Management System",
    page_icon="🛒",
    layout="wide"
)

# I-initialize ang database habang naglo-load ang app
init_db()

# Custom CSS para sa fix ng input background at styling
st.markdown("""
    <style>
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    .stDeployButton {display:none !important;}
    div[data-testid="stDecoration"] {display:none !important;}
    div[data-testid="stHeader"] {display:none !important;}
    div[data-testid="stToolbar"] {display:none !important;}
    
    .block-container {
        padding-top: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }

    .stApp {
        background: linear-gradient(135deg, #0056b3 0%, #0080ff 50%, #1a8cff 100%);
        color: white;
    }

    .field-label {
        color: white;
        font-weight: bold;
        font-size: 14px;
        text-align: right;
        padding-top: 8px;
    }

    input[type="text"], input[type="password"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 4px !important;
    }
    
    div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border-radius: 4px !important;
    }

    div.stButton > button {
        background-color: #1a6fb3 !important;
        color: white !important;
        border: 1px solid #ffffff !important;
        border-radius: 4px !important;
        font-weight: bold !important;
        padding: 4px 10px !important;
        width: 100%;
    }
    
    div.stButton > button:hover {
        background-color: #004080 !important;
        border-color: #ffffff !important;
    }

    div[data-testid="stCheckbox"] label span {
        color: white !important;
        font-size: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Title Section
col_icon, col_title = st.columns([0.6, 11.4])
with col_icon:
    st.markdown("<h1 style='margin:0; padding:0;'>🛒</h1>", unsafe_allow_html=True)
with col_title:
    st.markdown("<h1 style='color: white; font-size: 24px; font-weight: bold; margin:0; padding-top: 5px;'>DELA CRUZ STORE INVENTORY MANAGEMENT SYSTEM</h1>", unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.3); margin-top: 10px; margin-bottom: 30px;'>", unsafe_allow_html=True)

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
        _, center_col, _ = st.columns([1, 1.8, 1])
        with center_col:
            st.markdown("""
                <div style='text-align: center;'>
                    <h3 style='color: white; font-weight: bold; margin-bottom: 5px;'>CREATE ACCOUNT</h3>
                    <div style='font-size: 50px; line-height: 1; margin-bottom: 15px;'>📝</div>
                </div>
            """, unsafe_allow_html=True)

            reg_user = st.text_input("New Username", key="reg_user")
            reg_pass = st.text_input("New Password", type="password", key="reg_pass")
            reg_pass_conf = st.text_input("Confirm Password", type="password", key="reg_pass_conf")

            st.markdown("<br>", unsafe_allow_html=True)
            col_reg1, col_reg2 = st.columns(2)
            with col_reg1:
                if st.button("Register"):
                    if reg_user and reg_pass and reg_pass_conf:
                        if reg_pass == reg_pass_conf:
                            success = register_user(reg_user, reg_pass)
                            if success:
                                st.success("Account created successfully! Please login.")
                                st.session_state.page = "login"
                                st.rerun()
                            else:
                                st.error("Username already exists. Choose another.")
                        else:
                            st.warning("Passwords do not match!")
                    else:
                        st.warning("Please fill in all fields.")
            with col_reg2:
                if st.button("Back to Login"):
                    st.session_state.page = "login"
                    st.rerun()

    # 2. LOGIN PAGE
    else:
        _, center_col, _ = st.columns([1, 1.8, 1])
        with center_col:
            # --- PAGLALAGAY NG LOGO SA TAAS NG LOGIN ---
            try:
                # Siguraduhing pangalan ng logo file mo ay 'logo.png' at naka-upload sa GitHub
                st.image("ge.png", width=150, use_column_width=False)
            except:
                # Fallback icon kung sakaling hindi pa na-upload ang logo file
                st.markdown("<div style='text-align: center; font-size: 55px; margin-bottom: 15px;'>👤</div>", unsafe_allow_html=True)

            st.markdown("""
                <div style='text-align: center;'>
                    <h3 style='color: white; font-weight: bold; margin-bottom: 15px;'>USER LOGIN</h3>
                </div>
            """, unsafe_allow_html=True)

            row1_col1, row1_col2, row1_col3 = st.columns([1.2, 2.2, 1])
            with row1_col1:
                st.markdown("<p class='field-label'>Username</p>", unsafe_allow_html=True)
            with row1_col2:
                username_input = st.text_input("Username", label_visibility="collapsed", key="user_in")

            row2_col1, row2_col2, row2_col3 = st.columns([1.2, 2.2, 1])
            with row2_col1:
                st.markdown("<p class='field-label'>Password</p>", unsafe_allow_html=True)
            with row2_col2:
                show_pwd = st.session_state.get("show_pwd_check", False)
                pwd_type = "default" if show_pwd else "password"
                password_input = st.text_input("Password", type=pwd_type, label_visibility="collapsed", key="pass_in")
                st.checkbox("Show Password", key="show_pwd_check")

            with row1_col3:
                st.markdown("<div style='padding-top: 2px;'></div>", unsafe_allow_html=True)
                login_submitted = st.button("LOGIN", key="login_btn")

            if login_submitted:
                if username_input and password_input:
                    if verify_user(username_input, password_input):
                        st.session_state.logged_in = True
                        st.session_state.username = username_input
                        st.rerun()
                    else:
                        st.error("Invalid username or password!")
                else:
                    st.warning("Please enter both username and password!")

            st.markdown("<br>", unsafe_allow_html=True)

            bot_col1, _, bot_col2 = st.columns([1.5, 0.5, 1.5])
            with bot_col1:
                if st.button("Create Account"):
                    st.session_state.page = "register"
                    st.rerun()
            with bot_col2:
                if st.button("Forgot Password"):
                    st.info("Forgot Password feature coming soon!")

else:
    # --- DASHBOARD / LOGGED IN VIEW ---
    st.markdown(f"<h2 style='text-align: center; color: white;'>Welcome, {st.session_state.username}! 🎉</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #e6f2ff;'>Dito mo ilalagay ang Inventory Dashboard (Add Products, Stocks, Sales, etc.)</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("LOGOUT", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
