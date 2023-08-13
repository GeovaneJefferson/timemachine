from setup import *
from read_ini_file import UPDATEINIFILE


async def restore_backup_flatpaks_data():
	MAIN_INI_FILE=UPDATEINIFILE()
	
	print("Restoring flatpaks data...")
	for output in os.listdir(f"{MAIN_INI_FILE.flatpak_var_folder()}"):
		MAIN_INI_FILE.set_database_value('INFO', 'current_backing_up', f'{output}')

		# Restore flatpak data (var) folders from external device
		sub.run(f"{COPY_RSYNC_CMD} {MAIN_INI_FILE.flatpak_var_folder()}/{output} {src_flatpak_var_folder_location}", shell=True)

	for output in os.listdir(f"{MAIN_INI_FILE.flatpak_local_folder()}"):
		MAIN_INI_FILE.set_database_value('INFO', 'current_backing_up', f'{output}')

		# Restore flatpak data (Local) folders from external device
		sub.run(f"{COPY_RSYNC_CMD} {MAIN_INI_FILE.flatpak_local_folder()}/{output} {src_flatpak_local_folder_location}", shell=True)

	return "Task completed: Wallpaper"
            

if __name__ == '__main__':
    pass