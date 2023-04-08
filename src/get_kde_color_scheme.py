from setup import *

def get_kde_color_scheme():
    userKDEColorSchemeName = os.popen(getKDEUserColorSchemeCMD)

    count = 0
    for line in userKDEColorSchemeName:
        count += 1
        # print(f"{count}: {line.strip()}")
        if "current color scheme" in line:
            break

    return line.strip().split(" ")[1]

if __name__ == '__main__':
    pass
