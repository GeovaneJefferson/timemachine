from setup import *


def notification_message(message):
    CONFIG = configparser.ConfigParser()
    CONFIG.read(SRC_USER_CONFIG)
    with open(SRC_USER_CONFIG, 'w') as configfile:
        CONFIG.set('INFO', 'current_backing_up', f'{message}')
        CONFIG.write(configfile)


if __name__ == '__main__':
    pass