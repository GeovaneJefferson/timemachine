from server import *

def check_package_manager() -> str | None:
    """
    Determines the package manager available on the system.

    Returns:
        str: "deb" if dpkg is available, "rpm" if rpm is available.
        None: If no supported package manager is found.
    """
    try:
        # Check if dpkg command exists
        dpkg_exists = shutil.which("dpkg") is not None

        # Check if rpm command exists
        rpm_exists = shutil.which("rpm") is not None

        # Determine the package manager
        if dpkg_exists:
            logging.info("Detected package manager: dpkg (deb)")
            return "deb"
        elif rpm_exists:
            logging.info("Detected package manager: rpm")
            return "rpm"
        else:
            logging.warning("No supported package manager detected.")
            return None
    except Exception as e:
        # Log any unexpected errors
        logging.error(f"Error detecting package manager: {e}")
        return None


if __name__ == '__main__':
    pass
    # Example usage
    # package_manager = check_package_manager()
    # if package_manager:
    #     logging.info(f"Package manager detected: {package_manager}")
    # else:
    #     logging.error("No package manager detected.")