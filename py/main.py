#!/usr/bin/env python3

"""
Main entry point for the backup daemon.

This script may be executed from various working directories (the project
root when launched by the web server or the ``py`` directory during
development).  At import time many modules assume the workspace root is on
``sys.path`` (e.g. ``from py.server import SERVER``), so we add the parent of
``py`` to the path unconditionally.  This makes ``python py/main.py`` work
without having to modify the shell environment.
"""
import os
import sys
import logging
import signal
import atexit

# make sure the repository root is on sys.path so package imports resolve
# correctly regardless of cwd
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root not in sys.path:
    sys.path.insert(0, root)

try:
    import setproctitle
except ImportError:
    setproctitle = None

from daemon import Daemon


def main():
    """Main entry point."""
    daemon = None

    # Signal handler
    def signal_handler(signum, frame):
        logging.info(f"Received signal {signum}")
        if daemon:
            daemon.shutdown_event.set()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        # Initialize daemon
        daemon = Daemon()

        # Set process title
        if setproctitle:
            setproctitle.setproctitle(f'{daemon.server.APP_NAME} - daemon')

        # Register cleanup
        atexit.register(lambda: daemon.shutdown() if daemon else None)

        # Start daemon
        if not daemon.start():
            sys.exit(1)

    except KeyboardInterrupt:
        logging.info("Interrupted by user")
    except Exception as e:
        logging.error(f"Main error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
