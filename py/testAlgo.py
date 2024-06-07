import datetime
from py.algo import generer_graphe, algorithme_genetique, generer_horaires, afficher_emploi_du_temps_etudiant, get_filiere_etudiant, dessiner_graphe, calculer_effectif_par_session, \
    afficher_emploi_du_temps_par_session_affichage

# Définition des matières par filière
filiere_matieres = [
    ["Informatique", ["Informatique_Mathematiques", "Informatique_Algorithmique", "Informatique_BaseDeDonnees",
                      "Informatique_Reseaux"]],
    ["Biologie", ["Biologie_BiologieCellulaire", "Biologie_histologie", "Biologie_Genetique", "Biologie_Ecologie"]],
    ["Physique",
     ["Physique_PhysiqueQuantique", "Physique_PhysiqueNucleaire", "Physique_Mecanique", "Physique_Electromagnetisme"]],
    ["Mathematique", ["Mathematiques_Analyse", "Algebre", "Mathematiques_Statistiques", "Mathematiques_Optimisation"]],
    ["Chimie",
     ["Chimie_ChimieOrganique", "Chimie_ChimieInorganique", "Chimie_ChimieAnalytique", "Chimie_ChimieTheorique"]],
    ["Linguistique",
     ["Linguistique_Phonologie", "Linguistique_Semantique", "Linguistique_Syntaxe", "Linguistique_Grammaire",
      "Linguistique_Conjugaison"]],
    ["Histoire", ["Histoire_Antiquite", "Histoire_MoyenAge"]],
    ["Economie", ["Economie_Microeconomie"]],
]

# Création d'un dictionnaire des matières associées à chaque filière
filiere_matieres_dict = {matiere: filiere for filiere, matieres in filiere_matieres for matiere in matieres}

# Nombre d'élèves par filière
filiere_effectifs = {
    "Informatique": 30,
    "Biologie": 25,
    "Physique": 20,
    "Mathematique": 15,
    "Chimie": 10,
    "Linguistique": 10,
    "Histoire": 5,
    "Economie": 5
}

# Liste des étudiants et leurs filières
etudiants_dict = {
    "Alice": "Informatique",
    "Bob": "Biologie",
    "Charlie": "Physique",
    "David": "Mathematique",
    "Eve": "Chimie",
    "Faythe": "Linguistique",
    "Grace": "Histoire",
    "Heidi": "Economie"
}

# Durées des examens (en minutes)
durees_examens = {
    "Informatique_Mathematiques": 120,
    "Informatique_Algorithmique": 120,
    "Informatique_BaseDeDonnees": 120,
    "Informatique_Reseaux": 120,
    "Biologie_BiologieCellulaire": 120,
    "Biologie_histologie": 120,
    "Biologie_Genetique": 120,
    "Biologie_Ecologie": 120,
    "Physique_PhysiqueQuantique": 120,
    "Physique_PhysiqueNucleaire": 120,
    "Physique_Mecanique": 120,
    "Physique_Electromagnetisme": 120,
    "Mathematiques_Analyse": 120,
    "Algebre": 120,
    "Mathematiques_Statistiques": 120,
    "Mathematiques_Optimisation": 120,
    "Chimie_ChimieOrganique": 120,
    "Chimie_ChimieInorganique": 120,
    "Chimie_ChimieAnalytique": 120,
    "Chimie_ChimieTheorique": 120,
    "Linguistique_Phonologie": 107,
    "Linguistique_Semantique": 108,
    "Linguistique_Syntaxe": 106,
    "Linguistique_Grammaire": 120,
    "Linguistique_Conjugaison": 115,
    "Histoire_Antiquite": 120,
    "Histoire_MoyenAge": 120,
    "Economie_Microeconomie": 120
}

# Paramètres configurables
date_debut = datetime.datetime(2024, 5, 22, 8, 0)
amplitude_horaire_journaliere = 9  # en heures
pause_dejeuner = datetime.timedelta(hours=1)
pause_entre_examens = datetime.timedelta(minutes=15)

# Salles et capacités
salles_capacites = {
    "Salle_A": 10,
    "Salle_B": 20,
    "Salle_C": 30,
    "Salle_D": 40,
    "Salle_E": 10
}

nb_places_par_session = sum(salles_capacites.values())

# Générer le graphe des matières
graphe = generer_graphe(filiere_matieres)
max_iterations = 1000
population_size = 50
mutation_rate = 0.1
nb_iterations = 100

# Exécuter l'algorithme génétique pour trouver la meilleure solution
meilleure_solution, variance = algorithme_genetique(graphe, max_iterations, population_size, mutation_rate,
                                                    nb_iterations, nb_places_par_session, filiere_effectifs,
                                                    filiere_matieres_dict)

# Générer les horaires
horaires = generer_horaires(meilleure_solution, filiere_matieres_dict, durees_examens, debut=date_debut,
                            amplitude_horaire=amplitude_horaire_journaliere, pause_midi=pause_dejeuner,
                            pause=pause_entre_examens)

# Afficher les résultats
print("Coloration des noeuds :", meilleure_solution)
afficher_emploi_du_temps_par_session_affichage(horaires)

# Vérification des contraintes de places par session
session_effectifs = calculer_effectif_par_session(meilleure_solution, filiere_effectifs, filiere_matieres_dict)
for session, effectif in session_effectifs.items():
    assert effectif <= nb_places_par_session, f"La session {session} dépasse le nombre de places autorisées."

print("Variance de la solution :", variance)

# Debug: Afficher les effectifs par session et les détails de la variance
print("Effectifs par session:", session_effectifs)
moyenne_effectifs = sum(session_effectifs.values()) / len(session_effectifs)
print("Moyenne des effectifs par session:", moyenne_effectifs)

# Affichage de l'emploi du temps pour un étudiant spécifique
etudiant = "Bob"  # Changez cette valeur pour l'étudiant souhaité
filiere = get_filiere_etudiant(etudiants_dict, etudiant)
if filiere:
    afficher_emploi_du_temps_etudiant(horaires, filiere, filiere_matieres_dict)
else:
    print(f"Filière pour l'étudiant {etudiant} introuvable.")
dessiner_graphe(graphe, meilleure_solution)
