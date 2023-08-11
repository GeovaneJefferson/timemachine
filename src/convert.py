import sqlite3
import configparser

# Load INI data
config = configparser.ConfigParser()
config.read('config.ini')

# Connect to the SQLite database
conn = sqlite3.connect('config.db')
cursor = conn.cursor()

# Create a table to store the INI data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS config (
        section TEXT,
        key TEXT,
        value TEXT
    )
''')

# Insert INI data into the database
for section in config.sections():
    for key, value in config.items(section):
        cursor.execute('''
            INSERT INTO config (section, key, value)
            VALUES (?, ?, ?)
        ''', (section, key, value))

# Commit changes and close the connection
conn.commit()
conn.close()
