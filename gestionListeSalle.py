import pandas as pd

def lire_salles_et_capacites(fichier_csv_path):
    # Lire le fichier CSV
    fichier_csv = pd.read_csv(fichier_csv_path)

    # Initialiser le dictionnaire pour stocker les salles et capacités
    salles_capacites = {}

    # Parcours de chaque ligne du tableau
    for i in range(len(fichier_csv)):
        salle = fichier_csv.iloc[i, 0]  # La salle est dans la première colonne
        capacite = fichier_csv.iloc[i, 1]  # La capacité est dans la deuxième colonne
        salles_capacites[salle] = capacite

    return salles_capacites

