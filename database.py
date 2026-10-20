import sqlite3
import hashlib

DB_NAME = "inventory.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # User Table (UML Class: User)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(40) UNIQUE NOT NULL,
            password VARCHAR(64) NOT NULL,
            role VARCHAR(40) NOT NULL,
            name VARCHAR(40),
            createdAt DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Category Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Category (
            categoryID INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(40) NOT NULL,
            description VARCHAR(100)
        )
    """)

    # Supplier Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Supplier (
            Supplier_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name VARCHAR(40) NOT NULL,
            Address VARCHAR(100),
            phone INTEGER,
            fax INTEGER,
            Email VARCHAR(40),
            other_details VARCHAR(100)
        )
    """)

    # Product Table (UML Class: Product with expiryDate & lowStockLevel)[cite: 2]
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Product (
            productID VARCHAR(40) PRIMARY KEY,
            name VARCHAR(40) NOT NULL,
            description VARCHAR(100),
            categoryID INTEGER,
            price DECIMAL(10,2),
            quantity INTEGER,
            expiryDate DATE,
            lowStockLevel INTEGER DEFAULT 10,
            unit VARCHAR(20),
            supplierID INTEGER,
            FOREIGN KEY (categoryID) REFERENCES Category(categoryID),
            FOREIGN KEY (supplierID) REFERENCES Supplier(Supplier_ID)
        )
    """)

    # Sales Table (UML Class: Sales)[cite: 2]
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Sales (
            saleID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            totalAmount DECIMAL(10,2),
            paymentMethod VARCHAR(40),
            saleDate DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (userID) REFERENCES User(userID)
        )
    """)

    # SaleItem Table (UML Class: SaleItem)[cite: 2]
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SaleItem (
            saletItemID INTEGER PRIMARY KEY AUTOINCREMENT,
            saleID INTEGER,
            productID VARCHAR(40),
            quantity INTEGER,
            price DECIMAL(10,2),
            subtotal DECIMAL(10,2),
            FOREIGN KEY (saleID) REFERENCES Sales(saleID),
            FOREIGN KEY (productID) REFERENCES Product(productID)
        )
    """)

    # Settings Table (Store Information)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            storeName VARCHAR(100),
            address VARCHAR(200),
            contact VARCHAR(50)
        )
    """)

    # Default Admin & Staff Accounts
    cursor.execute("SELECT COUNT(*) FROM User")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO User (username, password, role, name) VALUES (?, ?, ?, ?)", 
                       ("admin", hash_password("admin123"), "Admin", "System Administrator"))
        cursor.execute("INSERT INTO User (username, password, role, name) VALUES (?, ?, ?, ?)", 
                       ("staff", hash_password("staff123"), "Staff", "Store Staff"))

    # Default Store Settings (Quirino Highway, Quezon City)[cite: 2]
    cursor.execute("SELECT COUNT(*) FROM Settings")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO Settings (storeName, address, contact) VALUES (?, ?, ?)",
                       ("Dela Cruz Sari-Sari Store", "1071 Brgy. Kaligayahan, Quirino Highway, Quezon City, Metro Manila", "09123456789"))

    # Default Categories & Products seed if empty
    cursor.execute("SELECT COUNT(*) FROM Category")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO Category (name, description) VALUES (?, ?)", [
            ("Inumin", "Softdrinks at Juice"),
            ("Chichirya", "Snacks at Biscuits"),
            ("Canned Goods", "Sardinas at Meatloaf")
        ])

    conn.commit()
    conn.close()

def register_user(username, password, role, name=""):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO User (username, password, role, name) VALUES (?, ?, ?, ?)",
                       (username, hash_password(password), role, name))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def verify_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE username = ? AND password = ?", (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user
