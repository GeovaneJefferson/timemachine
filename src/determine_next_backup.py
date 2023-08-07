from setup import *
from read_ini_file import UPDATEINIFILE
from get_days_name import get_days_name


MAIN_INI_FILE = UPDATEINIFILE()


def get_next_backup():
   # SUN
   if str(MAIN_INI_FILE.day_name()) == get_days_name():
      if str(MAIN_INI_FILE.ini_next_backup_sun()) and int(MAIN_INI_FILE.current_hour()) <= int(MAIN_INI_FILE.ini_next_hour()) and int(MAIN_INI_FILE.current_minute()) <= int(MAIN_INI_FILE.ini_next_minute()):
         return "Today"
      
      # TODO
      else:
         if str(MAIN_INI_FILE.ini_next_backup_mon()):
            return "Tomorrow"
         
         elif str(MAIN_INI_FILE.ini_next_backup_tue()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=2)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_wed()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=3)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_thu()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=4)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_fri()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=5)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_sat()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=6)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_sun()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=7)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')

   # MON
   elif str(MAIN_INI_FILE.day_name()) == get_days_name():
      if str(MAIN_INI_FILE.ini_next_backup_mon()) == 'True' and int(MAIN_INI_FILE.current_time()) < int(MAIN_INI_FILE.backup_time_military()):
         return "Today"
      
      else:
         if str(MAIN_INI_FILE.ini_next_backup_tue()):
            return "Tomorrow"
         
         elif str(MAIN_INI_FILE.ini_next_backup_wed()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=2)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_thu()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=3)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_fri()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=4)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_sat()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=5)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_sun()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=6)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_mon()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=7)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
   # TUE
   elif str(MAIN_INI_FILE.day_name()) == get_days_name():
      if str(MAIN_INI_FILE.ini_next_backup_tue()) == 'True' and int(MAIN_INI_FILE.current_time()) < int(MAIN_INI_FILE.backup_time_military()):
         return "Today"
      
      else:
         if str(MAIN_INI_FILE.ini_next_backup_wed()):
            return "Tomorrow"
         
         elif str(MAIN_INI_FILE.ini_next_backup_thu()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=2)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_fri()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=3)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_sat()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=4)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_sun()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=5)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_mon()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=6)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_tue()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=7)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
   # WED
   elif str(MAIN_INI_FILE.day_name()) == get_days_name():
      if str(MAIN_INI_FILE.ini_next_backup_wed()) == 'True' and int(MAIN_INI_FILE.current_time()) < int(MAIN_INI_FILE.backup_time_military()):
         return "Today"
      
      else:
         if str(MAIN_INI_FILE.ini_next_backup_thu()):
            return "Tomorrow"
         
         elif str(MAIN_INI_FILE.ini_next_backup_fri()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=2)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_sat()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=3)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_sun()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=4)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_mon()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=5)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_tue()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=6)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_wed()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=7)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
   # TUE
   elif str(MAIN_INI_FILE.day_name()) == get_days_name():
      if str(MAIN_INI_FILE.ini_next_backup_thu()) == 'True' and int(MAIN_INI_FILE.current_time()) < int(MAIN_INI_FILE.backup_time_military()):
         return "Today"
      
      else:
         if str(MAIN_INI_FILE.ini_next_backup_fri()):
            return "Tomorrow"
         
         elif str(MAIN_INI_FILE.ini_next_backup_sat()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=2)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_sun()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=3)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_mon()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=4)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_tue()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=5)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_wed()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=6)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_thu()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=7)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
   # FRI
   elif str(MAIN_INI_FILE.day_name()) == get_days_name():
      if str(MAIN_INI_FILE.ini_next_backup_fri()) == 'True' and int(MAIN_INI_FILE.current_time()) < int(MAIN_INI_FILE.backup_time_military()):
         return "Today"
      
      else:
         if str(MAIN_INI_FILE.ini_next_backup_sat()):
            return "Tomorrow"
         
         elif str(MAIN_INI_FILE.ini_next_backup_sun()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=2)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_mon()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=3)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_tue()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=4)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_wed()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=5)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_thu()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=6)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_fri()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=7)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
   # SAT
   elif str(MAIN_INI_FILE.day_name()) == get_days_name():
      if str(MAIN_INI_FILE.ini_next_backup_sat()) == 'True' and int(MAIN_INI_FILE.current_time()) < int(MAIN_INI_FILE.backup_time_military()):
         return "Today"
      
      else:
         if str(MAIN_INI_FILE.ini_next_backup_sun()):
            return "Tomorrow"
         
         elif str(MAIN_INI_FILE.ini_next_backup_mon()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=2)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_tue()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=3)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_wed()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=4)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_thu()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=5)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_fri()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=6)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
         elif str(MAIN_INI_FILE.ini_next_backup_sat()):
            # Set the locale for the current session to English (United States)
            locale.setlocale(locale.LC_TIME, 'en_US.utf8')

            # Get the current date
            current_date = datetime.datetime.today()

            # Add one day to the current date
            next_backup_date = current_date + datetime.timedelta(days=7)

            # Get the day of the week for the next backup date
            return next_backup_date.strftime('%a')
         
   else:
      return "None"
   

if __name__ == '__main__':
   pass