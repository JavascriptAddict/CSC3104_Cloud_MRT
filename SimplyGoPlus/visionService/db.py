from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import DictCursor
import os

load_dotenv()

class VisionDB:
    def __init__(self):
        database_url = os.getenv('VISION_DATABASE_URL')
        self.conn = psycopg2.connect(database_url)
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        self.initializeDB()


    def initializeDB(self):
        """Creates the visions table if it doesn't exist."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS visions (
            "userId" TEXT PRIMARY KEY,
            image bytea
            )""")
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()
    
    def getAllEmbeddings(self):
        """Fetch vision details by userId."""
        self.cursor.execute("SELECT * FROM visions")
        result = self.cursor.fetchall()
        if len(result) == 0:
            return False
        return result

    def createEmbedding(self, createData):
        """Insert a new vision into the database."""
        try:
            sql = '''INSERT INTO visions ("userId", "image") VALUES(%s,%s)'''
            self.cursor.execute(sql, createData)
            self.conn.commit()
            return self.cursor.lastrowid
        except psycopg2.DatabaseError as e:
            print(f"Database error: {e}")
            return False

    def updateEmbedding(self, userId, updateData):
        """Update vision information for the given userId."""
        try:
            sql = '''UPDATE visions SET "image" = %s WHERE "userId" = %s'''
            self.cursor.execute(sql, (updateData['image']))
            self.conn.commit()
            return self.cursor.rowcount > 0  # True if the vision was updated
        except psycopg2.DatabaseError as e:
            print(f"Database error: {e}")
            return False

    def deleteEmbedding(self, userId):
        """Delete vision by userId."""
        try:
            sql = '''DELETE FROM visions WHERE "userId" = %s'''
            self.cursor.execute(sql, (userId,))
            self.conn.commit()
            return self.cursor.rowcount > 0  # True if the vision was deleted
        except psycopg2.DatabaseError as e:
            print(f"Database error: {e}")
            return False
