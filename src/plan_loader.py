"""import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QMessageBox


class HaushaltsPlanWahl(QWidget):
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

            btn_edit = QPushButton("Umbenennen")
            btn_delete = QPushButton("Löschen")

            hbox.addWidget(label)
            hbox.addWidget(btn_edit)
            hbox.addWidget(btn_delete)

            self.button_layouts.append(hbox)
            self.layout.addLayout(hbox)

        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HaushaltsPlanWahl()
    window.show()
    sys.exit(app.exec())
"""