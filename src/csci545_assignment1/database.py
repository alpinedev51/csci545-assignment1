import sqlite3

DB_FILE = "nutrition_logs.db"


def init_db():
    """Initialize the local database with a table for logs and a table for nutrition info."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS food_logs
                 (id INTEGER PRIMARY KEY, date TEXT, food_item TEXT, weight_g REAL, 
                  calories REAL, protein REAL, carbs REAL, fats REAL)""")

    c.execute("""CREATE TABLE IF NOT EXISTS inventory
                 (name TEXT PRIMARY KEY, cals_per_100g REAL, prot_per_100g REAL, 
                  carb_per_100g REAL, fat_per_100g REAL)""")

    mock_data = [
        ("Broccoli", 34, 2.8, 7, 0.4),
        ("Cucumber", 15, 0.7, 3.6, 0.1),
        ("Mushroom", 22, 3.1, 3.3, 0.3),
        ("Bell Pepper", 31, 1, 6, 0.3),
        ("Salt Shaker", 0, 0, 0, 0),
        ("Strawberry", 24, 0, 6, 0),
        ("Lemon", 50, 0, 12, 0),
        ("Bagel", 249, 1, 80, 0.5),
        ("Guacamole", 327, 5, 15, 25),
        ("Unknown", 0, 0, 0, 0),
    ]
    c.executemany("INSERT OR IGNORE INTO inventory VALUES (?,?,?,?,?)", mock_data)
    conn.commit()
    conn.close()
