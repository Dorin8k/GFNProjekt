import sqlite3

connection = sqlite3.connect("test.db")

print(connection.total_changes)

cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Haushaltsplaene (id integer PRIMARY KEY, name text)")

cursor.execute("CREATE TABLE IF NOT EXISTS Eintraege (eintragid INTEGER PRIMARY KEY, planid INTEGER,"
               " name TEXT, wert REAL, bereich TEXT, typ TEXT, datum TEXT,"
               "FOREIGN KEY(planid) REFERENCES Haushaltsplaene(id))")



cursor.execute("INSERT INTO Haushaltsplaene VALUES (1, 'Test')")
cursor.execute("INSERT INTO Eintraege VALUES (1, 1, 'Test blyad', 124.25, 'Bullshit', 'Testküche', '11.02.2025')")

# Erstellen von Haushaltsplan 2 und 3
cursor.execute("INSERT INTO Haushaltsplaene (name) VALUES ('Haushaltsplan 2')")
cursor.execute("INSERT INTO Haushaltsplaene (name) VALUES ('Haushaltsplan 3')")


for i in range(1, 6):  # 5 Einträge für Haushaltsplan 1
    cursor.execute("INSERT INTO Eintraege (planid, name, wert, bereich, typ, datum) VALUES (1, 'Testeintrag {} für Haushaltsplan 1', {}, 'Bereich 1', 'Typ A', '11.02.2025')".format(i, i * 10))

for i in range(1, 6):  # 5 Einträge für Haushaltsplan 2
    cursor.execute("INSERT INTO Eintraege (planid, name, wert, bereich, typ, datum) VALUES (2, 'Testeintrag {} für Haushaltsplan 2', {}, 'Bereich 2', 'Typ B', '11.02.2025')".format(i, i * 20))

# Änderungen speichern
connection.commit()

print(connection.total_changes)


# dreifache Anführungszeichen für Zeilenumbruchfreie Strings
cursor.execute("""
    SELECT Eintraege.eintragid, Haushaltsplaene.name AS haushaltsplan_name, Eintraege.name, Eintraege.wert, Eintraege.bereich, Eintraege.typ, Eintraege.datum
    FROM Eintraege
    JOIN Haushaltsplaene ON Eintraege.planid = Haushaltsplaene.id
""")
rows = cursor.fetchall()

# Ausgabe
for row in rows:
    print(row)