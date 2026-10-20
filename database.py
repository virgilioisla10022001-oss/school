import sqlite3
import hashlib

def init_db():
    """I-initialize ang SQLite database at users table kung wala pa."""
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'Staff'
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password, role="Staff"):
    """Magrehistro ng bagong user na may SHA-256 password hashing."""
    try:
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
            (username, hashed_password, role)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Kapag ang username ay umiiral na sa database
        return False

def verify_user(username, password):
    """Suriin kung tama ang username at hashed password sa pag-login."""
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?", 
        (username, hashed_password)
    )
    user = cursor.fetchone()
    conn.close()
    return user is not None
