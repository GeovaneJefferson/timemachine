
from static.py.server import *
server = SERVER()


def base_folders_creation():
    """Ensure necessary directories exist."""
    app_main_backup_dir = str(server.app_main_backup_dir())

    try:
        # Create main backup folder
        os.makedirs(app_main_backup_dir, exist_ok=True)
        return True
    except PermissionError as e:
        return False
    except Exception as e:
        return False


if __name__ == '__main__':
    pass