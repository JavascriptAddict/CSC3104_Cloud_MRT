import sqlite3
import os

path = os.path.dirname(os.path.realpath(__file__))

class TransactionDB:
    def __init__(self):
        self.conn = sqlite3.connect(path + '/transaction.db')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
                    (transactionId varchar(255) PRIMARY KEY, 
                    amount NUMERIC(5, 2),
                    accountId varchar(255), 
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    def createTransaction(self, userObj):
        sql = '''INSERT INTO transactions (transactionId, amount, accountId, timestamp) VALUES(?,?,?,?)'''
        self.cursor.execute(sql, userObj)
        self.conn.commit()
        return self.cursor.lastrowid

    def updateTransaction(self, userObj):
        sql = '''UPDATE transactions
        SET amount = ?
        WHERE transactionId = ?'''
        self.cursor.execute(sql, (userObj['amount'], userObj['transactionId']))
        self.conn.commit()
        return self.cursor.rowcount #return the number of rows affected

    def getTransaction(self, userId):
        sql = '''SELECT * FROM transaction_record where accountId = ?'''
        self.cursor.execute(sql, (userId,))
        rows = self.cursor.fetchall()
        if rows is None:
            return None
        return rows

    def deleteTransaction(self, userId):
        #I don't think it's right to be able to delete transaction records
        pass