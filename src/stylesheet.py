# Font
titleFont = "Ubuntu"
titleFontSize = 10
titleFontSizeCompact = 8

temperatureFont = "Ubuntu"
temperatureFontSize = 22
temperatureSmallFontSize = 9

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

widgetStylesheet = ("""
    background-color:rgba(40,40,40,1);
    border-radius:10px;
    border:1px solid rgb(51,51,51);
    """)

weatherWidgetStylesheet = ("""
    background-color:rgb(29,148,255);
    border-radius:10px;
    border:0px solid rgb(51,51,51);
    """)

settingsWidgetStylesheet = ("""
    background-color:rgb(40,40,40);
    border-radius:10px;
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
    "QPushButton:disabled "
        "{"
            "background-color:rgb(255,255,255);"
            "color:rgba(223,222,223,1);"
            "border:0px;"
        "}")

buttonStylesheetDark = (
   "QPushButton"
        "{"
            "border-radius:6px;"
            "background-color:rgb(110,109,112);"
            "border:1px solid rgba(14,14,14,0.2);"
            "color:rgba(223,222,223,1);"
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
            "background-color:rgba(59,135,245,1);"
            "border:1px solid rgba(14,14,14,0.2);"
            "color:white;"
        "}"
    "QPushButton:hover"
        "{"
            "background-color:rgba(245,245,245,1);"
        "}"
    "QPushButton:disabled "
        "{"
            "background-color:rgb(255,255,255);"
            "color:rgba(223,222,223,1);"
            "border:0px;"
        "}")

buttonSystemTrayStylesheet = (
   "QPushButton"
        "{"
            "border:0px;"
            "border-radius:5px;"
        "}"
    "QPushButton:Hover"
        "{"
            "background-color:rgb(128,128,128);"
            "border:0px;"
        "}")

disconnectButtonSystemTrayStylesheet = (
    "QPushButton"
        "{"
            "background-color:rgb(128,128,128);"
            "border-radius:5px;"

        "}"
   "QPushButton:Hover"
        "{"
            "background-color:rgb(222,72,21);"
            "border-radius:5px;"
        "}")

closeButtonStylesheet = (
    "QPushButton"
        "{"
            "border-radius: 8px;"
            "background-color: transparent;"
        "}"
        "QPushButton:hover"
        "{"
            "background-color: transparent;"
        "}")

# WEATHER WIDGETS COLOR
clouds = ("""
    background-color:rgb(208,204,204);
    border-radius:9px;
    border:0px solid rgba(51,51,51,1);
        """)

snow = ("""
    border-radius:9px;
    border:0px solid rgba(230,230,230,1);
        """)

rain = ("""
    background-color:rgba(144,153,161,1);
    border-radius:9px;
    border:0px solid rgb(144,153,161);
        """)

sunny = ("""
    background-color:rgba(242,242,122,1);
    border-radius:9px;
    border:0px solid rgb(144,153,161);
        """)

clear = ("""
    background-color:gray;
    border-radius:9px;
    border:0px solid rgb(51,51,51);
    color:white;
        """)