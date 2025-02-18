import sys
import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QSpinBox, QPushButton, QVBoxLayout, QHBoxLayout, QDateEdit, QMessageBox

class NewEntryGUI(QtWidgets.QDialog):  # Jetzt QDialog statt QWidget!
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Neuen Eintrag erstellen")
        self.setGeometry(350, 200, 400, 350)

        layout = QVBoxLayout()

        # Titel
        self.title_label = QLabel("Neuen Eintrag erstellen")
        layout.addWidget(self.title_label)

        # Name des Eintrags
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name des Eintrags")
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)

        # Typ des Eintrags (Einnahme oder Ausgabe)
        self.type_dropdown = QComboBox()
        self.type_dropdown.addItems(["Einnahme", "Ausgabe"])
        layout.addWidget(QLabel("Typ:"))
        layout.addWidget(self.type_dropdown)

        # Wert des Eintrags
        self.value_input = QSpinBox()
        self.value_input.setMaximum(1000000)
        layout.addWidget(QLabel("Betrag:"))
        layout.addWidget(self.value_input)

        # Datum des Eintrags
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        layout.addWidget(QLabel("Datum:"))
        layout.addWidget(self.date_input)

        # Kategorie des Eintrags
        self.category_dropdown = QComboBox()
        self.category_dropdown.addItems(["Essen", "Miete", "Freizeit", "Transport", "Sonstiges"])
        layout.addWidget(QLabel("Kategorie:"))
        layout.addWidget(self.category_dropdown)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Speichern")
        self.save_button.clicked.connect(self.save_entry)

        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.clicked.connect(self.reject)  # Verhindert Fehler beim Schließen

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def save_entry(self):
        """Speichert den neuen Eintrag in die Datenbank."""

        name = self.name_input.text()
        entry_type = self.type_dropdown.currentText()
        value = self.value_input.value()
        date = self.date_input.text()
        category = self.category_dropdown.currentText()

        if not name:
            QMessageBox.warning(self, "Fehler", "Der Name darf nicht leer sein.")
            return

        conn = sqlite3.connect("../data/Haushaltsplan.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Eintraege (name, wert, typ, datum, bereich) VALUES (?, ?, ?, ?, ?)",
                       (name, value, entry_type, date, category))
        print(cursor.fetchone())  # Sollte ('Eintraege',)
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Erfolgreich", "Eintrag wurde gespeichert.")
        self.accept()  # Fenster schließen

"""if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = NewEntryGUI()
    window.exec_()  # Nutzt exec_(), damit es modal bleibt
"""