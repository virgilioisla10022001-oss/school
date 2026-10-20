import streamlit as st
import pandas as pd
import datetime
from database import init_db, register_user, verify_user, add_product, get_all_products, update_product, delete_product

st.set_page_config(
    page_title="Dela Cruz Sari-Sari Store Management",
    page_icon="🛒",
    layout="centered"
)

# I-initialize ang database habang naglo-load ang app
init_db()

# Custom CSS para sa Sari-Sari Store Clean Theme
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
        max-width: 750px !important;
        margin: auto !important;
    }

    .stApp {
        background: linear-gradient(135deg, #004b93 0%, #006dd1 50%, #1a8cff 100%);
        color: white;
    }

    input[type="text"], input[type="password"], input[type="number"], input[type="date"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 6px !important;
    }
    
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border-radius: 6px !important;
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

    div[data-testid="stCheckbox"] label span {
        color: white !important;
        font-size: 13px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Title Center Aligned
st.markdown("<h1 style='text-align: center; color: white; font-size: 22px; font-weight: bold;'>🛒 DELA CRUZ SARI-SARI STORE SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.3); margin-top: 5px; margin-bottom: 20px;'>", unsafe_allow_html=True)

# Session States
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "login"

if not st.session_state.logged_in:
    
    # REGISTER PAGE
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

    # LOGIN PAGE
    else:
        try:
            col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
            with col2:
                st.image("ge.png", width=250)
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

    # Tabs para sa iba't ibang features
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📦 View Stocks", 
        "➕ Add Product", 
        "📈 Dagdag / Bawas Stocks",
        "⚠️ Expiry Alerts", 
        "⚙️ Manage & Delete"
    ])

    products = get_all_products()

    # 1. VIEW STOCKS TAB
    with tab1:
        st.subheader("Kasalukuyang Inventory ng Paninda")
        
        if products:
            # Assuming columns: ID, Product Name, Category, Quantity, Price, Date Added, (optional Expiry)
            df = pd.DataFrame(products, columns=["ID", "Product Name", "Category", "Quantity", "Price (₱)", "Date Added"])
            
            # Overview Metrics
            total_items = len(df)
            total_qty = df["Quantity"].sum()
            total_val = (df["Quantity"] * df["Price (₱)"]).sum()
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Uri ng Paninda", total_items)
            m2.metric("Kabuuang Stocks", f"{total_qty:,}")
            m3.metric("Halaga (Capital/Value)", f"₱{total_val:,.2f}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Search Bar
            search_query = st.text_input("🔍 Mag-search ng paninda o kategorya...", "")
            if search_query:
                df = df[df['Product Name'].str.contains(search_query, case=False, na=False) | 
                        df['Category'].str.contains(search_query, case=False, na=False)]
            
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Wala pang nakatalang paninda. Magdagdag sa 'Add Product' tab.")

    # 2. ADD PRODUCT TAB (May kasamang Expiration Date)
    with tab2:
        st.subheader("Magdagdag ng Bagong Paninda")
        
        categories = ["Beverages / Inumin", "Canned Goods", "Snacks / Chichirya", "Instant Noodles", "Personal Care / Sabon", "Household Items", "Iba pa"]
        
        with st.form("add_product_form", clear_on_submit=True):
            prod_name = st.text_input("Pangalan ng Paninda (e.g., Century Tuna 155g)")
            category_choice = st.selectbox("Kategorya", options=categories)
            category_custom = st.text_input("Kapag 'Iba pa', isulat ang kategorya rito:")
            
            category = category_custom if category_choice == "Iba pa" and category_custom else category_choice
            
            col_q, col_p = st.columns(2)
            with col_q:
                quantity = st.number_input("Bilang ng Stock (Quantity)", min_value=0, step=1)
            with col_p:
                price = st.number_input("Presyo bawat piraso (₱)", min_value=0.0, format="%.2f")
            
            expiry_date = st.date_input("Expiration Date (Kung mayroon)", value=datetime.date.today() + datetime.timedelta(days=180))
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit_btn = st.form_submit_button("Save Product Record", use_container_width=True)
            
            if submit_btn:
                if prod_name:
                    # Maaari mong isama ang expiry_date sa pag-save kung susuportahan ng database function mo
                    if add_product(prod_name, category, quantity, price):
                        st.success(f"Matagumpay na naidagdag ang '{prod_name}'!")
                        st.rerun()
                    else:
                        st.error("May nangyaring error sa pag-save ng produkto.")
                else:
                    st.warning("Pakalagyan ng pangalan ang produkto.")

    # 3. DAGDAG / BAWAS STOCKS (QUICK RESTOCK / BENTA ADJUSTMENT)
    with tab3:
        st.subheader("⚡ Mabilisang Pag-dagdag o Pag-bawas ng Stocks")
        st.caption("Gamitin ito kapag may dumating na delivery o kapag may bultong binawas.")
        
        if products:
            product_dict = {f"{row[1]} (Kasalukuyang Stock: {row[3]})": row for row in products}
            selected_prod_label = st.selectbox("Pumili ng Paninda para i-Restock/Bawasan", options=list(product_dict.keys()), key="quick_stock_sel")
            
            selected_data = product_dict[selected_prod_label]
            prod_id, curr_name, curr_cat, curr_qty, curr_price, curr_date = selected_data
            
            with st.form("quick_restock_form"):
                st.write(f"**Paninda:** {curr_name} | **Kasalukuyang Stock:** {curr_qty}")
                
                action_type = st.radio("Piliin ang Aksyon:", ["Magdagdag ng Stock (Restock/Deliver)", "Bawasan ang Stock (Benta / Nabawas)"])
                adjustment_qty = st.number_input("Ilang piraso?", min_value=1, step=1, value=1)
                
                st.markdown("<br>", unsafe_allow_html=True)
                quick_submit = st.form_submit_button("I-update ang Stocks", use_container_width=True)
                
                if quick_submit:
                    if action_type == "Magdagdag ng Stock (Restock/Deliver)":
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
        st.caption("Paalala sa mga panindang malapit nang mapanis o ma-expire para maunang maibenta.")
        
        if products:
            # Gumawa ng simulang table para sa monitoring ng expiry
            df_expiry = pd.DataFrame(products, columns=["ID", "Product Name", "Category", "Quantity", "Price", "Date Added"])
            
            # Halimbawa ng pagpapakita ng status ng expiry
            st.info("💡 **Tip para sa Tindahan:** I-check ang mga de-lata, gatas, tinapay, at sitsirya kada linggo upang maiwasan ang pagka-expire sa estante.")
            
            # Pwedeng lagyan ng simulang badge o listahan
            st.dataframe(df_expiry[["Product Name", "Category", "Quantity", "Price"]], use_container_width=True, hide_index=True)
        else:
            st.info("Walang nakatalang paninda para i-monitor.")

    # 5. MANAGE & DELETE TAB
    with tab5:
        st.subheader("⚙️ Baguhin ang Detalye o Burahin ang Paninda")
        
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
        st.rerun()
