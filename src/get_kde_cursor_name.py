from setup import *

def users_kde_cursor_name():
    with open(f"{homeUser}/.config/xsettingsd/xsettingsd.conf", "r") as read:
        read = read.readlines()
        for count in range(len(read)):
            if read[count].split()[0] == "Gtk/CursorThemeName":
                return read[count].split()[1].replace('"','')

if __name__ == '__main__':
    pass
