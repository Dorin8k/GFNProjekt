import unittest
from data.database import Haushaltsverwaltung
from datetime import datetime, timedelta

class TestHaushaltsverwaltung(unittest.TestCase):
    def setUp(self):
        # Erstelle eine Instanz der Haushaltsverwaltung
        self.hw = Haushaltsverwaltung(":memory:")  # Verwende eine In-Memory-Datenbank für Tests
        self.hw._create_tables()  # Erstelle die Tabellen

        # Füge einen wiederkehrenden Eintrag hinzu, der mit dem bestehenden Plan verknüpft ist
        self.hw.addEintrag(1, 'Wiederkehrender Eintrag', 100, 'Test', 'Ausgaben', '01.01.2025', reihe=1, intervall='monatlich', von='01.01.2023', bis='31.12.2025')

    def test_autoAddEntry(self):
        # Set old_time to a date before the expected new entry date
        old_time = datetime.strptime('01.01.2023', "%d.%m.%Y")
        self.hw.updateLastChecked(1)  # Update the last checked time

        # Execute the autoAddEntry function
        self.hw.autoAddEntry(old_time, 1)

        # Check if new entries were created
        self.hw.cursor.execute("SELECT * FROM Eintraege WHERE planid = 1 AND name = 'Wiederkehrender Eintrag'")
        entries = self.hw.cursor.fetchall()

        # Check if more than one entry exists
        self.assertGreater(len(entries), 1, "Es sollten mehrere Einträge für den wiederkehrenden Eintrag vorhanden sein.")

        # Print the entries created for verification
        print("\nErstellte Einträge:")
        for entry in entries:
            eintrag_datum = datetime.strptime(entry[6], "%d.%m.%Y")  # Date is in the 7th field
            print(f"ID: {entry[0]}, Name: {entry[5]}, Wert: {entry[4]}, Datum: {eintrag_datum}, Typ: {entry[6]}")

        # Check if the entries are in the correct interval
        for entry in entries:
            eintrag_datum = datetime.strptime(entry[6], "%d.%m.%Y")  # Date is in the 7th field
            print(f"old_time: {old_time}, eintrag_datum: {eintrag_datum}, current_time: {datetime.now()}")  # Debugging output
            self.assertTrue(old_time < eintrag_datum, "Der Eintrag sollte nach dem alten Datum liegen.")

    def tearDown(self):
        # Schließe die Verbindung zur Datenbank
        self.hw.close()

if __name__ == '__main__':
    unittest.main()
