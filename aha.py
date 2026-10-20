import streamlit as st
import sqlite3
import hashlib

# 1. Page Configuration
st.set_page_config(
    page_title="Dela Cruz Store Inventory Management System",
    page_icon="🛒",
    layout="centered"
)

# 2. Custom CSS para itago ang "Manage app" button at iba pang Streamlit UI elements
hide_streamlit_style = """
    <style>
    div[data-testid="stStatusWidget"] {
        visibility: hidden;
        display: none !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 3. Database Connection & Setup
def init_db():
    conn = sqlite3.connect('store_inventory.db')
    cursor = conn.cursor()
    # Table para sa mga users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    # Table para sa inventory products
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            quantity INTEGER,
            price REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Helper function para i-hash ang password
def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hash(password, hashed_text):
    if make_hash(password) == hashed_text:
        return True
    return False

# Session State para sa Authentication
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'page' not in st.session_state:
    st.session_state['page'] = "Login"

# 4. Navigation Logic
if not st.session_state['logged_in']:
    
    st.markdown("<h2 style='text-align: center;'>🛒 DELA CRUZ STORE INVENTORY MANAGEMENT SYSTEM</h2>", unsafe_allow_html=True)
    st.write("---")
    
    # Pagpili ng Page (Login o Create Account)
    menu = ["Login", "Create Account", "Forgot Password"]
    choice = st.selectbox("Piliin ang gawain", menu, label_visibility="collapsed")
    
    if choice == "Login":
        st.markdown("<h3 style='text-align: center;'>USER LOGIN</h3>", unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="I-type ang username", key="login_user")
        show_password = st.checkbox("Show Password", key="login_show")
        password_type = "text" if show_password else "password"
        password = st.text_input("Password", type=password_type, placeholder="I-type ang password", key="login_pass")
        
        if st.button("LOGIN", use_container_width=True):
            conn = sqlite3.connect('store_inventory.db')
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            conn.close()
            
            if result and check_hash(password, result[0]):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("Matagumpay na nakapag-login!")
                st.rerun()
            else:
                st.error("Maling username o password.")
                
    elif choice == "Create Account":
        st.markdown("<h3 style='text-align: center;'>CREATE ACCOUNT</h3>", unsafe_allow_html=True)
        
        new_user = st.text_input("Bagong Username", placeholder="Ilagay ang gustong username", key="reg_user")
        new_pass = st.text_input("Bagong Password", type="password", placeholder="Ilagay ang password", key="reg_pass")
        
        if st.button("REGISTER", use_container_width=True):
            if new_user and new_pass:
                conn = sqlite3.connect('store_inventory.db')
                cursor = conn.cursor()
                try:
                    cursor.execute('INSERT INTO users(username, password) VALUES (?, ?)', (new_user, make_hash(new_pass)))
                    conn.commit()
                    st.success("Tagumpay ang paggawa ng account! Pwede ka nang mag-login.")
                except sqlite3.IntegrityError:
                    st.error("May gumagamit na ng username na ito.")
                finally:
                    conn.close()
            else:
                st.warning("Punan ang lahat ng kahon.")
                
    elif choice == "Forgot Password":
        st.markdown("<h3 style='text-align: center;'>RESET PASSWORD</h3>", unsafe_allow_html=True)
        f_user = st.text_input("Username", key="f_user")
        f_new_pass = st.text_input("Bagong Password", type="password", key="f_pass")
        
        if st.button("I-update ang Password", use_container_width=True):
            conn = sqlite3.connect('store_inventory.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (f_user,))
            if cursor.fetchone():
                cursor.execute('UPDATE users SET password = ? WHERE username = ?', (make_hash(f_new_pass), f_user))
                conn.commit()
                st.success("Na-update na ang password! Mag-login gamit ang bago mong password.")
            else:
                st.error("Walang nakitang ganitong username.")
            conn.close()

else:
    # 5. Main Dashboard (Pagkatapos mag-login)
    st.sidebar.title(f"Welcome, {st.session_state['username']}!")
    menu_option = st.sidebar.radio("Navigation", ["Dashboard & Inventory", "Mag-logout"])
    
    if menu_option == "Dashboard & Inventory":
        st.title("📦 Store Inventory Management")
        st.write("Dito mo mamamahala ang mga produkto sa iyong tindahan.")
        
        # Form para magdagdag ng produkto
        with st.form("add_product_form"):
            st.subheader("Magdagdag ng Bagong Produkto")
            item_name = st.text_input("Pangalan ng Produkto")
            quantity = st.number_input("Dami (Quantity)", min_value=1, value=1)
            price = st.number_input("Presyo (Price sa PHP)", min_value=0.0, value=0.0, format="%.2f")
            
            submit_product = st.form_submit_button("Idagdag sa Inventory")
            
            if submit_product:
                if item_name:
                    conn = sqlite3.connect('store_inventory.db')
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO products(item_name, quantity, price) VALUES (?, ?, ?)', (item_name, quantity, price))
                    conn.commit()
                    conn.close()
                    st.success(Tagumpay na naidagdag ang {item_name}!)
                else:
                    st.warning("Ilagay ang pangalan ng produkto.")
        
        st.write("---")
        st.subheader("📋 Listahan ng mga Produkto")
        
        # Ipakita ang mga produkto mula sa database
        conn = sqlite3.connect('store_inventory.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, item_name, quantity, price FROM products')
        rows = cursor.fetchall()
        conn.close()
        
        if rows:
            for row in rows:
                col1, col2, col3 = st.columns([3, 2, 2])
                col1.write(f"**{row[1]}**")
                col2.write(f"Qty: {row[2]}")
                col3.write(f"₱{row[3]:.2f}")
        else:
            st.info("Wala pang laman ang inventory.")

    elif menu_option == "Mag-logout":
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.success("Naka-logout na.")
        st.rerun()
