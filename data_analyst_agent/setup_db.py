# setup_database.py
import sqlite3
import os

DB_FILE = "./products.db"

# Delete the database file if it exists to ensure a clean start
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

# Connect to the SQLite database (this will create the file)
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create the 'products' table
cursor.execute("""
               CREATE TABLE products (
                 id INTEGER PRIMARY KEY,
                 name TEXT NOT NULL,
                 category TEXT NOT NULL,
                 price REAL NOT NULL,
                 stock INTEGER NOT NULL
               );
               """)

# Sample product data
products_data = [
    ("Gaming Laptop", "Electronics", 1299.99, 75),
    ("Smart Watch", "Electronics", 299.99, 200),
    ("Wireless Earbuds", "Electronics", 159.99, 350),
    ("Air Fryer", "Home Goods", 129.99, 180),
    ("Robot Dog", "Electronics", 799.99, 50),
    ("Smart Doorbell", "Home Goods", 179.99, 150),
    ("Electric Skateboard", "Sports", 599.99, 40),
    ("Drone with Camera", "Electronics", 899.99, 100),
    ("Smart Garden System", "Home Goods", 249.99, 80),
    ("3D Printer", "Electronics", 399.99, 60),
    ("Electric Scooter", "Sports", 699.99, 90),
    ("Smart Mirror", "Home Goods", 299.99, 70),
    ("Gaming Console", "Electronics", 499.99, 200),
    ("Smart Refrigerator", "Home Goods", 2499.99, 30),
    ("Foldable Smartphone", "Electronics", 1499.99, 100),
    ("Smart Treadmill", "Sports", 1299.99, 40),
    ("Home Security Camera", "Electronics", 149.99, 250),
    ("Smart Thermostat", "Home Goods", 199.99, 180),
    ("Electric Bicycle", "Sports", 1899.99, 35),
    ("Augmented Reality Glasses", "Electronics", 899.99, 80),
    ("Robot Lawn Mower", "Home Goods", 999.99, 45),
    ("Smart Weight Scale", "Health", 79.99, 300),
    ("Portable Power Station", "Electronics", 799.99, 120),
    ("Smart Toothbrush", "Health", 129.99, 200),
    ("Digital Drawing Tablet", "Electronics", 299.99, 150),
    ("Indoor Herb Garden", "Home Goods", 159.99, 140),
    ("Smart Golf Club", "Sports", 399.99, 60),
    ("Holographic Display", "Electronics", 2999.99, 20),
    ("Smart Water Bottle", "Health", 49.99, 400),
    ("Gaming Chair", "Furniture", 299.99, 100),
    ("Smart Dumbbells", "Sports", 249.99, 150),
    ("UV Sanitizer Box", "Health", 89.99, 280),
    ("Smart Projector", "Electronics", 799.99, 90),
    ("Air Quality Monitor", "Home Goods", 149.99, 200),
    ("Electric Surfboard", "Sports", 2499.99, 15),
    ("Brain-sensing Headband", "Health", 249.99, 100),
    ("Vertical Garden System", "Home Goods", 399.99, 70),
    ("Smart Piano", "Musical Instruments", 1999.99, 25),
    ("Flying Car Model", "Toys", 299.99, 120),
    ("Quantum Computer Kit", "Electronics", 4999.99, 10),
    ("Smart Basketball", "Sports", 99.99, 250),
    ("Home Elevator", "Home Goods", 9999.99, 5),
    ("Mind-controlled Drone", "Electronics", 1499.99, 30),
    ("Space Garden Kit", "Science", 599.99, 50),
    ("Neural Interface Headset", "Electronics", 3499.99, 15),
    ("Teleportation Pod Model", "Science", 899.99, 25),
    ("Anti-Gravity Simulator", "Science", 7999.99, 5),
    ("Time Machine Replica", "Collectibles", 1999.99, 20),
    ("Cybernetic Plant Pot", "Home Goods", 199.99, 150),
    ("DNA Analysis Kit", "Science", 399.99, 80),
    ("Fusion Reactor Model", "Science", 2999.99, 10),
    ("AI Chess Computer", "Games", 799.99, 50),
    ("Quantum Encryption Key", "Security", 1499.99, 30),
    ("Bionic Hand Prototype", "Science", 5999.99, 8),
    ("Plasma Globe Lamp", "Home Goods", 129.99, 200),
    ("Mars Colony VR Set", "Electronics", 899.99, 40),
    ("Nano Robot Kit", "Science", 699.99, 60),
    ("Sonic Screwdriver Replica", "Collectibles", 149.99, 300),
    ("Memory Transfer Device", "Electronics", 4999.99, 5),
    ("Levitating Plant Pot", "Home Goods", 299.99, 100),
    ("Personal Force Field", "Security", 3999.99, 15),
    ("Quantum Entanglement Watch", "Electronics", 2499.99, 25),
]

# Insert the data into the table
cursor.executemany(
    """
                   INSERT INTO products (name, category, price, stock)
                   VALUES (?, ?, ?, ?);
                   """,
    products_data,
)

# Commit the changes and close the connection
conn.commit()
conn.close()

print(f"Database '{DB_FILE}' created and populated successfully.")
print(f"Absolute path: {os.path.abspath(DB_FILE)}")
