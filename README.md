## Attention!
* This project (Time Machine) is not affiliated with Apple. 
* This is a backup application created using PySide6 for Linux.
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
When no backup is in progress, the menu bar will display the timestamp of the most recent backup along with other
relevant details. As your backup disk
reaches its storage limit, the earliest backups will be automatically purged to create space for new ones.

## Backup Frequency and Retention

- Time Machine follows a comprehensive backup strategy:

    Hourly Backups: Time Machine automatically creates backups every hour, preserving the last 24 hours of your selected home's data. This ensures that you can quickly recover files or data from the past day.

    Efficient Storage Management: When your backup disk reaches its capacity, Time Machine intelligently manages your backups. It automatically deletes the oldest backups to make room for new ones, maintaining an efficient storage balance.

    Minimal Disruption: The initial backup may take some time to complete, but you can continue using your computer without interruption. Subsequent backups are much faster since Time Machine only copies files that have changed since the last backup.

Time Machine's backup strategy combines convenience and efficiency to safeguard your data without disrupting your workflow.

## Monitoring Backup Status

- **Color Indicators:** Keep an eye on your system tray's color changes to stay informed about your backup status:
  - Green dot, a backup is been made right now.

Time Machine is currently in the process of backing up your files. Once the backup is complete, it will revert to the
normal icon.


- **Error Alerts:** If automatic backup is ON but your backup device becomes disconnected or is not mounted, you'll see
a red dot.
This could also indicate an issue
encountered during the backup process. In such cases, open the Time Machine main window and refer to the provided report
for details.


## Installation
During the installation process, you will need to provide your system password. Follow these steps:

1. Open a terminal.
2. Copy and paste the following command:


#### Command:

    git clone -b dev https://github.com/geovanejefferson/timemachine; cd timemachine/; python3 install.py



## Uninstall
To uninstall the application, use the following steps:

1. Open a terminal.
2. Copy and paste the following command to navigate to the uninstallation directory:

#### Command:

    cd .local/share/timemachine/; python3 uninstall.py

### To-Do List
- [x] Backup files/folders, flatpaks, wallpaper
- [x] System tray
- [ ] Redo UI
- [ ] Redo code (Cleaning)
- [ ] Enter in Time Machine (To restore files/folder)
- [ ] Migration Assistant (To restore and reinstall all files/folders, .debs, .rpm, wallpaper)

### Screenshoots
![Screenshot](https://raw.githubusercontent.com/GeovaneJefferson/timemachine/dev/src/screenshots/img_4.png)

