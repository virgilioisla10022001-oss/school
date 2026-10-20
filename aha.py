import streamlit as st
import pandas as pd
import datetime
from database import (
    init_db, register_user, verify_user, reset_password, 
    add_product, get_all_products, update_product, delete_product, 
    add_retail_log, get_retail_logs
)

st.set_page_config(
    page_title="Dela Cruz Store Inventory Management System",
    page_icon="🛒",
    layout="wide"
)

# Initialize Database
init_db()

# Custom CSS (inalis na ang background image, solid color/gradient na lang)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    
    .stApp {
        background: linear-gradient(rgba(0, 30, 70, 0.9), rgba(0, 30, 70, 0.9));
        color: white;
    }

    .block-container {
        padding-top: 2rem !important;
        max-width: 1000px !important;
        margin: auto !important;
    }

    div.stButton > button {
        background-color: #004080 !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.4) !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        padding: 8px 12px !important;
        width: 100%;
    }
    
    div.stButton > button:hover {
        background-color: #002b5c !important;
        border-color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGO AT HEADER ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    try:
        st.image("ge.png", width=90) # Dito lumilitaw ang logo mo
    except:
        st.write("Logo (ge.png)")

with col_title:
    st.markdown("<h1 style='color: white; font-size: 24px; font-weight: bold; margin-top: 15px;'>🛒 DELA CRUZ STORE INVENTORY MANAGEMENT SYSTEM</h1>", unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.3); margin-top: 5px; margin-bottom: 25px;'>", unsafe_allow_html=True)

# ... (ituloy ang natitirang code ng app.py simula sa st.session_state)
