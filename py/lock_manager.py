import os
import json
import threading
import time
import logging


class LockManager:
    def __init__(self, daemon):
        self.daemon = daemon
        self.ready_file_path = os.path.join(os.path.expanduser("~"), 
                                          f'.{daemon.server.APP_NAME.lower()}_daemon_ready')
        self.lock_file_path = os.path.join(os.path.expanduser("~"), 
                                         f'.{daemon.server.APP_NAME.lower()}_daemon.lock')

    def create_ready_state(self):
        """Create ready state file."""
        try:
            # FIXED: Access metadata.metadata directly
            with open(self.ready_file_path, 'w') as f:
                json.dump({
                    'pid': os.getpid(),
                    'ready_time': time.time(),
                    'metadata_count': len(self.daemon.metadata.metadata),
                    'flatpak_last_backup': self.daemon.flatpak_backup.last_backup_time,
                    'version': '2.1'
                }, f, indent=2)
            return True
        except Exception as e:
            logging.error(f"Failed to create ready state: {e}")
            return False

    def remove_ready_state(self):
        """Remove ready state file."""
        try:
            if os.path.exists(self.ready_file_path):
                os.remove(self.ready_file_path)
        except:
            pass

    def create_lock_file(self):
        """Create lock file."""
        try:
            with open(self.lock_file_path, 'w') as f:
                f.write(str(os.getpid()))
            return True
        except Exception as e:
            logging.error(f"Failed to create lock file: {e}")
            return False

    def remove_lock_file(self):
        """Remove lock file."""
        try:
            if os.path.exists(self.lock_file_path):
                os.remove(self.lock_file_path)
        except:
            pass

    def remove_socket_file(self):
        """Remove socket file."""
        try:
            control_socket_path = self.daemon.server.SOCKET_PATH + '.ctrl'
            if os.path.exists(control_socket_path):
                os.remove(control_socket_path)
                logging.info(f"Removed control socket: {control_socket_path}")
        except Exception as e:
            logging.error(f"Error removing control socket: {e}")