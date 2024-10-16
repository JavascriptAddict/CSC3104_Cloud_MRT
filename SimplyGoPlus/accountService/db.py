import sqlite3
import os

path = os.path.dirname(os.path.realpath(__file__))

class AccountDB:
    def __init__(self):
        self.conn = sqlite3.connect(path + '/account.db')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS accounts
                    (userId varchar(255) PRIMARY KEY, name varchar(255), nric varchar(255), username varchar(255), password varchar(255), accountStatus bool, walletId varchar(255))''')
    def createAccount(self, userObj):
        sql = '''INSERT INTO accounts (name, nric, username, password, accountStatus, userId, walletId) VALUES(?,?,?,?,?,?,?)'''
        self.cursor.execute(sql, userObj)
        self.conn.commit()
        return self.cursor.lastrowid

    def updateAccount(self, userObj):
        pass
    def getAccount(self, userId):
        self.cursor.execute('SELECT * FROM accounts WHERE userId = ?', (userId,))
        row = self.cursor.fetchone()
        return row
    def deleteAccount(self, userId):
        pass