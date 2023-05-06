#! /usr/bin/python3
from setup import *
from get_backup_folders import *
from get_time import *
from get_backup_date import get_backup_date
from get_user_de import get_user_de
from package_manager import package_manager
from get_user_wallpaper import *
from read_ini_file import UPDATEINIFILE
from add_backup_now_file import add_backup_now_file, can_backup_now_file_be_found, remove_backup_now_file

################################################################################
## Signal
################################################################################
# If user turn off or kill the app, update INI file
signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)


class PREPAREBACKUP:
    def __init__(self):
        print("Preparing the backup...")
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

        self.create_base_folders()

    def create_base_folders(self):
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
                print("TMB folder inside external, was created.")
                sub.run(f"{createCMDFolder} {mainIniFile.backup_folder_name()}",shell=True)

            ################################################################################
            # Create Application folder
            ################################################################################
            if not os.path.exists(str(mainIniFile.application_main_folder())):
                print("Application folder inside external, was created.")
                sub.run(f"{createCMDFolder} {str(mainIniFile.application_main_folder())}",shell=True)

            ################################################################################
            # Create Icon folder
            ################################################################################
            if not os.path.exists(str(mainIniFile.icon_main_folder())):
                print("Icon folder inside external, was created.")
                sub.run(f"{createCMDFolder} {str(mainIniFile.icon_main_folder())}",shell=True)

            ################################################################################
            # Create Font folder
            ################################################################################
            if not os.path.exists(str(mainIniFile.fonts_main_folder())):
                print("Fonts folder inside external, was created.")
                sub.run(f"{createCMDFolder} {str(mainIniFile.fonts_main_folder())}",shell=True)

            ################################################################################
            # Create Theme folder
            ################################################################################
            if not os.path.exists(str(mainIniFile.gtk_theme_main_folder())):
                print("Theme folder inside external, was created.")
                sub.run(f"{createCMDFolder} {str(mainIniFile.gtk_theme_main_folder())}",shell=True)

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
            # KDE OPTIONS
            ################################################################################
            if get_user_de() == 'kde':
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

                # ################################################################################
                # # Create Color Scheme folder
                # ################################################################################
                # if not os.path.exists(str(mainIniFile.color_scheme_main_folder())):
                #     print("Color scheme folder inside external, was created.")
                #     sub.run(f"{createCMDFolder} {str(mainIniFile.color_scheme_main_folder())}",shell=True)
                
            #     ################################################################################
            #     # Create Plasma Folder
            #     ################################################################################
            #     if not os.path.exists(str(mainIniFile.plasma_main_folder())):
            #         print("Plasma folder inside external, was created.")
            #         sub.run(f"{createCMDFolder} {str(mainIniFile.plasma_main_folder())}",shell=True)
                
            #     ################################################################################
            #     # Create Aurorae Folder
            #     ################################################################################
            #     if not os.path.exists(str(mainIniFile.aurorae_main_folder())):
            #         print("Aurorae folder inside external, was created.")
            #         sub.run(f"{createCMDFolder} {str(mainIniFile.aurorae_main_folder())}",shell=True)
                
            #     ################################################################################
            #     # Create Plasma Notes Folder
            #     ################################################################################
            #     if not os.path.exists(str(mainIniFile.kde_notes_main_folder())):
            #         print("Plasma Notes folder inside external, was created.")
            #         sub.run(f"{createCMDFolder} {str(mainIniFile.kde_notes_main_folder())}",shell=True)
                
            #     ################################################################################
            #     # Create Scripts Folder
            #     ################################################################################
            #     if not os.path.exists(str(mainIniFile.kde_scripts_main_folder())):
            #         print("Kde Scripts folder inside external, was created.")
            #         sub.run(f"{createCMDFolder} {str(mainIniFile.kde_scripts_main_folder())}",shell=True)
                
            #     ################################################################################
            #     # Create KdeGlobals
            #     ################################################################################
            #     if not os.path.exists(str(mainIniFile.kde_globals_main_folder())):
            #         print("KDE Globals folder inside external, was created.")
            #         sub.run(f"{createCMDFolder} {str(mainIniFile.kde_globals_main_folder())}",shell=True)
                
            #     ################################################################################
            #     # Create KGlobalShortcut Src
            #     ################################################################################
            #     if not os.path.exists(str(mainIniFile.kglobal_shortcut_src_main_folder())):
            #         print("KGlobal Shortcut Src folder inside external, was created.")
            #         sub.run(f"{createCMDFolder} {str(mainIniFile.kglobal_shortcut_src_main_folder())}",shell=True)
                
            #     ################################################################################
            #     # Create KdeKwinRc Src
            #     ################################################################################
            #     if not os.path.exists(str(mainIniFile.kde_kwinrc_main_folder())):
            #         print("KWinRc Src folder inside external, was created.")
            #         sub.run(f"{createCMDFolder} {str(mainIniFile.kde_kwinrc_main_folder())}",shell=True)
                
            ################################################################################
            # Create restore_settings.ini
            ################################################################################
            if not os.path.exists(str(mainIniFile.restore_settings_location())):
                print("Restore Settings ini inside external, was created.")
                sub.run(f"{createCMDFile} {str(mainIniFile.restore_settings_location())}",shell=True)

        except FileNotFoundError as error:
            error_trying_to_backup(error)

        self.has_icon_inside()
    
    def has_icon_inside(self):
        print("Checking icons...")
        self.iconInside = False

        # Get current use icon by user
        userCurrentGnomeIcon = os.popen(getUserIconCMD)
        userCurrentGnomeIcon = userCurrentGnomeIcon.read().strip()
        userCurrentGnomeIcon = userCurrentGnomeIcon.replace("'", "")

        ################################################################################
        # Get icon folders size
        ################################################################################
        # Try to find the current icon inside /usr/share/icons
        try:
            # Get folder size fomr /usr/share/icons
            self.getIconSize = os.popen(f"du -s /usr/share/icons/{userCurrentGnomeIcon}")
            self.getIconSize = self.getIconSize.read().strip("\t").strip("\n").replace(f"/usr/share/icons/{userCurrentGnomeIcon}", "").replace("\t", "")
            self.getIconSize = int(self.getIconSize)
            print("Icon found inside usr/share/icons")
            self.iconInside = True

        except :
            try:
                # If can not be found inside /usr/share/icons, try .icons in Home
                # Get folder size
                self.getIconSize = os.popen(f"du -s {homeUser}/.icons/{userCurrentGnomeIcon}")
                self.getIconSize = self.getIconSize.read().strip("\t").strip("\n").replace(f"{homeUser}/.icons/{userCurrentGnomeIcon}", "").replace("\t", "")
                self.getIconSize = int(self.getIconSize)
                print("Icon found inside .icons")
                self.iconInside = True

            except:
                pass

        self.has_theme_inside()

    def has_theme_inside(self):
        self.themeInside = False
        print("Checking themes...")
        try:
            ################################################################################
            # Get theme folders size
            ################################################################################
            # Get current use theme by user
            userCurrentTheme = os.popen(getUserThemeCMD)
            userCurrentTheme = userCurrentTheme.read().strip()
            userCurrentTheme = userCurrentTheme.replace("'", "")

            # Try to find the current icon inside /usr/share/icons
            # Get folder size fomr /usr/share/icons
            self.getThemeSize = os.popen(f"du -s /usr/share/themes/{userCurrentTheme}")
            self.getThemeSize = self.getThemeSize.read().strip("\t").strip("\n").replace(f"/usr/share/themes/{userCurrentTheme}", "").replace("\t", "")
            self.getThemeSize = int(self.getThemeSize)
            self.themeInside = True
        except:
            try:
                # If can not be found inside /usr/share/icons, try .icons in Home
                # Get folder size
                self.getThemeSize = os.popen(f"du -s {homeUser}/.themes/{userCurrentTheme}")
                self.getThemeSize = self.getThemeSize.read().strip("\t").strip("\n").replace(f"{homeUser}/.themes/{userCurrentTheme}", "").replace("\t", "")
                self.getThemeSize = int(self.getThemeSize)
                self.themeInside = True

            except:
                pass
        
        self.add_to_backup_list()

    def add_to_backup_list(self):
        self.systemSettingsFolderToBackupSizeList=[]
        # Check if Time Machine found icon and/or theme to be backup
        if self.iconInside:
            # Add icon size to list
            self.systemSettingsFolderToBackupSizeList.append(self.getIconSize)
        
        if self.themeInside:
            # Add theme size to list
            self.systemSettingsFolderToBackupSizeList.append(self.getThemeSize)

        if self.iconInside or self.themeInside:
            # Sum of system settings
            self.totalSystemSettingsFolderToBackupSize = int(sum(self.systemSettingsFolderToBackupSizeList))
   
        self.calculate_home_folders()

    def calculate_home_folders(self):
        print("Checking size of Home folders and size...")

        if str(mainIniFile.ini_allow_flatpak_data()) == "true":
            self.calculate_flatpak_folders()
        else:
            self.condition_to_continue()

    def calculate_flatpak_folders(self):
        print("Checking size of folders (Flatpak)...")

        self.condition_to_continue()
    
    def condition_to_continue(self):
        # This will check if Home + Flatpaks folders to backup has enough space to continue
        # with the backup process.
        print("Checking folders conditions (size)...")
        while True:
            ################################################################################
            # Home conditions to continue with the backup
            ################################################################################
            # Home + Icon + Theme + aditional number, just for safety
            if (int(total_home_folders_to_backup()) + 
                self.totalSystemSettingsFolderToBackupSize + 1500000 >= 
                int(free_space_home_folders())):

                print("Not enough space for new backup")
                print("Old folders will be deleted, to make space for the new ones.")
                print("Please wait...")

                ################################################################################
                # Get available dates inside TMB
                # Delete based in Dates
                ################################################################################
                try:
                    ################################################################################
                    # Delete oldest folders
                    ################################################################################
                    # Only deletes if exist more than one date folder inside
                    # Will return to the top, if free space is not enought, so app can delete more old folders
                    if len(get_backup_date()) > 1:
                        ################################################################################
                        # Write to INI file
                        ################################################################################
                        config = configparser.ConfigParser()
                        config.read(src_user_config)
                        with open(src_user_config, 'w') as configfile:
                            config.set('INFO', 'notification_add_info', "Deleting old backups...")
                            config.write(configfile)

                        # Action
                        print(f"Deleting {str(mainIniFile.ini_external_location())}/{baseFolderName}/{backupFolderName}/{get_backup_date()[-1]}...")
                        sub.run(f"rm -rf {str(mainIniFile.ini_external_location())}/{baseFolderName}/{backupFolderName}/{get_backup_date()[-1]}",shell=True)
                        
                        print(f"Deleting .trash...")
                        sub.run(f"rm -rf {str(mainIniFile.ini_external_location())}/.Trash-1000",shell=True)

                        # Return to calculate all folders to be backup
                        self.calculate_home_folders()
                
                    else:
                        # Set notification_id to 2
                        config = configparser.ConfigParser()
                        config.read(src_user_config)
                        with open(src_user_config, 'w') as configfile:
                            config.set('INFO', 'notification_id', "2")
                            # Turn backup now OFF
                            config.set('BACKUP', 'backup_now', 'false')
                            config.set('INFO', 'notification_add_info', "Please, manual delete file(s)/folder(s) inside "
                                    f"your backup device, to make space for {appName}'s backup!")
                            config.write(configfile)

                        print(f"Please, manual delete file(s)/folder(s) inside your backup device, to make space for {appName}'s "
                        "backup!")
                        exit()

                except FileNotFoundError as error:
                    print("Error trying to delete old backups!")
                    print(error)
                    exit()

            else:
                print("enough space to continue...")
                if str(mainIniFile.ini_allow_flatpak_data()) == "true":
                    ################################################################################
                    # Flatpaks conditions to continue with the backup
                    ################################################################################
                    # Sum Home folder + Flapatk var/app/ + Flapatk .local/share/flatpak
                    homePlusSystemSettingsPlusFlatpakToBackupSize = sum(
                        int(home_folders_size()) + 
                        int(flatpak_var_size()) + 
                        int(flatpak_local_size()) +
                        self.systemSettingsFolderToBackupSizeList)

                    ################################################################################
                    # Condition
                    ################################################################################
                    # Total fodlers to backup: HOme + flatpak(var/app) + flatpak + (.local/share/flatpak)
                    # FreSpace = External device free space

                    if homePlusSystemSettingsPlusFlatpakToBackupSize >= self.freeSpace:
                        # If Home folders to backup is good to continue, then check flatpaks folders
                        print("External has space enough to backup Home folders,")
                        # External devices has not space enough to backup FLatpaks folders
                        print(f"but not Flatpaks folders.")

                        # Calculate KBytes to MB or GB
                        spaceNeeded = homePlusSystemSettingsPlusFlatpakToBackupSize
                        # Condition
                        if len(str(spaceNeeded)) <= 6:
                            spaceNeeded = spaceNeeded / 1000 # Convert to MB
                            print(f"Total Space (Home + Flatpaks) needed: {(spaceNeeded):.1f} MB")
                            addToNotificationInfo = f"{(spaceNeeded):.1f} MB"

                        elif len(str(spaceNeeded)) > 6:
                            spaceNeeded = spaceNeeded / 1000000 # Convert to GB
                            print(f"Total Space (Home + Flatpaks) needed: {(spaceNeeded):.1f} GB")
                            addToNotificationInfo = f"{(spaceNeeded):.1f} GB"

                        else:
                            print(f"Total Space (Home + Flatpaks) needed: {spaceNeeded} KB")
                            addToNotificationInfo = f"{spaceNeeded} KB"

                        # Send notification to user telling the error
                        config = configparser.ConfigParser()
                        config.read(src_user_config)
                        with open(src_user_config, 'w') as configfile:
                            config.set('INFO', 'notification_id', "2")
                            config.set('INFO', 'notification_add_info', f"Space needed: {addToNotificationInfo}")
                            config.write(configfile)

                        # Signal
                        signal_exit()

                    else:
                        break

                else:
                    print("External has space enough to backup Home + Flatpaks installed names.")
                    print("External has space enough to continue.")
                    self.create_pre_folders_inside_external()

        self.create_pre_folders_inside_external()

    def create_pre_folders_inside_external(self):
        print("Creating pre folders...")
        try:
            ################################################################################
            # Create folder with DATE
            ################################################################################
            print("Creating folder with date...")
            if not os.path.exists(str(mainIniFile.date_folder_format())):
                sub.run(f"{createCMDFolder} {str(mainIniFile.date_folder_format())}",shell=True)  # Create folder with date

            ################################################################################
            # Create folder with TIME
            ################################################################################
            print("Creating folder with time...")
            if not os.path.exists(str(mainIniFile.time_folder_format())):
                sub.run(f"{createCMDFolder} {str(mainIniFile.time_folder_format())}",shell=True)

            ################################################################################
            # Create application folder
            ################################################################################
            if str(mainIniFile.ini_allow_flatpak_data()) == "true":
                # Create inside external "Var" Folder
                if not os.path.exists(str(mainIniFile.application_var_folder())):
                    sub.run(f"{createCMDFolder} {str(mainIniFile.application_var_folder())}",shell=True)  

                # Create inside external "Local" Folder
                if not os.path.exists(str(mainIniFile.application_local_folder())):
                    sub.run(f"{createCMDFolder} {str(mainIniFile.application_local_folder())}",shell=True)  

            ################################################################################
            # Create flatpak text
            ################################################################################
            if not os.path.exists(str(mainIniFile.flatpak_txt_location())):
                sub.run(f"{createCMDFile} {str(mainIniFile.flatpak_txt_location())}",shell=True)   

            ################################################################################
            # Create wallpaper folder
            ################################################################################
            if not os.path.exists(str(mainIniFile.wallpaper_main_folder())):
                sub.run(f"{createCMDFolder} {str(mainIniFile.wallpaper_main_folder())}",shell=True)   

        except FileNotFoundError as error:
            # Call error function 
            error_trying_to_backup(error)

        # Run prepare_backup first
        sub.Popen(f"python3 {src_backup_now_py}",shell=True)
        exit()


if __name__ == '__main__':
    mainIniFile = UPDATEINIFILE()
    main = PREPAREBACKUP()

