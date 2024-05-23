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
        self.charger_donnees()



    def charger_donnees(self):
        fichier_csv = pd.read_csv('Etudiant.csv', header=None)
        tableau = fichier_csv.values

        self.listeNumeroEtudiant = [str(row[1]).strip() for row in tableau]
        self.listeNom = [row[0] for row in tableau]
        self.listeMotDePasse = [str(row[2]).strip() for row in tableau]

    def handle_login(self):
        numeroEtudiant = self.findChild(QLineEdit, 'numeroLineEdit').text().strip()
        motDePasse = self.findChild(QLineEdit, 'passwordLineEdit').text().strip()

        print(f"Tentative de connexion avec - Numéro: {numeroEtudiant}, Mot de passe: {motDePasse}")  # Debug print

        if (self.authentifier(numeroEtudiant, motDePasse) == True) :
            self.planning_window = MainWindow()
            self.planning_window.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Erreur', 'Numéro étudiant ou mot de passe incorrect.')

    def authentifier(self, numero, motDePasse):
        try:
            if numero in self.listeNumeroEtudiant:
                index = self.listeNumeroEtudiant.index(numero)
                print(index)
                print(self.listeMotDePasse[index])
                print(self.listeMotDePasse[index])
                print(motDePasse)
                if (self.listeMotDePasse[index] == motDePasse):
                    print("Connexion réussie")
                    return True
            else:
                return False
        except ValueError:
            return False


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
