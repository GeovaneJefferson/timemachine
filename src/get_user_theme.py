from setup import *

def users_theme_name():
    userThemeName = os.popen(getUserThemeCMD)
    userThemeName = userThemeName.read().strip()
    userThemeName = userThemeName.replace("'", "")

    return userThemeName