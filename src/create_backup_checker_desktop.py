from setup import *


# Remember to change INSTALL too!!!
def create_backup_checker_desktop():
    # Create autostart folder if necessary
    if not os.path.exists(SRC_AUTOSTART_FOLDER_LOCATION):
        command = SRC_AUTOSTART_FOLDER_LOCATION
        sub.run(["mkdir", command], stdout=sub.PIPE, stderr=sub.PIPE).wait()

    # Edit file startup with system
    with open(DST_BACKUP_CHECK_DESKTOP, "w") as writer:
        writer.write(
            f"[Desktop Entry]\n "
            f"Type=Application\n "
            f"Exec=/bin/python3 {HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/at_boot.py\n "
            f"Hidden=false\n "
            f"NoDisplay=false\n "
            f"Name={APP_NAME}\n "
            f"Comment={APP_NAME}'s manager before boot.\n "
            f"Icon={SRC_RESTORE_ICON}")


if __name__ == '__main__':
    pass
