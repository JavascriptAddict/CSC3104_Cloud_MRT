import sqlite3
import os

path = os.path.dirname(os.path.realpath(__file__))

class VisionDB:
    def __init__(self):
        self.conn = sqlite3.connect(path + '/vision.db')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.initializeDB()

    def initializeDB(self):
        """Creates the visions table if it doesn't exist."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS visions (
            userId TEXT PRIMARY KEY,
            image BLOB
        )
        """)
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()
    
    def getAllEmbeddings(self):
        """Fetch vision details by userId."""
        self.cursor.execute("SELECT * FROM visions")
        result = self.cursor.fetchall()
        if len(result) > 0:
            return result
        return False

    def createEmbedding(self, createData):
        """Insert a new vision into the database."""
        try:
            self.cursor.execute("""
                INSERT INTO visions (userId, image) 
                VALUES (?, ?)
            """, createData)
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def updateEmbedding(self, userId, updateData):
        """Update vision information for the given userId."""
        try:
            self.cursor.execute("""
                UPDATE visions 
                SET image = ?
                WHERE userId = ?
            """, (updateData['image'], userId))
            self.conn.commit()
            return self.cursor.rowcount > 0  # True if the vision was updated
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def deleteEmbedding(self, userId):
        """Delete vision by userId."""
        try:
            self.cursor.execute("DELETE FROM visions WHERE userId = ?", (userId,))
            self.conn.commit()
            return self.cursor.rowcount > 0  # True if the vision was deleted
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
