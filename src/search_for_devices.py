#! /usr/bin/python3
from setup import *

# QTimer
timer = QtCore.QTimer()

################################################################
# Window management
################################################################
windowXSize = 500
windowYSize = 380


class EXTERNAL(QWidget):
    def __init__(self):
        super(EXTERNAL, self).__init__()
        self.foundInMedia = None
        self.chooseDevice = ()
        self.captureDevices = []

        self.iniUI()

    def iniUI(self):
        self.setWindowIcon(QIcon(src_backup_icon))
        self.setWindowTitle("External devices:")
        self.setFixedSize(windowXSize, windowYSize)
        # self.setFixedSize(windowXSize, windowYSize)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        ################################################################################
        # Center window
        ################################################################################
        centerPoint = QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen()).center()
        fg = self.frameGeometry()
        fg.moveCenter(centerPoint)
        self.move(fg.topLeft().x(), fg.topLeft().y())
        
        # Opening animation
        # self.openAnimation = QPropertyAnimation(self, b"size")
        # self.openAnimation.setEndValue(QSize(windowXSize, windowYSize))
        # self.openAnimation.setDuration(150)
        # self.openAnimation.start()

        self.read_ini_file()

    def read_ini_file(self):
        # Read INI file
        config = configparser.ConfigParser()
        config.read(src_user_config)
        self.iniHDName = config['EXTERNAL']['name']

        self.widgets()

    def widgets(self):
        ################################################################################
        # Frame
        ################################################################################
        self.whereFrame = QFrame()
        self.whereFrame.setFixedSize(440, 280)
        self.whereFrame.move(20, 40)

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
        
       # Protocol combobox
        # self.protocolComboBox = QComboBox(self)
        # self.protocolComboBox.setFrame(True)
        # self.protocolComboBox.setFixedSize(60, 28)
        # self.protocolComboBox.setFont(QFont("Ubuntu", 11))
        # self.protocolComboBox.move(20, 336)
        # self.protocolComboBox.setStyleSheet(
        #     "QComboBox"
        #     "{"
        #         "border: 0px solid transparent;"
        #     "}")

        # protocolList = [
        #     "ftp:",
        #     "stp:"]
        # self.protocolComboBox.addItems(protocolList)
        # self.protocolComboBox.currentIndexChanged.connect(self.on_every_combox_changed)

        # Cancel button
        self.cancelButton = QPushButton(self)
        self.cancelButton.setFont(item)
        self.cancelButton.setText("Cancel")
        self.cancelButton.adjustSize()
        self.cancelButton.move(300, 340)
        self.cancelButton.clicked.connect(self.on_button_cancel_clicked)

        # Use this device
        self.useDiskButton = QPushButton(self)
        self.useDiskButton.setFont(item)
        self.useDiskButton.setText("Use Disk")
        self.useDiskButton.adjustSize()
        # self.useDiskButton.setFixedSize(80, 28)
        self.useDiskButton.move(400, 340)
        self.useDiskButton.setEnabled(False)
        self.useDiskButton.clicked.connect(self.on_use_disk_clicked)

        # Update
        timer.timeout.connect(self.check_connection)
        timer.start(2000) # Update every x seconds
        self.check_connection()

    def check_connection(self):
        ################################################################################
        # Search external inside media
        ################################################################################
        try:
            print("Searching for external devices under media...")
            if len(os.listdir(f'{media}/{userName}')) != 0:
                print(f"{media} is Empty")
                self.foundInMedia = True
                self.where(media)
            else:
                for i in range(len(self.captureDevices)):
                    item = self.verticalLayout.itemAt(i)
                    widget = item.widget()
                    widget.deleteLater()
                    i -= 1

        except FileNotFoundError:
            print("No device found inside Media")
            try:
                if len(os.listdir(f'{run}/{userName}')) != 0:
                    self.foundInMedia = False
                    self.where(run)
                else:
                    for i in range(len(self.captureDevices)):
                        item = self.verticalLayout.itemAt(i)
                        widget = item.widget()
                        widget.deleteLater()
                        i -= 1

            except Exception:
                print("No device found inside Run...")
                pass

    def where(self, location):
        # Gettíng devices locations
        if self.foundInMedia:
            self.foundWhere = media
        else:
            self.foundWhere = run

        self.show_on_screen(location)

    def show_on_screen(self, location):
        print("Showing available devices")

        ################################################################################
        # Add buttons and images for each external
        ################################################################################
        # If not already in list, add
        for output in os.listdir(f'{location}/{userName}'):
            if output not in self.captureDevices:
                # If device is in list, display to user just on time per device
                self.captureDevices.append(output)

                # Avaliables external  devices
                self.availableDevices = QPushButton(self.whereFrame)
                self.availableDevices.setFont(QFont('Ubuntu', 12))
                self.availableDevices.setText(output)
                self.availableDevices.setFixedSize(444, 60)
                self.availableDevices.setCheckable(True)
                text = self.availableDevices.text()
                self.availableDevices.clicked.connect(lambda *args, text=text: self.on_device_clicked(text))

                # Image
                image = QLabel(self.availableDevices)
                image.setFixedSize(46, 46)
                image.move(6, 6)
                image.setStyleSheet(
                    "QLabel"
                    "{"
                    f"background-image: url({src_restore_small_icon});"
                    "background-repeat: no-repeat;"
                    "background-position: center;"
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

            # If x device is removed or unmounted, remove from screen
            for output in self.captureDevices:
                if output not in os.listdir(f'{location}/{userName}'):
                    # Current output index
                    index = self.captureDevices.index(output)
                    # Remove from list
                    self.captureDevices.remove(output)             
                    # Delete from screen
                    item = self.verticalLayout.itemAt(index)
                    widget = item.widget()
                    widget.deleteLater()
                    index -= 1

    def on_use_disk_clicked(self):
        ################################################################################
        # Adapt external name is it has space in the name
        ################################################################################
        if " " in self.chooseDevice:
            self.chooseDevice = str(self.chooseDevice.replace(" ", "\ "))

        ################################################################################
        # Update INI file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set(f'EXTERNAL', 'hd', f'{self.foundWhere}/{userName}/{self.chooseDevice}')
            config.set('EXTERNAL', 'name', f'{self.chooseDevice}')
            config.write(configfile)

        self.close()

    def on_device_clicked(self, output):
        if self.availableDevices.isChecked():
            self.chooseDevice = output
            # Enable use disk
            self.useDiskButton.setEnabled(True)
        else:
            self.chooseDevice = ""
            # Disable use disk
            self.useDiskButton.setEnabled(False)

    def on_button_cancel_clicked(self):
        exit()


APP = QApplication(sys.argv)
main = EXTERNAL()
main.show()
APP.exit(APP.exec())