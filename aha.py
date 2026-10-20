import streamlit as st
from database import init_db, register_user, verify_user

st.set_page_config(
    page_title="Dela Cruz Store Inventory Management System",
    page_icon="🛒",
    layout="wide"
)

# I-initialize ang database habang naglo-load ang app
init_db()

# Custom CSS para sa Modern Split-Screen Styling
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
        padding: 0rem !important;
        max-width: 100% !important;
    }

    .stApp {
        background-color: #ffffff;
    }

    /* Input Fields Styling */
    input[type="text"], input[type="password"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 6px !important;
        border: 1px solid #ced4da !important;
        padding: 10px !important;
    }
    
    div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border-radius: 6px !important;
    }

    /* Primary Login Button */
    div.stButton > button {
        background-color: #8b0000 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        padding: 8px 15px !important;
        width: 100%;
    }
    
    div.stButton > button:hover {
        background-color: #5c0000 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

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
        col_left, col_right = st.columns([1, 1], gap="medium")
        
        with col_left:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #fdfbfb 0%, #f4eae6 100%); padding: 6rem 3rem; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;'>
            """, unsafe_allow_html=True)
            try:
                st.image("ge.png", width=220)
            except:
                st.markdown("<h1>🛒</h1>", unsafe_allow_html=True)
            st.markdown("""
                    <h2 style='color: #2b2b2b; font-weight: bold; margin-top: 15px;'>DELA CRUZ STORE</h2>
                    <p style='color: #666; font-size: 14px; font-weight: bold;'>INVENTORY MANAGEMENT SYSTEM</p>
                </div>
            """, unsafe_allow_html=True)
            
        with col_right:
            st.markdown("<div style='padding: 6rem 4rem;'>", unsafe_allow_html=True)
            st.markdown("<h2 style='color: #2b2b2b; font-weight: bold;'>Create Account</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color: #666; font-size: 14px; margin-bottom: 2rem;'>Sign up to start managing your store inventory.</p>", unsafe_allow_html=True)
            
            reg_user = st.text_input("New Username", placeholder="Enter username", key="reg_u")
            reg_pass = st.text_input("New Password", type="password", placeholder="Enter password", key="reg_p")
            reg_pass_conf = st.text_input("Confirm Password", type="password", placeholder="Confirm password", key="reg_pc")
            
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
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
            with c2:
                if st.button("Back to Login", use_container_width=True):
                    st.session_state.page = "login"
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # 2. LOGIN PAGE (Split-Screen Modern Layout)
    else:
        col_left, col_right = st.columns([1, 1], gap="medium")
        
        # Left Side: Branding Panel
        with col_left:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #fdfbfb 0%, #f4eae6 100%); padding: 5rem 3rem; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;'>
            """, unsafe_allow_html=True)
            try:
                st.image("ge.png", width=230)
            except:
                st.markdown("<h1>🛒</h1>", unsafe_allow_html=True)
            st.markdown("""
                    <h2 style='color: #2b2b2b; font-weight: bold; margin-top: 15px;'>DELA CRUZ STORE</h2>
                    <p style='color: #666; font-size: 13px; letter-spacing: 2px; font-weight: bold;'>HOT • FRESH • RELIABLE</p>
                    <hr style='width: 40%; border: 1px solid #dcdcdc; margin: 15px auto;'>
                    <p style='color: #555; font-size: 14px; margin-top: 10px;'>Welcome to Dela Cruz Store!<br>Manage sales and inventory easily.</p>
                </div>
            """, unsafe_allow_html=True)
            
        # Right Side: Login Form Panel
        with col_right:
            st.markdown("<div style='padding: 6rem 4rem;'>", unsafe_allow_html=True)
            st.markdown("<h2 style='color: #2b2b2b; font-weight: bold;'>User Login</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color: #666; font-size: 14px; margin-bottom: 2rem;'>Please log in to access your dashboard.</p>", unsafe_allow_html=True)
            
            username_input = st.text_input("Username", placeholder="Enter username", key="user_in")
            password_input = st.text_input("Password", type="password", placeholder="Enter password", key="pass_in")
            
            # Forgot Password link area
            col_f1, col_f2 = st.columns([1, 1])
            with col_f2:
                if st.button("Forgot Password?", key="forgot_btn"):
                    st.info("Forgot Password feature coming soon!")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Login & Clear Buttons
            b_col1, b_col2 = st.columns(2)
            with b_col1:
                login_submitted = st.button("LOGIN", key="login_btn", use_container_width=True)
            with b_col2:
                clear_btn = st.button("CLEAR", key="clear_btn", use_container_width=True)
                if clear_btn:
                    st.rerun()

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

            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #666; font-size: 14px;'>Don't have an account?</p>", unsafe_allow_html=True)
            
            # Sign Up Button Link
            s_col1, s_col2, s_col3 = st.columns([1, 1.2, 1])
            with s_col2:
                if st.button("Sign Up", key="goto_reg", use_container_width=True):
                    st.session_state.page = "register"
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- DASHBOARD / LOGGED IN VIEW ---
    st.markdown(f"<h2 style='text-align: center; color: #333;'>Welcome, {st.session_state.username}! 🎉</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Dito mo ilalagay ang Inventory Dashboard (Add Products, Stocks, Sales, etc.)</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("LOGOUT", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
