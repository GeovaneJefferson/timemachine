from setup import *

def get_kde_color_scheme():
    config = configparser.ConfigParser()
    config.read(f"{homeUser}/.config/kdedefaults/kdeglobals")
    colorscheme = config['General']['ColorScheme']
    
    return colorscheme    
    # count = 0
    # for line in os.popen(getKDEUserColorSchemeCMD):
    #     # print(f"{count}: {line.strip()}")
    #     if "current color scheme" in line:
    #         break
    #     count += 1
    # line = line.replace("Icon theme","")    
    # line = line.strip().split(" ")[1]
    # return line

if __name__ == '__main__':
    pass