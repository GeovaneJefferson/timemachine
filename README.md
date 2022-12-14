## Attention!
* This project (Time Machine) is not affiliated with Apple. 
* This is a backup application created using PySide6 for Linux.
* Make sure that your clock method is "24-hour clock", not "12-hour clock" AM/PM.
* Time Machine WILL NOT ERASE OR FORMAT YOUR EXTERNAL DEVICE!

<p align="center">
  <img width="150" height="150" src="src/icons/backup_150px.png">
 <h1 align="left">Back up your PC with Time Machine</h1>
</p>
Use Time Machine, the built-in backup feature of your PC, to automatically back up your personal data, music, photos and 
documents. Having a backup allows you to recover files that you later delete or can't access.

## Connect a storage device to use for backups
Connect an external storage device to your PC, such as a USB, HD or SSD.

* Ideally, your backup disk should have at least twice the storage capacity of every disk or volume you're backing up. 
If your backup disk doesn't have enough storage space to contain a complete backup, Time Machine will let you know.

## Make a backup
**Back up automatically.** After you select your storage device in Time Machine, Time Machine automatically begins making
periodic backups.

**Back up manually.** To start a backup manually, without waiting for the next automatic backup, choose Back Up Now from
the Time Machine menu ![](src/screenshots/systemtrayicon.png)![systemtrayicon.png](src%2Ficons%2Fsystemtrayicon.png) in 
the menu bar.

**Check backup status.** Use the Time Machine menu ![](src/screenshots/systemtrayicon.png)![systemtrayicon.png](src%2Ficons%2Fsystemtrayicon.png) 
in the menu bar to check the status of a backup. For example, when a backup is not underway, the menu shows the date and 
time of the latest backup.

![](src/screenshots/img_3.png)

Backup is completed.

## Browse Time Machine Backups
First, open Time Machine and allow to "show in the system tray".
Then, click on Time Machine in system tray and select "Browse Time Backups"
(Remember, will only work if Time Machine has made at least one backup already.)


## Backup frequency and duration

Time Machine is able to make hourly backups for the past 24 hours, daily backups for the past month, or weekly backups. 

The oldest backups are deleted when your backup disk is full.

### Packages
* Inside "Application" folder, in your backup device, you will find folders: "deb", "rpm" etc.
These folders were created, so you can manually put ".deb" or ".rpm" packages inside, to be easily restore after a fresh
installation with Migration Assistant.

## Migration Assistant
A Welcome Screen is in development, something similar to Apple's "Migration Assistant", a easy way to restore your 
files/folders and apps, after a fresh installation.

## System Tray 
You will notice that your system tray will from time to time change its color to White, Blue or Red.
* ![](src/screenshots/systemtrayicon.png)![systemtrayicon.png](src%2Ficons%2Fsystemtrayicon.png) = Normal color, 
automatically backup is ON and your backup device is connected and mounted.


* ![systemtrayiconrun.png](src%2Ficons%2Fsystemtrayiconrun.png) = Time Machine is current backing your files, after is done,
it will change to ![](src/screenshots/systemtrayicon.png)![systemtrayicon.png](src%2Ficons%2Fsystemtrayicon.png).


* ![systemtrayiconerror.png](src%2Ficons%2Fsystemtrayiconerror.png) = If automatically backup is ON but your backup device
is disconnected or not mounted, you will see ![systemtrayiconerror.png](src%2Ficons%2Fsystemtrayiconerror.png).
  - ![systemtrayiconerror.png](src%2Ficons%2Fsystemtrayiconerror.png) can also mean that Time Machine had some problem to back up. Open Time Machine main window and 
  read the report about it.

## Installation:
You will be asked for your password.
* Copy and paste this command bellow to the terminal.

Command:

    git clone -b dev https://github.com/geovanejefferson/timemachine; cd timemachine/; python3 install.py


## Uninstall:
Command:

    cd .local/share/timemachine/; python3 uninstall.py
