from setup import *
from read_ini_file import UPDATEINIFILE


async def restore_backup_flatpaks_data():
	MAININIFILE=UPDATEINIFILE()
	
	print("Restoring flatpaks data...")
	try:
		for output in os.listdir(f"{MAININIFILE.flatpak_var_folder()}"):
			config=configparser.ConfigParser()
			config.read(SRC_USER_CONFIG)
			with open(SRC_USER_CONFIG, 'w') as configfile:
				config.set('INFO', 'current_backing_up', f"{output}")
				config.write(configfile)

			# Restore flatpak data (var) folders from external device
			sub.run(f"{COPY_RSYNC_CMD} {MAININIFILE.flatpak_var_folder()}/{output} {src_flatpak_var_folder_location}", shell=True)
	except:
		pass

	try:
		for output in os.listdir(f"{MAININIFILE.flatpak_local_folder()}"):
			config=configparser.ConfigParser()
			config.read(SRC_USER_CONFIG)
			with open(SRC_USER_CONFIG, 'w') as configfile:
				config.set('INFO', 'current_backing_up', f"{output}")
				config.write(configfile)

            # Restore flatpak data (Local) folders from external device
			sub.run(f"{COPY_RSYNC_CMD} {MAININIFILE.flatpak_local_folder()}/{output} {src_flatpak_local_folder_location}", shell=True)
	except:
		pass

	return "Task completed: Wallpaper"
            
if __name__ == '__main__':
    pass