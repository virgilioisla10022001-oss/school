# --- OPTIONAL: HELPER FUNCTIONS PARA SA INVENTORY PRODUCTS ---

def add_product(name: str, category: str, quantity: int, price: float):
    """Nagdaragdag ng bagong item sa inventory."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (product_name, category, quantity, price)
        VALUES (?, ?, ?, ?)
    """, (name, category, quantity, price))
    conn.commit()
    conn.close()

def get_all_products():
    """Kina-kukuha ang lahat ng produkto mula sa database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, product_name, category, quantity, price FROM products")
    rows = cursor.fetchall()
    conn.close()
    return rows
