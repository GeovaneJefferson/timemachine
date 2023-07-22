from setup import *
from read_ini_file import UPDATEINIFILE
from languages import determine_days_language
from get_system_language import system_language


def get_next_backup():
   MAININIFILE=UPDATEINIFILE()
   
   # SUN
   if str(MAININIFILE.day_name()) == determine_days_language(system_language())[0]:
      if str(MAININIFILE.ini_next_backup_sun()) and int(MAININIFILE.current_hour()) <= int(MAININIFILE.ini_next_hour()) and int(MAININIFILE.current_minute()) <= int(MAININIFILE.ini_next_minute()):
         return "Today"
      
      else:
         if str(MAININIFILE.ini_next_backup_mon()):
            return determine_days_language(str(system_language()))[1]
         
         elif str(MAININIFILE.ini_next_backup_tue()):
            return determine_days_language(str(system_language()))[2]
         
         elif str(MAININIFILE.ini_next_backup_wed()):
            return determine_days_language(str(system_language()))[3]
         
         elif str(MAININIFILE.ini_next_backup_thu()):
            return determine_days_language(str(system_language()))[4]
         
         elif str(MAININIFILE.ini_next_backup_fri()):
            return determine_days_language(str(system_language()))[5]
         
         elif str(MAININIFILE.ini_next_backup_sat()):
            return determine_days_language(str(system_language()))[6]
         
         elif str(MAININIFILE.ini_next_backup_sun()):
            return determine_days_language(str(system_language()))[0]
   # MON
   elif str(MAININIFILE.day_name()) == determine_days_language(system_language())[1]:
      if str(MAININIFILE.ini_next_backup_mon()) == "true" and int(MAININIFILE.current_time()) < int(MAININIFILE.backup_time_military()):
         return "Today"
      
      else:
         if str(MAININIFILE.ini_next_backup_tue()):
            return determine_days_language(str(system_language()))[2]
         
         elif str(MAININIFILE.ini_next_backup_wed()):
            return determine_days_language(str(system_language()))[3]
         
         elif str(MAININIFILE.ini_next_backup_thu()):
            return determine_days_language(str(system_language()))[4]
         
         elif str(MAININIFILE.ini_next_backup_fri()):
            return determine_days_language(str(system_language()))[5]
         
         elif str(MAININIFILE.ini_next_backup_sat()):
            return determine_days_language(str(system_language()))[6]
         
         elif str(MAININIFILE.ini_next_backup_sun()):
            return determine_days_language(str(system_language()))[0]
         
         elif str(MAININIFILE.ini_next_backup_mon()):
            return determine_days_language(str(system_language()))[1]
   # TUE
   elif str(MAININIFILE.day_name()) == determine_days_language(system_language())[2]:
      if str(MAININIFILE.ini_next_backup_tue()) == "true" and int(MAININIFILE.current_time()) < int(MAININIFILE.backup_time_military()):
         return "Today"
      
      else:
         if str(MAININIFILE.ini_next_backup_wed()):
            return determine_days_language(str(system_language()))[3]
         
         elif str(MAININIFILE.ini_next_backup_thu()):
            return determine_days_language(str(system_language()))[4]
         
         elif str(MAININIFILE.ini_next_backup_fri()):
            return determine_days_language(str(system_language()))[5]
         
         elif str(MAININIFILE.ini_next_backup_sat()):
            return determine_days_language(str(system_language()))[6]
         
         elif str(MAININIFILE.ini_next_backup_sun()):
            return determine_days_language(str(system_language()))[0]
         
         elif str(MAININIFILE.ini_next_backup_mon()):
            return determine_days_language(str(system_language()))[1]
         
         elif str(MAININIFILE.ini_next_backup_tue()):
            return determine_days_language(str(system_language()))[2]
   # WED
   elif str(MAININIFILE.day_name()) == determine_days_language(system_language())[3]:
      if str(MAININIFILE.ini_next_backup_wed()) == "true" and int(MAININIFILE.current_time()) < int(MAININIFILE.backup_time_military()):
         return "Today"
      
      else:
         if str(MAININIFILE.ini_next_backup_thu()):
            return determine_days_language(str(system_language()))[4]
         
         elif str(MAININIFILE.ini_next_backup_fri()):
            return determine_days_language(str(system_language()))[5]
         
         elif str(MAININIFILE.ini_next_backup_sat()):
            return determine_days_language(str(system_language()))[6]
         
         elif str(MAININIFILE.ini_next_backup_sun()):
            return determine_days_language(str(system_language()))[0]
         
         elif str(MAININIFILE.ini_next_backup_mon()):
            return determine_days_language(str(system_language()))[1]
         
         elif str(MAININIFILE.ini_next_backup_tue()):
            return determine_days_language(str(system_language()))[2]
         
         elif str(MAININIFILE.ini_next_backup_wed()):
            return determine_days_language(str(system_language()))[3]
   # TUE
   elif str(MAININIFILE.day_name()) == determine_days_language(system_language())[4]:
      if str(MAININIFILE.ini_next_backup_thu()) == "true" and int(MAININIFILE.current_time()) < int(MAININIFILE.backup_time_military()):
         return "Today"
      
      else:
         if str(MAININIFILE.ini_next_backup_fri()):
            return determine_days_language(str(system_language()))[5]
         
         elif str(MAININIFILE.ini_next_backup_sat()):
            return determine_days_language(str(system_language()))[6]
         
         elif str(MAININIFILE.ini_next_backup_sun()):
            return determine_days_language(str(system_language()))[0]
         
         elif str(MAININIFILE.ini_next_backup_mon()):
            return determine_days_language(str(system_language()))[1]
         
         elif str(MAININIFILE.ini_next_backup_tue()):
            return determine_days_language(str(system_language()))[2]
         
         elif str(MAININIFILE.ini_next_backup_wed()):
            return determine_days_language(str(system_language()))[3]
         
         elif str(MAININIFILE.ini_next_backup_thu()):
            return determine_days_language(str(system_language()))[4]
   # FRI
   elif str(MAININIFILE.day_name()) == determine_days_language(system_language())[5]:
      if str(MAININIFILE.ini_next_backup_fri()) == "true" and int(MAININIFILE.current_time()) < int(MAININIFILE.backup_time_military()):
         return "Today"
      
      else:
         if str(MAININIFILE.ini_next_backup_sat()):
            return determine_days_language(str(system_language()))[6]
         
         elif str(MAININIFILE.ini_next_backup_sun()):
            return determine_days_language(str(system_language()))[0]
         
         elif str(MAININIFILE.ini_next_backup_mon()):
            return determine_days_language(str(system_language()))[1]
         
         elif str(MAININIFILE.ini_next_backup_tue()):
            return determine_days_language(str(system_language()))[2]
         
         elif str(MAININIFILE.ini_next_backup_wed()):
            return determine_days_language(str(system_language()))[3]
         
         elif str(MAININIFILE.ini_next_backup_thu()):
            return determine_days_language(str(system_language()))[4]
         
         elif str(MAININIFILE.ini_next_backup_fri()):
            return determine_days_language(str(system_language()))[5]
   # SAT
   elif str(MAININIFILE.day_name()) == determine_days_language(system_language())[6]:
      if str(MAININIFILE.ini_next_backup_sat()) == "true" and int(MAININIFILE.current_time()) < int(MAININIFILE.backup_time_military()):
         return "Today"
      
      else:
         if str(MAININIFILE.ini_next_backup_sun()):
            return determine_days_language(str(system_language()))[0]
         
         elif str(MAININIFILE.ini_next_backup_mon()):
            return determine_days_language(str(system_language()))[1]
         
         elif str(MAININIFILE.ini_next_backup_tue()):
            return determine_days_language(str(system_language()))[2]
         
         elif str(MAININIFILE.ini_next_backup_wed()):
            return determine_days_language(str(system_language()))[3]
         
         elif str(MAININIFILE.ini_next_backup_thu()):
            return determine_days_language(str(system_language()))[4]
         
         elif str(MAININIFILE.ini_next_backup_fri()):
            return determine_days_language(str(system_language()))[5]
         
         elif str(MAININIFILE.ini_next_backup_sat()):
            return determine_days_language(str(system_language()))[6]
   else:
      return "None"
   
if __name__ == '__main__':
   pass