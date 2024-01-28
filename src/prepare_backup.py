from setup import *
from read_ini_file import UPDATEINIFILE
import error_catcher
from create_directory import create_directory, create_file

from get_sizes import (
    get_external_device_free_size
    )

from get_backup_date import get_backup_date
from get_users_de import get_user_de
from notification_massage import notification_message
from read_ini_file import UPDATEINIFILE
from get_sizes import needeed_size_to_backup_home

MAIN_INI_FILE = UPDATEINIFILE()

# Handle signal
signal.signal(signal.SIGINT, error_catcher.signal_exit)
signal.signal(signal.SIGTERM, error_catcher.signal_exit)

# Minimum folders to be saved
min_folder_num = 1

# System settings size list
system_settings_size_list = []

# Safe added space
safe_added_space = 2147483648  # 2 GB


def is_first_backup():
    try:
        # First backup made by Time Machine
        # Nothing inside MAIN backup folder
        if not any(os.scandir(MAIN_INI_FILE.main_backup_folder())):
            return True
        else:
            return False
    except FileNotFoundError:
            return True

def has_enough_space(needeed_space):
    # if backup size if higher than free space inside backup device
    if needeed_space > get_external_device_free_size():
        print("Not enough space for new backup, need",)
        print("Deleting old backups folders...")

        # Send notification status
        notification_message(f"Deleting old backups folders...")

        # Delete old backups
        delete_old_backups()
    else:
        # Enough space to continue
        print("Enough space to continue.")
        return True
    
