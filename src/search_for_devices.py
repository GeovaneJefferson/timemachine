#! /usr/bin/python3
from setup import *


class EXTERNAL(QWidget):
    def __init__(self):
        super(EXTERNAL, self).__init__()
        self.foundInMedia = None
        self.outputBox = ()
        self.iniUI()

    def iniUI(self):
        self.setWindowIcon(QIcon(src_backup_icon))
        self.setWindowTitle("Choose device:")
        self.setFixedSize(500, 380)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        ################################################################################
        # Center window
        ################################################################################
        centerPoint = QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen()).center()
        fg = self.frameGeometry()
        fg.moveCenter(centerPoint)
        self.move(fg.topLeft())

        self.read_ini_file()

    def read_ini_file(self):
        ################################################################################
        # Read INI file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)

        # Read INI file
        self.iniHDName = config['EXTERNAL']['name']

        self.widgets()

    def widgets(self):
        ################################################################################
        # Frame
        ################################################################################
        self.whereFrame = QFrame()
        self.whereFrame.setFixedSize(440, 280)
        self.whereFrame.move(20, 40)
        # self.whereFrame.setStyleSheet("""
        #    background-color: rgb(38, 39, 40);
        # """)

        # Scroll
        self.scroll = QScrollArea(self)
        self.scroll.setFixedSize(460, 280)
        self.scroll.move(20, 40)
        self.scroll.setWidgetResizable(True)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidget(self.whereFrame)

        # Vertical layout V
        self.verticalLayout = QVBoxLayout(self.whereFrame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        
        # Use this device
        self.useDiskButton = QPushButton(self)
        self.useDiskButton.setFont(item)
        self.useDiskButton.setText("Use Disk")
        self.useDiskButton.adjustSize()
        # self.useDiskButton.setFixedSize(80, 28)
        self.useDiskButton.move(400, 340)
        self.useDiskButton.setEnabled(False)
        self.useDiskButton.clicked.connect(self.on_use_disk_clicked)

        # Refresh button
        self.refreshButton = QPushButton(self)
        self.refreshButton.setFont(item)
        self.refreshButton.setText("Refresh")
        self.refreshButton.adjustSize()
        self.refreshButton.move(300, 340)
        self.refreshButton.clicked.connect(self.on_button_refresh_clicked)

        # Cancel button
        self.cancelButton = QPushButton(self)
        self.cancelButton.setFont(item)
        self.cancelButton.setText("Cancel")
        self.cancelButton.adjustSize()
        self.cancelButton.move(200, 340)
        self.cancelButton.clicked.connect(self.on_button_cancel_clicked)

        self.check_connection()

    def check_connection(self):
        ################################################################################
        # Search external inside media
        ################################################################################
        try:
            print("Searching for external devices under media...")
            if not len(os.listdir(f'{media}/{userName}')) == 0:
                print(f"{media} is Empty")
                self.foundInMedia = True
                self.show_on_screen(media)

                print("Searching for external devices under run...")
            elif not len(os.listdir(f'{run}/{userName}')) == 0:
                self.foundInMedia = False
                self.show_on_screen(run)

        except FileNotFoundError:
            print("No device found...")
            pass

    def show_on_screen(self, location):
        print("Showing available devices")
        ################################################################################
        # Check source
        ################################################################################
        if self.foundInMedia:
            self.foundWhere = media
        else:
            self.foundWhere = run

        ################################################################################
        # Add buttons and images for each external
        ################################################################################
        for output in os.listdir(f'{location}/{userName}'):
            # Avaliables external devices
            self.availableDevices = QPushButton(self.whereFrame)
            self.availableDevices.setFont(QFont('Ubuntu', 12))
            self.availableDevices.setText(output)
            self.availableDevices.setFixedSize(444, 60)
            self.availableDevices.setCheckable(True)
            text = self.availableDevices.text()
            self.availableDevices.clicked.connect(lambda *args, text=text: self.on_device_clicked(text))

            # Image
            image = QLabel(self.availableDevices)
            image.setFixedSize(96, 96)
            image.move(2, -15)
            image.setStyleSheet(
                "QLabel"
                "{"
                f"background-image: url({src_restore_small_icon});"
                "background-repeat: no-repeat;"
                "background-color: transparent;"

                "}")

            ################################################################################
            # Auto checked this choosed external device
            ################################################################################
            if text == self.iniHDName:
                self.availableDevices.setChecked(True)

            ################################################################################
            # Add widgets and Layouts
            ################################################################################
            # Vertical layout
            self.verticalLayout.addWidget(self.availableDevices, 0, QtCore.Qt.AlignHCenter)

    def on_use_disk_clicked(self):
        ################################################################################
        # Adapt external name is it has space in the name
        ################################################################################
        if " " in self.outputBox:
            self.outputBox = str(self.outputBox.replace(" ", "\ "))

        ################################################################################
        # Update INI file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set(f'EXTERNAL', 'hd', f'{self.foundWhere}/{userName}/{self.outputBox}')
            config.set('EXTERNAL', 'name', f'{self.outputBox}')
            config.write(configfile)

        self.close()

    def on_device_clicked(self, output):
        if self.availableDevices.isChecked():
            self.outputBox = output
            # Enable use disk
            self.useDiskButton.setEnabled(True)
        else:
            self.outputBox = ""
            # Disable use disk
            self.useDiskButton.setEnabled(False)

    def on_button_refresh_clicked(self):
        sub.Popen(f"python3 {src_search_for_devices}", shell=True)
        exit()

    def on_button_cancel_clicked(self):
        exit()


APP = QApplication(sys.argv)
main = EXTERNAL()
main.show()
APP.exit(APP.exec())
