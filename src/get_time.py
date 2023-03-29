from setup import *
from read_ini_file import UPDATEINIFILE


def get_date_time():
    mainIniFile = UPDATEINIFILE()
    timeFolder = f"{str(mainIniFile.day_name())}-{str(mainIniFile.current_month())}-{str(mainIniFile.current_year())}/{str(mainIniFile.current_hour())}-{str(mainIniFile.current_minute())}"
    return timeFolder

def get_date():
    mainIniFile = UPDATEINIFILE()
    dateFolder = f"{str(mainIniFile.current_date())}-{str(mainIniFile.current_month())}-{str(mainIniFile.current_year())}"
    return dateFolder

def latest_time_info():
    mainIniFile = UPDATEINIFILE()
    lastestTimeInfo = f'{str(mainIniFile.day_name())}, {str(mainIniFile.current_hour())}:{str(mainIniFile.current_minute())}'
    return lastestTimeInfo

def today_date():
    dateTime = datetime.now()
    todayDate = dateTime.strftime("%d-%m-%y")
    return todayDate

def current_time():
    dateTime = datetime.now()
    currentTime = dateTime.strftime("%H:%M")
    return currentTime
