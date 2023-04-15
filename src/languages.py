from setup import *

languageList = []

def determine_days_language(lang):
    languageList.clear()
    # ENG
    if lang == 'en':
        languageList.append("Sun")
        languageList.append("Mon")
        languageList.append("Tue")
        languageList.append("Wed")
        languageList.append("Thu")
        languageList.append("Fri")
        languageList.append("Sat")
        return languageList
    
    # DK
    elif lang == 'dk':
        languageList.append("Søn")
        languageList.append("Man")
        languageList.append("Tir")
        languageList.append("Ons")
        languageList.append("Tor")
        languageList.append("Fre")
        languageList.append("Lør")
        return languageList
    
    # ES
    elif lang == 'es':
        languageList.append("Dom")
        languageList.append("Lun")
        languageList.append("Mart")
        languageList.append("Miérc")
        languageList.append("Juev")
        languageList.append("Vier")
        languageList.append("Sáb")
        return languageList
    
    # PT
    elif lang == 'pt':
        languageList.append("Dom")
        languageList.append("Seg")
        languageList.append("Ter")
        languageList.append("Qua")
        languageList.append("Qui")
        languageList.append("Sex")
        languageList.append("Sáb")
        return languageList
    
    else:
        # ENG
        languageList.append("Sun")
        languageList.append("Mon")
        languageList.append("Tue")
        languageList.append("Wed")
        languageList.append("Thu")
        languageList.append("Fri")
        languageList.append("sat")
        return languageList