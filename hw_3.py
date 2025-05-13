import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QRadioButton



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('RadioButtons')
        self.setGeometry(100, 100, 300, 200)

        self.rR = QRadioButton('Red', self)
        self.rR.move(50, 50)
        self.rG = QRadioButton('Green', self)
        self.rG.move(50, 80)
        self.rB = QRadioButton('Blue', self)
        self.rB.move(50, 110)

        self.label = QLabel('Chose a color:', self)
        self.label.move(50, 20)
        self.label.setWordWrap(True)

        self.label2 = QLabel('', self)
        self.label2.move(50, 140)
        self.label2.setWordWrap(True)

        self.rB.toggled.connect(self.radio_changed)
        self.rG.toggled.connect(self.radio_changed)
        self.rR.toggled.connect(self.radio_changed)


    def radio_changed(self):
        if self.rB.isChecked():
            self.label2.setText('You chose color:[Blue]')
        elif self.rG.isChecked():
            self.label2.setText('You chose color:[Green]')
        elif self.rR.isChecked():
            self.label2.setText('You chose color:[Red]')

        self.label2.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())