from get_system_language import system_language
from languages import determine_days_language
from read_ini_file import UPDATEINIFILE

mainIniFile = UPDATEINIFILE()


print(str(system_language())[0:])
print(str(mainIniFile.day_name()))
print(str(determine_days_language(str(system_language())[0])))
print(str(mainIniFile.day_name()) in str(determine_days_language(str(system_language())[0])))