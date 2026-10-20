import sqlite3
import hashlib

def init_db():
    conn = sqlite3.connect('dela_cruz_store.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    try:
        conn = sqlite3.connect('dela_cruz_store.db', check_same_thread=False)
        cursor = conn.cursor()
        hashed_pwd = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pwd))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def verify_user(username, password):
    conn = sqlite3.connect('dela_cruz_store.db', check_same_thread=False)
    cursor = conn.cursor()
    hashed_pwd = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pwd))
    user = cursor.fetchone()
    conn.close()
    return user is not None
