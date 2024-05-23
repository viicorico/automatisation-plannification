import pandas as pd


def lire_donnees_etudiants(fichier_csv):
    # Lire le fichier CSV
    fichier_csv = pd.read_csv(fichier_csv, header=None)

    # Convertir en tableau NumPy
    tableau = fichier_csv.values

    # Initialiser les listes
    listeNumeroEtudiant = []
    listeNom = []
    listeMotDePasse = []
    listeFiliere = []

    # Obtenir le nombre de lignes
    compteur = len(tableau)

    # Remplir les listes avec les données
    for i in range(compteur):
        listeNumeroEtudiant.append(tableau[i][1])
        listeNom.append(tableau[i][0])
        listeMotDePasse.append(tableau[i][2])
        listeFiliere.append(tableau[i][3])

    return listeNumeroEtudiant, listeNom, listeMotDePasse, listeFiliere

# Fonction pour rechercher un étudiant selon son numéro d'étudiant
# renvoit le nom, la filiere le mot de passe de l'étudiant si trouvé, sinon renvoie -1,-1,-1 si on trouve pas l'élève'
def rechercherEtu(listeNumeroEtudiants,listeNom,listeMotDePasse, listeFiliere,numeroRecherche):
    compteur = len(listeNumeroEtudiants)
    for i in range(compteur):
        if(listeNumeroEtudiants[i]==numeroRecherche):
            return(listeNom[i], listeMotDePasse[i], listeFiliere[i])
    return (-1,-1,-1)

"""
numeroRecherche  = 723156

nom, motdePasse = rechercherEtu(listeNumeroEtudiant, listeNom, listeMotDePasse, numeroRecherche)

if(nom!= -1 and motdePasse!= -1):
    print(nom,motdePasse)
else:
    print("erreur !")
"""
