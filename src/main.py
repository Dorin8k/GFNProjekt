import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from data.database import Haushaltsverwaltung
from src.plan_loader import HaushaltsPlanWahl
from src.ui_window import HaushaltsGUI

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.plan_loader = HaushaltsPlanWahl()
        self.plan_loader.plan_selected.connect(self.start_main_window)  # Verknüpfen des Signals
        self.plan_loader.show()

    def start_main_window(self, db_name):
        self.main_window = HaushaltsGUI()  # Hauptfenster mit Datenbank starten
        self.main_window.show()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    db = Haushaltsverwaltung()
    window = HaushaltsGUI()
    window.show()
    sys.exit(app.exec_())
