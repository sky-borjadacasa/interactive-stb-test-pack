#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contants for MySky testing
"""

from stbt import Region

# Misc:
MY_SKY_OPEN_TIMEOUT = 25

# Regions:
MY_SKY_REGION = Region(880, 0, width=400, height=720) # The 400 pixels to the right and the whole height of the screen
MY_SKY_MOVING_BALLS_REGION = Region(1100, 0, width=180, height=100)
MY_SKY_GREETING_REGION = Region(930, 90, width=300, height=45)
MAIN_MENU_LOADING_REGION = Region(1015, 280, width=140, height=50)
MAIN_MENU_ITEM_1_REGION = Region(930, 135, width=300, height=150)
MAIN_MENU_ITEM_2_REGION = Region(930, 295, width=300, height=130)
MAIN_MENU_ITEM_3_REGION = Region(930, 435, width=300, height=130)

TRAFFIC_LIGHTS_REGION = Region(29, 21, width=20, height=33)

# TODO: Check if used:
WEATHER_CITY_NAME_REGION = Region(930, 590, width=200, height=45)
WEATHER_ICON_REGION = Region(1100, 625, width=70, height=55)
WEATHER_TEMP_REGION = Region(930, 630, width=115, height=60)
WEATHER_TEMP_MAX_REGION = Region(1180, 630, width=55, height=30)
WEATHER_TEMP_MIN_REGION = Region(1180, 660, width=55, height=30)

# Manage Your Account Regions:
MYA_TITLE_REGION = Region(950, 90, width=300, height=35)
MYA_MENU_ITEM_1_REGION = Region(930, 135, width=300, height=130)
MYA_MENU_ITEM_2_REGION = Region(930, 275, width=300, height=130)
MYA_MENU_ITEM_3_REGION = Region(930, 415, width=300, height=130)
MYA_MENU_ITEM_4_REGION = Region(930, 555, width=300, height=130)

# TODO: Check if used:
SKY_Q_NEXT_GENERATION = Region(940, 115, width=285, height=30)
SKY_Q_LONG_TEXT = Region(900, 435, width=350, height=140)

# Secret Scene Regions:
SECRET_SCENE_TITLE_REGION = Region(970, 120, width=230, height=40)
SS_MAIN_ITEM_1_REGION = Region(940, 425, width=280, height=40)
SS_MAIN_ITEM_2_REGION = Region(940, 475, width=280, height=40)
SS_DEV_MODE_TITLE_REGION = Region(1050, 125, width=60, height=40)
SS_DEV_MODE_SUBTITLE_REGION = Region(980, 235, width=205, height=40)

# Images:
SKY_TOP_LOGO = 'images/SkyTopLogo.png'
MENU_FIND_OUT_MORE = 'images/SkyQ.png'
MENU_MANAGE_YOUR_ACCOUNT = 'images/ManageYourAccount.png'
MENU_FIX_A_PROBLEM = 'images/FixAProblem.png'
# pylint:disable=stbt-missing-image
MOVING_BALLS = 'images/MovingBalls{0}.png'
TL_RED = 'images/TL_Red.png'
TL_YELLOW = 'images/TL_Yellow.png'
TL_GREEN = 'images/TL_Green.png'
