# TimeMachine

A modern, cross-platform desktop application for file backups, inspired by Apple's Time Machine. It provides a user-friendly interface to manage, browse, and restore your files.

The application combines a powerful Python backend for file system monitoring and backup operations with a sleek and modern user interface built using Electron.js.

## Key Features

- **Real-time File Monitoring:** Uses `watchdog` to efficiently detect file changes in real-time, ensuring your backups are always up-to-date.
- **Automated Backups:** A background daemon manages the backup process automatically without user intervention.
- **Modern Desktop UI:** A clean and intuitive interface built with Electron, HTML, and CSS for managing your backups.
- **Easy Restore:** A simple interface to browse your backup history and restore files or folders.
- **Desktop Integration:** Includes a `.desktop` file for seamless integration with application menus on Linux.
- **Dashboard:** A central view to monitor backup status and system health.

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** Electron.js, Vanilla JavaScript (ESM)
- **Core Dependencies:**
  - `watchdog` (Python) for file system monitoring.
  - `axios` (JavaScript) for communication between the frontend and backend.

## Installation

The easiest way to install the application is by using the provided installation script.

```bash
bash install.sh
```

This script will:
1.  Copy all necessary application files to `~/.local/share/timemachine`.
2.  Create a launcher command `timemachine` in `~/.local/bin`.
3.  Add an application entry to your desktop menu.

## Usage

### Running the Application (Installed)

After running the installation script, you can launch the application in two ways:
1.  Open your terminal and run `timemachine`.
2.  Find "TimeMachine" in your computer's application menu.

### Running for Development

If you want to run the application in a development environment:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/GeovaneJefferson/timemachine.git
    cd timemachine
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

4.  **Start the application:**
    ```bash
    npm start
    ```

> **Note for Wayland users:** The application launcher forces the use of X11 (`GDK_BACKEND=x11`) to ensure proper windowing and display behavior, as Electron can have compatibility issues with Wayland.

## Uninstallation

To remove the application from your system, run the uninstallation script:

```bash
bash uninstall.sh
```
