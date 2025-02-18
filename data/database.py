import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta



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
        erzeugungsZeit = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        # Einfügen der Haushaltspläne
        self.cursor.execute(f"INSERT OR IGNORE INTO Haushaltsplaene (id, name, lastChecked) VALUES (1, 'Haushaltsplan Beispiel', '{erzeugungsZeit}')")
        self.cursor.execute(f"INSERT OR IGNORE INTO Haushaltsplaene (id, name, lastChecked) VALUES (2, 'Haushaltsplan (inaktiv)', '{erzeugungsZeit}')")
        self.cursor.execute(f"INSERT OR IGNORE INTO Haushaltsplaene (id, name, lastChecked) VALUES (3, 'Haushaltsplan (inaktiv)', '{erzeugungsZeit}')")

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
        self.cursor.execute("INSERT OR IGNORE INTO Eintraege (eintragid,  planid, name, wert, bereich, typ, datum, reihe) VALUES (1, 1, 'Gehalt', 2500, 'Arbeit', 'Einkommen', '12-01-2025', 1)")
        self.cursor.execute("INSERT OR IGNORE INTO Eintraege (eintragid, planid, name, wert, bereich, typ, datum, reihe) VALUES (2, 1, 'Asiatisch Essen', 30, 'Verpflegung', 'Ausgaben', '12-01-2025', 1)")
        self.cursor.execute("INSERT OR IGNORE INTO Eintraege (eintragid, planid, name, wert, bereich, typ, datum, reihe) VALUES (3, 1, 'Europa Park', 250, 'Freizeit', 'Ausgaben', '12-01-2025', 1)")

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

    def autoAddEntry(self, oldTime, planid):
        currentTime = datetime.now()
        result = self.cursor.execute("""SELECT e.datum, r.von, r.bis, r.intervall, e.wert, e.name, e.typ, e.bereich, r.reihenID FROM Reihe r
        JOIN Eintraege e ON r.eintragid = e.eintragid WHERE planid = ?
        """, (planid,))
        for value in result:
            datumVon = datetime.strptime(value[1], "%d-%m-%Y")
            datumBis = datetime.strptime(value[2], "%d-%m-%Y")
            if currentTime > datumVon and oldTime < datumBis:
                eintragDatum = datetime.strptime(value[0], "%d-%m-%Y")
                match value[3]:
                    case "täglich":
                        intervall = relativedelta(days=1)
                    case "wöchentlich":
                        intervall = relativedelta(weeks=1)
                    case "monatlich":
                        intervall = relativedelta(months=1)
                    case "jährlich":
                        intervall = relativedelta(years=1)

                nextDate = eintragDatum + intervall
                i = 0
                while (i < 5000):
                    if nextDate > datumVon and nextDate < datumBis and nextDate < currentTime and nextDate > oldTime:
                        nextEntryDatum = datetime.strftime(nextDate, "%d-%m-%Y")
                        Haushaltsverwaltung.addEintrag(self, planid, value[5], value[4], value[7], value[6], nextEntryDatum, value[8])
                    if nextDate > currentTime:
                        break
                    nextDate = nextDate + intervall
                    i = i + 1








    def updateLastChecked(self, planid):
        # Aktuelles Datum und Uhrzeit abrufen
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        oldTime = Haushaltsverwaltung.lastChecked(self, planid)
        if oldTime.year < datetime.now().year or oldTime.month < datetime.now().month or oldTime.day < datetime.now().day:
            Haushaltsverwaltung.autoAddEntry(self, oldTime, planid)
        # SQL-Update-Anweisung ausführen
        self.cursor.execute("UPDATE Haushaltsplaene SET lastChecked = ? WHERE id = ?", (current_time, planid))
        self.conn.commit()

    def lastChecked(self, planID):
        currentTime = self.cursor.execute("SELECT lastChecked FROM Haushaltsplaene WHERE id = ?", (planID, ))
        currentTime = currentTime.fetchone()[0]
        currentTime = datetime.strptime(currentTime, "%d-%m-%Y %H:%M:%S")
        return currentTime



    def fetchEntryByReihenID(self, reihenID):
        query = """
        SELECT e.*
        FROM Eintraege e
        JOIN Reihe r ON e.eintragid = r.eintragID
        WHERE r.reihenID = ?
        """
        self.cursor.execute(query, (reihenID,))
        return self.cursor.fetchone()  # Gibt die erste gefundene Zeile zurück



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




    def fetchAllEintraege(self, planid, sort_by=None, filter_name=None, filter_bereich=None,
                          filter_typ=None, filter_date=None, filter_wert_von=None, filter_wert_bis=None):
        Haushaltsverwaltung.updateLastChecked(self, planid)
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


#test = Haushaltsverwaltung()
#eintragstest = test.fetchAllEintraege(1)
#print(eintragstest)
#test.close()



