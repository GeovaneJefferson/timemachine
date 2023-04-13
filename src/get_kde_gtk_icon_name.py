from setup import *

def get_kde_gtk_icon_name():
    with open(f"{homeUser}/.config/xsettingsd/xsettingsd.conf", "r") as read:
        read = read.readlines()
        for count in range(len(read)):
            if read[count].split()[0] == "Net/IconThemeName":
                return read[count].split()[1].replace('"','')

if __name__ == '__main__':
    pass
