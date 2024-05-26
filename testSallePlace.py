# Supposons que les fichiers CSV sont nommés en conséquence
from gestionEmploieTemps import assigner_salles_aux_etudiants
from tabulate import tabulate
etudiants_file = 'Etudiant.csv'
sessions_file = 'emploi_du_temps.csv'
matieres_file = 'Matieres.csv'
salles_file = 'listeSalle.csv'

# Nom de l'étudiant à filtrer
nom_etudiant = "BELHAJ Wael"

# Attribuer les salles et les places aux étudiants pour chaque session et filtrer par nom d'étudiant
assignments_etudiant = assigner_salles_aux_etudiants(etudiants_file, sessions_file, matieres_file, salles_file, nom_etudiant)

# Afficher les affectations pour l'étudiant spécifié
print(tabulate(assignments_etudiant, headers='keys', tablefmt='psql'))
