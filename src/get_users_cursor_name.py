from setup import *
from get_user_de import get_user_de

def users_cursor_name():
    if get_user_de() == 'kde':
        count = 0
        for line in os.popen(getKDEUserCursorCMD):
            count += 1
            # print(f"{count}: {line.strip()}")
            if "Current theme for this Plasma session" in line:
                break

        return line.strip().split(" ")[1]

    else:
        userCursorName = os.popen(getUserCursorCMD)
        userCursorName = userCursorName.read().strip()
        userCursorName = userCursorName.replace("'", "")

    return userCursorName
