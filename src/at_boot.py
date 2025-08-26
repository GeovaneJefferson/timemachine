from server import *

# Initialize the server instance
server = SERVER()

def at_boot():
    """
    Handles the startup process for the backup daemon. Checks if the daemon is already running,
    retrieves configuration values, and starts the daemon if necessary.
    """
    try:
        # Retrieve the driver location from the database
        try:
            driver_name: str = server.get_database_value(section='DRIVER', option='Driver_Location')
            logging.info(f"Driver location retrieved: {driver_name}")
        except Exception as e:
            logging.error(f"Error retrieving driver location: {e}")
            return

        # Check if automatic backup is enabled
        try:
            automatically_backup = server.get_database_value(section='BACKUP', option='automatically_backup')
            if str(automatically_backup).lower() not in ['true', '1', 'yes']:
                logging.info("Automatic backup is disabled.")
                return
        except Exception as e:
            logging.error(f"Error retrieving automatic backup setting: {e}")
            return

        # Check if the daemon is already running
        if not server.is_daemon_running():
            # Retrieve the daemon script path
            daemon_script_path = server.DAEMON_PY_LOCATION
            if not os.path.exists(daemon_script_path):
                logging.error(f"Daemon script not found at: {daemon_script_path}")
                return

            # Start the daemon process
            try:
                process = sub.Popen(
                    ['python3', daemon_script_path],
                    stdout=sub.PIPE,
                    stderr=sub.PIPE,
                    start_new_session=True # Ensure daemon runs independently
                )
                logging.info(f"Daemon process started with PID: {process.pid}. Daemon will manage its own PID file.")
            except Exception as e:
                logging.error(f"Error starting daemon: {e}")
                return
        else:
            logging.info("Daemon is already running, not starting again.")
    except Exception as e:
        logging.error(f"Unexpected error in at_boot: {e}")


if __name__ == "__main__":
    # Delay startup for 1 second (optional, explain purpose)
    time.sleep(1)
    at_boot()