import sys
import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QLabel, QComboBox, QPushButton, QLineEdit, QTableWidget, \
    QVBoxLayout, QHBoxLayout, QWidget, QSpinBox, QDateEdit
from src.edit_entry_gui import EditEntryGUI
from new_entry_gui import NewEntryGUI

class HaushaltsGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Haushaltsverwaltung")
        self.setGeometry(100, 100, 900, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Jahres- und Monatsauswahl mit Navigationsbuttons
        year_month_layout = QHBoxLayout()
        self.year_prev = QPushButton("<<")
        self.year_next = QPushButton(">>")
        self.year_label = QLabel("2025")

        self.month_prev = QPushButton("<<")
        self.month_next = QPushButton(">>")
        self.month_label = QLabel("Februar")

        year_month_layout.addWidget(self.year_prev)
        year_month_layout.addWidget(self.year_label)
        year_month_layout.addWidget(self.year_next)
        year_month_layout.addWidget(self.month_prev)
        year_month_layout.addWidget(self.month_label)
        year_month_layout.addWidget(self.month_next)

        self.layout.addLayout(year_month_layout)

        # Filter- und Suchbereich
        filter_layout = QHBoxLayout()

        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)

        self.min_input = QSpinBox()
        self.max_input = QSpinBox()
        self.max_input.setMaximum(1000000)

        self.type_dropdown = QComboBox()
        self.type_dropdown.addItems(["Einnahme", "Ausgabe"])
        self.category_dropdown = QComboBox()
        self.category_dropdown.addItems(["Essen", "Sport", "Arbeit", "Sonstiges"])
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Text input (Suche)")
        self.search_button = QPushButton("Suchen")
        self.search_button.clicked.connect(self.filter_table)

        filter_layout.addWidget(QLabel("Von:"))
        filter_layout.addWidget(self.date_from)
        filter_layout.addWidget(QLabel("Bis:"))
        filter_layout.addWidget(self.date_to)
        filter_layout.addWidget(QLabel("Min Wert:"))
        filter_layout.addWidget(self.min_input)
        filter_layout.addWidget(QLabel("Max Wert:"))
        filter_layout.addWidget(self.max_input)
        filter_layout.addWidget(self.type_dropdown)
        filter_layout.addWidget(self.category_dropdown)
        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(self.search_button)

        self.layout.addLayout(filter_layout)

        # Übersichtstabelle
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Name", "Wert", "Typ", "Datum", "Bereich", "Aktionen"])
        self.layout.addWidget(self.table)

        # Spaltenbreite anpassen
        self.table.setColumnWidth(0, 200)  # Name
        self.table.setColumnWidth(1, 100)  # Wert
        self.table.setColumnWidth(2, 100)  # Typ
        self.table.setColumnWidth(3, 150)  # Datum
        self.table.setColumnWidth(4, 150)  # Bereich
        self.table.setColumnWidth(5, 120)  # Aktionen

        # Letzte Aktualisierung anzeigen
        self.update_label = QLabel("Letztes Update: vor 5 Minuten")
        self.layout.addWidget(self.update_label)

        # Neuen Eintrag erstellen
        self.new_entry_button = QPushButton("Neuen Eintrag erstellen")
        self.new_entry_button.clicked.connect(self.open_new_entry_window)
        self.layout.addWidget(self.new_entry_button)

        # Datenbank laden
        self.init_database()
        self.load_data()

    def filter_table(self):
        """Filtert die Tabelle basierend auf dem Suchtext."""
        search_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            row_visible = any(
                self.table.item(row, col) and search_text in self.table.item(row, col).text().lower()
                for col in range(self.table.columnCount() - 1)  # Excluding action buttons
            )
            self.table.setRowHidden(row, not row_visible)

    def init_database(self):
        conn = sqlite3.connect("../Haushaltspläne.db")
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Eintraege (
            eintragid INTEGER PRIMARY KEY AUTOINCREMENT,
            planid INTEGER,
            name TEXT,
            wert REAL,
            bereich TEXT,
            typ TEXT,
            datum TEXT
        )
        """)
        conn.commit()
        conn.close()

    def load_data(self):
        conn = sqlite3.connect("../Haushaltspläne.db")
        cursor = conn.cursor()
        cursor.execute("SELECT eintragid, name, wert, typ, datum, bereich FROM Eintraege")
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            entry_id = row_data[0]
            for col_index, col_data in enumerate(row_data[1:]):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

            # Buttons für Bearbeiten und Löschen
            edit_button = QPushButton("✏")
            edit_button.clicked.connect(lambda _, id=entry_id: self.open_edit_window(id))
            delete_button = QPushButton("🗑")
            delete_button.clicked.connect(lambda _, id=entry_id: self.delete_entry(id))

            action_layout = QHBoxLayout()
            action_layout.addWidget(edit_button)
            action_layout.addWidget(delete_button)
            action_widget = QWidget()
            action_widget.setLayout(action_layout)

            self.table.setCellWidget(row_index, 5, action_widget)

    def open_new_entry_window(self):
        """Öffnet das Fenster zum Erstellen eines neuen Eintrags."""
        self.new_entry_window = NewEntryGUI(self)
        self.new_entry_window.show()

    def open_edit_window(self, entry_id):
        """Öffnet das Bearbeitungsfenster für einen Eintrag."""
        self.edit_window = EditEntryGUI(entry_id)
        self.edit_window.show()

    def delete_entry(self, entry_id):
        """Löscht einen Eintrag nach Bestätigung."""
        reply = QMessageBox.question(self, "Löschen", "Eintrag wirklich löschen?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            conn = sqlite3.connect("../Haushaltspläne.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Eintraege WHERE eintragid = ?", (entry_id,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Erfolgreich", "Eintrag wurde gelöscht.")
            self.load_data()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = HaushaltsGUI()
    window.show()
    sys.exit(app.exec_())
