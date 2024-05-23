import pandas as pd
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QLineEdit
from PyQt5.uic import loadUi

# Assurez-vous que 'MainWindow' dans 'planning.py' est correctement défini
from planning import MainWindow



class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('login.ui', self)
        self.loginButton.clicked.connect(self.handle_login)
        self.listeNumeroEtudiant = []
        self.listeNom = []
        self.listeMotDePasse = []
        self.load_student_data()



    def load_student_data(self):
        # Charger les données des étudiants à partir du fichier CSV
        fichier_csv = pd.read_csv('Etudiant.csv', header=None)
        df = fichier_csv
        self.listeNumeroEtudiant = df[1].tolist()
        self.listeNom = df[0].tolist()
        self.listeMotDePasse = df[2].tolist()
        print(self.listeMotDePasse)
    def handle_login(self):
        numeroEtudiant = self.findChild(QLineEdit, 'numeroLineEdit').text()
        motDePasse = self.findChild(QLineEdit, 'passwordLineEdit').text()

        if self.authentifier(numeroEtudiant, motDePasse):
            self.planning_window = MainWindow()
            self.planning_window.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Erreur', 'Numéro étudiant ou mot de passe incorrect.')

    def authentifier(self, numero, motDePasse):
        try:
            index = self.listeNumeroEtudiant.index(int(numero))
            return self.listeMotDePasse[index] == motDePasse
        except ValueError:
            return False


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
