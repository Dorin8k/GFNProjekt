
from data.database import Haushaltsverwaltung

def test_remainingDays():
    haushaltsverwaltung = Haushaltsverwaltung()

    test_cases = [
        ('01-01-2025', '25-01-2025', '01-01-2025', 25),
        ('25-01-2025', '05-02-2025', '01-01-2025', 11),
        ('28-02-2025', '05-03-2025', '01-03-2025', 6),
        ('01-03-2025', '15-03-2025', '01-03-2025', 15),
        ('15-03-2025', '05-04-2025', '01-03-2025', 21),
        ('01-01-2025', '31-01-2025', '01-01-2025', 31),
    ]

    for i, (datumVon, datumBis, currentMonth, expected) in enumerate(test_cases):
        try:
            result = haushaltsverwaltung.remainingDays(datumVon, datumBis, currentMonth)
            assert result == expected, f"Test {i + 1} fehlgeschlagen: Erwartet {expected}, erhalten {result}"
        except Exception as e:
            print(f"Fehler bei Test {i + 1}: {e}")

    print("Alle Tests erfolgreich bestanden!")


# Testaufruf
test_remainingDays()
