from setup import *

# Font
MAIN_FONT="Ubuntu"
titleFontSize=10
titleFontSizeCompact=8

temperatureFont="Ubuntu"
temperatureFontSize=22
temperatureSmallFontSize=9

# Button
BUTTONHEIGHT_SIZE=24
BUTTON_FONT_SIZE=10

# Migration Assistant
MIGRATION_ASSISTANT_TITLE=28

FONT_SIZE_11PX=11
fontSize24px=24

boldText=("""
        font-weight: bold;
        border:transparent;
        background-color:transparent;
        color:white;
        """)

boldTextBlack=("""
        font-weight: bold;
        border:transparent;
        background-color:transparent;
        color:black;
        """)

newsBoldText=("""
        color:rgb(247,63,95);
        font-weight: bold;
        border:transparent;
        background-color:transparent;
        """)

normalText=("""
        border:transparent;
        background-color:transparent;
        color:white;
        """)

applicationBackgroundBox=("""
        background-color:white;
        color:black;
        border:0px;
        """)

applicationBackgroundBoxDark=("""
        background-color:red;
        border-right:1px solid rgba(14,14,14,0.1);
        """)

separetorLine=("""
        border-top:1px solid rgba(14,14,14,0.1);
        """)

separetorLineDark=("""
        border-top:1px solid rgba(110, 109, 112, 1);
        """)

separetorLineLeftbackground=("""
        border-right:1px solid rgba(14,14,14,0.1);
        """)

separetorLineLeftbackgroundDark=("""
        border-right:1px solid rgba(110, 109, 112, 1);
        """)

timeBox=(
    """
        border-color: transparent;
        border:1px solid rgba(14,14,14,0.2);
        border-radius:4px;
    """)
 
leftBackgroundColorStylesheet=(
    """
        background-color:rgba(240, 241, 243, 1);
        border-right:1px solid rgba(14,14,14,0.1);
    """)

leftBackgroundColorStylesheetDark=(
    """
        background-color:rgba(45, 45, 45, 1);
        border-right:1px solid rgba(14,14,14,0.1);
    """)

buttonStylesheet=(
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

buttonStylesheetDark=(
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
            "background-color:rgba(69, 69, 70, 1);"
            "color:rgba(99, 99, 99, 1);"
        "}")

useDiskButtonStylesheet=(
   "QPushButton"
        "{"
            "border-radius:6px;"
            "background-color:rgba(75,145,247,1);"
            "border:1px solid rgba(14,14,14,0.2);"
            "color:rgba(255, 255, 255, 1);"
        "}"
    "QPushButton:hover"
        "{"
            "background-color:rgba(76,75,78,1);"
            "color:rgba(255, 255, 255,1);"
        "}"
    "QPushButton:disabled "
        "{"
            "background-color:rgb(255,255,255);"
            "color:rgba(223,222,223,1);"
            "border:0px;"
        "}")

availableDeviceButtonStylesheet =(
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

availableDeviceButtonStylesheetDark =(
   "QPushButton"
        "{"
            "border-radius:6px;"
            "background-color:rgba(110, 109, 112, 1);"
            "border:1px solid rgba(14,14,14,0.2);"
            "color:white;"
            "padding-left:45px;"
            "text-align:left;"
        "}"
    "QPushButton:hover"
        "{"
            "background-color:rgba(76,75,78,1);"
        "}"
    "QPushButton:disabled"
        "{"
            "background-color:rgb(255,255,255);"
            "color:rgba(223,222,223,1);"
            "border:0px;"
        "}"
    "QPushButton:checked"
        "{"
            "background-color:rgba(37, 37, 37, 1);"
            "border:1px solid rgba(98, 98, 98, 1);"
        "}")

externalWindowbackgroundStylesheet =( 
        "QWidget"
            "{"
                "background-color:white;"
                "border:1px solid rgba(14,14,14,0.1);"
                "border-radius: 8px;"
            "}")

externalWindowbackgroundStylesheetDark =( 
        "QWidget"
            "{"
                "background-color:rgba(69, 69, 70, 1);"
                "border:1px solid rgba(14,14,14,0.1);"
                "border-radius: 8px;"
                "color:white;"
            "}")

# WEATHER WIDGETS COLOR
clouds=("""
    background-color:rgb(208,204,204);
    border-radius:9px;
    border:0px solid rgba(51,51,51,1);
        """)

transparentBackground=("""
    background-color:0px;
    border-radius:0px;
    border:0px solid rgba(51,51,51,1);
        """)

