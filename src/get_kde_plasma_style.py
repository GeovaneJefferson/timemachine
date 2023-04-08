from setup import *

def users_kde_plasma_style_name():
    userKDEPlasmaStyleName = os.popen(getKDEUserPlasmaStyleCMD)

    count = 0
    for line in userKDEPlasmaStyleName:
        count += 1
        # print(f"{count}: {line.strip()}")
        if "current theme for this Plasma session" in line:
            break

    return line.strip().split(" ")[1]

if __name__ == '__main__':
    pass