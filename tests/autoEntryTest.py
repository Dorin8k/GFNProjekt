import unittest
import sqlite3
from data.database import Haushaltsverwaltung
from datetime import datetime, timedelta


def testAutoAddDays():
    test = Haushaltsverwaltung()
    test.addEintrag(1, 'Automatisch Gehalt', 2500, 'Arbeit', 'Einkommen', '12.01.2024', 'monatlich', '12.01.2024', '21.02.2025')
    test.addEintrag(1, 'Automatisch Asiatisch Essen', 30, 'Verpflegung', 'Ausgaben', '12.01.2024', 'jährlich', '12.01.2024', '21.02.2025')
    test.addEintrag(1, 'Automatisch Europa Park', 250, 'Freizeit', 'Ausgaben', '12.01.2025', 'wöchentlich', '12.01.2025', '21.02.2025')

    test.cursor.execute("UPDATE Haushaltsplaene SET lastChecked = '12.01.2024 12:00:00' WHERE id = 1")
    print (test.fetchAllEintraege(1))


testAutoAddDays()

