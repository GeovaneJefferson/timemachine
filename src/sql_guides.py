from setup import *
import sqlite3


# def connect_to_database():
#     # Connect to the SQLite database
#     conn = sqlite3.connect(SRC_USER_CONFIG_DB)
#     cursor = conn.cursor()


def update_database(section, key, value):
    cursor.execute('''
        UPDATE app_settings
        SET value = ?
        WHERE section = ? AND key = ?
    ''', (value, section, key))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def get_ini_folders(section, key, value):
    # Insert or replace data into the table
    cursor.execute(f'''
        INSERT OR REPLACE INTO {section} ({key}, {value})
        VALUES (?, ?)
    ''', (key, value))

    # Commit changes and close the connection
    conn.commit()
    conn.close()


def create_table(table):
    # Connect to the SQLite database
    conn = sqlite3.connect(SRC_USER_CONFIG_DB)
    cursor = conn.cursor()

    # Create table STATUS
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table} (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')

def add_to_table(table, key, value):      
    # Connect to the SQLite database
    conn = sqlite3.connect(SRC_USER_CONFIG_DB)
    cursor = conn.cursor()
          
    cursor.execute(f'''
        INSERT OR REPLACE INTO {table} (key, value)
        VALUES (?, ?)
    ''', (f'{key}', f'{value}'))

    conn.commit()
    # conn.close()

def print_status_data(table):
    # Connect to the SQLite database
    conn = sqlite3.connect(SRC_USER_CONFIG_DB)
    cursor = conn.cursor()
  
    # Execute a query to fetch all rows from the table
    query = f"SELECT * FROM {table}"
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Fetch column names
    column_names = [description[0] for description in cursor.description]

    # Close the connection
    conn.close()

    # Print the keys and values for each row
    for row in rows:
        print("Row:")
        for col_name, value in zip(column_names, row):
            print(f"{col_name}: {value}")(f"{column_names}: {value}")

def clear_db():
    if os.path.exists(SRC_USER_CONFIG_DB):
        os.remove(SRC_USER_CONFIG_DB)

def remove_key(table, key):
    # Connect to the SQLite database
    conn = sqlite3.connect(SRC_USER_CONFIG_DB)
    cursor = conn.cursor()

    # Call the function to print 'STATUS' data
    # Key to remove

    # Delete the key-value pair from the 'STATUS' table
    cursor.execute(f'DELETE FROM {table} WHERE key = ?', (f'{key}',))

    # Commit changes and close the connection
    conn.commit()
    conn.close()


def print_all_tables_data():
    # Connect to the SQLite database
    conn = sqlite3.connect(SRC_USER_CONFIG_DB)
    cursor = conn.cursor()

    # Get the list of all table names in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = cursor.fetchall()

    # Loop through each table
    for table_name in table_names:
        table_name = table_name[0]  # Extract the table name from the tuple

        print(f"Table: {table_name}")

        # Query all data from the current table
        cursor.execute(f"SELECT key, value FROM {table_name}")
        table_data = cursor.fetchall()

        # Print data for the current table
        for key, value in table_data:
            print(f"  {key}: {value}")

    # Close the connection
    conn.close()

def get_database_value(table, key):
    # Connect to the SQLite database
    conn = sqlite3.connect(SRC_USER_CONFIG_DB)
    cursor = conn.cursor()

    # Query the value from the specified table and key
    cursor.execute(f"SELECT value FROM {table} WHERE key = ?", (key,))
    result = cursor.fetchone()

    # Close the connection
    conn.close()

    if result:
        return result[0]  # The value is the first element in the result tuple
    else:
        return None  # Return None if the key doesn't exist

# create_table('RESTORE')
# add_to_table('RESTORE', 'system_settings', 'False')
# print_status_data('RESTORE')
# print(get_database_value('RESTORE', 'applications_packages'))
print(print_all_tables_data())

# True
# False
# None
def get_keys_from_table():
    # Connect to the SQLite database
    conn = sqlite3.connect(SRC_USER_CONFIG_DB)
    cursor = conn.cursor()

    # Query all keys from the specified table
    cursor.execute(f"SELECT key FROM RESTORE")
    keys = [row[0] for row in cursor.fetchall()]

    # Close the connection
    conn.close()


    for key in keys:
        print(key)

# get_keys_from_table()

# import sqlite3
# import configparser

# # Load INI data
# config = configparser.ConfigParser()
# config.read('config.ini')

# # Connect to the SQLite database
# conn = sqlite3.connect('config.db')
# cursor = conn.cursor()

# # Create a table to store the INI data
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS config (
#         section TEXT,
#         key TEXT,
#         value TEXT
#     )
# ''')

# # Insert INI data into the database
# for section in config.sections():
#     for key, value in config.items(section):
#         cursor.execute('''
#             INSERT INTO config (section, key, value)
#             VALUES (?, ?, ?)
#         ''', (section, key, value))

# # Commit changes and close the connection
# conn.commit()
# conn.close()

# #  #################################
# # Connect to the SQLite database
# conn = sqlite3.connect('config.db')
# cursor = conn.cursor()

# # Query the database for the value of 'unfinished_backup' in the 'STATUS' section
# section = 'STATUS'
# key = 'unfinished_backup'

# cursor.execute('''
#     SELECT value
#     FROM config
#     WHERE section = ? AND key = ?
# ''', (section, key))


# print(cursor.fetchone()[0])

# # Close the connection
# conn.close()


print(get_keys_from_table())