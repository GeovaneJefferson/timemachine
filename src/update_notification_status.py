from setup import *

# TODO
# Delete

def update_notification_status(status):
    config = configparser.ConfigParser()
    config.read(src_user_config)
    with open(src_user_config, 'w') as configfile:
        config.set('INFO', 'current_backing_up', f"{status}")
        config.write(configfile)

if __name__ == '__main__':
    pass
