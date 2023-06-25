#! /usr/bin/python3
from setup import *
from stylesheet import *
from detect_theme_color import detect_theme_color

config = configparser.ConfigParser()
config.read(src_user_config)


class ENTERTIMEMACHINE(QWidget):
    def __init__(self):
        super().__init__()

        # Variables
        self.filesToRestore = []
        self.filesToRestoreWithSpace = []
        self.extra1 = ""

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

        # xdg-open
        self.folderAlreadyOpened = False

        self.read_ini_file()

    def read_ini_file(self):
        ################################################################################
        # Read ini
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)

        self.iniExternalLocation = config['EXTERNAL']['hd']
        self.iniFolder = config.options('FOLDER')
        
        self.begin_settings()

    def begin_settings(self):
        # Detect dark theme
        if detect_theme_color(app):
            self.buttonStylesheetDetector = buttonStylesheetDark
        else:
            self.buttonStylesheetDetector = buttonStylesheet

        self.widgets()

    def widgets(self):
        # Base vertical layout
        baseV = QVBoxLayout()
        baseH = QHBoxLayout()

        ################################################################################
        # Left widget
        ################################################################################
        # Folders widget
        self.widgetLeft = QWidget()
        self.widgetLeft.setFixedWidth(200)

        self.foldersLayout = QVBoxLayout(self.widgetLeft)
        self.foldersLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.foldersLayout.setSpacing(5)
        
        ################################################################################
        # Center widget
        ################################################################################
        # Folders/Files 
        # Scroll
        widgetCenterForFolders = QWidget()
        self.scrollForFolders = QScrollArea()
        self.scrollForFolders.setWidgetResizable(True)
        self.scrollForFolders.setMinimumHeight(180)
        self.scrollForFolders.setWidget(widgetCenterForFolders)

        # Scroll files
        widgetCenterForFiles = QWidget()
        self.scrollForFiles = QScrollArea()
        self.scrollForFiles.setWidgetResizable(True)
        self.scrollForFiles.setWidget(widgetCenterForFiles)
        
        # Show loading label
        self.loadingLabel = QLabel(self)
        self.loadingLabel.move(0, 0)
        self.loadingLabel.setText("<h1>Loading...</h1>")
        self.loadingLabel.setFont(QFont("Ubuntu", 10))

        # Folders Layout
        self.foldersLayoutHorizontal = QHBoxLayout(widgetCenterForFolders)
        self.foldersLayoutHorizontal.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.foldersLayoutHorizontal.setContentsMargins(10, 20, 10, 20)

        # Files Layout
        self.filesLayoutGrid = QGridLayout(widgetCenterForFiles)
        self.filesLayoutGrid.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.filesLayoutGrid.setContentsMargins(10, 20, 10, 20)

        ################################################################################
        # Up/Down widget
        ################################################################################
        widgetUpDown = QWidget()
        widgetUpDown.setFixedWidth(120)

        # UpDown layout
        self.upDownLayout = QVBoxLayout(widgetUpDown)
        self.upDownLayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.upDownLayout.setSpacing(20)
        self.upDownLayout.setContentsMargins(20, 20, 20, 0)

        # Up button
        self.upButton = QPushButton()
        self.upButton.setText("ʌ")
        self.upButton.setFont(QFont("Ubuntu", 11))
        self.upButton.setFixedSize(38, 38)
        self.upButton.setStyleSheet(self.buttonStylesheetDetector)
        self.upButton.clicked.connect(self.change_date_up)

        # Down button
        self.downButton = QPushButton()
        self.downButton.setText("v")
        self.downButton.setFont(QFont("Ubuntu", 11))
        self.downButton.setFixedSize(38, 38)
        self.downButton.setStyleSheet(self.buttonStylesheetDetector)
        self.downButton.clicked.connect(self.change_date_down)

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
        
        ################################################################################
        # Right widget
        ################################################################################
        widgetRight = QWidget()
        widgetRight.setFixedWidth(120)

        # Times layout
        self.timesLayout = QVBoxLayout(widgetRight)
        self.timesLayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.timesLayout.setSpacing(20)
        self.timesLayout.setContentsMargins(10, 20, 10, 20)
       
        ################################################################################
        # Current location
        ################################################################################
        self.currentLocation = QLabel()
        self.currentLocation.setFont(QFont("Ubuntu", 14))
        self.currentLocation.setText("Pictures")
        self.currentLocation.setStyleSheet("""
                    background-color: transparent;
                """)

        ################################################################################
        # Restore and Cancel buttons
        ################################################################################
        # Cancel and restore layout
        self.restoreLayout = QHBoxLayout()
        self.restoreLayout.setSpacing(20)
        self.restoreLayout.setContentsMargins(10, 10, 10, 10)
        
        # Cancel button
        self.cancelButton = QPushButton()
        self.cancelButton.setText("Cancel")
        self.cancelButton.setFont(QFont("Ubuntu", 14))
        self.cancelButton.setFixedSize(120, 34)
        self.cancelButton.setEnabled(True)
        self.cancelButton.setStyleSheet(self.buttonStylesheetDetector)
        self.cancelButton.clicked.connect(lambda x: exit())

        # Restore button
        self.restoreButton = QPushButton()
        self.restoreButton.setText("   Restore   ")
        self.restoreButton.setFont(QFont("Ubuntu", 14))
        self.restoreButton.adjustSize()
        self.restoreButton.setStyleSheet(self.buttonStylesheetDetector)
        self.restoreButton.setEnabled(False)

        ################################################################################
        # Layouts
        ################################################################################
        baseH.addWidget(self.widgetLeft)
        baseH.addLayout(baseV)
        baseH.addWidget(widgetUpDown)
        baseH.addWidget(widgetRight)

        self.upDownLayout.addStretch()
        self.upDownLayout.addWidget(self.beforeGrayDate, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.upDownLayout.addWidget(self.upButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.upDownLayout.addWidget(self.dateLabel, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.upDownLayout.addWidget(self.downButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.upDownLayout.addWidget(self.afterGrayDate, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.upDownLayout.addStretch()
        
        baseV.addWidget(self.scrollForFolders)
        baseV.addWidget(self.scrollForFiles, 1)
        self.restoreLayout.addWidget(self.restoreButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        baseV.addLayout(self.restoreLayout)
        
        self.setLayout(baseH)

        self.get_folders()
    
    def get_folders(self):
        # Clean screen
        self.clean_stuff_on_screen("clean_folders")
        self.foldersLayout.addStretch()

        ################################################################################
        # GET FOLDERS
        ################################################################################
        # Sort folders alphabetically
        dummyList = []
        for folder in self.iniFolder:
            dummyList.append(folder)
            dummyList.sort()

        # Get available folders from INI file
        alreadyAdded = False
        for output in dummyList:
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
            self.foldersOnScreen.setStyleSheet(self.buttonStylesheetDetector)
            # self.foldersOnScreen.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/folder.png"))
            self.foldersOnScreen.clicked.connect(lambda *args, folder=output: self.change_folder(folder))
            self.foldersLayout.addWidget(self.foldersOnScreen)

            if not alreadyAdded:
                # Auto check the first folder
                self.foldersOnScreen.setChecked(True)
                # Auto select the first folder
                self.currentFolder = output
                alreadyAdded = True 
        
        # Add space
        self.foldersLayout.addStretch()

        self.get_date()

    def get_date(self):
        # Clean screen
        self.clean_stuff_on_screen("clean_files")
        
        try:
            if not self.alreadyGotDateList:
                for output in os.listdir(f"{self.iniExternalLocation}/"
                        f"{baseFolderName}/{backupFolderName}"):
                    # Hide hidden outputs
                    if "." not in output:
                        self.dateFolders.append(output)
                        self.dateFolders.sort(
                            reverse=True, 
                            key=lambda date: datetime.strptime(date, "%d-%m-%y"))
                        self.alreadyGotDateList = True

        except FileNotFoundError as error:
            # # Set notification_massage to 2
            # with open(src_user_config, 'w') as configfile:
            #     config.set('INFO', 'notification_massage', "2")
            #     config.set('INFO', 'notification_add_info', f"{error}")
            #     config.write(configfile)

            print("Backup devices was not found...")
            exit()
        
        # asyncio.run(self.get_time())
        self.get_time()

    def get_time(self):
        # Clean screen
        self.clean_stuff_on_screen("clean_time")

        ################################################################################
        # If inside the external "date folders" has not "time folder", pass to avoid display error :D
        ################################################################################
        try:
            # Clear list
            self.timeFolders.clear()
            for getTime in os.listdir(f"{self.iniExternalLocation}/"
                    f"{baseFolderName}/{backupFolderName}/"
                    f"{self.dateFolders[(self.countForDate)]}/"):

                # Add to list
                self.timeFolders.append(getTime)
                # Sort reverse=True
                self.timeFolders.sort(reverse=True)

                # Only add time button if self.currentFolder can be found inside current date and time
                if os.path.exists(f"{self.iniExternalLocation}/"
                        f"{baseFolderName}/{backupFolderName}/"
                        f"{self.dateFolders[(self.countForDate)]}/"
                        f"{getTime}/{self.currentFolder}"):

                    ################################################################################
                    # Time button
                    ################################################################################
                    # Change - to :
                    getTime = getTime.replace("-", ":")  
                    self.timeButton = QPushButton()
                    self.timeButton.setText(getTime)
                    # Change back : to -
                    getTime = getTime.replace(":", "-")  
                    self.timeButton.setFont(QFont("Ubuntu", 12))
                    self.timeButton.setFixedSize(100, 34)
                    self.timeButton.setCheckable(True)
                    self.timeButton.setAutoExclusive(True)
                    self.timeButton.setStyleSheet(self.buttonStylesheetDetector)
                    self.timeButton.clicked.connect(lambda *args, getTime=getTime: self.change_time(getTime))

                    ################################################################################
                    # Set current folder date
                    ################################################################################
                    self.timesLayout.addWidget(self.timeButton, QtCore.Qt.AlignHCenter)

                self.timeButton.setChecked(True)  # Auto selected that latest one

        except:
            # Reset self.countForDate
            self.countForDate = 0
            # Add to self.countForDate
            self.countForDate += 1
            # Return to Date
            self.get_date()

        # try:
        #     # Current folder that user is on
        #     print("")
        #     print("Date available: ", self.dateFolders)
        #     print("Time available: ", self.timeFolders)
        #     print("Current date: ", self.dateFolders[self.countForDate])
        #     print("Current time: ", self.timeFolders[self.countForTime])
        #     print("Current folder:", self.currentFolder)
        #     print(f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}"
        #             f"/{self.dateFolders[self.countForDate]}/{self.timeFolders[self.countForTime]}/"
        #             f"{self.currentFolder}")
        # except:
        #     pass

        asyncio.run(self.main())       

    async def main(self):
        print("Starting main")
        self.loadingLabel.setVisible(False)
        task = asyncio.create_task(self.show_on_screen())

        print("Task created")
        
        await task
        self.loadingLabel.setVisible(False)

        print("Main finished")

    async def show_on_screen(self):
        # Clean screen
        self.clean_stuff_on_screen("clean_files")

        # Show available files
        try:
            filesButtomX = 220
            filesButtomY = 120

            ################################################################################
            # (FILES) Preview of files that are not in imagePrefix
            ################################################################################
            count = 0
            horizontal = 0
            vertical = 0
            imagePrefix = (
                ".png", ".jpg", ".jpeg", 
                ".webp", ".gif", ".svg")
            
            for output in os.listdir(f"{self.iniExternalLocation}/"
                    f"{baseFolderName}/{backupFolderName}/{self.dateFolders[self.countForDate]}/"
                    f"{self.timeFolders[self.countForTime]}/{self.currentFolder}"):
            
            # for output in os.listdir(f"{self.iniExternalLocation}/"
            #     f"{baseFolderName}/{backupFolderName}/{self.dateFolders[self.countForDate]}/"
            #     f"{self.timeFolders[self.countForTime]}/{self.currentFolder}/{self.extra1}"):
            
                # Only show files and hide hidden outputs
                if not output.startswith("."):
                    print("     Files: ", output)
                    self.filesResult = QPushButton(self)
                    self.filesResult.setCheckable(True)
                    self.filesResult.setFixedSize(filesButtomX, filesButtomY)
                    self.filesResult.setIconSize(QtCore.QSize(64, 64))
                    self.filesResult.setStyleSheet(self.buttonStylesheetDetector)
                    self.filesResult.clicked.connect(
                            lambda *, output=output: self.add_to_restore(
                                output, self.dateFolders[self.countForDate],
                                self.timeFolders[self.countForTime]))

                    ################################################################################
                    # Text
                    ################################################################################
                    text = QLabel(self.filesResult)

                    # Short strings
                    countStrings = len(output)
                    recentEndswith = output.split(".")[-1]

                    # Label
                    if countStrings < 20:            
                        text.setText(f"{(output.capitalize())}")
                    else:
                        text.setText(f"{(output[:20].capitalize())}...{recentEndswith}")

                    text.setFont(QFont("Ubuntu", 11))
                    text.move(10, filesButtomY-25)

                    # Show bigger preview if mouse hover
                    if output.endswith(imagePrefix):
                        scaledHTML = 'width:"5%" height="250"'
                        self.filesResult.setToolTip(
                            f"<img src={self.iniExternalLocation}/{baseFolderName}/{backupFolderName}"
                            f"/{self.dateFolders[self.countForDate]}/{self.timeFolders[self.countForTime]}/"
                            f"{self.currentFolder}/{output} {scaledHTML}/>")

                    ################################################################################
                    # Preview of files that are not in imagePrefix
                    ################################################################################
                    # Image label
                    image = QLabel(self.filesResult)
                    image.move(10, 10)
                    image.setStyleSheet(
                        "QLabel"
                        "{"
                        "background-repeat: no-repeat;"
                        "}")

                    if output.endswith(imagePrefix):
                        image = QImage(f"{self.iniExternalLocation}/{baseFolderName}/{backupFolderName}/"
                            f"{self.dateFolders[self.countForDate]}/{self.timeFolders[self.countForTime]}/"
                            f"{self.currentFolder}/{output}")

                        # Convert the image to a pixmap and use it
                        pixmap = QPixmap.fromImage(image)
                        scaled_pixmap = pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio)
                        # scaled_pixmap = pixmap.scaled(self.filesResult.size(), QtCore.Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        self.filesResult.setIcon(QIcon(scaled_pixmap))
                        # self.filesResult.setIconSize(image.size())

                    elif output.endswith(".txt"):
                        self.filesResult.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/txt.png"))

                    elif output.endswith(".pdf"):
                        self.filesResult.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/pdf.png"))

                    elif output.endswith(".py"):
                        self.filesResult.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/py.png"))

                    elif output.endswith(".cpp"):
                        self.filesResult.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/cpp.png"))

                    elif output.endswith(".sh"):
                        self.filesResult.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/bash.png"))

                    elif output.endswith(".blend"):
                        self.filesResult.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/blend.png"))

                    elif output.endswith(".excel"):
                        self.filesResult.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/excel.png"))

                    elif output.endswith(".mp4"):
                        self.filesResult.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/mp4.png"))

                    elif output.endswith(".iso"):
                        self.filesResult.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/iso.png"))
                    
                    elif not output.endswith(".")and "." not in output:
                        self.filesResult.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/folder.svg"))

                    else:
                        self.filesResult.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/none.png"))

                    # Only show files and hide hidden outputs
                    if not output.startswith(".") and "." in output:
                        self.filesLayoutGrid.addWidget(self.filesResult, vertical, horizontal)
                    
                    else:
                        # Folders
                        print(output)
                        self.foldersLayoutHorizontal.addWidget(self.filesResult)

                    count += 1
                    # If filesButtomX if higher than scroll width, go to the next column
                    horizontal += 1
                    if self.scrollForFiles.width() <=800:
                        dimension = 3
                    elif self.scrollForFiles.width() <=1440:
                        dimension = 6

                    if count %dimension == 0:
                        # Reset counts
                        count = 0
                        # Reset horizontal
                        horizontal = 0
                        # Add 1 to vertical
                        vertical += 1

        except FileNotFoundError as error:
            print("")
            print(f"Current info {self.currentFolder}/{self.dateFolders[self.countForDate]}/"
                f"{self.timeFolders[self.countForTime]}")
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

        self.up_down()

    def up_down(self):
        try:
            # Date Index
            self.dateIndex = self.dateFolders.index(self.dateFolders[self.countForDate])
            ################################################################################
            # Up settings
            # If clicked on up, go back in time
            ################################################################################
            # 0 = The latest date available
            if self.dateIndex == 0: 
                self.downButton.setEnabled(False)
            else:
                self.downButton.setEnabled(True)

            ################################################################################
            # Down settings
            # If clicked on down, go forward in time
            ################################################################################
            if self.dateIndex + 1  == len(self.dateFolders):
                self.upButton.setEnabled(False)

            else:
                self.upButton.setEnabled(True)

        except Exception("error") as error:
            print(error)
            exit()
        
        self.label_updates()

    def label_updates(self):
        # Update current folder (label)
        self.currentLocation.setText(f"<h1>{self.currentFolder}</h1>")

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
            # Restore label + filesToRestore and self.filesToRestoreWithSpace lenght
            self.restoreButton.setText(f"   Restore({len(self.filesToRestore) + len(self.filesToRestoreWithSpace)})   ")

            # Hide up function if 1 or more items is/are selected
            # Up
            self.upButton.setEnabled(False)

            # Hide down function if 1 or more items is/are selected
            # Down
            self.downButton.setEnabled(False)

            # Hide time functions from TimeVLayout if 1 or more items is/are selected
            for i in range(self.timesLayout.count()):
                item = self.timesLayout.itemAt(i)
                widget = item.widget()
                widget.setEnabled(False)  # Disable function
                i -= 1

            try:
                # Hide folders functions from foldersVLayout if 1 or more items is/are selected
                for i in range(self.foldersLayout.count()):
                    item = self.foldersLayout.itemAt(i)
                    widget = item.widget()
                    widget.setEnabled(False)  # Disable function
                    i -= 1
            except:
                pass

        else:
            # Disable restore button
            self.restoreButton.setEnabled(False)
            # Set self.filesToRestore length
            self.restoreButton.setText("   Restore   ")
            
            # Show time functions from TimeVLayout if 1 or more items is/are selected
            for i in range(self.timesLayout.count()):
                item = self.timesLayout.itemAt(i)
                widget = item.widget()
                widget.setEnabled(True)
                i -= 1
            
            # Show folders functions from foldersVLayout if 1 or more items is/are selected
            try:
                for i in range(self.foldersLayout.count()):
                    item = self.foldersLayout.itemAt(i)
                    widget = item.widget()
                    widget.setEnabled(True)  
                    i -= 1
            except:
                pass
            
            ################################################################################
            # Reactivate buttons
            ################################################################################
            ################################################################################
            # Up settings
            # If clicked on up, go back in time
            ################################################################################
            # 0 = The latest date available
            if self.dateIndex == 0: 
                self.downButton.setEnabled(False)
            else:
                self.downButton.setEnabled(True)

            ################################################################################
            # Down settings
            # If clicked on down, go forward in time
            ################################################################################
            if self.dateIndex + 1  == len(self.dateFolders):
                self.upButton.setEnabled(False)

            else:
                self.upButton.setEnabled(True)

        ################################################################################
        # Connection restore button
        ################################################################################
        # self.restoreButton.clicked.connect(lambda *args: self.start_restore(getDate, getTime))
        self.restoreButton.clicked.connect(lambda *args: asyncio.run(self.pre_start_restoring(getDate, getTime)))
        
        asyncio.run(self.main())       

    async def pre_start_restoring(self, getDate, getTime):
        print("Starting main")
        task = asyncio.create_task(self.start_restore(getDate, getTime))

        print("Task created")
        
        await task

        print("Main finished")
        """
        After restore is done, open the item restore folder. 
        If is not opened already.
        """        
        if not self.folderAlreadyOpened:
            self.folderAlreadyOpened = True
            # Open folder manager
            print(f"Opening {homeUser}/{self.currentFolder}...")
            sub.Popen(f"xdg-open {homeUser}/{self.currentFolder}",shell=True)
            exit()

    async def start_restore(self, getDate, getTime):
        ################################################################################
        # Restore files without spaces
        ################################################################################
        print("Your files are been restored...")
        try:
            count = 0
            for _ in self.filesToRestore:
                sub.run(
                    f"{copyRsyncCMD} {self.iniExternalLocation}/{baseFolderName}/"
                    f"{backupFolderName}/{getDate}/{getTime}/{self.currentFolder}/"
                    f"{self.filesToRestore[count]} {homeUser}/{self.currentFolder}/",
                    shell=True)
                
                # Add to count
                count += 1

            ################################################################################
            # Restore files with spaces
            ################################################################################
            count = 0
            for _ in self.filesToRestoreWithSpace:
                sub.run(
                    f"{copyRsyncCMD} {self.iniExternalLocation}/{baseFolderName}/"
                    f"{backupFolderName}/{getDate}/{getTime}/{self.currentFolder}/"
                    f"{self.filesToRestoreWithSpace[count]} {homeUser}/"
                    f"{self.currentFolder}/", shell=True)

                # Add to count
                count += 1

        except:
            print("Error trying to restore files from external device...")
            exit()

    def change_date_up(self):
        # Clean screen
        self.clean_stuff_on_screen("times")

        self.countForTime = 0
        self.countForDate += 1
        # Return to get_date
        self.get_date()

    def change_date_down(self):
        # Clean screen
        self.clean_stuff_on_screen("times")

        self.countForTime = 0
        self.countForDate -= 1
        # Return to get_date
        self.get_date()

    def change_time(self, getTime):
        # Clean screen
        self.clean_stuff_on_screen("clean_files")

        # Index of the getTime
        index = self.timeFolders.index(getTime)
        # Add to
        self.countForTime = index

        asyncio.run(self.main())       

    def change_folder(self, folder):
        self.loadingLabel.setVisible(True)
        print(bool(self.loadingLabel.isVisible()))

        # Update self.currentFolder
        self.currentFolder = folder
        # Reset date
        self.countForDate = 0
        # Reset time
        self.countForTime = 0

        # Clean screen
        self.clean_stuff_on_screen("clean_files")

        # Return to getDate
        self.get_date()

    def clean_stuff_on_screen(self, exec):
        ################################################################################
        # Update screen files by removing items before show the new ones
        ################################################################################
        try:
            if exec == "clean_folders":
                for i in range(self.foldersLayout.count()):
                    item = self.foldersLayout.itemAt(i)
                    widget = item.widget()
                    widget.deleteLater()
                    i -= 1
        except:
            pass

        try:
            if exec == "clean_files":
                for i in range(self.filesLayoutGrid.count()):
                    item = self.filesLayoutGrid.itemAt(i)
                    widget = item.widget()
                    widget.deleteLater()
                    i -= 1
                
                # Clean folders too
                for i in range(self.foldersLayoutHorizontal.count()):
                    item = self.foldersLayoutHorizontal.itemAt(i)
                    widget = item.widget()
                    widget.deleteLater()
                    i -= 1
                
        except:
            pass

        try:
            if exec == "clean_time":
                for i in range(self.timesLayout.count()):
                    item = self.timesLayout.itemAt(i)
                    widget = item.widget()
                    widget.deleteLater()
                    i -= 1
        except:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ENTERTIMEMACHINE()
    
    # Windows settings
    main.setWindowTitle(f"Browser {appName} Backups")
    main.setWindowIcon(QIcon(src_backup_icon))
    main.setMinimumSize(1280, 720)
    main.showMaximized()
    
    main.show()
    app.exit(app.exec())