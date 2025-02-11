import sqlite3

connection = sqlite3.connect("test.db")

print(connection.total_changes)

cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Haushaltsplaene (id integer PRIMARY KEY AUTOINCREMENT, name text)")

cursor.execute("CREATE TABLE IF NOT EXISTS Eintraege (eintragid INTEGER PRIMARY KEY AUTOINCREMENT, planid INTEGER,"
               " name TEXT, wert REAL, bereich TEXT, typ TEXT, datum TEXT,"
               "FOREIGN KEY(planid) REFERENCES Haushaltsplaene(id))")



cursor.execute("INSERT INTO Haushaltsplaene VALUES (1, 'Test')")
cursor.execute("INSERT INTO Eintraege VALUES (1, 1, 'Test blyad', 124.25, 'Bullshit', 'Testküche', '11.02.2025')")

print(connection.total_changes)

cursor.execute("SELECT * FROM Eintraege")
rows = cursor.fetchall()
for row in rows:
    print(row)