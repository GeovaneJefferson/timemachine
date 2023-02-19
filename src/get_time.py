from setup import *

dateTime = datetime.now()
dateDay = dateTime.strftime("%d")
dateMonth = dateTime.strftime("%m")
dateYear = dateTime.strftime("%y")
dayName = dateTime.strftime("%a")
currentHour = dateTime.strftime("%H")
currentMinute = dateTime.strftime("%M")

def get_date_time():
    timeFolder = f"{dateDay}-{dateMonth}-{dateYear}/{currentHour}-{currentMinute}"
    return timeFolder

def get_date():
    dateFolder = f"{dateDay}-{dateMonth}-{dateYear}"
    return dateFolder

def latest_time_info():
    lastestTimeInfo = f'{dayName}, {currentHour}:{currentMinute}'
    return lastestTimeInfo

def today_date():
    todayDate = dateTime.strftime("%d-%m-%y")
    return todayDate

def current_time():
    currentTime = dateTime.strftime("%H:%M")
    return currentTime
