#!/usr/bin/env python
"""
Test cases for MySky
"""

from time import sleep

import datetime
import stbt
from stbt import FrameObject, match, MatchParameters, ocr, Region
import sky_plus_utils
from sky_plus_utils import SkyPlusTestUtils
import mysky_constants

def get_text_region(region):
    bottom = Region(region.x + 10, region.bottom - 45, width=region.width - 20, bottom=region.bottom - 5)
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
            self.utils = SkyPlusTestUtils(self._frame, debug_mode=True)
        return self.utils

    @property
    def is_visible(self):
        logo_visible = stbt.match('images/SkyTopLogo.png', region=mysky_constants.MY_SKY_REGION)
        text = self._utils.find_text(mysky_constants.MAIN_MENU_LOADING_REGION)
        loading_visible = (text == 'Loading...')
        return logo_visible and not loading_visible

    @property
    def title(self):
        text = self._utils.find_text(mysky_constants.MY_SKY_GREETING_REGION)
        return text

    @property
    def message(self):
        selected_list = [x for x in self.menu_items if x.selected == True]
        return selected_list[0].text

    @property
    def _info(self):
        return match('images/SkyTopLogo.png', frame=self._frame)

    @property
    def menu_items(self):
        items = []
        item = MySkyMenuItem(mysky_constants.MAIN_MENU_ITEM_1_REGION)
        items.append(item)
        item = MySkyMenuItem(mysky_constants.MAIN_MENU_ITEM_2_REGION)
        items.append(item)
        item = MySkyMenuItem(mysky_constants.MAIN_MENU_ITEM_3_REGION)
        items.append(item)

        for item in items:
            text_region = get_text_region(item.region)
            print 'REGION: {0}'.format(text_region)
            item.text = self._utils.find_text(text_region)
            item.selected = self._utils.match_color(text_region, mysky_constants.YELLOW_BACKGROUND_RGB)

        return items
