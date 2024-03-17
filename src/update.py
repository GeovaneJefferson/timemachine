from setup import *

def backup_db_file(update_now):
    # Make a copy of DB, and move it to src/
    src = SRC_USER_CONFIG_DB 
    dst = HOME_USER + "/.local/share/" + APP_NAME_CLOSE + "/src"
    # sub.run(['cp', '-rvf', src, dst])
    # shutil.copytree(src, dst)
    shutil.copy2(src, dst)
            
    if update_now:
        # sub.run(["rm", "-rf", SRC_PYCACHE])
        shutil.rmtree(SRC_PYCACHE)

        update_git(update_now)

def update_git(update_now):
    # Git pull
    print("Updating...")

    sub.run(["git", "stash"])
    sub.run(["git", "pull"])
    
    if update_now:
        delete_db_file(update_now)

def delete_db_file(update_now):
    # Delete DB 
    print("Deleting old ini file...")

    # sub.run(["rm", "-rf", SRC_USER_CONFIG_DB])
    os.remove(SRC_USER_CONFIG_DB)

    if update_now:
        restore_db_file(update_now)

def restore_db_file(update_now):
    print("Moving the backup DB...")

    # Move the backup DB to the right location
    src = HOME_USER + "/" + ".local/share/" + APP_NAME_CLOSE + "/src/config.db" 
    dst = SRC_USER_CONFIG_DB
    # sub.run(["mv", "-f", src, dst])
    shutil.move(src, dst)

    if update_now:
        open_app()

def open_app():
    # Re-open application
    sub.Popen(['python3', SRC_MAIN_WINDOW_PY])

    # Exit
    exit()