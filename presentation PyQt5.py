import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class PyQt5Presentation(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create UI elements
        title = QLabel("Wilkommen bei PyQt5!", self)
        description = QLabel("PyQt5 ist eine leistungsstarke Python-Bibliothek zum Erstellen von GUI-Anwendungen.")
        button = QPushButton("Click Me", self)
        button.clicked.connect(self.on_click)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(button)
        self.setLayout(layout)

        # Window properties
        self.setWindowTitle("PyQt5 Presentation")
        self.resize(400, 200)
        self.show()

    def on_click(self):
        self.setWindowTitle("Button Clicked!")

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PyQt5Presentation()
    sys.exit(app.exec_())