import pandas as pd

def extraire_filieres_et_matieres(fichier_csv_path):
    # Lire le fichier CSV
    fichier_csv = pd.read_csv(fichier_csv_path, header=None)
    tableau = fichier_csv.values

    # Extraire les noms des filières de la première ligne (colonnes paires)
    filiere_names = tableau[0][::2]

    # Initialiser un dictionnaire pour stocker les matières par filière
    filiere_matieres_dict = {filiere: [] for filiere in filiere_names}

    # Parcourir chaque ligne du tableau à partir de la deuxième ligne
    for i in range(1, len(tableau)):
        matieres_durees = tableau[i]
        for j, filiere in enumerate(filiere_names):
            matiere = matieres_durees[2 * j]
            filiere_matieres_dict[filiere].append(matiere)

    # Convertir le dictionnaire en liste pour correspondre à la structure souhaitée
    filiere_matieres = [[filiere, matieres] for filiere, matieres in filiere_matieres_dict.items()]

    return filiere_matieres

def extraire_matieres_et_durees(fichier_csv_path_fct):
    # Lire le fichier CSV
    fichier_csv_fct = pd.read_csv(fichier_csv_path_fct, header=None)
    tableau_fct = fichier_csv_fct.values

    # Initialiser un dictionnaire pour stocker les matières et leurs durées d'examen
    durees_examens_fct = {}

    # Parcourir chaque ligne du tableau à partir de la première ligne
    for i_fct in range(1, len(tableau_fct)):
        matieres_durees_fct = tableau_fct[i_fct]
        for j_fct in range(0, len(matieres_durees_fct), 2):
            matiere_fct = matieres_durees_fct[j_fct]
            duree_fct = matieres_durees_fct[j_fct + 1]
            durees_examens_fct[matiere_fct] = duree_fct

    return durees_examens_fct
