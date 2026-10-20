import base64
import sqlite3
import pandas as pd
import streamlit as st
from database import init_db, register_user, verify_user, get_connection

st.set_page_config(
    page_title="Dela Cruz Store Inventory Management System",
    page_icon="🛒",
    layout="wide"
)

# Initialize database tables and sample sari-sari store data
init_db()

def seed_sari_sari_store_data():
    """Naglalagay ng default Sari-Sari Store Categories, Suppliers, at Products kung walang laman."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Insert Default Categories
    cursor.execute("SELECT COUNT(*) FROM Category")
    if cursor.fetchone()[0] == 0:
        categories = [
            ("Inumin & Softdrinks", "Mga malamig na inumin, softdrinks, at juice"),
            ("Chichirya & Snacks", "Chippippy, biscuits, at tsokolate"),
            ("Canned Goods & Instant", "Sardinas, corned beef, at instant noodles"),
            ("Baking & Cooking Essentials", "Mantika, toyo, suka, asin, at asukal"),
            ("Toiletries & Household", "Sabon, shampoo, detergent, at tissue")
        ]
        cursor.executemany("INSERT INTO Category (Category_Name, Description) VALUES (?, ?)", categories)

    # 2. Insert Default Suppliers
    cursor.execute("SELECT COUNT(*) FROM Supplier")
    if cursor.fetchone()[0] == 0:
        suppliers = [
            ("San Miguel Food & Beverage", "Mandaluyong City", 1234567, 1234567, "smfb@supplier.ph", "Main Softdrinks Supplier"),
            ("Universal Robina Corp (URC)", "Pasig City", 2345678, 2345678, "urc@supplier.ph", "Snacks & Drinks Supplier"),
            ("Monde Nissin", "Santa Rosa, Laguna", 3456789, 3456789, "monde@supplier.ph", "Noodles & Biscuits"),
            ("Puregold Wholesale", "Quezon City", 4567890, 4567890, "puregold@supplier.ph", "General Merchandise Wholesale")
        ]
        cursor.executemany("""
            INSERT INTO Supplier (Name, Address, phone, fax, Email, other_details)
            VALUES (?, ?, ?, ?, ?, ?)
        """, suppliers)

    # 3. Insert Default Sari-Sari Store Products
    cursor.execute("SELECT COUNT(*) FROM Product")
    if cursor.fetchone()[0] == 0:
        products = [
            ("P-001", "Coke Mismo 290ml", "Malamig na Coke Mismo", "Bote", 15.0, 50, "Available", "Best seller", 1, 1),
            ("P-002", "Piattos Cheese Small", "Flavored Potato Chips", "Pack", 18.0, 30, "Available", "URC item", 2, 2),
            ("P-003", "Lucky Me Instant Pancit Canton Extra Hot", "Instant Noodles", "Pack", 15.0, 100, "Available", "Monde Nissin", 3, 3),
            ("P-004", "Mega Sardines Green 155g", "Easy open can sardines", "Can", 22.0, 40, "Available", "In Tomato Sauce", 4, 3),
            ("P-005", "Bear Brand Powdered Milk 33g", "Fortified Powdered Milk", "Sachet", 16.0, 60, "Available", "Single serve", 4, 1),
            ("P-006", "Surf Powder Sun Fresh 60g", "Detergent Powder", "Sachet", 8.0, 80, "Available", "Pang-laba", 4, 5)
        ]
        cursor.executemany("""
            INSERT INTO Product 
            (Product_ID, Product_Name, Product_description, Product_unit, Product_Price, Product_quantity, Product_Status, Other_Details, Supplier_ID, Category_ID)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, products)

    conn.commit()
    conn.close()

seed_sari_sari_store_data()

