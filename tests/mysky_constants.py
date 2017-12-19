#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contants for MySky testing
"""

import string
import numpy as np
from stbt import Region

# Misc:
MY_SKY_OPEN_TIMEOUT = 25

# Channels:
CHANNEL_SKY_ONE = '106'

# Regions:
MY_SKY_REGION = Region(880, 0, width=400, height=720) # The 400 pixels to the right and the whole height of the screen
MY_SKY_MOVING_BALLS_REGION = Region(1170, 0, width=110, height=75)
MY_SKY_GREETING_REGION = Region(930, 90, width=300, height=45)
MAIN_MENU_LOADING_REGION = Region(1015, 280, width=140, height=50)
MAIN_MENU_ITEM_1_REGION = Region(930, 135, width=300, height=150)
MAIN_MENU_ITEM_2_REGION = Region(930, 295, width=300, height=130)
MAIN_MENU_ITEM_3_REGION = Region(930, 435, width=300, height=130)

WEATHER_CITY_NAME_REGION = Region(930, 590, width=200, height=45)
WEATHER_ICON_REGION = Region(1100, 625, width=70, height=55)
WEATHER_TEMP_REGION = Region(930, 630, width=115, height=60)
WEATHER_TEMP_MAX_REGION = Region(1180, 630, width=55, height=30)
WEATHER_TEMP_MIN_REGION = Region(1180, 660, width=55, height=30)

SKY_Q_NEXT_GENERATION = Region(940, 115, width=285, height=30)
SKY_Q_LONG_TEXT = Region(900, 435, width=350, height=140)

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

# Colors:
YELLOW_BACKGROUND_RGB = np.array([235, 189, 0])
BLUE_BACKGROUND_RGB = np.array([30, 87, 161])
BLACK_RGB = np.array([0, 0, 0])
WHITE_RGB = np.array([255, 255, 255])
COLOR_LUMINANCE_THRESHOLD = 10
COLOR_DISTANCE_THRESHOLD = 25
PALETTE_SIZE = 2

# Text recognition:
OCR_CHAR_WHITELIST = string.ascii_letters + ' ' + string.digits
OCR_CHAR_WHITELIST_TEMP = string.digits + '-ºc'

# Strings:
STRING_MANAGE_YOUR_ACCOUNT = 'Manage your account'
STRING_FIX_A_PROBLEM = 'Fix a problem'
STRING_BILLS_AND_PAYMENTS = 'Bills and payments'
STRING_PACKAGE_AND_SETTINGS = 'TV package and settings'
STRING_BROADBAND_AND_TALK = 'Broadband and Talk'
STRING_DETAILS_AND_MESSAGES = 'My details and messages'
STRING_PICTURE_PROBLEMS = 'TV picture problems'
STRING_NO_SATELITE_SIGNAL = 'No satelite signal'
STRING_FORGOTTEN_PIN = 'Forgotten PIN'
STRING_GOOD_MORNING = 'Good Morning'
STRING_GOOD_AFTERNOON = 'Good Afternoon'
STRING_GOOD_EVENING = 'Good Evening'
STRING_FIND_OUT_MORE = 'Find out more'
STRING_LOADING = 'Loading...'
STRING_NEXT_GENERATION = 'The next generation box'
STRING_YOUR_LOCAL_WEATHER = 'Your local weather'
STRING_INTERACTIVE_MY_SKY = 'Interactive My Sky'
STRING_SS_CLOSE_POPUP = 'Close this popup'
STRING_SS_DEVELOPER_MODE = 'Developer mode'
STRING_SS_VCN = 'VCN'

# Fuzzy set:
FUZZY_SET = [STRING_MANAGE_YOUR_ACCOUNT,
             STRING_FIX_A_PROBLEM,
             STRING_BILLS_AND_PAYMENTS,
             STRING_PACKAGE_AND_SETTINGS,
             STRING_BROADBAND_AND_TALK,
             STRING_DETAILS_AND_MESSAGES,
             STRING_PICTURE_PROBLEMS,
             STRING_NO_SATELITE_SIGNAL,
             STRING_FORGOTTEN_PIN,
             STRING_GOOD_MORNING,
             STRING_GOOD_AFTERNOON,
             STRING_GOOD_EVENING,
             STRING_FIND_OUT_MORE,
             STRING_LOADING,
             STRING_NEXT_GENERATION,
             STRING_YOUR_LOCAL_WEATHER,
             STRING_INTERACTIVE_MY_SKY,
             STRING_SS_CLOSE_POPUP,
             STRING_SS_DEVELOPER_MODE,
             STRING_SS_VCN]
