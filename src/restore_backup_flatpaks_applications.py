from setup import *
from read_ini_file import UPDATEINIFILE


def restore_backup_flatpaks_applications():
    mainIniFile = UPDATEINIFILE()

    print("Installing flatpaks apps...")
    # Restore flatpak apps
    with open(f"{mainIniFile.flatpak_txt_location()}", "r") as read_file:
        read_file = read_file.readlines()

        for output in read_file:
            output = output.strip()
            with open(src_user_config, 'w') as configfile:
                config.set('INFO', 'feedback_status', f"{output}")
                config.write(configfile)

            sub.run(f"{flatpakInstallCommand} {output}", shell=True)
