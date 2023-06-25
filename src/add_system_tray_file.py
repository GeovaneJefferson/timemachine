from setup import *

def add_system_tray_file():
    if not os.path.isfile(f"{dst_folder_timemachine}/src/system_tray_is_running.txt"):
        os.mkfifo(f"{dst_folder_timemachine}/src/system_tray_is_running.txt")
        return True
    else:
    	return False

def can_system_tray_file_be_found():
    if os.path.exists(f"{dst_folder_timemachine}/src/system_tray_is_running.txt"):
        return True
    else:
        return False
    
def remove_system_tray_file():
    sub.run(f"rm {dst_folder_timemachine}/src/system_tray_is_running.txt",shell=True)

if __name__ == '__main__':
	pass