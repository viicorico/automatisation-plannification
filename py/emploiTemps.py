import datetime
import locale
import os
import sys
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi

from py.algo import get_filiere_etudiant
from gestionEtudiant import calculer_effectifs_par_filiere
from gestionListeSalle import lire_salles_et_capacites
from gestionMatiere import extraire_matieres_et_durees, extraire_filieres_et_matieres
from gestionEmploieTemps import generer_et_afficher_emploi_du_temps, ecrire_emploi_du_temps_csv, \
    lire_emploi_du_temps_csv, generate_time_slots, generate_random_color, \
    lire_etudiants_csv, assigner_salles_aux_etudiants
# Configurer la locale en français pour les noms de jours
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
# Réglages de l'affichage de pandas pour voir toutes les colonnes et lignes
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

# Chargement des fichiers CSV
fichier_csv_path = 'Etudiant.csv'
filiere_effectifs = calculer_effectifs_par_filiere(fichier_csv_path)
fichier_csv_path_salles = 'ListeSalle.csv'
salles_capacites = lire_salles_et_capacites(fichier_csv_path_salles)
fichier_csv_path_matieres = 'Matieres.csv'
durees_examens = extraire_matieres_et_durees(fichier_csv_path_matieres)
filiere_matieres = extraire_filieres_et_matieres(fichier_csv_path_matieres)

# Paramètres de l'emploi du temps
date_debut = datetime.datetime(2024, 5, 23, 8, 0)
amplitude_horaire_journaliere = 10
pause_dejeuner = datetime.timedelta(hours=1)
pause_entre_examens = datetime.timedelta(minutes=20)

# Génération de l'emploi du temps
emploi_du_temps_df = generer_et_afficher_emploi_du_temps(filiere_matieres, filiere_effectifs, durees_examens,
                                                         date_debut, amplitude_horaire_journaliere, pause_dejeuner,
                                                         pause_entre_examens, salles_capacites)

# Chemin du fichier CSV
file_path = 'emploi_du_temps.csv'

# Écriture de l'emploi du temps dans un fichier CSV
if emploi_du_temps_df is not None and isinstance(emploi_du_temps_df, pd.DataFrame):
    ecrire_emploi_du_temps_csv(emploi_du_temps_df, file_path)

# Lecture de l'emploi du temps depuis le fichier CSV
emploi_du_temps_lu_df = lire_emploi_du_temps_csv(file_path)

# Pré-assignation des salles à tous les étudiants et écriture dans un fichier CSV
etudiants_df = pd.read_csv(fichier_csv_path, header=None)
assignments_list = []

for prenom in etudiants_df.iloc[:, 0].unique():
    assignments_etudiant = assigner_salles_aux_etudiants(fichier_csv_path, file_path, fichier_csv_path_matieres,
                                                         fichier_csv_path_salles, prenom)
    assignments_etudiant['Prenom'] = prenom
    assignments_list.append(assignments_etudiant)

all_assignments_df = pd.concat(assignments_list, ignore_index=True)
preassigned_rooms_file = '../csv/Salle_Place.csv'
all_assignments_df.to_csv(preassigned_rooms_file, index=False)


etudiants_file = 'Etudiant.csv'
sessions_file = 'emploi_du_temps.csv'
matieres_file = 'Matieres.csv'
salles_file = 'listeSalle.csv'



