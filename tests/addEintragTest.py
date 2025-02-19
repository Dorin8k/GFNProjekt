import random
from datetime import datetime, timedelta
from data.database import Haushaltsverwaltung

def test_addEintrag(haushaltsverwaltung):
    # Aktuelles Datum
    today = datetime.now()

    # Erstelle 5 einmalige Einträge
    for i in range(5):
        name = f"Einmaliger Eintrag {i + 1}"
        wert = round(random.uniform(10, 100), 2)  # Zufälliger Wert zwischen 10 und 100
        bereich = random.choice(['Essen', 'Transport', 'Freizeit', 'Sonstiges'])
        typ = random.choice(['Ausgaben', 'Einkommen'])
        datum = today + timedelta(days=random.randint(1, (30 + 31)))  # Zufälliges Datum in den nächsten 30-61 Tagen
        datum_str = datum.strftime("%d.%m.%Y")

        haushaltsverwaltung.addEintrag(planid=1, name=name, wert=wert, bereich=bereich, typ=typ, datum=datum_str, reihe=None)

    # Erstelle 5 wiederkehrende Einträge
    for i in range(5):
        name = f"Wiederkehrender Eintrag {i + 1}"
        wert = round(random.uniform(10, 100),2)  # Zufälliger Wert zwischen 10 und 100
        bereich = random.choice(['Essen', 'Transport', 'Freizeit', 'Sonstiges'])
        typ = random.choice(['Ausgaben', 'Einkommen'])
        von = today.strftime("%d.%m.%Y")  # Startdatum ist heute
        bis = (today + timedelta(days=random.randint(30, 60))).strftime("%d.%m.%Y")  # Enddatum in 30-60 Tagen
        intervall = random.choice(['täglich', 'wöchentlich', 'monatlich'])  # Zufälliges Intervall

        haushaltsverwaltung.addEintrag(planid=1, name=name, wert=wert, bereich=bereich, typ=typ, datum=von, reihe=None, intervall=intervall, von=von, bis=bis)

    # Ausgabe der Einträge
    eintraege = haushaltsverwaltung.fetchAllEintraege(planid=1)
    for eintrag in eintraege:
        print(eintrag)

# Beispielaufruf der Testfunktion
test = Haushaltsverwaltung()
test_addEintrag(test)
test.close()
