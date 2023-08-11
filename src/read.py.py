import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('config.db')
cursor = conn.cursor()

# Query the database for the value of 'unfinished_backup' in the 'STATUS' section
section = 'STATUS'
key = 'unfinished_backup'

cursor.execute('''
    SELECT value
    FROM config
    WHERE section = ? AND key = ?
''', (section, key))


print(cursor.fetchone()[0])

# Close the connection
conn.close()
