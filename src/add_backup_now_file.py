from setup import *

def add_backup_now_file():
    if not os.path.exists(f"{src_folder_timemachine}/src/backup_now_is_running.txt"):
        os.mkfifo(f"{src_folder_timemachine}/src/backup_now_is_running.txt")
        return True
    else:
        return False

def can_backup_now_file_be_found():
    if os.path.exists(f"{src_folder_timemachine}/src/backup_now_is_running.txt"):
        return True
    else:
        return False

if __name__ == '__main__':
	pass