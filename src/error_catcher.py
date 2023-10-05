from setup import *
from read_ini_file import UPDATEINIFILE

MAIN_INI_FILE = UPDATEINIFILE()

def signal_exit(*args):
    # Set unafineshed backup to Yes
    # MAIN_INI_FILE.set_database_value('STATUS', 'unfinished_backup', 'Yes')
    
    if args:
        messages = args  # Use the entire args tuple as a list
        print("All messages are:", messages)
    
    else:
        print("No messages provided.")

    # Check if location exist
    if not os.path.exists(LOG_LOCATION):
        # Create file
        sub.run(
            ['touch', LOG_LOCATION],
            stdout=sub.PIPE,
            stderr=sub.PIPE)
        
    with open(LOG_LOCATION, 'w') as writer:
        writer.write(str(messages))
        
def error_trying_to_backup(e):
    MAIN_INI_FILE.set_database_value('INFO', 'saved_notification', f'{e}')
    exit()