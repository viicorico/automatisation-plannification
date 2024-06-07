import pandas as pd

def lire_donnees_Admin(fichier_csv):
    """
    Lire les données des administrateurs à partir d'un fichier CSV et les stocker dans des listes.

    :param fichier_csv: Le chemin vers le fichier CSV contenant les informations des administrateurs.
    :return: Trois listes contenant les numéros d'administrateur, les noms et les mots de passe.
    """
    # Lire le fichier CSV
    fichier_csv = pd.read_csv('Administrateur.csv', header=None)

    # Convertir les données du fichier CSV en tableau numpy
    tableau = fichier_csv.values

    # Afficher le tableau pour vérification (à des fins de débogage)
    print(tableau)

    # Initialiser les listes pour stocker les numéros, noms et mots de passe
    listeNumeroAdmin = []
    listeNom = []
    listeMotDePasse = []

    # Obtenir le nombre de lignes dans le tableau
    compteur = len(tableau)

    # Parcourir chaque ligne du tableau et extraire les données
    for i in range(compteur):
        listeNumeroAdmin.append(tableau[i][1])
        listeNom.append(tableau[i][0])
        listeMotDePasse.append(tableau[i][2])

    # Retourner les listes
    return listeNumeroAdmin, listeNom, listeMotDePasse

def rechercherAdmin(listeNumeroAdmin, listeNom, listeMotDePasse, numeroRecherche):
    """
    Rechercher un administrateur par son numéro dans les listes fournies.

    :param listeNumeroAdmin: Liste des numéros d'administrateur.
    :param listeNom: Liste des noms des administrateurs.
    :param listeMotDePasse: Liste des mots de passe des administrateurs.
    :param numeroRecherche: Le numéro d'administrateur à rechercher.
    :return: Une tuple contenant le nom et le mot de passe de l'administrateur, ou (-1, -1) si non trouvé.
    """
    # Obtenir le nombre d'administrateurs
    compteur = len(listeNumeroAdmin)

    # Parcourir chaque administrateur pour trouver une correspondance
    for i in range(compteur):
        if listeNumeroAdmin[i] == numeroRecherche:
            # Si une correspondance est trouvée, retourner le nom et le mot de passe
            return listeNom[i], listeMotDePasse[i]

    # Si aucune correspondance n'est trouvée, retourner (-1, -1)
    return -1, -1

