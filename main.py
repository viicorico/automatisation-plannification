from PyQt5.QtWidgets import QApplication, QMainWindow
from py.login import LoginWindow



#Main permet l'ouverture de l'emploie du temps(Nous pouvons le faire avec login.py).
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login_window = LoginWindow()
        self.setCentralWidget(self.login_window)
        screen = QApplication.desktop().screenGeometry()
        largeur = screen.width()
        hauteur = screen.height()


        self.setGeometry(0, 0, largeur, hauteur)


        self.showMaximized()

if __name__ == "__main__":
    app = QApplication([])
    #with open('stylesheet.qss', 'r') as file:
        #app.setStyleSheet(file.read())
    main_window = MainWindow()
    main_window.show()
    app.exec_()

