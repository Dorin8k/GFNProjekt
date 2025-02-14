import sqlite3
from datetime import datetime, timedelta


class Haushaltsverwaltung:
    def __init__(self, database="Haushaltspläne.db"):
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        # Erstellen der Tabelle Haushaltsplaene
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Haushaltsplaene (
            id INTEGER PRIMARY KEY,
            name TEXT,
            lastChecked TEXT
        )
        """)

        # Einfügen der Haushaltspläne
        self.cursor.execute("INSERT OR IGNORE INTO Haushaltsplaene (id, name, lastChecked) VALUES (1, 'Haushaltsplan Beispiel', '2025-02-13')")
        self.cursor.execute("INSERT OR IGNORE INTO Haushaltsplaene (id, name, lastChecked) VALUES (2, 'Haushaltsplan (inaktiv)', '2025-02-13')")
        self.cursor.execute("INSERT OR IGNORE INTO Haushaltsplaene (id, name, lastChecked) VALUES (3, 'Haushaltsplan (inaktiv)', '2025-02-13')")

        # Erstellen der Tabelle Eintraege
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Eintraege (
            eintragid INTEGER PRIMARY KEY,
            planid INTEGER,
            name TEXT,
            wert REAL,
            bereich TEXT,
            typ TEXT,
            datum TEXT,
            reihe INTEGER,
            FOREIGN KEY(planid) REFERENCES Haushaltsplaene (id)
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reihe (
            reihenID INTEGER Primary KEY,
            eintragID INTEGER,
            intervall text,
            von TEXT,
            bis TEXT,
            FOREIGN KEY(eintragID) REFERENCES Eintraege (eintragid)
            
        )
        """)
        #Einfügen von Beispieldaten
        self.cursor.execute("INSERT OR IGNORE INTO Eintraege (eintragid,  planid, name, wert, bereich, typ, datum, reihe) VALUES (1, 1, 'Gehalt', 2500, 'Arbeit', 'Einkommen', '2025-01-12', 1)")
        self.cursor.execute("INSERT OR IGNORE INTO Eintraege (eintragid, planid, name, wert, bereich, typ, datum, reihe) VALUES (2, 1, 'Asiatisch Essen', 30, 'Verpflegung', 'Ausgaben', '2025-01-11', 1)")
        self.cursor.execute("INSERT OR IGNORE INTO Eintraege (eintragid, planid, name, wert, bereich, typ, datum, reihe) VALUES (3, 1, 'Europa Park', 250, 'Freizeit', 'Ausgaben', '2025-01-12', 1)")

        # Änderungen speichern
        self.conn.commit()

    def close(self):
        self.conn.close()

    """
    def getLastEintraegeID(self):
        self.cursor.execute("SELECT MAX(eintragid) FROM Eintraege")
        maxID = self.cursor.fetchone()[0]
        return (maxID + 1) if maxID is not None else 1 #Wenn noch keine ID Vorhanden, nimm 1
    """

    def updateLastChecked(self, planid):
        # Aktuelles Datum und Uhrzeit abrufen
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # SQL-Update-Anweisung ausführen
        self.cursor.execute("UPDATE Haushaltsplaene SET lastChecked = ? WHERE id = ?", (current_time, planid))
        self.conn.commit()

    def lastChecked(self, planID):
        currentTime = self.cursor.execute("SELECT lastChecked FROM Haushaltsplaene WHERE id = ?", (planID, ))
        currentTime = currentTime.fetchone()[0]
        currentTime = datetime.strptime(currentTime, "%d-%m-%Y %H:%M:%S")
        return currentTime


    def formatTimeAgo(lastChecked):
        # Konvertiere den gespeicherten Zeitstempel in ein datetime-Objekt
        last_checked_time = datetime.strptime(lastChecked, "%d-%m-%Y %H:%M:%S")
        current_time = datetime.now()

        # Berechne die Zeitdifferenz
        time_diff = current_time - last_checked_time

        # Bestimme die Zeitspanne in Sekunden
        seconds = time_diff.total_seconds()

        # Formatierung der Ausgabe
        if seconds < 60:
            return f"vor {int(seconds)} Sekunden"
        elif seconds < 3600:  # weniger als eine Stunde
            minutes = seconds // 60
            return f"vor {int(minutes)} Minuten"
        elif seconds < 86400:  # weniger als ein Tag
            hours = seconds // 3600
            return f"vor {int(hours)} Stunden"
        else:  # mehr als ein Tag
            # Gebe das Datum der letzten Änderung im Format "DD-MM-YYYY" zurück
            return last_checked_time.strftime("%d-%m-%Y")

    def renamePlan(self, id, newName):
        self.cursor.execute("UPDATE Haushaltsplaene SET name = ? WHERE id = ?", (newName, id))
        self.conn.commit()


    # Komplette Abänderung eines Eintrags bei Bedarf
    def renameEintrag(self, eintragid, planID, newName, newWert, newBereich, newTyp, newDate):
        self.cursor.execute("""
        UPDATE Eintraege 
        SET name = ?, wert = ?, bereich = ?, typ = ?, datum = ?
        WHERE eintragid = ? AND planid = ?
        """, (newName, newWert, newBereich, newTyp, newDate, eintragid, planID ))
        self.conn.commit()

    def deleteEintrag(self, eintragid, planID):
        self.cursor.execute("DELETE FROM Eintraege WHERE eintragid = ? AND planid = ?", (eintragid, planID))
        self.conn.commit()


    def addEintrag(self, planid, name, wert, bereich, typ, datum, reihe=None, intervall=None, von=None, bis=None):
        self.cursor.execute("INSERT INTO Eintraege (planid, name, wert, bereich, typ, datum, reihe) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (planid, name, wert, bereich, typ, datum, reihe))

        eintragID = (self.cursor.lastrowid) #Generiert die ID für den Eintrag

        if intervall and von and bis:
            self.addWiederkehrende(eintragID, intervall, von, bis)
        self.conn.commit()


    def addWiederkehrende(self, eintragID, intervall, von, bis):
        self.cursor.execute("INSERT INTO Reihe (eintragID, intervall, von, bis) VALUES (?, ?, ?, ?)"
                            , (eintragID, intervall, von, bis))
        self.conn.commit()

    def checkDailies(self, planID):
        currentDay = datetime.now()
        currentMonth = currentDay.month
        currentYear = currentDay.year

        self.cursor.execute("""
        SELECT e.eintragid, e.planid, e.name, e.wert, e.bereich, e.typ, e.reihe, r.intervall , r.von, r.bis
        FROM Eintraege e
        JOIN Reihe r ON e.eintragid = r.eintragID
        WHERE e.planid = ? AND r.intervall = 'täglich'



    """
    def addWiederkehrende(self, eintragID, intervall, von, bis):
        # Aktuelles Datum, Monat und Jahr einholen
        today = datetime.now()
        currentMonth = today.month
        currentYear = today.year

        # Start- und Enddatum konvertieren
        startDate = datetime.strptime(von, "%Y-%m-%d")
        endDate = datetime.strptime(bis, "%Y-%m-%d")
        currentDate = startDate

        while currentDate <= endDate:
            # Überprüfen, ob das aktuelle Datum im aktuellen Monat und Jahr liegt
            if currentDate.month == currentMonth and currentDate.year == currentYear:
                newDate = currentDate.strftime("%Y-%m-%d")
                self.cursor.execute("INSERT INTO Eintraege (planid, name, wert, bereich, typ, datum, reihe) SELECT planid, name, wert, bereich, typ, ?, reihe FROM Eintraege WHERE eintragid = ?", (newDate, eintragID))

            # Erhöhe das Datum je nach Intervall
            if intervall == "täglich":
                currentDate += timedelta(days=1)
            elif intervall == "wöchentlich":
                currentDate += timedelta(weeks=1)
            elif intervall == "monatlich":
                currentDate += timedelta(days=30)  # Grobe Schätzung für einen Monat
            elif intervall == "jährlich":
                currentDate += timedelta(days=365)  # Grobe Schätzung für ein Jahr
            """

    def fetchAllEintraege(self, planid, sort_by=None, filter_name=None, filter_bereich=None,
                          filter_typ=None, filter_date=None, filter_wert_von=None, filter_wert_bis=None):
        # Holt alle Einträge für einen bestimmten Plan, sortiert und gefiltert nach den angegebenen Kriterien.
        query = """
        SELECT e.name, e.wert, e.bereich, e.typ, e.datum, e.reihe, r.intervall, r.von, r.bis 
        FROM Eintraege e
        LEFT JOIN Reihe r ON e.eintragid = r.eintragID
        WHERE e.planid = ?
        """
        params = [planid]

        if filter_name:
            query += " AND e.name LIKE ?"
            params.append(f"%{filter_name}%")  # Wildcard für Teilübereinstimmungen

        if filter_bereich:
            query += " AND e.bereich = ?"
            params.append(filter_bereich)

        if filter_typ:
            query += " AND e.typ = ?"
            params.append(filter_typ)

        if filter_date:
            query += " AND e.datum = ?"
            params.append(filter_date)

        if filter_wert_von is not None:  # Überprüfen ob der filter_wert_von gesetzt ist
            query += " AND e.wert >= ?"
            params.append(filter_wert_von)

        if filter_wert_bis is not None:  # Überprüfen, ob filter_wert_bis gesetzt ist
            query += " AND e.wert <= ?"
            params.append(filter_wert_bis)

        if sort_by:
            query += f" ORDER BY {sort_by}"

        self.cursor.execute(query, params)
        return self.cursor.fetchall()


test = Haushaltsverwaltung()
eintragstest = test.fetchAllEintraege(1)
print(eintragstest)
test.close()



