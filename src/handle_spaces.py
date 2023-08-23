from setup import *

def handle_spaces(string):
    # Handle spaces
    if " " in string:
        return string.replace(' ', '\ ')
    else:
        return string