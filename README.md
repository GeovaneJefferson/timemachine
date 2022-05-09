# Time Machine
A backup application, created using PySide6.

## Features:
* Local snapshots one or multiple times per day
* Rsync incremental
* Enter Time Machine (Coming soon...)
* The oldest backups are deleted when your backup disk is full.


* Important: Time Machine does not back up system files!


## Info:
### The oldest backups are deleted when your backup disk is full.

Time Machine will automatically delete the oldest backup, until has enough space for a new backup, but will keep at least one backup left.

#### Still not enough space for a new backup?

Time Machine will send you a notification, asking you to manually delete some file(s)/folder(s), so it can proceed with the backup. 

## Enter Time Machine:
Coming soon...

## Requirements:
* pip-pyside6

## Installation:
You will be asked for your password! 
Before begin with the installation, please, make sure that your system is updated :D

The "install.py" will automatically install "python3-pip" and "pip-pyside6". (Dependencies)

Inside Time Machine folder, right click, "open terminal", write "python3 install.py" and press Enter.

Example:

    python3 install.py
    
## Uninstall:
Inside Time Machine folder, right click, "open terminal", write "python3 uninstall.py" and press Enter.

Example:

    python3 uninstall.py

## Tested Platforms
  * Ubuntu 
  * Elementary OS
  * MXLinux (KDE)
  * Opensuse (KDE)
  * Fedora 
  * Manjaro (KDE)
  * EndeavourOS

## Screenshots
![img.png](src/screenshots/img.png)
![img_1.png](src/screenshots/img_1.png)