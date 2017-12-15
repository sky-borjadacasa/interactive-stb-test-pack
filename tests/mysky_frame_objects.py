#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for MySky
"""

import stbt
from stbt import FrameObject, match, Region
from sky_plus_utils import SkyPlusTestUtils, debug
import mysky_constants

def get_text_region(region):
    """Get region of item where text should be located

    Args:
        region (stbt.Region): Region to crop

    Returns:
        Region of the text
    """
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
    """FrameObject class to analyze MySky main menu."""

    @property
    def _utils(self):
        try:
            return self.utils
        except AttributeError:
            self.utils = SkyPlusTestUtils(self._frame)
        return self.utils

    @property
    def is_visible(self):
        logo_visible = stbt.match(mysky_constants.SKY_TOP_LOGO, region=mysky_constants.MY_SKY_REGION)
        sleep(0.5)
        text = self._utils.find_text(mysky_constants.MAIN_MENU_LOADING_REGION)
        debug('[FIND LOADING] Text found: {0}'.format(text))
        loading_visible = (text == mysky_constants.STRING_LOADING)
        return logo_visible and not loading_visible

    @property
    def title(self):
        text = self._utils.find_text(mysky_constants.MY_SKY_GREETING_REGION)
        return text

    @property
    def message(self):
        selected_list = [x for x in self.menu_items if x.selected]
        return selected_list[0].text

    @property
    def _info(self):
        return match(mysky_constants.SKY_TOP_LOGO, frame=self._frame)

    def weather_loaded(self):
        string = self._utils.find_text(mysky_constants.WEATHER_CITY_NAME_REGION, fuzzy=True)
        assert string == mysky_constants.STRING_YOUR_LOCAL_WEATHER, \
            '[Weather] Message should be [{0}], but is [{1}]'.format(mysky_constants.STRING_YOUR_LOCAL_WEATHER, string)

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
            debug('REGION: {0}'.format(text_region))
            item.text = self._utils.find_text(text_region)
            item.selected = self._utils.match_color(text_region, mysky_constants.YELLOW_BACKGROUND_RGB)

        return items
