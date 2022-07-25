#! /usr/bin/python3
from setup import *

config = configparser.ConfigParser()
config.read(src_user_config)


class UI(QWidget):
    def __init__(self):
        super().__init__()

        # Variables
        self.filesToRestore = []
        self.filesToRestoreWithSpace = []

        # Folders
        self.currentFolder = str()
        
        # Times
        self.timeFolders = []
        self.countForTime = 0
        self.excludeTimeList = []

        # Dates
        self.dateFolders = []
        self.dateIndex = 0
        self.countForDate = 0
        self.alreadyGotDateList = False

        self.iniUI()

    def iniUI(self):
        ################################################################################
        # Window manager
        ################################################################################
        self.setWindowTitle(f"Enter {appName}")
        self.setWindowIcon(QIcon(src_restore_icon))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.showFullScreen()

        self.read_ini_file()

    def read_ini_file(self):
        ################################################################################
        # Read ini
        ################################################################################
        self.iniExternalLocation = config['EXTERNAL']['hd']
        self.iniFolder = config.options('FOLDER')

        self.widgets()

    def widgets(self):
        ################################################################################
        # Base layouts
        ################################################################################
        # Base vertical layout
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setAlignment(QtCore.Qt.AlignVCenter)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        
        # Middle horizontal layout
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setAlignment(QtCore.Qt.AlignHCenter)
        self.horizontalLayout.setSpacing(20)

        # Cancel and restore layout
        self.cancelRestoreLayout = QHBoxLayout()
        self.cancelRestoreLayout.setSpacing(20)
        self.cancelRestoreLayout.setContentsMargins(20, 20, 20, 20)
        
        # Up down layout
        self.updownLayoutV = QVBoxLayout()
        
        # Time layout
        self.timeLayoutV = QVBoxLayout()
        self.timeLayoutV.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.timeLayoutV.setSpacing(20)
        self.timeLayoutV.setContentsMargins(20, 0, 20, 0)

        # Result layout
        self.foldersLayout = QVBoxLayout()
        self.foldersLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.foldersLayout.setSpacing(20)
        self.foldersLayout.setContentsMargins(20, 0, 0, 0)

        ################################################################################
        # ScrollArea
        # Place to show all available files from external
        ################################################################################
        self.scrollWidget = QWidget()
        self.scroll = QScrollArea()
        # self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll.setMinimumSize(900, 700)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.scrollWidget)
       
        # Files vertical layout
        self.filesGridLayout = QGridLayout(self.scrollWidget)
        self.filesGridLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.filesGridLayout.setContentsMargins(20, 20, 20, 20)
        self.filesGridLayout.setSpacing(20)

        ################################################################################
        # Buttons
        ################################################################################
        # Cancel button
        self.cancelButton = QPushButton()
        self.cancelButton.setText("Cancel")
        self.cancelButton.setFont(QFont("Ubuntu", 14))
        self.cancelButton.setFixedSize(120, 34)
        self.cancelButton.setEnabled(True)
        self.cancelButton.clicked.connect(lambda x: exit())

        # Restore button
        self.restoreButton = QPushButton()
        self.restoreButton.setText("Restore")
        self.restoreButton.setFont(QFont("Ubuntu", 14))
        self.restoreButton.setFixedSize(120, 34)
        self.restoreButton.setEnabled(False)

        # Up button
        self.upButton = QPushButton()
        self.upButton.setText("ʌ")
        self.upButton.setFont(QFont("Ubuntu", 11))
        self.upButton.setFixedSize(38, 38)
        self.upButton.clicked.connect(self.change_date_up)

        # Down button
        self.downButton = QPushButton()
        self.downButton.setText("v")
        self.downButton.setFont(QFont("Ubuntu", 11))
        self.downButton.setFixedSize(38, 38)
        self.downButton.clicked.connect(self.change_date_down)

        ################################################################################
        # Labels
        ################################################################################
        # Before gray date
        self.beforeGrayDate = QLabel()
        self.beforeGrayDate.setFont(QFont("Ubuntu", 10))
        self.beforeGrayDate.setStyleSheet("""
            background-color: transparent;
            color: gray;
        """)
        
        # After gray date
        self.afterGrayDate = QLabel()
        self.afterGrayDate.setFont(QFont("Ubuntu", 10))
        self.afterGrayDate.setStyleSheet("""
            background-color: transparent;
            color: gray;
        """)

        # Data label
        self.dateLabel = QLabel()
        self.dateLabel.setFont(QFont("Ubuntu", 12))
        self.dateLabel.setStyleSheet("""
            background-color: transparent;
        """)
        
        # Current location
        self.currentLocation = QLabel()
        self.currentLocation.setFont(QFont("Ubuntu", 34))
        self.currentLocation.setStyleSheet("""
                    background-color: transparent;
                """)

        ################################################################################
        # Add widgets and Layouts
        ################################################################################
        self.horizontalLayout.addLayout(self.foldersLayout, 0)
        self.horizontalLayout.addWidget(self.scroll, 1, QtCore.Qt.AlignVCenter)
        self.horizontalLayout.addLayout(self.updownLayoutV, 0)
        self.horizontalLayout.addLayout(self.timeLayoutV, 0)

        self.updownLayoutV.addStretch()
        self.updownLayoutV.addWidget(self.beforeGrayDate, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.updownLayoutV.addWidget(self.upButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.updownLayoutV.addWidget(self.dateLabel, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.updownLayoutV.addWidget(self.downButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.updownLayoutV.addWidget(self.afterGrayDate, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.updownLayoutV.addStretch()

        self.cancelRestoreLayout.addWidget(self.cancelButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.cancelRestoreLayout.addWidget(self.restoreButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

        self.verticalLayout.addWidget(self.currentLocation, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.verticalLayout.addLayout(self.horizontalLayout, 0)
        self.verticalLayout.addLayout(self.cancelRestoreLayout, 0)

        self.setLayout(self.verticalLayout)

        self.get_folders()

    def get_folders(self):
        # Clean screen
        for _ in range(1):
            self.clean_stuff_on_screen("foldersLayout")

        ################################################################################
        # Get available folders from INI file
        ################################################################################
        # TODO
        for output in self.iniFolder:
            # Capitalize first letter
            output = output.capitalize()
            # Can output be found inside Users Home?
            try:
                os.listdir(f"{homeUser}/{output}")
            except:
                # Lower output first letter
                output = output.lower() # Lower output first letter

            ################################################################################
            # Create folders buttons
            ################################################################################
            self.foldersOnScreen = QPushButton()
            self.foldersOnScreen.setText(output)
            self.foldersOnScreen.setFont(QFont("Ubuntu", 12))
            self.foldersOnScreen.setFixedSize(140, 34)
            self.foldersOnScreen.setCheckable(True)
            self.foldersOnScreen.setAutoExclusive(True)
            self.foldersOnScreen.clicked.connect(lambda *args, folder=output: self.change_folder(folder))

            self.foldersLayout.addWidget(self.foldersOnScreen, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        # Can not auto check, because other times it is in the same layout :C
        # Auto check latest folder and time button
        # self.foldersOnScreen.setChecked(True)
        # Add output to self.currentFolder
        self.currentFolder = output

        self.get_date()

    def get_date(self):
        # Clean screen
        for _ in range(1):
            self.clean_stuff_on_screen("filesGridLayout")

        try:
            if not self.alreadyGotDateList:
                for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}"):
                    # Hide hidden outputs
                    if "." not in output:
                        self.dateFolders.append(output)
                        self.dateFolders.sort(reverse=True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))
                        self.alreadyGotDateList = True

        except FileNotFoundError as error:
            # Set notification_id to 2
            with open(src_user_config, 'w') as configfile:
                config.set('INFO', 'notification_id', "2")
                config.set('INFO', 'notification_add_info', f"{error}")
                config.write(configfile)

            print("External not mounted or available...")
            exit()

        print("Date available: ", self.dateFolders)
        print("Current date: ", self.dateFolders[self.countForDate])
        print("")

        # # Update date label
        # self.dateLabel.setText(f"{self.dateFolders[(self.countForDate)]}")
        # # Update before gray date
        # self.beforeGrayDate.setText(f"{self.dateFolders[(self.countForDate) + 1]}")
        # # Update after gray date
        # if self.downButton.isEnabled():
        #     self.afterGrayDate.setText(f"{self.dateFolders[(self.countForDate) - 1]}")
        # else:
        #     self.afterGrayDate.setText(" asd")
            
        self.get_time()

    def get_time(self):
        # Clean screen
        for _ in range(1):
            self.clean_stuff_on_screen("timeLayoutV")

        ################################################################################
        # If inside the external "date folders" has not "time folder", pass to avoid display error :D
        ################################################################################
        try:
            # Clear list
            self.timeFolders.clear()
            for getTime in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/"
                f"{self.dateFolders[(self.countForDate)]}/"):

                self.timeFolders.append(getTime)
                self.timeFolders.sort(reverse=True)

                # Only add time button if self.currentFolder can be found inside current date and time
                if os.path.exists(f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/"
                    f"{self.dateFolders[(self.countForDate)]}/{getTime}/{self.currentFolder}"):

                    ################################################################################
                    # Time button
                    ################################################################################
                    getTime = getTime.replace("-", ":")  # Change - to :
                    self.timeButton = QPushButton()
                    self.timeButton.setText(getTime)
                    getTime = getTime.replace(":", "-")  # Change back : to -
                    self.timeButton.setFont(QFont("Ubuntu", 12))
                    self.timeButton.setFixedSize(100, 34)
                    self.timeButton.setCheckable(True)
                    self.timeButton.setAutoExclusive(True)
                    self.timeButton.clicked.connect(lambda *args, getTime=getTime: self.change_time(getTime))

                    ################################################################################
                    # Set current folder date
                    ################################################################################
                    self.timeLayoutV.addWidget(self.timeButton, 1, QtCore.Qt.AlignRight)

                # self.timeButton.setChecked(True)  # Auto selected that latest one

        except:
            # Reset self.countForDate
            self.countForDate = 0
            # Add to self.countForDate
            self.countForDate += 1
            # Return to Date
            self.get_date()

        try:
            # Current folder that user is on
            print("")
            print("Date available: ", self.dateFolders)
            print("Time available: ", self.timeFolders)
            print("Current date: ", self.dateFolders[self.countForDate])
            print("Current time: ", self.timeFolders[self.countForTime])
            print("Current folder:", self.currentFolder)
            print(f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}"
                    f"/{self.dateFolders[self.countForDate]}/{self.timeFolders[self.countForTime]}/"
                    f"{self.currentFolder}")
        except:
            pass

        self.show_on_screen()

    def show_on_screen(self):
        # Clean screen
        for _ in range(1):
            self.clean_stuff_on_screen("filesGridLayout")

        # Show available files
        try:
            horizontal = 0
            vertical = 0
            imagePrefix = ((".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"))
            for output in os.listdir(f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}"
                f"/{self.dateFolders[self.countForDate]}/{self.timeFolders[self.countForTime]}/{self.currentFolder}"):
                # Only show files and hide hidden outputs
                if not output.startswith(".") and "." in output:
                    print("     Files: ", output)

                    # Buttons for output
                    self.searchResult = QPushButton(self)
                    self.searchResult.setCheckable(True)
                    self.searchResult.setFixedSize(455, 48)

                    # Show bigger preview if mouse hover
                    if output.endswith(imagePrefix):
                        scaledHTML = 'width:"100%" height="250"'
                        self.searchResult.setToolTip(
                            f"<img src={self.iniExternalLocation}/{baseFolderName}/{backupFolderName}"
                            f"/{self.dateFolders[self.countForDate]}/{self.timeFolders[self.countForTime]}/"
                            f"{self.currentFolder}/{output} {scaledHTML}/>")

                    self.searchResult.clicked.connect(
                        lambda *args, output=output: self.add_to_restore(output, self.dateFolders[self.countForDate],
                        self.timeFolders[self.countForTime]))

                    ################################################################################
                    # Preview of files that are not in imagePrefix
                    ################################################################################
                    # Image label
                    image = QLabel(self.searchResult)
                    # image.setMinimumSize(96, 96)
                    image.move(14, 12)
                    image.setStyleSheet(
                        "QLabel"
                        "{"
                        "background-repeat: no-repeat;"
                        "}")

                    if output.endswith(imagePrefix):
                        # image = QLabel(self.searchResult)
                        scaledHTML = 'width:"20%" height="25"'
                        image.setText(
                            f"<img  src={self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/"
                            f"{self.dateFolders[self.countForDate]}/{self.timeFolders[self.countForTime]}/{self.currentFolder}/{output} {scaledHTML}/>")
                        image.setStyleSheet("""
                             background-color: transparent;
                         """)

                    elif output.endswith(".txt"):
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/txt.png);"
                            "background-color: transparent;"
                            "}")

                    elif output.endswith(".pdf"):
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/pdf.png);"
                            "background-color: transparent;"
                            "}")

                    elif output.endswith(".py"):
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/py.png);"
                            "background-color: transparent;"
                            "}")

                    elif output.endswith(".cpp"):
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/c.png);"
                            "background-color: transparent;"
                            "}")

                    elif output.endswith(".sh"):
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/bash.png);"
                            "background-color: transparent;"
                            "}")

                    elif output.endswith(".blend"):
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/blend.png);"
                            "background-color: transparent;"
                            "}")

                    elif output.endswith(".excel"):
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/excel.png);"
                            "background-color: transparent;"
                            "}")

                    elif output.endswith(".mp4"):
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/mp4.png);"
                            "background-color: transparent;"
                            "}")

                    elif output.endswith(".iso"):
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/iso.png);"
                            "background-color: transparent;"
                            "}")

                    # else:
                    #     image.setFixedSize(64, 64)
                    #     image.move(30, 40)
                    #     image.setStyleSheet(
                    #         "QLabel"
                    #         "{"
                    #         f"background-image: url({homeUser}/.local/share/timemachine/src/icons/folder.png);"
                    #         "background-color: transparent;"
                    #         "}")

                    ################################################################################
                    # Text
                    ################################################################################
                    text = QLabel(self.searchResult)
                    text.setText(output.capitalize())
                    text.setFont(QFont("Ubuntu", 11))
                    text.setAlignment(Qt.AlignTop | Qt.AlignLeft)
                    text.move(65, 15)
                    text.setStyleSheet("""
                        background-color: transparent;
                    """)

                    # Add layout and widgets
                    self.filesGridLayout.addWidget(self.searchResult, vertical, horizontal)

                    ################################################################################
                    # Display number of item on the screen
                    ################################################################################
                    # TODO
                    # NO DYNAMIC RESULT!
                    horizontal += 1
                    # Only allow x number of item in the row
                    if horizontal %2 == 0:
                        horizontal = 0
                        vertical += 1
                     
        except FileNotFoundError as error:
            # self.excludeTimeList.append(self.timeFolders[self.countForTime])

            print("")
            print(f"Current info {self.currentFolder}/{self.dateFolders[self.countForDate]}/{self.timeFolders[self.countForTime]}")
            print("Change time...")
            print("INDEX TIME:", self.timeFolders.index(self.timeFolders[self.countForTime]) + 1)
            print("ITEM INSIDE:", len(self.timeFolders))

            # Change time if inside the timeList has more then 1 item
            # and is not at the end of the time list
            if len(self.timeFolders) > 1 and not len(self.timeFolders) == self.timeFolders.index(self.timeFolders[self.countForTime]) + 1:
                # Add to
                self.countForTime += 1
                # Go back to get_time
                self.get_time()

            else:
                print("No more times to change...")
                print("Change dates...")
                self.countForDate += 1
                self.countForTime = 0

                # Go back to get_date
                self.get_date()

        self.up_down()

    def up_down(self):
        try:
            ################################################################################
            # Up settings
            # If clicked on up, go back in time
            ################################################################################
            if self.dateFolders.index(self.dateFolders[self.countForDate]) == 0: # 0 = The latest date available
                self.downButton.setEnabled(False)
            else:
                self.downButton.setEnabled(True)

            ################################################################################
            # Down settings
            # If clicked on down, go forward in time
            ################################################################################
            if self.dateFolders.index(self.dateFolders[self.countForDate]) + 1  == len(self.dateFolders):
                self.upButton.setEnabled(False)

            else:
                self.upButton.setEnabled(True)

        except Exception("error") as error:
            print(error)
            exit()

        self.label_updates()

    def label_updates(self):
        # Update current folder (label)
        self.currentLocation.setText(self.currentFolder)

        # Update date label
        self.dateLabel.setText(f"{self.dateFolders[(self.countForDate)]}")
        # Update before gray date
        if self.upButton.isEnabled():
            self.beforeGrayDate.setText(f"{self.dateFolders[(self.countForDate) + 1]}")
        else:
            self.beforeGrayDate.setText("")

        # Update after gray date
        if self.downButton.isEnabled():
            self.afterGrayDate.setText(f"{self.dateFolders[(self.countForDate) - 1]}")
        else:
            self.afterGrayDate.setText("")

    def add_to_restore(self, output, getDate, getTime):
        ################################################################################
        # Check for spaces inside output and sort them
        ################################################################################
        if not " " in output:
            if not output in self.filesToRestore:  # Check if output is already inside list
                self.filesToRestore.append(output)  # Add output to the list files to restore

            else:
                self.filesToRestore.remove(output)  # Remove item if already in list

        else:
            if not output in self.filesToRestoreWithSpace:  # Check if output is already inside list
                self.filesToRestoreWithSpace.append(output)  # Add output to the list files to restore

            else:
                self.filesToRestoreWithSpace.remove(output)  # Remove item if already in list

        print("")
        print("No spaces list   : ", self.filesToRestore)
        print("with spaces list : ", self.filesToRestoreWithSpace)

        ################################################################################
        # Enable/Disable functions if item(s) is/are selected
        ################################################################################
        if len(self.filesToRestore) or len(self.filesToRestoreWithSpace) >= 1:  # If something inside list
            self.restoreButton.setEnabled(True)

            # Set self.filesToRestore length
            self.restoreButton.setText(f"Restore({len(self.filesToRestore)})")

            # Hide up function if 1 or more items is/are selected
            # Up
            self.upButton.setEnabled(False)

            # Hide down function if 1 or more items is/are selected
            # Down
            self.downButton.setEnabled(False)

            # Hide time functions from TimeVLayout if 1 or more items is/are selected
            for i in range(self.timeLayoutV.count()):
                item = self.timeLayoutV.itemAt(i)
                widget = item.widget()
                widget.setEnabled(False)  # Disable function
                i -= 1

            # Hide folders functions from foldersVLayout if 1 or more items is/are selected
            for i in range(self.foldersLayout.count()):
                item = self.foldersLayout.itemAt(i)
                widget = item.widget()
                widget.setEnabled(False)  # Disable function
                i -= 1

        else:
            self.restoreButton.setEnabled(False)

            # Set self.filesToRestore length
            self.restoreButton.setText("Restore")

            # # Clean screen
            # for _ in range(1):
            #     print("Cleaning")
            #     self.clean_stuff_on_screen("timeLayoutV")

            # # Clean screen
            # for _ in range(1):
            #     print("Cleaning")
            #     self.clean_stuff_on_screen("foldersLayout")

            # Show time functions from TimeVLayout if 1 or more items is/are selected
            for i in range(self.timeLayoutV.count()):
                item = self.timeLayoutV.itemAt(i)
                widget = item.widget()
                widget.setEnabled(True)  # Enable function
                i -= 1

            # Show folders functions from foldersVLayout if 1 or more items is/are selected
            for i in range(self.foldersLayout.count()):
                item = self.foldersLayout.itemAt(i)
                widget = item.widget()
                widget.setEnabled(True)  # Enable function
                i -= 1
            ################################################################################
            # Reactivate buttons
            ################################################################################
            if self.dateIndex != 0:  # If is not last/top date
                self.upButton.setEnabled(True)

            if not (self.dateIndex + 1) == len(self.dateFolders):  # If is not last/bottom date
                self.downButton.setEnabled(True)

        ################################################################################
        # Connection restore button
        ################################################################################
        self.restoreButton.clicked.connect(lambda *args: self.start_restore(getDate, getTime))

    def start_restore(self, getDate, getTime):
        ################################################################################
        # Restore files without spaces
        ################################################################################
        try:
            count = 0
            for _ in self.filesToRestore:
                sub.run(
                    f"{copyRsyncCMD} {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/{getDate}/{getTime}/"
                    f"{self.currentFolder}/{self.filesToRestore[count]} {homeUser}/{self.currentFolder}/ &",
                    shell=True)

                # Add to count
                count += 1

            ################################################################################
            # Restore files with spaces
            ################################################################################
            count = 0
            for _ in self.filesToRestoreWithSpace:
                sub.run(
                    f"{copyRsyncCMD} {self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/{getDate}/{getTime}/"
                    f"{self.currentFolder}/{self.filesToRestoreWithSpace[count]} {homeUser}/"
                    f"{self.currentFolder}/ &", shell=True)

                # Add to count
                count += 1

        except:
            print("Error trying to restore files from external device...")
            ################################################################################
            # Set notification_id to 10
            ################################################################################
            with open(src_user_config, 'w') as configfile:
                config.set('INFO', 'notification_id', "9")
                config.write(configfile)

            sub.Popen(f"python3 {src_notification}", shell=True)  # Call notification
            exit()

        print("Your files are been restored...")
        exit()

    def change_date_up(self):
        try:
            # Clean screen
            for _ in range(1):
                print("Cleaning")
                self.clean_stuff_on_screen("timeLayoutV")
        except:
            pass

        self.countForTime = 0
        self.countForDate += 1
        # Return to get_date
        self.get_date()

    def change_date_down(self):
        try:
            # Clean screen
            for _ in range(1):
                print("Cleaning")
                self.clean_stuff_on_screen("timeLayoutV")
        except:
            pass

        self.countForTime = 0
        self.countForDate -= 1
        # Return to get_date
        self.get_date()

    def change_time(self, getTime):
        try:
            # Clean screen
            for _ in range(1):
                print("Cleaning")
                self.clean_stuff_on_screen("filesGridLayout")
        except:
            pass

        # Index of the getTime
        index = self.timeFolders.index(getTime)
        # Add to
        self.countForTime = index
        # Return to getDate
        self.show_on_screen()

    def change_folder(self, folder):
        # Update self.currentFolder
        self.currentFolder = folder
        # Reset date
        self.countForDate = 0
        # Reset time
        self.countForTime = 0
        # Return to getDate
        self.get_date()

    def clean_stuff_on_screen(self, exec):
        ################################################################################
        # Update screen files by removing items before show the new ones
        ################################################################################
        if exec == "foldersLayout":
            for i in range(self.foldersLayout.count()):
                item = self.foldersLayout.itemAt(i)
                widget = item.widget()
                widget.deleteLater()
                i -= 1

        if exec == "timeLayoutV":
            for i in range(self.timeLayoutV.count()):
                item = self.timeLayoutV.itemAt(i)
                widget = item.widget()
                widget.deleteLater()
                i -= 1

        if exec == "filesGridLayout":
            for i in range(self.filesGridLayout.count()):
                item = self.filesGridLayout.itemAt(i)
                widget = item.widget()
                widget.deleteLater()
                i -= 1


app = QApplication(sys.argv)
main = UI()
main.show()
app.exit(app.exec())
