from setup import *

USER_DE = os.popen(GET_USER_DE).read().strip().lower()

def get_user_de():
    if ":" in USER_DE:
        return USER_DE.split(":")[1]
    else:
        return USER_DE        

if __name__ == '__main__':
    pass