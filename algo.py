import networkx as nx
import random
import matplotlib.pyplot as plt
import hashlib
import datetime


def generer_graphe(filiere_matieres):
    G = nx.Graph()
    for filiere, matieres in filiere_matieres:
        for matiere in matieres:
            G.add_node(matiere)
    for filiere, matieres in filiere_matieres:
        for i in range(len(matieres)):
            for j in range(i + 1, len(matieres)):
                G.add_edge(matieres[i], matieres[j])
    return G


def solution_initiale(G):
    coloration = nx.coloring.greedy_color(G, strategy="largest_first")
    return coloration


def calculer_effectif_par_session(solution, filiere_effectifs, filiere_matieres_dict):
    session_effectifs = {}
    for matiere, session in solution.items():
        filiere = filiere_matieres_dict[matiere]
        effectif = filiere_effectifs[filiere]
        if session not in session_effectifs:
            session_effectifs[session] = 0
        session_effectifs[session] += effectif
    return session_effectifs


def est_solution_valide(solution, G, nb_places_par_session, filiere_effectifs, filiere_matieres_dict):
    session_effectifs = calculer_effectif_par_session(solution, filiere_effectifs, filiere_matieres_dict)
    for u, v in G.edges:
        if solution[u] == solution[v]:
            return False
    for effectif in session_effectifs.values():
        if effectif > nb_places_par_session:
            return False
    return True


def ajuster_sessions(solution, nb_places_par_session, filiere_effectifs, filiere_matieres_dict):
    session_effectifs = calculer_effectif_par_session(solution, filiere_effectifs, filiere_matieres_dict)

    max_session = max(session_effectifs.keys(), default=-1) + 1
    for session, effectif in list(session_effectifs.items()):
        while effectif > nb_places_par_session:
            for matiere in list(solution.keys()):
                if solution[matiere] == session and effectif > nb_places_par_session:
                    solution[matiere] = max_session
                    filiere = filiere_matieres_dict[matiere]
                    effectif -= filiere_effectifs[filiere]
                    session_effectifs[max_session] = session_effectifs.get(max_session, 0) + filiere_effectifs[filiere]
                    if effectif <= nb_places_par_session:
                        break
            session_effectifs[session] = effectif
            max_session += 1

    return solution


def generer_voisinage(solution, nb_places_par_session, filiere_effectifs, filiere_matieres_dict):
    voisinage = []
    for _ in range(len(solution)):
        examen1, examen2 = random.sample(list(solution.keys()), 2)
        voisin = solution.copy()
        voisin[examen1], voisin[examen2] = voisin[examen2], voisin[examen1]
        voisin = ajuster_sessions(voisin, nb_places_par_session, filiere_effectifs, filiere_matieres_dict)
        voisinage.append(voisin)
    return voisinage


def calculer_variance_examen(solution):
    sessions = set(solution.values())
    effectifs = {session: list(solution.values()).count(session) for session in sessions}
    moyenne = sum(effectifs.values()) / len(sessions)
    variance = sum([(effectif - moyenne) ** 2 for effectif in effectifs.values()]) / len(sessions)
    return variance


def hash_solution(solution):
    hash_object = hashlib.sha256(str(solution).encode())
    return hash_object.hexdigest()


def algorithme_genetique(G, max_iterations, population_size, mutation_rate, nb_iterations, nb_places_par_session,
                         filiere_effectifs, filiere_matieres_dict):
    meilleures_solutions = {}

    for _ in range(nb_iterations):
        population = [
            ajuster_sessions(solution_initiale(G), nb_places_par_session, filiere_effectifs, filiere_matieres_dict) for
            _ in range(population_size)]
        meilleure_solution = population[0]
        meilleure_variance = calculer_variance_examen(meilleure_solution)
        meilleure_solution_hash = hash_solution(meilleure_solution)

        iterations_sans_amelioration = 0

        while iterations_sans_amelioration < max_iterations:
            population = selectionner_parents(population)
            enfants = croiser_parents(population, nb_places_par_session, filiere_effectifs, filiere_matieres_dict)
            population.extend(enfants)
            population = muter_population(population, mutation_rate, nb_places_par_session, filiere_effectifs,
                                          filiere_matieres_dict)

            for solution in population:
                solution = ajuster_sessions(solution, nb_places_par_session, filiere_effectifs, filiere_matieres_dict)
                if not est_solution_valide(solution, G, nb_places_par_session, filiere_effectifs,
                                           filiere_matieres_dict):
                    continue
                variance_solution = calculer_variance_examen(solution)
                solution_hash = hash_solution(solution)
                if solution_hash not in meilleures_solutions:
                    meilleures_solutions[solution_hash] = {'solution': solution, 'variance': variance_solution}
                else:
                    if variance_solution < meilleures_solutions[solution_hash]['variance']:
                        meilleures_solutions[solution_hash]['solution'] = solution
                        meilleures_solutions[solution_hash]['variance'] = variance_solution
                        meilleure_solution = solution
                        meilleure_variance = variance_solution
                        meilleure_solution_hash = solution_hash
                        iterations_sans_amelioration = 0
                    else:
                        iterations_sans_amelioration += 1

        meilleures_solutions[meilleure_solution_hash] = {'solution': meilleure_solution, 'variance': meilleure_variance}

    meilleure_solution_globale = min(meilleures_solutions.values(), key=lambda x: x['variance'])['solution']
    meilleure_variance_globale = min(meilleures_solutions.values(), key=lambda x: x['variance'])['variance']

    return meilleure_solution_globale, meilleure_variance_globale


def selectionner_parents(population):
    return random.choices(population, k=len(population))


