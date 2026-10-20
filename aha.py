import streamlit as st
import pandas as pd
from database import init_db, register_user, verify_user, add_product, get_all_products, update_product, delete_product

st.set_page_config(
    page_title="Dela Cruz Store Inventory Management System",
    page_icon="🛒",
    layout="centered"
)

# I-initialize ang database habang naglo-load ang app
init_db()

# Custom CSS para sa FIXED container size at alignment
st.markdown("""
    <style>
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    .stDeployButton {display:none !important;}
    div[data-testid="stDecoration"] {display:none !important;}
    div[data-testid="stHeader"] {display:none !important;}
    div[data-testid="stToolbar"] {display:none !important;}
    
    /* Lock layout width para hindi nag-a-adjust sa iba't ibang screen */
    .block-container {
        padding-top: 1.5rem !important;
        max-width: 500px !important;
        width: 500px !important;
        margin: auto !important;
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
    
    div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border-radius: 6px !important;
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
    </style>
""", unsafe_allow_html=True)

# Header Title Center Aligned
st.markdown("<h1 style='text-align: center; color: white; font-size: 20px; font-weight: bold;'>🛒 DELA CRUZ STORE INVENTORY MANAGEMENT SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.3); margin-top: 5px; margin-bottom: 20px;'>", unsafe_allow_html=True)

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
        st.markdown("<h3 style='text-align: center; color: white; font-weight: bold; margin-bottom: 5px;'>CREATE ACCOUNT</h3>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 45px; margin-bottom: 15px;'>📝</div>", unsafe_allow_html=True)

        reg_user = st.text_input("New Username", key="reg_user")
        reg_pass = st.text_input("New Password", type="password", key="reg_pass")
        reg_pass_conf = st.text_input("Confirm Password", type="password", key="reg_pass_conf")

        st.markdown("<br>", unsafe_allow_html=True)
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

    # 2. LOGIN PAGE
    else:
        try:
            col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
            with col2:
                st.image("ge.png", width=350)
        except:
            st.markdown("<div style='text-align: center; font-size: 70px; margin-bottom: 10px;'>👤</div>", unsafe_allow_html=True)

        st.markdown("<h3 style='text-align: center; color: white; font-weight: bold; margin-top: 10px; margin-bottom: 20px;'>USER LOGIN</h3>", unsafe_allow_html=True)

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
                st.info("Coming soon!")

else:
    # --- DASHBOARD / LOGGED IN VIEW ---
    st.markdown(f"<h2 style='text-align: center; color: white;'>Welcome, {st.session_state.username}! 🎉</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #e6f2ff;'>Dela Cruz Store Inventory Dashboard</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.3);'>", unsafe_allow_html=True)

    # Navigation Tabs para sa Inventory Management
    tab1, tab2, tab3 = st.tabs(["📦 View Stocks", "➕ Add Product", "⚙️ Manage Stocks"])

    # 1. VIEW STOCKS TAB
    with tab1:
        st.subheader("Current Inventory Stocks")
        products = get_all_products()
        
        if products:
            df = pd.DataFrame(products, columns=["ID", "Product Name", "Category", "Quantity", "Price (₱)", "Date Added"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Wala pang nakasabit na produkto sa inventory. Magdagdag sa 'Add Product' tab.")

    # 2. ADD PRODUCT TAB
    with tab2:
        st.subheader("Add New Product")
        with st.form("add_product_form"):
            prod_name = st.text_input("Product Name")
            category = st.text_input("Category (e.g., Canned Goods, Beverages, Snacks)")
            quantity = st.number_input("Quantity / Stocks", min_value=0, step=1)
            price = st.number_input("Price per Unit (₱)", min_value=0.0, format="%.2f")
            
            submit_btn = st.form_submit_button("Save Product")
            
            if submit_btn:
                if prod_name:
                    if add_product(prod_name, category, quantity, price):
                        st.success(f"Matagumpay na naidagdag ang '{prod_name}'!")
                        st.rerun()
                    else:
                        st.error("May nangyaring error sa pag-save ng produkto.")
                else:
                    st.warning("Pakalagyan ng pangalan ang produkto.")

    # 3. MANAGE STOCKS TAB (Update / Delete)
    with tab3:
        st.subheader("Update or Delete Product")
        products = get_all_products()
        
        if products:
            product_dict = {f"{row[1]} (ID: {row[0]})": row for row in products}
            selected_prod_label = st.selectbox("Pumili ng Produkto na I-update/I-delete", options=list(product_dict.keys()))
            
            selected_data = product_dict[selected_prod_label]
            prod_id, curr_name, curr_cat, curr_qty, curr_price, _ = selected_data
            
            with st.form("update_form"):
                new_name = st.text_input("Product Name", value=curr_name)
                new_cat = st.text_input("Category", value=curr_cat)
                new_qty = st.number_input("Quantity", min_value=0, value=curr_qty, step=1)
                new_price = st.number_input("Price (₱)", min_value=0.0, value=float(curr_price), format="%.2f")
                
                col_update, col_delete = st.columns(2)
                with col_update:
                    update_btn = st.form_submit_button("Update Product", use_container_width=True)
                with col_delete:
                    delete_btn = st.form_submit_button("Delete Product", use_container_width=True)
                
                if update_btn:
                    if update_product(prod_id, new_name, new_cat, new_qty, new_price):
                        st.success("Na-update na ang produkto!")
                        st.rerun()
                    else:
                        st.error("Hindi na-update ang produkto.")
                        
                if delete_btn:
                    if delete_product(prod_id):
                        st.warning(f"Nabura na ang '{curr_name}' sa inventory.")
                        st.rerun()
                    else:
                        st.error("Hindi mabura ang produkto.")
        else:
            st.info("Walang mga produktong maaring i-manage.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("LOGOUT", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.page = "login"
        st.rerun()
s
