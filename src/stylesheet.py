from setup import *
# Button
buttonHeightSize = 24
buttonFontSize = QFont(mainFont,10)

# Migration Assistant
migrationAssistantTitle = QFont(mainFont,28)

# Font
mainFont = "Ubuntu"

titleFont = "Ubuntu"
titleFontSize = 10
titleFontSizeCompact = 8

temperatureFont = "Ubuntu"
temperatureFontSize = 22
temperatureSmallFontSize = 9

fontSize11px = QFont(mainFont,11)
fontSize24px = QFont(mainFont,24)



newsFont = "Ubuntu"
newsFontSize = 10

boldText = ("""
        font-weight: bold;
        border:transparent;
        background-color:transparent;
        color:white;
        """)

boldTextBlack = ("""
        font-weight: bold;
        border:transparent;
        background-color:transparent;
        color:black;
        """)

newsBoldText = ("""
        color:rgb(247,63,95);
        font-weight: bold;
        border:transparent;
        background-color:transparent;
        """)

normalText = ("""
        border:transparent;
        background-color:transparent;
        color:white;
        """)

whiteBox = ("""
        background-color:white;
        color:black;
        border:0px;
        """)

separetorLine = ("""
        border-top:1px solid rgba(14,14,14,0.1);
        """)

timeBox = (
    """
        border-color: transparent;
        border:1px solid rgba(14,14,14,0.2);
        border-radius:4px;
    """)
 

buttonStylesheet = (
   "QPushButton"
        "{"
            "border-radius:6px;"
            "background-color:rgb(255,255,255);"
            "border:1px solid rgba(14,14,14,0.2);"
            "color:black;"
        "}"
    "QPushButton:hover"
        "{"
            "background-color:rgba(245,245,245,1);"
        "}"
    "QPushButton:disabled"
        "{"
            "background-color:rgb(255,255,255);"
            "color:rgba(223,222,223,1);"
            "border:0px;"
        "}"
    "QPushButton:checked"
        "{"
            "background-color:rgba(213,213,213,1);"
        "}")

buttonStylesheetDark = (
   "QPushButton"
        "{"
            "border-radius:6px;"
            "background-color:rgba(110, 109, 112, 1);"
            "border:1px solid rgba(14,14,14,0.2);"
            "color:rgba(223, 222, 223, 1);"
        "}"
    "QPushButton:hover"
        "{"
            "background-color:rgba(76,75,78,1);"
        "}"
    "QPushButton:disabled "
        "{"
            "background-color:rgb(255,255,255);"
            "color:rgba(223,222,223,1);"
            "border:0px;"
        "}")

useDiskButtonStylesheet = (
   "QPushButton"
        "{"
            "border-radius:6px;"
            "background-color:rgba(21, 100, 220, 1);"
            "border:1px solid rgba(14,14,14,0.2);"
            "color:rgba(225, 234, 248, 1);"
        "}"
    "QPushButton:hover"
        "{"
            # "background-color:rgba(245,245,245,1);"
            "color:rgba(223,222,223,1);"
        "}"
    "QPushButton:disabled "
        "{"
            "background-color:rgb(255,255,255);"
            "color:rgba(223,222,223,1);"
            "border:0px;"
        "}")

availableDeviceButtonStylesheet  = (
   "QPushButton"
        "{"
            "border-radius:6px;"
            "background-color:rgb(255,255,255);"
            "border:1px solid rgba(14,14,14,0.2);"
            "color:black;"
            "padding-left:45px;"
            "text-align:left;"
        "}"
    "QPushButton:hover"
        "{"
            "background-color:rgba(245,245,245,1);"
        "}"
    "QPushButton:disabled"
        "{"
            "background-color:rgb(255,255,255);"
            "color:rgba(223,222,223,1);"
            "border:0px;"
        "}"
    "QPushButton:checked"
        "{"
            "background-color:rgba(213,213,213,1);"
        "}")

externalWindowbackground =( 
        "QWidget"
            "{"
                "background-color:white;"
            "}")


# WEATHER WIDGETS COLOR
clouds = ("""
    background-color:rgb(208,204,204);
    border-radius:9px;
    border:0px solid rgba(51,51,51,1);
        """)

transparentBackground = ("""
    background-color:0px;
    border-radius:0px;
    border:0px solid rgba(51,51,51,1);
        """)

if __name__ == '__main__':
    pass