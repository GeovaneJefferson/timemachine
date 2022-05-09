from setup import *

config = configparser.ConfigParser()
config.read(src_user_config)


class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Time Machine")
        app_icon = QIcon(src_restore_icon)
        self.setWindowIcon(app_icon)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            background-color: rgb(38, 39, 40);
        """)

        self.showFullScreen()

        ################################################################################
        ## Variables
        ################################################################################
        self.filesToRestore = []
        self.filesToRestoreWithSpace = []
        self.count = 0
        self.countTime = 0
        self.chooseFolder = []

        ################################################################################
        ## Read ini
        ################################################################################
        self.getExternalLocation = config['EXTERNAL']['hd']
        self.getIniFolders = config.options('FOLDER')

        self.widgets()

    def widgets(self):
        ################################################################################
        ## Base layouts
        ################################################################################
        self.baseVLayout = QVBoxLayout()
        self.baseVLayout.setAlignment(QtCore.Qt.AlignVCenter)
        self.baseVLayout.setContentsMargins(20, 20, 20, 20)

        self.baseHLayout = QHBoxLayout()
        self.baseHLayout.setAlignment(QtCore.Qt.AlignHCenter)
        self.baseHLayout.setSpacing(20)

        self.buttonHLayout = QHBoxLayout()
        self.buttonHLayout.setSpacing(20)
        self.buttonHLayout.setContentsMargins(20, 20, 20, 20)

        self.updownVLayout = QVBoxLayout()
        self.updownVLayout.setContentsMargins(0, 0, 0, 0)

        self.timeVLayout = QVBoxLayout()
        self.timeVLayout.setAlignment(QtCore.Qt.AlignVCenter)
        self.timeVLayout.setSpacing(20)
        self.timeVLayout.setContentsMargins(20, 0, 20, 0)

        self.foldersVLayout = QVBoxLayout()
        self.foldersVLayout.setAlignment(QtCore.Qt.AlignVCenter)
        self.foldersVLayout.setSpacing(20)
        self.foldersVLayout.setContentsMargins(20, 0, 0, 0)

        ################################################################################
        ## ScrollArea
        ################################################################################
        scrollWidget = QWidget()
        scrollWidget.setStyleSheet(
            "QWidget"
            "{"
            "background-color: rgb(24, 25, 26);"
            "border-radius: 5px;"
            "}")

        scroll = QScrollArea()
        scroll.setFixedSize(900, 600)
        # scroll.setVerticalicalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            "QScrollBar::handle"
            "{"
            "background : rgb(58, 59, 60);"
            "}"
            "QScrollBar::handle::pressed"
            "{"
            "background : rgb(68, 69, 70);"
            "}")
        scroll.setWidget(scrollWidget)

        ################################################################################
        ## Files verticalical layout
        ################################################################################
        self.filesGridLayout = QGridLayout(scrollWidget)
        self.filesGridLayout.setAlignment(QtCore.Qt.AlignHCenter)
        self.filesGridLayout.setContentsMargins(20, 20, 20, 20)
        self.filesGridLayout.setSpacing(20)

        ################################################################################
        ## Cancel button
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
        ## Restore button
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
        ## Up button
        ################################################################################
        self.upButton = QPushButton()
        self.upButton.setText("Up")
        self.upButton.setFont(QFont("DejaVu Sans", 11))
        self.upButton.setFixedSize(50, 50)
        self.upButton.clicked.connect(lambda x: self.get_date(True))
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
        ## Down button
        ################################################################################
        self.downButton = QPushButton()
        self.downButton.setText("Down")
        self.downButton.setFont(QFont("DejaVu Sans", 11))
        self.downButton.setFixedSize(50, 50)
        self.downButton.clicked.connect(lambda x: self.get_date(False))
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
        ## Label date
        ################################################################################
        self.labelDate = QLabel()
        self.labelDate.setFont(QFont("DejaVu Sans", 12))
        self.labelDate.setStyleSheet("""
            background-color: transparent;
        """)

        ################################################################################
        ## Current lcoation
        ################################################################################
        self.currentLocation = QLabel()
        self.currentLocation.setFont(QFont("DejaVu Sans", 34))
        self.currentLocation.setStyleSheet("""
            background-color: transparent;
        """)

        ################################################################################
        ## Add widgets and Layouts
        ################################################################################
        # Empty space
        widget = QWidget()
        widget.setFixedSize(425, 425)
        widget.setStyleSheet("""
            background-color: transparent;
        """)

        # BaseHLayout
        self.baseHLayout.addLayout(self.foldersVLayout, 0)
        # self.baseHLayout.addWidget(widget)
        self.baseHLayout.addWidget(scroll, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.baseHLayout.addLayout(self.updownVLayout, 0)
        self.baseHLayout.addLayout(self.timeVLayout, 0)

        # ButtonLayout
        self.updownVLayout.addStretch()
        self.updownVLayout.addWidget(self.upButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.updownVLayout.addWidget(self.labelDate, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.updownVLayout.addWidget(self.downButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.updownVLayout.addStretch()

        # ButtonHLayout
        self.buttonHLayout.addWidget(self.cancelButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.buttonHLayout.addWidget(self.restoreButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

        # BaseVLayout
        self.baseVLayout.addWidget(self.currentLocation, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.baseVLayout.addStretch()
        self.baseVLayout.addLayout(self.baseHLayout, 0)
        self.baseVLayout.addLayout(self.buttonHLayout, 0)
        self.baseVLayout.addStretch()

        self.setLayout(self.baseVLayout)

        self.get_folders()

    def get_folders(self):
        ################################################################################
        ## Remove items from files result
        ################################################################################
        for i in range(self.foldersVLayout.count()):
            item = self.foldersVLayout.itemAt(i)
            widget = item.widget()
            widget.deleteLater()
            i -= 1

        ################################################################################
        ## Get available folders from INI file
        ################################################################################
        for output in self.getIniFolders:
            output = output.capitalize()
            ################################################################################
            ## Create buttons for it
            ################################################################################
            self.foldersButton = QPushButton()
            self.foldersButton.setText(output.capitalize())
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

            ################################################################################
            ## Set current folder date
            ################################################################################
            self.foldersVLayout.addWidget(self.foldersButton, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        ################################################################################
        ## Auto check latest folder and time button
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

    def get_date(self, direction, getFolder):
        ################################################################################
        ## Get available dates inside {folderName}
        ################################################################################
        try:
            self.dateFolders = []
            for output in os.listdir(f"{self.getExternalLocation}/{folderName}/"):
                if not "." in output:
                    self.dateFolders.append(output)
                    self.dateFolders.sort(reverse=True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))

        except FileNotFoundError:
            print("External not detected.")
            not_available_notification()
            exit()

        ################################################################################
        ## Dates up or down
        ################################################################################
        print("Date available: ", self.dateFolders)
        if direction == None:
            self.count = 0

        elif not direction:
            self.count += 1

        else:
            self.count -= 1

        getDate = self.dateFolders[self.count]
        ################################################################################
        ## Set current folder date
        ################################################################################
        self.labelDate.setText(getDate)

        self.get_time(getDate, getFolder)

    def get_time(self, getDate, getFolder):
        self.index = self.dateFolders.index(getDate)

        ################################################################################
        ## Disable up
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
        ## Disable down
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
        ## Remove items
        ################################################################################
        for i in range(self.timeVLayout.count()):
            item = self.timeVLayout.itemAt(i)
            widget = item.widget()
            widget.deleteLater()
            i -= 1

        ################################################################################
        ## Get available times inside {folderName}
        ################################################################################
        timeFolders = []
        for getTime in os.listdir(f"{self.getExternalLocation}/{folderName}/{getDate}/"):
            timeFolders.append(getTime)

            ################################################################################
            ## Time button
            ################################################################################
            getTime = getTime.replace("-", ":")  # Change - to :
            self.timeButton = QPushButton()
            self.timeButton.setText(getTime)
            getTime = getTime.replace(":", "-")  # Change back : to -
            self.timeButton.setFont(QFont("DejaVu Sans", 12))
            self.timeButton.setFixedSize(100, 34)
            self.timeButton.setCheckable(True)
            self.timeButton.setAutoExclusive(True)
            self.timeButton.clicked.connect(lambda *args, getTime=getTime: self.show_on_screen(getDate, getTime))
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

            # self.countTime += 1

            ################################################################################
            ## Set current folder date
            ################################################################################
            self.timeVLayout.addWidget(self.timeButton, 1, QtCore.Qt.AlignRight)

        print("Time available: ", timeFolders)
        self.timeButton.setChecked(True)  # Auto selected that lastest one
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

        # self.timeButton.setChecked(True)  # Auto selected that lastest one
        # self.timeButton.setStyleSheet(
        #     "QPushButton"
        #     "{"
        #     "color: white;"
        #     "background-color: rgb(58, 59, 60);"
        #     "border: 0px;"
        #     "border-radius: 5px;"
        #     "}"
        #     "QPushButton::hover"
        #     "{"
        #     "background-color: rgb(68, 69, 70);"
        #     "}"
        #     "QPushButton::checked"
        #     "{"
        #     "background-color: rgb(24, 25, 26);"
        #     "border: 1px solid white;"
        #     "}")

        self.show_on_screen(getDate, getTime, getFolder)

    def show_on_screen(self, getDate, getTime, getFolder):
        print(getFolder)
        ################################################################################
        ## Only allow one item inside chooseFolder list
        ################################################################################
        # TODO
        if len(self.chooseFolder) > 1:
            self.chooseFolder.clear()

        self.chooseFolder.append(getFolder)

        print(len(self.chooseFolder))
        print(self.chooseFolder)
        if len(self.chooseFolder) > 1:
            index = self.chooseFolder.index(getFolder)
            self.chooseFolder.remove(self.chooseFolder[index])

        ################################################################################
        ## Set current location text on screen
        ################################################################################
        try:
            self.currentLocation.setText(getFolder)
        except:
            self.currentLocation.setText("")

        ################################################################################
        ## Remove items from files result
        ################################################################################
        for i in range(self.filesGridLayout.count()):
            item = self.filesGridLayout.itemAt(i)
            widget = item.widget()
            widget.deleteLater()
            i -= 1

        ################################################################################
        ## Show available files
        ################################################################################
        try:
            horizontal = 0
            vertical = 0
            for output in os.listdir(f"{self.getExternalLocation}/{folderName}/{getDate}/{getTime}/{getFolder}"):
                if "." in output and not output.startswith("."):
                    print("Files: ", output)

                    self.buttonFiles = QPushButton(self)
                    self.buttonFiles.setCheckable(True)
                    self.buttonFiles.setFixedSize(150, 150)
                    scaledHTML = 'width:"100%" height="250"'
                    self.buttonFiles.setToolTip(
                        f"<img src={self.getExternalLocation}/{folderName}/{getDate}/{getTime}/{getFolder}/{output} {scaledHTML}/>")
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
                    self.buttonFiles.clicked.connect(lambda *args, output=output: self.add_to_restore(output, getDate, getTime))

                    ################################################################################
                    ## Preview
                    ################################################################################
                    # image = QLabel(self.buttonFiles)
                    # pixmap = QPixmap(f"{self.getExternalLocation}/{folderName}/{getDate}/{getTime}/{self.requested}/{output}")
                    # pixmap = pixmap.scaled(128, 128, QtCore.Qt.KeepAspectRatio)
                    # image.setPixmap(pixmap)

                    ################################################################################
                    ## Set icons
                    ################################################################################
                    if output.endswith(".png") or output.endswith(".jpg") or output.endswith(
                            ".jpeg") or output.endswith(".webp") or output.endswith(".gif") or output.endswith(".svg"):
                        image = QLabel(self.buttonFiles)
                        scaledHTML = 'width:"100%" height="60"'
                        image.setText(
                            f"<img  src={self.getExternalLocation}/{folderName}/{getDate}/{getTime}/{getFolder}/{output} {scaledHTML}/>")
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
                            f"background-image: url({home_user}/.local/share/timemachine/src/icons/txt.png);"
                            "background-color: transparent;"
                        "}")

                    elif output.endswith(".pdf"):
                        image = QLabel(self.buttonFiles)
                        image.setFixedSize(96, 96)
                        image.move(20, 20)
                        image.setStyleSheet(
                        "QLabel"
                        "{"
                            f"background-image: url({home_user}/.local/share/timemachine/src/icons/pdf.png);"
                            "background-color: transparent;"
                        "}")

                    elif output.endswith(".py"):
                        image = QLabel(self.buttonFiles)
                        image.setFixedSize(96, 96)
                        image.move(20, 20)
                        image.setStyleSheet(
                        "QLabel"
                        "{"
                            f"background-image: url({home_user}/.local/share/timemachine/src/icons/py.png);"
                            "background-color: transparent;"
                        "}")

                    elif output.endswith(".cpp"):
                        image = QLabel(self.buttonFiles)
                        image.setFixedSize(96, 96)
                        image.move(20, 20)
                        image.setStyleSheet(
                        "QLabel"
                        "{"
                            f"background-image: url({home_user}/.local/share/timemachine/src/icons/c.png);"
                            "background-color: transparent;"
                        "}")

                    elif output.endswith(".sh"):
                        image = QLabel(self.buttonFiles)
                        image.setFixedSize(96, 96)
                        image.move(20, 20)
                        image.setStyleSheet(
                        "QLabel"
                        "{"
                            f"background-image: url({home_user}/.local/share/timemachine/src/icons/bash.png);"
                            "background-color: transparent;"
                        "}")

                    elif output.endswith(".blend"):
                        image = QLabel(self.buttonFiles)
                        image.setFixedSize(96, 96)
                        image.move(20, 20)
                        image.setStyleSheet(
                        "QLabel"
                        "{"
                            f"background-image: url({home_user}/.local/share/timemachine/src/icons/blend.png);"
                            "background-color: transparent;"
                        "}")

                    elif output.endswith(".excel"):
                        image = QLabel(self.buttonFiles)
                        image.setFixedSize(96, 96)
                        image.move(20, 20)
                        image.setStyleSheet(
                        "QLabel"
                        "{"
                            f"background-image: url({home_user}/.local/share/timemachine/src/icons/excel.png);"
                            "background-color: transparent;"
                        "}")

                    elif output.endswith(".mp4"):
                        image = QLabel(self.buttonFiles)
                        image.setFixedSize(96, 96)
                        image.move(20, 20)
                        image.setStyleSheet(
                        "QLabel"
                        "{"
                            f"background-image: url({home_user}/.local/share/timemachine/src/icons/mp4.png);"
                            "background-color: transparent;"
                        "}")
                         
                    else:
                        image = QLabel(self.buttonFiles)
                        image.setFixedSize(96, 96)
                        image.move(20, 20)
                        image.setStyleSheet(
                        "QLabel"
                        "{"
                            f"background-image: url({home_user}/.local/share/timemachine/src/icons/none.png);"
                            "background-color: transparent;"
                        "}")

                    ################################################################################
                    ## Text
                    ################################################################################
                    text = QLabel(self.buttonFiles)
                    text.setText(output.capitalize())
                    text.setFont(QFont("DejaVu Sans", 9))
                    text.move(20, 120)
                    text.setStyleSheet("""
                        color: white;
                        border: 0px;
                        background-color: transparent;
                    """)

                    ################################################################################
                    ## Add layout and widgets
                    ################################################################################
                    self.filesGridLayout.addWidget(self.buttonFiles, vertical, horizontal)

                    ################################################################################
                    ## Condition
                    ################################################################################
                    horizontal += 1
                    if horizontal == 5:
                        horizontal = 0
                        vertical += 1

        except FileNotFoundError:
            print(f"Source files not found inside {folderName}.")

    def add_to_restore(self, output, getDate, getTime):
        ################################################################################
        ## Check for spaces inside output and sort them
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
        ## Enable/Disable buttons
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

            for i in range(self.timeVLayout.count()):  # Hide times
                item = self.timeVLayout.itemAt(i)
                widget = item.widget()
                widget.hide()
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

            ################################################################################
            ## Show hides times
            ################################################################################
            for i in range(self.timeVLayout.count()):
                item = self.timeVLayout.itemAt(i)
                widget = item.widget()
                widget.show()
                i -= 1

            ################################################################################
            ## Reactivate buttons
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
        ## Connection restore button
        ################################################################################
        self.restoreButton.clicked.connect(lambda x: self.start_restore(getDate, getTime))

    def start_restore(self, getDate, getTime):
        # config = configparser.ConfigParser()
        # config.read(src_user_config)
        ################################################################################
        ## Restore files without spaces
        ################################################################################
        try:
            count = 0
            for _ in self.filesToRestore:
                sub.run(
                    f"{copyCmd} {self.getExternalLocation}/{folderName}/{getDate}/{getTime}/{self.requested}/{self.filesToRestore[count]} {home_user}/{self.requested}/ &",
                    shell=True)
                count += 1

            ################################################################################
            ## Restore files with spaces
            ################################################################################
            count = 0
            for _ in self.filesToRestoreWithSpace:
                sub.run(
                    f'{copyCmd} {self.getExternalLocation}/{folderName}/{getDate}/{getTime}/{self.requested}/"{self.filesToRestoreWithSpace[count]}" {home_user}/{self.requested}/ &',
                    shell=True)
                count += 1

        except:
            failed_restore()  # Notification
            exit()

        been_restored()  # Notification
        exit()

    def keyPressEvent(self, event):
        if event.key():  # == Qt.Key_Esc
            exit()


app = QApplication(sys.argv)
tic = time.time()
main = UI()
main.show()
toc = time.time()
print(f'{app_name} {(toc - tic):.4f} seconds')
app.exit(app.exec())
