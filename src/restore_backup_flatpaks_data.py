from setup import *
from read_ini_file import UPDATEINIFILE


async def restore_backup_flatpaks_data():
	mainIniFile = UPDATEINIFILE()
	
	print("Restoring flatpaks data...")
	try:
		for output in os.listdir(f"{mainIniFile.application_var_folder()}"):
			config = configparser.ConfigParser()
			config.read(src_user_config)
			with open(src_user_config, 'w') as configfile:
				config.set('INFO', 'current_backing_up', f"{output}")
				config.write(configfile)

			# Restore flatpak data (var) folders from external device
			sub.run(f"{copyRsyncCMD} {mainIniFile.application_var_folder()}/{output} {src_flatpak_var_folder_location}", shell=True)
	except:
		pass

	try:
		for output in os.listdir(f"{mainIniFile.application_local_folder()}"):
			config = configparser.ConfigParser()
			config.read(src_user_config)
			with open(src_user_config, 'w') as configfile:
				config.set('INFO', 'current_backing_up', f"{output}")
				config.write(configfile)

            # Restore flatpak data (Local) folders from external device
			sub.run(f"{copyRsyncCMD} {mainIniFile.application_local_folder()}/{output} {src_flatpak_local_folder_location}", shell=True)
	except:
		pass

	return "Task completed: Wallpaper"
            
if __name__ == '__main__':
    pass