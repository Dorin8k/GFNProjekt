
from data.database import Haushaltsverwaltung

def test_haushaltsverwaltung():
    verwaltung = Haushaltsverwaltung()

    # Test 1: Alle Einträge ohne Filter
    print("Test 1: Alle Einträge ohne Filter")
    eintraege = verwaltung.fetchAllEintraege(1)
    print(eintraege)

    # Test 2: Filter nach Name
    print("\nTest 2: Filter nach Name (Gehalt)")
    eintraege = verwaltung.fetchAllEintraege(1, filter_name='Gehalt')
    print(eintraege)

    # Test 3: Filter nach Bereich
    print("\nTest 3: Filter nach Bereich (Verpflegung)")
    eintraege = verwaltung.fetchAllEintraege(1, filter_bereich='Verpflegung')
    print(eintraege)

    # Test 4: Filter nach Typ
    print("\nTest 4: Filter nach Typ (Ausgaben)")
    eintraege = verwaltung.fetchAllEintraege(1, filter_typ='Ausgaben')
    print(eintraege)

    # Test 5: Filter nach Datum
    print("\nTest 5: Filter nach Datum (2025-01-12)")
    eintraege = verwaltung.fetchAllEintraege(1, filter_date='12-01-2025')
    print(eintraege)

    # Test 6: Filter nach Wert von
    print("\nTest 6: Filter nach Wert von (30.0)")
    eintraege = verwaltung.fetchAllEintraege(1, filter_wert_von=30.0)
    print(eintraege)

    # Test 7: Filter nach Wert bis
    print("\nTest 7: Filter nach Wert bis (250.0)")
    eintraege = verwaltung.fetchAllEintraege(1, filter_wert_bis=250.0)
    print(eintraege)

    # Test 8: Filter nach Wert von und Wert bis
    print("\nTest 8: Filter nach Wert von (30.0) und Wert bis (250.0)")
    eintraege = verwaltung.fetchAllEintraege(1, filter_wert_von=30.0, filter_wert_bis=250.0)
    print(eintraege)

    # Test 9: Kombination aller Filter
    print("\nTest 9: Kombination aller Filter")
    eintraege = verwaltung.fetchAllEintraege(
        1,
        filter_name='Neues Gehalt',
        filter_bereich='Arbeit',
        filter_typ='Einkommen',
        filter_date='12-01-2025',
        filter_wert_von=1000.0,
        filter_wert_bis=3000.0
    )
    print(eintraege)

    # Test 10: Eintrag umbenennen
    print("\nTest 10: Eintrag umbenennen")
    verwaltung.renameEintrag(1, 1, 'Neues Gehalt', 3000, 'Arbeit', 'Einkommen', '12-01-2025')
    eintraege = verwaltung.fetchAllEintraege(1)
    print(eintraege)

    # Test 11: Eintrag löschen
    print("\nTest 11: Eintrag löschen")
    verwaltung.deleteEintrag(2, 1)  # Lösche den Eintrag mit eintragid 2
    eintraege = verwaltung.fetchAllEintraege(1)
    print(eintraege)

    # Test 12: Plan umbenennen
    print("\nTest 12: Plan umbenennen")
    verwaltung.renamePlan(1, 'Neuer Haushaltsplan')
    # Überprüfen, ob der Plan umbenannt wurde
    verwaltung.cursor.execute("SELECT name FROM Haushaltsplaene WHERE id = 1")
    print("Neuer Name des Plans:", verwaltung.cursor.fetchone())

    verwaltung.close()

# Führe die Tests aus
test_haushaltsverwaltung()