from pathlib import Path
from setup import *

config = configparser.ConfigParser()
config.read(src_user_config)


class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(app_name)
        # self.setFixedSize(1000, 600)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.showFullScreen()

        self.setStyleSheet("""
            background-color: rgba(30, 30, 30, 150);
        """)

        getResolution = QtWidgets.QDesktopWidget().screenGeometry(0)
        self.screen_x = getResolution.width()  # Screen resolution x
        self.screen_y = getResolution.height()  # Screen resolution y
        self.screen_city = getResolution.center()

        # Variables
        self.filesToRestore = []

        self.home_user = str(Path.home())  # Get home user
        self.user_folders = os.listdir(f"{self.home_user}/")
        self.copyCmd = "rsync -avruzh"
        self.count = 0
        self.downClicked = False
        self.alreadyAddedListLayoutWidget = False

        # Fonts
        self.font1 = "DejaVu Sherif"
        self.font2 = "Arial Black"
        self.font3 = "Monospace"
        self.font4 = "Noto Sans Cond Blk"

        # Read ini
        self.getHDName = config['EXTERNAL']['name']
        self.getExternalLocation = config['EXTERNAL']['hd']

        # Read restoreSttings
        with open('restoreSettings.txt', 'r') as self.reader:
            self.reader = self.reader.readline()
            self.reader = self.reader.replace(':', '').strip()
            print(f"Search files from : {self.reader}")

        self.widgets()

    def widgets(self):
        ################################################################################
        ## Base layouts
        ################################################################################
        self.baseVLayout = QVBoxLayout(self)
        self.baseVLayout.setContentsMargins(20, 20, 20, 20)

        self.baseHLayout = QHBoxLayout()
        # self.baseHLayout.setSpacing(20)

        self.buttonHLayout = QHBoxLayout()
        self.buttonHLayout.setSpacing(20)
        self.buttonHLayout.setContentsMargins(20, 20, 20, 20)

        ################################################################################
        ## Vertical layout
        ################################################################################
        self.verticalLayout = QVBoxLayout() 
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        ################################################################################
        ## ScrollArea
        ################################################################################
        widget = QWidget()
        widget.setFixedSize(1920, 1080)
        widget.setStyleSheet("""
            background-color: rgba(30, 30, 30, 150);
        """)

        # scrollWidget = QWidget(widget)
        # scrollWidget.setMaximumSize(900, 600)
        # scrollWidget.setStyleSheet("""
        #     background-color: rgb(24, 25, 26);
        # """)

        # scroll = QScrollArea(scrollWidget) 
        # scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # scroll.setWidgetResizable(True)
        # scroll.setStyleSheet( 
        #     "QScrollBar::handle"
        #         "{"
        #             "background : rgb(58, 59, 60);"
        #         "}"
        #     "QScrollBar::handle::pressed"
        #         "{"
        #             "background : rgb(68, 69, 70);"
        #         "}"
        #     )
        # croll.setWidget(scrollWidget)
        
        ################################################################################
        ## Vertical layout
        ################################################################################
        self.filesLayout = QVBoxLayout()
        self.filesLayout.setContentsMargins(20, 20, 20, 20)
        self.filesLayout.setSpacing(20)
        
        ################################################################################
        ## Cancel button 
        ################################################################################
        self.cancelButton = QPushButton()
        self.cancelButton.setText("Cancel")
        self.cancelButton.setFont(QFont(self.font4, 14))
        self.cancelButton.setFixedSize(120, 34)
        self.cancelButton.setStyleSheet(
            "QPushButton"
                "{"
                    "background-color: rgb(58, 59, 60);"
                    "border: 0px;"
                    "border-radius: 5px;"
                "}"
            "QPushButton::hover"
                "{"
                    "background-color: rgb(68, 69, 70);"
                "}"
        )
        self.cancelButton.setEnabled(True)
        self.cancelButton.clicked.connect(lambda x: exit())

        ################################################################################
        ## Restore button 
        ################################################################################
        self.restoreButton = QPushButton()
        self.restoreButton.setText("Restore")
        self.restoreButton.setFont(QFont(self.font4, 14))
        self.restoreButton.setFixedSize(120, 34)
        self.restoreButton.setStyleSheet(
            "QPushButton"
                "{"
                    "background-color: rgb(58, 59, 60);"
                    "border: 0px;"
                    "border-radius: 5px;"
                "}"
            "QPushButton::hover"
                "{"
                    "background-color: rgb(68, 69, 70);"
                "}"
        )
        self.restoreButton.setEnabled(False)
        
        ################################################################################
        ## Up button 
        ################################################################################
        self.upButton = QPushButton()
        self.upButton.setText("Up")
        self.upButton.setFont(QFont(self.font4, 10))
        self.upButton.setFixedSize(40, 40)
        self.upButton.setStyleSheet(
            "QPushButton"
                "{"
                    "background-color: rgb(58, 59, 60);"
                    "border: 0px;"
                    "border-radius: 5px;"
                "}"      
            "QPushButton::hover"
                "{"
                    "background-color: rgb(68, 69, 70);"
                "}"
            )
          
        ################################################################################
        ## Down button 
        ################################################################################
        self.downButton = QPushButton()
        self.downButton.setText("Down")
        self.downButton.setFont(QFont(self.font4, 10))
        self.downButton.setFixedSize(40, 40)     
        self.downButton.setStyleSheet(
            "QPushButton"
                "{"
                    "background-color: rgb(58, 59, 60);"
                    "border: 0px;"
                    "border-radius: 5px;"
                "}"      
            "QPushButton::hover"
                "{"
                    "background-color: rgb(68, 69, 70);"
                "}"
            )   
        self.downButton.clicked.connect(lambda x: self.get_date())
          
        ################################################################################
        ## Label date 
        ################################################################################
        self.labelDate = QLabel()
        self.labelDate.setFont(QFont(self.font2, 12))

        frame = QFrame(widget)
        frame.setFixedSize(900, 500)
        frame.setStyleSheet("""
            background-image: url("/home/geovane/Dropbox/python/timemachine/src/icons/folder.png")
        """)
   
        ################################################################################
        ## Add widgets and Layouts
        ################################################################################
        # self.baseHLayout.addWidget(scroll)
        self.baseHLayout.addWidget(frame, 1, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.upButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)  
        self.verticalLayout.addWidget(self.labelDate, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)  
        self.verticalLayout.addWidget(self.downButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)  
        self.verticalLayout.addStretch()
        
        self.buttonHLayout.addWidget(self.cancelButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)  
        self.buttonHLayout.addWidget(self.restoreButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)  
        
        self.baseVLayout.addLayout(self.baseHLayout, QtCore.Qt.AlignHCenter)
        self.baseVLayout.addLayout(self.buttonHLayout, QtCore.Qt.AlignVCenter)
        self.baseVLayout.addStretch()
        
        self.baseHLayout.addLayout(self.verticalLayout)

        self.get_date()

    def get_date(self):
        # count = self.filesLayout.count()
        # print("COUNT :", count)
        # for _ in range(count):
        #     item = self.filesLayout.itemAt(count - 1)
        #     widget = item.widget()
        #     widget.deleteLater()
            
        ################################################################################
        ## Get available dates inside TMB
        ################################################################################
        dateFolders = []
        for output in os.listdir(f"{self.getExternalLocation}/TMB/"):
            dateFolders.append(output)
            dateFolders.sort(reverse=True)

        getDate = dateFolders[self.count]
        self.count += 1
        ################################################################################
        ## Set current folder date
        ################################################################################
        self.labelDate.setText(getDate)

        self.get_files(getDate)

    def get_files(self, getDate):
        ################################################################################
        ## Get available times inside TMB
        ################################################################################
        timeFolders = []
        for output in os.listdir(f"{self.getExternalLocation}/TMB/{getDate}/"):
            timeFolders.append(output)
            timeFolders.sort(reverse=True)
            # output = output.replace("-", ":")   # Change - to :
            # output = output.replace(":", "-")   # Change back : to - 

        self.show_on_screen(getDate, timeFolders[0])

    def show_on_screen(self, getDate, getTime):
        ################################################################################
        ## Show available files
        ################################################################################
        for output in os.listdir(f"{self.getExternalLocation}/TMB/{getDate}/{getTime}/{self.reader}"):
            if "." in output and not output.startswith("."):
                print("Output: ", output)

                self.buttonFiles =  QPushButton(self)
                self.buttonFiles.setCheckable(True)
                self.buttonFiles.setFixedSize(640, 60)
                self.buttonFiles.setStyleSheet(
                "QPushButton"
                    "{"
                        "background-color: rgb(36, 37, 38);"
                        "border: 0px;"
                        "border-radius: 5px;"
                    "}"      
                "QPushButton::hover"
                    "{"
                        "background-color: rgb(58, 59, 60);"
                    "}"
                "QPushButton::checked"
                    "{"
                        "background-color: rgb(24, 25, 26);"
                        "border: 1px solid white;"
                    "}"
                )
                self.buttonFiles.clicked.connect(lambda x, output=output: self.add_to_restore(output, getDate, getTime))

                ################################################################################
                ## Preview
                ################################################################################
                # image = QLabel(self.buttonFiles)
                # pixmap = QPixmap(f"{self.getExternalLocation}/TMB/{getDate}/{getTime}/{self.reader}/{output}")
                # pixmap = pixmap.scaled(128, 128, QtCore.Qt.KeepAspectRatio)
                # image.setPixmap(pixmap)

                # # Output preview
                # image = QLabel(self.buttonFiles)
                # image.setAlignment(QtCore.Qt.AlignHCenter)
                # pixmap = QPixmap("icons/folder.png")
                # pixmap = pixmap.scaled(64, 64, QtCore.Qt.KeepAspectRatio)
                # image.move(40, 40)
                # image.setStyleSheet("""
                #     background-color: transparent;
                # """)

                ################################################################################
                ## Text
                ################################################################################
                text = QLabel(self.buttonFiles)
                text.setText(output.capitalize())
                text.setFont(QFont(self.font2, 8))
                text.move(20, 10)
                text.setStyleSheet("""
                    color: white;
                    border: 0px;
                    background-color: transparent;
                                    """)
                
                ################################################################################
                ## Add layout and widgets
                ################################################################################
                self.filesLayout.addWidget(self.buttonFiles)

    def add_to_restore(self, output, getDate, getTime):
        ################################################################################
        ## Add to the list
        ################################################################################
        if not output in self.filesToRestore:  # Check if output is already inside list
            self.filesToRestore.append(output)  # Add output to the list files to restore 
        else:  
            self.filesToRestore.remove(output) # Remove item if already in list
        
        ################################################################################
        ## Enable restore button
        ################################################################################ 
        if len(self.filesToRestore) >= 1:
            self.restoreButton.setEnabled(True)
        else:
            self.restoreButton.setEnabled(False)
        
        ################################################################################
        ## Connection restore button
        ################################################################################ 
        self.restoreButton.clicked.connect(lambda x: self.start_restore(getDate, getTime))  

    def start_restore(self, getDate, getTime):
        config = configparser.ConfigParser()
        config.read(src_user_config)

        try:
            count = 0
            for _ in self.filesToRestore:
                sub.run(f"{self.copyCmd} {self.getExternalLocation}/TMB/{getDate}/{getTime}/{self.reader}/{self.filesToRestore[count]} {home_user}/{self.reader}/", shell=True)
                count += 1
        except:
            failed_restore()  # Notification

        complete_restore()  # Notification
        exit()

    def keyPressEvent(self, event):
        if event.key():  # == Qt.Key_Esc
            exit()


app = QApplication(sys.argv)
main = UI()
main.show()
app.exit(app.exec())
