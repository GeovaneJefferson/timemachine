from setup import *

def users_kde_cursor_name():
    userKDECursorName = os.popen(getKDEUserCursorCMD)

    count = 0
    for line in userKDECursorName:
        count += 1
        # print(f"{count}: {line.strip()}")
        if "Current theme for this Plasma session" in line:
            break

    return line.strip().split(" ")[1]

print(users_kde_cursor_name())