def create_base_folders():
    print('Creating base folders...')

    # Create necessaries folders and files
    try:
        ################################################################################
        # Create TMB (Base)
        ################################################################################
        if not os.path.exists(MAIN_INI_FILE.create_base_folder()):
            command = MAIN_INI_FILE.create_base_folder()

            # Check if the directory exists, and create it if necessary
            create_directory(command)

            # sub.run(
            #     ["mkdir", command], 
            #     stdout=sub.PIPE, 
            #     stderr=sub.PIPE)

        ################################################################################
        # Create backup folder
        ################################################################################
        if not os.path.exists(str(MAIN_INI_FILE.backup_folder_name())):
            command = f"{str(MAIN_INI_FILE.backup_folder_name())}"

            # Check if the directory exists, and create it if necessary
            create_directory(command)

            # sub.run(
            #     ["mkdir", command], 
            #     stdout=sub.PIPE, 
            #     stderr=sub.PIPE)

        ###############################################################################
        # Create MAIN backup folder
        ###############################################################################
        if not os.path.exists(MAIN_INI_FILE.main_backup_folder()):
            # Create MAIN backup folder
            command = MAIN_INI_FILE.main_backup_folder()

            # Check if the directory exists, and create it if necessary
            create_directory(command)

            # sub.run(
            #     ["mkdir", command], 
            #     stdout=sub.PIPE, 
            #     stderr=sub.PIPE)
        
        ###############################################################################
        # Create include txt file
        ################################################################################
        if not os.path.exists(MAIN_INI_FILE.include_to_backup()):
            command = MAIN_INI_FILE.include_to_backup()

            # Check if the directory exists, and create it if necessary
            create_directory(command)
            # Check if the file exists, and create it if necessary
            create_file(command)

        ################################################################################
        # Create Application folder
        ################################################################################
        if not os.path.exists(str(MAIN_INI_FILE.application_main_folder())):
            command = f"{str(MAIN_INI_FILE.application_main_folder())}"
            
            # Check if the directory exists, and create it if necessary
            create_directory(command)
            
            # sub.run(
            #     ["mkdir", command], 
            #     stdout=sub.PIPE, 
            #     stderr=sub.PIPE)

        ################################################################################
        # Create flatpak folder
        ################################################################################
        if not os.path.exists(str(MAIN_INI_FILE.create_flatpak_folder())):
            command = f"{str(MAIN_INI_FILE.create_flatpak_folder())}"
            
            # Check if the directory exists, and create it if necessary
            create_directory(command)
            
            # sub.run(
            #     ["mkdir", command], 
            #     stdout=sub.PIPE, 
            #     stderr=sub.PIPE)
        
        ################################################################################
        # Create pip text file
        ################################################################################
        if not os.path.exists(str(MAIN_INI_FILE.pip_packages_txt_location())):
            command = f"{str(MAIN_INI_FILE.pip_packages_txt_location())}"
            # Check if the directory exists, and create it if necessary
            create_directory(command)
            # Check if the file exists, and create it if necessary
            create_file(command)
            
            # sub.run(
            #     ["touch", command], 
            #     stdout=sub.PIPE, 
            #     stderr=sub.PIPE)
            
        ################################################################################
        # Create flatpak text file
        ################################################################################
        if not os.path.exists(str(MAIN_INI_FILE.flatpak_txt_location())):
            command = f"{str(MAIN_INI_FILE.flatpak_txt_location())}"
            # Check if the directory exists, and create it if necessary
            create_directory(command)
            # Check if the file exists, and create it if necessary
            create_file(command)

            # sub.run(
            #     ["touch", command], 
            #     stdout=sub.PIPE, 
            #     stderr=sub.PIPE)

        ################################################################################
        # Create Flatpak DATA folder
        ################################################################################
        # Create inside external "Var" Folder
        if not os.path.exists(MAIN_INI_FILE.flatpak_var_folder()):
            command = f"{str(MAIN_INI_FILE.flatpak_var_folder())}"

            # Check if the directory exists, and create it if necessary
            create_directory(command)

            # sub.run(
            #     ["mkdir", command], 
            #     stdout=sub.PIPE, 
            #     stderr=sub.PIPE)

        # Create inside external "Local" Folder
        if not os.path.exists(str(MAIN_INI_FILE.flatpak_local_folder())):
            command = f"{str(MAIN_INI_FILE.flatpak_local_folder())}"

            # Check if the directory exists, and create it if necessary
            create_directory(command)

            # sub.run(
            #     ["mkdir", command], 
            #     stdout=sub.PIPE, 
            #     stderr=sub.PIPE)

        ################################################################################
        # Create wallpaper folder
        ################################################################################
        if not os.path.exists(str(MAIN_INI_FILE.wallpaper_main_folder())):
            command = f"{str(MAIN_INI_FILE.wallpaper_main_folder())}"

            # Check if the directory exists, and create it if necessary
            create_directory(command)

            # sub.run(
            #     ["mkdir", command], 
            #     stdout=sub.PIPE, 
            #     stderr=sub.PIPE)

        ################################################################################
        # Package manager
        ################################################################################
        # Create RPM folder (Folder to manual place rpms apps)
        ################################################################################
        if not os.path.exists(str(MAIN_INI_FILE.rpm_main_folder())):
            command = f"{str(MAIN_INI_FILE.rpm_main_folder())}"

            # Check if the directory exists, and create it if necessary
            create_directory(command)

            # sub.run(
            #     ["mkdir", command], 
            #     stdout=sub.PIPE, 
            #     stderr=sub.PIPE)

        # Create Deb folder (Folder to manual place deb apps)
        if not os.path.exists(str(MAIN_INI_FILE.deb_main_folder())):
            command = f"{str(MAIN_INI_FILE.deb_main_folder())}"

            # Check if the directory exists, and create it if necessary
            create_directory(command)

            # sub.run(
            #     ["mkdir", command], 
            #     stdout=sub.PIPE, 
            #     stderr=sub.PIPE)

        ################################################################################
        # GNOME
        ################################################################################
        if get_user_de() == 'gnome':
            # Create gnome folder
            if not os.path.exists(MAIN_INI_FILE.gnome_main_folder()):
                command = MAIN_INI_FILE.gnome_main_folder()
               
                # Check if the directory exists, and create it if necessary
                create_directory(command)

                # sub.run(
                #     ["mkdir", command], 
                #     stdout=sub.PIPE, 
                #     stderr=sub.PIPE)
            
            # Create configuration folder
            if not os.path.exists(MAIN_INI_FILE.gnome_configurations_folder_main_folder()):
                command = MAIN_INI_FILE.gnome_configurations_folder_main_folder()
               
                # Check if the directory exists, and create it if necessary
                create_directory(command)

                # sub.run(
                #     ["mkdir", command], 
                #     stdout=sub.PIPE, 
                #     stderr=sub.PIPE)

            ################################################################################
            # Create gnome LOCAL SHARE
            ################################################################################
            if not os.path.exists(MAIN_INI_FILE.gnome_local_share_main_folder()):
                command = MAIN_INI_FILE.gnome_local_share_main_folder()
               
                # Check if the directory exists, and create it if necessary
                create_directory(command)

                # sub.run(
                #     ["mkdir", command], 
                #     stdout=sub.PIPE, 
                #     stderr=sub.PIPE)

            ################################################################################
            # Create gnome CONFIG
            ################################################################################
            if not os.path.exists(MAIN_INI_FILE.gnome_config_main_folder()):
                command = MAIN_INI_FILE.gnome_config_main_folder()
               
                # Check if the directory exists, and create it if necessary
                create_directory(command)

                # sub.run(
                #     ["mkdir", command], 
                #     stdout=sub.PIPE, 
                #     stderr=sub.PIPE)

        ################################################################################
        # KDE
        ################################################################################
        elif get_user_de() == 'kde':
            # Create kde folder
            if not os.path.exists(MAIN_INI_FILE.kde_main_folder()):
                command = MAIN_INI_FILE.kde_main_folder()
               
                # Check if the directory exists, and create it if necessary
                create_directory(command)

                # sub.run(
                #     ["mkdir", command], 
                #     stdout=sub.PIPE, 
                #     stderr=sub.PIPE)

            # Create configuration folder
            if not os.path.exists(MAIN_INI_FILE.kde_configurations_folder_main_folder()):
                command = MAIN_INI_FILE.kde_configurations_folder_main_folder()
               
                # Check if the directory exists, and create it if necessary
                create_directory(command)

                # sub.run(
                #     ["mkdir", command], 
                #     stdout=sub.PIPE, 
                #     stderr=sub.PIPE)

            ################################################################################
            # Create KDE LOCAL SHARE
            ################################################################################
            if not os.path.exists(str(MAIN_INI_FILE.kde_local_share_main_folder())):
                command = f"{str(MAIN_INI_FILE.kde_local_share_main_folder())}"
               
                # Check if the directory exists, and create it if necessary
                create_directory(command)

                # sub.run(
                #     ["mkdir", command], 
                #     stdout=sub.PIPE, 
                #     stderr=sub.PIPE)

            ################################################################################
            # Create KDE CONFIG
            ################################################################################
            if not os.path.exists(str(MAIN_INI_FILE.kde_config_main_folder())):
                command = f"{str(MAIN_INI_FILE.kde_config_main_folder())}"
               
                # Check if the directory exists, and create it if necessary
                create_directory(command)

                # sub.run(
                #     ["mkdir", command], 
                #     stdout=sub.PIPE, 
                #     stderr=sub.PIPE)

            ################################################################################
            # Create KDE SHARE CONFIG
            ################################################################################
            if not os.path.exists(str(MAIN_INI_FILE.kde_share_config_main_folder())):
                command = f"{str(MAIN_INI_FILE.kde_share_config_main_folder())}"
               
                # Check if the directory exists, and create it if necessary
                create_directory(command)

                # sub.run(
                #     ["mkdir", command], 
                #     stdout=sub.PIPE, 
                #     stderr=sub.PIPE)

        ################################################################################
        # Create restore_settings.ini
        ################################################################################
        if not os.path.exists(str(MAIN_INI_FILE.restore_settings_location())):
            print("Restore Settings ini inside external, was created.")
            command = f"{str(MAIN_INI_FILE.restore_settings_location())}"
            
            # Check if the directory exists, and create it if necessary
            create_directory(command)
            # Check if the file exists, and create it if necessary
            create_file(command)

            # sub.run(
            #     ["touch", command], 
            #     stdout=sub.PIPE, 
            #     stderr=sub.PIPE)

    except FileNotFoundError as e:
        error_catcher.signal_exit.error_trying_to_backup(e)

