import base64
import streamlit as st
from database import init_db, register_user, verify_user

st.set_page_config(
    page_title="Dela Cruz Store Inventory Management System",
    page_icon="🛒",
    layout="wide"
)

# I-initialize ang database habang naglo-load ang app
init_db()

# Custom CSS para sa full center alignment at styling
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
        padding-top: 1.5rem !important;
        max-width: 100% !important;
    }

    .stApp {
        background: linear-gradient(135deg, #0056b3 0%, #0080ff 50%, #1a8cff 100%);
        color: white;
    }

    input[type="text"], input[type="password"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 6px !important;
    }
    
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border-radius: 6px !important;
        color: #000000 !important;
    }

    div.stButton > button {
        background-color: #1a6fb3 !important;
        color: white !important;
        border: 1px solid #ffffff !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        padding: 8px 12px !important;
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

    .responsive-logo-max {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 100%;
        max-width: 450px;
        height: auto;
        object-fit: contain;
    }
    </style>
""", unsafe_allow_html=True)

# Header Title Center Aligned
st.markdown("<h1 style='text-align: center; color: white; font-size: 24px; font-weight: bold;'>🛒 DELA CRUZ STORE INVENTORY MANAGEMENT SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.3); margin-top: 10px; margin-bottom: 25px;'>", unsafe_allow_html=True)

# Session States
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "login"

if not st.session_state.logged_in:
    
    # 1. CREATE ACCOUNT PAGE
    if st.session_state.page == "register":
        _, center_col, _ = st.columns([1, 1.8, 1])
        with center_col:
            st.markdown("<h3 style='text-align: center; color: white; font-weight: bold; margin-bottom: 5px;'>CREATE ACCOUNT</h3>", unsafe_allow_html=True)
            st.markdown("<div style='text-align: center; font-size: 45px; margin-bottom: 15px;'>📝</div>", unsafe_allow_html=True)

            reg_user = st.text_input("New Username", key="reg_user")
            reg_pass = st.text_input("New Password", type="password", key="reg_pass")
            reg_pass_conf = st.text_input("Confirm Password", type="password", key="reg_pass_conf")
            
            # Role selection base sa Role table mo
            reg_role = st.selectbox("Account Role", ["Staff", "Admin"], key="reg_role")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Register Account", use_container_width=True):
                if reg_user and reg_pass and reg_pass_conf:
                    if reg_pass == reg_pass_conf:
                        if register_user(reg_user, reg_pass, reg_role):
                            st.success("Account created successfully! Please login.")
                            st.session_state.page = "login"
                            st.rerun()
                        else:
                            st.error("Username already exists. Please choose another.")
                    else:
                        st.warning("Passwords do not match!")
                else:
                    st.warning("Please fill in all fields.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Back to Login", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()

    # 2. LOGIN PAGE
    else:
        _, center_col, _ = st.columns([1, 1.8, 1])
        with center_col:
            try:
                def get_image_base64(path):
                    with open(path, "rb") as img_file:
                        return base64.b64encode(img_file.read()).decode()
                
                img_data = get_image_base64("ge.png")
                st.markdown(
                    f'<div style="text-align: center; margin-bottom: 15px;">'
                    f'<img src="data:image/png;base64,{img_data}" class="responsive-logo-max">'
                    f'</div>', 
                    unsafe_allow_html=True
                )
            except Exception:
                st.markdown("<div style='text-align: center; font-size: 80px; margin-bottom: 10px;'>👤</div>", unsafe_allow_html=True)

            st.markdown("<h3 style='text-align: center; color: white; font-weight: bold; margin-top: 5px; margin-bottom: 20px;'>USER LOGIN</h3>", unsafe_allow_html=True)

            username_input = st.text_input("Username", key="user_in")
            
            show_pwd = st.session_state.get("show_pwd_check", False)
            pwd_type = "default" if show_pwd else "password"
            password_input = st.text_input("Password", type=pwd_type, key="pass_in")
            st.checkbox("Show Password", key="show_pwd_check")

            st.markdown("<br>", unsafe_allow_html=True)
            
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

            st.markdown("<br>", unsafe_allow_html=True)

            b1, b2 = st.columns(2)
            with b1:
                if st.button("Create Account", use_container_width=True):
                    st.session_state.page = "register"
                    st.rerun()
            with b2:
                if st.button("Forgot Password", use_container_width=True):
                    st.info("Feature coming soon!")

else:
    # --- DASHBOARD / LOGGED IN VIEW ---
    st.sidebar.title(f"Hello, {st.session_state.username}!")
    menu = st.sidebar.radio("Navigation", ["Dashboard", "Products", "Categories", "Suppliers", "Orders", "Customers"])

    if menu == "Dashboard":
        st.markdown(f"<h2 style='color: white;'>Welcome to the Inventory Dashboard, {st.session_state.username}! 🎉</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #e6f2ff;'>Dito mo na ilalagay ang mga summary metrics tulad ng Total Products, Low Stock alerts, at Quick Actions base sa iyong ERD tables.</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Products", value="0", delta="0")
        with col2:
            st.metric(label="Total Categories", value="0", delta="0")
        with col3:
            st.metric(label="Total Suppliers", value="0", delta="0")

    elif menu == "Products":
        st.subheader("📦 Product Management")
        st.info("Dito mo isasama ang form para mag-add ng Product at Product table view.")

    elif menu == "Categories":
        st.subheader("📑 Category Management")
        st.info("Dito mo isasama ang pamamahala ng mga kategorya ng produkto.")

    elif menu == "Suppliers":
        st.subheader("🚚 Supplier Management")
        st.info("Dito mo isasama ang listahan at detalye ng mga suppliers.")

    elif menu == "Orders":
        st.subheader("🛒 Order Transactions")
        st.info("Dito mo isasama ang paggawa ng Orders at Order Details.")

    elif menu == "Customers":
        st.subheader("👥 Customer Management")
        st.info("Dito mo isasama ang listahan ng mga customers.")

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("LOGOUT", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
