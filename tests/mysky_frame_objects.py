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

# Regions:
MY_SKY_REGION = Region(880, 0, width=400, height=720) # The 400 pixels to the right and the whole height of the screen
MAIN_MENU_ITEM_REGION = Region(930, 130, width=300, height=450)
MAIN_MENU_ITEM_1_REGION = Region(930, 135, width=300, height=150)
MAIN_MENU_ITEM_2_REGION = Region(930, 295, width=300, height=130)
MAIN_MENU_ITEM_3_REGION = Region(930, 435, width=300, height=130)

# Images:

def stbt_to_utils_region(region):
    x1 = region.x
    y1 = region.y
    x2 = region.right
    y2 = region.bottom
    return ((x1, y1), (x2, y2))

def text_region(region):
    bottom = Region(region.x + 10, region.bottom - pixels, width=region.width - 20, bottom=region.bottom - 5)
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
        selected_list = [x for x in self.menu_items if x.selected == True]
        # XXX
        return 'selected_list[0].text'

    @property
    def _info(self):
        return match('images/SkyTopLogo.png', frame=self._frame)

    @property
    def menu_items(self):
        items = []
        item = MySkyMenuItem(MAIN_MENU_ITEM_1_REGION)
        items.append(item)
        item = MySkyMenuItem(MAIN_MENU_ITEM_2_REGION)
        items.append(item)
        item = MySkyMenuItem(MAIN_MENU_ITEM_3_REGION)
        items.append(item)

        for item in items:
            text_region = stbt_to_utils_region(text_region(item.region))
            # XXX
            print 'REGION: {0}'.format(text_region)
            item.text, item.selected = self._utils.find_text_in_box(text_region)

        return items