def create_date_and_time_folder():
    # Create folder with current date
    if not os.path.exists(MAIN_INI_FILE.date_folder_format()):
        command = MAIN_INI_FILE.date_folder_format()

        # Check if the directory exists, and create it if necessary
        create_directory(command)

        # sub.run(
        #     ["mkdir", command], 
        #     stdout=sub.PIPE, 
        #     stderr=sub.PIPE)

    # Create folder inside the current date with current time
    if not os.path.exists(MAIN_INI_FILE.time_folder_format()):
        command = MAIN_INI_FILE.time_folder_format()

        # Check if the directory exists, and create it if necessary
        create_directory(command)

        # sub.run(
        #     ["mkdir", command], 
        #     stdout=sub.PIPE, 
        #     stderr=sub.PIPE)
    
def delete_old_backups():
    try:
        # Keep at the minimum date folder(s)
        if len(get_backup_date()) > min_folder_num:
            # Send notification status
            notification_message(f"Current backing up: {get_backup_date()[-1]}")

            # Get full backup device's location
            database_hd = MAIN_INI_FILE.hd_hd()

            backup_date = get_backup_date()[-1]
            
            # Deleting old backups
            print(
                f'Deleting {database_hd}/{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}/{backup_date}...')
            
            command = (
                f"{database_hd}/{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}/{backup_date}")
            
            sub.run(
                ["rm", "-rf", command],
                stdout=sub.PIPE,
                stderr=sub.PIPE)

            # Deleting .trash inside backup device to get more free space
            print(f"Deleting .Trash-1000...")
            
            # Delete the .Trash-1000 inside backup device
            command = f'{database_hd}/.Trash-1000'
            sub.run(
                ["rm", "-rf", command], 
                stdout=sub.PIPE, 
                stderr=sub.PIPE)

        # Manual delete
        else:
            print(
                f'Please, manual delete file(s)/folder(s) inside your backup device.')

            # Send notification status
            notification_message(f"Please, manual delete file(s)/folder(s) inside your backup device!")

        # Go back and check the backup size needeed
        has_enough_space(needeed_size_to_backup_home())

    # Error while deleting old backup
    except Exception as e:
        print(f"Error while deleting old backup: {e}")
        
        # Send notification status
        notification_message(f"Error while deleting old backup: {e}")
        
        # Set DB backup now to False
        MAIN_INI_FILE.set_database_value('STATUS', 'backing_up_now', 'False')

        # Exit
        exit()


