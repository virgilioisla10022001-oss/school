import streamlit as st
import pandas as pd
from database import init_db, register_user, verify_user, add_product, get_all_products, update_product, delete_product

st.set_page_config(
    page_title="Dela Cruz Store Inventory Management System",
    page_icon="🛒",
    layout="wide"
)

# I-initialize ang database habang naglo-load ang app
init_db()

# Custom CSS para sa Professional Styling
st.markdown("""
    <style>
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    .stDeployButton {display:none !important;}
    
    .stApp {
        background: linear-gradient(135deg, #f4f7f6 0%, #e9ecef 100%);
        color: #333333;
    }

    /* Professional Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0056b3 0%, #004080 100%);
        color: white;
    }
    
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }

    div.stButton > button {
        background-color: #0056b3 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        padding: 8px 12px !important;
        width: 100%;
    }
    
    div.stButton > button:hover {
        background-color: #004080 !important;
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

# --- NOT LOGGED IN VIEW (Login & Register Pages) ---
if not st.session_state.logged_in:
    
    # Center container for login/register using columns
    _, col_center, _ = st.columns([1, 1.2, 1])
    
    with col_center:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # 1. REGISTER PAGE
        if st.session_state.page == "register":
            st.markdown("<h2 style='text-align: center; color: #0056b3;'>📝 CREATE ACCOUNT</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray;'>Register a new system user</p>", unsafe_allow_html=True)

            reg_user = st.text_input("New Username", key="reg_user")
            reg_pass = st.text_input("New Password", type="password", key="reg_pass")
            reg_pass_conf = st.text_input("Confirm Password", type="password", key="reg_pass_conf")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Register Account", use_container_width=True):
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
                st.image("ge.png", width=120)
            except:
                st.markdown("<div style='text-align: center; font-size: 60px; margin-bottom: 10px;'>🛒</div>", unsafe_allow_html=True)

            st.markdown("<h3 style='text-align: center; color: #0056b3; font-weight: bold;'>DELA CRUZ STORE IMS</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray; font-size: 14px;'>Inventory Management System Portal</p>", unsafe_allow_html=True)

            username_input = st.text_input("Username", key="user_in")
            show_pwd = st.session_state.get("show_pwd_check", False)
            pwd_type = "default" if show_pwd else "password"
            password_input = st.text_input("Password", type=pwd_type, key="pass_in")
            st.checkbox("Show Password", key="show_pwd_check")

            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("SIGN IN", use_container_width=True, key="login_btn"):
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
                if st.button("Register", use_container_width=True):
                    st.session_state.page = "register"
                    st.rerun()
            with b2:
                if st.button("Forgot Password", use_container_width=True):
                    st.info("Please contact system admin.")

# --- DASHBOARD / LOGGED IN VIEW ---
else:
    # Sidebar Navigation & User Profile
    with st.sidebar:
        st.markdown(f"### 👤 Welcome, **{st.session_state.username}**!")
        st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
        
        st.markdown("#### 🧭 Navigation")
        selected_tab = st.radio(
            "Go to",
            ["📦 View Stocks", "➕ Add Product", "⚙️ Manage Stocks"],
            label_visibility="collapsed"
        )
        
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
        if st.button("🚪 LOGOUT", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.page = "login"
            st.rerun()

    # Main Header Banner
    st.markdown("<h1 style='color: #0056b3; font-size: 26px;'>🛒 Dela Cruz Store Inventory Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #dcdcdc; margin-top: 0px; margin-bottom: 20px;'>", unsafe_allow_html=True)

    products = get_all_products()

    # 1. VIEW STOCKS TAB
    if selected_tab == "📦 View Stocks":
        st.subheader("Current Inventory Stocks")
        
        # Summary Metrics Cards
        if products:
            df_metrics = pd.DataFrame(products, columns=["ID", "Product Name", "Category", "Quantity", "Price", "Date Added"])
            total_items = len(df_metrics)
            total_stock_qty = df_metrics["Quantity"].sum()
            total_inventory_value = (df_metrics["Quantity"] * df_metrics["Price"]).sum()
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Unique Products", total_items)
            m2.metric("Total Stock Quantity", f"{total_stock_qty:,}")
            m3.metric("Estimated Inventory Value", f"₱{total_inventory_value:,.2f}")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Search / Filter Feature
            search_query = st.text_input("🔍 Search Inventory Product...", "")
            if search_query:
                df_metrics = df_metrics[df_metrics['Product Name'].str.contains(search_query, case=False, na=False) | 
                                        df_metrics['Category'].str.contains(search_query, case=False, na=False)]
            
            st.dataframe(df_metrics, use_container_width=True, hide_index=True)
        else:
            st.info("Wala pang nakasabit na produkto sa inventory. Magdagdag sa 'Add Product' tab.")

    # 2. ADD PRODUCT TAB
    elif selected_tab == "➕ Add Product":
        st.subheader("Add New Product Entry")
        
        col_form, _ = st.columns([1.5, 1])
        with col_form:
            with st.form("add_product_form", clear_on_submit=True):
                prod_name = st.text_input("Product Name")
                category = st.text_input("Category (e.g., Canned Goods, Beverages, Snacks)")
                quantity = st.number_input("Quantity / Stocks", min_value=0, step=1)
                price = st.number_input("Price per Unit (₱)", min_value=0.0, format="%.2f")
                
                st.markdown("<br>", unsafe_allow_html=True)
                submit_btn = st.form_submit_button("Save Product Record")
                
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
    elif selected_tab == "⚙️ Manage Stocks":
        st.subheader("Update or Delete Product Record")
        
        if products:
            product_dict = {f"{row[1]} (ID: {row[0]} | Category: {row[2]})": row for row in products}
            selected_prod_label = st.selectbox("Pumili ng Produkto na I-update/I-delete", options=list(product_dict.keys()))
            
            selected_data = product_dict[selected_prod_label]
            prod_id, curr_name, curr_cat, curr_qty, curr_price, _ = selected_data
            
            col_manage, _ = st.columns([1.5, 1])
            with col_manage:
                with st.form("update_form"):
                    new_name = st.text_input("Product Name", value=curr_name)
                    new_cat = st.text_input("Category", value=curr_cat)
                    new_qty = st.number_input("Quantity", min_value=0, value=curr_qty, step=1)
                    new_price = st.number_input("Price (₱)", min_value=0.0, value=float(curr_price), format="%.2f")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    col_update, col_delete = st.columns(2)
                    with col_update:
                        update_btn = st.form_submit_button("Update Details", use_container_width=True)
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
