# -*- coding: utf-8 -*-

import datetime
import os
import sys
import pandas as pd
import random
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from algo import generer_graphe, algorithme_genetique, generer_horaires
from gestionEtudiant import calculer_effectifs_par_filiere
from gestionListeSalle import lire_salles_et_capacites
from gestionMatiere import extraire_matieres_et_durees, extraire_filieres_et_matieres

# Réglages de l'affichage de pandas
pd.set_option('display.max_columns', None)  # Afficher toutes les colonnes
pd.set_option('display.max_rows', None)  # Afficher toutes les lignes
pd.set_option('display.width', None)  # Ne pas tronquer la largeur de l'affichage

# Exemple d'utilisation
fichier_csv_path = 'Etudiant.csv'
filiere_effectifs = calculer_effectifs_par_filiere(fichier_csv_path)
fichier_csv_path = 'ListeSalle.csv'
salles_capacites = lire_salles_et_capacites(fichier_csv_path)
fichier_csv_path = 'Matieres.csv'
durees_examens = extraire_matieres_et_durees(fichier_csv_path)
filiere_matieres = extraire_filieres_et_matieres(fichier_csv_path)

print("Liste des matières extraites :")
for filiere, matieres in filiere_matieres:
    print(f"{filiere} : {matieres}")

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
    return slots

def generate_random_color(existing_colors):
    """Génère une couleur aléatoire qui est suffisamment différente des couleurs existantes."""
    while True:
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        if color not in existing_colors:
            return color

# Paramètres de l'emploi du temps
date_debut = datetime.datetime(2024, 5, 22, 8, 0)
amplitude_horaire_journaliere = 9  # en heures
pause_dejeuner = datetime.timedelta(hours=1)
pause_entre_examens = datetime.timedelta(minutes=15)

# Générer l'emploi du temps
emploi_du_temps_df = generer_et_afficher_emploi_du_temps(filiere_matieres, filiere_effectifs, durees_examens,
                                                         date_debut, amplitude_horaire_journaliere, pause_dejeuner,
                                                         pause_entre_examens, salles_capacites)
print("Colonnes du DataFrame généré : ",
      emploi_du_temps_df.columns.tolist())  # Afficher les colonnes du DataFrame généré

# Chemin du fichier CSV
file_path = 'emploi_du_temps.csv'

# Écrire l'emploi du temps dans le fichier CSV
if emploi_du_temps_df is not None and isinstance(emploi_du_temps_df, pd.DataFrame):
    ecrire_emploi_du_temps_csv(emploi_du_temps_df, file_path)
else:
    print("Erreur : l'emploi du temps généré est vide ou n'est pas un DataFrame.")

# Lire l'emploi du temps depuis le fichier CSV
emploi_du_temps_lu_df = lire_emploi_du_temps_csv(file_path)
print("Colonnes du DataFrame lu : ", emploi_du_temps_lu_df.columns.tolist())  # Afficher les colonnes du DataFrame lu

if emploi_du_temps_lu_df is not None:
    print("Données de l'emploi du temps lues avec succès :")
    print(emploi_du_temps_lu_df)
else:
    print("Erreur : impossible de lire les données de l'emploi du temps.")

# PyQt5 Schedule Display Application

class ScheduleApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("EDT1.ui", self)
        self.date_debut = date_debut  # Sauvegarde de la date de début
        self.amplitude_horaire_journaliere = amplitude_horaire_journaliere
        self.interval_minutes = 15  # Intervalle de 15 minutes
        self.populate_schedule()  # Affiche l'emploi du temps

        self.comboBox.currentIndexChanged.connect(self.change_schedule)

    def populate_schedule(self):
        emploi_du_temps_df = lire_emploi_du_temps_csv('emploi_du_temps.csv')
        if emploi_du_temps_df is None:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Impossible de charger l'emploi du temps.")
            return

        # Vérifier que la colonne 'Matière' existe
        if 'Matière' not in emploi_du_temps_df.columns:
            QtWidgets.QMessageBox.warning(self, "Erreur",
                                          f"Colonne 'Matière' non trouvée. Colonnes disponibles : {emploi_du_temps_df.columns.tolist()}")
            return

        start_time = self.date_debut.time()
        end_time = (datetime.datetime.combine(datetime.date.today(), start_time) +
                    datetime.timedelta(hours=self.amplitude_horaire_journaliere)).time()

        time_slots = generate_time_slots(datetime.datetime.combine(datetime.date.today(), start_time),
                                         datetime.datetime.combine(datetime.date.today(), end_time),
                                         self.interval_minutes)

        print("Créneaux horaires générés :", time_slots)

        self.tableWidget.setRowCount(len(time_slots))  # Nombre de créneaux horaires
        self.tableWidget.setColumnCount(6)  # 6 jours de la semaine
        self.tableWidget.setHorizontalHeaderLabels(['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'])
        self.tableWidget.setVerticalHeaderLabels(time_slots)

        # Clear existing data
        self.tableWidget.clearContents()

        # Générer des couleurs aléatoires pour chaque matière
        subject_colors = {}
        existing_colors = set()

        for matiere in emploi_du_temps_df['Matière'].unique():
            color = generate_random_color(existing_colors)
            subject_colors[matiere] = color
            existing_colors.add(color)

        print("Couleurs générées pour chaque matière :", subject_colors)

        date_to_col = {}
        for i in range(6):
            date_to_col[(self.date_debut + datetime.timedelta(days=i)).strftime("%Y-%m-%d")] = i

        print("Mapping des dates aux colonnes :", date_to_col)

        time_to_row = {time: index for index, time in enumerate(time_slots)}

        print("Mapping des temps aux lignes :", time_to_row)

        for _, entry in emploi_du_temps_df.iterrows():
            date = entry["Date"]
            start_time = entry["Début"][:5]  # Ajustement du format de l'heure
            end_time = entry["Fin"][:5]  # Ajustement du format de l'heure
            subject = entry["Matière"]

            print(f"Traitement de l'entrée : {entry}")

            start_row = time_to_row.get(start_time, None)
            end_row = time_to_row.get(end_time, None)
            col = date_to_col.get(date, None)

            print(f"start_row: {start_row}, end_row: {end_row}, col: {col}")

            if start_row is not None and end_row is not None and col is not None:
                for row in range(start_row, end_row):
                    if row == start_row:
                        item = QtWidgets.QTableWidgetItem(f"{subject}\n\n{entry['Session']}")
                    else:
                        item = QtWidgets.QTableWidgetItem("")
                    item.setBackground(QtGui.QColor(subject_colors.get(subject, "#FFFFFF")))
                    self.tableWidget.setItem(row, col, item)
                    print(f"Élément ajouté à la ligne {row}, colonne {col}")

        self.tableWidget.resizeRowsToContents()  # Resize rows to fit content
        self.tableWidget.resizeColumnsToContents()  # Resize columns to fit content

    def change_schedule(self):
        self.populate_schedule()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ScheduleApp()
    window.show()
    sys.exit(app.exec_())
