from setup import *
from read_ini_file import UPDATEINIFILE
from notification_massage import notification_message
# from get_flatpaks_folders_size import flatpak_var_list, flatpak_local_list


MAIN_INI_FILE = UPDATEINIFILE()

async def backup_flatpak():
    counter = 0
    flatpak_list = []

    try:
        # Write all installed flatpak apps by the name
        with open(MAIN_INI_FILE.flatpak_txt_location(), 'w') as configfile:
            for flatpak in os.popen(GET_FLATPAKS_APPLICATIONS_NAME):
                flatpak_list.append(flatpak)

                configfile.write(flatpak_list[counter])
                
                notification_message(f'Backing up: {flatpak_list[counter]}')
                
                counter += 1
    
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
    #                 ["cp", "-rvf", command], 
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
    #                 ["cp", "-rvf", command],
    #                 stdout=sub.PIPE,
    #                 stderr=sub.PIPE)
        
    #     except:
    #         pass


if __name__ == '__main__':
    pass