from setup import *

def update_app():
    # Check if ini file exist and can be found
    if os.path.exists(src_user_config):
        # Make a copy and move to /src
        sub.run(
            f"{copyCPCMD} {src_user_config} {homeUser}/.local/share/timemachine/src",shell=True)

    # Update
    os.popen("git stash; git pull")

    # Delete the old ini file inside "ini" folder
    # sub.run(f"rm {src_user_config}", shell=True)

    # Restore the copy to inside "ini" folder
    # sub.run(f"{copyCPCMD} {homeUser}/.local/share/{appNameClose}/src/user.ini {src_user_config}",shell=True)
    sub.run(f"cp -rv {homeUser}/.local/share/{appNameClose}/src/user.ini {src_user_config}",shell=True)

    # Delete the copy
    # sub.run(f"rm {homeUser}/.local/share/{appNameClose}/src/user.ini ", shell=True)


    # Re-open app
    sub.Popen(f"python3 {src_main_window_py}", shell=True)
    exit()

update_app()