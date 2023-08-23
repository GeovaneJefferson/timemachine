from setup import *

def backup_ini_file(update_now):
    # Make a copy of DB, and move it to src/
    sub.run(f"{COPY_CP_CMD} {SRC_USER_CONFIG_DB} {HOME_USER}/.local/share/{APP_NAME_CLOSE}/src", shell=True)
    
    if update_now:
        sub.run(f"rm -rf {src_pycache}", shell=True)
        update_git(update_now)

def update_git(update_now):
    # Git pull
    print("Updating...")

    sub.run(["git", "stash"], check=True)
    sub.run(["git", "pull"], check=True)
    
    if update_now:
        delete_ini_file(update_now)

def delete_ini_file(update_now):
    # Delete DB 
    print("Deleting old ini file...")

    sub.run(f"rm -f {SRC_USER_CONFIG_DB}", shell=True)

    if update_now:
        restore_ini_file(update_now)

def restore_ini_file(update_now):
    print("Moving the backup DB...")
    # Move the backup DB to the right location
    sub.run(f"mv -f {HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/config.db {SRC_USER_CONFIG_DB}",shell=True)
    
    if update_now:
        open_app()

def open_app():
    # Re-open application
    sub.Popen(f"python3 {SRC_MAIN_WINDOW_PY}", shell=True)
    exit()