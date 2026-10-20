import base64
import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime
from database import init_db, register_user, verify_user, get_connection

st.set_page_config(
    page_title="Dela Cruz Store Inventory Management System",
    page_icon="🛒",
    layout="wide"
)

init_db()

# Custom CSS Styling
st.markdown("""
    <style>
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    .stApp {
        background: linear-gradient(135deg, #0056b3 0%, #0080ff 50%, #1a8cff 100%);
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
        color: #000000 !important;
    }
    div.stButton > button {
        background-color: #1a6fb3 !important;
        color: white !important;
        border: 1px solid #ffffff !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #004080 !important;
    }
    .responsive-logo-max {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 100%;
        max-width: 350px;
        height: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Header Title
st.markdown("<h1 style='text-align: center; color: white; font-size: 24px; font-weight: bold;'>🛒 DELA CRUZ SARI-SARI STORE INVENTORY MANAGEMENT SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 13px; color: #d0e1fd;'>1071 Brgy. Kaligayahan, Quirino Highway, Quezon City, Metro Manila[cite: 2]</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.3); margin-top: 5px; margin-bottom: 20px;'>", unsafe_allow_html=True)

# Session States
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "page" not in st.session_state:
    st.session_state.page = "login"

if not st.session_state.logged_in:
    
    # REGISTER PAGE
    if st.session_state.page == "register":
        _, center_col, _ = st.columns([1, 1.8, 1])
        with center_col:
            st.markdown("<h3 style='text-align: center; color: white;'>CREATE ACCOUNT</h3>", unsafe_allow_html=True)
            reg_name = st.text_input("Full Name", key="reg_name")
            reg_user = st.text_input("Username", key="reg_user")
            reg_pass = st.text_input("Password", type="password", key="reg_pass")
            reg_role = st.selectbox("Role", ["Staff", "Admin"], key="reg_role")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Register Account"):
                if reg_user and reg_pass:
                    if register_user(reg_user, reg_pass, reg_role, reg_name):
                        st.success("Account created successfully! Please login.")
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        st.error("Username already taken.")
                else:
                    st.warning("Please fill in required fields.")

            if st.button("Back to Login"):
                st.session_state.page = "login"
                st.rerun()

    # LOGIN PAGE
    else:
        _, center_col, _ = st.columns([1, 1.8, 1])
        with center_col:
            try:
                with open("ge.png", "rb") as f:
                    img_data = base64.b64encode(f.read()).decode()
                st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{img_data}" class="responsive-logo-max"></div>', unsafe_allow_html=True)
            except Exception:
                st.markdown("<div style='text-align: center; font-size: 70px;'>👤</div>", unsafe_allow_html=True)

            st.markdown("<h3 style='text-align: center; color: white;'>USER LOGIN</h3>", unsafe_allow_html=True)
            username_input = st.text_input("Username", key="user_in")
            password_input = st.text_input("Password", type="password", key="pass_in")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("LOGIN"):
                if username_input and password_input:
                    user = verify_user(username_input, password_input)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_info = dict(user)
                        st.rerun()
                    else:
                        st.error("Invalid username or password!")
                else:
                    st.warning("Please enter credentials.")

            b1, b2 = st.columns(2)
            with b1:
                if st.button("Create Account"):
                    st.session_state.page = "register"
                    st.rerun()
            with b2:
                if st.button("Forgot Password"):
                    st.info("Contact System Administrator.")

else:
    # DASHBOARD & MAIN NAVIGATION (System Flowchart Modules)[cite: 2]
    user = st.session_state.user_info
    st.sidebar.markdown(f"### 👤 Welcome, {user['name'] or user['username']}")
    st.sidebar.markdown(f"**Role:** `{user['role']}`")
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio("Navigation", [
        "📊 Dashboard", 
        "📦 Manage Products", 
        "🛒 Record Sales (POS)", 
        "📋 View Inventory & Alerts", 
        "📈 Generate Reports", 
        "👥 Manage Users", 
        "⚙️ Settings"
    ])

    conn = get_connection()

    if menu == "📊 Dashboard":
        st.subheader("📊 System Dashboard & Overview")
        
        total_p = pd.read_sql_query("SELECT COUNT(*) as c FROM Product", conn).iloc[0]['c']
        total_s = pd.read_sql_query("SELECT COUNT(*) as c FROM Sales", conn).iloc[0]['c']
        low_stock = pd.read_sql_query("SELECT COUNT(*) as c FROM Product WHERE quantity <= lowStockLevel", conn).iloc[0]['c']
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Products", total_p)
        c2.metric("Total Sales Transactions", total_s)
        c3.metric("Low Stock Alerts ⚠️", low_stock, delta_color="inverse")

        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 **System Note:** Centralizing product records, sales monitoring, and expiration tracking for the Dela Cruz Sari-Sari Store[cite: 2].")

    elif menu == "📦 Manage Products":
        st.subheader("📦 Product Management (Add / Update / Delete)")
        
        tab1, tab2 = st.tabs(["View Products", "Add New Product"])
        
        with tab1:
            df = pd.read_sql_query("""
                SELECT p.productID as 'ID', p.name as 'Product Name', c.name as 'Category', 
                       p.price as 'Price (₱)', p.quantity as 'Stock', p.lowStockLevel as 'Min Stock', 
                       p.expiryDate as 'Expiry Date', p.unit as 'Unit'
                FROM Product p
                LEFT JOIN Category c ON p.categoryID = c.categoryID
            """, conn)
            st.dataframe(df, use_container_width=True)

        with tab2:
            if user['role'] != 'Admin':
                st.warning("Only Admin accounts can add products.")
            else:
                with st.form("add_product_form"):
                    p_id = st.text_input("Product ID / Code (e.g., P-101)")
                    p_name = st.text_input("Product Name")
                    p_desc = st.text_input("Description")
                    
                    cat_df = pd.read_sql_query("SELECT * FROM Category", conn)
                    cat_choice = st.selectbox("Category", cat_df["name"].tolist()) if not cat_df.empty else None
                    
                    price = st.number_input("Price (₱)", min_value=0.0, value=15.0)
                    qty = st.number_input("Initial Quantity", min_value=0, value=50)
                    low_lvl = st.number_input("Low Stock Warning Level", min_value=1, value=10)
                    unit = st.selectbox("Unit", ["Piece", "Pack", "Sachet", "Bottle", "Can", "Kg"])
                    expiry = st.date_input("Expiration Date", value=datetime.today())

                    submitted = st.form_submit_button("Save Product")
                    if submitted and p_id and p_name:
                        cat_id = int(cat_df[cat_df["name"] == cat_choice]["categoryID"].values[0]) if cat_choice else None
                        try:
                            cur = conn.cursor()
                            cur.execute("""
                                INSERT INTO Product (productID, name, description, categoryID, price, quantity, expiryDate, lowStockLevel, unit)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (p_id, p_name, p_desc, cat_id, price, qty, expiry, low_lvl, unit))
                            conn.commit()
                            st.success(f"Product '{p_name}' successfully added!")
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.error("Product ID already exists!")

    elif menu == "🛒 Record Sales (POS)":
        st.subheader("🛒 Point of Sale & Sales Recording")
        
        products = pd.read_sql_query("SELECT productID, name, price, quantity FROM Product WHERE quantity > 0", conn)
        
        if products.empty:
            st.warning("No products available for sale.")
        else:
            selected_prod = st.selectbox("Select Product", products["name"].tolist())
            prod_row = products[products["name"] == selected_prod].iloc[0]
            
            st.write(f"**Available Stock:** {prod_row['quantity']} | **Price:** ₱{prod_row['price']:.2f}")
            sale_qty = st.number_input("Quantity to Sell", min_value=1, max_value=int(prod_row['quantity']), value=1)
            payment_method = st.selectbox("Payment Method", ["Cash", "GCash", "Credit"])

            if st.button("Confirm Sale & Deduct Stock"):
                total_amount = sale_qty * prod_row['price']
                cur = conn.cursor()
                
                # Insert Sale Record[cite: 2]
                cur.execute("INSERT INTO Sales (userID, totalAmount, paymentMethod) VALUES (?, ?, ?)",
                            (user['userID'], total_amount, payment_method))
                sale_id = cur.lastrowid
                
                # Insert Sale Item[cite: 2]
                cur.execute("INSERT INTO SaleItem (saleID, productID, quantity, price, subtotal) VALUES (?, ?, ?, ?, ?)",
                            (sale_id, prod_row['productID'], sale_qty, prod_row['price'], total_amount))
                
                # Update Stock Quantity[cite: 2]
                cur.execute("UPDATE Product SET quantity = quantity - ? WHERE productID = ?",
                            (sale_qty, prod_row['productID']))
                
                conn.commit()
                st.success(f"Sale recorded successfully! Total: ₱{total_amount:.2f}")
                st.rerun()

    elif menu == "📋 View Inventory & Alerts":
        st.subheader("📋 Inventory Monitoring & Expiry Checks")
        
        # Low Stock Alert query[cite: 2]
        st.markdown("### ⚠️ Low Stock Warnings")
        low_df = pd.read_sql_query("SELECT productID, name, quantity, lowStockLevel FROM Product WHERE quantity <= lowStockLevel", conn)
        if not low_df.empty:
            st.dataframe(low_df, use_container_width=True)
        else:
            st.success("All product stocks are at healthy levels!")

        st.markdown("### 📅 Expiration Date Monitoring")
        exp_df = pd.read_sql_query("SELECT productID, name, expiryDate, quantity FROM Product ORDER BY expiryDate ASC", conn)
        st.dataframe(exp_df, use_container_width=True)

    elif menu == "📈 Generate Reports":
        st.subheader("📈 Inventory & Sales Reports")
        
        rep_type = st.selectbox("Select Report Type", ["Sales Report", "Complete Inventory Report", "Low Stock Report"])
        
        if rep_type == "Sales Report":
            df_rep = pd.read_sql_query("""
                SELECT s.saleID as 'Sale ID', u.username as 'Staff', s.totalAmount as 'Total (₱)', 
                       s.paymentMethod as 'Payment', s.saleDate as 'Date'
                FROM Sales s
                LEFT JOIN User u ON s.userID = u.userID
            """, conn)
            st.dataframe(df_rep, use_container_width=True)
            
        elif rep_type == "Complete Inventory Report":
            df_rep = pd.read_sql_query("SELECT productID, name, price, quantity, expiryDate FROM Product", conn)
            st.dataframe(df_rep, use_container_width=True)
            
        elif rep_type == "Low Stock Report":
            df_rep = pd.read_sql_query("SELECT productID, name, quantity, lowStockLevel FROM Product WHERE quantity <= lowStockLevel", conn)
            st.dataframe(df_rep, use_container_width=True)

    elif menu == "👥 Manage Users":
        st.subheader("👥 User Account Management")
        if user['role'] != 'Admin':
            st.error("Restricted Access: Only Administrators can manage users.")
        else:
            df_users = pd.read_sql_query("SELECT userID, username, role, name, createdAt FROM User", conn)
            st.dataframe(df_users, use_container_width=True)

    elif menu == "⚙️ Settings":
        st.subheader("⚙️ Store Information Settings[cite: 2]")
        settings = pd.read_sql_query("SELECT * FROM Settings LIMIT 1", conn).iloc[0]
        
        with st.form("settings_form"):
            s_name = st.text_input("Store Name", value=settings['storeName'])
            s_addr = st.text_input("Store Address", value=settings['address'])
            s_contact = st.text_input("Contact Number", value=settings['contact'])
            
            if st.form_submit_button("Update Settings"):
                cur = conn.cursor()
                cur.execute("UPDATE Settings SET storeName = ?, address = ?, contact = ? WHERE id = ?",
                            (s_name, s_addr, s_contact, settings['id']))
                conn.commit()
                st.success("Store settings updated successfully!")
                st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.sidebar.button("LOGOUT", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_info = None
        st.rerun()

    conn.close()
