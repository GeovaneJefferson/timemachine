from setup import *

def backup_ini_file(update_now):
    # Make a copy of DB, and move it to src/
    src = SRC_USER_CONFIG_DB 
    dst = HOME_USER + "/.local/share/" + APP_NAME_CLOSE + "/src"
    sub.run(["cp", "-rv", src, dst])
            
    if update_now:
        command = src_pycache
        sub.run(["rm", "-rf", command])

        update_git(update_now)

def update_git(update_now):
    # Git pull
    print("Updating...")

    sub.run(["git", "stash"])
    sub.run(["git", "pull"])
    
    if update_now:
        delete_ini_file(update_now)

def delete_ini_file(update_now):
    # Delete DB 
    print("Deleting old ini file...")

    command = SRC_USER_CONFIG_DB
    sub.run(["rm", "-rf", command])

    if update_now:
        restore_ini_file(update_now)

def restore_ini_file(update_now):
    print("Moving the backup DB...")
    # Move the backup DB to the right location
    src = HOME_USER + "/" + ".local/share/{APP_NAME_CLOSE}/src/config.db" 
    dst = SRC_USER_CONFIG_DB
    sub.run(["mv", "-f", src, dst])
            
    if update_now:
        open_app()

def open_app():
    # Re-open application
    command = SRC_MAIN_WINDOW_PY
    sub.Popen(["python3", command])
    exit()