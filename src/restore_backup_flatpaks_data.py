from setup import *
from read_ini_file import UPDATEINIFILE
from notification_massage import notification_message_current_backing_up
from handle_spaces import handle_spaces


MAIN_INI_FILE = UPDATEINIFILE()

async def restore_backup_flatpaks_data():
	print('Restoring flatpaks data...')
	
	for data in os.listdir(MAIN_INI_FILE.flatpak_var_folder()):
		# Handle spaces
		data = handle_spaces(data)
		
		notification_message_current_backing_up(f'Restoring: {data}...')

		# Restore flatpak data (var) folders from external device
		src = MAIN_INI_FILE.flatpak_var_folder() + '/' + data
		dst = SRC_FLATPAK_VAR_FOLDER_LOCATION
		
		sub.run(
			['cp', '-rvf', 
			src, dst])
                    
	for data in os.listdir(MAIN_INI_FILE.flatpak_local_folder()):
		# Handle spaces
		data = handle_spaces(data)

		notification_message_current_backing_up(f'Restoring: {data}...')

		# Restore flatpak data (Local) folders from external device
		src = MAIN_INI_FILE.flatpak_local_folder() + '/' + data
		dst = SRC_FLATPAK_LOCAL_FOLDER_LOCATION
		
		sub.run(
			['cp', '-rvf', 
			src, dst])
                         

if __name__ == '__main__':
    pass