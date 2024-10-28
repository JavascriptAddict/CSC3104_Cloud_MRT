import sqlite3
import os

path = os.path.dirname(os.path.realpath(__file__))

class AccountDB:
    def __init__(self):
        self.conn = sqlite3.connect(path + '/account.db')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.initializeDB()

    def initializeDB(self):
        """Creates the accounts table if it doesn't exist."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            userId TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            nric TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            accountStatus BOOLEAN NOT NULL,
            walletId TEXT,
            walletAmount FLOAT
        )
        """)
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()
    
    def getAccountById(self, userId):
        """Fetch account details by userId."""
        self.cursor.execute("SELECT * FROM accounts WHERE userId = ?", (userId,))
        result = self.cursor.fetchone()
        if result:
            return dict(result)
        return False

    def getAccountByUsername(self, username):
        """Fetch account details by userId."""
        self.cursor.execute("SELECT * FROM accounts WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        if result:
            return dict(result)
        return False

    def createAccount(self, createData):
        """Insert a new account into the database."""
        try:
            self.cursor.execute("""
                INSERT INTO accounts (name, nric, username, password, accountStatus, userId, walletId, walletAmount) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, createData)
            self.conn.commit()
            return self.getAccountById(createData[-3])  # Return created account using userId
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def updateAccount(self, userId, updateData):
        """Update account information for the given userId."""
        try:
            self.cursor.execute("""
                UPDATE accounts 
                SET name = ?, nric = ?, username = ? 
                WHERE userId = ?
            """, (updateData['name'], updateData['nric'], updateData['username'], userId))
            self.conn.commit()
            return self.cursor.rowcount > 0  # True if the account was updated
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def deleteAccount(self, userId):
        """Delete account by userId."""
        try:
            self.cursor.execute("DELETE FROM accounts WHERE userId = ?", (userId,))
            self.conn.commit()
            return self.cursor.rowcount > 0  # True if the account was deleted
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
