import sqlite3

try:
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('members.db')
    cursor = conn.cursor()

    # Create table
    # Create table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS members (
        Id INTEGER UNIQUE,
        Name TEXT NOT NULL,
        Email TEXT NOT NULL,
        Expiry_date TEXT,
        Contact TEXT,
        Gender TEXT,
        Birthday TEXT,
        Address TEXT
    )
    ''')


    # Commit changes and close connection
    conn.commit()
    print("Database and table created successfully.")

except sqlite3.Error as e:
    print("Error creating SQLite table:", e)

finally:
    if conn:
        conn.close()

