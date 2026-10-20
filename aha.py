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

# Custom CSS
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
        padding-top: 1.5rem !important;
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

# --- LOGO AT HEADER SA GITNA ---
col_l1, col_l2, col_l3 = st.columns([1, 1, 1])
with col_l2:
    try:
        # Malaking Logo sa Gitna (180px width)
        st.image("ge.png", width=180)
    except:
        pass

st.markdown("<h1 style='text-align: center; color: white; font-size: 26px; font-weight: bold; margin-top: 10px;'>🛒 DELA CRUZ STORE INVENTORY MANAGEMENT SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.3); margin-top: 5px; margin-bottom: 25px;'>", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "login"

if not st.session_state.logged_in:
    _, col_center, _ = st.columns([1, 1.5, 1])
    with col_center:
        
        if st.session_state.page == "register":
            st.markdown("<h3 style='text-align: center; color: white;'>CREATE ACCOUNT</h3>", unsafe_allow_html=True)
            
            fullname = st.text_input("Full Name", placeholder="e.g., Juan Dela Cruz")
            reg_user = st.text_input("Username", placeholder="e.g., juandelacruz25")
            reg_pass = st.text_input("Password", type="password", placeholder="I-type ang iyong password")
            email = st.text_input("Email Address", placeholder="e.g., juandelacruz@gmail.com")
            birthday = st.date_input("Birthday", value=datetime.date(2000, 1, 1))
            contact = st.text_input("Contact Number", placeholder="e.g., 09123456789")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create Account", use_container_width=True):
                if not fullname:
                    st.warning("⚠️ Mangyaring ilagay ang iyong Full Name.")
                elif not reg_user:
                    st.warning("⚠️ Mangyaring ilagay ang iyong Username.")
                elif not reg_pass:
                    st.warning("⚠️ Mangyaring ilagay ang iyong Password.")
                elif not email or "@" not in email:
                    st.warning("⚠️ Maling Email Address! Siguraduhing mayroon itong '@' (hal. juandelacruz@gmail.com).")
                elif not contact or not contact.isdigit() or len(contact) != 11:
                    st.warning("⚠️ Maling Contact Number! Siguraduhing ito ay eksaktong 11 digits at nagsisimula sa 09.")
                else:
                    if register_user(fullname, reg_user, reg_pass, email, str(birthday), contact):
                        st.success("Account created successfully! Please login.")
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        st.error("⚠️ Ang Username na ito ay nagagamit na. Pumili ng iba.")
            
            if st.button("Back to Login", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()

        elif st.session_state.page == "forgot":
            st.markdown("<h3 style='text-align: center; color: white;'>FORGOT PASSWORD</h3>", unsafe_allow_html=True)
            st.caption("Enter your username and email address to reset password:")
            
            f_user = st.text_input("Username", placeholder="e.g., juandelacruz25")
            f_email = st.text_input("Email Address", placeholder="e.g., juandelacruz@gmail.com")
            new_pass = st.text_input("New Password", type="password", placeholder="I-type ang bagong password")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Verify Email and Reset Password", use_container_width=True):
                if f_user and f_email and new_pass:
                    if reset_password(f_user, f_email, new_pass):
                        st.success("Password reset successfully! You can now login.")
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        st.error("Username and Email do not match our records.")
                else:
                    st.warning("Please fill in all fields.")

            if st.button("Back to Login", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()

        else:
            st.markdown("<h3 style='text-align: center; color: white;'>USER LOGIN</h3>", unsafe_allow_html=True)
            
            username_input = st.text_input("Username", placeholder="I-type ang username")
            password_input = st.text_input("Password", type="password", placeholder="I-type ang password")
            st.checkbox("Show Password", key="show_pwd_check")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("LOGIN", use_container_width=True):
                if username_input and password_input:
                    user = verify_user(username_input, password_input)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.username = username_input
                        st.session_state.user_data = user
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
                    st.session_state.page = "forgot"
                    st.rerun()

else:
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c_head1, c_head2 = st.columns([3, 1])
    with c_head1:
        st.markdown(f"<h3 style='color: white;'>Dela Cruz Store Inventory Dashboard</h3>", unsafe_allow_html=True)
    with c_head2:
        st.markdown(f"<p style='text-align: right; color: #d0e8ff; font-size: 13px;'>{current_time}</p>", unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)

    tab_dash, tab_inv, tab_log, tab_rep, tab_admin, tab_about = st.tabs([
        "📊 Dashboard", 
        "📦 Inventory Management", 
        "📝 Log Retails", 
        "📈 Reports", 
        "⚙️ Admin Settings",
        "ℹ️ About System"
    ])

    products = get_all_products()
    
    with tab_dash:
        total_products = len(products)
        low_stock_count = sum(1 for p in products if 0 < p[4] <= 5)
        out_of_stock_count = sum(1 for p in products if p[4] == 0)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.info(f"**All Products**\n\nTotal Products: {total_products}")
        with m2:
            st.warning(f"**Low Stock Products**\n\nLow Stock: {low_stock_count}")
        with m3:
            st.error(f"**Out of Stock Products**\n\nOut of Stock: {out_of_stock_count}")

        st.markdown("### Latest Products")
        if products:
            df_latest = pd.DataFrame(products, columns=["ID", "Name", "Brand", "Category", "Quantity", "Price", "Expiry", "Date Added"])
            st.dataframe(df_latest[["Name", "Brand", "Quantity", "Date Added"]].tail(5), use_container_width=True, hide_index=True)
        else:
            st.info("No products recorded yet.")

    with tab_inv:
        st.subheader("Inventory Management & Product Records")
        
        col_form, col_table = st.columns([1, 1.5])
        
        with col_form:
            st.markdown("#### ➕ Add New Product")
            with st.form("inventory_form", clear_on_submit=True):
                p_name = st.text_input("Product Name", placeholder="e.g., Bear Brand 33g")
                p_brand = st.text_input("Brand Name", placeholder="e.g., Nestlé")
                p_qty = st.number_input("Quantity", min_value=0, step=1)
                categories = ["Beverages & Dairy", "Canned & Processed Goods", "Snacks, Chips, & Biscuits", "Instant & Ready-to-Eat", "Cigarettes", "Rice, Grains, & Cooking Ingredients", "Coffee", "Others"]
                p_cat = st.selectbox("Category", options=categories)
                p_price = st.number_input("Price (₱)", min_value=0.0, format="%.2f")
                p_expiry = st.date_input("Expiry Date", value=datetime.date.today() + datetime.timedelta(days=180))
                
                submitted = st.form_submit_button("Add Product", use_container_width=True)
                if submitted:
                    if p_name:
                        add_product(p_name, p_brand, p_cat, p_qty, p_price, str(p_expiry), str(datetime.date.today()))
                        st.success(f"Successfully added '{p_name}'!")
                        st.rerun()
                    else:
                        st.warning("Please enter a product name.")

            st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2); margin: 20px 0;'>", unsafe_allow_html=True)
            
            # --- DELETE PRODUCT SECTION ---
            st.markdown("#### 🗑️ Delete Product")
            if products:
                prod_delete_options = {f"ID: {p[0]} | {p[1]} ({p[2]})": p[0] for p in products}
                selected_del_label = st.radio("Pumili ng Produktong Buburahin", options=list(prod_delete_options.keys()))
                
                if st.button("Delete Selected Product", use_container_width=True):
                    del_id = prod_delete_options[selected_del_label]
                    delete_product(del_id)
                    st.success("Product deleted successfully!")
                    st.rerun()
            else:
                st.info("Walang produktong pwedeng i-delete.")

        with col_table:
            st.markdown("#### Product Records List")
            if products:
                df_inv = pd.DataFrame(products, columns=["ID", "Product Name", "Brand", "Category", "Quantity", "Price", "Expiry Date", "Date Added"])
                
                cat_filter = st.selectbox("Category Filter", ["All Categories"] + list(df_inv["Category"].unique()))
                if cat_filter != "All Categories":
                    df_inv = df_inv[df_inv["Category"] == cat_filter]
                
                st.dataframe(df_inv[["ID", "Product Name", "Brand", "Quantity", "Category", "Expiry Date"]], use_container_width=True, hide_index=True)
            else:
                st.info("No records found.")

    with tab_log:
        st.subheader("Dela Cruz Store Retail Log")
        st.caption("Record and monitor items sold to customers.")
        
        if products:
            prod_options = {p[1]: p for p in products}
            selected_item = st.selectbox("Product", options=list(prod_options.keys()))
            qty_sold = st.number_input("Quantity Sold", min_value=1, step=1)
            
            if st.button("Add Retail Log", use_container_width=True):
                item_info = prod_options[selected_item]
                item_id, name, brand, cat, current_qty, price, expiry, added = item_info
                
                if current_qty >= qty_sold:
                    new_qty = current_qty - qty_sold
                    update_product(item_id, name, brand, cat, new_qty, price, expiry)
                    add_retail_log(name, brand, qty_sold)
                    st.success(f"Recorded sale for {qty_sold} pc(s) of {name}!")
                    st.rerun()
                else:
                    st.error("Error: Insufficient stock available.")
            
            st.markdown("---")
            logs = get_retail_logs()
            if logs:
                df_logs = pd.DataFrame(logs, columns=["Log ID", "Product Name", "Brand", "Quantity Sold", "Date Time"])
                st.dataframe(df_logs, use_container_width=True, hide_index=True)
            else:
                st.info("No sales logs yet.")
        else:
            st.info("No products available to log.")

    with tab_rep:
        st.subheader("Dela Cruz Store Inventory Management Report")
        
        if st.button("Generate Weekly Report", use_container_width=True):
            st.success("Weekly Inventory Report successfully generated!")
            
        st.markdown("#### Past Reports:")
        report_data = [
            {"ID": "None", "Date": "2025-05-06", "File": "C:\\Users\\Downloads\\CDOES\\Nitrux\\rep1.txt"},
            {"ID": "None", "Date": "2025-05-06", "File": "C:\\Users\\Downloads\\CDOES\\Nitrux\\rep2.txt"},
            {"ID": "None", "Date": "2025-04-30", "File": "C:\\Users\\Downloads\\CDOES\\Nitrux\\rep3.txt"},
        ]
        df_reports = pd.DataFrame(report_data)
        st.dataframe(df_reports, use_container_width=True, hide_index=True)
        
        if st.button("Delete Selected Report"):
            st.info("Report deleted successfully.")

    with tab_admin:
        st.subheader("Admin Settings Dashboard")
        u_data = st.session_state.get("user_data", ["", "", "", "", "", "", ""])
        
        col_ad1, col_ad2 = st.columns(2)
        with col_ad1:
            st.markdown("### Admin Account Information")
            st.text_input("Full Name", value=u_data[1], disabled=True)
            st.text_input("Username", value=u_data[2], disabled=True)
            st.text_input("Email", value=u_data[4], disabled=True)
            st.text_input("Birthday", value=u_data[5], disabled=True)
            st.text_input("Contact Number", value=u_data[6], disabled=True)
            
        with col_ad2:
            st.markdown("### Manage Units of Measurement")
            unit_name = st.text_input("Unit Name:", placeholder="e.g., box")
            unit_qty = st.text_input("Quantity (pcs):", placeholder="e.g., 24")
            
            unit_box = st.text_area("Units List:", value="packs(cigarettes) - 20 pcs\npcs - 1 pcs\ncases(softdrinks) - 12 pcs", height=100)
            
            c_u1, c_u2 = st.columns(2)
            with c_u1:
                if st.button("Add Unit", use_container_width=True):
                    st.success("Unit added successfully!")
            with c_u2:
                if st.button("Delete Unit", use_container_width=True):
                    st.warning("Unit deleted.")

    with tab_about:
        st.subheader("About the System")
        st.markdown("""
        **Dela Cruz Store Inventory Management System**  
        
        This system is designed to support family-owned retail establishments in managing their product inventory, tracking retail logs, monitoring stock expiration levels, and generating automated inventory reports.  
        
        * **Core Modules:**
          * User Authentication & Account Recovery
          * Real-time Inventory & Stock Level Dashboard
          * Retail Sales Tracking & Logging
          * Units of Measurement Configuration
          * Automated Weekly Report Generation
        """)

    st.markdown("<br><hr>", unsafe_allow_html=True)
    if st.button("EXIT / LOGOUT SYSTEM", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.page = "login"
        st.rerun()
