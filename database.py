import sqlite3
import hashlib

DB_NAME = "inventory.db"

def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Enables column access by name
    return conn

def hash_password(password):
    """Hash password using SHA-256 for basic security."""
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    """Initialize the database and create tables based on the ERD schema."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Role Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Role (
            Role_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Role_Name VARCHAR(40) UNIQUE NOT NULL,
            Description VARCHAR(40)
        )
    """)

    # 2. Staff Table (Maps to your Login / Authentication)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Staff (
            Staff_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            First_Name VARCHAR(40),
            Last_Name VARCHAR(40),
            Address VARCHAR(40),
            Phone INTEGER,
            Email VARCHAR(40),
            UserName VARCHAR(40) UNIQUE NOT NULL,
            PassWord VARCHAR(40) NOT NULL,
            Role_ID INTEGER,
            FOREIGN KEY (Role_ID) REFERENCES Role(Role_ID)
        )
    """)

    # 3. Supplier Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Supplier (
            Supplier_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name VARCHAR(40) NOT NULL,
            Address VARCHAR(40),
            phone INTEGER,
            fax INTEGER,
            Email VARCHAR(40),
            other_details VARCHAR(40)
        )
    """)

    # 4. Category Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Category (
            Category_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Category_Name VARCHAR(40) NOT NULL,
            Description VARCHAR(40)
        )
    """)

    # 5. Product Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Product (
            Product_ID VARCHAR(40) PRIMARY KEY,
            Product_Name VARCHAR(40) NOT NULL,
            Product_description VARCHAR(40),
            Product_unit VARCHAR(40),
            Product_Price FLOAT(8,1),
            Product_quantity INTEGER,
            Product_Status VARCHAR(40),
            Other_Details VARCHAR(40),
            Supplier_ID INTEGER,
            Category_ID INTEGER,
            FOREIGN KEY (Supplier_ID) REFERENCES Supplier(Supplier_ID),
            FOREIGN KEY (Category_ID) REFERENCES Category(Category_ID)
        )
    """)

    # 6. Customer Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Customer (
            Customer_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            First_Name VARCHAR(40),
            Last_Name VARCHAR(40),
            Address VARCHAR(40),
            phone INTEGER,
            Email VARCHAR(40),
            Staff_ID INTEGER,
            FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID)
        )
    """)

    # 7. Order Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "Order" (
            Order_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Date_of_Order DATE,
            Order_Details VARCHAR(40),
            Customer_ID INTEGER,
            FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID)
        )
    """)

    # 8. Payment Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Payment (
            Bill_number INTEGER PRIMARY KEY AUTOINCREMENT,
            Payment_Type VARCHAR(40),
            Other_Details VARCHAR(40)
        )
    """)

    # 9. Order_Detail Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Order_Detail (
            Order_Detail_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Unit_Price FLOAT(8,1),
            Size INTEGER,
            Quantity INTEGER,
            Discount INTEGER,
            Total FLOAT(8,1),
            Date DATE,
            Product_ID VARCHAR(40),
            Order_ID INTEGER,
            Bill_number INTEGER,
            FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID),
            FOREIGN KEY (Order_ID) REFERENCES "Order"(Order_ID),
            FOREIGN KEY (Bill_number) REFERENCES Payment(Bill_number)
        )
    """)

    # Insert default roles if they don't exist yet
    cursor.execute("SELECT COUNT(*) FROM Role")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO Role (Role_Name, Description) VALUES ('Admin', 'System Administrator')")
        cursor.execute("INSERT INTO Role (Role_Name, Description) VALUES ('Staff', 'Store Staff / Cashier')")

    conn.commit()
    conn.close()

def register_user(username, password, role_name):
    """Registers a new staff user and assigns a Role ID based on Role_Name."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Get Role ID from Role Name
        cursor.execute("SELECT Role_ID FROM Role WHERE Role_Name = ?", (role_name,))
        role_row = cursor.fetchone()
        if not role_row:
            conn.close()
            return False
        
        role_id = role_row["Role_ID"]
        hashed_pw = hash_password(password)

        cursor.execute("""
            INSERT INTO Staff (UserName, PassWord, Role_ID)
            VALUES (?, ?, ?)
        """, (username, hashed_pw, role_id))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Username already exists
        conn.close()
        return False

def verify_user(username, password):
    """Verifies user credentials during login."""
    conn = get_connection()
    cursor = conn.cursor()
    
    hashed_pw = hash_password(password)
    
    cursor.execute("""
        SELECT * FROM Staff WHERE UserName = ? AND PassWord = ?
    """, (username, hashed_pw))
    
    user = cursor.fetchone()
    conn.close()
    
    return user is not None