def croiser_parents(population, nb_places_par_session, filiere_effectifs, filiere_matieres_dict):
    enfants = []
    for _ in range(len(population)):
        parent1, parent2 = random.sample(population, 2)
        cut_point = random.randint(0, len(parent1))
        enfant = {key: parent1[key] if idx < cut_point else parent2[key] for idx, key in enumerate(parent1)}
        enfant = ajuster_sessions(enfant, nb_places_par_session, filiere_effectifs, filiere_matieres_dict)
        enfants.append(enfant)
    return enfants


def muter_population(population, mutation_rate, nb_places_par_session, filiere_effectifs, filiere_matieres_dict):
    for solution in population:
        if random.random() < mutation_rate:
            examen1, examen2 = random.sample(list(solution.keys()), 2)
            solution[examen1], solution[examen2] = solution[examen2], solution[examen1]
            solution = ajuster_sessions(solution, nb_places_par_session, filiere_effectifs, filiere_matieres_dict)
    return population


def generer_horaires(solution, filiere_matieres_dict, durees_examens, debut=datetime.datetime(2024, 5, 22, 8, 0),
                     amplitude_horaire=9, pause_midi=datetime.timedelta(hours=1), pause=datetime.timedelta(minutes=15)):
    horaires = {}
    current_time = debut
    end_time = debut + datetime.timedelta(hours=amplitude_horaire)
    solution_copy = solution.copy()  # Create a copy to avoid modifying the original

    while solution_copy:
        session = min(solution_copy.values())
        horaires[session] = []
        session_start_time = current_time

        # Ajustement pour la première session de la journée
        exam_times = []
        for matiere, session_assign in list(solution_copy.items()):
            if session_assign == session:
                debut_examen = session_start_time
                fin_examen = session_start_time + datetime.timedelta(minutes=durees_examens[matiere])
                exam_times.append((debut_examen, fin_examen, matiere))
                del solution_copy[matiere]

        if session_start_time.time() == debut.time():
            latest_end_time = max(fin for _, fin, _ in exam_times)
            for i, (start, end, matiere) in enumerate(exam_times):
                adjusted_start = latest_end_time - (end - start)
                exam_times[i] = (adjusted_start, latest_end_time, matiere)

        # Ajustement pour la dernière session de la journée
        if session_start_time.time() >= (end_time - datetime.timedelta(hours=1)).time():
            earliest_start_time = min(start for start, _, _ in exam_times)
            for i, (start, end, matiere) in enumerate(exam_times):
                adjusted_end = earliest_start_time + (end - start)
                exam_times[i] = (earliest_start_time, adjusted_end, matiere)

        # Enregistre les horaires ajustés
        for start, end, matiere in exam_times:
            horaires[session].append((start.date(), start.time(), end.time(), matiere))
            current_time = end + pause

        # Pause déjeuner
        if current_time.time() >= datetime.time(12, 0) and current_time.time() < datetime.time(13, 0):
            current_time = current_time.replace(hour=13, minute=0)

        # Vérifie si l'amplitude horaire est dépassée pour le jour courant
        if current_time.time() >= end_time.time():
            current_time = current_time.replace(hour=debut.hour, minute=debut.minute) + datetime.timedelta(days=1)
            end_time = current_time + datetime.timedelta(hours=amplitude_horaire)

    return horaires


def dessiner_graphe(G, solution):
    pos = nx.spring_layout(G)
    couleurs = [solution[noeud] if noeud in solution else 0 for noeud in G.nodes]
    nx.draw(G, pos, with_labels=True, node_color=couleurs, cmap=plt.cm.tab20, node_size=1500)
    plt.show()


def afficher_emploi_du_temps_par_session(horaires):
    for session, exams in horaires.items():
        print(f"\nSession {session + 1}:")
        for date, debut, fin, matiere in exams:
            print(f"{date} {debut} - {fin}: {matiere}")


def afficher_emploi_du_temps_etudiant(horaires, filiere, filiere_matieres_dict):
    print(f"Emploi du temps pour la filière {filiere}:")
    for session, exams in horaires.items():
        for date, debut, fin, matiere in exams:
            if filiere_matieres_dict[matiere] == filiere:
                print(f"{date} {debut} - {fin}: {matiere}")


def get_filiere_etudiant(etudiants_dict, etudiant):
    return etudiants_dict.get(etudiant, None)


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

filiere_matieres_dict = {matiere: filiere for filiere, matieres in filiere_matieres for matiere in matieres}

# nombre d'élèves par filière
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

graphe = generer_graphe(filiere_matieres)
max_iterations = 1000
population_size = 50
mutation_rate = 0.1
nb_iterations = 100

meilleure_solution, variance = algorithme_genetique(graphe, max_iterations, population_size, mutation_rate,
                                                    nb_iterations, nb_places_par_session, filiere_effectifs,
                                                    filiere_matieres_dict)

# Générer les horaires
horaires = generer_horaires(meilleure_solution, filiere_matieres_dict, durees_examens, debut=date_debut,
                            amplitude_horaire=amplitude_horaire_journaliere, pause_midi=pause_dejeuner,
                            pause=pause_entre_examens)

# Vérification et affichage des résultats
print("Coloration des noeuds :", meilleure_solution)
afficher_emploi_du_temps_par_session(horaires)

# Vérification des contraintes de places par session
session_effectifs = calculer_effectif_par_session(meilleure_solution, filiere_effectifs, filiere_matieres_dict)
for session, effectif in session_effectifs.items():
    assert effectif <= nb_places_par_session, f"La session {session} dépasse le nombre de places autorisées."

dessiner_graphe(graphe, meilleure_solution)

print("Variance de la solution :", variance)

# Debug: Print session effectifs and variance details
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