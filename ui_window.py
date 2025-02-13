"""GUI Version 1.2 mit platzhalter für sqlite"""
"""Details ins Introduction_README(in work) ----> 
pip install 
PyQt5
sqlite3"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QHBoxLayout, QLabel, QLineEdit, QComboBox, QMessageBox, QDateEdit,
                             QSpinBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate

class Haushaltsbuch(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Haushaltsbuch")
        self.setGeometry(200, 200, 750, 550)
        self.setWindowIcon(QIcon("assets/ra.jpg"))  # Eigenes Icon setzen

        # Daten-Speicher (Dummy-Daten)
        self.entries = [
            {"name": "Einkauf", "value": 70, "date": "2025-02-10", "category": "Essen", "type": "Ausgabe"},
            {"name": "Gym Beitrag", "value": 40, "date": "2025-02-01", "category": "Sport", "type": "Ausgabe"},
            {"name": "Gehalt", "value": 2500, "date": "2025-01-29", "category": "Arbeit", "type": "Einnahme"}
        ]

        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        # Filter Section
        filter_layout = QHBoxLayout()

        self.filter_box = QComboBox()
        self.filter_box.addItems(["Alle", "Einnahme", "Ausgabe"])
        self.filter_box.currentTextChanged.connect(self.apply_filter)
        filter_layout.addWidget(QLabel("Typ:"))
        filter_layout.addWidget(self.filter_box)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Suche nach Name...")
        self.search_input.textChanged.connect(self.apply_filter)
        filter_layout.addWidget(QLabel("Name:"))
        filter_layout.addWidget(self.search_input)

        self.min_value = QSpinBox()
        self.min_value.setMaximum(100000)
        self.min_value.setPrefix("Min: ")
        self.min_value.valueChanged.connect(self.apply_filter)
        filter_layout.addWidget(self.min_value)

        self.max_value = QSpinBox()
        self.max_value.setMaximum(100000)
        self.max_value.setValue(100000)
        self.max_value.setPrefix("Max: ")
        self.max_value.valueChanged.connect(self.apply_filter)
        filter_layout.addWidget(self.max_value)

        layout.addLayout(filter_layout)

        # Table for entries
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Betrag (€)", "Datum", "Kategorie", "Typ"])
        self.table.setStyleSheet("background-color: #f8f9fa; border-radius: 10px;")
        layout.addWidget(self.table)

        # Entry input section
        entry_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("📝 Name")
        self.value_input = QSpinBox()
        self.value_input.setMaximum(50000)
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("📂 Kategorie")
        self.type_box = QComboBox()
        self.type_box.addItems(["Einnahme", "Ausgabe"])
        self.add_entry_button = QPushButton("➕ Eintrag hinzufügen")

        entry_layout.addWidget(self.name_input)
        entry_layout.addWidget(self.value_input)
        entry_layout.addWidget(self.date_input)
        entry_layout.addWidget(self.category_input)
        entry_layout.addWidget(self.type_box)
        entry_layout.addWidget(self.add_entry_button)
        layout.addLayout(entry_layout)

        # Entry management buttons
        self.delete_entry_button = QPushButton("❌ Eintrag löschen")
        layout.addWidget(self.delete_entry_button)

        self.central_widget.setLayout(layout)

        # Button Events
        self.add_entry_button.clicked.connect(self.add_entry)
        self.delete_entry_button.clicked.connect(self.delete_entry)

        # Lade Einträge in die Tabelle
        self.load_entries()

    ##Moderneres Style Sheet
    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
                color: white;
            }
            QLabel {
                font-size: 14px;
                color: white;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 10px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLineEdit, QSpinBox, QComboBox, QDateEdit {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
            }
        """)

    ##Lädt die Einträge in die Tabelle (entweder alle oder gefiltert).
    def load_entries(self, filtered_entries=None):
        self.table.setRowCount(0)

        if filtered_entries is None:
            filtered_entries = self.entries  # Default: alle Einträge

        for row_index, row_data in enumerate(filtered_entries):
            self.table.insertRow(row_index)
            for col_index, key in enumerate(["name", "value", "date", "category", "type"]):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(row_data[key])))

    ##Fügt einen neuen Eintrag zur Liste hinzu.
    def add_entry(self):
        name = self.name_input.text().strip()
        value = self.value_input.value()
        date = self.date_input.date().toString("yyyy-MM-dd")
        category = self.category_input.text().strip()
        entry_type = self.type_box.currentText()

        if name and category:
            new_entry = {"name": name, "value": value, "date": date, "category": category, "type": entry_type}
            self.entries.append(new_entry)
            self.load_entries()
            self.name_input.clear()
            self.category_input.clear()
            self.value_input.setValue(0)
        else:
            QMessageBox.warning(self, "Fehler", "Bitte alle Felder ausfüllen!")

    ##Löscht den ausgewählten Eintrag.
    def delete_entry(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            del self.entries[selected_row]
            self.load_entries()
        else:
            QMessageBox.warning(self, "Fehler", "Bitte einen Eintrag auswählen!")

    ##Wendet die Filter auf die Einträge an.
    def apply_filter(self):
        filter_type = self.filter_box.currentText()
        search_text = self.search_input.text().strip().lower()
        min_val = self.min_value.value()
        max_val = self.max_value.value()

        filtered_entries = [
            entry for entry in self.entries if
            (filter_type == "Alle" or entry["type"] == filter_type) and
            (search_text in entry["name"].lower()) and
            (min_val <= entry["value"] <= max_val)
        ]

        self.load_entries(filtered_entries)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Haushaltsbuch()
    window.show()
    sys.exit(app.exec_())
