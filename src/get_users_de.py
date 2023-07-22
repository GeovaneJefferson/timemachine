from setup import *


def get_user_de():
    user_DE=os.popen(GET_USER_DE).read().strip().lower()
    
    if ":" in user_DE:
        return user_DE.split(":")[1]
    
    else:
        return user_DE        


if __name__ == '__main__':
    pass