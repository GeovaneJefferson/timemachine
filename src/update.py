from setup import *

def backup_ini_file(update_now):
    # Check if ini file exist and can be found
    # Make a copy and move to /src
    sub.run(f"{COPY_CP_CMD} {SRC_USER_CONFIG_DB} {HOME_USER}/.local/share/{APP_NAME_CLOSE}/src", shell=True)
    
    if update_now:
        sub.run(f"rm -rf {src_pycache}", shell=True)
        update_git(update_now)

def update_git(update_now):
    print("Updating...")

    sub.Popen(["git", "stash"])
    # sub.Popen(["git", "reset", "--hard"])
    sub.Popen(["git", "pull"])
    
    if update_now:
        delete_ini_file(update_now)

def delete_ini_file(update_now):
    print("Deleting old ini file...")

    sub.run(f"rm -f {SRC_USER_CONFIG_DB}", shell=True)

    if update_now:
        restore_ini_file(update_now)

def restore_ini_file(update_now):
    sub.run(f"{COPY_CP_CMD} {HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/config.db {SRC_USER_CONFIG_DB}",shell=True)
    
    if update_now:
        open_app()

def open_app():
    sub.Popen(f"python3 {SRC_MAIN_WINDOW_PY}", shell=True)
    exit()