from setup import *

def users_kde_cursor_name():
    with open(f"{homeUser}/.config/xsettingsd/xsettingsd.conf", "r") as read:
        read = read.readlines()
        for count in range(len(read)):
            if read[count].split()[0] == "Gtk/CursorThemeName":
                return read[count].split()[1].replace('"','')

    # userKDECursorName = os.popen(getKDEUserCursorCMD)

    # count = 0
    # for line in userKDECursorName:
    #     count += 1
    #     if "Current theme for this Plasma session" in line:
    #         break

    # return line.strip().split(" ")[1]

if __name__ == '__main__':
    pass
