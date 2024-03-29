from setup import *
from read_ini_file import UPDATEINIFILE
from notification_massage import notification_message_current_backing_up


MAIN_INI_FILE = UPDATEINIFILE()

async def restore_backup_flatpaks_applications():
    print("Installing flatpaks apps...")

    with open(f"{MAIN_INI_FILE.flatpak_txt_location()}", "r") as read_flatpak_file:
        read_flatpak_file = read_flatpak_file.readlines()
        
    for flatpak in read_flatpak_file:
        flatpak = flatpak.strip()

        if flatpak not in read_exclude:
            # Install only if flatpak if not in the exclude app list
            try:
                # Update DB
                MAIN_INI_FILE.set_database_value('INFO', 'current_backing_up', f'{flatpak}')
                
                print(f'Installing: {flatpak}...')
                
                notification_message_current_backing_up(f'Installing: {flatpak}...')
                
                # Install them
                sub.run(
                    ["flatpak", "install", "--system",
                    "--noninteractive", "--assumeyes", "--or-update",
                    flatpak], stdout=sub.PIPE, stderr=sub.PIPE)
                
            except Exception as e:
                print(e)
                pass


if __name__ == '__main__':
    pass
