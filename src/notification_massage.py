from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()

def notification_message(message):
    MAIN_INI_FILE.set_database_value('INFO', 'current_backing_up', f'{message}')


if __name__ == '__main__':
    pass