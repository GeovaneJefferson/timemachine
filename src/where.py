from setup import *

# Configparser
config = configparser.ConfigParser()
config.read(src_user_config)


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        loadUi(src_ui_where, self)
        self.setWindowTitle("External Screen")
        appIcon = QIcon(src_restore_icon)
        self.setWindowIcon(appIcon)
        self.setFixedHeight(325)
        self.setFixedWidth(400)

        # Connections
        self.button_where_cancel.clicked.connect(self.btn_cancel_clicked)
        self.button_where_refresh.clicked.connect(self.btn_refresh_clicked)

        # Add buttons and images for each external
        vertical = 20
        vertical_img = 32
        for self.storage in local_media:
            print(self.storage)
            label_image = QLabel(self)
            pixmap = QPixmap(src_restore_small_icon)
            label_image.setPixmap(pixmap)
            label_image.setFixedSize(48, 48)
            label_image.move(30, vertical_img)
            vertical_img = vertical_img + 50

            button = QPushButton(self.storage, self.where_frame)
            button.setFixedSize(280, 30)
            button.move(60, vertical)
            vertical = vertical + 50
            text = button.text()
            button.show()
            button.clicked.connect(lambda ch, text=text: self.on_button_clicked(text))

    @staticmethod
    def on_button_clicked(choose):
        # Read/Load user.config (backup automatically)
        with open(src_user_config, 'w') as configfile:
            config.set('EXTERNAL', 'hd', '/media/' + user_name + '/' + choose)
            config.set('EXTERNAL', 'name', choose)
            config.write(configfile)
            exit()

    @staticmethod
    def btn_cancel_clicked():
        exit()

    @staticmethod
    def btn_refresh_clicked():
        sub.Popen("python3 " + src_where_py, shell=True)  # Call where py
        exit()


app = QApplication(sys.argv)
main = UI()
main.show()
app.exit(app.exec())
