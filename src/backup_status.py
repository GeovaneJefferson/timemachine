from setup import *
from read_ini_file import UPDATEINIFILE


MAIN_INI_FILE = UPDATEINIFILE()

def progress_bar_status():
    try:
        progress_value = MAIN_INI_FILE.get_database_value("STATUS", "progress_bar")
        
        if progress_value is not None:
            return str(f'{progress_value:.1f}% done.')
        else:
            return "Progress value not available."  # or any default value or message you prefer
    except Exception as e:
        # Save error log
        MAIN_INI_FILE.report_error(e)