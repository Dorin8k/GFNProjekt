import qdarkstyle
from PyQt5.QtCore import Qt

def load_stylesheet(self):
    self.setWindowFlags(Qt.FramelessWindowHint)  # Entfernt den Standard-Fensterrahmen
    return qdarkstyle.load_stylesheet_pyqt5() + """
                /* 🌑 Hauptfenster */
                QMainWindow {
                    background-color: #121212;
                    color: white;
                    border: none;
                }
    
                /* 🖤 Eigene Titelleiste */
                QWidget#title_bar {
                    background-color: black;
                    color: white;
                    border-bottom: 2px solid #444;
                }
    
                /* 📌 Menüleiste */
                QMenuBar {
                    background-color: #1E1E1E;
                    color: white;
                    border-bottom: 1px solid #444;
                }
    
                /* 🔘 Buttons */
                QPushButton {
                    background-color: #333;
                    color: white;
                    border-radius: 5px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: #555;
                }
                QPushButton:pressed {
                    background-color: #777;
                }
    
                /* 📋 Tabellen-Styling */
                QTableWidget {
                    background-color: #1E1E1E;
                    alternate-background-color: #2A2A2A;
                    color: black;  /* Textfarbe in Tabellen auf Weiß setzen */
                    gridline-color: #444;
                    border: 2px solid #333;
                    font-size: 14px;
                }
    
                /* 📌 Tabellen-Kopfzeile */
                QHeaderView::section {
                    background-color: #2A2A2A;
                    color: white;  /* Kopfzeilen-Textfarbe auf Weiß setzen */
                    font-weight: bold;
                    padding: 6px;
                    border: 1px solid #444;
                }
                QLabel {
                    color: white;  /* Labels explizit weiß setzen */
                    font-size: 14px;
                    font-weight: bold;
                }
                /* ✍ Eingabefelder */
                QLineEdit, QComboBox, QSpinBox, QDateEdit {
                    background-color: #222;
                    color: white;  /* Eingabefeld-Textfarbe auf Weiß setzen */
                    border: 1px solid #444;
                    border-radius: 5px;
                    padding: 5px;
                }
                QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDateEdit:focus {
                    border: 1px solid #007ACC;
                }
    
                /* 🔘 Minimieren- und Schließen-Button */
                QPushButton#minimize_button {
                    background-color: gray;
                    color: white;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton#minimize_button:hover {
                    background-color: darkgray;
                }
    
                QPushButton#close_button {
                    background-color: red;
                    color: white;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton#close_button:hover {
                    background-color: darkred;
                }
                """