from setup import *


def handle_spaces(string):
    string = str(string)
    
    # Handle spaces
    if " " in string:
        return string.replace(' ', '\ ')
    
    else:
        return string
    

if __name__ == '__main__':
    pass