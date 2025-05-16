import sys, os, sqlite3, csv, socket, shutil

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableView, QSpinBox, QProgressBar, QPushButton, QLineEdit,
    QLabel, QStatusBar, QFileDialog, QMessageBox, QFormLayout,
    QSplashScreen, QGraphicsOpacityEffect
)
from PyQt6.QtGui import QAction, QMovie, QPixmap, QIcon
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QTimer
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel

class PortScanner(QThread):
    progress = pyqtSignal(int, bool)
    finished = pyqtSignal()