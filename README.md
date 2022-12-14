## Attention!
* This project (Time Machine) is not affiliated with Apple. 
* This is a backup application created using PySide6 for Linux.
* Make sure that your clock method is "24 hour clock", not "12 hour clock" AM/PM.
* Time Machine WILL NOT ERASE OR FORMAT YOUR EXTERNAL DEVICE!

<p align="center">
  <img width="150" height="150" src="src/icons/backup_150px.png">
 <h1 align="left">Back up your PC with Time Machine</h1>
</p>
Use Time Machine, the built-in backup feature of your PC, to automatically back up your personal data, music, photos and documents. Having a backup allows you to recover files that you later delete or can't access.

## Connect a storage device to use for backups
Connect an external storage device to your PC, such as a USB, HD or SSD.

* Ideally, your backup disk should have at least twice the storage capacity of every disk or volume you're backing up. If your backup disk doesn't have enough storage space to contain a complete backup, Time Machine will let you know.

## Make a backup
**Back up automatically**. After you select your storage device in Time Machine, Time Machine automatically begins making periodic backups.

**Back up manually**. To start a backup manually, without waiting for the next automatic backup, choose Back Up Now from the Time Machine menu ![](src/screenshots/systemtrayicon.png) in the menu bar.

**Check backup status**. Use the Time Machine menu ![](src/screenshots/systemtrayicon.png) in the menu bar to check the status of a backup. For example, when a backup is not underway, the menu shows the date and time of the latest backup.

## Browse Time Machine Backups
First, open Time Machine and allow to "show in the system tray".

Then, click on Time Machine in system tray and select "Browse Time Backups"
(Remember, will only work if Time Machine has made at least one backup already.)

## Create a Time Machine backup
1. Connect an external storage device, such as a USB or HD/SSD.
2. Open Time Machine, click on "Select Backup Disk". This can also be done via system tray Time Machine, after enabled.
3. Then, click on "Back Up Now".

By now, Time Machine will backup:
* Your files and folders (If you choose to)
* Flatpaks installed names
* Flatpaks installed Data (If you choose to) - Not fully tested
* Wallpaper (Automatic, Only for Gnome) 
* Theme, Icon and cursor theme.

#### Packages
* Inside of "Application" folder, in your backup device, you will find folders: "deb", "rpm" etc.
These folders was created, so you can manual put ".deb" or ".rpm" packages inside, to be easily restore with
Migration Assistant.

## Migration Assistant
A Welcome Screen is in development, something similar to Apple's "Migration Assistant", a easy way to restore your files/folders and apps, after a fresh install.

## System Tray 
You will notice that your system tray will from time to time change its color to White, Blue or Red.
* White = Normal color, automatically backup is ON and your backup device is connected and mounted.
* Blue = Time Machine is current backing your files, after is done, it will changes to White color.
* Red = If automatically backup is ON but your backup device is disconnected or not mounted, you will see a Red system tray icon.
  - Red system tray icon can also mean that Time Machine had some problem to back up. Open Time Machine main window and read the report about it.

## Requirements
* pyside6

## Installation:
You will be asked for your password.
* Copy and paste this command bellow to the terminal.

Example:

    git clone -b dev https://github.com/geovanejefferson/timemachine; cd timemachine/; python3 install.py


## Uninstall:
Command:

    cd .local/share/timemachine/; python3 uninstall.py

## Screenshots:
![](src/screenshots/img.png)
![](src/screenshots/img_2.png)
![](src/screenshots/img_3.png)
