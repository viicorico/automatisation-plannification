import pandas as pd

import pandas as pd

def calculer_effectifs_par_filiere(fichier_csv_path_fct):
    # Lire le fichier CSV
    fichier_csv_fct = pd.read_csv(fichier_csv_path_fct, header=None)

    # Initialiser le dictionnaire pour stocker les effectifs par filière
    filiere_effectifs_fct = {}

    # Parcours de chaque ligne du tableau à partir de la première ligne
    for i_fct in range(len(fichier_csv_fct)):
        filiere_fct = fichier_csv_fct.iloc[i_fct, -1]  # La filière est dans la dernière colonne
        if filiere_fct in filiere_effectifs_fct:
            filiere_effectifs_fct[filiere_fct] += 1
        else:
            filiere_effectifs_fct[filiere_fct] = 1

    return filiere_effectifs_fct


"""
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


def rechercherEtu(listeNumeroEtudiants,listeNom,listeMotDePasse,numeroRecherche):
    compteur = len(listeNumeroEtudiants)
    for i in range(compteur):
        if(listeNumeroEtudiants[i]==numeroRecherche):
            return(listeNom[i], listeMotDePasse[i])
    return (-1,-1)

numeroRecherche  = 723156

nom, motdePasse = rechercherEtu(listeNumeroEtudiant, listeNom, listeMotDePasse, numeroRecherche)

if(nom!= -1 and motdePasse!= -1):
    print(nom,motdePasse)
else:
    print("erreur !")
"""
