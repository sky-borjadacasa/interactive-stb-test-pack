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
# TODO: Remove this logic, use the traffic lights only
MY_SKY_MOVING_BALLS_REGION = Region(1100, 0, width=180, height=100)
TRAFFIC_LIGHTS_REGION = Region(29, 21, width=20, height=33)

# MySky Regions:
MAIN_MENU_LOADING_REGION = Region(1015, 280, width=140, height=50)
MAIN_MENU_ITEM_1_REGION = Region(930, 95, width=300, height=150)
MAIN_MENU_ITEM_2_REGION = Region(930, 255, width=300, height=130)
MAIN_MENU_ITEM_3_REGION = Region(930, 395, width=300, height=130)
MAIN_MENU_ITEM_4_REGION = Region(930, 535, width=300, height=130)


# Manage Your Account Regions:
MYA_TITLE_REGION = Region(950, 90, width=300, height=35)
MYA_MENU_ITEM_1_REGION = Region(930, 135, width=300, height=130)
MYA_MENU_ITEM_2_REGION = Region(930, 275, width=300, height=130)
MYA_MENU_ITEM_3_REGION = Region(930, 415, width=300, height=130)
MYA_MENU_ITEM_4_REGION = Region(930, 555, width=300, height=130)

# Secret Scene Regions:
SECRET_SCENE_TITLE_REGION = Region(970, 120, width=230, height=40)
SS_MAIN_ITEM_1_REGION = Region(940, 425, width=280, height=40)
SS_MAIN_ITEM_2_REGION = Region(940, 475, width=280, height=40)
SS_DEV_MODE_TITLE_REGION = Region(1050, 125, width=60, height=40)
SS_DEV_MODE_SUBTITLE_REGION = Region(980, 235, width=205, height=40)
SS_DEV_MODE_ITEM_REGIONS = [Region(932, 283, width=290, height=50),
                            Region(932, 333, width=290, height=50),
                            Region(932, 383, width=290, height=50),
                            Region(932, 433, width=290, height=50),
                            Region(932, 483, width=290, height=50),
                            Region(932, 533, width=290, height=50),
                            Region(932, 583, width=290, height=50),
                            Region(932, 633, width=290, height=50)]

# Images:
SKY_TOP_LOGO = 'images/SkyTopLogo.png'
# TODO: Fix this:
MENU_EXPLORE_MORE = 'images/SkyQ.png'
MENU_MANAGE_YOUR_ACCOUNT = 'images/ManageYourAccount.png'
MENU_FIX_A_PROBLEM = 'images/FixAProblem.png'
# pylint:disable=stbt-missing-image
MOVING_BALLS = 'images/MovingBalls{0}.png'
TL_RED = 'images/TL_Red.png'
TL_YELLOW = 'images/TL_Yellow.png'
TL_GREEN = 'images/TL_Green.png'
