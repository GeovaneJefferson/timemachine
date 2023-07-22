from setup import *
from read_ini_file import UPDATEINIFILE


def get_date_time():
    MAIN_INI_FILE=UPDATEINIFILE()
    return f"{str(MAIN_INI_FILE.day_name())}-{str(MAIN_INI_FILE.current_month())}-{str(MAIN_INI_FILE.current_year())}/{str(MAIN_INI_FILE.current_hour())}-{str(MAIN_INI_FILE.current_minute())}"

def get_date():
    MAIN_INI_FILE=UPDATEINIFILE()
    return f"{str(MAIN_INI_FILE.current_date())}-{str(MAIN_INI_FILE.current_month())}-{str(MAIN_INI_FILE.current_year())}"

def latest_time_info():
    MAIN_INI_FILE=UPDATEINIFILE()
    return f'{str(MAIN_INI_FILE.day_name())}, {str(MAIN_INI_FILE.current_hour())}:{str(MAIN_INI_FILE.current_minute())}'

def today_date():
    date_time=datetime.now()
    return date_time.strftime("%d-%m-%y")

def current_time():
    date_time=datetime.now()
    return date_time.strftime("%H:%M")


if __name__ == '__main__':
    pass