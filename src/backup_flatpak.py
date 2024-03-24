from setup import *
from read_ini_file import UPDATEINIFILE
from notification_massage import notification_message


MAIN_INI_FILE = UPDATEINIFILE()

def backup_flatpak():
    flatpak_list= []

    try:
        # Open flatpak file
        with open(MAIN_INI_FILE.flatpak_txt_location(), 'w') as configfile:
            for flatpak in os.popen(GET_FLATPAKS_APPLICATIONS_NAME):
                flatpak = str(flatpak).strip()

                # Filter list to remove dupli
                if flatpak not in flatpak_list:
                    flatpak_list.append(flatpak)
                
                    # Write to file
                    configfile.write(flatpak + '\n')
                        
                    notification_message(f'Backing up: {flatpak}')
    except Exception:
        pass
    

    # # Backup flatpak data
    # if MAIN_INI_FILE.get_database_value('STATUS', 'allow_flatpak_data'):
    #     try:
    #         # .var/app
    #         for counter in range(len(flatpak_var_list())):
    #             # Copy the Flatpak var/app folders
    #             src = flatpak_var_list()[counter]
    #             dst = MAIN_INI_FILE.flatpak_var_folder()
    #             command = src + ' ' + dst
                
    #             notification_message(
    #                 f'Backing up: {flatpak_var_list()[counter]}')
                
    #             print(f'Backing up: {flatpak_var_list()[counter]}')
                
    #             sub.run(
    #                 ['cp', '-rvf', command], 
    #                 stdout=sub.PIPE, 
    #                 stderr=sub.PIPE)

                
    #         # .local/share/flatpak
    #         for counter in range(len(flatpak_local_list())):
    #             # Copy the Flatpak var/app folders
    #             src = flatpak_local_list()[counter]
    #             dst = MAIN_INI_FILE.flatpak_local_folder()
    #             command = src + ' ' + dst

    #             notification_message(
    #                 f'Backing up: {flatpak_local_list()[counter]}')

    #             print(f'Backing up: {flatpak_local_list()[counter]}')

    #             sub.run(
    #                 ['cp', '-rvf', command],
    #                 stdout=sub.PIPE,
    #                 stderr=sub.PIPE)
        
    #     except:
    #         pass


if __name__ == '__main__':
    pass