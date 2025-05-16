import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sqlite3


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = sqlite3.connect('base.db')
        self.db.cursor().execute(
            'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, email TEXT, birth TEXT)')
        self.db.commit()

        self.setWindowTitle("Прога")
        self.setGeometry(100, 100, 800, 600)

        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.layout = QVBoxLayout()
        self.central.setLayout(self.layout)

        self.name = QLineEdit()
        self.age = QLineEdit()
        self.email = QLineEdit()
        self.birth = QLineEdit()

        self.layout.addWidget(QLabel("Имя:"))
        self.layout.addWidget(self.name)
        self.layout.addWidget(QLabel("Возраст:"))
        self.layout.addWidget(self.age)
        self.layout.addWidget(QLabel("Почта:"))
        self.layout.addWidget(self.email)
        self.layout.addWidget(QLabel("ДР:"))
        self.layout.addWidget(self.birth)

        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add)
        self.layout.addWidget(self.add_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Имя", "Возраст", "Почта", "ДР"])
        self.layout.addWidget(self.table)

        self.update_btn = QPushButton("Обновить")
        self.update_btn.clicked.connect(self.update)
        self.layout.addWidget(self.update_btn)

        self.load()

    def add(self):
        c = self.db.cursor()
        c.execute("INSERT INTO users (name, age, email, birth) VALUES (?, ?, ?, ?)",
                  (self.name.text(), self.age.text(), self.email.text(), self.birth.text()))
        self.db.commit()
        self.load()
        self.name.clear()
        self.age.clear()
        self.email.clear()
        self.birth.clear()

    def update(self):
        row = self.table.currentRow()
        if row == -1:
            return
        id = self.table.item(row, 0).text()
        c = self.db.cursor()
        c.execute("UPDATE users SET name=?, age=?, email=?, birth=? WHERE id=?",
                  (self.name.text(), self.age.text(), self.email.text(), self.birth.text(), id))
        self.db.commit()
        self.load()

    def load(self):
        c = self.db.cursor()
        c.execute("SELECT * FROM users")
        data = c.fetchall()
        self.table.setRowCount(len(data))
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))


app = QApplication(sys.argv)
window = Main()
window.show()
app.exec()