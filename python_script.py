import sqlite3

conn = sqlite3.connect("pharmacy.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        expiry_date TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
print("Database initialized successfully!")
