from setup import *

def backup_ini_file(updateNow):
    """
    Check if ini file exist and can be found
    Make a copy and move to /src
    """
    sub.run(f"{copyCPCMD} {src_user_config} {homeUser}/.local/share/{appNameClose}/src",shell=True)
    if updateNow:
        update_git(updateNow)

def update_git(updateNow):
    sub.run("git stash; git pull",shell=True)
    if updateNow:
        delete_ini_file(updateNow)

def delete_ini_file(updateNow):
    sub.run(f"rm -f {src_user_config}", shell=True)
    if updateNow:
        restore_ini_file(updateNow)

def restore_ini_file(updateNow):
    sub.run(f"{copyCPCMD} {homeUser}/.local/share/{appNameClose}/src/user.ini {src_user_config}",shell=True)
    if updateNow:
        open_app()

def open_app():
    sub.Popen(f"python3 {src_main_window_py}", shell=True)
    exit()

