import sqlite3

def init_db():
    conn = sqlite3.connect("store_inventory.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            birthday TEXT,
            contact TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            brand TEXT,
            category TEXT,
            quantity INTEGER,
            price REAL,
            expiry_date TEXT,
            date_added TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS retail_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            brand TEXT,
            quantity_sold INTEGER,
            date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_date TEXT,
            file_path TEXT
        )
    """)
    conn.commit()
    conn.close()

def register_user(fullname, username, password, email, birthday, contact):
    try:
        conn = sqlite3.connect("store_inventory.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (fullname, username, password, email, birthday, contact) VALUES (?, ?, ?, ?, ?, ?)",
                       (fullname, username, password, email, birthday, contact))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def verify_user(username, password):
    conn = sqlite3.connect("store_inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def reset_password(username, email, new_password):
    conn = sqlite3.connect("store_inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND email = ?", (username, email))
    user = cursor.fetchone()
    if user:
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def add_product(product_name, brand, category, quantity, price, expiry_date, date_added):
    conn = sqlite3.connect("store_inventory.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (product_name, brand, category, quantity, price, expiry_date, date_added) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (product_name, brand, category, quantity, price, expiry_date, date_added))
    conn.commit()
    conn.close()

def get_all_products():
    conn = sqlite3.connect("store_inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_product(prod_id, product_name, brand, category, quantity, price, expiry_date):
    conn = sqlite3.connect("store_inventory.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE products SET product_name = ?, brand = ?, category = ?, quantity = ?, price = ?, expiry_date = ?
        WHERE id = ?
    """, (product_name, brand, category, quantity, price, expiry_date, prod_id))
    conn.commit()
    conn.close()

def delete_product(prod_id):
    conn = sqlite3.connect("store_inventory.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (prod_id,))
    conn.commit()
    conn.close()

def add_retail_log(product_name, brand, qty_sold):
    conn = sqlite3.connect("store_inventory.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO retail_logs (product_name, brand, quantity_sold) VALUES (?, ?, ?)", (product_name, brand, qty_sold))
    conn.commit()
    conn.close()

def get_retail_logs():
    conn = sqlite3.connect("store_inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM retail_logs")
    rows = cursor.fetchall()
    conn.close()
    return rows  # Naayos ang typo mula sa 'rowss'
