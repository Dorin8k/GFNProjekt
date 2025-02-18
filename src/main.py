import sys
from PyQt5 import QtWidgets

from data.database import HaushaltsverwaltungDatenbank
from src.ui_window import HaushaltsGUI

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    db = HaushaltsverwaltungDatenbank()
    window = HaushaltsGUI()
    window.show()
    sys.exit(app.exec_())
