import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QDoubleSpinBox, QPushButton, QVBoxLayout, QHBoxLayout, \
    QWidget, QDateEdit, QMessageBox


class EditEntryGUI(QtWidgets.QWidget):
    def __init__(self, entry_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eintrag bearbeiten")
        self.setGeometry(350, 200, 400, 350)
        self.entry_id = entry_id

        layout = QVBoxLayout()

        # Titel
        self.title_label = QLabel("Eintrag bearbeiten")
        layout.addWidget(self.title_label)

        # Name des Eintrags
        self.name_input = QLineEdit()
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)

        # Typ des Eintrags (Einnahme oder Ausgabe)
        self.type_dropdown = QComboBox()
        self.type_dropdown.addItems(["Einnahme", "Ausgabe"])
        layout.addWidget(QLabel("Typ:"))
        layout.addWidget(self.type_dropdown)

        # Wert des Eintrags
        self.value_input = QDoubleSpinBox()
        self.value_input.setMaximum(1000000.00)
        self.value_input.setDecimals(2)
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
        'self.save_button.clicked.connect(self.save_entry)'
        self.cancel_button = QPushButton("Abbrechen")
        'self.cancel_button.clicked.connect(self.close)'

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.load_entry()

    '''#Lädt die bestehenden Daten des Eintrags aus der Datenbank.
    def load_entry(self):
        
        conn = sqlite3.connect("../data/Haushaltsplan.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, wert, typ, datum, bereich FROM Eintraege WHERE eintragid = ?", (self.entry_id,))
        entry = cursor.fetchone()
        conn.close()

        if entry:
            self.name_input.setText(entry[0])
            self.value_input.setValue(float(entry[1]))
            self.type_dropdown.setCurrentText(entry[2])
            self.date_input.setDate(QtCore.QDate.fromString(entry[3], "yyyy-MM-dd"))
            self.category_dropdown.setCurrentText(entry[4])
    
    # Speichert die bearbeiteten Daten des Eintrags.
    def save_entry(self):
        
        name = self.name_input.text()
        entry_type = self.type_dropdown.currentText()
        value = self.value_input.value()
        date = self.date_input.date().toString("yyyy-MM-dd")
        category = self.category_dropdown.currentText()

        if not name:
            QMessageBox.warning(self, "Fehler", "Der Name darf nicht leer sein.")
            return

        conn = sqlite3.connect("../data/Haushaltsplan.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE Eintraege SET name = ?, wert = ?, typ = ?, datum = ?, bereich = ? WHERE eintragid = ?",
                       (name, value, entry_type, date, category, self.entry_id))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Erfolgreich", "Eintrag wurde aktualisiert.")
        self.close()
'''

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = EditEntryGUI(1)  # Beispielhafte ID
    window.show()
    sys.exit(app.exec_())
