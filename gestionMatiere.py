import pandas as pd

def lire_donnees_Matiere(fichier_csv):
# Spécifiez le chemin vers votre fichier CSV
    fichier_csv = pd.read_csv('Matieres.csv', header=None)

    tableau = fichier_csv.values

    # Afficher le tableau
    #print(tableau)

    listeMatiereGI = []
    listeDureeMatiereGI = []

    listeMatiereGMI = []
    listeDureeMatiereGMI = []

    listeMatiereGMF = []
    listeDureeMatiereGMF = []

    compteur = len(tableau)
    for i in range(1,compteur):

        listeMatiereGI.append(tableau[i][0])
        listeDureeMatiereGI.append(tableau[i][1])

        listeMatiereGMI.append(tableau[i][2])
        listeDureeMatiereGMI.append(tableau[i][3])

        listeMatiereGMF.append(tableau[i][4])
        listeDureeMatiereGMF.append(tableau[i][5])
    return listeMatiereGI, listeDureeMatiereGI, listeMatiereGMI, listeDureeMatiereGMI, listeMatiereGMF, listeDureeMatiereGMF




