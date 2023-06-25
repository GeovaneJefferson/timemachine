from setup import *


def create_backup_checker_desktop():
    # Create autostart folder if necessary
    if not os.path.exists(src_autostart_folder_location):
        sub.run(f"{createCMDFolder} {src_autostart_folder_location}", shell=True)
    
    print("Creating backup_check.desktop ...")
    with open(dst_backup_check_desktop, "w") as writer: 
        writer.write(
            f"[Desktop Entry]\n "
            f"Type=Application\n "
            f"Exec=/bin/python3 {homeUser}/.local/share/{appNameClose}/src/at_boot.py\n "
            f"Hidden=false\n "
            f"NoDisplay=false\n "
            f"Name={appName}\n "
            f"Comment={appName}'s manager before boot.\n "
            f"Icon={src_restore_icon}")
        
if __name__ == '__main__':
    pass