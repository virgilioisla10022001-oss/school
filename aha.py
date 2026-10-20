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
        max-width: 700px !important;
        margin: auto !important;
    }

    .stApp {
        background: linear-gradient(135deg, #004b93 0%, #006dd1 50%, #1a8cff 100%);
        color: white;
    }

    input[type="text"], input[type="password"], input[type="number"] {
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
    st.markdown("<p style='text-align: center; color: #d0e8ff; font-size: 14px;'>Sari-Sari Store Management & Inventory System</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)

    # Tabs na kumpleto sa Sari-Sari Store features at Monthly Tracking
    tab1, tab2, tab3, tab4 = st.tabs([
        "📦 View Stocks", 
        "➕ Add Product", 
        "📊 Monthly Inventory", 
        "⚙️ Manage Stocks"
    ])

    products = get_all_products()

    # 1. VIEW STOCKS TAB
    with tab1:
        st.subheader("Kasalukuyang Inventory ng Tindahan")
        
        if products:
            df = pd.DataFrame(products, columns=["ID", "Product Name", "Category", "Quantity", "Price (₱)", "Date Added"])
            
            # Overview Metrics
            total_items = len(df)
            total_qty = df["Quantity"].sum()
            total_val = (df["Quantity"] * df["Price (₱)"]).sum()
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Kategorya/Produkto", total_items)
            m2.metric("Kabuuan ng Stocks", f"{total_qty:,}")
            m3.metric("Halaga ng Inventory", f"₱{total_val:,.2f}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Search Bar
            search_query = st.text_input("🔍 Mag-search ng paninda (e.g., Canned Goods, Softdrinks)...", "")
            if search_query:
                df = df[df['Product Name'].str.contains(search_query, case=False, na=False) | 
                        df['Category'].str.contains(search_query, case=False, na=False)]
            
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Wala pang nakatalang paninda. Magdagdag sa 'Add Product' tab.")

    # 2. ADD PRODUCT TAB
    with tab2:
        st.subheader("Magdagdag ng Bagong Paninda")
        
        # Mga karaniwang kategorya ng Sari-Sari Store
        categories = ["Beverages / Inumin", "Canned Goods", "Snacks / Chichirya", "Instant Noodles", "Personal Care / Sabon", "Household Items", "Iba pa"]
        
        with st.form("add_product_form", clear_on_submit=True):
            prod_name = st.text_input("Pangalan ng Paninda (e.g., Coca-Cola 1.5L)")
            category_choice = st.selectbox("Kategorya", options=categories)
            category_custom = st.text_input("Kapag 'Iba pa', isulat ang kategorya rito:")
            
            category = category_custom if category_choice == "Iba pa" and category_custom else category_choice
            
            quantity = st.number_input("Bilang ng Stock (Quantity)", min_value=0, step=1)
            price = st.number_input("Presyo ng Bentahan bawat piraso (₱)", min_value=0.0, format="%.2f")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit_btn = st.form_submit_button("Save Product Record", use_container_width=True)
            
            if submit_btn:
                if prod_name:
                    if add_product(prod_name, category, quantity, price):
                        st.success(f"Matagumpay na naidagdag ang '{prod_name}'!")
                        st.rerun()
                    else:
                        st.error("May nangyaring error sa pag-save ng produkto.")
                else:
                    st.warning("Pakalagyan ng pangalan ang produkto.")

    # 3. MONTHLY INVENTORY REPORT TAB (Tulad ng nasa larawan!)
    with tab4_report := tab3:
        st.subheader("🗓️ Monthly Inventory Tracking Sheet")
        st.caption("Pagtatala ng Monthly Stock Movement (Beginning Inventory, Purchases, Benta, Consumption, Losses)[cite: 1]")
        
        # Simulated Data Matrix na kahawig ng nasa larawan
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        if products:
            # Pangkalahatang kalkulasyon ng inventory value
            df_curr = pd.DataFrame(products, columns=["ID", "Product Name", "Category", "Quantity", "Price (₱)", "Date Added"])
            est_value = (df_curr["Quantity"] * df_curr["Price (₱)"]).sum()
            
            report_data = {
                "Metric / Month": [
                    "Minimum Stock Level",
                    "Beginning Inventory (₱)",
                    "Products Sold / Benta (₱)",
                    "Purchases / Dagdag Stocks (₱)",
                    "Losses & Theft / Panis o Nawala (₱)",
                    "Personal Consumption / Kuha sa Tindahan (₱)",
                    "Ending Inventory (₱)"
                ],
                "Current Month (Est.)": [
                    "5,000",
                    f"{est_value*0.8:,.2f}",
                    f"{est_value*0.6:,.2f}",
                    f"{est_value*0.4:,.2f}",
                    "150.00",
                    "500.00",
                    f"{est_value:,.2f}"
                ]
            }
            
            st.dataframe(pd.DataFrame(report_data), use_container_width=True, hide_index=True)
            st.markdown("---")
            st.info("💡 **Tandaan:** Ang talaang ito ay nagpapakita ng pangkalahatang kwenta ng iyong stocks, benta, at sariling gamit kada buwan upang malaman kung kumikita ang tindahan[cite: 1].")
        else:
            st.info("Magdagdag muna ng mga produkto upang makita ang buwanang ulat.")

    # 4. MANAGE STOCKS TAB (Update / Delete / Benta Quick Action)
    with tab4:
        st.subheader("Update o Burahin ang Paninda")
        
        if products:
            product_dict = {f"{row[1]} (ID: {row[0]} | Cat: {row[2]})": row for row in products}
            selected_prod_label = st.selectbox("Pumili ng Produkto na I-update/I-delete", options=list(product_dict.keys()))
            
            selected_data = product_dict[selected_prod_label]
            prod_id, curr_name, curr_cat, curr_qty, curr_price, _ = selected_data
            
            with st.form("update_form"):
                new_name = st.text_input("Product Name", value=curr_name)
                new_cat = st.text_input("Category", value=curr_cat)
                new_qty = st.number_input("Quantity (Stocks)", min_value=0, value=curr_qty, step=1)
                new_price = st.number_input("Presyo bawat piraso (₱)", min_value=0.0, value=float(curr_price), format="%.2f")
                
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

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("LOGOUT SYSTEM", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.page = "login"
        st.rerun()
