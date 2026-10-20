import streamlit as st

st.set_page_config(
    page_title="Dela Cruz Store Inventory Management System",
    page_icon="🛒",
    layout="wide"
)

# Custom CSS para sa exact design matching
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
    
    .block-container {
        padding-top: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }

    /* Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0056b3 0%, #0080ff 50%, #1a8cff 100%);
        color: white;
    }

    /* Form Label Styling */
    .field-label {
        color: white;
        font-weight: bold;
        font-size: 14px;
        text-align: right;
        padding-top: 8px;
    }

    /* Modern Text Inputs */
    div[data-baseweb="input"] {
        border-radius: 4px !important;
        background-color: white !important;
    }
    div[data-baseweb="input"] input {
        color: black !important;
    }

    /* Custom Button Styling */
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

    /* Checkbox Styling */
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

# Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    # Center Column Layout
    _, center_col, _ = st.columns([1, 1.8, 1])

    with center_col:
        # User Icon & Login Header
        st.markdown("""
            <div style='text-align: center;'>
                <h3 style='color: white; font-weight: bold; margin-bottom: 5px;'>USER LOGIN</h3>
                <div style='font-size: 55px; line-height: 1; margin-bottom: 15px;'>👤</div>
            </div>
        """, unsafe_allow_html=True)

        # Login Form Layout (Label + Input + Login Button side-by-side)
        row1_col1, row1_col2, row1_col3 = st.columns([1.2, 2.2, 1])
        with row1_col1:
            st.markdown("<p class='field-label'>Username</p>", unsafe_allow_html=True)
        with row1_col2:
            username_input = st.text_input("Username", label_visibility="collapsed", key="user_in")

        row2_col1, row2_col2, row2_col3 = st.columns([1.2, 2.2, 1])
        with row2_col1:
            st.markdown("<p class='field-label'>Password</p>", unsafe_allow_html=True)
        with row2_col2:
            # Checkbox state para sa Show Password
            show_pwd = st.session_state.get("show_pwd_check", False)
            pwd_type = "default" if show_pwd else "password"
            password_input = st.text_input("Password", type=pwd_type, label_visibility="collapsed", key="pass_in")
            
            # Show password checkbox sa ilalim mismo ng password field
            st.checkbox("Show Password", key="show_pwd_check")

        with row1_col3:
            # Login Button katabi ng Username field
            st.markdown("<div style='padding-top: 2px;'></div>", unsafe_allow_html=True)
            login_submitted = st.button("LOGIN", key="login_btn")

        if login_submitted:
            if username_input and password_input:
                st.session_state.logged_in = True
                st.session_state.username = username_input
                st.rerun()
            else:
                st.error("Please enter both username and password!")

        st.markdown("<br>", unsafe_allow_html=True)

        # Bottom Buttons (Create Account & Forgot Password)
        bot_col1, _, bot_col2 = st.columns([1.5, 0.5, 1.5])
        with bot_col1:
            if st.button("Create Account"):
                st.info("Create Account feature clicked!")
        with bot_col2:
            if st.button("Forgot Password"):
                st.info("Forgot Password feature clicked!")

else:
    # Authenticated View
    st.markdown(f"<h2 style='text-align: center; color: white;'>Welcome, {st.session_state.username}! 🎉</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("LOGOUT", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
