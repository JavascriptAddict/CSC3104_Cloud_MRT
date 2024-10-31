from dotenv import load_dotenv
import psycopg2
import os
from psycopg2.extras import DictCursor

load_dotenv()

class TransactionDB:
    def __init__(self):

        database_url = os.getenv('TRANSACTION_DATABASE_URL')
        self.conn = psycopg2.connect(database_url)
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS transactions (
            "transactionId" TEXT NOT NULL,
            amount NUMERIC(5,2) NOT NULL,
            "accountId" TEXT NOT NULL,
            "timestamp" TIMESTAMP WITHOUT TIME ZONE,
            CONSTRAINT transaction_pkey PRIMARY KEY ("transactionId")
        )
        '''
        
        # Execute the CREATE TABLE statement
        self.cursor.execute(create_table_sql)
        self.conn.commit()
        print("Table 'transactions' created successfully.")

    def createTransaction(self, userObj):
        sql = '''INSERT INTO transactions ("transactionId", amount, "accountId", "timestamp") 
                 VALUES (%s, %s, %s, %s) RETURNING "transactionId"'''
        self.cursor.execute(sql, userObj)
        self.conn.commit()
        return self.cursor.fetchone()['transactionId']

    def updateTransaction(self, userObj):
        sql = '''UPDATE transactions
                 SET amount = %s
                 WHERE "transactionId" = %s'''
        self.cursor.execute(sql, (userObj['amount'], userObj['transactionId']))
        self.conn.commit()
        return self.cursor.rowcount #return the number of rows affected

    def getTransaction(self, transactionId):
        sql = '''SELECT * FROM transactions WHERE "transactionId" = %s'''
        self.cursor.execute(sql, (transactionId,))
        row = self.cursor.fetchone()

        if row is None:
            return None

        if row["timestamp"] is not None:
            row["timestamp"] = row["timestamp"].isoformat()  # Convert to string format
            
        return row

    def deleteTransaction(self, transactionId):
        sql = '''DELETE FROM transactions WHERE "transactionId" = %s'''
        self.cursor.execute(sql, (transactionId,))
        self.conn.commit()
        return self.cursor.rowcount  # Return the number of rows affected

    def close(self):
        self.cursor.close()
        self.conn.close()
