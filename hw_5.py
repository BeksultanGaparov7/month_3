import argparse
import sqlite3
from sqlite3 import Error

class UserManager:
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self._initialize_db()

    def _connect(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except Error as e:
            print(f"Ошибка подключения к БД: {e}")
            raise

    def _initialize_db(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            name   TEXT    NOT NULL,
            age    INTEGER,
            email  TEXT    UNIQUE,
            city   TEXT
        );
        """
        conn = self._connect()
        try:
            conn.execute(sql)
            conn.commit()
        finally:
            conn.close()

    def add_user(self, name, age, email=None, city=None):
        sql = "INSERT INTO users (name, age, email, city) VALUES (?, ?, ?, ?)"
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute(sql, (name, age, email, city))
            conn.commit()
            return cur.lastrowid
        except Error as e:
            print(f"Ошибка при добавлении пользователя: {e}")
            raise
        finally:
            conn.close()

    def get_all_users(self):
        sql = "SELECT * FROM users ORDER BY id"
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute(sql)
            return cur.fetchall()
        finally:
            conn.close()

    def update_user(self, user_id, name=None, age=None, email=None, city=None):
        fields = []
        params = []
        if name is not None:
            fields.append("name = ?")
            params.append(name)
        if age is not None:
            fields.append("age = ?")
            params.append(age)
        if email is not None:
            fields.append("email = ?")
            params.append(email)
        if city is not None:
            fields.append("city = ?")
            params.append(city)

        if not fields:
            return 0

        params.append(user_id)
        sql = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
            return cur.rowcount
        finally:
            conn.close()

def parse_args():
    parser = argparse.ArgumentParser(description='CRUD CLI для таблицы users')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('add', help='Добавить пользователя')
    p.add_argument('--name', required=True, help='Имя')
    p.add_argument('--age', type=int, required=True, help='Возраст')
    p.add_argument('--email', help='Email')
    p.add_argument('--city', help='Город')

    sub.add_parser('list', help='Показать всех пользователей')

    p = sub.add_parser('update', help='Обновить данные пользователя')
    p.add_argument('--id', type=int, required=True, help='ID пользователя')
    p.add_argument('--name', help='Новое имя')
    p.add_argument('--age', type=int, help='Новый возраст')
    p.add_argument('--email', help='Новый email')
    p.add_argument('--city', help='Новый город')

    return parser.parse_args()

def main():
    args = parse_args()
    db = UserManager()

    if args.cmd == 'add':
        uid = db.add_user(args.name, args.age, args.email, args.city)
        print(f'✅ Пользователь создан с ID={uid}')

    elif args.cmd == 'list':
        rows = db.get_all_users()
        print("ID | Name       | Age | Email                | City")
        print("------------------------------------------------------------")
        for r in rows:
            print(f"{r['id']:2d} | {r['name']:<10} | {r['age'] or '-':>3} | {r['email'] or '-':<20} | {r['city'] or '-'}")

    elif args.cmd == 'update':
        count = db.update_user(args.id, args.name, args.age, args.email, args.city)
        if count:
            print(f'✅ Обновлено строк: {count}')
        else:
            print("⚠️ Нечего обновлять или пользователь не найден.")

if __name__ == '__main__':
    main()