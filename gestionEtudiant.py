import pandas as pd

def calculer_effectifs_par_filiere(fichier_csv_path_fct):
    # Lire le fichier CSV
    fichier_csv_fct = pd.read_csv(fichier_csv_path_fct, header=None)

    # Initialiser le dictionnaire pour stocker les effectifs par filière
    filiere_effectifs_fct = {}

    # Parcours de chaque ligne du tableau à partir de la première ligne
    for i_fct in range(len(fichier_csv_fct)):
        filiere_fct = fichier_csv_fct.iloc[i_fct, -1]  # La filière est dans la dernière colonne du fichier étudiant
        if filiere_fct in filiere_effectifs_fct:
            filiere_effectifs_fct[filiere_fct] += 1
        else:
            filiere_effectifs_fct[filiere_fct] = 1

    return filiere_effectifs_fct


