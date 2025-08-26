from server import *

# Initialize logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

server = SERVER()

def device_location() -> str | None:
    """
    Determines the location of connected devices by checking the MEDIA and RUN paths.

    Returns:
        str: The path where devices are found ('/media' or '/run').
        None: If no devices are found.
    """
    # Construct paths to check for devices
    media_path = f'{server.MEDIA}/{server.USERNAME}'
    run_path = f'{server.RUN}/{server.USERNAME}'

    try:
        # Check for devices in MEDIA
        if os.path.exists(media_path) and os.listdir(media_path):
            #logging.info(f"Devices found in MEDIA path: {media_path}")
            return server.MEDIA
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error accessing MEDIA path: {e}")
        #logging.warning(f"Error accessing MEDIA path: {e}")

    try:
        # Check for devices in RUN if MEDIA is empty or not available
        if os.path.exists(run_path) and os.listdir(run_path):
            #logging.info(f"Devices found in RUN path: {run_path}")
            return server.RUN
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error accessing RUN path: {e}")
        #logging.warning(f"Error accessing RUN path: {e}")

    # Log and return None if no devices are found
    #logging.warning("No devices found.")
    return None


if __name__ == '__main__':
    pass
    # # Example usage
    # location = device_location()
    # if location:
    #     logging.info(f"Devices are located in: {location}")
    # else:
    #     logging.error("No devices detected.")
