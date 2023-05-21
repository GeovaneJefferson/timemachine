from setup import *

def update_notification_status(status):
    config = configparser.ConfigParser()
    config.read(src_user_config)
    with open(src_user_config, 'w') as configfile:
        config.set('INFO', 'feedback_status', f"{status}")
        configfile.write(configfile)
