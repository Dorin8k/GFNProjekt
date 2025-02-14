"""
# Haushaltskasse mit PyQt5 – Einrichtung und Funktionsweise

## Einführung
Dieses Projekt ist eine GUI - Anwendung zur Verwaltung einer Haushaltskasse.Es ermöglicht das Erstellen, Bearbeiten
und Löschen von Einträgen zu Einnahmen und Ausgaben.Die Anwendung basiert auf ** PyQt5 ** und wir werden mit ** SQLite ** als Datenbank nutzen.

## 1. Einrichtung der Entwicklungsumgebung

### Installation von PyQt5 und Datenbankabhängigkeiten
Zunächst müssen wir PyQt5 sowie die benötigten Datenbankbibliotheken installieren:

bash
pip install
PyQt5
sqlite3
mysql - connector - python

### Projektstruktur

## 2. SQLite vs MySQL – Welche Datenbank soll genutzt werden?
### SQLite
SQLite ist leichtgewichtig, benötigt keinen separaten Server und speichert die Daten lokal in einer Datei.

#### Vorteile:
- Keine Einrichtung erforderlich
- Perfekt für kleine Anwendungen

### MySQL
MySQL erfordert einen separaten Server
und bietet mehr Skalierbarkeit für größere Datenmengen.

#### Vorteile:
- Skalierbarkeit
- Mehrbenutzerzugriff

## 3. GUI mit PyQt5 und Datenbankanbindung
Die GUI besteht aus:
- Einem ** Hauptfenster ** (`QMainWindow`)
- Einem ** Tabellenwidget ** (`QTableWidget`) zur Anzeige der Einträge
- ** Eingabefeldern ** (`QLineEdit`, `QDateEdit`, `QComboBox`) zur Erfassung neuer Einträge
- ** Buttons ** (`QPushButton`) für verschiedene Aktionen
"""

#### Einrichtung von SQLite in Python:
##
import sqlite3

class SQLiteDB:
    def __init__(self, db_name="haushaltskasse.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS finanzen (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                betrag REAL,
                datum TEXT,
                kategorie TEXT
            )
        """)
        self.conn.commit()


### Code-Snippet für das Hauptfenster
"""
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QHBoxLayout, QLabel, QLineEdit, QComboBox, QMessageBox, QDateEdit,
                             QSpinBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate

##Hauptfenster
class Haushaltskasse(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("Haushaltskasse")
        self.setGeometry(200, 200, 800, 500)
        self.db = db
        self.init_ui()



## 4. Verwaltung von Einträgen mit Datenbank
### Eintrag hinzufügen

def add_entry(self):
    name = self.name_input.text()
    value = float(self.value_input.text())
    date = self.date_input.date().toString("yyyy-MM-dd")
    category = self.category_box.currentText()

    if name and value:
        self.db.cursor.execute("INSERT INTO finanzen (name, betrag, datum, kategorie) VALUES (%s, %s, %s, %s)",
                               (name, value, date, category))
        self.db.conn.commit()
    else:
        QMessageBox.warning(self, "Fehler", "Bitte Name und Wert eingeben!")


### Eintrag bearbeiten

def edit_entry(self):
    selected_row = self.table.currentRow()
    if selected_row != -1:
        id_value = self.table.item(selected_row, 0).text()
        name = self.name_input.text()
        value = float(self.value_input.text())
        date = self.date_input.date().toString("yyyy-MM-dd")
        category = self.category_box.currentText()

        self.db.cursor.execute("UPDATE finanzen SET name=%s, betrag=%s, datum=%s, kategorie=%s WHERE id=%s",
                               (name, value, date, category, id_value))
        self.db.conn.commit()
    else:
        QMessageBox.warning(self, "Fehler", "Bitte einen Eintrag auswählen!")


### Eintrag löschen

def delete_entry(self):
    selected_row = self.table.currentRow()
    if selected_row != -1:
        id_value = self.table.item(selected_row, 0).text()
        self.db.cursor.execute("DELETE FROM finanzen WHERE id=%s", (id_value,))
        self.db.conn.commit()
    else:
        QMessageBox.warning(self, "Fehler", "Bitte einen Eintrag auswählen!")