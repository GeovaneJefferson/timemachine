from setup import *
from read_ini_file import UPDATEINIFILE
from notification_massage import notification_message
from create_directory import create_directory, create_file


MAIN_INI_FILE = UPDATEINIFILE()

def backup_pip_packages():
    # Check for pip packages file
    
    ################################################################################
    # Create pip text file
    ################################################################################
    pip_packages_txt_location = MAIN_INI_FILE.pip_packages_txt_location()
    
    # Check if the directory exists, and create it if necessary
    create_directory(pip_packages_txt_location)
    # Check if the file exists, and create it if necessary
    create_file(pip_packages_txt_location)

    ################################################################################
    # Get pip packages list
    ################################################################################
    try:
        pip_freeze_output = sub.check_output(
            ['pip', 'freeze']).decode(
            'utf-8')

        lenght_of_packages = len(str(pip_freeze_output).split())

        # Remove paskages versions numbers
        count = 0
        with open(MAIN_INI_FILE.pip_packages_txt_location(), 'w') as file:
            for line in str(pip_freeze_output).split():
                line = pip_freeze_output.split()[count].split('==')[0] 

                # Do not use '\n' at the last number
                if (lenght_of_packages - 1) != count:
                    file.write(line + '\n')

                else:
                    file.write(line)
                
                # Notification
                notification_message(f'Backing up PIP: {line}')

                count += 1 

    except:
        pass


if __name__ == '__main__':
    backup_pip_packages()