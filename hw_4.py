import sqlite3

def init_db(db_path="my_database.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            email VARCHAR(30),
            city TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
    conn.commit()
    conn.close()

def add_user(name, age, email, city, db_path="my_database.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("INSERT INTO users2 (name, age, email, city) VALUES (?, ?, ?, ?)", (name, age, email, city))
    conn.commit()
    conn.close()

def get_users_by_age_range(min_age, max_age, db_path='my_database.db'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users2 WHERE age BETWEEN ? AND ?", (min_age, max_age))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_recent_users(limit=5, db_path='my_database.db'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users2 ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_all_users(db_path="my_database.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, name, age FROM users2")
    rows = cur.fetchall()
    conn.close()
    return rows

if __name__ == '__main__':
    init_db()

    add_user("Елена", 28, "elena@example.com", "Москва")
    add_user("Игорь", 35, "igor@example.com", "Казань")
    add_user("Наташа", 22, "nata@example.com", "Москва")

    for user in get_users_by_age_range(25, 35):
        print(user)

    for user2 in get_recent_users(2):
        print(user2)
