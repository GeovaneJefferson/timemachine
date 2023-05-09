from setup import *

def users_theme_name():
    userThemeName = os.popen(getUserThemeCMD)
    userThemeName = userThemeName.read().strip()
    userThemeName = userThemeName.replace("'", "")

    return userThemeName

def users_theme_size():
    try:
        userThemeSize = os.popen(f"du -s {homeUser}/.themes/{users_theme_name()}")
        userThemeSize = userThemeSize.read().strip("\t").strip("\n").replace(f"{homeUser}/.themes/{users_theme_name()}", "").replace("\t", "")
        userThemeSize = int(userThemeSize)
    except ValueError:
        try:
            userThemeSize = os.popen(f"du -s {homeUser}/.local/share/themes/{users_theme_name()}")
            userThemeSize = userThemeSize.read().strip("\t").strip("\n").replace(f"{homeUser}/.local/share/themes/{users_theme_name()}", "").replace("\t", "")
            userThemeSize = int(userThemeSize)
        except ValueError:
            try:
                userThemeSize = os.popen(f"du -s /usr/share/themes/{users_theme_name()}")
                userThemeSize = userThemeSize.read().strip("\t").strip("\n").replace(f"/usr/share/themes/{users_theme_name()}", "").replace("\t", "")
                userThemeSize = int(userThemeSize)
            except ValueError:
                return None

    return userThemeSize 

if __name__ == '__main__':
    pass