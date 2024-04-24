import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout
from Login.c2w_login import LoginWindow
from PyQt5 import QtGui

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = LoginWindow()

    ex.setWindowIcon(QtGui.QIcon('.\\assets\\images\\logo.jpg')) 
    ex.setWindowTitle('User Info Form Application') 
    ex.setGeometry(1100, 40, 768, 1024) 
    ex.setFixedSize(750,750) 
    ex.show() 
    sys.exit(app.exec_())