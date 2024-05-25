from algo import generer_graphe, algorithme_genetique, generer_horaires
import datetime
import os
import sys
import pandas as pd
import random
def generer_et_afficher_emploi_du_temps(filiere_matieres, filiere_effectifs, durees_examens, date_debut,
                                        amplitude_horaire_journaliere, pause_dejeuner, pause_entre_examens,
                                        salles_capacites, max_iterations=1000, population_size=50, mutation_rate=0.1,
                                        nb_iterations=100):
    filiere_matieres_dict = {matiere: filiere for filiere, matieres in filiere_matieres for matiere in matieres}
    nb_places_par_session = sum(salles_capacites.values())
    graphe = generer_graphe(filiere_matieres)
    meilleure_solution, variance = algorithme_genetique(graphe, max_iterations, population_size, mutation_rate,
                                                        nb_iterations, nb_places_par_session, filiere_effectifs,
                                                        filiere_matieres_dict)
    horaires = generer_horaires(meilleure_solution, filiere_matieres_dict, durees_examens, debut=date_debut,
                                amplitude_horaire=amplitude_horaire_journaliere, pause_midi=pause_dejeuner,
                                pause=pause_entre_examens)
    emploi_du_temps_df = afficher_emploi_du_temps_par_session(horaires)

    # Ensure emploi_du_temps_df is a DataFrame
    if not isinstance(emploi_du_temps_df, pd.DataFrame):
        emploi_du_temps_df = pd.DataFrame(emploi_du_temps_df)

    return emploi_du_temps_df
def ecrire_emploi_du_temps_csv(df, file_path):
    """Écrit le DataFrame dans un fichier CSV existant ou crée un nouveau fichier si nécessaire."""
    print("Écriture du DataFrame dans le fichier CSV...")
    print("Colonnes du DataFrame à écrire :", df.columns.tolist())
    df.to_csv(file_path, index=False)
    print(f"Le contenu du fichier '{file_path}' a été mis à jour avec succès.")

def lire_emploi_du_temps_csv(file_path):
    """Lit le fichier CSV et renvoie un DataFrame."""
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        print("Données lues du fichier CSV :", df.head())
        print("Colonnes lues du fichier CSV :", df.columns.tolist())
        return df
    else:
        print(f"Erreur : le fichier '{file_path}' n'existe pas.")
        return None

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
    print("Colonnes du DataFrame généré :", emploi_du_temps_df.columns.tolist())
    print("Aperçu du DataFrame généré :", emploi_du_temps_df.head())
    return emploi_du_temps_df

def generate_time_slots(start_time, end_time, interval_minutes):
    """Génère une liste de créneaux horaires entre start_time et end_time avec l'intervalle donné."""
    slots = []
    current_time = start_time
    while current_time < end_time:
        slots.append(current_time.strftime('%H:%M'))
        current_time += datetime.timedelta(minutes=interval_minutes)
    slots.append(end_time.strftime('%H:%M'))
    return slots

def generate_random_color(existing_colors):
    """Génère une couleur aléatoire qui est suffisamment différente des couleurs existantes."""
    while True:
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        if color not in existing_colors:
            return color
