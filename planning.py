import PyQt5
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QMainWindow
from PyQt5.uic import loadUi
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("planning.ui", self)

    def configure_table(self):
        # Configurer l'apparence du tableau
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(['Date', 'Heure', 'Matière', 'Salle'])

        # Ajuster la taille des colonnes
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.tableWidget.columnCount() - 1,
                                                                 self.tableWidget.horizontalHeader().Stretch)

        self.tableWidget.setStyleSheet("""
                  QTableWidget {
                      background-color: #f0f0f0;
                      alternate-background-color: #e0e0e0;
                      selection-background-color: #a0a0a0;
                  }
                  QHeaderView::section {
                      background-color: #d3d3d3;
                      font-weight: bold;
                      font-size: 12pt;
                  }
                  QTableWidget::item {
                      padding: 5px;
                  }
              """)
        self.tableWidget.setSortingEnabled(True)

        # Exemple pour ajouter des données
        self.add_exam('2024-05-18', '10:00', 'Mathématiques', 'Salle 101')

    def add_exam(self, date, time, subject, room):
        rowposition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowposition)
        self.tableWidget.setItem(rowposition, 0, QTableWidgetItem(date))
        self.tableWidget.setItem(rowposition, 1, QTableWidgetItem(time))
        self.tableWidget.setItem(rowposition, 2, QTableWidgetItem(subject))
        self.tableWidget.setItem(rowposition, 3, QTableWidgetItem(room))

if __name__ =="__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



