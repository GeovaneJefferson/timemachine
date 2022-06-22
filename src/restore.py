#! /usr/bin/env python3
from setup import *

config = configparser.ConfigParser()
config.read(src_user_config)


class UI(QWidget):
    def __init__(self):
        super().__init__()
        # Variables
        self.filesToRestore = []
        self.filesToRestoreWithSpace = []
        self.dateIndex = 0
        self.chooseFolder = []

        self.iniUI()

    def iniUI(self):
        ################################################################################
        # Window manager
        ################################################################################
        self.setWindowTitle(f"Enter {appName}")
        app_icon = QIcon(src_restore_icon)
        self.setWindowIcon(app_icon)

        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        # self.showFullScreen()
        self.setMinimumSize(1400, 800)
        # Color settings
        self.setStyleSheet("""
            background-color: rgb(38, 39, 40);
            """)

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
        self.layoutV = QVBoxLayout()
        self.layoutV.setAlignment(QtCore.Qt.AlignVCenter)
        self.layoutV.setContentsMargins(20, 20, 20, 20)

        self.layoutH = QHBoxLayout()
        self.layoutH.setAlignment(QtCore.Qt.AlignHCenter)
        self.layoutH.setSpacing(20)

        self.buttonLayoutH = QHBoxLayout()
        self.buttonLayoutH.setSpacing(20)
        self.buttonLayoutH.setContentsMargins(20, 20, 20, 20)

        self.updownLayoutV = QVBoxLayout()
        self.updownLayoutV.setContentsMargins(0, 0, 0, 0)

        self.timeLayoutV = QVBoxLayout()
        self.timeLayoutV.setAlignment(QtCore.Qt.AlignVCenter)
        self.timeLayoutV.setSpacing(20)
        self.timeLayoutV.setContentsMargins(20, 0, 20, 0)

        self.foldersLayoutV = QVBoxLayout()
        self.foldersLayoutV.setAlignment(QtCore.Qt.AlignVCenter)
        self.foldersLayoutV.setSpacing(20)
        self.foldersLayoutV.setContentsMargins(20, 0, 0, 0)

        ################################################################################
        # Search box
        # Search for files inside Enter Time Machine
        ################################################################################
        # self.searchBox = QLineEdit(self)
        # self.searchBox.move(500, 30)
        # self.searchBox.setMinimumSize(350, 25)
        # self.searchBox.setPlaceholderText("Search for files...")
        # self.searchBox.setStyleSheet(
        # "QLineEdit"
        # "{"
        # "color: white;"
        # "}")

        ################################################################################
        # ScrollArea
        # Place to show all available files from external
        ################################################################################
        self.scrollWidget = QWidget()
        self.scrollWidget.setStyleSheet(
            "QWidget"
            "{"
            "background-color: rgb(24, 25, 26);"
            "border-radius: 5px;"
            "}")

        self.scroll = QScrollArea()
        self.scroll.setFixedSize(900, 600)
        # self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet(
            "QScrollBar::handle"
            "{"
            "background : rgb(58, 59, 60);"
            "}"
            "QScrollBar::handle::pressed"
            "{"
            "background : rgb(68, 69, 70);"
            "}")
        self.scroll.setWidget(self.scrollWidget)

        ################################################################################
        # Files vertical layout
        ################################################################################
        self.filesGridLayout = QGridLayout(self.scrollWidget)
        self.filesGridLayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.filesGridLayout.setContentsMargins(20, 20, 20, 20)
        self.filesGridLayout.setSpacing(20)

        ################################################################################
        # Cancel button
        ################################################################################
        self.cancelButton = QPushButton()
        self.cancelButton.setText("Cancel")
        self.cancelButton.setFont(QFont("DejaVu Sans", 14))
        self.cancelButton.setFixedSize(120, 34)
        self.cancelButton.setEnabled(True)
        self.cancelButton.clicked.connect(lambda x: exit())
        self.cancelButton.setStyleSheet(
            "QPushButton"
            "{"
            "color: white;"
            "background-color: rgb(58, 59, 60);"
            "border: 0px;"
            "border-radius: 5px;"
            "}"
            "QPushButton::hover"
            "{"
            "background-color: rgb(68, 69, 70);"
            "}")

        ################################################################################
        # Restore button
        ################################################################################
        self.restoreButton = QPushButton()
        self.restoreButton.setText("Restore")
        self.restoreButton.setFont(QFont("DejaVu Sans", 14))
        self.restoreButton.setFixedSize(120, 34)
        self.restoreButton.setEnabled(False)
        self.restoreButton.setStyleSheet(
            "QPushButton"
            "{"
            "background-color: rgb(58, 59, 60);"
            "border: 0px;"
            "border-radius: 5px;"

            "}"
            "QPushButton::hover"
            "{"
            "background-color: rgb(68, 69, 70);"
            "}")

        ################################################################################
        # Up button
        ################################################################################
        self.upButton = QPushButton()
        self.upButton.setText("Up")
        self.upButton.setFont(QFont("DejaVu Sans", 11))
        self.upButton.setFixedSize(50, 50)
        self.upButton.clicked.connect(lambda x: self.get_date(True, self.chooseFolder[0]))
        self.upButton.setStyleSheet(
            "QPushButton"
            "{"
            "background-color: rgb(58, 59, 60);"
            "border: 0px;"
            "border-radius: 5px;"
            "}"
            "QPushButton::hover"
            "{"
            "background-color: rgb(68, 69, 70);"
            "}")

        ################################################################################
        # Down button
        ################################################################################
        self.downButton = QPushButton()
        self.downButton.setText("Down")
        self.downButton.setFont(QFont("DejaVu Sans", 11))
        self.downButton.setFixedSize(50, 50)
        self.downButton.clicked.connect(lambda x: self.get_date(False, self.chooseFolder[0]))
        self.downButton.setStyleSheet(
            "QPushButton"
            "{"
            "background-color: rgb(58, 59, 60);"
            "border: 0px;"
            "border-radius: 5px;"
            "}"
            "QPushButton::hover"
            "{"
            "background-color: rgb(68, 69, 70);"
            "}")

        ################################################################################
        # Label date
        ################################################################################
        self.dateLabel = QLabel()
        self.dateLabel.setFont(QFont("DejaVu Sans", 12))
        self.dateLabel.setStyleSheet("""
                    background-color: transparent;
                """)

        ################################################################################
        # Current location
        ################################################################################
        self.currentLocation = QLabel()
        self.currentLocation.setFont(QFont("DejaVu Sans", 34))
        self.currentLocation.setStyleSheet("""
                    background-color: transparent;
                """)

        ################################################################################
        # Add widgets and Layouts
        ################################################################################
        # BaseHLayout
        self.layoutH.addLayout(self.foldersLayoutV, 0)
        self.layoutH.addWidget(self.scroll, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.layoutH.addLayout(self.updownLayoutV, 0)
        self.layoutH.addLayout(self.timeLayoutV, 0)

        # ButtonLayout
        self.updownLayoutV.addStretch()
        self.updownLayoutV.addWidget(self.upButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.updownLayoutV.addWidget(self.dateLabel, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.updownLayoutV.addWidget(self.downButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.updownLayoutV.addStretch()

        # ButtonHLayout
        self.buttonLayoutH.addWidget(self.cancelButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.buttonLayoutH.addWidget(self.restoreButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

        # layoutV
        self.layoutV.addWidget(self.currentLocation, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.layoutV.addStretch()
        self.layoutV.addLayout(self.layoutH, 0)
        self.layoutV.addLayout(self.buttonLayoutH, 0)
        self.layoutV.addStretch()

        self.setLayout(self.layoutV)

        self.get_folders()

    def get_folders(self):
        ################################################################################
        # Update screen files by remover items before show the new ones
        ################################################################################
        for i in range(self.foldersLayoutV.count()):
            item = self.foldersLayoutV.itemAt(i)
            widget = item.widget()
            widget.deleteLater()
            i -= 1

        ################################################################################
        # Get available folders from INI file
        ################################################################################
        for output in self.iniFolder:
            output = output.capitalize()
            ################################################################################
            # Create buttons for it
            ################################################################################
            self.foldersButton = QPushButton()
            self.foldersButton.setText(output)
            self.foldersButton.setFont(QFont("DejaVu Sans", 12))
            self.foldersButton.setFixedSize(140, 34)
            self.foldersButton.setCheckable(True)
            self.foldersButton.setAutoExclusive(True)
            self.foldersButton.clicked.connect(lambda *args, output=output: self.get_date(None, output))
            self.foldersButton.setStyleSheet(
                "QPushButton"
                "{"
                "color: white;"
                "background-color: rgb(58, 59, 60);"
                "border-radius: 5px;"
                "}"
                "QPushButton::hover"
                "{"
                "background-color: rgb(68, 69, 70);"
                "}"
                "QPushButton::checked"
                "{"
                "background-color: rgb(24, 25, 26);"
                "border: 1px solid white;"
                "}")

            # Set current folder date
            self.foldersLayoutV.addWidget(self.foldersButton, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        ################################################################################
        # Auto check latest folder and time button
        ################################################################################
        self.foldersButton.setChecked(True)
        self.foldersButton.setStyleSheet(
            "QPushButton"
            "{"
            "color: white;"
            "background-color: rgb(58, 59, 60);"
            "border: 0px;"
            "border-radius: 5px;"
            "}"
            "QPushButton::hover"
            "{"
            "background-color: rgb(68, 69, 70);"
            "}"
            "QPushButton::checked"
            "{"
            "background-color: rgb(24, 25, 26);"
            "border: 1px solid white;"
            "}")
            
        self.get_date(None, output)

    def get_date(self, dateDirection, getFolder):
        ################################################################################
        # Get available dates inside {folderName}
        ################################################################################
        try:
            self.dateFolders = []
            for output in os.listdir(f"{self.iniExternalLocation}/{folderName}/"):
                if "." not in output:
                    self.dateFolders.append(output)
                    self.dateFolders.sort(reverse=True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))

        except FileNotFoundError:
            ################################################################################
            # Set notification_id to 3
            ################################################################################
            with open(src_user_config, 'w') as configfile:
                config.set('INFO', 'notification_id', "3")
                config.write(configfile)

            print("External not mounted or available...")
            sub.Popen(f"python3 {src_notification}", shell=True)  # Call notification_available_notification()  # Call not available notification
            exit()

        ################################################################################
        # Dates up or down
        ################################################################################
        print("Date available: ", self.dateFolders)
        if dateDirection is None:
            self.dateIndex = 0

        elif not dateDirection:
            self.dateIndex += 1

        else:
            self.dateIndex -= 1

        getDate = self.dateFolders[self.dateIndex]
        ################################################################################
        # Set current folder date
        ################################################################################
        self.dateLabel.setText(getDate)

        self.get_time(getDate, getFolder)

    def get_time(self, getDate, getFolder):
        self.index = self.dateFolders.index(getDate)

        ################################################################################
        # Disable up
        ################################################################################
        if self.index == 0:
            self.upButton.setEnabled(False)
            self.upButton.setStyleSheet(
                "QPushButton"
                "{"
                "color: gray;"
                "background-color: rgb(58, 59, 60);"
                "border: 0px;"
                "border-radius: 5px;"
                "}"
                "QPushButton::hover"
                "{"
                "background-color: rgb(68, 69, 70);"
                "}")

        else:
            self.upButton.setEnabled(True)
            self.upButton.setStyleSheet(
                "QPushButton"
                "{"
                "color: white;"
                "background-color: rgb(58, 59, 60);"
                "border: 0px;"
                "border-radius: 5px;"
                "}"
                "QPushButton::hover"
                "{"
                "background-color: rgb(68, 69, 70);"
                "}")

        ################################################################################
        # Disable down
        ################################################################################
        if (self.index + 1) == len(self.dateFolders):
            self.downButton.setEnabled(False)
            self.downButton.setStyleSheet(
                "QPushButton"
                "{"
                "color: gray;"
                "background-color: rgb(58, 59, 60);"
                "border: 0px;"
                "border-radius: 5px;"
                "}"
                "QPushButton::hover"
                "{"
                "background-color: rgb(68, 69, 70);"
                "}")

        else:
            self.downButton.setEnabled(True)
            self.downButton.setStyleSheet(
                "QPushButton"
                "{"
                "color: white;"
                "background-color: rgb(58, 59, 60);"
                "border: 0px;"
                "border-radius: 5px;"
                "}"
                "QPushButton::hover"
                "{"
                "background-color: rgb(68, 69, 70);"
                "}")

        ################################################################################
        # Remove items
        ################################################################################
        for i in range(self.timeLayoutV.count()):
            item = self.timeLayoutV.itemAt(i)
            widget = item.widget()
            widget.deleteLater()
            i -= 1

        ################################################################################
        # If inside the external "date folders" has not "time folder", pass to avoid display error :D
        ################################################################################
        try:
            ################################################################################
            # Get available times inside {folderName}
            ################################################################################
            timeFolders = []
            for getTime in os.listdir(f"{self.iniExternalLocation}/{folderName}/{getDate}/"):
                timeFolders.append(getTime)
                timeFolders.sort(reverse=True)

                ################################################################################
                # Time button
                ################################################################################
                getTime = getTime.replace("-", ":")  # Change - to :
                self.timeButton = QPushButton()
                self.timeButton.setText(getTime)
                getTime = getTime.replace(":", "-")  # Change back : to -
                self.timeButton.setFont(QFont("DejaVu Sans", 12))
                self.timeButton.setFixedSize(100, 34)
                self.timeButton.setCheckable(True)
                self.timeButton.setAutoExclusive(True)
                self.timeButton.clicked.connect(
                    lambda *args, getTime=getTime: self.show_on_screen(getDate, getTime, getFolder))
                self.timeButton.setStyleSheet(
                    "QPushButton"
                    "{"
                    "color: white;"
                    "background-color: rgb(58, 59, 60);"
                    "border-radius: 5px;"
                    "}"
                    "QPushButton::hover"
                    "{"
                    "background-color: rgb(68, 69, 70);"
                    "}"
                    "QPushButton::checked"
                    "{"
                    "background-color: rgb(24, 25, 26);"
                    "border: 1px solid white;"
                    "}")

                ################################################################################
                # Set current folder date
                ################################################################################
                self.timeLayoutV.addWidget(self.timeButton, 1, QtCore.Qt.AlignRight)

            print("Time available: ", timeFolders)
            self.timeButton.setChecked(True)  # Auto selected that latest one
            self.timeButton.setStyleSheet(
                "QPushButton"
                "{"
                "color: white;"
                "background-color: rgb(58, 59, 60);"
                "border: 0px;"
                "border-radius: 5px;"
                "}"
                "QPushButton::hover"
                "{"
                "background-color: rgb(68, 69, 70);"
                "}"
                "QPushButton::checked"
                "{"
                "background-color: rgb(24, 25, 26);"
                "border: 1px solid white;"
                "}")

        except:
            pass

        self.show_on_screen(getDate, getTime, getFolder)

    def show_on_screen(self, getDate, getTime, getFolder):
        print(f"Choose folder: {getFolder}")
        ################################################################################
        # Only allow one item inside chooseFolder list
        ################################################################################
        self.chooseFolder.append(getFolder)

        if len(self.chooseFolder) > 1:  #
            self.chooseFolder.remove(self.chooseFolder[0])

        ################################################################################
        # Set current location text on screen
        ################################################################################
        try:
            self.currentLocation.setText(getFolder)
        except:
            self.currentLocation.setText("")

        ################################################################################
        # Remove items from files result
        ################################################################################
        for i in range(self.filesGridLayout.count()):
            item = self.filesGridLayout.itemAt(i)
            widget = item.widget()
            widget.deleteLater()
            i -= 1

        ################################################################################
        # Show available files
        ################################################################################
        try:
            horizontal = 0
            vertical = 0
            for output in os.listdir(f"{self.iniExternalLocation}/{folderName}/{getDate}/{getTime}/{getFolder}"):
                if "." in output and not output.startswith("."):
                    print("     Files: ", output)
                    self.buttonFiles = QPushButton(self)
                    self.buttonFiles.setCheckable(True)
                    self.buttonFiles.setFixedSize(415, 150)
                    self.buttonFiles.setStyleSheet(
                        "QPushButton"
                        "{"
                        "background-color: rgb(36, 37, 38);"
                        "border-top: 2px solid rgb(58, 59, 60);"
                        "border-radius: 5px;"
                        "}"
                        "QPushButton::hover"
                        "{"
                        "background-color: rgb(58, 59, 60);"
                        "}"
                        "QPushButton::checked"
                        "{"
                        "background-color: rgb(24, 25, 26);"
                        "border: 1px solid white;"
                        "}")

                    ################################################################################
                    # Preview only if is a image
                    ################################################################################
                    if output.endswith(".png") or output.endswith(".jpg") or output.endswith(
                            ".jpeg") or output.endswith(".webp") or output.endswith(".gif") or output.endswith(".svg"):
                        scaledHTML = 'width:"100%" height="250"'
                        self.buttonFiles.setToolTip(
                            f"<img src={self.iniExternalLocation}/{folderName}/{getDate}/{getTime}/{getFolder}/{output} "
                            f"{scaledHTML}/>")

                    self.buttonFiles.clicked.connect(
                        lambda *args, output=output: self.add_to_restore(output, getDate, getTime))

                    ################################################################################
                    # Set icons inside self.buttonFiles
                    ################################################################################
                    if output.endswith(".png") or output.endswith(".jpg") or output.endswith(
                            ".jpeg") or output.endswith(".webp") or output.endswith(".gif") or output.endswith(".svg"):
                        image = QLabel(self.buttonFiles)
                        scaledHTML = 'width:"100%" height="85"'
                        image.setText(
                            f"<img  src={self.iniExternalLocation}/{folderName}/{getDate}/{getTime}/{getFolder}/{output} "
                            f"{scaledHTML}/>")
                        image.move(20, 20)
                        image.setStyleSheet("""
                             background-color: transparent;
                         """)

                    elif output.endswith(".txt"):
                        image = QLabel(self.buttonFiles)
                        image.setFixedSize(96, 96)
                        image.move(20, 20)
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/txt.png);"
                            "background-color: transparent;"
                            "}")

                    elif output.endswith(".pdf"):
                        image = QLabel(self.buttonFiles)
                        image.setFixedSize(96, 96)
                        image.move(20, 20)
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/pdf.png);"
                            "background-color: transparent;"
                            "}")

                    elif output.endswith(".py"):
                        image = QLabel(self.buttonFiles)
                        image.setFixedSize(96, 96)
                        image.move(20, 20)
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/py.png);"
                            "background-color: transparent;"
                            "}")

                    elif output.endswith(".cpp"):
                        image = QLabel(self.buttonFiles)
                        image.setFixedSize(96, 96)
                        image.move(20, 20)
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/c.png);"
                            "background-color: transparent;"
                            "}")

                    elif output.endswith(".sh"):
                        image = QLabel(self.buttonFiles)
                        image.setFixedSize(96, 96)
                        image.move(20, 20)
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/bash.png);"
                            "background-color: transparent;"
                            "}")

                    elif output.endswith(".blend"):
                        image = QLabel(self.buttonFiles)
                        image.setFixedSize(96, 96)
                        image.move(20, 20)
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/blend.png);"
                            "background-color: transparent;"
                            "}")

                    elif output.endswith(".excel"):
                        image = QLabel(self.buttonFiles)
                        image.setFixedSize(96, 96)
                        image.move(20, 20)
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/excel.png);"
                            "background-color: transparent;"
                            "}")

                    elif output.endswith(".mp4"):
                        image = QLabel(self.buttonFiles)
                        image.setFixedSize(96, 96)
                        image.move(20, 20)
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/mp4.png);"
                            "background-color: transparent;"
                            "}")

                    elif output.endswith(".iso"):
                        image = QLabel(self.buttonFiles)
                        image.setFixedSize(96, 96)
                        image.move(20, 20)
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/iso.png);"
                            "background-color: transparent;"
                            "}")

                    else:
                        image = QLabel(self.buttonFiles)
                        image.setFixedSize(96, 96)
                        image.move(20, 20)
                        image.setStyleSheet(
                            "QLabel"
                            "{"
                            f"background-image: url({homeUser}/.local/share/timemachine/src/icons/none.png);"
                            "background-color: transparent;"
                            "}")

                    ################################################################################
                    # Text
                    ################################################################################
                    text = QLabel(self.buttonFiles)
                    text.setText(output.capitalize())
                    text.setFont(QFont("DejaVu Sans", 9))
                    text.setAlignment(Qt.AlignTop | Qt.AlignLeft)
                    text.move(20, 120)
                    text.setStyleSheet("""
                        color: white;
                        border: 0px;
                        background-color: transparent;
                    """)

                    ################################################################################
                    # Add layout and widgets
                    ################################################################################
                    self.filesGridLayout.addWidget(self.buttonFiles, vertical, horizontal)

                    ################################################################################
                    # Condition
                    ################################################################################
                    horizontal += 1
                    if horizontal == 2:
                        horizontal = 0
                        vertical += 1

        except FileNotFoundError:
            print(f"Source files not found inside {folderName}.")

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
            self.restoreButton.setStyleSheet(
                "QPushButton"
                "{"
                "color: white;"
                "background-color: rgb(58, 59, 60);"
                "border: 0px;"
                "border-radius: 5px;"

                "}"
                "QPushButton::hover"
                "{"
                "background-color: rgb(68, 69, 70);"
                "}")
            
            # Set self.filesToRestore length
            self.restoreButton.setText(f"Restore({len(self.filesToRestore)})")
            
            # Hide up function if 1 or more items is/are selected
            # Up
            self.upButton.setEnabled(False)
            self.upButton.setStyleSheet(
                "QPushButton"
                "{"
                "color: gray;"
                "background-color: rgb(58, 59, 60);"
                "border: 0px;"
                "border-radius: 5px;"

                "}"
                "QPushButton::hover"
                "{"
                "background-color: rgb(68, 69, 70);"
                "}")

            # Hide down function if 1 or more items is/are selected
            # Down
            self.downButton.setEnabled(False)
            self.downButton.setStyleSheet(
                "QPushButton"
                "{"
                "color: gray;"
                "background-color: rgb(58, 59, 60);"
                "border: 0px;"
                "border-radius: 5px;"

                "}"
                "QPushButton::hover"
                "{"
                "background-color: rgb(68, 69, 70);"
                "}")

            # Hide time functions from TimeVLayout if 1 or more items is/are selected
            for i in range(self.timeLayoutV.count()):
                item = self.timeLayoutV.itemAt(i)
                widget = item.widget()
                # widget.hide()   # Hide times
                widget.setEnabled(False)  # Disable function
                i -= 1

            # Hide folders functions from foldersVLayout if 1 or more items is/are selected
            for i in range(self.foldersLayoutV.count()):
                item = self.foldersLayoutV.itemAt(i)
                widget = item.widget()
                # widget.hide()   # Hide times
                widget.setEnabled(False)  # Disable function
                i -= 1

        else:
            self.restoreButton.setEnabled(False)
            self.restoreButton.setStyleSheet(
                "QPushButton"
                "{"
                "color: gray;"
                "background-color: rgb(58, 59, 60);"
                "border: 0px;"
                "border-radius: 5px;"
                "}")
            
            # Set self.filesToRestore length
            self.restoreButton.setText("Restore")

            ################################################################################
            # Show hides times from TimeVLayout
            ################################################################################
            for i in range(self.timeLayoutV.count()):
                item = self.timeLayoutV.itemAt(i)
                widget = item.widget()
                # widget.show()
                widget.setEnabled(True)  # Enable function
                i -= 1

            ################################################################################
            # Show hides times from FoldersVLayout
            ################################################################################
            for i in range(self.foldersLayoutV.count()):
                item = self.foldersLayoutV.itemAt(i)
                widget = item.widget()
                # widget.show()
                widget.setEnabled(True)  # Enable function
                i -= 1

            ################################################################################
            # Reactivate buttons
            ################################################################################
            if self.index != 0:  # If is not last/top date
                self.upButton.setEnabled(True)
                self.upButton.setStyleSheet(
                    "QPushButton"
                    "{"
                    "color: white;"
                    "background-color: rgb(58, 59, 60);"
                    "border: 0px;"
                    "border-radius: 5px;"

                    "}"
                    "QPushButton::hover"
                    "{"
                    "background-color: rgb(68, 69, 70);"
                    "}")

            if not (self.index + 1) == len(self.dateFolders):  # If is not last/bottom date
                self.downButton.setEnabled(True)
                self.downButton.setStyleSheet(
                    "QPushButton"
                    "{"
                    "color: white;"
                    "background-color: rgb(58, 59, 60);"
                    "border: 0px;"
                    "border-radius: 5px;"

                    "}"
                    "QPushButton::hover"
                    "{"
                    "background-color: rgb(68, 69, 70);"
                    "}")

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
                    f"{copyCmd} {self.iniExternalLocation}/{folderName}/{getDate}/{getTime}/{self.chooseFolder[0]}/"
                    f"{self.filesToRestore[count]} {homeUser}/{self.chooseFolder[0]}/ &",
                    shell=True)
                count += 1

            ################################################################################
            # Restore files with spaces
            ################################################################################
            count = 0
            for _ in self.filesToRestoreWithSpace:
                sub.run(
                    f'{copyCmd} {self.iniExternalLocation}/{folderName}/{getDate}/{getTime}/{self.chooseFolder[0]}/"'
                    f'{self.filesToRestoreWithSpace[count]}" {homeUser}/{self.chooseFolder[0]}/ &',
                    shell=True)
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

        ################################################################################
        # Set notification_id to 9
        ################################################################################
        with open(src_user_config, 'w') as configfile:
            config.set('INFO', 'notification_id', "8")
            config.write(configfile)

        print("Your files are been restored...")
        sub.Popen(f"python3 {src_notification}",
                  shell=True)  # Call notification_available_notification()  # Call not available notification
        exit()

    # def keyPressEvent(self, event):
    #     if event.key():  # == Qt.Key_Esc
    #         exit()


app = QApplication(sys.argv)
tic = time.time()
main = UI()
main.show()
toc = time.time()
print(f'{appName} {(toc - tic):.4f} seconds')
app.exit(app.exec())
