import sqlite3

db_path = "users.db"

def connect_db():
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOENCREMENT,
            name TEXT NOT NULL,
            age INT,
            email TEXT UNIQUE,
            phone TEXT
        )
    """)
    conn.commit()
    conn.close()

def update_user(user_id, name, age, email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""UPDATE users SET name = ?, age = ?, email = ? WHERE id = ?""", (name, age, email))
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated


