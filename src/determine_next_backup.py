from setup import *
from read_ini_file import UPDATEINIFILE
from get_days_name import get_days_name
import datetime


MAIN_INI_FILE = UPDATEINIFILE()


def get_next_backup():
   print(MAIN_INI_FILE.day_name())
   print(get_days_name())
   print(MAIN_INI_FILE.ini_next_backup_mon())
   print(int(MAIN_INI_FILE.current_time()))
   print(int(MAIN_INI_FILE.backup_time_military()))
   
   # Check if today is the day to backup
   if str(MAIN_INI_FILE.day_name()) == get_days_name():  # Will return ex. Mon == Mon, so is today
      # Had yet not backup today
      if int(MAIN_INI_FILE.current_hour()) > int(MAIN_INI_FILE.ini_next_hour()) and int(MAIN_INI_FILE.current_minute()) <= int(MAIN_INI_FILE.ini_next_minute()):
         return "Today"
      # Has already made a backup
      else:
         return check_days()
   else:
      return check_days()

def check_days():
   if str(MAIN_INI_FILE.ini_next_backup_sun()):
      return get_locale_settings_language(0)
   elif str(MAIN_INI_FILE.ini_next_backup_mon()):
      return get_locale_settings_language(1)
   elif str(MAIN_INI_FILE.ini_next_backup_tue()):
      return get_locale_settings_language(2)
   elif str(MAIN_INI_FILE.ini_next_backup_wed()):
      return get_locale_settings_language(3)
   elif str(MAIN_INI_FILE.ini_next_backup_thu()):
      return get_locale_settings_language(4)
   elif str(MAIN_INI_FILE.ini_next_backup_fri()):
      return get_locale_settings_language(5)
   elif str(MAIN_INI_FILE.ini_next_backup_sat()):
      return get_locale_settings_language(6)
   else:
      return "None"
   
def get_locale_settings_language(day_number):
   # Get users locale settings language
   user_locale = locale.getdefaultlocale()
   user_locale_str = f"{user_locale[0]}.{user_locale[1].lower()}"

   # Set the locale for the current session to English (United States)
   locale.setlocale(locale.LC_TIME, user_locale_str)
   # Get the current date
   current_date = datetime.datetime.today()
   # Add one day to the current date
   next_backup_date = current_date + datetime.timedelta(days=day_number)
   # Get the day of the week for the next backup date
   return next_backup_date.strftime('%a')


if __name__ == '__main__':
   pass