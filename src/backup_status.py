from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()

def progress_bar_status():
    return str(f'{MAIN_INI_FILE.get_database_value("STATUS", "progress_bar"):.1f}% done.') 

    # f'{MAIN_INI_FILE.get_database_value('STATUS', 'progress_bar'):.1f}% done - {converted_size:.2f} GB left to be copied.') 


if __name__ == '__main__':
    pass