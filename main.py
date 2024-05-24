from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from login import LoginWindow

from gestionEtudiant import lire_donnees_etudiants
from gestionEtudiant import rechercherEtu

from gestionAdministrateur import lire_donnees_Admin
from gestionAdministrateur import rechercherAdmin

from gestionMatiere import lire_donnees_Matiere


# Chemin du fichier CSV Etudiants
fichier_csv = 'Etudiant.csv'

# Chemin du fichier CSV Administrateurs
fichierAdmin_csv = 'Administrateur.csv'

# Chemin du fichier CSV Matieres
fichierMatiere_csv = 'Matieres.csv'

# Lire les données des étudiants
listeNumeroEtudiant, listeNom, listeMotDePasse, listeFiliere = lire_donnees_etudiants(fichier_csv)

# Fonction qui recherche un étudiant par selon son numéro d'étudiant
# et qui retourne son nom et son mot de passe et sa filiere'


# Afficher les listes
print("Numéros d'étudiant:", listeNumeroEtudiant)
print("Noms:", listeNom)
print("Mots de passe:", listeMotDePasse)
print("Filières:", listeFiliere)

#Exemple de recherche d'un étudiant avec son numéro étudiant
numeroRechercheEtudiant  = 723156
nom, filiere, motdePasse = rechercherEtu(listeNumeroEtudiant, listeNom, listeMotDePasse, listeFiliere,numeroRechercheEtudiant)
print(nom, filiere, motdePasse)

listeNumeroAdmin, listeNom, listeMotDePasse = lire_donnees_Admin(fichier_csv)

# Afficher les listes des administrateurs
print("Numéros d'administrateurs:", listeNumeroAdmin)
print("Noms:", listeNom)
print("Mots de passe:", listeMotDePasse)

#Exemple de recherche d'un Administrateur avec son numéro administrateur
numeroRechercheAdmin  = 333
nom, motdePasse = rechercherAdmin(listeNumeroAdmin, listeNom, listeMotDePasse,numeroRechercheAdmin)
print(nom, motdePasse)

listeMatiereGI, listeDureeMatiereGI, listeMatiereGMI, listeDureeMatiereGMI, listeMatiereGMF, listeDureeMatiereGMF = lire_donnees_Matiere(fichierMatiere_csv)

print(listeMatiereGI)
print(listeDureeMatiereGI)

print(listeMatiereGMI)
print(listeDureeMatiereGMI)

print(listeMatiereGMF)
print(listeDureeMatiereGI)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login_window = LoginWindow()
        self.setCentralWidget(self.login_window)
        screen = QApplication.desktop().screenGeometry()
        largeur = screen.width()
        hauteur = screen.height()

        # Définir la taille de la fenêtre pour occuper toute la résolution de l'écran
        self.setGeometry(0, 0, largeur, hauteur)

        # Pour s'assurer que la fenêtre est affichée en plein écran
        self.showMaximized()

if __name__ == "__main__": # C'est le main github
    app = QApplication([])
    #with open('stylesheet.qss', 'r') as file:
        #app.setStyleSheet(file.read())
    main_window = MainWindow()
    main_window.show()
    app.exec_()

