#! /usr/bin/python3
from setup import *
from check_connection import *
from get_backup_date import get_backup_date
from get_backup_time import get_latest_backup_time
from stylesheet import *
from read_ini_file import UPDATEINIFILE
from PIL import Image

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
        self.current_folder = str()
        
        # Times
        self.timeFolders = []
        self.count_for_time = 0
        self.excludeTimeList = []

        # Dates
        self.date_index = 0
        self.count_for_date = 0
        self.alreadyGotDateList = False

        # xdg-open
        self.folderAlreadyOpened = False

        # Start task
        asyncio.run(self.start())

    def load_ui(self):
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
        self.loadingLabel = QLabel(self.scrollForFiles)
        self.loadingLabel.move(365, 300)
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
        self.upButton.clicked.connect(self.change_date_up)

        # Down button
        self.downButton = QPushButton()
        self.downButton.setText("v")
        self.downButton.setFont(QFont("Ubuntu", 11))
        self.downButton.setFixedSize(38, 38)
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
        self.currentLocation.setText("{self.current_folder}")
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
        self.cancelButton.clicked.connect(lambda x: exit())

        # Restore button
        self.restoreButton = QPushButton()
        self.restoreButton.setText("Restore")
        self.restoreButton.setFont(QFont("Ubuntu", 14))
        self.restoreButton.adjustSize()
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

    def get_selection_folders(self):
        # Clean ui
        self.clean_stuff_on_screen("clean_folders")

        # Get folders and sort them alpha.
        sortedFolderList = []
        for sortedFolder in mainIniFile.ini_folders():
            sortedFolderList.append(sortedFolder)
            sortedFolderList.sort()

        # Add buttons for sorted ini folder
        alreadyAdded = False
        for folder in sortedFolderList:
            # Capitalize first letter
            folder = folder.capitalize()

            # Can folder be found inside Users Home?
            try:
                os.listdir(f"{homeUser}/{folder}")
            except:
                # Lower folder first letter
                folder = folder.lower() 

            # Create folders buttons
            self.foldersOnScreen = QPushButton()
            self.foldersOnScreen.setText(folder)
            self.foldersOnScreen.setFont(QFont("Ubuntu", 12))
            self.foldersOnScreen.setFixedSize(140, 34)
            self.foldersOnScreen.setCheckable(True)
            self.foldersOnScreen.setAutoExclusive(True)
            # self.foldersOnScreen.setIcon(QIcon(f"{homeUser}/.local/share/{appNameClose}/src/icons/folder.png"))
            self.foldersOnScreen.clicked.connect(lambda *args, folder=folder: self.change_folder(folder))
            self.foldersLayout.addWidget(self.foldersOnScreen)

            if not alreadyAdded:
                # Auto check the first folder
                self.foldersOnScreen.setChecked(True)

                # Auto select the first folder
                self.current_folder = folder

                # Already added to True
                alreadyAdded = True 
        
        # Add space
        self.foldersLayout.addStretch()

    def get_date(self):
        # Clean ui
        self.clean_stuff_on_screen("clean_files")

        # Get available dates to choose
        self.get_available_dates_list = get_backup_date()
        
        # Print available dates
        print("Date available: ", self.get_available_dates_list)

        # Current available date
        self.current_available_date = self.get_available_dates_list[self.count_for_date]

        if not self.alreadyGotDateList:
            self.alreadyGotDateList = True
        
    def get_time(self):
        # Clean ui
        self.clean_stuff_on_screen("clean_time")
        
        # Get available times to choose
        self.get_available_times_list = get_latest_backup_time()
        
        # Print available times
        print("Times available: ", self.get_available_times_list)

        try:
            # Create buttons for times
            for count in range(len(self.get_available_times_list)):
                getTime = self.get_available_times_list[count] 

                # Change - to :
                getTime = str(getTime).replace("-", ":")  
                self.timeButton = QPushButton()
                self.timeButton.setText(getTime)

                # Change back : to -
                getTime = getTime.replace(":", "-")  
                self.timeButton.setFont(item)
                self.timeButton.setFixedSize(100, 34)
                self.timeButton.setCheckable(True)
                self.timeButton.setAutoExclusive(True)
                self.timeButton.setStyleSheet(buttonStylesheet)
                self.timeButton.clicked.connect(lambda *args, getTime=getTime: self.change_time(getTime))

                # Add widget
                self.timesLayout.addWidget(self.timeButton, QtCore.Qt.AlignHCenter)
        
        except:
            # Reset count for date
            self.count_for_date = 0

            # + 1 for count for date
            self.count_for_date += 1

            # Go to get_date
            self.get_date()
        
        try:
            # Current folder that user is on
            print("")
            print("Current date: ", get_backup_date()[self.count_for_date])
            print("Current time: ", get_latest_backup_time()[count])
            print("Current folder:", self.current_folder)

        except:
            pass
 
    def show_on_screen(self):
        # Clean ui
        self.clean_stuff_on_screen("clean_files")

        # Show available files
        try:
            filesButtomX = 220
            filesButtomY = 120

            # (FILES) Preview of files that are not in imagePrefix
            count = 0
            horizontal = 0
            vertical = 0
            imagePrefix = (
                ".png", ".jpg", ".jpeg", 
                ".webp", ".gif", ".svg")

            print("Checking inside...")
            print(f"{mainIniFile.backup_folder_name()}/{get_backup_date()[self.count_for_date]}/"
                f"{get_latest_backup_time()[count]}/{self.current_folder}/")
            
            for output in os.listdir(f"{mainIniFile.backup_folder_name()}/{get_backup_date()[self.count_for_date]}/"
                f"{get_latest_backup_time()[count]}/{self.current_folder}/"):
                print(output)
            
                # Only show files and hide hidden outputs
                if not output.startswith("."):
                    print("     Files: ", output)
                    self.filesResult = QPushButton(self)
                    self.filesResult.setCheckable(True)
                    self.filesResult.setFixedSize(filesButtomX, filesButtomY)
                    self.filesResult.setIconSize(QtCore.QSize(64, 64))
                    self.filesResult.clicked.connect(
                            lambda *, output=output: self.add_to_restore(
                                output, get_backup_date()[self.count_for_date],
                                get_latest_backup_time()[self.count_for_time]))

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
                        scaledHTML = 'width:"100%" height="250"'
                        self.filesResult.setToolTip(
                            f"<img src={mainIniFile.backup_folder_name()}/{get_backup_date()[self.count_for_date]}/"
                            f"{get_latest_backup_time()[self.count_for_time]}/{self.current_folder}/{output} {scaledHTML}/>")
                        
                
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

                    # if output.endswith(imagePrefix):
                    #     scaledHTML = 'width:"100%" height="80"'
                        
                    #     image.setText(
                    #         f"<img  src={mainIniFile.backup_folder_name()}/{get_backup_date()[self.count_for_date]}/"
                    #         f"{get_latest_backup_time()[self.count_for_time]}/{self.current_folder}/{output} {scaledHTML}/>")

                    if output.endswith(".txt"):
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
            # print("")
            # print(f"Current info {self.current_folder}/{get_backup_date()[self.count_for_date]}/"
            #     f"{self.timeFolders[self.count_for_time]}")
            # print("Change time...")
            # print("INDEX TIME:", self.timeFolders.index(self.timeFolders[self.count_for_time]) + 1)
            # print("ITEM INSIDE:", len(self.timeFolders))

            # Change time if inside the timeList has more then 1 item
            # and is not at the end of the time list
            if len(self.timeFolders) > 1 and not len(self.timeFolders) == self.timeFolders.index(self.timeFolders[self.count_for_time]) + 1:
                # Add to
                self.count_for_time += 1
                # Go back to get_time
                self.get_time()

            else:
                print("No more times to change...")
                print("Change dates...")
                self.count_for_date += 1
                self.count_for_time = 0
            
        self.up_down()
        
    def up_down(self):
        # Date Index
        self.date_index = get_backup_date().index(get_backup_date()[self.count_for_date])

        ################################################################################
        # Up settings
        # If clicked on up, go back in time
        ################################################################################
        # 0 = The latest date available
        if self.date_index == 0: 
            self.downButton.setEnabled(False)

        else:
            self.downButton.setEnabled(True)

        ################################################################################
        # Down settings
        # If clicked on down, go forward in time
        ################################################################################
        if self.date_index + 1  == len(get_backup_date()):
            self.upButton.setEnabled(False)

        else:
            self.upButton.setEnabled(True)

        self.label_updates()

    def label_updates(self):
        # Update current folder (label)
        self.currentLocation.setText(f"<h1>{self.current_folder}</h1>")

        # Update date label
        self.dateLabel.setText(f"{get_backup_date()[(self.count_for_date)]}")
        # Update before gray date
        if self.upButton.isEnabled():
            self.beforeGrayDate.setText(f"{get_backup_date()[(self.count_for_date) + 1]}")
        else:
            self.beforeGrayDate.setText("")

        # Update after gray date
        if self.downButton.isEnabled():
            self.afterGrayDate.setText(f"{get_backup_date()[(self.count_for_date) - 1]}")
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
            self.restoreButton.setText(f"Restore({len(self.filesToRestore) + len(self.filesToRestoreWithSpace)})")

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
            self.restoreButton.setText("Restore")
            
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
            if self.date_index == 0: 
                self.downButton.setEnabled(False)
            else:
                self.downButton.setEnabled(True)

            ################################################################################
            # Down settings
            # If clicked on down, go forward in time
            ################################################################################
            if self.date_index + 1  == len(get_backup_date()):
                self.upButton.setEnabled(False)

            else:
                self.upButton.setEnabled(True)

        ################################################################################
        # Connection restore button
        ################################################################################
        self.restoreButton.clicked.connect(lambda *args: self.start_restore(getDate, getTime))

    def start_restore(self, getDate, getTime):
        ################################################################################
        # Restore files without spaces
        ################################################################################
        print("Your files are been restored...")
        try:
            count = 0
            for _ in self.filesToRestore:
                sub.run(
                    f"{copyRsyncCMD} {mainIniFile.ini_external_location()}/{baseFolderName}/"
                    f"{backupFolderName}/{getDate}/{getTime}/{self.current_folder}/"
                    f"{self.filesToRestore[count]} {homeUser}/{self.current_folder}/",
                    shell=True)
                
                # Add to count
                count += 1

            ################################################################################
            # Restore files with spaces
            ################################################################################
            count = 0
            for _ in self.filesToRestoreWithSpace:
                sub.run(
                    f"{copyRsyncCMD} {mainIniFile.ini_external_location()}/{baseFolderName}/"
                    f"{backupFolderName}/{getDate}/{getTime}/{self.current_folder}/"
                    f"{self.filesToRestoreWithSpace[count]} {homeUser}/"
                    f"{self.current_folder}/", shell=True)

                # Add to count
                count += 1

        except:
            print("Error trying to restore files from external device...")
            exit()

        """
        After restore is done, open the item restore folder. 
        If is not opened already.
        """        
        if not self.folderAlreadyOpened:
            self.folderAlreadyOpened = True
            # Open folder manager
            print(f"Opening {homeUser}/{self.current_folder}...")
            sub.Popen(f"xdg-open {homeUser}/{self.current_folder}",shell=True)
            exit()

    def change_date_up(self):
        # Clean screen
        self.clean_stuff_on_screen("times")

        self.count_for_time = 0
        self.count_for_date += 1

        # Return to get_date
        self.get_date()
        self.get_time()
        self.show_on_screen()

    def change_date_down(self):
        # Clean screen
        self.clean_stuff_on_screen("times")

        self.count_for_time = 0
        self.count_for_date -= 1
        
        # Return to get_date
        self.get_date()
        self.get_time()
        self.show_on_screen()

    def change_time(self, getTime):
        # Clean screen
        self.clean_stuff_on_screen("clean_files")

        # Index of the getTime
        index = self.timeFolders.index(getTime)
        # Add to
        self.count_for_time = index
        # Return to getDate
        self.show_on_screen()

    def change_folder(self, folder):
        # Update self.current_folder
        self.current_folder = folder

        # Reset date
        self.count_for_date = 0

        # Reset time
        self.count_for_time = 0

        # Clean screen
        self.clean_stuff_on_screen("clean_files")

        # Return to getDate
        self.get_date()
        self.get_time()
        self.show_on_screen()

    def clean_stuff_on_screen(self, exec):
        print("Cleanning...")

        # Update screen files by removing items before show the new ones
        try:
            if exec == "clean_folders":
                for i in range(self.foldersLayout.count()):
                    item = self.foldersLayout.itemAt(i)
                    widget = item.widget()
                    widget.deleteLater()
                    i -= 1

                print("Cleaning folders/files...")

        except Exception as error:
            print(error)
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

                print("Cleaning folders/files...")
                
        except Exception as error:
            print(error)
            pass

        try:
            if exec == "clean_time":
                for i in range(self.timesLayout.count()):
                    item = self.timesLayout.itemAt(i)
                    widget = item.widget()
                    widget.deleteLater()
                    i -= 1
        
                print("Cleaning times...")
        
        except Exception as error:
            print(error)
            pass

    async def start(self):
        # Start process
        print("Loading ui...")
        self.load_ui()

        print("Getting available folders to select...")
        self.get_selection_folders()
        
        print("Checking connection...")
        if is_connected(str(mainIniFile.ini_hd_name())):

            # Create task for get_date
            print("Getting dates...")
            # await asyncio.create_task(self.get_date())
            self.get_date()
            
            # Show available times
            print("Getting time...")
            self.get_time()

            print("Showing results...")
            self.loadingLabel.setVisible(True)

            # Show available files/folders
            self.show_on_screen()
            # asyncio.create_task(self.show_on_screen())

            print("Loading")
            # Set loading label to True
            self.loadingLabel.setVisible(False)

            self.up_down()
            self.label_updates()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    mainIniFile = UPDATEINIFILE()
    main = ENTERTIMEMACHINE()

    main.setWindowTitle(f"Browser {appName} Backups")
    main.setWindowIcon(QIcon(src_backup_icon))
    main.setFixedSize(1280, 720)

    main.show()
    # App loop
    app.exit(app.exec())