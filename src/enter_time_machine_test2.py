#! /usr/bin/python3
from setup import *
from check_connection import is_connected
from get_backup_date import get_backup_date
from get_backup_time import get_latest_backup_time
from stylesheet import *
from read_ini_file import UPDATEINIFILE


class ENTERTIMEMACHINE(QWidget):
    def __init__(self):
        super().__init__()
        # Files to restore list
        self.files_to_restore = []
        # Files to restore with space in it list
        self.files_to_restore_with_space = []

        # Current folder
        self.current_folder = str()
        
        # Time folders list
        self.time_folders_list = []
        # Counter for time folder
        self.counter_for_time = 0

        # Date folder index
        self.date_index = 0
        # Counter for date folder 
        self.count_for_date = 0
        # Alredy got list of dates
        self.already_got_date_list = False

        # xdg-open
        self.folderAlreadyOpened=False

    def widgets(self):
        # Base vertical layout
        baseV=QVBoxLayout()
        baseH=QHBoxLayout()

        ################################################################################
        # Left widget
        ################################################################################
        # Folders widget
        self.widgetLeft=QWidget()
        self.widgetLeft.setFixedWidth(200)

        self.backup_folders_layout=QVBoxLayout(self.widgetLeft)
        self.backup_folders_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.backup_folders_layout.setSpacing(5)
        
        ################################################################################
        # Center widget
        ################################################################################
        # Folders/Files 
        # Scroll
        widgetCenterForFolders=QWidget()
        self.scrollForFolders=QScrollArea()
        self.scrollForFolders.setWidgetResizable(True)
        self.scrollForFolders.setMinimumHeight(180)
        self.scrollForFolders.setWidget(widgetCenterForFolders)

        # Scroll files
        widgetCenterForFiles=QWidget()
        self.scrollForFiles=QScrollArea()
        self.scrollForFiles.setWidgetResizable(True)
        self.scrollForFiles.setWidget(widgetCenterForFiles)
        
        # Show loading label
        # self.loadingLabel = QLabel(self.scrollForFiles)
        # self.loadingLabel.move(365, 300)
        # self.loadingLabel.setText("<h1>Loading...</h1>")
        # self.loadingLabel.setFont(QFont("Ubuntu", 10))

        # Folders Layout
        self.foldersLayoutHorizontal=QHBoxLayout(widgetCenterForFolders)
        self.foldersLayoutHorizontal.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.foldersLayoutHorizontal.setContentsMargins(10, 20, 10, 20)

        # Files Layout
        self.filesLayoutGrid=QGridLayout(widgetCenterForFiles)
        self.filesLayoutGrid.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.filesLayoutGrid.setContentsMargins(10, 20, 10, 20)

        ################################################################################
        # Up/Down widget
        ################################################################################
        widgetUpDown=QWidget()
        widgetUpDown.setFixedWidth(120)

        # UpDown layout
        self.upDownLayout=QVBoxLayout(widgetUpDown)
        self.upDownLayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.upDownLayout.setSpacing(20)
        self.upDownLayout.setContentsMargins(20, 20, 20, 0)

        # Up button
        self.upButton=QPushButton()
        self.upButton.setText("ʌ")
        self.upButton.setFont(QFont("Ubuntu", 11))
        self.upButton.setFixedSize(38, 38)
        self.upButton.clicked.connect(self.change_date_up)

        # Down button
        self.downButton=QPushButton()
        self.downButton.setText("v")
        self.downButton.setFont(QFont("Ubuntu", 11))
        self.downButton.setFixedSize(38, 38)
        self.downButton.clicked.connect(self.change_date_down)

        # Before gray date
        self.beforeGrayDate=QLabel()
        self.beforeGrayDate.setFont(QFont("Ubuntu", 10))
        self.beforeGrayDate.setStyleSheet("""
            background-color: transparent;
            color: gray;
        """)
        
        # After gray date
        self.afterGrayDate=QLabel()
        self.afterGrayDate.setFont(QFont("Ubuntu", 10))
        self.afterGrayDate.setStyleSheet("""
            background-color: transparent;
            color: gray;
        """)

        # Data label
        self.dateLabel=QLabel()
        self.dateLabel.setFont(QFont("Ubuntu", 12))
        self.dateLabel.setStyleSheet("""
            background-color: transparent;
        """)
        
        ################################################################################
        # Right widget
        ################################################################################
        widgetRight=QWidget()
        widgetRight.setFixedWidth(120)

        # Times layout
        self.backup_time_layout=QVBoxLayout(widgetRight)
        self.backup_time_layout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.backup_time_layout.setSpacing(20)
        self.backup_time_layout.setContentsMargins(10, 20, 10, 20)
       
        ################################################################################
        # Current location
        ################################################################################
        self.currentLocation=QLabel()
        self.currentLocation.setFont(QFont("Ubuntu", 14))
        self.currentLocation.setText("{self.current_folder } ")
        self.currentLocation.setStyleSheet("""
                    background-color: transparent;
                """)

        ################################################################################
        # Restore and Cancel buttons
        ################################################################################
        # Cancel and restore layout
        self.restoreLayout=QHBoxLayout()
        self.restoreLayout.setSpacing(20)
        self.restoreLayout.setContentsMargins(10, 10, 10, 10)
        
        # Cancel button
        self.cancelButton=QPushButton()
        self.cancelButton.setText("Cancel")
        self.cancelButton.setFont(QFont("Ubuntu", 14))
        self.cancelButton.setFixedSize(120, 34)
        self.cancelButton.setEnabled(True)
        self.cancelButton.clicked.connect(lambda x: exit())

        # Restore button
        self.restoreButton=QPushButton()
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

    def get_backup_folders(self):
        # List for sorted folders
        sorted_folder_list = []
        # If not already added
        already_auto_checked = False
        
        # Clean ui
        self.clean_stuff_on_screen("clean_folders")

        ###############################################
        # Sort folders 
        ###############################################
        for sorted_folder in MAIN_INI_FILE.ini_folders():
            sorted_folder_list.append(sorted_folder)
            sorted_folder_list.sort()

        ###############################################
        # Add buttons for sorted ini folder
        ###############################################
        for folder in sorted_folder_list:
            # Capitalize first letter
            folder = folder.capitalize()

            # Can folder be found inside Users Home?
            try:
                os.listdir(f"{HOME_USER}/{folder}")
            except:
                # Lower folder first letter
                folder = folder.lower() 

            # Create backup folders 
            self.backup_folders_names = QPushButton()
            self.backup_folders_names.setText(folder)
            self.backup_folders_names.setFont(QFont(MAIN_FONT, BIGGER_FONT_SIZE))
            self.backup_folders_names.setFixedSize(140, 34)
            self.backup_folders_names.setCheckable(True)
            self.backup_folders_names.setAutoExclusive(True)
            # self.backup_folders_names.setIcon(QIcon(f"{homeUser}/.local/share/{APPNAMEClose}/src/icons/folder.png"))
            self.backup_folders_names.clicked.connect(lambda *args, folder = folder: self.change_folder(folder))
            self.backup_folders_layout.addWidget(self.backup_folders_names)

            if not already_auto_checked:
                # Auto check the first folder in sorted list
                self.backup_folders_names.setChecked(True)
                # Auto select the first folder
                self.current_folder = folder
                # Already added to True
                already_auto_checked=True 
        
        # Strecth
        self.backup_folders_layout.addStretch()

    def get_backup_dates(self):
        # Clean ui
        self.clean_stuff_on_screen("clean_files")
        # Get available dates to choose
        self.get_available_dates_list = get_backup_date()
        # Print available dates
        # print("Date available: ", self.get_available_dates_list)
        # Current available date
        self.current_available_date = self.get_available_dates_list[self.count_for_date]

        if not self.already_got_date_list:
            self.already_got_date_list = True
        
    def get_backup_times(self):
        # Clean ui
        self.clean_stuff_on_screen("clean_time")
        # Get available times to choose
        self.get_available_times_list=get_latest_backup_time()
        # Print available times
        # print("Times available: ", self.get_available_times_list)

        # Create buttons for backup time folders
        try:
            for counter in range(len(self.get_available_times_list)):
                backup_time_folders = self.get_available_times_list[counter] 
                
                # Change - to :
                backup_time_folders = str(backup_time_folders).replace("-", ":")  
                available_backup_time_button = QPushButton()
                available_backup_time_button.setText(backup_time_folders)

                # Change back : to -
                backup_time_folders=backup_time_folders.replace(":", "-")  

                available_backup_time_button.setFont(ITEM)
                available_backup_time_button.setFixedSize(100, 34)
                available_backup_time_button.setCheckable(True)
                available_backup_time_button.setAutoExclusive(True)
                available_backup_time_button.setStyleSheet(buttonStylesheet)
                available_backup_time_button.clicked.connect(lambda *args,\
                                                    backup_time_folders = backup_time_folders:\
                                                    self.change_time(backup_time_folders))

                # Add widget
                self.backup_time_layout.addWidget(
                    available_backup_time_button, QtCore.Qt.AlignHCenter)
        
        except:
            # Reset counter for date
            self.count_for_date = 0
            # + 1 for counter for date
            self.count_for_date += 1
            # Go to get_backup_dates
            self.get_backup_dates()
        
    def show_on_screen(self):
        # Clean ui
        self.clean_stuff_on_screen("clean_files")

        # Show available files
        try:
            files_button_size_x = 220
            files_button_size_y = 120

            # (FILES) Preview of files that are not in imagePrefix
            counter = 0
            horizontal = 0
            vertical = 0
            imagePrefix = (
                ".png", ".jpg", ".jpeg", 
                ".webp", ".gif", ".svg")

            print("Checking inside...")
            for output in os.listdir(f"{MAIN_INI_FILE.backup_folder_name()}/{get_backup_date()[self.count_for_date]}/"
                f"{get_latest_backup_time()[counter]}/{self.current_folder } /"):
                print(output)
            
                # Only show files and hide hidden outputs
                if not output.startswith("."):
                    print("     Files: ", output)
                    self.filesResult = QPushButton(self)
                    self.filesResult.setCheckable(True)
                    self.filesResult.setFixedSize(files_button_size_x, files_button_size_y)
                    self.filesResult.setIconSize(QtCore.QSize(64, 64))
                    self.filesResult.clicked.connect(
                            lambda *, output=output: self.add_to_restore(
                                output, get_backup_date()[self.count_for_date],
                                get_latest_backup_time()[self.counter_for_time]))

                    ################################################################################
                    # Text
                    ################################################################################
                    text=QLabel(self.filesResult)

                    # Short strings
                    countStrings=len(output)
                    recentEndswith=output.split(".")[-1]

                    # Label
                    if countStrings < 20:            
                        text.setText(f"{(output.capitalize())}")
                    else:
                        text.setText(f"{(output[:20].capitalize())}...{recentEndswith}")

                    text.setFont(QFont("Ubuntu", 11))
                    text.move(10, files_button_size_y-25)

                    # Show bigger preview if mouse hover
                    if output.endswith(imagePrefix):
                        scaledHTML='width:"100%" height="250"'
                        self.filesResult.setToolTip(
                            f"<img src={MAIN_INI_FILE.backup_folder_name()}/{get_backup_date()[self.count_for_date]}/"
                            f"{get_latest_backup_time()[self.counter_for_time]}/{self.current_folder } /{output} {scaledHTML}/>")
                        
                
                    ################################################################################
                    # Preview of files that are not in imagePrefix
                    ################################################################################
                    # Image label
                    image=QLabel(self.filesResult)
                    image.move(10, 10)
                    image.setStyleSheet(
                        "QLabel"
                        "{"
                        "background-repeat: no-repeat;"
                        "}")

                    # if output.endswith(imagePrefix):
                    #     scaledHTML='width:"100%" height="80"'
                        
                    #     image.setText(
                    #         f"<img  src={MAIN_INI_FILE.backup_folder_name()}/{get_backup_date()[self.count_for_date]}/"
                    #         f"{get_latest_backup_time()[self.counter_for_time]}/{self.current_folder } /{output} {scaledHTML}/>")

                    if output.endswith(".txt"):
                        self.filesResult.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/txt.png"))

                    elif output.endswith(".pdf"):
                        self.filesResult.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/pdf.png"))

                    elif output.endswith(".py"):
                        self.filesResult.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/py.png"))

                    elif output.endswith(".cpp"):
                        self.filesResult.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/cpp.png"))

                    elif output.endswith(".sh"):
                        self.filesResult.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/bash.png"))

                    elif output.endswith(".blend"):
                        self.filesResult.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/blend.png"))

                    elif output.endswith(".excel"):
                        self.filesResult.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/excel.png"))

                    elif output.endswith(".mp4"):
                        self.filesResult.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/mp4.png"))

                    elif output.endswith(".iso"):
                        self.filesResult.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/iso.png"))
                    
                    elif not output.endswith(".")and "." not in output:
                        self.filesResult.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/folder.svg"))

                    else:
                        self.filesResult.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/none.png"))

                    # Only show files and hide hidden outputs
                    if not output.startswith(".") and "." in output:
                        self.filesLayoutGrid.addWidget(self.filesResult, vertical, horizontal)
                    
                    else:
                        # Folders
                        self.foldersLayoutHorizontal.addWidget(self.filesResult)

                    counter += 1
                    # If files_button_size_x if higher than scroll width, go to the next column
                    horizontal += 1
                    if self.scrollForFiles.width() <=800:
                        dimension=3
                    elif self.scrollForFiles.width() <=1440:
                        dimension=6

                    if counter %dimension == 0:
                        # Reset counts
                        counter=0
                        # Reset horizontal
                        horizontal=0
                        # Add 1 to vertical
                        vertical += 1

        except FileNotFoundError as error:
            # Change time if inside the timeList has more then 1 item
            # and is not at the end of the time list
            if len(self.time_folders_list ) > 1 and not len(self.time_folders_list ) == self.time_folders_list . index(self.time_folders_list [ self.counter_for_time]) + 1:
                # Add to
                self.counter_for_time += 1
                # Go back to get_backup_times
                self.get_backup_times()

            else:
                print("No more times to change...")
                print("Change dates...")
                self.count_for_date += 1
                self.counter_for_time=0
            
        self.up_down()
        
    def up_down(self):
        # Date Index
        self.date_index = get_backup_date().index(get_backup_date()[self.count_for_date])

        ################################################################################
        # Up settings
        # If clicked on up, go back in time
        ################################################################################
        # 0=The latest date available
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
        self.currentLocation.setText(f"<h1>{self.current_folder } </h1>")

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
        
    def add_to_restore(self, output, getDate, backup_time_folders):
        if not " " in output:
            if not output in self.files_to_restore:  # Check if output is already inside list
                self.files_to_restore.append(output)  # Add output to the list files to restore

            else:
                self.files_to_restore.remove(output)  # Remove item if already in list

        else:
            if not output in self.files_to_restore_with_space :   # Check if output is already inside list
                self.files_to_restore_with_space . append(output)  # Add output to the list files to restore

            else:
                self.files_to_restore_with_space . remove(output)  # Remove item if already in list

        print("")
        print("No spaces list   : ", self.files_to_restore)
        print("with spaces list : ", self.files_to_restore_with_space ) 

        ################################################################################
        # Enable/Disable functions if item(s) is/are selected
        ################################################################################
        if len(self.files_to_restore) or len(self.files_to_restore_with_space )  >= 1:  # If something inside list
            self.restoreButton.setEnabled(True)
            # Restore label + files_to_restore and self.files_to_restore_with_space   lenght
            self.restoreButton.setText(f"Restore({len(self.files_to_restore) + len(self.files_to_restore_with_space ) })")

            # Hide up function if 1 or more items is/are selected
            # Up
            self.upButton.setEnabled(False)

            # Hide down function if 1 or more items is/are selected
            # Down
            self.downButton.setEnabled(False)

            # Hide time functions from TimeVLayout if 1 or more items is/are selected
            for i in range(self.backup_time_layout.count()):
                item=self.backup_time_layout.itemAt(i)
                widget=item.widget()
                widget.setEnabled(False)  # Disable function
                i -= 1

            try:
                # Hide folders functions from foldersVLayout if 1 or more items is/are selected
                for i in range(self.backup_folders_layout.count()):
                    item=self.backup_folders_layout.itemAt(i)
                    widget=item.widget()
                    widget.setEnabled(False)  # Disable function
                    i -= 1
            except:
                pass

        else:
            # Disable restore button
            self.restoreButton.setEnabled(False)
            # Set self.files_to_restore length
            self.restoreButton.setText("Restore")
            
            # Show time functions from TimeVLayout if 1 or more items is/are selected
            for i in range(self.backup_time_layout.count()):
                item=self.backup_time_layout.itemAt(i)
                widget=item.widget()
                widget.setEnabled(True)
                i -= 1
            
            # Show folders functions from foldersVLayout if 1 or more items is/are selected
            try:
                for i in range(self.backup_folders_layout.count()):
                    item=self.backup_folders_layout.itemAt(i)
                    widget=item.widget()
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
            # 0=The latest date available
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
        self.restoreButton.clicked.connect(lambda *args: self.start_restore(getDate, backup_time_folders))

    def start_restore(self, getDate, backup_time_folders):
        ################################################################################
        # Restore files without spaces
        ################################################################################
        print("Your files are been restored...")
        try:
            counter=0
            for _ in self.files_to_restore:
                sub.run(
                    f"{COPY_RSYNC_CMD} {MAIN_INI_FILE.ini_external_location()}/{BASE_FOLDER_NAME}/"
                    f"{BACKUP_FOLDER_NAME}/{getDate}/{backup_time_folders}/{self.current_folder } /"
                    f"{self.files_to_restore[counter]} {HOME_USER}/{self.current_folder } /",
                    shell=True)
                
                # Add to counter
                counter += 1

            ################################################################################
            # Restore files with spaces
            ################################################################################
            counter=0
            for _ in self.files_to_restore_with_space : 
                sub.run(
                    f"{COPY_RSYNC_CMD} {MAIN_INI_FILE.ini_external_location()}/{BASE_FOLDER_NAME}/"
                    f"{BACKUP_FOLDER_NAME}/{getDate}/{backup_time_folders}/{self.current_folder } /"
                    f"{self.files_to_restore_with_space [ counter]} {HOME_USER}/"
                    f"{self.current_folder } /", shell=True)

                # Add to counter
                counter += 1

        except:
            print("Error trying to restore files from external device...")
            exit()

        """
        After restore is done, open the item restore folder. 
        If is not opened already.
        """        
        if not self.folderAlreadyOpened:
            self.folderAlreadyOpened=True
            # Open folder manager
            print(f"Opening {HOME_USER}/{self.current_folder } ...")
            sub.Popen(f"xdg-open {HOME_USER}/{self.current_folder } ",shell=True)
            exit()

    def change_date_up(self):
        # Clean screen
        self.clean_stuff_on_screen("times")

        self.counter_for_time=0
        self.count_for_date += 1

        # Return to get_backup_dates
        self.get_backup_dates()
        self.get_backup_times()
        self.show_on_screen()

    def change_date_down(self):
        # Clean screen
        self.clean_stuff_on_screen("times")

        self.counter_for_time=0
        self.count_for_date -= 1
        
        # Return to get_backup_dates
        self.get_backup_dates()
        self.get_backup_times()
        self.show_on_screen()

    def change_time(self, backup_time_folders):
        # Clean screen
        self.clean_stuff_on_screen("clean_files")

        # Index of the backup_time_folders
        index=self.time_folders_list . index(backup_time_folders)
        # Add to
        self.counter_for_time=index
        # Return to getDate
        self.show_on_screen()

    def change_folder(self, folder):
        # Update self.current_folder 
        self.current_folder = folder
        # Reset date
        self.count_for_date=0
        # Reset time
        self.counter_for_time=0

        # Clean screen
        self.clean_stuff_on_screen("clean_files")

        # Return to getDate
        self.get_backup_dates()
        self.get_backup_times()
        self.show_on_screen()

    def clean_stuff_on_screen(self, exec):
        print("Cleanning...")

        # Update screen files by removing items before show the new ones
        try:
            if exec == "clean_folders":
                for i in range(self.backup_folders_layout.count()):
                    item=self.backup_folders_layout.itemAt(i)
                    widget=item.widget()
                    widget.deleteLater()
                    i -= 1

                print("Cleaning folders/files...")

        except Exception as error:
            print(error)
            pass

        try:
            if exec == "clean_files":
                for i in range(self.filesLayoutGrid.count()):
                    item=self.filesLayoutGrid.itemAt(i)
                    widget=item.widget()
                    widget.deleteLater()
                    i -= 1
                
                # Clean folders too
                for i in range(self.foldersLayoutHorizontal.count()):
                    item=self.foldersLayoutHorizontal.itemAt(i)
                    widget=item.widget()
                    widget.deleteLater()
                    i -= 1

                print("Cleaning folders/files...")
                
        except Exception as error:
            print(error)
            pass

        try:
            if exec == "clean_time":
                for i in range(self.backup_time_layout.count()):
                    item=self.backup_time_layout.itemAt(i)
                    widget=item.widget()
                    widget.deleteLater()
                    i -= 1
        
                print("Cleaning times...")
        
        except Exception as error:
            print(error)
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    MAIN_INI_FILE = UPDATEINIFILE()
    MAIN = ENTERTIMEMACHINE()

    MAIN.setWindowTitle(f"Browser {APP_NAME} Backups")
    MAIN.setWindowIcon(QIcon(SRC_BACKUP_ICON))
    MAIN.setFixedSize(1280, 720)

    print("Loading ui...")
    MAIN.widgets()

    print("Getting available folders to select...")
    MAIN.get_backup_folders()

    print("Checking connection...")
    if is_connected(MAIN_INI_FILE.ini_hd_name()):
        # Create task for get_backup_dates
        print("Getting dates...")
        MAIN.get_backup_dates()
        
        # Show available times
        print("Getting time...")
        print(" ")
        MAIN.get_backup_times()

        # print("Showing results...")
        # MAIN.loadingLabel.setVisible(True)

        # Show available files/folders
        t_f_f = threading.Thread(target=MAIN.show_on_screen,)
        t_f_f.start()
        # MAIN.show_on_screen()

        # Set loading label to True
        # print("Loading")
        # MAIN.loadingLabel.setVisible(False)

        MAIN.up_down()
        MAIN.label_updates()

    MAIN.show()
    app.exit(app.exec())