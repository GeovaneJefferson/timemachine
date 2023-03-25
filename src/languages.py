from setup import *

list = []

def determine_days_language():
    config = configparser.ConfigParser()
    config.read(src_user_config)
    iniSystemLanguage = config['INFO']['language']

    # ENG
    if iniSystemLanguage == 'en':
        list.append("Sun")
        list.append("Mon")
        list.append("Tue")
        list.append("Wed")
        list.append("Thu")
        list.append("Fru")
        list.append("sat")
        return list
    
    # DK
    elif iniSystemLanguage == 'dk':
        list.append("Søn")
        list.append("Man")
        list.append("Tir")
        list.append("Ons")
        list.append("Tor")
        list.append("Fre")
        list.append("Lør")
        return list
    
    # ES
    elif iniSystemLanguage == 'es':
        list.append("Dom")
        list.append("Lun")
        list.append("Mart")
        list.append("Miérc")
        list.append("Juev")
        list.append("Vier")
        list.append("Sáb")
        return list
    
    else:
        # ENG
        list.append("Sun")
        list.append("Mon")
        list.append("Tue")
        list.append("Wed")
        list.append("Thu")
        list.append("Fru")
        list.append("sat")
        return list