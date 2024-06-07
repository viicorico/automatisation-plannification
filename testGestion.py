from gestionEtudiant import calculer_effectifs_par_filiere
from gestionListeSalle import lire_salles_et_capacites
from gestionMatiere import extraire_filieres_et_matieres, extraire_matieres_et_durees

# Extraction des filières et des matières depuis le fichier CSV
fichier_csv_path = 'Matieres.csv'
filiere_matieres = extraire_filieres_et_matieres(fichier_csv_path)

# Affichage de la structure des filières et des matières
print("\nStructure finale :")
print(filiere_matieres)

# Extraction des durées d'examen des matières depuis le fichier CSV
durees_examens = extraire_matieres_et_durees(fichier_csv_path)

# Affichage du dictionnaire des matières avec leurs durées d'examen
print("Dictionnaire des matières avec leurs durées d'examen :")
print(durees_examens)

# Extraction des capacités des salles depuis le fichier CSV
fichier_csv_path = 'ListeSalle.csv'
salles_capacites = lire_salles_et_capacites(fichier_csv_path)

# Affichage du dictionnaire des salles avec leurs capacités
print("Dictionnaire des salles avec leurs capacités :")
print(salles_capacites)

# Calcul des effectifs par filière depuis le fichier CSV
fichier_csv_path_fct = 'Etudiant.csv'
filiere_effectifs_fct = calculer_effectifs_par_filiere(fichier_csv_path_fct)

# Affichage du dictionnaire des effectifs par filière
print("Effectifs par filière :")
print(filiere_effectifs_fct)
