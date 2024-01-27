from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()

def progress_bar_status():
    try:
        return str(f'{MAIN_INI_FILE.get_database_value("STATUS", "progress_bar"):.1f}% done.') 
    except Exception as e:
        # Save error log
        MAIN_INI_FILE.report_error(e)

    # f'{MAIN_INI_FILE.get_database_value('STATUS', 'progress_bar'):.1f}% done - {converted_size:.2f} GB left to be copied.') 