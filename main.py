from PyQt5.QtWidgets import QApplication, QMainWindow
from py.login import LoginWindow




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login_window = LoginWindow()
        self.setCentralWidget(self.login_window)
        screen = QApplication.desktop().screenGeometry()
        largeur = screen.width()
        hauteur = screen.height()

        # définir la taille de la fenêtre pour occuper toute la résolution de l'écran
        self.setGeometry(0, 0, largeur, hauteur)

        # afin de s'assurer que la fenêtre est affichée en plein écran
        self.showMaximized()

if __name__ == "__main__": # C'est le main github
    app = QApplication([])

    main_window = MainWindow()
    main_window.show()
    app.exec_()

