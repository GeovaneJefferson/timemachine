from setup import *


def get_kde_icon_name():
    with open(f"{HOME_USER}/.config/kdeglobals", "r") as read:
        read = read.readlines()
        
        for counter in range(len(read)):
            try:
                if '[Icons]' in read[counter]:
                    break
            except:
                pass 

        return read[counter+1].split()[0].replace('Theme=','')


if __name__ == '__main__':
    pass
