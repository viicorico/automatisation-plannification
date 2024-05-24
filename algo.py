import networkx as nx
import random
import matplotlib.pyplot as plt
import hashlib
import datetime
import pandas as pd

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


def generer_horaires(solution, filiere_matieres_dict, durees_examens, debut,
                     amplitude_horaire, pause_midi, pause):
    horaires = {}
    current_time = debut
    end_time = debut + datetime.timedelta(hours=amplitude_horaire)
    solution_copy = solution.copy()  # Create a copy to avoid modifying the original

    while solution_copy:
        session = min(solution_copy.values())
        horaires[session] = []
        session_start_time = current_time

        # Collecte des examens pour cette session
        exam_times = []
        for matiere, session_assign in list(solution_copy.items()):
            if session_assign == session:
                debut_examen = session_start_time
                fin_examen = debut_examen + datetime.timedelta(minutes=durees_examens[matiere])

                # Ajouter l'examen à la liste de la session
                exam_times.append((debut_examen, fin_examen, matiere))
                del solution_copy[matiere]

        # Ajustement pour la pause déjeuner pour toute la session
        if any(start.time() < datetime.time(12, 0) and end.time() > datetime.time(12, 0) for start, end, _ in exam_times):
            for i, (start, end, matiere) in enumerate(exam_times):
                if start.time() < datetime.time(12, 0):
                    adjusted_start = datetime.datetime.combine(start.date(), datetime.time(13, 0))
                    adjusted_end = adjusted_start + (end - start)
                    exam_times[i] = (adjusted_start, adjusted_end, matiere)

        # Ajustement pour la dernière session de la journée
        if any(end > end_time for _, end, _ in exam_times):
            earliest_start_time = min(start for start, _, _ in exam_times)
            for i, (start, end, matiere) in enumerate(exam_times):
                adjusted_start = earliest_start_time + pause
                adjusted_end = adjusted_start + (end - start)
                exam_times[i] = (adjusted_start, adjusted_end, matiere)

        # Enregistre les horaires ajustés pour cette session
        for start, end, matiere in exam_times:
            horaires[session].append((start.date(), start.time(), end.time(), matiere))
            current_time = end + pause

        # Pause déjeuner
        if current_time.time() >= datetime.time(12, 0) and current_time.time() < datetime.time(13, 0):
            current_time = current_time.replace(hour=13, minute=0)

        max_exam_duration = max(durees_examens[matiere] for _, _, matiere in exam_times)
        # Vérifie si l'amplitude horaire est dépassée pour le jour courant en ajoutant la durée maximale des examens
        if current_time + datetime.timedelta(minutes=max_exam_duration) >= end_time:
            current_time = current_time.replace(hour=debut.hour, minute=debut.minute) + datetime.timedelta(days=1)
            end_time = current_time + datetime.timedelta(hours=amplitude_horaire)

    return horaires



def dessiner_graphe(G, solution):
    pos = nx.spring_layout(G)
    couleurs = [solution[noeud] if noeud in solution else 0 for noeud in G.nodes]
    nx.draw(G, pos, with_labels=True, node_color=couleurs, cmap=plt.cm.tab20, node_size=1500)
    plt.show()


def afficher_emploi_du_temps_par_session(horaires):
    # Créer une liste pour collecter les informations des examens
    emploi_du_temps_data = []

    for session, exams in horaires.items():
        for date, debut, fin, matiere in exams:
            emploi_du_temps_data.append({
                "Session": session + 1,
                "Date": date,
                "Début": debut,
                "Fin": fin,
                "Matière": matiere
            })

    # Convertir la liste en DataFrame
    emploi_du_temps_df = pd.DataFrame(emploi_du_temps_data)
    return emploi_du_temps_df

def afficher_emploi_du_temps_par_session_affichage(horaires):
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


