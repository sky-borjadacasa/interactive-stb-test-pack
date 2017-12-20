#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contants for Interactive testing
"""

import numpy as np
from stbt import Region

# Channels:
CHANNEL_SKY_ONE = '106'

# Regions:
TITLE_REGION = Region(45, 30, width=170, height=45)
HELP_TITLE_REGION = Region(45, 85, width=210, height=35)
GET_HELP_REGION = Region(45, 120, width=465, height=30)

MAIN_MENU_ITEM_REGIONS = [Region(100, 338, width=530, height=32),
                          Region(100, 374, width=530, height=32),
                          Region(100, 410, width=530, height=32),
                          Region(100, 446, width=530, height=32),
                          Region(100, 482, width=530, height=32),
                          Region(100, 518, width=530, height=32),
                          Region(100, 554, width=530, height=32),
                          Region(100, 590, width=530, height=32),
                          Region(647, 338, width=530, height=32)]

# Images:
INTERACTIVE_SKY_LOGO = 'images/InteractiveSkyLogo.png'

# Colors:
YELLOW_BACKGROUND_RGB = np.array([235, 189, 0])
COLOR_LUMINANCE_THRESHOLD = 10
COLOR_DISTANCE_THRESHOLD = 25
PALETTE_SIZE = 2
