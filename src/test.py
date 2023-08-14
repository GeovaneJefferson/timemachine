# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
from ui_form import Ui_MainWindow
from setup import *
from read_ini_file import UPDATEINIFILE
from datetime import datetime

MAIN_INI_FILE  = UPDATEINIFILE()

LIST_TO_RESTORE = []
FILES_TO_RESTORE = []
FILES_TO_RESTORE_WITH_SPACES = []

IMAGE_PREFIX = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg")

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ALREADY_CHECKED_FIRST_FOLDER = False
        self.ALREADY_OPENED_FILE_MANAGER = False
        
        self.INDEX_TIME = 0
        
        self.COUNTER_FOR_DATE = 0
        self.COUNTER_FOR_TIME = 0

        self.CURRENT_FOLDER = ""

        self.LIST_FOR_DATE_FOLDERS = []
        self.LIST_FOR_TIME_FOLDERS = []

        self.currentLocationLabel = QLabel(self)

        # Connections
        # Up button
        self.ui.btn_up.clicked.connect(self.btn_up_clicked)
        # Down button
        self.ui.btn_down.clicked.connect(self.btn_down_clicked)

        self.list_of_backup_folders()

    def list_of_backup_folders(self):
        FOLDERS_LIST = []

        # Connect to the SQLite database
        conn = sqlite3.connect(SRC_USER_CONFIG_DB)
        cursor = conn.cursor()

        # Query all keys from the specified table
        cursor.execute(f"SELECT key FROM FOLDER")
        keys = [row[0] for row in cursor.fetchall()]

        # Close the connection
        conn.close()

        for folder in keys:
            FOLDERS_LIST.append(folder)
            FOLDERS_LIST.sort()

        return FOLDERS_LIST

    def create_backup_home_folders_buttons(self):        
        # Get available folders from INI file
        for folder in self.list_of_backup_folders():
            try:
                # Can folder be found inside Users Home?
                folder = folder.capitalize()
                os.listdir(f"{HOME_USER}/{folder}")
            except:
                # Lower folder first letter
                folder = folder.lower() # Lower folder first letter

            ################################################################################
            # PUSH BUTTON
            ################################################################################
            self.btn_backup_home_folders = QPushButton()
            self.btn_backup_home_folders.setText(folder)
            self.btn_backup_home_folders.setFixedSize(140, 34)
            # self.btn_backup_home_folders.setCheckable(True)
            # self.btn_backup_home_folders.setAutoExclusive(True)
            self.btn_backup_home_folders.setStyleSheet(
                """
                    QPushButton 
                    {
                        color: black;
                        background: rgba(255, 255, 255, 0.7);
                        border: 1px solid rgba(0, 0, 0, 0.073);
                        border-bottom: 1px solid rgba(0, 0, 0, 0.183);
                        border-radius: 5px;
                        padding: 5px 12px 6px 12px;
                        outline: none;
                        font-size: 12px;
                    }
                    
                    QPushButton:hover 
                    {
                        font-size: 12px;
                        font-weight: bold;
                    }

                    QPushButton:checked
                    {
                        font-size: 12px;
                        color: rgba(0, 0, 0, 0.63);
                        background: rgba(249, 249, 249, 0.3);
                        border-bottom: 1px solid rgba(0, 0, 0, 0.073);
                    }
                """)

            self.btn_backup_home_folders.clicked.connect(lambda *args, dir = folder: self.change_dir(dir))
            self.ui.folders_layout.addWidget(self.btn_backup_home_folders)

            # Auto check the first folder in the list
            if not self.ALREADY_CHECKED_FIRST_FOLDER:
                self.btn_backup_home_folders.setChecked(True)
                # Set as current selected folder
                self.CURRENT_FOLDER = folder
                # Set already checked to True
                self.ALREADY_CHECKED_FIRST_FOLDER = True 

        self.list_of_backup_dates()

    def list_of_backup_dates(self):
        ALREADY_GOT_LIST_OF_DATES = []
        
        counter = 0
        if not ALREADY_GOT_LIST_OF_DATES:
            for date_folder_to_be_sort in os.listdir(
                    f"{MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}"):
                
                # Hide hidden date_folder_to_be_sort
                if "." not in date_folder_to_be_sort:
                    ALREADY_GOT_LIST_OF_DATES = True

                    self.LIST_FOR_DATE_FOLDERS.append(date_folder_to_be_sort)
                    self.LIST_FOR_DATE_FOLDERS.sort(
                        reverse = False, 
                        key = lambda date_folder_to_be_sort:\
                            datetime.strptime(date_folder_to_be_sort, "%d-%m-%y")
                    )

                # Limit number of dates button on screen
                counter += 1
                if counter == 20:
                    break

        return self.LIST_FOR_DATE_FOLDERS
    
    def create_backup_dates_buttons(self):
        # Show sorted dates folders 
        for date in self.LIST_FOR_DATE_FOLDERS:
            ################################################################################
            # PUSH BUTTON
            ################################################################################
            self.btn_backup_date_folders = QPushButton()
            
            # Convert date from 00-00-00 to Xxxxx 00, 000
            date_obj = datetime.strptime(date, "%d-%m-%y")
            formatted_date = date_obj.strftime("%B %d, %Y")
            
            # Set text to button
            self.btn_backup_date_folders.setText(formatted_date)
            self.btn_backup_date_folders.setMinimumWidth(120)
            self.btn_backup_date_folders.setFixedHeight(28)
            self.btn_backup_date_folders.setCheckable(True)
            self.btn_backup_date_folders.setAutoExclusive(True)
            self.btn_backup_date_folders.clicked.connect(
                    lambda *args, date = date:\
                        self.change_date(date)
                    )
            self.btn_backup_date_folders.setStyleSheet(
                    "QPushButton"
                    "{"
                        "color: black;"
                        "background: rgba(255, 255, 255, 0.7);"
                        "border: 1px solid rgba(0, 0, 0, 0.073);"
                        "border-bottom: 1px solid rgba(0, 0, 0, 0.183);"
                        "border-radius: 5px;"
                        "padding: 5px 12px 6px 12px;"
                        "outline: none;"
                        "font-size: 8px;"
                    "}"
                    
                    "QPushButton:hover" 
                    "{"
                        "font-size: 12px;"
                        "font-weight: bold;"
                    "}"

                    "QPushButton:checked"
                    "{"
                        "font-size: 12px;"
                        "color: rgba(0, 0, 0, 0.63);"
                        "background: rgba(249, 249, 249, 0.3);"
                        "border-bottom: 1px solid rgba(0, 0, 0, 0.073);"
                    "}")
            
            self.ui.dates_layout.addWidget(self.btn_backup_date_folders, QtCore.Qt.AlignHCenter)
        
        # Auto selected first date button
        for index in range(self.ui.dates_layout.count()):
            button = self.ui.dates_layout.itemAt(index).widget()
            if isinstance(button, QPushButton):
                # Check the last of the list
                button.setChecked(index == self.ui.dates_layout.count() - 1)
                # Select the last button on the list
                self.COUNTER_FOR_DATE = self.ui.dates_layout.count() - 1

    def create_backup_times_buttons(self):
        self.clean_stuff_on_screen("clean_files")

        try:
            inside_this_date_folder = f"{MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/"\
                f"{BACKUP_FOLDER_NAME}/{self.LIST_FOR_DATE_FOLDERS[(self.COUNTER_FOR_DATE)]}/"
        
            ################################################################################
            # If inside the external "date folders" has not "time folder", pass to avoid display error :D
            ################################################################################
            for time_folder in os.listdir(inside_this_date_folder):
                # Add found "dates time" to the Time list
                self.LIST_FOR_TIME_FOLDERS.append(time_folder)
                # Sort and reverse
                self.LIST_FOR_TIME_FOLDERS.sort(reverse=True)
                
                # Only add time button if self.CURRENT_FOLDER can be found inside current date and time
                if os.path.exists(
                        f"{MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}/"
                        f"{self.LIST_FOR_DATE_FOLDERS[(self.COUNTER_FOR_DATE)]}/{time_folder}/"):

                    ################################################################################
                    # PUSH BUTTON
                    ################################################################################
                    self.btn_backup_time_folders = QPushButton()
                    self.btn_backup_time_folders.setText(time_folder.replace("-", ":")  )
                    # time_folder = time_folder.replace(":", "-")  
                    self.btn_backup_time_folders.setFixedSize(100, 34)
                    # self.btn_backup_time_folders.setCheckable(True)
                    # self.btn_backup_time_folders.setAutoExclusive(True)
                    self.btn_backup_time_folders.setStyleSheet("""
                            color: black;
                            background: rgba(255, 255, 255, 0.7);
                            border: 1px solid rgba(0, 0, 0, 0.073);
                            border-bottom: 1px solid rgba(0, 0, 0, 0.183);
                            border-radius: 5px;
                            padding: 5px 12px 6px 12px;
                            outline: none;
                    """)

                # Auto selected that latest one
                self.btn_backup_time_folders.setChecked(True)  
        
        except IndexError as e:
            # Reset self.COUNTER_FOR_DATE
            self.COUNTER_FOR_TIME = 0
            # Add to self.COUNTER_FOR_DATE
            self.COUNTER_FOR_TIME += 1

        self.show_results()

    def show_results(self):
        conter = 0
        horizontal = 0
        vertical = 0

        # Clear previous results
        self.clean_stuff_on_screen("clean_files")
        
        try:
            inside_current_folder = f"{MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/"\
                f"{BACKUP_FOLDER_NAME}/{self.LIST_FOR_DATE_FOLDERS[self.COUNTER_FOR_DATE]}/"\
                f"{self.LIST_FOR_TIME_FOLDERS[self.COUNTER_FOR_TIME]}/{self.CURRENT_FOLDER}"
        
            # Show available files
            for results in os.listdir(inside_current_folder):
                # Only show files and hide hidden outputs
                if not results.startswith("."):
                    print("     Files: ", results)

                    # BUTTON
                    self.btn_backup_results = QPushButton()
                    self.btn_backup_results.setCheckable(True)
                    self.btn_backup_results.setFixedSize(160, 180)
                    self.btn_backup_results.setIconSize(QtCore.QSize(64, 64))
                    self.btn_backup_results.clicked.connect
                    (
                        lambda *, results = results: self.add_to_restore
                        (
                            results, self.LIST_FOR_DATE_FOLDERS[self.COUNTER_FOR_DATE],
                            self.LIST_FOR_TIME_FOLDERS[self.COUNTER_FOR_TIME])
                    )
                    
                    self.btn_backup_results.setStyleSheet(
                        "QPushButton" 
                            "{"
                                "color: black;"
                                "background: rgba(255, 255, 255, 0.7);"
                                "border: 1px solid rgba(0, 0, 0, 0.073);"
                                "border-bottom: 1px solid rgba(0, 0, 0, 0.183);"
                                "border-radius: 5px;"
                                "padding: 5px 12px 6px 12px;"
                                "outline: none;"
                                "font-size: 8px;"
                            "}"
                            
                        "QPushButton:hover"
                            "{"
                                "font-size: 12px;"
                                "font-weight: bold;"
                            "}"

                        "QPushButton:checked"
                            "{"
                                "font-size: 12px;"
                                "color: rgba(0, 0, 0, 0.63);"
                                "background: rgba(249, 249, 249, 0.3);"
                                "border-bottom: 1px solid rgba(0, 0, 0, 0.073);"
                            "}")
                    
                    # Text
                    text = QLabel(self.btn_backup_results)
                    text.setStyleSheet(
                        """
                            border: 0px;
                        """
                    )

                    # Short strings
                    countStrings = len(results)
                    recentEndswith = results.split(".")[-1]

                    # Label
                    if countStrings < 20:            
                        text.setText(f"{(results.capitalize())}")
                    else:
                        text.setText(f"{(results[:20].capitalize())}...{recentEndswith}")

                    # text.setFont(QFont("Ubuntu", 11))
                    text.move(0, (180 - 25))

                    # Show bigger preview if mouse hover
                    if results.endswith(IMAGE_PREFIX):
                        scaledHTML='width:"5%" height="250"'
                        self.btn_backup_results.setToolTip(
                            f"<img src={MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}"
                            f"/{self.LIST_FOR_DATE_FOLDERS[self.COUNTER_FOR_DATE]}/"
                            f"{self.LIST_FOR_TIME_FOLDERS[self.COUNTER_FOR_TIME]}/"
                            f"{self.CURRENT_FOLDER}/{results} {scaledHTML}/>")

                    ################################################################################
                    # Preview of files that are not in IMAGE_PREFIX
                    ################################################################################
                    # Image label
                    image = QLabel(self.btn_backup_results)
                    image.move(10, 10)
                    image.setStyleSheet(
                        "QLabel"
                        "{"
                        "background-repeat: no-repeat;"
                        "}")

                    # if results.endswith(IMAGE_PREFIX):
                    #     image = QImage(f"{MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}/"
                    #         f"{self.LIST_FOR_DATE_FOLDERS[self.COUNTER_FOR_DATE]}/{self.LIST_FOR_TIME_FOLDERS[self.COUNTER_FOR_TIME]}/"
                    #         f"{self.CURRENT_FOLDER}/{results}")

                    #     # Convert the image to a pixmap and use it
                    #     pixmap = QPixmap.fromImage(image)
                    #     scaled_pixmap=pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio)
                    #     self.btn_backup_results.setIcon(QIcon(scaled_pixmap))

                    if results.endswith(".txt"):
                        self.btn_backup_results.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/txt.png"))

                    elif results.endswith(".pdf"):
                        self.btn_backup_results.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/pdf.png"))

                    elif results.endswith(".py"):
                        self.btn_backup_results.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/py.png"))

                    elif results.endswith(".cpp"):
                        self.btn_backup_results.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/cpp.png"))

                    elif results.endswith(".sh"):
                        self.btn_backup_results.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/bash.png"))

                    elif results.endswith(".blend"):
                        self.btn_backup_results.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/blend.png"))

                    elif results.endswith(".excel"):
                        self.btn_backup_results.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/excel.png"))

                    elif results.endswith(".mp4"):
                        self.btn_backup_results.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/mp4.png"))

                    elif results.endswith(".iso"):
                        self.btn_backup_results.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/iso.png"))
                    
                    elif not results.endswith(".")and "." not in results:
                        self.btn_backup_results.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/folder.svg"))

                    else:
                        self.btn_backup_results.setIcon(QIcon(f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/none.png"))

                    self.ui.results_layout_grid.addWidget(self.btn_backup_results, vertical, horizontal)
                    
                    # Show x horizontal items per page
                    conter += 1
                    horizontal += 1

                    if conter %5 == 0:
                        # Reset counts
                        conter = 0
                        # Reset horizontal
                        horizontal = 0
                        # Add 1 to vertical
                        vertical += 1

        # Change dates until find current folder as backup inside backup device
        except FileNotFoundError as f:
            # list_of_available_times = len(self.LIST_FOR_TIME_FOLDERS)
            if len(self.LIST_FOR_TIME_FOLDERS) > 1 and \
                not len(self.LIST_FOR_TIME_FOLDERS) ==\
                self.LIST_FOR_TIME_FOLDERS.index(
                self.LIST_FOR_TIME_FOLDERS[self.COUNTER_FOR_TIME]) + 1:

                # If is not the last time folder available at this date
                # Change time
                self.COUNTER_FOR_TIME += 1
                # Get new restults
                self.show_results()
            
            else:
                # Needs to be "-", because list is reverse, down to the top
                self.COUNTER_FOR_DATE -= 1
                # Reset time
                self.COUNTER_FOR_TIME = 0
                # Get new restults
                self.show_results()

            # Autocheck the found date button
            self.check_found_date_button()

        # If a non backup folder was clicked
        except IndexError as i:
            print(i)
            pass

        # print("Date available: ", self.LIST_FOR_DATE_FOLDERS)
        # print("Time available: ", self.LIST_FOR_TIME_FOLDERS)
        # print("Current date: ", self.LIST_FOR_DATE_FOLDERS[self.COUNTER_FOR_DATE])
        # print("Current time: ", self.LIST_FOR_TIME_FOLDERS[self.COUNTER_FOR_TIME])
        # print("COUNT DATE INDEX:", self.COUNTER_FOR_DATE)
        # print("COUNT TIME INDEX:", self.COUNTER_FOR_TIME)
        # print("Current folder:", self.CURRENT_FOLDER)
        # print("")

        self.check_up_down_arrow()
        # self.label_update()
            
    def check_up_down_arrow(self):
        # Get index of the current time folder
        self.INDEX_TIME = self.LIST_FOR_TIME_FOLDERS.index(self.LIST_FOR_TIME_FOLDERS[self.COUNTER_FOR_TIME])
        
        ################################################################################
        # DOWN ARROW
        ################################################################################
        # If the first time from list is checked
        if self.INDEX_TIME  == 0:  # 0 = The latest time folder available
            # Disable down arrow, unable to go back from 0
            self.ui.btn_down.setEnabled(False)
        else:
            # Enable down arrow, able to go back from current index
            self.ui.btn_down.setEnabled(True)
        
        ################################################################################
        # UP ARROW
        ################################################################################
        # If is there more options to choosed from time list
        if self.INDEX_TIME  + 1  == len(self.LIST_FOR_TIME_FOLDERS):
            # Disable up arrow, unable to go forward, there is no more options to choose
            self.ui.btn_up.setEnabled(False)
        else:
            # Enable up arrow, able to go forward, there is more options to choose
            self.ui.btn_up.setEnabled(True)

        self.label_update()

    def label_update(self):
        date_now = MAIN_INI_FILE.current_date() + "-" + MAIN_INI_FILE.current_month()+ "-"+ MAIN_INI_FILE.current_year()

        # Update current folder (label)
        self.currentLocationLabel.setText(f"<h1>{self.CURRENT_FOLDER}</h1>")
        self.currentLocationLabel.adjustSize()

        try:
            if self.LIST_FOR_DATE_FOLDERS[self.COUNTER_FOR_DATE] == str(date_now):
                # Update date label
                self.ui.label_gray_time.setText(f'Today ({self.LIST_FOR_TIME_FOLDERS[self.COUNTER_FOR_TIME]})'.replace("-", ":"))
            else:
                self.ui.label_gray_time.setText(f'({self.LIST_FOR_TIME_FOLDERS[self.COUNTER_FOR_TIME]})'.replace("-", ":"))
        # If a non backup folder was clicked
        except IndexError as i:
            print(i)
            pass


    ################################################################################
    # STATIC
    ################################################################################
    def btn_up_clicked(self):
        # self.COUNTER_FOR_DATE = 0
        self.COUNTER_FOR_TIME += 1

        # Show results after change index for current time folder
        self.show_results()

    def btn_down_clicked(self):
        # self.COUNTER_FOR_DATE = 0
        self.COUNTER_FOR_TIME -= 1
        
        # Show results after change index for current time folder
        self.show_results()

    def change_date(self, date):
        # for index in range(self.ui.dates_layout.count()):
        #     button = self.ui.dates_layout.itemAt(index).widget()
        #     if isinstance(button, QPushButton):
        #         button.setChecked(False)
        #         break

        # Reset times int, so it begins from [0] 
        # = The first time available inside the choosed date
        self.COUNTER_FOR_TIME = 0
        
        # Clean folders time list, before add the new one from new choosed date
        self.LIST_FOR_TIME_FOLDERS.clear()

        # Change current date
        # Index of the date
        self.COUNTER_FOR_DATE = self.LIST_FOR_DATE_FOLDERS.index(date)
        
        # Return to get backup folders time after date has changed
        self.create_backup_times_buttons()

    def change_dir(self, dir):
        # Update self.CURRENT_FOLDER
        self.CURRENT_FOLDER = dir
        # Reset time
        self.COUNTER_FOR_TIME = 0
        # self.COUNTER_FOR_DATE = 0
        
        # Auto selected first date button
        # for index in range(self.ui.dates_layout.count()):
        #     button = self.ui.dates_layout.itemAt(index).widget()
        #     if isinstance(button, QPushButton):
        #         # Select the last button on the list
        #         self.COUNTER_FOR_DATE = self.ui.dates_layout.count() - 1

        # self.check_found_date_button()
        self.show_results()
    
    def clean_stuff_on_screen(self, clean):
        ################################################################################
        # Update screen files by removing items before show the new ones
        ################################################################################
        if clean == "clean_folders":
            print("Cleaning folders...")
            for i in range(self.ui.folders_layout.count()):
                widget = self.ui.folders_layout.itemAt(i).widget()
                widget.deleteLater()
                i -= 1

        elif clean == "clean_files":
            print("Cleaning results...")
            for i in range(self.ui.results_layout_grid.count()):
                widget = self.ui.results_layout_grid.itemAt(i).widget()
                widget.deleteLater()
                i -= 1
            
        # if clean == "clean_time":
        #     for i in range(self.ui.tim.count()):
        #         widget = self.ui.tim.itemAt(i).widget()
        #         widget.deleteLater()
        #         i -= 1

    def add_thumbs(self):
        for index in range(self.ui.results_layout_grid.count()):
            button = self.ui.results_layout_grid.itemAt(index).widget()

            if isinstance(button, QPushButton):
                if button.text().endswith(IMAGE_PREFIX):
                    image = QImage
                    (
                        f"{MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}/"
                        f"{self.LIST_FOR_DATE_FOLDERS[self.COUNTER_FOR_DATE]}/{self.LIST_FOR_TIME_FOLDERS[self.COUNTER_FOR_TIME]}/"
                        f"{self.CURRENT_FOLDER}/{button.text()}"
                    )

                    # Convert the image to a pixmap and use it
                    pixmap = QPixmap.fromImage(image)
                    scaled_pixmap = pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio)
                    button.setIcon(QIcon(scaled_pixmap))
        
    def add_to_restore(self, output, date, time):
        if not " " in output:
            if not output in FILES_TO_RESTORE:  # Check if output is already inside list
                FILES_TO_RESTORE.append(output)  # Add output to the list files to restore
            else:
                FILES_TO_RESTORE.remove(output)  # Remove item if already in list

        else:
            if not output in FILES_TO_RESTORE_WITH_SPACES:  # Check if output is already inside list
                FILES_TO_RESTORE_WITH_SPACES.append(output)  # Add output to the list files to restore
            else:
                FILES_TO_RESTORE_WITH_SPACES.remove(output)  # Remove item if already in list

        print("")
        print("No spaces list   : ", FILES_TO_RESTORE)
        print("with spaces list : ", FILES_TO_RESTORE_WITH_SPACES)

        ################################################################################
        # Enable/Disable functions if item(s) is/are selected
        ################################################################################
        # TODO
        if len(FILES_TO_RESTORE) or len(FILES_TO_RESTORE_WITH_SPACES) >= 1:  # If something inside list
            self.ui.btn_restore.setEnabled(True)
            # Restore label + filesToRestore and FILES_TO_RESTORE_WITH_SPACES lenght
            self.ui.btn_restore.setText(f"   Restore({len(FILES_TO_RESTORE) + len(FILES_TO_RESTORE_WITH_SPACES)})   ")

            # Hide up function if 1 or more items is/are selected
            # Up
            self.ui.btn_up.setEnabled(False)

            # Hide down function if 1 or more items is/are selected
            # Down
            self.ui.btn_down.setEnabled(False)

            try:
                # Hide time functions from TimeVLayout if 1 or more items is/are selected
                for i in range(self.ui.dates_layout.count()):
                    item = self.ui.dates_layout.itemAt(i)
                    widget = item.widget()
                    widget.setEnabled(False)  # Disable function
                    i -= 1
            except AttributeError:
                pass

            try:
                # Hide folders functions from foldersVLayout if 1 or more items is/are selected
                for i in range(self.ui.folders_layout.count()):
                    item = self.ui.folders_layout.itemAt(i)
                    widget = item.widget()
                    widget.setEnabled(False)  # Disable function
                    i -= 1
            except AttributeError:
                pass

        else:
            # Disable restore button
            self.ui.btn_restore.setEnabled(False)
            # Set FILES_TO_RESTORE length
            self.ui.btn_restore.setText("   Restore   ")
            
            try:
                # Show time functions from TimeVLayout if 1 or more items is/are selected
                for i in range(self.ui.dates_layout.count()):
                    item=self.ui.dates_layout.itemAt(i)
                    widget=item.widget()
                    widget.setEnabled(True)
                    i -= 1
            except AttributeError:
                pass
            
            try:
                # Show folders functions from foldersVLayout if 1 or more items is/are selected
                for i in range(self.ui.folders_layout.count()):
                    item=self.ui.folders_layout.itemAt(i)
                    widget=item.widget()
                    widget.setEnabled(True)  
                    i -= 1
            except ArithmeticError:
                pass

        # Connection restore button
        self.ui.btn_restore.clicked.connect(lambda *args, date = date, time = time: self.start_restore(date, time))
    
    def start_restore(self, date, time):
        MAIN_INI_FILE.set_database_value('STATUS', 'is_restoring', 'True')

        ################################################################################
        # Restore files without spaces
        ################################################################################
        print("Your files are been restored...")
        
        counter = 0
        for _ in FILES_TO_RESTORE:
            print(f"Restoring {COPY_RSYNC_CMD} {MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/"
                f"{BACKUP_FOLDER_NAME}/{date}/{time}/{self.CURRENT_FOLDER}/"
                f"{FILES_TO_RESTORE[counter]} {HOME_USER}/{self.CURRENT_FOLDER}/")
            
            sub.Popen(
                f"{COPY_RSYNC_CMD} {MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/"
                f"{BACKUP_FOLDER_NAME}/{date}/{time}/{self.CURRENT_FOLDER}/"
                f"{FILES_TO_RESTORE[counter]} {HOME_USER}/{self.CURRENT_FOLDER}/",
                shell=True)
            
            # Add to counter
            counter += 1

        ################################################################################
        # Restore files with spaces
        ################################################################################
        counter = 0
        for _ in FILES_TO_RESTORE_WITH_SPACES:
            # print(f"Restoring {COPY_RSYNC_CMD} {MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/"
            #     f"{BACKUP_FOLDER_NAME}/{date}/{time}/{self.CURRENT_FOLDER}/"
            #     f"{FILES_TO_RESTORE_WITH_SPACES[counter]} {HOME_USER}/{self.CURRENT_FOLDER}/")
            
            sub.Popen(
                f"{COPY_RSYNC_CMD} {MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/"
                f"{BACKUP_FOLDER_NAME}/{date}/{time}/{self.CURRENT_FOLDER}/"
                f"{FILES_TO_RESTORE_WITH_SPACES[counter]} {HOME_USER}/"
                f"{self.CURRENT_FOLDER}/", shell=True)

            # Add to counter
            counter += 1

        # Open file manager
        if not self.ALREADY_OPENED_FILE_MANAGER:
            self.ALREADY_OPENED_FILE_MANAGER = True

            # Open folder manager
            sub.Popen(f"xdg-open {HOME_USER}/{self.CURRENT_FOLDER}",shell=True)
        
        MAIN_INI_FILE.set_database_value('STATUS', 'is_restoring', 'False')

        exit()

    def check_found_date_button(self):
        try:
            # Make sure to check the found date button
            found_in_this_date_and_time = self.LIST_FOR_DATE_FOLDERS.index(self.LIST_FOR_DATE_FOLDERS[self.COUNTER_FOR_DATE])
            for index in range(self.ui.dates_layout.count()):
                button = self.ui.dates_layout.itemAt(index).widget()

                if index == found_in_this_date_and_time:
                    if isinstance(button, QPushButton):
                        button.setChecked(True)  
                        button.click()  
                        break

        # If a non backup folder was clicked
        except IndexError as i:
            print(i)
            pass

if __name__ == "__main__":
    APP = QApplication(sys.argv)
    
    MAIN = MainWindow()
    MAIN.create_backup_home_folders_buttons()
    MAIN.create_backup_dates_buttons()
    MAIN.create_backup_times_buttons()

    MAIN.showFullScreen()
    MAIN.show()
    
    sys.exit(APP.exec())
