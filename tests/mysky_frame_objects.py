#!/usr/bin/env python
"""
Test cases for MySky
"""

from time import sleep

import datetime
import stbt
from stbt import FrameObject, match, MatchParameters, ocr, Region
import sky_plus_utils
from sky_plus_utils import SkyPlusTestUtils, get_utils_region, MySkyMenuItem

# Constants:
BOTTOM_TEXT_SIZE = 45

# Regions:
MY_SKY_REGION = Region(880, 0, width=400, height=720) # The 400 pixels to the right and the whole height of the screen
MAIN_MENU_ITEM_REGION = Region(925, 130, width=300, height=450)
MAIN_MENU_ITEM_1_REGION = Region(925, 135, width=300, height=150)
MAIN_MENU_ITEM_2_REGION = Region(925, 135, width=300, height=130)
MAIN_MENU_ITEM_3_REGION = Region(925, 435, width=300, height=130)

# Images:

def stbt_to_utils_region(region):
    x1 = region.x
    y1 = region.y
    x2 = region.right
    y2 = region.bottom
    return ((x1, y1), (x2, y2))

def get_bottom_region(region, pixels):
    bottom = Region(region.x, region.bottom - pixels, width=region.width, bottom=region.bottom)
    return bottom

class MySkyMenuItem(object):
    """Class to store the attributes of a MySky menu item"""

    text = ''
    selected = False
    region = None

    def __init__(self, region):
        self.region = region


class MySkyMainMenu(FrameObject):

    @property
    def _utils(self):
        try:
            return self.utils
        except AttributeError:
            self.utils = SkyPlusTestUtils(self._frame)
        return self.utils

    @property
    def is_visible(self):
        return stbt.match('images/SkyTopLogo.png', region=MY_SKY_REGION)

    @property
    def title(self):
        text, _ = self._utils.find_text_in_box(sky_plus_utils.MY_SKY_GREETING_REGION)
        return text

    @property
    def message(self):
        # TODO: Return selected box text
        text, _ = self._utils.find_text_in_box(sky_plus_utils.MY_SKY_GREETING_REGION)
        return text

    @property
    def _info(self):
        return match('images/SkyTopLogo.png', frame=self._frame)

    @property
    def menu_items(self):
        item1 = MySkyMenuItem(MAIN_MENU_ITEM_1_REGION)
        text, selected = self._utils.find_text_in_box(stbt_to_utils_region(get_bottom_region(item1.region, BOTTOM_TEXT_SIZE)))
        item1.text = text
        item1.selected = selected

        return [item1]



        #region = get_utils_region(MAIN_MENU_ITEM_REGION)
        #return self._utils.get_menu_items(region=region)
