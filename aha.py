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
    .login-container {
        background-color: rgba(0, 0, 0, 0.15);
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

col_icon, col_title = st.columns([1, 12])
with col_icon:
    st.markdown("<h1>🛒</h1>", unsafe_allow_html=True)
with col_title:
    st.markdown("<h1 style='color: white; font-size: 24px; padding-top: 10px;'>DELA CRUZ STORE INVENTORY MANAGEMENT SYSTEM</h1>", unsafe_allow_html=True)

st.write("---")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    _, center_col, _ = st.columns([1, 1.2, 1])

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

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Create Account", use_container_width=True):
                st.info("Redirecting to Create Account...")
        with col_btn2:
            if st.button("Forgot Password", use_container_width=True):
                st.info("Redirecting to Password Recovery...")
                
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown(f"<h2 style='text-align: center;'>Welcome, {st.session_state.username}! 🎉</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #d0e1fd;'>Dela Cruz Store - Main Inventory Dashboard</h4>", unsafe_allow_html=True)
    
    st.write("")
    st.info("Dito mo na ilalagay ang mga inventory tables, stocks, at mga produkto mo.")

    if st.button("LOGOUT"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
