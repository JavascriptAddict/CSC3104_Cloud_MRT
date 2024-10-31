from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import DictCursor
import os

load_dotenv()

class AccountDB:
    def __init__(self):
        database_url = os.getenv('ACCOUNT_DATABASE_URL')
        self.conn = psycopg2.connect(database_url)
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)

        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS public.account (
            "accountId" TEXT NOT NULL,
            "name" TEXT NOT NULL,
            "nric" TEXT NOT NULL,
            "username" TEXT NOT NULL,
            "password" TEXT NOT NULL,
            "accountStatus" BOOLEAN NOT NULL,
            "walletAmount" NUMERIC(5,2),
            CONSTRAINT account_pkey PRIMARY KEY ("accountId")
        )
        '''
        try:
            self.cursor.execute(create_table_sql)
            self.conn.commit()
            print("Table 'accounts' created successfully.")
        except psycopg2.Error as e:
            print(f"Database error during table creation: {e}")
            self.conn.rollback()
    
    def getAccountById(self, accountId):
        """Fetch account details by accountId."""
        try:
            sql = 'SELECT * FROM public.account WHERE "accountId" = %s'
            self.cursor.execute(sql, (accountId,))
            result = self.cursor.fetchone()
            return dict(result) if result else False
        except psycopg2.Error as e:
            print(f"Database error during getAccountById: {e}")
            self.conn.rollback()
            return False

    def getAccountByUsername(self, username):
        """Fetch account details by username."""
        try:
            sql = 'SELECT * FROM public.account WHERE "username" = %s'
            self.cursor.execute(sql, (username,))
            result = self.cursor.fetchone()
            return dict(result) if result else False
        except psycopg2.Error as e:
            print(f"Database error during getAccountByUsername: {e}")
            self.conn.rollback()
            return False

    def createAccount(self, accountData):
        """Insert a new account into the database."""
        sql = '''
            INSERT INTO public.account ("accountId", "name", "nric", "username", "password", "accountStatus", "walletAmount") 
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING "accountId"
        '''
        try:
            self.cursor.execute(sql, accountData)
            self.conn.commit()
            return self.getAccountById(accountData[0])  # Return created account using accountId
        except psycopg2.Error as e:
            print(f"Database error during createAccount: {e}")
            self.conn.rollback()
            return False

    def updateAccount(self, accountId, updateData):
        """Update account information for the given accountId."""
        sql = '''
            UPDATE public.account 
            SET "name" = %s, "nric" = %s, "username" = %s
            WHERE "accountId" = %s
        '''
        try:
            # Use individual values instead of dictionary
            self.cursor.execute(sql, (updateData['name'], updateData['nric'], updateData['username'], accountId))
            self.conn.commit()
            return self.cursor.rowcount > 0  # True if the account was updated
        except psycopg2.Error as e:
            print(f"Database error during updateAccount: {e}")
            self.conn.rollback()
            return False

    def updateWallet(self, userId, amount):
        """Update wallet information for the given userId."""
        try:
            self.cursor.execute("""
                UPDATE accounts 
                SET walletAmount = ?
                WHERE userId = ?
            """, (amount, userId))
            self.conn.commit()
            return self.cursor.rowcount > 0  # True if the account was updated
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        
    def deleteAccount(self, userId):
        """Delete account by userId."""
        try:
            self.cursor.execute(sql, (accountId,))
            self.conn.commit()
            return self.cursor.rowcount > 0  # True if the account was deleted
        except psycopg2.Error as e:
            print(f"Database error during deleteAccount: {e}")
            self.conn.rollback()
            return False
    
    def close(self):
        self.cursor.close()
        self.conn.close()
