from setup import *
from get_folders_to_be_backup import home_folders_size
from get_flatpaks_folders_size import get_external_device_free_size ,flatpak_var_size, flatpak_local_size
from get_backup_date import get_backup_date
from get_users_de import get_user_de
# Package manager
# from package_manager import package_manager
from notification_massage import notification_message
from read_ini_file import UPDATEINIFILE


# Handle signal
signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)


class PREPAREBACKUP:
    def __init__(self):
        # System settings size list
        self.system_settings_size_list = []
        # Safe added space
        self.safe_added_space = 1000000

        self.backing_up_now()

    def backing_up_now(self):
        MAIN_INI_FILE.set_database_value('STATUS', 'backing_up_now', 'True')

        self.begin_backup_process()

    # Check backup size, as the backup device size
    def begin_backup_process(self):
        print("Calculating backup sizes ...")

        # Check backup sizes needeed, delete old backup if is a must
        if self.get_backup_sizes():
            # Create base folders
            self.create_base_folders()
            # Create folders with date/time inside backup device
            self.create_date_time_folder()
            # Call backup now .py
            sub.Popen(f"python3 {src_backup_now_py}", shell=True)

        else:
            # Not enough space to make a new backup
            print("Not enough space for a new backup!")
            print("Please, manual delete old backups. ")
            
            # Set backup now to False and unfinished_backup to True
            MAIN_INI_FILE.set_database_value('STATUS', 'backing_up_now', 'False')
            # MAIN_INI_FILE.set_database_value('STATUS', 'unfinished_backup', 'True')

        # Send notification status
        notification_message("")
        
        # Quit
        exit()

    def create_base_folders(self):
        print("Creating base folders...")

        # Create base folders
        try:
            ################################################################################
            # Create TMB (Base)
            ################################################################################
            if not os.path.exists(str(MAIN_INI_FILE.create_base_folder())):
                print(f"{CREATE_CMD_FOLDER} {str(MAIN_INI_FILE.create_base_folder())}")
                sub.run(f"{CREATE_CMD_FOLDER} {str(MAIN_INI_FILE.create_base_folder())}",shell=True)

            ################################################################################
            # Create backup folder
            ################################################################################
            if not os.path.exists(str(MAIN_INI_FILE.backup_folder_name())):
                sub.run(f"{CREATE_CMD_FOLDER} {MAIN_INI_FILE.backup_folder_name()}",shell=True)

            ################################################################################
            # Create Application folder
            ################################################################################
            if not os.path.exists(str(MAIN_INI_FILE.application_main_folder())):
                sub.run(f"{CREATE_CMD_FOLDER} {str(MAIN_INI_FILE.application_main_folder())}",shell=True)

            ################################################################################
            # Create flatpak folder
            ################################################################################
            if not os.path.exists(str(MAIN_INI_FILE.create_flatpak_folder())):
                sub.run(f"{CREATE_CMD_FOLDER} {MAIN_INI_FILE.create_flatpak_folder()}",shell=True)

            ################################################################################
            # Create flatpak text
            ################################################################################
            if not os.path.exists(str(MAIN_INI_FILE.flatpak_txt_location())):
                sub.run(f"{CREATE_CMD_FILE} {str(MAIN_INI_FILE.flatpak_txt_location())}",shell=True)

            ################################################################################
            # Create Flatpak DATA folder
            ################################################################################
            if MAIN_INI_FILE.get_database_value('STATUS', 'allow_flatpak_data'):
                # Create inside external "Var" Folder
                if not os.path.exists(MAIN_INI_FILE.flatpak_var_folder()):
                    sub.run(f"{CREATE_CMD_FOLDER} {MAIN_INI_FILE.flatpak_var_folder()}",shell=True)

                # Create inside external "Local" Folder
                if not os.path.exists(str(MAIN_INI_FILE.flatpak_local_folder())):
                    sub.run(f"{CREATE_CMD_FOLDER} {str(MAIN_INI_FILE.flatpak_local_folder())}",shell=True)

            ################################################################################
            # Create wallpaper folder
            ################################################################################
            if not os.path.exists(str(MAIN_INI_FILE.wallpaper_main_folder())):
                sub.run(f"{CREATE_CMD_FOLDER} {str(MAIN_INI_FILE.wallpaper_main_folder())}",shell=True)

            ################################################################################
            # Package manager
            ################################################################################
            # Create RPM folder (Folder to manual place rpms apps)
            ################################################################################
            if not os.path.exists(str(MAIN_INI_FILE.rpm_main_folder())):
                sub.run(f"{CREATE_CMD_FOLDER} {str(MAIN_INI_FILE.rpm_main_folder())}",shell=True)

            # Create Deb folder (Folder to manual place deb apps)
            if not os.path.exists(str(MAIN_INI_FILE.deb_main_folder())):
                sub.run(f"{CREATE_CMD_FOLDER} {str(MAIN_INI_FILE.deb_main_folder())}",shell=True)

            ################################################################################
            # GNOME
            ################################################################################
            if get_user_de() == 'gnome':
                # Create gnome folder
                if not os.path.exists(str(MAIN_INI_FILE.gnome_main_folder())):
                    sub.run(f"{CREATE_CMD_FOLDER} {str(MAIN_INI_FILE.gnome_main_folder())}",shell=True)

                # Create configuration folder
                if not os.path.exists(str(MAIN_INI_FILE.gnome_configurations_folder_main_folder())):
                    sub.run(f"{CREATE_CMD_FOLDER} {str(MAIN_INI_FILE.gnome_configurations_folder_main_folder())}",shell=True)

                ################################################################################
                # Create gnome LOCAL SHARE
                ################################################################################
                if not os.path.exists(str(MAIN_INI_FILE.gnome_local_share_main_folder())):
                    sub.run(f"{CREATE_CMD_FOLDER} {str(MAIN_INI_FILE.gnome_local_share_main_folder())}",shell=True)

                ################################################################################
                # Create gnome CONFIG
                ################################################################################
                if not os.path.exists(str(MAIN_INI_FILE.gnome_config_main_folder())):
                    sub.run(f"{CREATE_CMD_FOLDER} {str(MAIN_INI_FILE.gnome_config_main_folder())}",shell=True)

            ################################################################################
            # KDE
            ################################################################################
            elif get_user_de() == 'kde':
                # Create kde folder
                if not os.path.exists(str(MAIN_INI_FILE.kde_main_folder())):
                    sub.run(f"{CREATE_CMD_FOLDER} {str(MAIN_INI_FILE.kde_main_folder())}",shell=True)

                # Create configuration folder
                if not os.path.exists(str(MAIN_INI_FILE.kde_configurations_folder_main_folder())):
                    sub.run(f"{CREATE_CMD_FOLDER} {str(MAIN_INI_FILE.kde_configurations_folder_main_folder())}",shell=True)

                ################################################################################
                # Create KDE LOCAL SHARE
                ################################################################################
                if not os.path.exists(str(MAIN_INI_FILE.kde_local_share_main_folder())):
                    sub.run(f"{CREATE_CMD_FOLDER} {str(MAIN_INI_FILE.kde_local_share_main_folder())}",shell=True)

                ################################################################################
                # Create KDE CONFIG
                ################################################################################
                if not os.path.exists(str(MAIN_INI_FILE.kde_config_main_folder())):
                    sub.run(f"{CREATE_CMD_FOLDER} {str(MAIN_INI_FILE.kde_config_main_folder())}",shell=True)

                ################################################################################
                # Create KDE SHARE CONFIG
                ################################################################################
                if not os.path.exists(str(MAIN_INI_FILE.kde_share_config_main_folder())):
                    sub.run(f"{CREATE_CMD_FOLDER} {str(MAIN_INI_FILE.kde_share_config_main_folder())}",shell=True)

            ################################################################################
            # Create restore_settings.ini
            ################################################################################
            if not os.path.exists(str(MAIN_INI_FILE.restore_settings_location())):
                print("Restore Settings ini inside external, was created.")
                sub.run(f"{CREATE_CMD_FILE} {str(MAIN_INI_FILE.restore_settings_location())}",shell=True)

        except FileNotFoundError as e:
            error_trying_to_backup(e)

    def get_backup_sizes(self):
        # Home + System Settings + safe additional size
        # 
        if MAIN_INI_FILE.get_database_value('STATUS', 'allow_flatpak_data'):
            backup_size_needeed = int(home_folders_size()) + self.safe_added_space

        # Home + System Settings + Flatpak data + safe additional size
        else:
            backup_size_needeed = int(home_folders_size() +
                                    flatpak_var_size() +
                                    flatpak_local_size() +
                                    self.safe_added_space)

        # if backup size if higher than free space inside backup device
        if backup_size_needeed > get_external_device_free_size():
            print("Not enough space for new backup")
            print("Deleting old backups folders...")
            # Send notification status
            notification_message(f"Deleting old backups folders...")

            # Delete old backups
            self.delete_old_backups()

        else:
            # Enough space to continue
            return True

    def delete_old_backups(self):
        try:
            # Keep at least one backup folder
            if len(get_backup_date()) > 1:
                # Send notification status
                notification_message(f"Current backing up: {get_backup_date()[-1]}")

                # Deleting old backups
                print(f"Deleting {MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}/{get_backup_date()[-1]}...")
                sub.run(f"rm -rf {MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}/{get_backup_date()[-1]}",shell=True)

                # Deleting .trash inside backup device to get more free space
                # print(f"Deleting .trash...")
                # sub.run(f"rm -rf {str(MAININIFILE.ini_external_location())}/.Trash-1000",shell=True)

            else:
                print(f"Please, manual delete file(s)/folder(s) inside your backup device, to make space for {APP_NAME}'s "
                "backup!")

                # Send notification status
                notification_message(f"Please, manual delete file(s)/folder(s) inside your backup device!")

            # Go back and check the backup size needeed
            self.get_backup_sizes()

        # Error while deleting old backup
        except Exception as e:
            print(f"Error while deleting old backup: {e}")
            # Send notification status
            notification_message(f"Error while deleting old backup: {e}")
            # TODO
            # Cancel backup
            # Quit
            exit()

    def create_date_time_folder(self):
        print("Creating pre folders...")

        # Create folder with current date
        try:
            if not os.path.exists(MAIN_INI_FILE.date_folder_format()):
                sub.run(f"{CREATE_CMD_FOLDER} {MAIN_INI_FILE.date_folder_format()}", shell=True)

            # Create folder inside the current date with current time
            if not os.path.exists(MAIN_INI_FILE.time_folder_format()):
                sub.run(f"{CREATE_CMD_FOLDER} {MAIN_INI_FILE.time_folder_format()}", shell=True)

        except FileNotFoundError as e:
            # Send error message
            error_trying_to_backup(e)


if __name__ == '__main__':
    MAIN_INI_FILE = UPDATEINIFILE()
    main = PREPAREBACKUP()
