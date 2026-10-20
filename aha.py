import streamlit as st

st.set_page_config(
    page_title="Dela Cruz Store Inventory Management System",
    page_icon="🛒",
    layout="wide"
)

# Custom CSS para TULUYAN AT MABILIS na itago ang Streamlit Navigation / Header / Toolbar
st.markdown("""
    <style>
    /* Itago ang pangkalahatang Streamlit header, footer, at toolbar sa itaas */
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    .stDeployButton {display:none !important;}
    div[data-testid="stDecoration"] {display:none !important;}
    div[data-testid="stHeader"] {display:none !important;}
    div[data-testid="stToolbar"] {display:none !important;}
    
    /* Alisin ang spacing sa itaas */
    .block-container {
        padding-top: 1rem !important;
        max-width: 100% !important;
    }

    /* Gradient background */
    .stApp {
        background: linear-gradient(135deg, #0056b3 0%, #4da6ff 100%);
        color: white;
    }

    /* Login Form Box */
    .login-container {
        background-color: rgba(0, 0, 0, 0.15);
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Header Title
col_icon, col_title = st.columns([0.5, 11.5])
with col_icon:
    st.markdown("<h1>🛒</h1>", unsafe_allow_html=True)
with col_title:
    st.markdown("<h1 style='color: white; font-size: 26px; padding-top: 10px;'>DELA CRUZ STORE INVENTORY MANAGEMENT SYSTEM</h1>", unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    _, center_col, _ = st.columns([1, 1.3, 1])

    with center_col:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: white;'>👤 USER LOGIN</h3>", unsafe_allow_html=True)
        
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        
        if st.button("LOGIN", use_container_width=True):
            if username_input and password_input:
                st.session_state.logged_in = True
                st.session_state.username = username_input
                st.rerun()
            else:
                st.warning("Please enter both username and password!")

        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown(f"<h2 style='text-align: center;'>Welcome, {st.session_state.username}! 🎉</h2>", unsafe_allow_html=True)
    if st.button("LOGOUT"):
        st.session_state.logged_in = False
        st.rerun()
