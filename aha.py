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
        st.rerun()
