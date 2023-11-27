from setup import *
from read_ini_file import UPDATEINIFILE
from notification_massage import notification_message


MAIN_INI_FILE = UPDATEINIFILE()

def backup_pip_packages():
    try:
        # Get pip packages
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

    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    backup_pip_packages()