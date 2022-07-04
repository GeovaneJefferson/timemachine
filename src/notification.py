#! /usr/bin/python3
from setup import *

# QTimer
timer = QtCore.QTimer()

# Read ini file
config = configparser.ConfigParser()
config.read(src_user_config)


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.read_ini_file()

    def read_ini_file(self):
        # Read INI file
        self.iniNotificationAddInfo = config['INFO']['notification_add_info']

        self.iniUI()

    def iniUI(self):
        # Window size
        self.setFixedSize(260, 260)
        # Window dimensions
        screen = app.primaryScreen()
        rect = screen.availableGeometry()
        self.x = (rect.width())
        self.y = (rect.height())

        # Window position TOP
        self.windowXPosition = self.x - 240
        self.windowYPosition = 40

        # Window position Bottom
        # self.windowXPosition = self.x - 240
        # self.windowYPosition = self.y - 270

        # Window manager dimensions
        self.move(self.windowXPosition, self.windowYPosition)

        # Other settings
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.widget()

    def widget(self):
        self.widget = QWidget(self)
        self.widget.setFixedSize(240, 260)
        self.widget.setStyleSheet(
            "QWidget"
            "{"
            "background-color: rgb(250, 250, 250);" # White color rgb(255, 255, 255) # Black color rgb(40, 40, 40)
            "border-radius: 15px;"
            "}")

        # creating a blur effect
        # self.blur_effect = QGraphicsBlurEffect()
        # self.blur_effect.setBlurRadius(5)
        # self.widget.setGraphicsEffect(self.blur_effect)

        # Vertical layout
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(0)

        #################################################################
        ###  Title text
        #################################################################
        self.titleLabel = QLabel()
        self.titleLabel.setText(appName)
        self.titleLabel.setFont(QFont("Ubuntu, Light", 14))
        self.titleLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.titleLabel.setFixedSize(120, 30)
        self.titleLabel.setStyleSheet("""
            color: rgb(0, 0, 0);
            background-color: transparent;
            border: transparent;
        """)    # 65,65,65

        #################################################################
        ###  Image inside the notification
        #################################################################
        self.image = QLabel()
        self.image.setFixedSize(128, 128)
        self.image.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.image.setStyleSheet(f"""
            background-image: url({src_backup_icon});
            background-repeat: no-repeat;
            border: 0px;
        """)

        ################################################################
        ##  Message text
        ################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        # Read messageID from INI file
        self.messageID = config['INFO']['notification_id']

        # Message label
        self.messageText = QLabel()
        self.messageText.setFont(QFont("Ubuntu", 10))
        self.messageText.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.messageText.adjustSize()
        self.messageText.setStyleSheet("""
            color: rgb(0, 0, 0);
            background-color: transparent;
            border: transparent;
        """)    # 55,55,55

        self.notification_id()

    def notification_id(self):
        ################################################################
        ##  Back up will start shortly
        ################################################################
        if self.messageID == "0":
            self.messageText.setText("All settings was reset!")
            self.messageText.setAlignment(QtCore.Qt.AlignHCenter)
        elif self.messageID == "1":
            self.messageText.setText("Back up will start shortly...")
            self.messageText.setAlignment(QtCore.Qt.AlignHCenter)
        elif self.messageID == "2":
            self.messageText.setText("Backup is done!")
            self.messageText.setAlignment(QtCore.Qt.AlignHCenter)
        elif self.messageID == "3":
            self.messageText.setText("External not mounted or available...")
            self.messageText.setAlignment(QtCore.Qt.AlignHCenter)
        elif self.messageID == "4":
            self.messageText.setText("Error trying to back up!")
            self.messageText.setAlignment(QtCore.Qt.AlignHCenter)
        elif self.messageID == "5":
            self.messageText.setText("Error trying to read INI file!")
            self.messageText.setAlignment(QtCore.Qt.AlignHCenter)
        elif self.messageID == "6":
            self.messageText.setText("Error trying to delete old backups!")
            self.messageText.setAlignment(QtCore.Qt.AlignHCenter)
        elif self.messageID == "7":
            self.messageText.setText("Please, manual delete old backups!")
            self.messageText.setAlignment(QtCore.Qt.AlignHCenter)
        elif self.messageID == "8":
            self.messageText.setText("Your files are been restored...")
            self.messageText.setAlignment(QtCore.Qt.AlignHCenter)
        elif self.messageID == "9":
            self.messageText.setText("Error trying to restore your files!")
            self.messageText.setAlignment(QtCore.Qt.AlignHCenter)
        elif self.messageID == "10":
            self.messageText.setText("Not enough space to backup!\n"
                f"{self.iniNotificationAddInfo}")
            self.messageText.setAlignment(QtCore.Qt.AlignHCenter)
            
        else:
            pass

        #################################################################
        ###  Ok button
        #################################################################
        self.okButton = QPushButton()
        self.okButton.setText("Close")
        self.okButton.setFont(QFont("Ubuntu", 11))
        self.okButton.setFixedSize(200, 34)
        self.okButton.clicked.connect(self.end_animation)
        self.okButton.setStyleSheet(
            "QPushButton"
            "{"
            "color: white;"
            "background-color: rgba(41, 147, 247, 1);"
            "border-radius: 10px;"
            "border: 0px"
            "}"
            "QPushButton:hover"
            "{"
            "background-color: rgba(162, 167, 175, 1);"
            "}")

        ################################################################################
        # Add widgets and Layouts
        ################################################################################
        self.verticalLayout.addWidget(self.titleLabel, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.verticalLayout.addWidget(self.image, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.verticalLayout.addWidget(self.messageText, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.verticalLayout.addWidget(self.okButton, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.setLayout(self.verticalLayout)

        self.start_animation()

    def start_animation(self):
        #################################################################
        ###  Start animation
        #################################################################
        self.startAnimation = QPropertyAnimation(self.widget, b"geometry")
        self.startAnimation.setDuration(1000)
        self.startAnimation.setStartValue(QRect(self.x, 0, 0, 0))
        # How far the widget will go from "outside to inside"
        self.startAnimation.setEndValue(QRect(10, 0, 0, 0))
        self.startAnimation.setEasingCurve(QEasingCurve.OutCirc)
        self.startAnimation.start()

        timer.timeout.connect(self.end_animation)
        timer.start(5000)

    def end_animation(self):
        self.move(self.x, self.windowYPosition)

        #################################################################
        ###  End animation
        #################################################################
        self.endAnimation = QPropertyAnimation(self.widget, b"geometry")
        self.endAnimation.setDuration(1000)
        # Push widget to the righ, far from the screen
        self.endAnimation.setEndValue(QRect(260, 0, 0, 0))
        self.endAnimation.setEasingCurve(QEasingCurve.OutCirc)
        self.endAnimation.start()

        timer.timeout.connect(lambda *args: exit())
        timer.start(1000)


app = QApplication(sys.argv)
main = UI()
main.show()
app.exit(app.exec())
