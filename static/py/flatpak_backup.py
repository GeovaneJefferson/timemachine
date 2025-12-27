import os
import time
import json
import logging
import subprocess
from datetime import datetime


class FlatpakBackup:
    def __init__(self, daemon):
        self.daemon = daemon
        self.last_backup_time = 0

    def backup_flatpaks(self):
        """Backs up the list of installed Flatpak applications."""
        logging.info("Starting Flatpak application backup...")

        if not self._has_driver_connection() or not self._is_backup_location_writable():
            logging.warning("Backup device not available or not writable. Skipping Flatpak backup.")
            return

        commands_to_try = [
            self.daemon.server.GET_FLATPAKS_APPLICATIONS_NAME_CONTAINER.split(),
            self.daemon.server.GET_FLATPAKS_APPLICATIONS_NAME_NON_CONTAINER.split()
        ]

        output = None
        for command in commands_to_try:
            output = self._execute_flatpak_command(command)
            if output is not None:
                break

        if output is not None and output.strip():
            success = self._save_flatpak_list(output)
            if success:
                self.last_backup_time = time.time()
                logging.info("Flatpak backup completed successfully")
        else:
            logging.error("All attempts to list Flatpak applications failed.")

    def _execute_flatpak_command(self, command: list) -> str:
        """Execute flatpak command and return output."""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30,
                check=True
            )
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            logging.error(f"Flatpak command timed out: {command}")
            return None
        except subprocess.CalledProcessError as e:
            logging.error(f"Flatpak command failed (exit {e.returncode}): {e.stderr}")
            return None
        except Exception:
            return None

    def _save_flatpak_list(self, flatpak_list: str) -> bool:
        """Save flatpak list to backup location."""
        try:
            flatpak_backup_dir = os.path.join(self.daemon.app_backup_dir, "flatpaks")
            os.makedirs(flatpak_backup_dir, exist_ok=True)
            flatpak_file = os.path.join(flatpak_backup_dir, "flatpak_applications.txt")
            
            with open(flatpak_file, 'w') as f:
                f.write(flatpak_list)
            
            # Also save as JSON
            json_file = os.path.join(flatpak_backup_dir, "flatpak_applications.json")
            applications = []
            for line in flatpak_list.splitlines():
                if line.strip():
                    parts = line.split('\t')
                    if len(parts) >= 3:
                        applications.append({
                            "name": parts[0].strip(),
                            "version": parts[1].strip(),
                            "arch": parts[2].strip(),
                            "branch": parts[3].strip() if len(parts) > 3 else "",
                            "origin": parts[4].strip() if len(parts) > 4 else ""
                        })
            
            with open(json_file, 'w') as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "total_applications": len(applications),
                    "applications": applications
                }, f, indent=2)
            
            logging.info(f"Flatpak application list saved to {flatpak_file}")
            return True
        except Exception as e:
            logging.error(f"Failed to save Flatpak list: {e}")
            return False

    def _has_driver_connection(self) -> bool:
        """Check if backup location is available."""
        return os.path.exists(self.daemon.app_backup_dir)

    def _is_backup_location_writable(self) -> bool:
        """Check if backup location is writable."""
        try:
            import uuid
            test_file = os.path.join(self.daemon.app_backup_dir, f".test_{uuid.uuid4().hex}")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            return True
        except:
            return False