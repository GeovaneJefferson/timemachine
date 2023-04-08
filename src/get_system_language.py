import locale

def system_language():
    return str(locale.getdefaultlocale()).split(",")[0].replace("'","").replace("(","").split("_")[0]
if __name__ == '__main__':
    pass