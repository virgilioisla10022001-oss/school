import sqlite3
import hashlib
import os

DB_NAME = "inventory.db"


def hash_password(password: str, salt: bytes = None) -> tuple[str, str]:
    if salt is None:
        salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    return hashed.hex(), salt.hex()


def init_db():
    """I-in-initialize ang database at awtomatikong gagawa ng default admin account."""
    with sqlite3.connect(DB_NAME, check_same_thread=False) as conn:
        cursor = conn.cursor()
        
        # 1. Siguraduhing malinis at tama ang Users Table schema
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 2. Products Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                category TEXT,
                quantity INTEGER DEFAULT 0,
                price REAL DEFAULT 0.0,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        # 3. Automatic Default Account
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            p_hash, s_hex = hash_password("admin123")
            cursor.execute("""
                INSERT INTO users (username, password_hash, salt)
                VALUES (?, ?, ?)
            """, ("admin", p_hash, s_hex))
            conn.commit()


def register_user(username: str, password: str) -> bool:
    init_db()
    username_clean = username.strip().lower()
    
    if not username_clean or not password:
        return False

    password_hash, salt_hex = hash_password(password)

    try:
        with sqlite3.connect(DB_NAME, check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password_hash, salt)
                VALUES (?, ?, ?)
            """, (username_clean, password_hash, salt_hex))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print(f"Error registering user: {e}")
        return False


def verify_user(username: str, password: str) -> bool:
    init_db()
    username_clean = username.strip().lower()

    try:
        with sqlite3.connect(DB_NAME, check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT password_hash, salt FROM users WHERE username = ?
            """, (username_clean,))
            result = cursor.fetchone()

        if not result:
            return False

        stored_hash, stored_salt_hex = result
        stored_salt = bytes.fromhex(stored_salt_hex)
        input_hash, _ = hash_password(password, stored_salt)

        return input_hash == stored_hash
    except Exception as e:
        print(f"Error verifying user: {e}")
        return False


def add_product(product_name: str, category: str, quantity: int, price: float) -> bool:
    init_db()
    try:
        with sqlite3.connect(DB_NAME, check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO products (product_name, category, quantity, price)
                VALUES (?, ?, ?, ?)
            """, (product_name.strip(), category.strip(), quantity, price))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error adding product: {e}")
        return False


def get_all_products():
    init_db()
    try:
        with sqlite3.connect(DB_NAME, check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, product_name, category, quantity, price, date_added FROM products")
            return cursor.fetchall()
    except Exception as e:
        print(f"Error getting products: {e}")
        return []


def update_product(product_id: int, product_name: str, category: str, quantity: int, price: float) -> bool:
    init_db()
    try:
        with sqlite3.connect(DB_NAME, check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE products 
                SET product_name = ?, category = ?, quantity = ?, price = ?
                WHERE id = ?
            """, (product_name.strip(), category.strip(), quantity, price, product_id))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error updating product: {e}")
        return False


def delete_product(product_id: int) -> bool:
    init_db()
    try:
        with sqlite3.connect(DB_NAME, check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error deleting product: {e}")
        return False