class PREPAREBACKUP:
    # Check backup size, as the backup device size
    def prepare_the_backup(self):
        # Create base folders
        create_base_folders()

        # Backup to MAIN backup folder
        if is_first_backup():
            # Check if backup device has space enough 
            if has_enough_space(needeed_size_to_backup_home()):
                # May continue to backup
                print('Prepare backup: True')
                return True

            else:
                print('Prepare backup: False')
                # May not continue to backup
                return False

        else:
            # Check if backup device has space enough 
            if has_enough_space(needeed_size_to_backup_home()):
                # Only create date/time folder, if has 'UPDATED' to update
                # Read the include file and process each item's information
                with open(MAIN_INI_FILE.include_to_backup(), 'r') as f:
                    lines = f.readlines()

                    # Read .include to backup txt file
                    for status in lines:
                        # Only get the status information
                        if status.startswith('Status'):
                            # Filter the information
                            status = status.strip().split(':')[-1].strip()

                    # Get more information
                    # for i in range(0, len(lines), 4):
                    #     # filename = lines[i + 0].split(':')[-1].strip()
                    #     # size_string = lines[i + 1].split(':')[-1].strip()
                    #     # size = int(size_string.split()[0])
                    #     # location = lines[i + 2].split(':')[-1].strip()
                    #     status = lines[i + 4].split(':')[-1].strip()
                            if status == 'UPDATED':
                                # Create a new date/time folder for a updated file
                                print('Creating a date/time folder.')
                                create_date_and_time_folder()
                                break      

                # May continue to backup
                print('Prepare backup: True')
                return True

            else:
                # Not enough space to make a new backup
                print("Not enough space for a new backup!")
                print("Please, manual delete old backups. ")
                
                # Set backup now to False and unfinished_backup to True
                MAIN_INI_FILE.set_database_value(
                    'STATUS', 'backing_up_now', 'False')
                # MAIN_INI_FILE.set_database_value('STATUS', 'unfinished_backup', 'True')
                
                # Notification to user
                notification_message('Not enough space for a new backup!')
				
                # May not continue to backup
                print('Prepare backup: False')
                return False

if __name__ == '__main__':
    MAIN_PREPARE = PREPAREBACKUP()
    MAIN_PREPARE.prepare_the_backup()