# Custom CSS
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
        max-width: 100% !important;
    }

    .stApp {
        background: linear-gradient(135deg, #0056b3 0%, #0080ff 50%, #1a8cff 100%);
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
        color: #000000 !important;
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

    .responsive-logo-max {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 100%;
        max-width: 450px;
        height: auto;
        object-fit: contain;
    }
    </style>
""", unsafe_allow_html=True)

# Main Header
st.markdown("<h1 style='text-align: center; color: white; font-size: 24px; font-weight: bold;'>🛒 DELA CRUZ SARI-SARI STORE INVENTORY SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.3); margin-top: 10px; margin-bottom: 25px;'>", unsafe_allow_html=True)

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
        _, center_col, _ = st.columns([1, 1.8, 1])
        with center_col:
            st.markdown("<h3 style='text-align: center; color: white; font-weight: bold;'>CREATE ACCOUNT</h3>", unsafe_allow_html=True)
            st.markdown("<div style='text-align: center; font-size: 45px; margin-bottom: 15px;'>📝</div>", unsafe_allow_html=True)

            reg_user = st.text_input("New Username", key="reg_user")
            reg_pass = st.text_input("New Password", type="password", key="reg_pass")
            reg_pass_conf = st.text_input("Confirm Password", type="password", key="reg_pass_conf")
            reg_role = st.selectbox("Account Role", ["Staff", "Admin"], key="reg_role")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Register Account", use_container_width=True):
                if reg_user and reg_pass and reg_pass_conf:
                    if reg_pass == reg_pass_conf:
                        if register_user(reg_user, reg_pass, reg_role):
                            st.success("Account created successfully! Please login.")
                            st.session_state.page = "login"
                            st.rerun()
                        else:
                            st.error("Username already exists!")
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
        _, center_col, _ = st.columns([1, 1.8, 1])
        with center_col:
            try:
                def get_image_base64(path):
                    with open(path, "rb") as img_file:
                        return base64.b64encode(img_file.read()).decode()
                
                img_data = get_image_base64("ge.png")
                st.markdown(
                    f'<div style="text-align: center; margin-bottom: 15px;">'
                    f'<img src="data:image/png;base64,{img_data}" class="responsive-logo-max">'
                    f'</div>', 
                    unsafe_allow_html=True
                )
            except Exception:
                st.markdown("<div style='text-align: center; font-size: 80px; margin-bottom: 10px;'>👤</div>", unsafe_allow_html=True)

            st.markdown("<h3 style='text-align: center; color: white; font-weight: bold;'>USER LOGIN</h3>", unsafe_allow_html=True)

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
                    st.info("Feature coming soon!")

else:
    # LOGGED IN DASHBOARD
    st.sidebar.markdown(f"### 👤 User: **{st.session_state.username}**")
    menu = st.sidebar.radio("Navigation", ["Dashboard", "Products (Paninda)", "Categories", "Suppliers", "Logout"])

    conn = get_connection()

    if menu == "Dashboard":
        st.markdown(f"<h2 style='color: white;'>🏪 Sari-Sari Store Summary</h2>", unsafe_allow_html=True)
        
        # Quick Statistics
        total_prod = pd.read_sql_query("SELECT COUNT(*) as count FROM Product", conn).iloc[0]['count']
        total_cat = pd.read_sql_query("SELECT COUNT(*) as count FROM Category", conn).iloc[0]['count']
        total_sup = pd.read_sql_query("SELECT COUNT(*) as count FROM Supplier", conn).iloc[0]['count']
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Kabuuang Paninda (Products)", total_prod)
        c2.metric("Mga Kategorya (Categories)", total_cat)
        c3.metric("Mga Supplier", total_sup)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📋 Mabilisang Silip sa Inventory")
        df_overview = pd.read_sql_query("""
            SELECT p.Product_ID, p.Product_Name, c.Category_Name, p.Product_Price as 'Presyo (₱)', p.Product_quantity as 'Stocks'
            FROM Product p
            LEFT JOIN Category c ON p.Category_ID = c.Category_ID
        """, conn)
        st.dataframe(df_overview, use_container_width=True)

    elif menu == "Products (Paninda)":
        st.subheader("📦 Pamamahala ng mga Paninda")
        
        tab1, tab2 = st.tabs(["📄 Masterlist ng Paninda", "➕ Magdagdag ng Bagong Item"])
        
        with tab1:
            df_prod = pd.read_sql_query("""
                SELECT 
                    p.Product_ID as 'ID',
                    p.Product_Name as 'Pangalan',
                    c.Category_Name as 'Kategorya',
                    s.Name as 'Supplier',
                    p.Product_unit as 'Unidad',
                    p.Product_Price as 'Presyo (₱)',
                    p.Product_quantity as 'Stocks',
                    p.Product_Status as 'Status'
                FROM Product p
                LEFT JOIN Category c ON p.Category_ID = c.Category_ID
                LEFT JOIN Supplier s ON p.Supplier_ID = s.Supplier_ID
            """, conn)
            st.dataframe(df_prod, use_container_width=True)

        with tab2:
            st.write("Fill up the details below to add a new sari-sari store item:")
            
            # Form Inputs
            col_a, col_b = st.columns(2)
            with col_a:
                p_id = st.text_input("Product Code/ID (e.g., P-007)")
                p_name = st.text_input("Pangalan ng Item (e.g., Great Taste White)")
                p_desc = st.text_input("Deskripsyon", "Sachet coffee")
                p_unit = st.selectbox("Unidad", ["Sachet", "Pack", "Bote", "Can", "Piece", "Kg"])
            
            with col_b:
                cats_df = pd.read_sql_query("SELECT Category_ID, Category_Name FROM Category", conn)
                sups_df = pd.read_sql_query("SELECT Supplier_ID, Name FROM Supplier", conn)
                
                cat_choice = st.selectbox("Kategorya", cats_df["Category_Name"].tolist()) if not cats_df.empty else None
                sup_choice = st.selectbox("Supplier", sups_df["Name"].tolist()) if not sups_df.empty else None
                
                p_price = st.number_input("Presyo (₱)", min_value=0.0, value=10.0, step=0.5)
                p_qty = st.number_input("Bilang ng Stock", min_value=0, value=20, step=1)

            if st.button("Save Product"):
                if p_id and p_name and cat_choice and sup_choice:
                    selected_cat_id = int(cats_df[cats_df["Category_Name"] == cat_choice]["Category_ID"].values[0])
                    selected_sup_id = int(sups_df[sups_df["Name"] == sup_choice]["Supplier_ID"].values[0])
                    
                    try:
                        cur = conn.cursor()
                        cur.execute("""
                            INSERT INTO Product (Product_ID, Product_Name, Product_description, Product_unit, Product_Price, Product_quantity, Product_Status, Other_Details, Supplier_ID, Category_ID)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (p_id, p_name, p_desc, p_unit, p_price, p_qty, "Available", "Added via app", selected_sup_id, selected_cat_id))
                        conn.commit()
                        st.success(f"Nai-save na ang '{p_name}'!")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("Nagagamit na ang Product ID na ito. Pumili ng iba.")
                else:
                    st.warning("Paki-kumpleto ang mga kinakailangang field.")

    elif menu == "Categories":
        st.subheader("📑 Listahan ng Kategorya")
        df_cat = pd.read_sql_query("SELECT Category_ID as 'ID', Category_Name as 'Kategorya', Description as 'Deskripsyon' FROM Category", conn)
        st.dataframe(df_cat, use_container_width=True)

    elif menu == "Suppliers":
        st.subheader("🚚 Listahan ng mga Supplier")
        df_sup = pd.read_sql_query("SELECT Supplier_ID as 'ID', Name as 'Pangalan', Address, Phone, Email, other_details as 'Detalye' FROM Supplier", conn)
        st.dataframe(df_sup, use_container_width=True)

    elif menu == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    conn.close()
