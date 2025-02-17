from data.database import Haushaltsverwaltung

# Beispiel für die Verwendung der Funktion
haushaltsverwaltung = Haushaltsverwaltung()
eintrag = haushaltsverwaltung.fetchEntryByReihenID(1)  # Ersetzen Sie 1 durch die gewünschte reihenID
print(eintrag)  # Gibt den Eintrag zurück, der mit der angegebenen reihenID verknüpft ist
haushaltsverwaltung.close()
