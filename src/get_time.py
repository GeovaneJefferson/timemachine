from setup import *

def get_date_time():
    global dateDay, dateMonth, dateYear, dayName, currentHour, currentMinute
    global dateTime

    dateTime = datetime.now()
    dateDay = dateTime.strftime("%d")
    dateMonth = dateTime.strftime("%m")
    dateYear = dateTime.strftime("%y")
    dayName = dateTime.strftime("%a")
    currentHour = dateTime.strftime("%H")
    currentMinute = dateTime.strftime("%M")

    timeFolder = f"{dateDay}-{dateMonth}-{dateYear}/{currentHour}-{currentMinute}"
    return timeFolder

def get_date():
    dateFolder = f"{dateDay}-{dateMonth}-{dateYear}"
    return dateFolder

def latest_time_info():
    lastestTimeInfo = f'{dayName}, {currentHour}:{currentMinute}'
    return lastestTimeInfo

def today_date():
    todayDate = datetime.now()
    todayDate = todayDate.strftime("%d-%m-%y")
    return todayDate
    



print(get_date_time())
print(get_date())