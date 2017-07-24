#!/usr/bin/env python
"""
Contants for MySky testing
"""

import numpy as np
import stbt
from stbt import Region

# Regions:
MY_SKY_REGION = Region(880, 0, width=400, height=720) # The 400 pixels to the right and the whole height of the screen
MY_SKY_GREETING_REGION = Region(930, 90, width=300, height=45)
MAIN_MENU_LOADING_REGION = Region(1015, 280, width=140, height=50)
MAIN_MENU_ITEM_1_REGION = Region(930, 135, width=300, height=150)
MAIN_MENU_ITEM_2_REGION = Region(930, 295, width=300, height=130)
MAIN_MENU_ITEM_3_REGION = Region(930, 435, width=300, height=130)

# Images:
SKY_TOP_LOGO='images/SkyTopLogo.png'

# Text recognition:
OCR_CHAR_WHITELIST = string.ascii_letters + ' ' + string.digits

# Colors:
YELLOW_BACKGROUND_RGB = np.array([235, 189, 0])
BLUE_BACKGROUND_RGB = np.array([30, 87, 161])
BLACK_RGB = np.array([0, 0, 0])
WHITE_RGB = np.array([255, 255, 255])
COLOR_THRESHOLD = 10
PALETTE_SIZE = 2

# Strings:
STRING_SKY_Q='Sky Q'
STRING_MANAGE_YOUR_ACCOUNT='Manage your account'
STRING_FIX_A_PROBLEM='Fix a problem'
STRING_BILLS_AND_PAYMENTS='Bills and payments'
STRING_PACKAGE_AND_SETTINGS='TV package and settings'
STRING_BROADBAND_AND_TALK='Broadband and Talk'
STRING_DETAILS_AND_MESSAGES='My details and messages'
STRING_PICTURE_PROBLEMS='TV picture problems'
STRING_NO_SATELITE_SIGNAL='No satelite signal'
STRING_FORGOTTEN_PIN='Forgotten PIN'
STRING_GOOD_MORNING='Good Morning'
STRING_GOOD_AFTERNOON='Good Afternoon'
STRING_FIND_OUT_MORE='Find out more'
STRING_LOADING='Loading...'


class MySkyMenuItem(object):
    """Class to store the attributes of a MySky menu item"""

    text = ''
    selected = False
    region = None

    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.region = (top_left, bottom_right)

def load_fuzzy_set():
    """Function to load the fuzzy matching expression dictionary

    Returns:
        List of the expressions to match
    """
    lines = [STRING_SKY_Q,
        STRING_MANAGE_YOUR_ACCOUNT,
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
        STRING_FIND_OUT_MORE,
        STRING_LOADING]
    return lines
