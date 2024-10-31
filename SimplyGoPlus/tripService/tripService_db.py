import sqlite3
import os

path = os.path.dirname(os.path.realpath(__file__))

class TripDB:
    def __init__(self):
        self.conn = sqlite3.connect(path + '/trip.db')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS trip_record
                    (tripId varchar(255) PRIMARY KEY,
                    accountId varchar(255),
                    entry varchar(255),
                    exit varchar(255),
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    def createTrip(self, userObj):
        sql = '''INSERT INTO trip_record (tripId, accountId, entry, exit, timestamp) VALUES(?,?,?,?,?)'''
        self.cursor.execute(sql, userObj)
        self.conn.commit()
        return self.cursor.lastrowid

    def updateTrip(self, userObj):
        sql = '''UPDATE trip_record
        SET entry = ?, exit = ?
        WHERE tripId = ?'''
        self.cursor.execute(sql, (userObj['entry'], userObj['exit'], userObj['tripId']))
        self.conn.commit()
        return self.cursor.rowcount #return the number of rows affected

    def getTrip(self, tripId):
        sql = '''SELECT * FROM trip_record where tripId = ?'''
        self.cursor.execute(sql, (tripId,))
        row = self.cursor.fetchone()

        if row is None:
            return None

        return row

    def deleteTrip(self, userId):
        #I don't think it's right to be able to delete trip records
        pass