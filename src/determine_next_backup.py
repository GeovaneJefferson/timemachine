from setup import *
from read_ini_file import UPDATEINIFILE
from languages import determine_days_language
from get_system_language import system_language


def get_next_backup():
    mainIniFile = UPDATEINIFILE()

    # SUN
    if str(mainIniFile.day_name()) == determine_days_language(str(system_language())[0]):
        if str(mainIniFile.ini_next_backup_sun()) == "true" and int(mainIniFile.current_hour()) <= int(mainIniFile.ini_next_hour()) and int(mainIniFile.current_minute()) <= int(mainIniFile.ini_next_minute()):
           return "Today"
        else:
            if str(mainIniFile.ini_next_backup_mon()) == "true":
               return determine_days_language(str(system_language()))[1]
            elif str(mainIniFile.ini_next_backup_tue()) == "true":
               return determine_days_language(str(system_language()))[2]
            elif str(mainIniFile.ini_next_backup_wed()) == "true":
               return determine_days_language(str(system_language()))[3]
            elif str(mainIniFile.ini_next_backup_thu()) == "true":
               return determine_days_language(str(system_language()))[4]
            elif str(mainIniFile.ini_next_backup_fri()) == "true":
               return determine_days_language(str(system_language()))[5]
            elif str(mainIniFile.ini_next_backup_sat()) == "true":
               return determine_days_language(str(system_language()))[6]
            elif str(mainIniFile.ini_next_backup_sun()) == "true":
               return determine_days_language(str(system_language()))[0]
    # MON
    elif str(mainIniFile.day_name()) == determine_days_language(str(system_language()))[1]:
        if str(mainIniFile.ini_next_backup_mon()) == "true" and int(mainIniFile.current_time()) < int(mainIniFile.backup_time()):
           return "Today"
        else:
            if str(mainIniFile.ini_next_backup_tue()) == "true":
               return determine_days_language(str(system_language()))[2]
            elif str(mainIniFile.ini_next_backup_wed()) == "true":
               return determine_days_language(str(system_language()))[3]
            elif str(mainIniFile.ini_next_backup_thu()) == "true":
               return determine_days_language(str(system_language()))[4]
            elif str(mainIniFile.ini_next_backup_fri()) == "true":
               return determine_days_language(str(system_language()))[5]
            elif str(mainIniFile.ini_next_backup_sat()) == "true":
               return determine_days_language(str(system_language()))[6]
            elif str(mainIniFile.ini_next_backup_sun()) == "true":
               return determine_days_language(str(system_language()))[0]
            elif str(mainIniFile.ini_next_backup_mon()) == "true":
               return determine_days_language(str(system_language()))[1]
    # TUE
    elif str(mainIniFile.day_name()) == determine_days_language(str(system_language()))[2]:
        if str(mainIniFile.ini_next_backup_tue()) == "true" and int(mainIniFile.current_time()) < int(mainIniFile.backup_time()):
           return "Today"
        else:
            if str(mainIniFile.ini_next_backup_wed()) == "true":
               return determine_days_language(str(system_language()))[3]
            elif str(mainIniFile.ini_next_backup_thu()) == "true":
               return determine_days_language(str(system_language()))[4]
            elif str(mainIniFile.ini_next_backup_fri()) == "true":
               return determine_days_language(str(system_language()))[5]
            elif str(mainIniFile.ini_next_backup_sat()) == "true":
               return determine_days_language(str(system_language()))[6]
            elif str(mainIniFile.ini_next_backup_sun()) == "true":
               return determine_days_language(str(system_language()))[0]
            elif str(mainIniFile.ini_next_backup_mon()) == "true":
               return determine_days_language(str(system_language()))[1]
            elif str(mainIniFile.ini_next_backup_tue()) == "true":
               return determine_days_language(str(system_language()))[2]
    # WED
    elif str(mainIniFile.day_name()) == determine_days_language(str(system_language()))[3]:
        if str(mainIniFile.ini_next_backup_wed()) == "true" and int(mainIniFile.current_time()) < int(mainIniFile.backup_time()):
           return "Today"
        else:
            if str(mainIniFile.ini_next_backup_thu()) == "true":
               return determine_days_language(str(system_language()))[4]
            elif str(mainIniFile.ini_next_backup_fri()) == "true":
               return determine_days_language(str(system_language()))[5]
            elif str(mainIniFile.ini_next_backup_sat()) == "true":
               return determine_days_language(str(system_language()))[6]
            elif str(mainIniFile.ini_next_backup_sun()) == "true":
               return determine_days_language(str(system_language()))[0]
            elif str(mainIniFile.ini_next_backup_mon()) == "true":
               return determine_days_language(str(system_language()))[1]
            elif str(mainIniFile.ini_next_backup_tue()) == "true":
               return determine_days_language(str(system_language()))[2]
            elif str(mainIniFile.ini_next_backup_wed()) == "true":
               return determine_days_language(str(system_language()))[3]
    # TUE
    elif str(mainIniFile.day_name()) == determine_days_language(str(system_language()))[4]:
        if str(mainIniFile.ini_next_backup_thu()) == "true" and int(mainIniFile.current_time()) < int(mainIniFile.backup_time()):
           return "Today"
        else:
            if str(mainIniFile.ini_next_backup_fri()) == "true":
               return determine_days_language(str(system_language()))[5]
            elif str(mainIniFile.ini_next_backup_sat()) == "true":
               return determine_days_language(str(system_language()))[6]
            elif str(mainIniFile.ini_next_backup_sun()) == "true":
               return determine_days_language(str(system_language()))[0]
            elif str(mainIniFile.ini_next_backup_mon()) == "true":
               return determine_days_language(str(system_language()))[1]
            elif str(mainIniFile.ini_next_backup_tue()) == "true":
               return determine_days_language(str(system_language()))[2]
            elif str(mainIniFile.ini_next_backup_wed()) == "true":
               return determine_days_language(str(system_language()))[3]
            elif str(mainIniFile.ini_next_backup_thu()) == "true":
               return determine_days_language(str(system_language()))[4]
    # FRI
    elif str(mainIniFile.day_name()) == determine_days_language(str(system_language()))[5]:
        if str(mainIniFile.ini_next_backup_fri()) == "true" and int(mainIniFile.current_time()) < int(mainIniFile.backup_time()):
           return "Today"
        else:
            if str(mainIniFile.ini_next_backup_sat()) == "true":
               return determine_days_language(str(system_language()))[6]
            elif str(mainIniFile.ini_next_backup_sun()) == "true":
               return determine_days_language(str(system_language()))[0]
            elif str(mainIniFile.ini_next_backup_mon()) == "true":
               return determine_days_language(str(system_language()))[1]
            elif str(mainIniFile.ini_next_backup_tue()) == "true":
               return determine_days_language(str(system_language()))[2]
            elif str(mainIniFile.ini_next_backup_wed()) == "true":
               return determine_days_language(str(system_language()))[3]
            elif str(mainIniFile.ini_next_backup_thu()) == "true":
               return determine_days_language(str(system_language()))[4]
            elif str(mainIniFile.ini_next_backup_fri()) == "true":
               return determine_days_language(str(system_language()))[5]
    # SAT
    elif str(mainIniFile.day_name()) == determine_days_language(str(system_language()))[6]:
        if str(mainIniFile.ini_next_backup_sat()) == "true" and int(mainIniFile.current_time()) < int(mainIniFile.backup_time()):
           return "Today"
        else:
            if str(mainIniFile.ini_next_backup_sun()) == "true":
               return determine_days_language(str(system_language()))[0]
            elif str(mainIniFile.ini_next_backup_mon()) == "true":
               return determine_days_language(str(system_language()))[1]
            elif str(mainIniFile.ini_next_backup_tue()) == "true":
               return determine_days_language(str(system_language()))[2]
            elif str(mainIniFile.ini_next_backup_wed()) == "true":
               return determine_days_language(str(system_language()))[3]
            elif str(mainIniFile.ini_next_backup_thu()) == "true":
               return determine_days_language(str(system_language()))[4]
            elif str(mainIniFile.ini_next_backup_fri()) == "true":
               return determine_days_language(str(system_language()))[5]
            elif str(mainIniFile.ini_next_backup_sat()) == "true":
               return determine_days_language(str(system_language()))[6]
    else:
       return "None"
    

#print(str(mainIniFile.day_name()))
print(determine_days_language(str(system_language())))
# print(determine_days_language(str(system_language())))
print(get_next_backup())