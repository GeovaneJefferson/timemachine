from setup import *

USER_DE = os.environ.get(GET_USER_DE).lower()

def get_user_de():
    if ':' in USER_DE:
        return USER_DE.split(':')[1]
    else:
        return USER_DE        


if __name__ == '__main__':
    pass