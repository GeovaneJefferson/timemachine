from email.mime import base
from re import search
from setup import *


class UI(QWidget):
    def __init__(self):
        super().__init__()
        # Screen settings
        get_resolution = QtWidgets.QDesktopWidget().screenGeometry(0)
        self.screen_x = get_resolution.width()  # Screen resolution x
        self.screen_y = get_resolution.height() # Screen resolution y

        # Variables
        self.home_user = str(Path.home())  # Get home user
        self.user_folders = os.listdir(self.home_user + "/")

        # Fonts
        self.font1 = "DejaVu Sherif"
        self.font2 = "Arial Black"
        self.font3 = "Monospace"
        self.font4 = "Noto Sans Cond Blk"

        self.widgets()

    def widgets(self):
        # Layouts
        # Base layout
        self.baseLayout = QHBoxLayout()
        self.baseLayout.setAlignment(QtCore.Qt.AlignCenter)

        # Grid layout
        self.gridLayout = QGridLayout()
        self.gridLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(10)

        # Vertical layout
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.setSpacing(10)  # Spacing between up and down

        # Buttons
        # Button up date
        self.btn_up_date = QPushButton()
        self.btn_up_date.setText("Up")
        self.btn_up_date.setFixedSize(50, 50)      

        # Button down date
        self.btn_down_date = QPushButton(self)
        self.btn_down_date.setText("Down")
        self.btn_down_date.setFixedSize(50, 50)  
        self.btn_down_date.move(int(1800), int(self.screen_y - 50))

        # Add to layout
        self.baseLayout.addLayout(self.gridLayout, 0)
        self.baseLayout.addLayout(self.verticalLayout, 0)

        # Set layouts
        self.setLayout(self.baseLayout)

        self.cli()

    def cli(self):
        # # Frame
        # verticalPosition = 3.5
        # horizontalPosition = 3.5
        # sizeBack = 750
        
        # for _ in range(2):
        #     self.frameBack = QFrame(self)
        #     self.frameBack.setGeometry(int(self.screen_x / horizontalPosition), int(self.screen_y / verticalPosition), sizeBack, 500)
        #     self.frameBack.setStyleSheet("""
        #         background-color: rgb(30, 30, 30);
        #         border-radius: 15px;
        #         border : 2px solid black;
        #                         """)
        #     verticalPosition += .5
        #     horizontalPosition -= .2
        #     sizeBack -= 50

        self.frameFront = QFrame(self)
        self.frameFront.setGeometry(int(self.screen_x / self.screen_x + 299), int(self.screen_y / self.screen_y + 219), self.screen_x - 600, self.screen_y - 400)
        self.frameFront.setStyleSheet("""
            background-color: rgb(30, 30, 30);
            border-radius: 15px;
            border : 2px solid black;

                            """)

        # Show results
        count = int()
        vert = int()
        for show_folders in os.listdir("/home/geovane/Dropbox"):
            if not show_folders.startswith("."):
                print(show_folders)
                # Folders result
                button = QPushButton(self.frameFront)
                # button.setText(show_folders)
                button.setFixedSize(128, 128)
                if show_folders.endswith(".mp4"):
                    button.setIcon(QIcon("icons/mp4.png"))
                elif show_folders.endswith(".jpeg"):
                    button.setIcon(QIcon("icons/jpeg.png"))
                else:
                    button.setIcon(QIcon("icons/folder.png"))
                
                button.setIconSize(QSize(128, 128))
                button.setStyleSheet("""
                    color: white;
                    border-radius: 15px;
                                                """)
                button.clicked.connect(lambda ch, sendResult=show_folders: print("You clicked on", sendResult))
                # button.clicked.connect(self.delete_all)  # Close if clicked on

                self.gridLayout.addWidget(button, vert, count)

                count += 1
                if count % 5 == 0:
                    vert += 1
                    count = 0

                # Title of the folders
                title = QLabel(button)
                title.setText(show_folders.capitalize())
                title.move(10,100)
                title.setFont(QFont(self.font4, 10))
                title.setStyleSheet("""
                    color: white;
                    border : 0px;
                                    """)
                title = title.text()

    def keyPressEvent(self, event):
        if event.key():  # == Qt.Key_Esc
            exit()

            
app = QApplication(sys.argv)
main = UI()
main.show()
main.showFullScreen()
app.exit(app.exec())
                                    