TimeMachine Backup

A modern backup application for Linux (tested on Fedora) that provides automated file backup and synchronization with a web-based interface.
Why Flask?

I built this with Flask because I wanted to learn web application development. While Electron might not be ideal for all desktop applications, using Flask allowed me to:

    Create a responsive web interface accessible from any browser

    Learn modern web development patterns

    Build a system that can potentially be accessed remotely

    Separate the UI from the backup engine for cleaner architecture

The web interface approach also means I could quickly iterate on the UI without dealing with native toolkit complexities. That said, I'm considering rewriting the UI in Gtk4 or Qt6 in the future for better native integration.
Features

    Linux Desktop Application: Optimized for Linux systems (tested on Fedora)

    Modern Web Interface: Responsive UI built with HTML/CSS and Tailwind CSS

    Python Backend: Flask server handling backup logic and daemon management

    Automated Backups: Set up once and let the daemon handle the rest

    Folder Selection: Choose specific folders to include in your backups

    Background Daemon: Runs continuously even after closing the UI

    File Search & Restore: Find and restore files from backups with hash-based location tracking

    Version History: Access multiple versions of backed up files

    Storage Device Management: Select and manage backup storage devices

Project Structure
text

timemachine-electron/
├── config/              # Configuration files
├── static/             # Static assets (CSS, JS, images)
├── templates/          # HTML templates
├── .gitignore          # Git ignore rules
├── Requirements.txt    # Python dependencies
├── app.py             # Flask application and web interface
├── daemon.py          # Backup daemon with watchdog monitoring
├── server.py          # Core server functionality
└── [other modules]    # Additional Python modules

To Run

    Install Python dependencies
    bash

pip install -r Requirements.txt

Start the Flask server
bash

python3 app.py

    The server will typically run on http://localhost:5000

    Open the web interface in your browser and navigate to http://localhost:5000

    Setup your backup:

        Under Devices, select your backup storage device

        In Preferences, choose folders to be backed up

        Click "RUN" at the top of the page to start the backup daemon

    You may now:

        Close the browser tab/window

        Stop the Flask server (app.py)

    The backup daemon will continue running in the background.

Important: Starting the Daemon

The daemon does NOT start automatically after configuration! You must explicitly:

    Complete device selection and folder configuration

    Click the "RUN" button at the top of the web interface

    The daemon will start in the background and begin monitoring your selected folders

Important: After System Reboot

⚠️ AUTO-START NOT YET IMPLEMENTED ⚠️

Currently, the backup daemon does NOT automatically start when your computer boots up. You need to manually start it after every system reboot:

    Start the Flask server (if not already running):
    bash

python3 app.py

    Open the web interface at http://localhost:5000

    Click the "RUN" button again to restart the daemon

Note: The autostart feature is on my TODO list. Until it's implemented, you'll need to manually start the daemon after each system restart.
Key Components
app.py - Web Interface

    Flask-based web application

    Device selection and management

    Folder configuration interface

    File search and restore functionality

    Backup status monitoring

    WebSocket for live transfer updates

    "RUN" button to manually start the daemon

daemon.py - Backup Engine

    Watchdog-based file system monitoring

    Incremental backup system

    Atomic file operations

    Hardlink optimization for unchanged files

    Flatpak application backup

    Background daemon with UNIX socket control

    Manually started via the "RUN" button in the UI

Backup Features

    Real-time Monitoring: Watches selected folders for changes

    Incremental Backups: Only copies changed files

    Hardlink Optimization: Reuses unchanged file data

    Atomic Operations: Safe file copying with journaling

    Moved File Detection: Tracks renamed and moved files

    Flatpak Backup: Periodically backs up installed Flatpak applications

    Manual Control: You decide when to start/stop the backup process

File Search & Restore

    Hash-based Search: Find moved files using content hashing

    Database Tracking: Tracks file locations across moves

    Version History: Access previous versions of files

    Quick Restore: Restore files to original or custom locations

Development
Technology Stack

    Backend: Python, Flask

    File Monitoring: Watchdog

    Database: SQLite for file location tracking

    System Integration: psutil, platform-specific tools

Future Considerations

    GTK4/Qt6 UI: Considering native toolkit for better integration

    System Tray: Add tray icon for quick access

    Native Notifications: Better system integration

    Configuration Wizard: Improved setup experience

    Auto-start: Implement systemd service or autostart entry (TODO)

File Descriptions

    app.py: Main web application with API endpoints

    daemon.py: Core backup daemon with monitoring

    server.py: Shared server functionality and constants

    search_handler.py: File search and indexing

    storage_util.py: Storage device detection

    daemon_control.py: Daemon management utilities

Requirements

    Python 3.7+

    Linux (tested on Fedora)

    Required Python packages (see Requirements.txt):

        Flask

        watchdog

        psutil

        flask-sock

Note

This application is specifically designed and tested for Linux systems, with Fedora as the primary development platform. Some features may require adjustment for other Linux distributions.

Important Reminders:

    After configuring your backup, you must click the "RUN" button at the top of the page to actually start the backup daemon!

    After system reboot, you need to manually start the Flask server and click "RUN" again (autostart not yet implemented)

    The daemon continues running in the background even after closing the web interface
