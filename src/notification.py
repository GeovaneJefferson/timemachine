from setup import *


# QTimer
timer = QtCore.QTimer()


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.setFixedSize(260, 260)

        screen = app.primaryScreen()
        rect = screen.availableGeometry()
        self.x = (rect.width())
        self.y = (rect.height())

        self.move((self.x - 260), (self.y - 280))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.widget()

    def widget(self):
        self.widget = QWidget(self)
        self.widget.setFixedSize(240, 260)
        self.widget.setStyleSheet(
            "QWidget"
            "{"
            "background-color: rgb(0, 0, 0);" # White color rgb(255, 255, 255) # Black color rgb(40, 40, 40)
            "border-radius: 10px;"
            "border: 1px solid rgb(40, 40, 40);" # 200,200,200
            "}")

        # creating a blur effect
        # self.blur_effect = QGraphicsBlurEffect()
        # self.blur_effect.setBlurRadius(5)
        # self.widget.setGraphicsEffect(self.blur_effect)

        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 10, 0, 10)

        #################################################################
        ###  Title text
        #################################################################
        titleText = QLabel()
        titleText.setText(appName)
        titleText.setFont(QFont("Ubuntu, Light", 14))
        titleText.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        titleText.setFixedSize(120, 30)
        titleText.setStyleSheet("""
            color: rgb(255, 255, 255);
            background-color: transparent;
            border: transparent;
        """)    # 65,65,65

        #################################################################
        ###  Main image
        #################################################################
        image = QLabel()
        image.setFixedSize(130, 130)
        image.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        image.setStyleSheet(f"""
            background-image: url({src_backup_icon});
            background-repeat: no-repeat;
            border: 0px;
        """)

        ################################################################
        ##  Message text
        ################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)

        # INI file
        messageID = config['INFO']['notification_id']
        
        self.messageText = QLabel()
        ################################################################
        ##  Back up will start shortly
        ################################################################
        if messageID == "0":
            self.messageText.setText("All settings was reset!") 
        
        elif messageID == "1":
            self.messageText.setText("Back up will start shortly...")

        elif messageID == "2":
            self.messageText.setText("Backup is done!")

        elif messageID == "3":
            self.messageText.setText("External not mounted or available...")

        elif messageID == "4":
            self.messageText.setText("Error trying to back up!")

        elif messageID == "5":
            self.messageText.setText("Error trying to read INI file!")

        elif messageID == "6":
            self.messageText.setText("Error trying to delete old backups!")

        elif messageID == "7":
            self.messageText.setText("Please, manual delete old backups!")

        elif messageID == "8":
            self.messageText.setText("Please, choose an external device first!")

        elif messageID == "9":
            self.messageText.setText("Your files are been restored...")

        elif messageID == "10":
            self.messageText.setText("Error trying to restore your files!")

        else:
            pass

        self.messageText.setFont(QFont("Ubuntu, Light", 9))
        self.messageText.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.messageText.setFixedSize(220, 30)
        self.messageText.setStyleSheet("""
            color: rgb(255, 255, 255);
            background-color: transparent;
            border: transparent;
        """)    # 55,55,55

        #################################################################
        ###  Ok button
        #################################################################
        self.okButton = QPushButton()
        self.okButton.setText("Close")
        self.okButton.setFont(QFont("Ubuntu", 9))
        self.okButton.setFixedSize(200, 32)
        self.okButton.clicked.connect(self.end_animation)
        self.okButton.setStyleSheet(
            "QPushButton"
            "{"
            "color: white;"
            "background-color: rgba(20, 110, 255, 1);"
            "border-radius: 5px;"
            "border: 0px"
            "}"
            "QPushButton:hover"
            "{"
            "background-color: rgba(162, 167, 175, 1);"
            "}")

        self.verticalLayout.addWidget(titleText, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.verticalLayout.addWidget(image, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.verticalLayout.addWidget(self.messageText, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.verticalLayout.addWidget(self.okButton, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.setLayout(self.verticalLayout)

        self.start_animation()

    def start_animation(self):
        #################################################################
        ###  Start animation
        #################################################################
        self.anim = QPropertyAnimation(self.widget, b"geometry")
        self.anim.setDuration(1000)
        self.anim.setStartValue(QRect(self.x, 0, 0, 0))
        self.anim.setEndValue(QRect(0, 0, 0, 0))
        self.anim.setEasingCurve(QEasingCurve.OutCirc)
        self.anim.start()

        timer.timeout.connect(self.end_animation)
        timer.start(5000)

    def end_animation(self):
        self.move(self.x, (self.y - 280))

        #################################################################
        ###  End animation
        #################################################################
        self.endAnimation = QPropertyAnimation(self.widget, b"geometry")
        self.endAnimation.setDuration(1000)
        self.endAnimation.setEndValue(QRect(260, 0, 0, 0))
        self.endAnimation.setEasingCurve(QEasingCurve.OutCirc)
        self.endAnimation.start()

        timer.timeout.connect(lambda *args: exit())
        timer.start(1000)


app = QApplication(sys.argv)
main = UI()
main.show()
app.exit(app.exec())
