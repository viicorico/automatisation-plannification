# -*- coding: utf-8 -*-

import datetime
import locale
import os
import sys
import pandas as pd
import random
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from gestionEtudiant import calculer_effectifs_par_filiere
from gestionListeSalle import lire_salles_et_capacites
from gestionMatiere import extraire_matieres_et_durees, extraire_filieres_et_matieres
from gestionEmploieTemps import generer_et_afficher_emploi_du_temps,ecrire_emploi_du_temps_csv,lire_emploi_du_temps_csv,afficher_emploi_du_temps_par_session,generate_time_slots,generate_random_color
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


# Paramètres de l'emploi du temps
date_debut = datetime.datetime(2024, 5, 22, 8, 0)
amplitude_horaire_journaliere = 10  # en heures
pause_dejeuner = datetime.timedelta(hours=1)
pause_entre_examens = datetime.timedelta(minutes=20)

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


# Set locale to French for day names
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')


class ScheduleApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("EDT1.ui", self)
        self.date_debut = datetime.datetime(2024, 5, 22, 8, 0)  # Sauvegarde de la date de début
        self.amplitude_horaire_journaliere = 10
        self.interval_minutes = 5  # Intervalle de 5 minutes
        self.comboBox.currentIndexChanged.connect(self.change_schedule)
        self.comboBoxFiliere.currentIndexChanged.connect(self.filter_schedule)
        self.buttonRechercher.clicked.connect(self.search_student)  # Connecter le bouton de recherche
        self.populate_filiere_combobox()  # Remplir la combobox des filières
        self.populate_schedule()  # Affiche l'emploi du temps
        self.populate_completer()  # Remplir le completer

    def populate_filiere_combobox(self):
        # Ajoute toutes les filières disponibles dans la combobox
        self.comboBoxFiliere.addItem("Toutes")
        for filiere, _ in filiere_matieres:
            self.comboBoxFiliere.addItem(filiere)

    def populate_completer(self):
        # Remplir le completer avec les prénoms des étudiants
        etudiant_csv_path = 'Etudiant.csv'
        if os.path.exists(etudiant_csv_path):
            etudiants_df = pd.read_csv(etudiant_csv_path, header=None)  # Lire sans en-têtes
            self.etudiants_df = etudiants_df  # Stocker le DataFrame des étudiants
            print("Colonnes trouvées dans le fichier CSV:",
                  etudiants_df.columns.tolist())  # Afficher les colonnes pour le débogage
            prenoms = etudiants_df.iloc[:, 0].unique().tolist()  # Utiliser la première colonne par défaut
            completer = QtWidgets.QCompleter(prenoms, self.lineEditPrenom)
            completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
            completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
            self.lineEditPrenom.setCompleter(completer)
        else:
            print(f"Erreur : le fichier '{etudiant_csv_path}' n'existe pas.")

    def populate_schedule(self):
        emploi_du_temps_df = lire_emploi_du_temps_csv('emploi_du_temps.csv')
        if emploi_du_temps_df is None:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Impossible de charger l'emploi du temps.")
            return

        self.filter_schedule()

    def filter_schedule(self):
        filiere_selectionnee = self.comboBoxFiliere.currentText()
        emploi_du_temps_df = lire_emploi_du_temps_csv('emploi_du_temps.csv')
        if emploi_du_temps_df is None:
            return

        if filiere_selectionnee != "Toutes":
            emploi_du_temps_df = emploi_du_temps_df[emploi_du_temps_df["Matière"].isin(
                [matiere for filiere, matieres in filiere_matieres if filiere == filiere_selectionnee for matiere in
                 matieres])]

        start_time = self.date_debut.time()
        end_time = (datetime.datetime.combine(datetime.date.today(), start_time) +
                    datetime.timedelta(hours=self.amplitude_horaire_journaliere)).time()

        time_slots = generate_time_slots(datetime.datetime.combine(datetime.date.today(), start_time),
                                         datetime.datetime.combine(datetime.date.today(), end_time),
                                         self.interval_minutes)

        print("Créneaux horaires générés :", time_slots)

        self.tableWidget.setRowCount(len(time_slots))  # Nombre de créneaux horaires
        unique_dates = emploi_du_temps_df['Date'].unique()
        self.tableWidget.setColumnCount(len(unique_dates))  # Nombre de jours dans le planning

        # Include both date and day of the week in column headers
        column_headers = [f"{date} ({pd.to_datetime(date).strftime('%A')})" for date in unique_dates]
        self.tableWidget.setHorizontalHeaderLabels(column_headers)  # Afficher les dates et jours des sessions

        # Afficher une étiquette toutes les 30 minutes
        self.tableWidget.setVerticalHeaderLabels([time_slots[i] if i % 6 == 0 else '' for i in range(len(time_slots))])

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

        date_to_col = {date: idx for idx, date in enumerate(unique_dates)}

        print("Mapping des dates aux colonnes :", date_to_col)

        time_to_row = {time: index for index, time in enumerate(time_slots)}

        print("Mapping des temps aux lignes :", time_to_row)

        for _, entry in emploi_du_temps_df.iterrows():
            date = entry["Date"]
            start_time = entry["Début"][:5]
            end_time = entry["Fin"][:5]
            subject = entry["Matière"]

            print(f"Traitement de l'entrée : {entry}")

            start_row = time_to_row.get(start_time, None)
            end_row = time_to_row.get(end_time, None)
            col = date_to_col.get(date, None)

            print(f"start_row: {start_row}, end_row: {end_row}, col: {col}")

            if start_row is not None and end_row is not None and col is not None:
                duration_minutes = (datetime.datetime.strptime(end_time, '%H:%M') - datetime.datetime.strptime(
                    start_time, '%H:%M')).seconds // 60
                duration_intervals = duration_minutes // self.interval_minutes

                for row in range(start_row, start_row + duration_intervals):
                    if row == start_row:
                        item = QtWidgets.QTableWidgetItem(f"{subject}\n\n{entry['Session']}")
                    else:
                        item = QtWidgets.QTableWidgetItem("")
                    item.setBackground(QtGui.QColor(subject_colors.get(subject, "#FFFFFF")))
                    item.setFlags(QtCore.Qt.ItemIsEnabled)  # Rendre les cellules non éditables
                    self.tableWidget.setItem(row, col, item)
                    print(f"Élément ajouté à la ligne {row}, colonne {col}")

        # Ajuster la hauteur des lignes pour qu'elles soient proportionnelles aux créneaux de 5 minutes
        for row in range(len(time_slots)):
            self.tableWidget.setRowHeight(row, 10)  # Par exemple, 10 pixels par créneau de 5 minutes

        self.tableWidget.resizeColumnsToContents()  # Resize columns to fit content

    def search_student(self):
        prenom = self.lineEditPrenom.text()
        print(f"Recherche pour le prénom : {prenom}")

        if hasattr(self, 'etudiants_df'):
            etudiants_filtered = self.etudiants_df[self.etudiants_df.iloc[:, 0] == prenom]
            if not etudiants_filtered.empty:
                print(f"Étudiants trouvés pour le prénom {prenom} :")
                print(etudiants_filtered)
                # Afficher les informations pertinentes des étudiants trouvés
            else:
                print(f"Aucun étudiant trouvé pour le prénom {prenom}")
        else:
            print("Erreur : Les données des étudiants ne sont pas chargées.")

    def change_schedule(self):
        self.populate_schedule()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ScheduleApp()
    window.show()
    sys.exit(app.exec_())