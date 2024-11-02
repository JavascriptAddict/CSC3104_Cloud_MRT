from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import DictCursor
import os

load_dotenv()

class TripDB:
    def __init__(self):
        database_url = os.getenv('TRIP_DATABASE_URL')
        self.conn = psycopg2.connect(database_url)
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        self.initializeDB()

    def initializeDB(self):
        """Creates the trips table if it doesn't exist."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            tripId TEXT PRIMARY KEY,
            accountId TEXT,
            entry TEXT,
            exit TEXT,
            timestamp TIMESTAMP
            )""")
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def createTrip(self, userObj):
        try:
            sql = '''INSERT INTO trips ("tripId", "accountId", "entry", "exit", "timestamp") VALUES(%s,%s,%s,%s,%s)'''
            self.cursor.execute(sql, userObj)
            self.conn.commit()
            return self.cursor.lastrowid
        except psycopg2.DatabaseError as e:
            print(f"Database error: {e}")
            return False

    def updateTrip(self, userObj):
        try:
            sql = '''UPDATE trips
            SET "entry" = %s, "exit" = %s
            WHERE "tripId" = %s'''
            self.cursor.execute(sql, (userObj['entry'], userObj['exit'], userObj['tripId']))
            self.conn.commit()
            return self.cursor.rowcount #return the number of rows affected
        except psycopg2.DatabaseError as e:
            print(f"Database error: {e}")
            return False

    def getTrip(self, accountId):
        try:
            sql = '''SELECT * FROM trips where "accountId" = %s'''
            self.cursor.execute(sql, (accountId,))
            rows = self.cursor.fetchall()
            if rows is None:
                return None

            # Convert the timestamp to a string
            for row in rows:
                if row["timestamp"] is not None:
                    row["timestamp"] = row["timestamp"].isoformat()
            return rows
        except psycopg2.DatabaseError as e:
            print(f"Database error: {e}")
            return False

    def getTripByUserId(self, userId):
        try:
            sql = '''SELECT * FROM trips where "accountId" = %s AND (exit = %s)'''
            self.cursor.execute(sql, (userId,"",))
            row = self.cursor.fetchone()
            if row is None:
                return None
            if row["timestamp"] is not None:
                row["timestamp"] = row["timestamp"].isoformat()  # Convert to string format
            return row
        except psycopg2.DatabaseError as e:
            print(f"Database error: {e}")
            return False

    def deleteTrip(self, userId):
        #I don't think it's right to be able to delete trip records
        pass

