from setup import *

def backup_ini_file(updateNow):
    # Check if ini file exist and can be found
    # Make a copy and move to /src
    sub.run(f"{copyCPCMD} {src_user_config} {homeUser}/.local/share/timemachine/src",shell=True)
    if updateNow:
        update_git(updateNow)

def update_git(updateNow):
    os.popen("git stash; git pull")
    if updateNow:
        restore_ini_file(updateNow)

def delete_ini_file():
    sub.run(f"rm {homeUser}/.local/share/{appNameClose}/src/user.ini ", shell=True)

def restore_ini_file(updateNow):
    sub.run(f"{copyCPCMD} {homeUser}/.local/share/{appNameClose}/src/user.ini {src_user_config}",shell=True)
    if updateNow:
        open_app(updateNow)

def open_app(updateNow):
    sub.Popen(f"python3 {src_main_window_py}", shell=True)
    exit()

