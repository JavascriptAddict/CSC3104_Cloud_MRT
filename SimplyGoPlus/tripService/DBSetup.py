import sqlite3

# Create a connection to the database file (if it doesn't exist, it will be created)
conn = sqlite3.connect('trip.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS trip (
    tripId INTEGER PRIMARY KEY, 
    walletId TEXT, 
    amount NUMERIC(5, 2), 
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

# Commit changes
conn.commit()

# Close the connection
conn.close()