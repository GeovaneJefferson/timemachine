from setup import *
from get_user_de import get_user_de
from get_kde_font import FONT

def get_user_font():
    if get_user_de() == 'kde':
        mainFont = FONT()
        return  f"{mainFont.get_kde_font()}, {mainFont.get_kde_font_size()}"

    else:
        userFontName = os.popen(getUserFontCMD)
        userFontName = userFontName.read().replace("'", "")
        userFontName = " ".join(userFontName.split())
        return userFontName 
    
if __name__ == '__main__':
    pass