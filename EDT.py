# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi

class ScheduleApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("EDT.ui", self)
        self.populate_schedule()

    def populate_schedule(self):
        self.tableWidget.setRowCount(26)  # 26 créneaux horaires de 8h à 20h avec des intervalles de 30 minutes
        self.tableWidget.setColumnCount(6)  # 6 jours de la semaine
        self.tableWidget.setHorizontalHeaderLabels(['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'])
        self.tableWidget.setVerticalHeaderLabels(['8h', '8h30', '9h', '9h30', '10h', '10h30', '11h', '11h30', '12h', '12h30', '13h', '13h30', '14h', '14h30', '15h', '15h30', '16h', '16h30', '17h', '17h30', '18h', '18h30', '19h', '19h30', '20h'])

        # Defining colors for different types of subjects
        subject_colors = {
            "Probabilités avancées et simulation monte carlo": "#00FF00",  # Green
            "Analyse et programmation orientée objet": "#00FF00",          # Green
            "Statistiques inférentielles": "#00FF00",                     # Green
            "Optimisation linéaire": "#00FF00",                           # Green
            "Interaction et coopération": "#FFA500",                      # Orange
            "Gestion de l'entreprise II": "#FFA500",                      # Orange
            "Optimisation non linéaire": "#0000FF",                       # Blue
            "Équations différentielles": "#0000FF"                        # Blue
        }

        schedule_data = [
            {"day": "Lundi", "start_time": "9h", "end_time": "12h", "subject": "Probabilités avancées et simulation monte carlo", "location": "Salle FER HELLX 2\nPlace 202\n9h-12h"},
            {"day": "Lundi", "start_time": "14h", "end_time": "16h", "subject": "Optimisation linéaire", "location": "Salle FER HELLX 2\nPlace 207\n14h-16h"},
            {"day": "Mardi", "start_time": "9h", "end_time": "10h30", "subject": "Interaction et coopération", "location": "Salle FER HELLX 2\nPlace 405\n9h-10h30"},
            {"day": "Mardi", "start_time": "11h", "end_time": "12h", "subject": "Analyse et programmation orientée objet", "location": "Salle FER HELLX 2\nPlace 203\n11h-12h"},
            {"day": "Mardi", "start_time": "14h", "end_time": "16h", "subject": "Gestion de l'entreprise II", "location": "Salle FER HELLX 2\nPlace 405\n14h-16h"},
            {"day": "Jeudi", "start_time": "14h", "end_time": "16h", "subject": "Statistiques inférentielles", "location": "Salle FER HELLX 2\nPlace 209\n14h-16h"},
            {"day": "Vendredi", "start_time": "9h", "end_time": "11h", "subject": "Optimisation non linéaire", "location": "Salle FER HELLX 2\nPlace 205\n9h-11h"},
            {"day": "Vendredi", "start_time": "14h", "end_time": "16h", "subject": "Équations différentielles", "location": "Salle FER HELLX 2\nPlace 202\n14h-16h"},
        ]

        day_to_col = {"Lundi": 0, "Mardi": 1, "Mercredi": 2, "Jeudi": 3, "Vendredi": 4, "Samedi": 5}
        time_to_row = {"8h": 0, "8h30": 1, "9h": 2, "9h30": 3, "10h": 4, "10h30": 5, "11h": 6, "11h30": 7, "12h": 8, "12h30": 9, "13h": 10, "13h30": 11, "14h": 12, "14h30": 13, "15h": 14, "15h30": 15, "16h": 16, "16h30": 17, "17h": 18, "17h30": 19, "18h": 20, "18h30": 21, "19h": 22, "19h30": 23, "20h": 24}

        for entry in schedule_data:
            start_row = time_to_row[entry["start_time"]]
            end_row = time_to_row[entry["end_time"]]
            col = day_to_col[entry["day"]]
            for row in range(start_row, end_row):
                if row == start_row:
                    item = QtWidgets.QTableWidgetItem(f"{entry['subject']}\n\n{entry['location']}")
                else:
                    item = QtWidgets.QTableWidgetItem("")
                item.setBackground(QtGui.QColor(subject_colors[entry["subject"]]))
                self.tableWidget.setItem(row, col, item)

        self.tableWidget.resizeRowsToContents()  # Resize rows to fit content
        self.tableWidget.resizeColumnsToContents()  # Resize columns to fit content

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ScheduleApp()
    window.show()
    sys.exit(app.exec_())



