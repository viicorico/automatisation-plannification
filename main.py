from PyQt5.QtWidgets import QApplication, QMainWindow
from login import LoginWindow

from gestionEtudiant import lire_donnees_etudiants

# Chemin du fichier CSV
fichier_csv = 'Etudiant.csv'

# Lire les données des étudiants
listeNumeroEtudiant, listeNom, listeMotDePasse, listeFiliere = lire_donnees_etudiants(fichier_csv)

# Afficher les listes
print("Numéros d'étudiant:", listeNumeroEtudiant)
print("Noms:", listeNom)
print("Mots de passe:", listeMotDePasse)
print("Filières:", listeFiliere)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login_window = LoginWindow()
        self.setCentralWidget(self.login_window)

if __name__ == "__main__": # C'est le main github
    app = QApplication([])
    #with open('stylesheet.qss', 'r') as file:
        #app.setStyleSheet(file.read())
    main_window = MainWindow()
    main_window.show()
    app.exec_()