import sys
import sqlite3
import datetime
import qdarkstyle
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (
    QTableWidgetItem, QMessageBox, QLabel, QComboBox, QPushButton,
    QLineEdit, QTableWidget, QVBoxLayout, QHBoxLayout, QWidget,
    QSpinBox, QDateEdit
)
from data.database import Haushaltsverwaltung
from PyQt5.QtGui import QIcon, QColor, QBrush
from PyQt5.QtCore import Qt
from src.edit_entry_gui import EditEntryGUI
from new_entry_gui import NewEntryGUI
from styles import load_stylesheet

class HaushaltsGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # 🌙 Dark Mode aktivieren
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        # 🌟 Fenster-Einstellungen
        self.setWindowTitle("Haushaltsverwaltung")
        self.setGeometry(400, 200, 900, 600)

        # 🎨 Allgemeines Styling für das Fenster
        self.setWindowFlags(Qt.FramelessWindowHint)  # Entfernt den Standard-Fensterrahmen

        self.setStyleSheet = load_stylesheet(self)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        # Eigene Titelleiste hinzufügen
        self.title_bar = QWidget(self)
        self.title_bar.setFixedHeight(40)  # Höhe der Titelleiste
        self.title_bar.setObjectName("title_bar")  # Objektname für Styling setzen

        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(10, 0, 10, 0)

        self.title_label = QLabel("Haushaltsverwaltung")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 16px; color: white;")
        title_layout.addWidget(self.title_label)

        # Minimieren-Button mit Hover-Effekt
        self.minimize_button = QPushButton("-")
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.setObjectName("minimize_button")
        self.minimize_button.clicked.connect(self.showMinimized)

        # Schließen-Button mit Hover-Effekt
        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(30, 30)
        self.close_button.setObjectName("close_button")
        self.close_button.clicked.connect(self.close)

        title_layout.addWidget(self.minimize_button)
        title_layout.addWidget(self.close_button)

        self.title_bar.setLayout(title_layout)
        self.layout.insertWidget(0, self.title_bar)  # Setzt die Titelleiste ganz oben

        self.central_widget.setLayout(self.layout)

        # Jahres- und Monatsauswahl mit Navigationsbuttons
        year_month_layout = QHBoxLayout()

        # Jahressteuerung
        self.year_prev = QPushButton("<<")
        self.year_next = QPushButton(">>")
        self.year_prev.setIcon(QIcon("icons/left_arrow.png"))
        self.year_next.setIcon(QIcon("icons/right_arrow.png"))

        self.current_year = datetime.datetime.now().year
        self.year_dropdown = QComboBox()
        self.year_dropdown.addItems(["Alle Jahre"] + [str(y) for y in range(2000, self.current_year + 3)])
        self.year_dropdown.setCurrentText(str(self.current_year))

        # Monatssteuerung
        self.month_prev = QPushButton("<<")
        self.month_next = QPushButton(">>")
        self.month_prev.setIcon(QIcon("icons/left_arrow.png"))
        self.month_next.setIcon(QIcon("icons/right_arrow.png"))

        self.month_dropdown = QComboBox()
        self.month_dropdown.addItems(["Alle Monate", "Januar", "Februar", "März", "April", "Mai", "Juni",
                                      "Juli", "August", "September", "Oktober", "November", "Dezember"])
        self.month_dropdown.setCurrentText("Alle Monate")

        # Layout zusammenfügen
        year_month_layout.addWidget(self.year_prev)
        year_month_layout.addWidget(self.year_dropdown)
        year_month_layout.addWidget(self.year_next)
        year_month_layout.addWidget(self.month_prev)
        year_month_layout.addWidget(self.month_dropdown)
        year_month_layout.addWidget(self.month_next)

        self.layout.addLayout(year_month_layout)

        # Signale verbinden
        self.year_prev.clicked.connect(lambda: self.change_year(-1))
        self.year_next.clicked.connect(lambda: self.change_year(1))
        self.month_prev.clicked.connect(lambda: self.change_month(-1))
        self.month_next.clicked.connect(lambda: self.change_month(1))

        # Filter- und Suchbereich
        filter_layout = QHBoxLayout()

        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(datetime.date(2000, 1, 1))  # Frühestmögliches Datum als Standard

        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(datetime.date(self.current_year, 12, 31))  # Standard: 31. Dezember des aktuellen Jahres

        self.min_input = QSpinBox()
        self.max_input = QSpinBox()
        self.max_input.setMaximum(100000)
        self.max_input.setValue(100000)

        self.type_dropdown = QComboBox()
        self.type_dropdown.addItems(["Einnahmen & Ausgaben", "Einnahme", "Ausgabe"])  # Standard: Alle Typen
        self.type_dropdown.setCurrentIndex(0)  # Standardmäßig auf "Einnahmen & Ausgaben"

        self.category_dropdown = QComboBox()
        self.category_dropdown.addItems(
            ["Alle Kategorien", "Essen", "Sport", "Arbeit", "Sonstiges"])  # Standard: Alle Kategorien
        self.category_dropdown.setCurrentIndex(0)  # Standardmäßig auf "Alle Kategorien"

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Text input (Suche)")
        self.search_button = QPushButton("Suchen")
        self.search_button.setStyleSheet("background-color: #B3E5FC; color: #01579B; border-radius: 5px; padding: 5px;")

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
        self.table.setStyleSheet(
            "background-color: white; alternate-background-color: #F5F5F5;")  # Alternierende Farben
        self.table.setAlternatingRowColors(True)  # Wechselt die Zeilenfarben für bessere Lesbarkeit

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
        self.update_label = QLabel("Letztes Update: Wird geladen...")
        self.layout.addWidget(self.update_label)

        # Neuen Eintrag erstellen
        self.new_entry_button = QPushButton("Neuen Eintrag erstellen")
        self.new_entry_button.clicked.connect(self.open_new_entry_window)
        self.layout.addWidget(self.new_entry_button)

        # Datenbank laden

        self.load_data()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'old_pos'):
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    # Ändert das Jahr basierend auf den Pfeiltasten und aktualisiert das Bis-Datum.
    def change_year(self, step):

        if self.year_dropdown.currentText() == "Alle Jahre":
            return  # Kein Wechsel, wenn "Alle Jahre" ausgewählt ist

        current_year = int(self.year_dropdown.currentText())
        new_year = current_year + step

        # Überprüfen, ob das neue Jahr im erlaubten Bereich ist
        all_years = [int(self.year_dropdown.itemText(i)) for i in range(1, self.year_dropdown.count())]
        if new_year in all_years:
            self.year_dropdown.setCurrentText(str(new_year))

            # Automatische Aktualisierung des "Bis:" Datums
            self.date_to.setDate(datetime.date(new_year, 12, 31))

        self.filter_table()

    # Ändert den Monat basierend auf den Pfeiltasten, ohne 'Alle Monate' als Option & ohne Absturz.
    def change_month(self, step):
        current_index = self.month_dropdown.currentIndex()

        # Falls "Alle Monate" aktiv ist, springe direkt zu Januar (beim Vorwärtsklick) oder Dezember (beim Rückwärtsklick)
        if current_index == 0:
            new_index = 1 if step > 0 else 12
        else:
            new_index = current_index + step

        # Falls der Index außerhalb von 1-12 geht, umschließen
        if new_index < 1:
            new_index = 12
        elif new_index > 12:
            new_index = 1

        self.month_dropdown.setCurrentIndex(new_index)

        # Automatische Aktualisierung des "Von:"- und "Bis:"-Datums basierend auf dem neuen Monat
        selected_year = int(
            self.year_dropdown.currentText()) if self.year_dropdown.currentText() != "Alle Jahre" else self.current_year

        # den ersten Tag auf 1. des Monats und den letzten Tag importieren
        first_day = 1  # **Immer auf den 1. des Monats setzen**
        last_day = (datetime.date(selected_year, new_index, 28) + datetime.timedelta(
            days=4)).day  # Automatisch letzter Tag des Monats

        self.date_from.setDate(datetime.date(selected_year, new_index, first_day))
        self.date_to.setDate(datetime.date(selected_year, new_index, last_day))

        self.filter_table()  # Tabelle aktualisieren

    '''def filter_table(self):
        """Filtert die Einträge basierend auf den ausgewählten Filtern und aktualisiert die Tabelle."""
        conn = sqlite3.connect("../data/Haushaltspläne.db")
        cursor = conn.cursor()

        # 📝 Basis-SQL-Abfrage (1=1 sorgt dafür, dass wir Bedingungen flexibel hinzufügen können)
        query = "SELECT eintragid, name, wert, bereich, typ, datum FROM Eintraege WHERE 1=1"
        params = []

        # 📌 Jahr filtern (wenn nicht "Alle Jahre")
        selected_year = self.year_dropdown.currentText()
        if selected_year != "Alle Jahre":
            query += " AND strftime('%Y', datum) = ?"
            params.append(selected_year)

        # 📌 Monat filtern (wenn nicht "Alle Monate")
        selected_month = self.month_dropdown.currentIndex()
        if selected_month > 0:  # "Alle Monate" hat Index 0
            month_number = f"{selected_month:02d}"
            query += " AND strftime('%m', datum) = ?"
            params.append(month_number)

        # 📌 Zeitraum filtern (Von/Bis)
        date_from = self.date_from.date().toString("yyyy-MM-dd")
        date_to = self.date_to.date().toString("yyyy-MM-dd")
        if date_from and date_to:
            query += " AND date(datum) BETWEEN date(?) AND date(?)"
            params.extend([date_from, date_to])

        # 📌 Betrag filtern (Min & Max) – nur falls Werte gesetzt sind
        min_value = self.min_input.value()
        max_value = self.max_input.value()
        if min_value > 0 or max_value < 100000:
            query += " AND wert BETWEEN ? AND ?"
            params.extend([min_value, max_value])

        # 📌 Typ filtern (Einnahme oder Ausgabe)
        selected_type = self.type_dropdown.currentText()
        if selected_type == "Einnahme":
            query += " AND typ = ?"
            params.append("Einnahme")
        elif selected_type == "Ausgabe":
            query += " AND typ = ?"
            params.append("Ausgabe")
        # Falls "Einnahmen & Ausgaben" gewählt wurde, wird nichts hinzugefügt (= beide erlaubt)

        # 📌 Kategorie filtern (wenn nicht "Alle Kategorien")
        selected_category = self.category_dropdown.currentText()
        if selected_category != "Alle Kategorien":
            query += " AND bereich = ?"
            params.append(selected_category)

        # 📌 Textsuche (sucht in Name, Bereich & Typ)
        search_text = self.search_input.text().strip()
        if search_text:
            query += " AND (name LIKE ? OR bereich LIKE ? OR typ LIKE ?)"
            params.extend([f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"])

        # 🔍 Debugging: SQL-Abfrage prüfen (optional auskommentieren)
        # print("SQL Query:", query)
        # print("Params:", params)

        # 🏗 SQL-Abfrage ausführen
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        # 🔄 Tabelle aktualisieren
        self.table.setRowCount(len(rows))

        for row_index, row_data in enumerate(rows):
            entry_id = row_data[0]
            name, wert, bereich, typ, datum = row_data[1:]

            # 🟢 Hintergrundfarben setzen (Einnahmen = Grün, Ausgaben = Grau)
            typ = typ.strip()
            wert = float(wert)
            if typ in ["Einnahme", "Einkommen"]:
                wert_text = f"+{wert:.2f} €"
                row_color = QColor(144, 238, 144)  # **Grün für Einnahmen**
            elif typ in ["Ausgabe", "Ausgaben"]:
                wert_text = f"-{wert:.2f} €"
                row_color = QColor(211, 211, 211)  # **Grau für Ausgaben**
            else:
                wert_text = f"{wert:.2f} €"
                row_color = QColor(255, 255, 255)  # Standard weiß

            # 📌 Hintergrundfarbe auf jede Spalte anwenden
            for col_index, col_data in enumerate([name, wert_text, bereich, typ, datum]):
                item = QTableWidgetItem(str(col_data))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(row_color)
                self.table.setItem(row_index, col_index, item)
        self.update_last_update_label()

    def init_database(self):
        conn = sqlite3.connect("../data/Haushaltspläne.db")
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
    '''
    def load_data(self):
        conn = sqlite3.connect("../data/Haushaltspläne.db")
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

    #Öffnet das Fenster zum Erstellen eines neuen Eintrags.
    def open_new_entry_window(self):
        self.new_entry_window = NewEntryGUI(self)
        self.new_entry_window.show()

    # Öffnet das Bearbeitungsfenster für einen Eintrag.
    def open_edit_window(self, entry_id):
        self.edit_window = EditEntryGUI(entry_id)
        self.edit_window.show()

    # Löscht einen Eintrag nach Bestätigung.
    def delete_entry(self, entry_id):

        reply = QMessageBox.question(self, "Löschen", "Eintrag wirklich löschen?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            conn = sqlite3.connect("../data/Haushaltspläne.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Eintraege WHERE eintragid = ?", (entry_id,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Erfolgreich", "Eintrag wurde gelöscht.")
            self.load_data()
