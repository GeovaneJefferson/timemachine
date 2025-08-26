from server import *

# Initialize the server instance
server = SERVER()

def has_driver_connection() -> bool:
    """
    Checks if there is a connection to the backup driver.

    Returns:
        bool: True if the backup driver is connected, False otherwise.
    """
    try:
        # Check connection to the backup driver
        if os.path.exists(server.DRIVER_LOCATION):
            logging.info(f"Connection to backup driver established: {server.DRIVER_LOCATION}")
            return True  # Connection exists
        else:
            logging.warning(f"No connection to backup device: {server.DRIVER_LOCATION}")
            return False  # No connection
    except Exception as e:
        # Log an error if the driver location cannot be retrieved
        logging.error(f"Error reading {server.APP_NAME}'s database: {e}")
        return False

if __name__ == '__main__':
    pass
    # # Example usage
    # if has_driver_connection():
    #     logging.info("Backup driver is connected.")
    # else:
    #     logging.error("Backup driver is not connected.")
