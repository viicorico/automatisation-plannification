# Exemple d'utilisation
from gestionEtudiant import calculer_effectifs_par_filiere
from gestionListeSalle import lire_salles_et_capacites
from gestionMatiere import extraire_filieres_et_matieres, extraire_matieres_et_durees

fichier_csv_path = 'Matieres.csv'
filiere_matieres = extraire_filieres_et_matieres(fichier_csv_path)


# Exemple d'affichage sous forme de la structure demandée
print("\nStructure finale :")
print(filiere_matieres)

fichier_csv_path = 'Matieres.csv'
durees_examens = extraire_matieres_et_durees(fichier_csv_path)

# Affichage du dictionnaire pour vérification
print("Dictionnaire des matières avec leurs durées d'examen :")
print(durees_examens)

# Exemple d'utilisation
fichier_csv_path = 'ListeSalle.csv'
salles_capacites = lire_salles_et_capacites(fichier_csv_path)

# Affichage du dictionnaire pour vérification
print("Dictionnaire des salles avec leurs capacités :")
print(salles_capacites)
# Exemple d'utilisation
fichier_csv_path_fct = 'Etudiant.csv'
filiere_effectifs_fct = calculer_effectifs_par_filiere(fichier_csv_path_fct)

# Affichage du dictionnaire pour vérification
print("Effectifs par filière :")
print(filiere_effectifs_fct)