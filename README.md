# Time Machine
A backup application, created using PySide6.

## Features:
* Local snapshots one or multiple times per day
* Rsync incremental
* Enter Time Machine (Can be used to restore files)
* Backup your installed apps APT and Flatpak. (Only the apps names). Obs. Work still in progress...

* Important: Time Machine does not back up system files.

## Enter Time Machine:
Obs. Work still in progress...

Enter Time Machine can be used to restore files from the external device.
To access this feature, you have to:
1. Make a backup to an external device using Time Machine.
2. For example, to recover a file you accidentally deleted from your Documents folder, open the Documents folder (Dolphin).
3. Then, right click on some file inside that folder.

Wait a moment, and you will see all back-ups files for that selected folder.

## Requirements:
* pip-pyside6

## Installation:
The "install.py" will automatically install "python3-pip" and "pip-pyside6". (Dependencies)

Inside Time Machine folder, right click, "open terminal", write "python3 install.py" and press Enter.

Example:

    python3 install.py
## Uninstall:
Inside Time Machine folder, right click, "open terminal", write "python3 uninstall.py" and press Enter.

Example:

    python3 uninstall.py

## Supported Platforms
  * Ubuntu (KDE)
  * Opensuse (KDE)
  * Fedora (KDE)

## Screenshots
![screenshot1](https://user-images.githubusercontent.com/66172718/160672425-e8111a80-062e-48d1-9161-1b3d6a4a9a22.png)
![screenshot2](https://user-images.githubusercontent.com/66172718/160672460-28f5491f-eddb-4bff-b756-6a0708407e6f.png)
![screenshot3](https://user-images.githubusercontent.com/66172718/160672472-4b1fa208-e69e-44ed-a372-e01286395f1a.png)
