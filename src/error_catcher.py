from setup import *
from read_ini_file import UPDATEINIFILE
from create_directory import create_directory, create_file


MAIN_INI_FILE = UPDATEINIFILE()

def signal_exit(*args):
    # Set unafineshed backup to Yes
    # MAIN_INI_FILE.set_database_value('STATUS', 'unfinished_backup', 'Yes')
    
    if args:
        messages = args  # Use the entire args tuple as a list
        print("All messages are:", messages)
    
    else:
        print("No messages provided.")
    
    # Check if the directory exists, and create it if necessary
    create_directory(LOG_LOCATION)
    # Check if the file exists, and create it if necessary
    create_file(LOG_LOCATION)

    # Write bug in to it
    with open(LOG_LOCATION, 'w') as writer:
        writer.write(str(messages))
        
def error_trying_to_backup(e):
    MAIN_INI_FILE.set_database_value('INFO', 'saved_notification', f'{e}')
    exit()