import unittest
from data.database import Haushaltsverwaltung
from datetime import datetime, timedelta

class TestHaushaltsverwaltung(unittest.TestCase):
    def setUp(self):
        # Erstelle eine Instanz der Haushaltsverwaltung
        self.hw = Haushaltsverwaltung(":memory:")  # Verwende eine In-Memory-Datenbank für Tests
        self.hw._create_tables()  # Erstelle die Tabellen

        # Füge einen wiederkehrenden Eintrag hinzu, der mit dem bestehenden Plan verknüpft ist
        self.hw.addEintrag(1, 'Wiederkehrender Eintrag', 100, 'Test', 'Ausgaben', '01-01-2023', reihe=1, intervall='monatlich', von='01-01-2023', bis='31-12-2023')

    def test_autoAddEntry(self):
        # Setze die Zeit auf einen Punkt, an dem neue Einträge erstellt werden sollten
        old_time = datetime.strptime('01-01-2023', "%d-%m-%Y")
        self.hw.updateLastChecked(1)  # Aktualisiere den letzten Prüfzeitpunkt

        # Führe die autoAddEntry-Funktion aus
        self.hw.autoAddEntry(old_time, 1)

        # Überprüfe, ob neue Einträge erstellt wurden
        self.hw.cursor.execute("SELECT * FROM Eintraege WHERE planid = 1 AND name = 'Wiederkehrender Eintrag'")
        entries = self.hw.cursor.fetchall()

        # Überprüfe, ob mehr als einen Eintrag vorhanden ist
        self.assertGreater(len(entries), 1, "Es sollten mehrere Einträge für den wiederkehrenden Eintrag vorhanden sein.")

        # Überprüfe, ob die Einträge im richtigen Intervall liegen
        for entry in entries:
            eintrag_datum = datetime.strptime(entry[6], "%d-%m-%Y")  # Datum ist im 7. Feld
            print(f"old_time: {old_time}, eintrag_datum: {eintrag_datum}, current_time: {datetime.now()}")  # Debugging-Ausgabe
            self.assertTrue(old_time < eintrag_datum, "Der Eintrag sollte nach dem alten Datum liegen.")

        def tearDown(self):
            # Schließe die Verbindung zur Datenbank
            self.hw.close()

if __name__ == '__main__':
    unittest.main()
