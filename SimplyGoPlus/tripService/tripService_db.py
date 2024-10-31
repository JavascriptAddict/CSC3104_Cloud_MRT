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
        # Create table if it does not exist
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS trips (
                "tripId" TEXT NOT NULL,
                "accountId" TEXT NOT NULL,
                entry TEXT NOT NULL,
                exit TEXT,
                "timestamp" TIMESTAMP WITHOUT TIME ZONE,
                CONSTRAINT trip_pkey PRIMARY KEY ("tripId"))'''
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def createTrip(self, userObj):
        sql = '''INSERT INTO trips ("tripId", "accountId", "entry", "exit", "timestamp") VALUES(%s,%s,%s,%s,%s)'''
        self.cursor.execute(sql, userObj)
        self.conn.commit()
        return self.cursor.lastrowid

    def updateTrip(self, userObj):
        sql = '''UPDATE trips
        SET "entry" = %s, "exit" = %s
        WHERE "tripId" = %s'''
        self.cursor.execute(sql, (userObj['entry'], userObj['exit'], userObj['tripId']))
        self.conn.commit()
        return self.cursor.rowcount #return the number of rows affected

    def getTrip(self, tripId):
        sql = '''SELECT * FROM trips where "tripId" = %s'''
        self.cursor.execute(sql, (tripId,))
        row = self.cursor.fetchone()

        if row is None:
            return None

        # Convert the timestamp to a string
        if row["timestamp"] is not None:
            row["timestamp"] = row["timestamp"].isoformat()  # Convert to string format
        return row

    def deleteTrip(self, userId):
        #I don't think it's right to be able to delete trip records
        pass

