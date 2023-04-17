from setup import *

class FONT:
    def get_kde_font(self):
        with open(f"{homeUser}/.config/kdeglobals", "r") as read:
            read = read.readlines()

            for count in range(len(read)):
                if read[count].startswith("font="):
                    return (read[count]).strip().split(",")[0].replace("font=","")

    def get_kde_font_size(self):
        with open(f"{homeUser}/.config/kdeglobals", "r") as read:
            read = read.readlines()

            for count in range(len(read)):
                if read[count].startswith("font="):
                    return (read[count]).strip().split(",")[1]


if __name__ == '__main__':
    pass