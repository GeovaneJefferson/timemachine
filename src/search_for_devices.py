from setup import *


class EXTERNAL(QWidget):
    def __init__(self):
        super(EXTERNAL, self).__init__()
        self.foundInMedia = None
        self.iniUI()

    def iniUI(self):
        self.setWindowIcon(QIcon(src_restore_icon))
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

        # INI file
        self.iniHDName = config['EXTERNAL']['name']

        self.widgets()

    def widgets(self):
        ################################################################################
        # Frame
        ################################################################################
        self.whereFrame = QFrame()
        self.whereFrame.setFixedSize(440, 280)
        self.whereFrame.move(20, 40)
        self.whereFrame.setStyleSheet("""
            background-color: rgb(48, 49, 50);
        """)

        # Scroll
        self.scroll = QScrollArea(self)
        self.scroll.setFixedSize(460, 280)
        self.scroll.move(20, 40)
        self.scroll.setWidgetResizable(True)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setStyleSheet(
            "QScrollBar::handle"
            "{"
            "background : rgb(58, 59, 60);"
            "}"
            "QScrollBar::handle::pressed"
            "{"
            "background : rgb(68, 69, 70);"
            "}")
        self.scroll.setWidget(self.whereFrame)

        # Vertical layout V
        self.verticalLayout = QVBoxLayout(self.whereFrame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        # Refresh button
        self.refreshButton = QPushButton(self)
        self.refreshButton.setFont(item)
        self.refreshButton.setText("Refresh")
        self.refreshButton.setFixedSize(80, 28)
        self.refreshButton.move(300, 340)
        self.refreshButton.clicked.connect(self.on_button_refresh_clicked)

        # Cancel button
        self.cancelButton = QPushButton(self)
        self.cancelButton.setFont(item)
        self.cancelButton.setText("Cancel")
        self.cancelButton.setFixedSize(80, 28)
        self.cancelButton.move(400, 340)
        self.cancelButton.clicked.connect(self.on_button_cancel_clicked)

        # # Update
        # timer.timeout.connect(self.check_connection_media)
        # timer.start(1000)
        self.check_connection_media()

    def check_connection_media(self):
        print("Searching for external devices under media...")
        ################################################################################
        # Search external inside media
        ################################################################################
        try:
            print((f'{media}/{userName}'))
            os.listdir(f'{media}/{userName}')
            self.foundInMedia = True
            self.show_one_screen(media)

        except FileNotFoundError:
            self.check_connection_run(run)

    def check_connection_run(self):
        print("Searching for external devices under run...")
        ############################################################################# ###
        # Search external inside run/media
        ################################################################################
        try:
            print((f'{run}/{userName}'))
            os.listdir(f'{run}/{userName}')  # Opensuse, external is inside "/run"
            self.foundInMedia = False
            self.show_one_screen(run)

        except FileNotFoundError:
            print("No external devices mounted or available...")
            pass

    def show_one_screen(self, location):
        print("Showing on screen...")
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
            availableDevices = QPushButton(self.whereFrame)
            availableDevices.setFont(QFont('DejaVu Sans', 12))
            availableDevices.setText(output)
            availableDevices.setFixedSize(440, 60)
            availableDevices.setCheckable(True)
            text = availableDevices.text()
            availableDevices.clicked.connect(lambda *args, text=text: self.on_device_clicked(text))
            availableDevices.setStyleSheet(
            "QPushButton"
            "{"
                "background-color: rgb(58, 59, 60);"
                f"background-image: url({src_restore_small_icon});"
                "background-repeat: no-repeat;"
                "background-position: left;"
                "border-radius: 2px;"
                "border: 1px solid gray;"
                "color: white;"
            "}"
            "QPushButton::hover"
            "{"
                "background-color: rgb(68, 69, 70);"
            "}")

            ################################################################################
            # Auto checked this choosed external device
            ################################################################################
            if text == self.iniHDName:
                availableDevices.setChecked(True)

            ################################################################################
            # Add widgets and Layouts
            ################################################################################
            # Vertical layout
            self.verticalLayout.addWidget(availableDevices, 0, QtCore.Qt.AlignHCenter)

    def on_device_clicked(self, get):
        ################################################################################
        # Adapt external name is it has space in the name
        ################################################################################
        if " " in get:
            get = str(get.replace(" ", "\ "))

        print(get)
        print(self.foundWhere)

        ################################################################################
        # Write changes to ini
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set(f'EXTERNAL', 'hd', f'{self.foundWhere}/{userName}/{get}')
            config.set('EXTERNAL', 'name', get)
            config.write(configfile)

        self.close()

    def on_button_refresh_clicked(self):
        sub.Popen(f"python3 {src_search_for_devices}", shell=True)
        exit()

    def on_button_cancel_clicked(self):
        exit()


APP = QApplication(sys.argv)
main = EXTERNAL()
main.show()
APP.exit(APP.exec())
