import streamlit as st
import pandas as pd
import datetime
from database import init_db, register_user, verify_user, add_product, get_all_products, update_product, delete_product

st.set_page_config(
    page_title="Dela Cruz Store Inventory Management System",
    page_icon="🛒",
    layout="wide"
)

# I-initialize ang database habang naglo-load ang app
init_db()

# Custom CSS: awit.png bilang background na may dark/soft overlay para malinaw ang teksto at hindi masakit sa mata
st.markdown("""
    <style>
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    .stDeployButton {display:none !important;}
    div[data-testid="stDecoration"] {display:none !important;}
    div[data-testid="stHeader"] {display:none !important;}
    div[data-testid="stToolbar"] {display:none !important;}
    
    /* Background Image setup na may overlay filter para hindi sobrang maliwanag */
    .stApp {
        background: linear-gradient(rgba(0, 30, 70, 0.75), rgba(0, 30, 70, 0.75)), url("awit.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
    }

    /* Wide layout pero centered container */
    .block-container {
        padding-top: 2rem !important;
        max-width: 900px !important;
        margin: auto !important;
    }

    /* Input Field Styling para malinaw ang basahin */
    input[type="text"], input[type="password"], input[type="number"], input[type="date"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 6px !important;
    }
    
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border-radius: 6px !important;
    }

    /* Button Styling */
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

    div[data-testid="stCheckbox"] label span {
        color: white !important;
        font-size: 13px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Title Center Aligned
st.markdown("<h1 style='text-align: center; color: white; font-size: 24px; font-weight: bold;'>🛒 DELA CRUZ SARI-SARI STORE MANAGEMENT SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.3); margin-top: 5px; margin-bottom: 25px;'>", unsafe_allow_html=True)

# Session States
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "login"
if "owner_verified" not in st.session_state:
    st.session_state.owner_verified = False

if not st.session_state.logged_in:
    
    _, col_center, _ = st.columns([1, 1.5, 1])
    with col_center:
        # 1. REGISTER PAGE
        if st.session_state.page == "register":
            st.markdown("<h3 style='text-align: center; color: white; font-weight: bold;'>CREATE ACCOUNT</h3>", unsafe_allow_html=True)
            st.markdown("<div style='text-align: center; font-size: 40px; margin-bottom: 15px;'>📝</div>", unsafe_allow_html=True)

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
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Back to Login", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()

        # 2. LOGIN PAGE
        else:
            try:
                col_img1, col_img2, col_img3 = st.columns([0.2, 0.6, 0.2])
                with col_img2:
                    st.image("ge.png", width=220)
            except:
                st.markdown("<div style='text-align: center; font-size: 60px; margin-bottom: 10px;'>🏠</div>", unsafe_allow_html=True)

            st.markdown("<h3 style='text-align: center; color: white; font-weight: bold;'>STORE LOGIN PORTAL</h3>", unsafe_allow_html=True)

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
                if st.button("Create Account", use_container_width=True):
                    st.session_state.page = "register"
                    st.rerun()
            with b2:
                if st.button("Forgot Password", use_container_width=True):
                    st.info("Please contact store owner.")

else:
    # --- DASHBOARD / LOGGED IN VIEW ---
    st.markdown(f"<h3 style='text-align: center; color: white;'>Maligayang Pagdating, {st.session_state.username}! 👋</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #d0e8ff; font-size: 14px;'>Sari-Sari Store Inventory & Expiry Management System</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)

    # Navigation Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📦 View Stocks", 
        "➕ Add Product", 
        "⚡ Restock / Bawas", 
        "⚠️ Expiry Alerts", 
        "⚙️ Owner & Manage"
    ])

    products = get_all_products()

    # 1. VIEW STOCKS TAB
    with tab1:
        st.subheader("Kasalukuyang Inventory ng Paninda")
        
        if products:
            df = pd.DataFrame(products, columns=["ID", "Product Name", "Category", "Quantity", "Price (₱)", "Date Added"])
            
            total_items = len(df)
            total_qty = df["Quantity"].sum()
            total_val = (df["Quantity"] * df["Price (₱)"]).sum()
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Uri ng Paninda", total_items)
            m2.metric("Kabuuang Stocks", f"{total_qty:,}")
            m3.metric("Halaga ng Inventory", f"₱{total_val:,.2f}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            search_query = st.text_input("🔍 Mag-search ng paninda o kategorya...", "")
            if search_query:
                df = df[df['Product Name'].str.contains(search_query, case=False, na=False) | 
                        df['Category'].str.contains(search_query, case=False, na=False)]
            
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Wala pang nakatalang paninda. Magdagdag sa 'Add Product' tab.")

    # 2. ADD PRODUCT TAB (May Expiration Date)
    with tab2:
        st.subheader("Magdagdag ng Bagong Paninda")
        
        categories = ["Beverages / Inumin", "Canned Goods", "Snacks / Chichirya", "Instant Noodles", "Personal Care / Sabon", "Household Items", "Iba pa"]
        
        with st.form("add_product_form", clear_on_submit=True):
            prod_name = st.text_input("Pangalan ng Paninda (e.g., Bear Brand 33g)")
            category_choice = st.selectbox("Kategorya", options=categories)
            category_custom = st.text_input("Kapag 'Iba pa', isulat ang kategorya rito:")
            
            category = category_custom if category_choice == "Iba pa" and category_custom else category_choice
            
            col_q, col_p = st.columns(2)
            with col_q:
                quantity = st.number_input("Bilang ng Stock (Quantity)", min_value=0, step=1)
            with col_p:
                price = st.number_input("Presyo bawat piraso (₱)", min_value=0.0, format="%.2f")
            
            expiry_date = st.date_input("Expiration Date", value=datetime.date.today() + datetime.timedelta(days=180))
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit_btn = st.form_submit_button("Save Product Record", use_container_width=True)
            
            if submit_btn:
                if prod_name:
                    if add_product(prod_name, category, quantity, price):
                        st.success(f"Matagumpay na naidagdag ang '{prod_name}' (Expiry: {expiry_date})!")
                        st.rerun()
                    else:
                        st.error("May nangyaring error sa pag-save ng produkto.")
                else:
                    st.warning("Pakalagyan ng pangalan ang produkto.")

    # 3. QUICK RESTOCK / BAWAS STOCKS TAB
    with tab3:
        st.subheader("⚡ Mabilisang Pag-dagdag o Pag-bawas ng Stocks")
        st.caption("Gamitin ito kapag may dumating na delivery o kaya'y nabawas/nabenta.")
        
        if products:
            product_dict = {f"{row[1]} (Stock: {row[3]})": row for row in products}
            selected_prod_label = st.selectbox("Pumili ng Paninda", options=list(product_dict.keys()), key="quick_restock_sel")
            
            selected_data = product_dict[selected_prod_label]
            prod_id, curr_name, curr_cat, curr_qty, curr_price, _ = selected_data
            
            with st.form("quick_restock_form"):
                st.write(f"**Paninda:** {curr_name} | **Kasalukuyang Stock:** {curr_qty}")
                
                action_type = st.radio("Aksyon:", ["Magdagdag ng Stock (Restock / Delivery)", "Bawasan ang Stock (Benta / Nabawas)"])
                adjustment_qty = st.number_input("Ilang piraso?", min_value=1, step=1, value=1)
                
                st.markdown("<br>", unsafe_allow_html=True)
                quick_submit = st.form_submit_button("I-update ang Stocks", use_container_width=True)
                
                if quick_submit:
                    if action_type == "Magdagdag ng Stock (Restock / Delivery)":
                        new_qty_val = curr_qty + adjustment_qty
                    else:
                        new_qty_val = max(0, curr_qty - adjustment_qty)
                    
                    if update_product(prod_id, curr_name, curr_cat, new_qty_val, curr_price):
                        st.success(f"Matagumpay na na-update ang stock ng '{curr_name}'! Bagong bilang: {new_qty_val}")
                        st.rerun()
                    else:
                        st.error("Nabigo sa pag-update ng stock.")
        else:
            st.info("Walang mga produktong maaring i-update.")

    # 4. EXPIRY ALERTS TAB
    with tab4:
        st.subheader("⚠️ Monitoring ng Expiration Dates")
        st.caption("Gabay para sa mga panindang malapit nang mapanis o ma-expire.")
        
        if products:
            df_expiry = pd.DataFrame(products, columns=["ID", "Product Name", "Category", "Quantity", "Price", "Date Added"])
            st.info("💡 **Paalala sa Tindahan:** Ugaliing ilagay sa unahan ng estante ang mga produktong mas maaga ang expiration date (First-In, First-Out).")
            st.dataframe(df_expiry[["Product Name", "Category", "Quantity", "Price"]], use_container_width=True, hide_index=True)
        else:
            st.info("Walang nakatalang paninda para i-monitor.")

    # 5. OWNER VERIFICATION & MANAGE/DELETE TAB
    with tab5:
        st.subheader("🔐 Owner Verification & Management")
        st.caption("Kailangan ang Owner PIN para makapag-update o magbura ng produkto.")
        
        OWNER_PIN = "1234"  # Default Owner PIN Code
        
        if not st.session_state.owner_verified:
            with st.form("owner_pin_form"):
                entered_pin = st.text_input("Ilagay ang Owner PIN Code", type="password")
                pin_submit = st.form_submit_button("I-verify ang PIN", use_container_width=True)
                
                if pin_submit:
                    if entered_pin == OWNER_PIN:
                        st.session_state.owner_verified = True
                        st.success("Matagumpay na na-verify ang Owner! Pwede nang mag-manage.")
                        st.rerun()
                    else:
                        st.error("Maling PIN code! Subukan muli.")
        else:
            st.success("✅ Authorized Owner Mode Active")
            if st.button("I-lock Muli (Logout Owner)", use_container_width=True):
                st.session_state.owner_verified = False
                st.rerun()
                
            st.markdown("---")
            if products:
                product_dict_m = {f"{row[1]} (ID: {row[0]} | Kat: {row[2]})": row for row in products}
                selected_prod_label_m = st.selectbox("Pumili ng Produkto na I-edit/I-delete", options=list(product_dict_m.keys()), key="manage_sel")
                
                selected_data_m = product_dict_m[selected_prod_label_m]
                prod_id_m, curr_name_m, curr_cat_m, curr_qty_m, curr_price_m, _ = selected_data_m
                
                with st.form("update_form"):
                    new_name = st.text_input("Product Name", value=curr_name_m)
                    new_cat = st.text_input("Category", value=curr_cat_m)
                    new_qty = st.number_input("Quantity", min_value=0, value=curr_qty_m, step=1)
                    new_price = st.number_input("Price (₱)", min_value=0.0, value=float(curr_price_m), format="%.2f")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    col_update, col_delete = st.columns(2)
                    with col_update:
                        update_btn = st.form_submit_button("Update Details", use_container_width=True)
                    with col_delete:
                        delete_btn = st.form_submit_button("Delete Product", use_container_width=True)
                    
                    if update_btn:
                        if update_product(prod_id_m, new_name, new_cat, new_qty, new_price):
                            st.success("Na-update na ang produkto!")
                            st.rerun()
                        else:
                            st.error("Hindi na-update ang produkto.")
                            
                    if delete_btn:
                        if delete_product(prod_id_m):
                            st.warning(f"Nabura na ang '{curr_name_m}' sa inventory.")
                            st.rerun()
                        else:
                            st.error("Hindi mabura ang produkto.")
            else:
                st.info("Walang mga produktong maaring i-manage.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("LOGOUT SYSTEM", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.page = "login"
        st.session_state.owner_verified = False
        st.rerun()
