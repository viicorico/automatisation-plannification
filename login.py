from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

from planning import MainWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('login.ui', self)
        self.loginButton.clicked.connect(self.handle_login)

    def handle_login(self):
        # Vous pouvez ajouter une vérification de nom d'utilisateur et mot de passe ici
        self.planning_window = MainWindow()
        self.planning_window.show()
        self.close()