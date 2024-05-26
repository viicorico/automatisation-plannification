import pandas as pd
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QLineEdit
from PyQt5.uic import loadUi
from emploiTemps import ScheduleApp




class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('login.ui', self)
        self.loginButton.clicked.connect(self.handle_login)
        self.listeNumeroEtudiant = []
        self.listeNom = []
        self.listeMotDePasseEtudiant = []
        self.listeNumeroAdmin = []
        self.listMotDePasseAdmin = []
        self.charger_donnees()



    def charger_donnees(self):
        fichier_etu_csv = pd.read_csv('Etudiant.csv', header=None)
        tableau_etu = fichier_etu_csv.values
        self.listeNumeroEtudiant = [str(row[1]).strip() for row in tableau_etu]
        self.listeNom = [row[0] for row in tableau_etu]
        self.listeMotDePasseEtudiant = [str(row[2]).strip() for row in tableau_etu]

        fichier_admin_csv = pd.read_csv('Administrateur.csv', header=None)
        tableau_admin = fichier_admin_csv.values
        self.listeNumeroAdmin = [str(row[1]).strip() for row in tableau_admin]
        self.listMotDePasseAdmin = [str(row[2]).strip() for row in tableau_admin]



    def handle_login(self):
        numero = self.findChild(QLineEdit, 'numeroLineEdit').text().strip()
        motDePasse = self.findChild(QLineEdit, 'passwordLineEdit').text().strip()

        print(f"Tentative de connexion avec - Numéro: {numero}, Mot de passe: {motDePasse}")  # Debug print
        if (len(numero) == 6):
            if (self.authentifierEtudiant(numero, motDePasse) == True) :
                self.planning_window = MainWindow()
                self.planning_window.show()
                self.close()
            else:
                QMessageBox.warning(self, 'Erreur', 'Numéro étudiant ou mot de passe incorrect.')

        elif (len(numero) == 3):
            if (self.authentifierAdmin(numero, motDePasse) == True) :
                self.emploiTemps_window = ScheduleApp()
                self.emploiTemps_window.show()
                self.close()
            else:
                QMessageBox.warning(self, 'Erreur', 'Numéro étudiant ou mot de passe incorrect.')
        else:
            QMessageBox.warning(self, 'Erreur', 'Numéro étudiant ou mot de passe incorrect.')

    def authentifierEtudiant(self, numero, motDePasse):
        try:
            if numero in self.listeNumeroEtudiant:
                index = self.listeNumeroEtudiant.index(numero)
                print(index)
                print(self.listeMotDePasseEtudiant[index])
                print(self.listeMotDePasseEtudiant[index])
                print(motDePasse)
                if (self.listeMotDePasseEtudiant[index] == motDePasse):
                    print("Connexion réussie")
                    return True
            else:
                return False
        except ValueError:
            return False

    def authentifierAdmin(self, numero, motDePasse):
        try:
            if numero in self.listeNumeroAdmin:
                index = self.listeNumeroAdmin.index(numero)
                print(index)
                print(self.listMotDePasseAdmin[index])
                print(self.listMotDePasseAdmin[index])
                print(motDePasse)
                if (self.listMotDePasseAdmin[index] == motDePasse):
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
