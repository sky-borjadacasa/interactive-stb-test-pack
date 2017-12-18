#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for MySky
"""

import stbt
from stbt import FrameObject, Region
import sky_plus_utils
from sky_plus_utils import debug
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

# pylint: disable=too-few-public-methods
class MySkyMenuItem(object):
    """Class to store the attributes of a MySky menu item"""

    text = ''
    selected = False
    image = None
    region = None

    def __init__(self, image, region):
        self.image = image
        self.region = region
        text_region = get_text_region(region)
        debug('REGION: {0}'.format(text_region))
        self.text = sky_plus_utils.find_text(image, text_region)
        self.selected = sky_plus_utils.match_color(image, text_region, mysky_constants.YELLOW_BACKGROUND_RGB)


class MySkyMainMenu(FrameObject):
    """FrameObject class to analyze MySky main menu."""

    @property
    def is_visible(self):
        # pylint: disable=stbt-frame-object-missing-frame
        logo_visible = stbt.match(mysky_constants.SKY_TOP_LOGO, region=mysky_constants.MY_SKY_REGION)
        if logo_visible:
            text = sky_plus_utils.find_text(self._frame, mysky_constants.MAIN_MENU_LOADING_REGION)
            debug('[FIND LOADING] Text found: {0}'.format(text))
            loading_visible = (text == mysky_constants.STRING_LOADING)
            return not loading_visible
        return False

    @property
    def greeting(self):
        """Get greeting from top of the menu"""
        text = sky_plus_utils.find_text(self._frame, mysky_constants.MY_SKY_GREETING_REGION)
        return text

    @property
    def message(self):
        """Get selected item text"""
        selected_list = [x for x in self.menu_items if x.selected]
        return selected_list[0].text

    def weather_loaded(self):
        """Check if weather section is loaded"""
        # TODO: Check icons and temperature
        string = sky_plus_utils.find_text(self._frame, mysky_constants.WEATHER_CITY_NAME_REGION)
        assert string == mysky_constants.STRING_YOUR_LOCAL_WEATHER, \
            '[Weather] Message should be [{0}], but is [{1}]'.format(mysky_constants.STRING_YOUR_LOCAL_WEATHER, string)

    @property
    def menu_items(self):
        """Get menu items list"""
        items = []
        item = MySkyMenuItem(self._frame, mysky_constants.MAIN_MENU_ITEM_1_REGION)
        items.append(item)
        item = MySkyMenuItem(self._frame, mysky_constants.MAIN_MENU_ITEM_2_REGION)
        items.append(item)
        item = MySkyMenuItem(self._frame, mysky_constants.MAIN_MENU_ITEM_3_REGION)
        items.append(item)

        for item in items:
            text_region = get_text_region(item.region)
            debug('REGION: {0}'.format(text_region))
            item.text = sky_plus_utils.find_text(self._frame, text_region)
            item.selected = sky_plus_utils.match_color(self._frame, text_region, mysky_constants.YELLOW_BACKGROUND_RGB)

        return items

class SecretSceneMainMenu(FrameObject):
    """FrameObject class to analyze MySky main menu."""

    @property
    def is_visible(self):
        # pylint: disable=stbt-frame-object-missing-frame
        logo_visible = stbt.match(mysky_constants.SKY_TOP_LOGO, region=mysky_constants.MY_SKY_REGION)
        if logo_visible:
            text = sky_plus_utils.find_text(self._frame, mysky_constants.SECRET_SCENE_TITLE_REGION)
            debug('[FIND LOADING] Text found: {0}'.format(text))
            title_visible = (text == mysky_constants.STRING_INTERACTIVE_MY_SKY)
            return title_visible
        return False

    @property
    def title(self):
        """Get title from top of the menu"""
        text = sky_plus_utils.find_text(self._frame, mysky_constants.SECRET_SCENE_TITLE_REGION)
        return text

    @property
    def message(self):
        """Get selected item text"""
        selected_list = [x for x in self.menu_items if x.selected]
        return selected_list[0].text

    @property
    def menu_items(self):
        """Get menu items list"""
        items = []
        item = MySkyMenuItem(self._frame, mysky_constants.SS_MAIN_ITEM_1_REGION)
        items.append(item)
        item = MySkyMenuItem(self._frame, mysky_constants.SS_MAIN_ITEM_2_REGION)
        items.append(item)

        for item in items:
            text_region = get_text_region(item.region)
            debug('REGION: {0}'.format(text_region))
            item.text = sky_plus_utils.find_text(self._frame, text_region)
            item.selected = sky_plus_utils.match_color(self._frame, text_region, mysky_constants.YELLOW_BACKGROUND_RGB)

        return items
