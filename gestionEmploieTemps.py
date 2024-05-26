from algo import generer_graphe, algorithme_genetique, generer_horaires
import datetime
import os
import pandas as pd
import random

# Fonction pour générer et afficher l'emploi du temps
def generer_et_afficher_emploi_du_temps(filiere_matieres, filiere_effectifs, durees_examens, date_debut,
                                        amplitude_horaire_journaliere, pause_dejeuner, pause_entre_examens,
                                        salles_capacites, max_iterations=1000, population_size=50, mutation_rate=0.1,
                                        nb_iterations=100):
    # Créer un dictionnaire de matières à partir des filières
    filiere_matieres_dict = {matiere: filiere for filiere, matieres in filiere_matieres for matiere in matieres}
    # Calculer le nombre total de places disponibles par session
    nb_places_par_session = sum(salles_capacites.values())
    # Générer le graphe des matières
    graphe = generer_graphe(filiere_matieres)
    # Appliquer l'algorithme génétique pour trouver la meilleure solution
    meilleure_solution, variance = algorithme_genetique(graphe, max_iterations, population_size, mutation_rate,
                                                        nb_iterations, nb_places_par_session, filiere_effectifs,
                                                        filiere_matieres_dict)
    # Générer les horaires à partir de la solution
    horaires = generer_horaires(meilleure_solution, filiere_matieres_dict, durees_examens, debut=date_debut,
                                amplitude_horaire=amplitude_horaire_journaliere, pause_midi=pause_dejeuner,
                                pause=pause_entre_examens)
    # Afficher l'emploi du temps par session
    emploi_du_temps_df = afficher_emploi_du_temps_par_session(horaires)

    if not isinstance(emploi_du_temps_df, pd.DataFrame):
        emploi_du_temps_df = pd.DataFrame(emploi_du_temps_df)

    return emploi_du_temps_df

# Fonction pour écrire l'emploi du temps dans un fichier CSV
def ecrire_emploi_du_temps_csv(df, file_path):
    df.to_csv(file_path, index=False)

# Fonction pour lire l'emploi du temps depuis un fichier CSV
def lire_emploi_du_temps_csv(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return None

# Fonction pour afficher l'emploi du temps par session
def afficher_emploi_du_temps_par_session(horaires):
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

    emploi_du_temps_df = pd.DataFrame(emploi_du_temps_data)
    return emploi_du_temps_df

# Fonction pour générer des créneaux horaires
def generate_time_slots(start_time, end_time, interval_minutes):
    slots = []
    current_time = start_time
    while current_time < end_time:
        slots.append(current_time.strftime('%H:%M'))
        current_time += datetime.timedelta(minutes=interval_minutes)
    slots.append(end_time.strftime('%H:%M'))
    return slots

# Fonction pour générer une couleur aléatoire
def generate_random_color(existing_colors):
    while True:
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        if color not in existing_colors:
            return color

# Fonction pour lire les données des étudiants depuis un fichier CSV
def lire_etudiants_csv(file_path):
    df = pd.read_csv(file_path, usecols=[0, 3], header=None, names=["Nom", "Filière"])
    etudiants_dict = {row["Nom"]: row["Filière"] for index, row in df.iterrows()}
    return etudiants_dict

# Fonction pour lire les sessions et les matières depuis un fichier CSV
def lire_sessions_et_matieres(fichier):
    df = pd.read_csv(fichier)
    return df[['Session', 'Matière']]

# Fonction pour lire les étudiants depuis un fichier CSV
def lire_etudiants(fichier):
    df = pd.read_csv(fichier)
    return df.iloc[:, [0, 3]]

# Fonction pour lire les matières par filière depuis un fichier CSV
def lire_matieres_par_filiere(fichier):
    df = pd.read_csv(fichier)
    filieres = df.columns[::2]
    matieres = {filiere: df[filiere].dropna().tolist() for filiere in filieres}
    return matieres

# Fonction pour lire les salles et leurs capacités depuis un fichier CSV
def lire_salles_et_capacites(fichier):
    df = pd.read_csv(fichier)
    return df

# Fonction pour assigner les salles aux étudiants pour chaque matière et session
def assigner_salles_aux_etudiants(etudiants_file, sessions_file, matieres_file, salles_file, nom_etudiant):
    etudiants = lire_etudiants(etudiants_file)
    sessions = lire_sessions_et_matieres(sessions_file)
    matieres = lire_matieres_par_filiere(matieres_file)
    salles = lire_salles_et_capacites(salles_file)

    etudiants.columns = ['Nom', 'Filiere']
    all_combinations = []

    for filiere, matieres_list in matieres.items():
        etudiants_filiere = etudiants[etudiants['Filiere'] == filiere]
        for matiere in matieres_list:
            sessions_matiere = sessions[sessions['Matière'] == matiere]
            if not sessions_matiere.empty:
                for session in sessions_matiere.itertuples():
                    for etudiant in etudiants_filiere.itertuples():
                        all_combinations.append({
                            'Nom': etudiant.Nom,
                            'Filiere': filiere,
                            'Matière': matiere,
                            'Session': session.Session
                        })

    etudiant_matiere = pd.DataFrame(all_combinations)
    salle_capacite = salles.set_index('Salles')['capacite'].to_dict()
    room_assignments = []

    for session, group in etudiant_matiere.groupby('Session'):
        salle_utilisation = {salle: 0 for salle in salle_capacite.keys()}
        for index, row in group.iterrows():
            subject = row['Matière']
            student_name = row['Nom']

            assigned = False
            for salle, capacite in salle_capacite.items():
                if salle_utilisation[salle] < capacite / 2:
                    place_num = salle_utilisation[salle] * 2 + 1
                    room_assignments.append({
                        'Étudiant': student_name,
                        'Session': session,
                        'Matière': subject,
                        'Salle': salle,
                        'Place': place_num,
                        'Capacité': capacite
                    })
                    salle_utilisation[salle] += 1
                    assigned = True
                    break

    room_assignments_df = pd.DataFrame(room_assignments)
    room_assignments_df['Place'] = room_assignments_df.groupby('Salle')['Place'].transform(lambda x: random.sample(list(x), len(x)))
    assignments_etudiant = filtrer_par_nom(room_assignments_df, nom_etudiant)

    return assignments_etudiant

# Fonction pour filtrer les assignments par nom d'étudiant
def filtrer_par_nom(df, nom):
    return df[df['Étudiant'] == nom]
