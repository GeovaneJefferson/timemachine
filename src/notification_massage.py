from setup import *

def notification_massage(message):
    try:
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w', encoding='utf8') as configfile:
            config.set('INFO', 'notification_massage', f'{message}')
            config.write(configfile)

    except Exception as error:
        print("Notificatio Massage Error:",error)
        exit()

if __name__ == '__main__': 
    pass