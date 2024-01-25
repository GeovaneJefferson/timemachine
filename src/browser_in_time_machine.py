# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_fo

from ui.ui_untitled import Ui_MainWindow
from setup import *
from read_ini_file import UPDATEINIFILE
from datetime import datetime
from get_latest_backup_date import latest_backup_date_label
from handle_spaces import handle_spaces

def get_full_location(item, column):
    item_txt = item.text(column)
    full_location = item_txt

    parent_item = item.parent()
    while parent_item:
        parent_txt = parent_item.text(column)
        full_location = f"{parent_txt}/{full_location}"
        parent_item = parent_item.parent()

    return full_location

def item_full_location(item, column):
    item_txt = item.text(column)
    full_location = item_txt

    parent_item = item.parent()

    while parent_item:
        parent_txt = parent_item.text(column)
        full_location = f"{parent_txt}/{full_location}"
        parent_item = parent_item.parent()

    return full_location

def size_format(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"

        size_bytes /= 1024.0

def get_all_backup_folders():
    folders_list = []

    # Connect to the SQLite database
    conn = sqlite3.connect(SRC_USER_CONFIG_DB)
    cursor = conn.cursor()
    # Query all keys from the specified table
    cursor.execute(f"SELECT key FROM FOLDER")
    keys = [row[0] for row in cursor.fetchall()]
    # Close the connection
    conn.close()

    for folder in keys:
        folders_list.append(folder)
        folders_list.sort()

    return folders_list


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.folder_already_opened = False

        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)  # This ensures exclusive behavior

        self.checked_items = []

        self.ALREADY_CHECKED_FIRST_FOLDER = False

        self.files_to_restore = []
        self.list_of_preview_items = []
        self.LIST_OF_ALL_BACKUP_DATES = []
        self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE = []

        self.INDEX_TIME = 0
        self.COUNTER_FOR_DATE = 0
        self.COUNTER_FOR_TIME = 0

        self.current_location_label = QLabel(self)
        self.current_folder = ''

        # # Connections
        # # Up button
        # self.ui.btn_up.clicked.connect(self.btn_up_clicked)
        # # Down button
        # self.ui.btn_down.clicked.connect(self.btn_down_clicked)
        # # Cancel button
        # self.ui.btn_cancel.clicked.connect(btn_cancel_clicked)
        # # Restore button
        # self.ui.btn_restore.clicked.connect(self.start_restore)

        # Settings from QTree
        self.ui.tree_widget.setHeaderLabels(["Name", "Date Modified", "Size", "Type"])
        self.ui.tree_widget.setColumnWidth(0, 250)
        self.ui.tree_widget.setColumnWidth(1, 150)
        # self.ui.tree_widget.clicked.connect(self.selected_item_for_preview)
        # self.ui.tree_widget.itemSelectionChanged.connect(self.selected_item_for_preview)
        self.ui.tree_widget.itemChanged.connect(self.qtree_checkbox_clicked)

        # Settings for the preview window
        self.preview_window = None

    def add_backup_folders(self):
        folder_list = []
        # Get backup folder from main folder
        for folder in os.listdir(MAIN_INI_FILE.main_backup_folder()):
            folder_list.append(folder)

        # Sort them
        folder_list.sort()

        for folder in folder_list:
            folder = str(folder)

            try:
                # Can the folder be found inside Users Home?
                folder = folder.capitalize()
                
                # Try to access it  
                os.listdir(f"{HOME_USER}/{folder}")

            except FileNotFoundError:
                # Lower folder first letter
                folder = folder.lower()  # Lower folder first letter

            ################################################################################
            # PUSH BUTTON
            ################################################################################
            self.btn_backup_home_folders = QPushButton()
            self.btn_backup_home_folders.setText(folder)
            self.btn_backup_home_folders.setFixedSize(140, 34)
            self.btn_backup_home_folders.setCheckable(True)
            self.btn_backup_home_folders.setAutoExclusive(True)
            self.btn_backup_home_folders.setStyleSheet(
                """
                    QPushButton
                    {
                        padding: 5px 12px 6px 12px;
                        outline: none;
                        font-size: 12px;
                    }
                """)
            # self.btn_backup_home_folders.clicked.connect(lambda *args, directory=folder: self.change_directory(directory))
            self.ui.folders_layout.addWidget(self.btn_backup_home_folders)

            # Automatically check the first folder in the list
            if not self.ALREADY_CHECKED_FIRST_FOLDER:
                self.btn_backup_home_folders.setChecked(True)
                # Set as current selected folder
                self.current_folder = folder
                # Set already checked to True
                self.ALREADY_CHECKED_FIRST_FOLDER = True

        # Add stretch after the last added folder
        self.ui.folders_layout.addStretch()

    def show_results(self):
        # Clean previous results
        # self.delete_all_results()

        # Show files/folder from the current folder in main
        inside_current_folder = f'{MAIN_INI_FILE.main_backup_folder()}/'\
                                f'{self.current_folder}'

        print(inside_current_folder)

        # Add options to QTree
        file_list = []
        try:
            for filename in os.listdir(inside_current_folder):
                full_path = os.path.join(inside_current_folder, filename)

                # Is a file
                if os.path.isfile(full_path): 
                    # Size
                    result_size = os.path.getsize(full_path)
                    # Date 
                    date_modified = os.path.getmtime(full_path)
                    # Extension 
                    extension = os.path.splitext(filename)[1]

                    # Fix extension
                    if extension == '':
                        extension = '.txt'

                    formatted_date = datetime.fromtimestamp(
                        date_modified).strftime('%Y-%m-%d %H:%M:%S')
                    
                    formatted_size = size_format(result_size) if result_size is not None else ''
                    file_list.append((filename, 
                                      formatted_date,
                                      formatted_size,
                                      extension,
                                      date_modified))

            # Sort the file list by filename before populating the tree
            file_list.sort(key=lambda x: x[0])

            # Add result to the QTree Widget
            for item_data in file_list:
                qt_item = QTreeWidgetItem(self.ui.tree_widget, item_data[:-1])
                qt_item.setData(1, Qt.UserRole, item_data[-1])  # Store the timestamp as user data
                qt_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                qt_item.setCheckState(0, Qt.Unchecked)

            self.qtree_add_results(inside_current_folder)

        except FileNotFoundError:
            pass

    def qtree_add_results(self, inside_current_folder):
        for folder_name in os.listdir(inside_current_folder):
            folder_path = os.path.join(inside_current_folder, folder_name)

            # Is a dir
            if os.path.isdir(folder_path):
                folder_item = QTreeWidgetItem(self.ui.tree_widget, [folder_name, '', '', 'Folder'])
                
                # Chekbox for folders
                folder_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                folder_item.setCheckState(0, Qt.Unchecked)
                
                # self.qtree_add_sub_items(folder_item, folder_path)
        
    
    def qtree_add_sub_items(self, parent_item, folder_path):
        for item_name in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item_name)

            # Is a dir
            if os.path.isdir(item_path):
                # sub_folder_item = QTreeWidgetItem(parent_item, [item_name, '', '', 'Folder'])

                print(item_path)
                
                # Checkbox
                folder = QTreeWidgetItem(parent_item,
                                        [item_name,
                                        formatted_date,
                                        formatted_size,
                                        extension])
                folder.setData(1, Qt.UserRole, date_modified)  # Store the timestamp as user data
                folder.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                folder.setCheckState(0, Qt.Unchecked)

                # TODO
                # By uncomment this, will add all subfolders and so on, but freezes ui
                # self.qtree_add_sub_items(sub_folder_item, item_path)
                
            elif os.path.isfile(item_path):
                item_size = os.path.getsize(item_path)
                date_modified = os.path.getmtime(item_path)
                extension = os.path.splitext(item_name)[1]

                formatted_date = datetime.fromtimestamp(date_modified).strftime('%Y-%m-%d %H:%M:%S')
                formatted_size = size_format(item_size) if item_size is not None else ''

                # Checkbox
                item = QTreeWidgetItem(parent_item, [item_name, formatted_date, formatted_size, extension])
                item.setData(1, Qt.UserRole, date_modified)  # Store the timestamp as user data
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                item.setCheckState(0, Qt.Unchecked)

    def qtree_checkbox_clicked(self, item, column):
        if item.checkState(column) == Qt.Checked:
            item_txt = item.text(column)

            # Item full location
            item_full_location = get_full_location(item, column)

            if item_full_location not in self.files_to_restore:
                # Add if not already in the list
                self.files_to_restore.append(item_full_location)
        
            else:
                # Remove from the list
                self.files_to_restore.remove(item_full_location)

        elif item.checkState(column) == Qt.Unchecked:
            # Item full location
            item_full_location = item.text(column)
            
            try:
                self.files_to_restore.remove(item_full_location)
        
            except ValueError:
                pass
            
        if self.files_to_restore:
            self.show_small_preview(self.files_to_restore[-1])
        
        else:
            self.ui.small_preview_label.clear()
        
        # Add to the restore list
        self.add_to_restore()
    
    def show_small_preview(self, item_txt):
        # Item extension
        item_extension = str(item_txt).split('.')[-1]
        
        # Item full location
        item_full_location = f'{MAIN_INI_FILE.main_backup_folder()}/'\
                            f'{self.current_folder}/{item_txt}'
        
        print('Item full location:', item_full_location)
        
        # Is a file
        if os.path.isfile(item_full_location):
            # Image
            if item_extension in IMAGE_TYPES:
                pixmap = QPixmap(item_full_location)
                pixmap = pixmap.scaledToWidth(196, Qt.SmoothTransformation)
                self.ui.small_preview_label.setPixmap(pixmap)

                # Hide ui text
                self.ui.small_preview_text.setFixedHeight(0)
                self.ui.small_preview_text.hide()

                # Expand ui label
                self.ui.small_preview_label.setFixedHeight(222)
                self.ui.small_preview_label.show()

            elif item_extension in TXT_TYPES:
                self.read_file(item_full_location)

            # Non ok item
            else:
                # Hide ui text
                self.ui.small_preview_text.setFixedHeight(0)
                self.ui.small_preview_text.hide()

                # Hide ui label
                self.ui.small_preview_label.setFixedHeight(0)
                self.ui.small_preview_label.hide()     

    def read_file(self, file):
        with open(file, "r") as file:
            # Hide ui label
            self.ui.small_preview_label.setFixedHeight(0)
            self.ui.small_preview_label.hide()

            # Expand ui text
            self.ui.small_preview_text.setFixedHeight(222)
            self.ui.small_preview_text.show()

            self.ui.small_preview_text.adjustSize()
            self.ui.small_preview_text.setPlainText(file.read())
            self.ui.small_preview_text.moveCursor(QTextCursor.Start)
            self.ui.small_preview_text.setStyleSheet(
                '''
                    font-size: 10px;
                ''')
    
    def add_to_restore(self):
        ################################################################################
        # Enable/Disable functions if item(s) is/are selected
        ################################################################################
        if len(self.files_to_restore)  >= 1:  # If something inside the list
            # If it has at least one item, enable restore button
            self.ui.btn_restore.setEnabled(True)
            
            # Update restore label
            self.ui.btn_restore.setText(
                f'   Restore({len(self.files_to_restore)})   ')

            # Disable other buttons if items have been selected
            self.ui.btn_up.setEnabled(False)
            self.ui.btn_down.setEnabled(False)

            # Disable all home folders
            for i in range(self.ui.folders_layout.count()):
                item_from_list = self.ui.folders_layout.itemAt(i)
                widget = item_from_list.widget()

                if isinstance(widget, QPushButton):
                    widget.setEnabled(False)  # Disable function
                    i -= 1

            # # Disable all home folders
            # for i in range(self.ui.dates_layout.count()):
            #     item_from_list = self.ui.dates_layout.itemAt(i)
            #     widget = item_from_list.widget()
                
            #     if isinstance(widget, QPushButton):
            #         widget.setEnabled(False)  # Disable function
            #         i -= 1

        # If not, item was selected
        else:
            # Disable restore button
            self.ui.btn_restore.setEnabled(False)
            # Set self.files_to_restore length
            self.ui.btn_restore.setText("   Restore   ")

            # Enable all home folders            
            for i in range(self.ui.folders_layout.count()):
                item_from_list = self.ui.folders_layout.itemAt(i)
                widget = item_from_list.widget()
                if isinstance(widget, QPushButton):
                    widget.setEnabled(True)  # Disable function
                    i -= 1

            # # Enable all dates folders            
            # for i in range(self.ui.dates_layout.count()):
            #     item_from_list = self.ui.dates_layout.itemAt(i)
            #     widget = item_from_list.widget()
            #     if isinstance(widget, QPushButton):
            #         widget.setEnabled(True)  # Disable function
            #         i -= 1

class PreviewWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preview")
        self.setModal(True)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.file_directory = ''

        self.layout = QVBoxLayout(self)

    def set_preview(self, pixmap):
        open_file_button = QPushButton()
        open_file_button.setText("Open File Directory")
        open_file_button.setFocusPolicy(Qt.NoFocus)
        open_file_button.clicked.connect(self.open_file_button_clicked)

        if isinstance(pixmap, QPixmap):
            pixmap = pixmap.scaledToWidth((screen_height - 440), Qt.SmoothTransformation)
            preview_label = QLabel(self)
            preview_label.setPixmap(pixmap)

            self.layout.addWidget(preview_label)

        elif isinstance(pixmap, str):
            text_browser = QTextBrowser(self)
            text_browser.setFixedSize(
                (screen_height - 440), 
                (screen_height - 440))
            text_browser.setPlainText(pixmap)
            text_browser.adjustSize()
            text_browser.moveCursor(QTextCursor.Start)

            # Layouts
            self.layout.addWidget(text_browser)
            self.layout.addWidget(open_file_button)

        self.layout.addWidget(open_file_button)
        self.layout.setAlignment(open_file_button, Qt.AlignHCenter | Qt.AlignVCenter)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.remove_items()

    def remove_items(self):
        for i in range(self.layout.count()):
            widget_item = self.layout.itemAt(i)

            if widget_item.widget():
                print("Removing items")
                widget_item.widget().deleteLater()

        self.close()

    def open_file_button_clicked(self):
        file_directory = "/".join(self.file_directory.split("/")[:-1])
        # Open file directory
        sub.Popen(["xdg-open", file_directory], stdout=sub.PIPE, stderr=sub.PIPE).wait()
        
        # Close external preview window
        self.remove_items()



if __name__ == "__main__":
    APP = QApplication(sys.argv)

    screen = APP.primaryScreen()  # Get the primary screen
    size = screen.size()  # Get the screen size
    screen_width = size.width()  # Get the screen width
    screen_height = size.height()  # Get the screen height

    MAIN_INI_FILE = UPDATEINIFILE()
    MAIN = MainWindow()
    MAIN.setWindowTitle("Browser In Time Machine")

    # Get all backup folders
    get_all_backup_folders()
    # Add all backup folders
    MAIN.add_backup_folders()

    MAIN.show_results()

    # # Get all backup dates
    # MAIN.get_all_backup_dates()
    # # Add all backup dates
    # MAIN.add_backup_dates()

    # # Add  backup times folders for the current date folder
    # MAIN.add_backup_times()

    # MAIN.update_labels()

    # MAIN.showFullScreen()
    MAIN.show()

    sys.exit(APP.exec())
