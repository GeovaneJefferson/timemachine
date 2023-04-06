from setup import *

def users_kde_color_scheme_name():
    userKDEColorSchemeName = os.popen(getKDEUserColorSchemeCMD)

    count = 0
    for line in userKDEColorSchemeName:
        count += 1
        # print(f"{count}: {line.strip()}")
        if "current color scheme" in line:
            break

    return line.strip().split(" ")[1]

print(users_kde_color_scheme_name())
