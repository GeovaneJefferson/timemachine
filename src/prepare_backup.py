#! /usr/bin/python3
from setup import *
from get_backup_folders import *
from get_time import *
from get_size import get_external_device_free_size ,flatpak_var_size, flatpak_local_size
from get_backup_date import get_backup_date
from get_user_de import get_user_de
from package_manager import package_manager
from get_user_icon import users_icon_size
from get_user_theme import users_theme_size
from get_user_wallpaper import *
from read_ini_file import UPDATEINIFILE
from add_backup_now_file import add_backup_now_file, can_backup_now_file_be_found

################################################################################
## Signal
################################################################################
# If user turn off or kill the app, update INI file
signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)


class PREPAREBACKUP:
    def __init__(self):
        print("Preparing the backup...")
        self.systemSettingsFolderToBackupSizeList = []
        self.begin_settings()

    def begin_settings(self):
        try:
            if not can_backup_now_file_be_found():
                add_backup_now_file()
            
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                config.set('BACKUP', 'backup_now', "true")
                config.write(configfile)
                
        except KeyError as error:
            print(error)
            exit()

        self.start_process()

    def start_process(self):
        if self.may_continue_to_backup():

            # Create base folders
            self.create_base_folders()
            
            # Calculate size
            self.system_settings_size_calculation()

            # Create folders with date/time
            self.create_date_time_folder()

            sub.Popen(f"python3 {src_backup_now_py}",shell=True)

        else:
            print("Error!")

        exit()

    def create_base_folders(self):
        print("Creating base folders...")
        try:
            ################################################################################
            # Create TMB (Base)
            ################################################################################
            if not os.path.exists(str(mainIniFile.create_base_folder())):
                print(f"{createCMDFolder} {str(mainIniFile.create_base_folder())}")
                sub.run(f"{createCMDFolder} {str(mainIniFile.create_base_folder())}",shell=True)

            ################################################################################
            # Create backup folder
            ################################################################################
            if not os.path.exists(str(mainIniFile.backup_folder_name())):
                sub.run(f"{createCMDFolder} {mainIniFile.backup_folder_name()}",shell=True)

            ################################################################################
            # Create Application folder
            ################################################################################
            if not os.path.exists(str(mainIniFile.application_main_folder())):
                sub.run(f"{createCMDFolder} {str(mainIniFile.application_main_folder())}",shell=True)

            ################################################################################
            # Create Icon folder
            ################################################################################
            if not os.path.exists(str(mainIniFile.icon_main_folder())):
                sub.run(f"{createCMDFolder} {str(mainIniFile.icon_main_folder())}",shell=True)

            # ################################################################################
            # # Create Font folder
            # ################################################################################
            # if not os.path.exists(str(mainIniFile.fonts_main_folder())):
            #     sub.run(f"{createCMDFolder} {str(mainIniFile.fonts_main_folder())}",shell=True)

            # ################################################################################
            # # Create Theme folder
            # ################################################################################
            # if not os.path.exists(str(mainIniFile.gtk_theme_main_folder())):
            #     sub.run(f"{createCMDFolder} {str(mainIniFile.gtk_theme_main_folder())}",shell=True)

            ################################################################################
            # Create flatpak text
            ################################################################################
            if not os.path.exists(str(mainIniFile.flatpak_txt_location())):
                sub.run(f"{createCMDFile} {str(mainIniFile.flatpak_txt_location())}",shell=True)   

            ################################################################################
            # Create Flatpak DATA folder
            ################################################################################
            if str(mainIniFile.ini_allow_flatpak_data()) == "true":
                # Create inside external "Var" Folder
                if not os.path.exists(str(mainIniFile.application_var_folder())):
                    sub.run(f"{createCMDFolder} {str(mainIniFile.application_var_folder())}",shell=True)  

                # Create inside external "Local" Folder
                if not os.path.exists(str(mainIniFile.application_local_folder())):
                    sub.run(f"{createCMDFolder} {str(mainIniFile.application_local_folder())}",shell=True)  

            ################################################################################
            # Create wallpaper folder
            ################################################################################
            if not os.path.exists(str(mainIniFile.wallpaper_main_folder())):
                sub.run(f"{createCMDFolder} {str(mainIniFile.wallpaper_main_folder())}",shell=True)   

            ################################################################################
            # Package manager
            ################################################################################
            if package_manager() == f"{rpmFolderName}": 
                ################################################################################
                # Create RPM folder (Folder to manual place rpms apps)
                ################################################################################
                if not os.path.exists(str(mainIniFile.rpm_main_folder())):
                    sub.run(f"{createCMDFolder} {str(mainIniFile.rpm_main_folder())}",shell=True)   
            
            elif package_manager() == f"{debFolderName}": 
                ################################################################################
                # Create Deb folder (Folder to manual place deb apps)
                ################################################################################
                if not os.path.exists(str(mainIniFile.deb_main_folder())):
                    sub.run(f"{createCMDFolder} {str(mainIniFile.deb_main_folder())}",shell=True)   
            
            ################################################################################
            # GNOME
            ################################################################################
            if get_user_de() == 'gnome':
                # Create gnome folder
                if not os.path.exists(str(mainIniFile.gnome_main_folder())):
                    sub.run(f"{createCMDFolder} {str(mainIniFile.gnome_main_folder())}",shell=True)
               
                # Create configuration folder
                if not os.path.exists(str(mainIniFile.gnome_configurations_folder_main_folder())):
                    sub.run(f"{createCMDFolder} {str(mainIniFile.gnome_configurations_folder_main_folder())}",shell=True)
               
                ################################################################################
                # Create gnome LOCAL SHARE
                ################################################################################
                if not os.path.exists(str(mainIniFile.gnome_local_share_main_folder())):
                    sub.run(f"{createCMDFolder} {str(mainIniFile.gnome_local_share_main_folder())}",shell=True)
               
                ################################################################################
                # Create gnome CONFIG
                ################################################################################
                if not os.path.exists(str(mainIniFile.gnome_config_main_folder())):
                    sub.run(f"{createCMDFolder} {str(mainIniFile.gnome_config_main_folder())}",shell=True)

            ################################################################################
            # KDE
            ################################################################################
            elif get_user_de() == 'kde':
                # Create kde folder
                if not os.path.exists(str(mainIniFile.kde_main_folder())):
                    sub.run(f"{createCMDFolder} {str(mainIniFile.kde_main_folder())}",shell=True)
               
                # Create configuration folder
                if not os.path.exists(str(mainIniFile.kde_configurations_folder_main_folder())):
                    sub.run(f"{createCMDFolder} {str(mainIniFile.kde_configurations_folder_main_folder())}",shell=True)
               
                ################################################################################
                # Create KDE LOCAL SHARE
                ################################################################################
                if not os.path.exists(str(mainIniFile.kde_local_share_main_folder())):
                    sub.run(f"{createCMDFolder} {str(mainIniFile.kde_local_share_main_folder())}",shell=True)
               
                ################################################################################
                # Create KDE CONFIG
                ################################################################################
                if not os.path.exists(str(mainIniFile.kde_config_main_folder())):
                    sub.run(f"{createCMDFolder} {str(mainIniFile.kde_config_main_folder())}",shell=True)
                
                ################################################################################
                # Create KDE SHARE CONFIG
                ################################################################################
                if not os.path.exists(str(mainIniFile.kde_share_config_main_folder())):
                    sub.run(f"{createCMDFolder} {str(mainIniFile.kde_share_config_main_folder())}",shell=True)
                
            ################################################################################
            # Create restore_settings.ini
            ################################################################################
            if not os.path.exists(str(mainIniFile.restore_settings_location())):
                print("Restore Settings ini inside external, was created.")
                sub.run(f"{createCMDFile} {str(mainIniFile.restore_settings_location())}",shell=True)

        except FileNotFoundError as error:
            error_trying_to_backup(error)

    def system_settings_size_calculation(self):
        if users_icon_size() is not None:
            self.systemSettingsFolderToBackupSizeList.append(users_icon_size())
        
        if users_theme_size() is not None:
            self.systemSettingsFolderToBackupSizeList.append(users_theme_size())

        try:
            return int(sum(self.systemSettingsFolderToBackupSizeList))
        except:
            return None

    def may_continue_to_backup(self):
        print("Checking folders conditions (size)...")

        while True:
            # Home + Icon + Theme + aditional number, just for safety
            if str(mainIniFile.ini_allow_flatpak_data()) == "true":
                calculation = int(home_folders_size()) + self.system_settings_size_calculation() + 1000000
            else:
                calculation = int(home_folders_size() + 
                                self.system_settings_size_calculation() + 
                                flatpak_var_size() + 
                                flatpak_local_size() +
                                1000000) # 5 GB

            # print(f"Space need to backup:{calculation}")
            # print(f"FreeSpace inside backup device:{get_external_device_free_size()}")
            
            ################################################################################
            # Delete old backupt if necessary
            ################################################################################
            # TODO
            if calculation > get_external_device_free_size():
                print("Not enough space for new backup")
                print("Old folders will be deleted, to make space for the new ones.")
                print("Please wait...")
                
                # ################################################################################
                # # Extra Information
                # ################################################################################
                # # Calculate KBytes to MB or GB
                # # Condition
                # if len(str(spaceNeeded)) <= 6:
                #     spaceNeeded = spaceNeeded / 1000 # Convert to MB
                #     print(f"Total Space (Home + Flatpaks) needed: {(spaceNeeded):.1f} MB")
                #     addToNotificationInfo = f"{(spaceNeeded):.1f} MB"

                # elif len(str(spaceNeeded)) > 6:
                #     spaceNeeded = spaceNeeded / 1000000 # Convert to GB
                #     print(f"Total Space (Home + Flatpaks) needed: {(spaceNeeded):.1f} GB")
                #     addToNotificationInfo = f"{(spaceNeeded):.1f} GB"

                # else:
                #     print(f"Total Space (Home + Flatpaks) needed: {spaceNeeded} KB")
                #     addToNotificationInfo = f"{spaceNeeded} KB"

                # config = configparser.ConfigParser()
                # config.read(src_user_config)
                # with open(src_user_config, 'w') as configfile:
                #     config.set('INFO', 'notification_massage', "2")
                #     config.set('INFO', 'notification_add_info', f"Space needed: {addToNotificationInfo}")
                #     config.write(configfile)

                try:
                    # Only deletes if exist more than one date folder inside
                    if len(get_backup_date()) > 1:
                        ################################################################################
                        # Write to INI file
                        ################################################################################
                        # config = configparser.ConfigParser()
                        # config.read(src_user_config)
                        # with open(src_user_config, 'w') as configfile:
                        #     config.set('INFO', 'current_backing_up', f"Deleting {get_backup_date()[-1]}...")
                        #     config.write(configfile)

                        # Action
                        # print(f"Deleting {str(mainIniFile.ini_external_location())}/{baseFolderName}/{backupFolderName}/{get_backup_date()[-1]}...")
                        sub.run(f"rm -rf {str(mainIniFile.ini_external_location())}/{baseFolderName}/{backupFolderName}/{get_backup_date()[-1]}",shell=True)
                        
                        print(f"Deleting .trash...")
                        sub.run(f"rm -rf {str(mainIniFile.ini_external_location())}/.Trash-1000",shell=True)

                        # Return to calculate all folders to be backup
                        # need_space_for_home_to_be_backup()
                
                    else:
                        # config = configparser.ConfigParser()
                        # config.read(src_user_config)
                        # with open(src_user_config, 'w') as configfile:
                            # config.set('INFO', 'notification_massage', "2")
                            # config.set('BACKUP', 'backup_now', 'false')
                            # config.set('INFO', 'notification_add_info', "Please, manual delete file(s)/folder(s) inside "
                            #         f"your backup device, to make space for {appName}'s backup!")
                            # config.write(configfile)

                        print(f"Please, manual delete file(s)/folder(s) inside your backup device, to make space for {appName}'s "
                        "backup!")
                        exit()

                except Exception as error:
                    print("Error trying to delete old backups!")
                    print(error)
                    return False

            else:
                print("enough space to continue...")
                return True

    def create_date_time_folder(self):
        print("Creating pre folders...")
        try:
            ################################################################################
            # Create folder with DATE
            ################################################################################
            if not os.path.exists(str(mainIniFile.date_folder_format())):
                sub.run(f"{createCMDFolder} {str(mainIniFile.date_folder_format())}",shell=True)

            ################################################################################
            # Create folder with TIME
            ################################################################################
            if not os.path.exists(str(mainIniFile.time_folder_format())):
                sub.run(f"{createCMDFolder} {str(mainIniFile.time_folder_format())}",shell=True)

        except FileNotFoundError as error:
            # Call error function 
            error_trying_to_backup(error)


if __name__ == '__main__':
    mainIniFile = UPDATEINIFILE()
    main = PREPAREBACKUP()

