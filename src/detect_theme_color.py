from setup import *


def detect_theme_color(app):
    if app.palette().window().color().getRgb()[0] < 55:
        return True
    
    else:
        return False