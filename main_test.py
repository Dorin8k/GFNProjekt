import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout,
                             QPushButton, QHBoxLayout, QComboBox, QLineEdit, QDateEdit, QSpinBox, QDialog, QFormLayout)
from PyQt5.QtCore import Qt, QDate


class FinanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finanzübersicht")
        self.setGeometry(100, 100, 800, 500)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Year and Month Selection
        top_layout = QHBoxLayout()
        self.year_combo = QComboBox()
        self.year_combo.addItems(["2024", "2025", "2026"])
        self.month_combo = QComboBox()
        self.month_combo.addItems(["Januar", "Februar", "März", "April", "May", "Juni", "July", "August", "September", "Oktober", "November", "Dezember"])
        top_layout.addWidget(QLabel("Jahr:"))
        top_layout.addWidget(self.year_combo)
        top_layout.addWidget(QLabel("Monat:"))
        top_layout.addWidget(self.month_combo)
        layout.addLayout(top_layout)

        # Filter options
        filter_layout = QHBoxLayout()
        self.date_start = QDateEdit()
        self.date_start.setCalendarPopup(True)
        self.date_end = QDateEdit()
        self.date_end.setCalendarPopup(True)
        self.date_start.setDate(QDate.currentDate())
        self.date_end.setDate(QDate.currentDate())
        self.min_value = QSpinBox()
        self.min_value.setMaximum(10000)
        self.max_value = QSpinBox()
        self.max_value.setMaximum(10000)
        self.type_filter = QComboBox()
        self.type_filter.addItems(["Alle", "Eingabe", "Ausgabe"])
        self.search_box = QLineEdit()
        self.search_button = QPushButton("Suchen")

        filter_layout.addWidget(QLabel("Frühestens:"))
        filter_layout.addWidget(self.date_start)
        filter_layout.addWidget(QLabel("Spätestens:"))
        filter_layout.addWidget(self.date_end)
        filter_layout.addWidget(QLabel("Mindestens:"))
        filter_layout.addWidget(self.min_value)
        filter_layout.addWidget(QLabel("Maximal:"))
        filter_layout.addWidget(self.max_value)
        filter_layout.addWidget(QLabel("Typ:"))
        filter_layout.addWidget(self.type_filter)
        filter_layout.addWidget(self.search_box)
        filter_layout.addWidget(self.search_button)
        layout.addLayout(filter_layout)

        # Table for Entries
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Wert", "Typ", "Datum", "Bereich"])
        self.load_data()
        layout.addWidget(self.table)

        # Add Entry Button
        self.add_button = QPushButton("Neuen Eintrag erstellen")
        self.add_button.clicked.connect(self.add_entry)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def load_data(self):
        self.data = [["Einkauf", "70 €", "Ausgabe", "10.02.25", "Essen"],
                     ["Beitrag im Gym", "40 €", "Ausgabe", "01.02.25", "Sport"],
                     ["Gehalt", "2.500 €", "Eingabe", "29.01.25", "Arbeit"]]

        self.table.setRowCount(len(self.data))
        for row_idx, row_data in enumerate(self.data):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(col_data))

    def add_entry(self):
        dialog = AddEntryDialog(self)
        if dialog.exec_():
            new_entry = dialog.get_data()
            self.data.append(new_entry)
            self.table.setRowCount(len(self.data))
            for col_idx, col_data in enumerate(new_entry):
                self.table.setItem(len(self.data) - 1, col_idx, QTableWidgetItem(col_data))


class AddEntryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Neuer Eintrag")
        self.layout = QFormLayout()

        self.name_input = QLineEdit()
        self.value_input = QLineEdit()
        self.type_input = QComboBox()
        self.type_input.addItems(["Eingabe", "Ausgabe"])
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.category_input = QLineEdit()

        self.layout.addRow("Name:", self.name_input)
        self.layout.addRow("Wert:", self.value_input)
        self.layout.addRow("Typ:", self.type_input)
        self.layout.addRow("Datum:", self.date_input)
        self.layout.addRow("Bereich:", self.category_input)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)

    def get_data(self):
        return [
            self.name_input.text(),
            self.value_input.text() + " €",
            self.type_input.currentText(),
            self.date_input.date().toString("dd.MM.yy"),
            self.category_input.text()
        ]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FinanceApp()
    window.show()
    sys.exit(app.exec_())
