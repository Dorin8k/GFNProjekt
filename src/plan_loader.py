import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import pyqtSignal

class HaushaltsPlanWahl(QWidget):
    plan_selected = pyqtSignal(str)  # Signal, das den ausgewählten Plan sendet

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Haushaltsplan Manager")
        self.setGeometry(100, 100, 500, 200)

        self.layout = QVBoxLayout()

        # Labels für die drei Pläne
        self.plan_labels = []
        self.button_layouts = []

        for i in range(1, 4):
            hbox = QHBoxLayout()
            label = QLabel(f"Haushaltsplan {i}")
            self.plan_labels.append(label)

            btn_select = QPushButton("Öffnen")
            btn_edit = QPushButton("Umbenennen")
            btn_delete = QPushButton("Löschen")

            btn_select.clicked.connect(lambda _, plan=i: self.select_plan(plan))

            hbox.addWidget(label)
            hbox.addWidget(btn_select)
            hbox.addWidget(btn_edit)
            hbox.addWidget(btn_delete)

            self.button_layouts.append(hbox)
            self.layout.addLayout(hbox)

        self.setLayout(self.layout)

    def select_plan(self, plan_id):
        plan_name = f"Haushaltsplan_{plan_id}.db"
        self.plan_selected.emit(plan_name)  # Signal senden
        self.close()  # Schließt `plan_loader.py`, sobald ein Plan ausgewählt wird


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HaushaltsPlanWahl()
    window.show()
    sys.exit(app.exec())