# Application PyQt5 pour l'affichage de l'emploi du temps
class ScheduleApp(QtWidgets.QMainWindow):
    def __init__(self):
        """Initialise la fenêtre principale de l'application."""
        super().__init__()
        loadUi("EDT1.ui", self)
        self.setWindowIcon(QIcon('../img/logo.ico'))
        self.date_debut = datetime.datetime(2024, 5, 22, 8, 0)
        self.amplitude_horaire_journaliere = 10
        self.interval_minutes = 5

        # Connexion des signaux et des slots
        self.comboBox.currentIndexChanged.connect(self.change_schedule)
        self.comboBoxFiliere.currentIndexChanged.connect(self.filter_schedule)
        self.buttonRechercher.clicked.connect(self.search_student)

        # Initialisation de la fenêtre
        self.populate_filiere_combobox()
        self.filter_schedule()
        self.populate_completer()
        self.tableWidget.cellClicked.connect(self.show_details)

        # Charger les données de pré-assignation des salles
        self.preassigned_rooms_df = pd.read_csv(preassigned_rooms_file)

    def populate_filiere_combobox(self):
        """Remplit la combobox des filières."""
        self.comboBoxFiliere.addItem("Toutes")
        for filiere, _ in filiere_matieres:
            self.comboBoxFiliere.addItem(filiere)

    def populate_completer(self):
        """Configure l'auto-complétion pour la recherche d'étudiants."""
        etudiant_csv_path = 'Etudiant.csv'
        if os.path.exists(etudiant_csv_path):
            etudiants_df = pd.read_csv(etudiant_csv_path, header=None)
            self.etudiants_df = etudiants_df
            prenoms = etudiants_df.iloc[:, 0].unique().tolist()
            completer = QtWidgets.QCompleter(prenoms, self.lineEditPrenom)
            completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
            completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
            self.lineEditPrenom.setCompleter(completer)
        else:
            QtWidgets.QMessageBox.warning(self, "Erreur", f"Le fichier '{etudiant_csv_path}' n'existe pas.")

    def populate_schedule(self):
        """Charge l'emploi du temps depuis le fichier CSV et l'affiche."""
        emploi_du_temps_df = lire_emploi_du_temps_csv('emploi_du_temps.csv')
        if emploi_du_temps_df is None:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Impossible de charger l'emploi du temps.")
            return

        self.filter_schedule()

    def filter_scheduled(self, filiere_selectionnee=None):
        """Filtre l'emploi du temps en fonction de la filière sélectionnée."""
        emploi_du_temps_df = lire_emploi_du_temps_csv('emploi_du_temps.csv')
        if emploi_du_temps_df is None:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Impossible de lire le fichier emploi_du_temps.csv")
            return

        if filiere_selectionnee is None:
            filiere_selectionnee = self.comboBoxFiliere.currentText()

        if filiere_selectionnee != "Toutes":
            emploi_du_temps_df = emploi_du_temps_df[emploi_du_temps_df["Matière"].isin(
                [matiere for filiere, matieres in filiere_matieres if filiere == filiere_selectionnee for matiere in matieres])]

        start_time = self.date_debut.time()
        end_time = (datetime.datetime.combine(datetime.date.today(), start_time) +
                    datetime.timedelta(hours=self.amplitude_horaire_journaliere)).time()

        time_slots = generate_time_slots(datetime.datetime.combine(datetime.date.today(), start_time),
                                         datetime.datetime.combine(datetime.date.today(), end_time),
                                         self.interval_minutes)

        self.tableWidget.setRowCount(len(time_slots))
        unique_dates = emploi_du_temps_df['Date'].unique()
        self.tableWidget.setColumnCount(len(unique_dates))

        column_headers = [f"{date} ({pd.to_datetime(date).strftime('%A')})" for date in unique_dates]
        self.tableWidget.setHorizontalHeaderLabels(column_headers)

        self.tableWidget.setVerticalHeaderLabels([time_slots[i] if i % 6 == 0 else '' for i in range(len(time_slots))])

        self.tableWidget.clearContents()

        subject_colors = {}
        existing_colors = set()

        for matiere in emploi_du_temps_df['Matière'].unique():
            color = generate_random_color(existing_colors)
            subject_colors[matiere] = color
            existing_colors.add(color)

        date_to_col = {date: idx for idx, date in enumerate(unique_dates)}

        time_to_row = {time: index for index, time in enumerate(time_slots)}

        for _, entry in emploi_du_temps_df.iterrows():
            date = entry["Date"]
            start_time = entry["Début"][:5]
            end_time = entry["Fin"][:5]
            subject = entry["Matière"]

            start_row = time_to_row.get(start_time, None)
            end_row = time_to_row.get(end_time, None)
            col = date_to_col.get(date, None)

            if start_row is not None and end_row is not None and col is not None:
                duration_minutes = (datetime.datetime.strptime(end_time, '%H:%M') - datetime.datetime.strptime(start_time, '%H:%M')).seconds // 60
                duration_intervals = duration_minutes // self.interval_minutes

                for row in range(start_row, start_row + duration_intervals):
                    if row == start_row:
                        item = QtWidgets.QTableWidgetItem(f"{subject}\n\nSession {entry['Session']}")
                    else:
                        item = QtWidgets.QTableWidgetItem("")
                    item.setBackground(QtGui.QColor(subject_colors.get(subject, "#FFFFFF")))
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableWidget.setItem(row, col, item)

        for row in range(len(time_slots)):
            self.tableWidget.setRowHeight(row, 20)

        self.tableWidget.resizeColumnsToContents()

    def filter_schedule(self):
        """Filtre et affiche l'emploi du temps en fonction de la filière sélectionnée."""
        filiere_selectionnee = self.comboBoxFiliere.currentText()
        emploi_du_temps_df = lire_emploi_du_temps_csv('emploi_du_temps.csv')
        if emploi_du_temps_df is None:
            return

        if filiere_selectionnee != "Toutes":
            emploi_du_temps_df = emploi_du_temps_df[emploi_du_temps_df["Matière"].isin(
                [matiere for filiere, matieres in filiere_matieres if filiere == filiere_selectionnee for matiere in matieres])]

        start_time = self.date_debut.time()
        end_time = (datetime.datetime.combine(datetime.date.today(), start_time) +
                    datetime.timedelta(hours=self.amplitude_horaire_journaliere)).time()

        time_slots = generate_time_slots(datetime.datetime.combine(datetime.date.today(), start_time),
                                         datetime.datetime.combine(datetime.date.today(), end_time),
                                         self.interval_minutes)

        self.tableWidget.setRowCount(len(time_slots))
        unique_dates = emploi_du_temps_df['Date'].unique()
        self.tableWidget.setColumnCount(len(unique_dates))

        column_headers = [f"{date} ({pd.to_datetime(date).strftime('%A')})" for date in unique_dates]
        self.tableWidget.setHorizontalHeaderLabels(column_headers)

        self.tableWidget.setVerticalHeaderLabels([time_slots[i] if i % 6 == 0 else '' for i in range(len(time_slots))])

        self.tableWidget.clearContents()

        subject_colors = {}
        existing_colors = set()

        for matiere in emploi_du_temps_df['Matière'].unique():
            color = generate_random_color(existing_colors)
            subject_colors[matiere] = color
            existing_colors.add(color)

        date_to_col = {date: idx for idx, date in enumerate(unique_dates)}

        time_to_row = {time: index for index, time in enumerate(time_slots)}

        for _, entry in emploi_du_temps_df.iterrows():
            date = entry["Date"]
            start_time = entry["Début"][:5]
            end_time = entry["Fin"][:5]
            subject = entry["Matière"]

            start_row = time_to_row.get(start_time, None)
            end_row = time_to_row.get(end_time, None)
            col = date_to_col.get(date, None)

            if start_row is not None and end_row is not None and col is not None:
                duration_minutes = (datetime.datetime.strptime(end_time, '%H:%M') - datetime.datetime.strptime(start_time, '%H:%M')).seconds // 60
                duration_intervals = duration_minutes // self.interval_minutes

                for row in range(start_row, start_row + duration_intervals):
                    if row == start_row:
                        item = QtWidgets.QTableWidgetItem(f"{subject}\n\nSession {entry['Session']}")
                    else:
                        item = QtWidgets.QTableWidgetItem("")
                    item.setBackground(QtGui.QColor(subject_colors.get(subject, "#FFFFFF")))
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableWidget.setItem(row, col, item)

        for row in range(len(time_slots)):
            self.tableWidget.setRowHeight(row, 20)

        self.tableWidget.resizeColumnsToContents()

    def generate_individual_planning(self, prenom):
        """Génère et affiche l'emploi du temps individuel pour un étudiant donné."""
        etudiants_dict = lire_etudiants_csv("Etudiant.csv")
        if etudiants_dict is None:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Impossible de lire le fichier Etudiant.csv")
            return

        filiere = get_filiere_etudiant(etudiants_dict, prenom)
        if not filiere:
            QtWidgets.QMessageBox.warning(self, "Erreur", f"Aucun étudiant trouvé avec le prénom '{prenom}'")
            return

        assignments_etudiant = self.preassigned_rooms_df[self.preassigned_rooms_df['Prenom'] == prenom]
        self.filter_scheduled(filiere_selectionnee=filiere)

        for _, row in assignments_etudiant.iterrows():
            session = row['Session']
            salle = row['Salle']
            place = row['Place']

            for i in range(self.tableWidget.rowCount()):
                for j in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(i, j)
                    if item and f"Session {session}" in item.text():
                        item.setText(f"{item.text()}\nSalle: {salle}\nPlace: {place}")

    def search_student(self):
        """Recherche un étudiant par son prénom et affiche son emploi du temps."""
        prenom = self.lineEditPrenom.text()
        etudiants_dict = lire_etudiants_csv("Etudiant.csv")
        if etudiants_dict is None:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Impossible de lire le fichier Etudiant.csv")
            return

        filiere = get_filiere_etudiant(etudiants_dict, prenom)
        if not filiere:
            QtWidgets.QMessageBox.warning(self, "Erreur", f"Aucun étudiant trouvé avec le prénom '{prenom}'")
            return

        assignments_etudiant = self.preassigned_rooms_df[self.preassigned_rooms_df['Prenom'] == prenom]
        self.filter_scheduled(filiere_selectionnee=filiere)

        for _, row in assignments_etudiant.iterrows():
            session = row['Session']
            salle = row['Salle']
            place = row['Place']

            for i in range(self.tableWidget.rowCount()):
                for j in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(i, j)
                    if item and f"Session {session}" in item.text():
                        item.setText(f"{item.text()}\nSalle: {salle}\nPlace: {place}")

    def show_details(self, row, column):
        """Affiche les détails de l'emploi du temps lorsqu'une cellule est cliquée."""
        item = self.tableWidget.item(row, column)
        if item:
            text = item.text()
            if "Salle" in text and "Place" in text:
                QtWidgets.QMessageBox.information(self, "Détails", text)

    def change_schedule(self):
        """Met à jour l'emploi du temps lorsque la sélection change."""
        self.populate_schedule()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ScheduleApp()
    window.show()
    sys.exit(app.exec_())
