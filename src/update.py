from setup import *

def update_app():
    # Check if ini file exist and can be found
    # Make a copy and move to /src
    print("Backup user.ini file")
    sub.run(f"{copyCPCMD} {src_user_config} {homeUser}/.local/share/timemachine/src",shell=True)

    # Update
    print("Updating...")
    os.popen("git stash; git pull")

    # Restore the copy to inside "ini" folder
    print("Restoring user.ini from backup location")
    sub.run(f"{copyCPCMD} {homeUser}/.local/share/{appNameClose}/src/user.ini {src_user_config}",shell=True)

    # Delete the copy
    # print("Deleting backup user.ini")
    # sub.run(f"rm {homeUser}/.local/share/{appNameClose}/src/user.ini ", shell=True)

    # Re-open app
    print(f"Starting {src_main_window_py}")
    sub.Popen(f"python3 {src_main_window_py}", shell=True)
    exit()


update_app()