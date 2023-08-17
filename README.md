## Attention!
* This project (Time Machine) is not affiliated with Apple. 
* This is a backup application created using PySide6 for Linux.
* Make sure that your clock method is "24-hour clock", not "12-hour clock" AM/PM.
* Time Machine WILL NOT ERASE OR FORMAT YOUR EXTERNAL DEVICE!

<p align="center">
  <img width="150" height="150" src="src/icons/backup_150px.png">
 <h1 align="center">Automatic PC Backups with Time Machine</h1>
</p>

Ensure the safety of your essential files by learning how to set up automatic backups for your PC using Time Machine.
Safeguard your personal data, cherished music, precious photos, and vital documents effortlessly.
Having a reliable backup system in place grants you the power to recover mistakenly deleted files or access data
that might otherwise be out of reach.

## Getting Started: Connecting Your Backup Storage

Begin by linking an external storage device, such as a USB drive, hard disk, or SSD, to your PC.

- For optimal results, aim to have a backup disk with at least twice the storage capacity of every disk or volume you
intend to back up. If your chosen backup disk falls short on space to accommodate a full backup, Time Machine will
promptly notify you.

- It's recommended to have a backup disk with at least twice the storage capacity of your target disks/volumes to ensure
comprehensive coverage. Time Machine will alert you if your backup disk lacks the space needed for a complete backup.

## Crafting Your Backup

- Automated Backups: Once you've designated your storage device within the Time Machine settings, the automated backup
process initiates seamlessly at regular intervals.

- Manual Backups: To take charge and initiate a backup manually, without waiting for the next automated cycle, simply opt
for "Back Up Now" from the Time Machine menu bar.

- Real-time Backup Status: Keep tabs on the ongoing backup activities by utilizing the Time Machine menu bar.
For instance, if a backup is on the brink of commencement, a notification will appear in the menu bar, indicating which
files or folders are currently being backed up. 
When no backup is in progress, the menu bar will display the timestamp of the most recent backup along with other relevant details.

## Tailoring Backup Frequency and Duration

- Time Machine affords you the flexibility to schedule backups on an hourly, daily, or weekly basis. As your backup disk
reaches its storage limit, the earliest backups will be automatically purged to create space for new ones.

## System Tray 

- You will notice that your system tray will from time to time change its color from White to Blue or Red.
- ![](src/screenshots/git-systemtrayicon.png)![git-systemtrayicon.png](src%2Ficons%2Fgit-systemtrayicon.png)=Normal color, 
automatically backup is ON and your backup device is connected and mounted.


-![git-systemtrayiconrun.png](src%2Ficons%2Fgit-systemtrayiconrun.png)=Time Machine is current backing up your files, after is done,
it will change to ![](src/screenshots/git-systemtrayicon.png)![git-systemtrayicon.png](src%2Ficons%2Fgit-systemtrayicon.png).


- ![git-systemtrayiconerror.png](src%2Ficons%2Fgit-systemtrayiconerror.png)=If automatically backup is ON but your backup device
is disconnected or not mounted, you will see ![git-systemtrayiconerror.png](src%2Ficons%2Fgit-systemtrayiconerror.png).
  - ![git-systemtrayiconerror.png](src%2Ficons%2Fgit-systemtrayiconerror.png) can also mean that Time Machine had some problem to back up. Open Time Machine main window and 
  read the report about it.

## Installation:
You will be asked for your password.
- Copy and paste this command bellow to the terminal.

Command:

    git clone -b dev https://github.com/geovanejefferson/timemachine; cd timemachine/; python3 install.py


## Uninstall:
Command:

    cd .local/share/timemachine/; python3 uninstall.py
