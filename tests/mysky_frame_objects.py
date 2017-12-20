#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for MySky
"""

import time
import cv2
import stbt
from stbt import FrameObject, Region
import sky_plus_utils
from sky_plus_utils import debug, IMAGE_DEBUG_MODE
import mysky_constants
import interactive_constants
import sky_plus_strings

def get_text_region(region):
    """Get region of item where text should be located

    Args:
        region (stbt.Region): Region to crop

    Returns:
        Region of the text
    """
    bottom = Region(region.x + 10, region.bottom - 45, width=region.width - 20, bottom=region.bottom - 5)
    return bottom

def detect_moving_balls(frame):
    """Detect moving balls in the given frame

    Args:
        frame (stbt.Frame): Frame to search

    Returns:
        True if moving balls are found, False otherwise
    """
    for i in range(1, 5):
        filename = mysky_constants.MOVING_BALLS.format(i)
        debug('[MOVING BALLS] Using file: {0}'.format(filename))
        if IMAGE_DEBUG_MODE:
            cv2.imwrite('moving_balls_frame_{0}.jpg'.format(time.time()), sky_plus_utils.crop_image(frame, mysky_constants.MY_SKY_MOVING_BALLS_REGION))
        moving_balls = stbt.match(filename, frame=frame, region=mysky_constants.MY_SKY_MOVING_BALLS_REGION)
        if moving_balls:
            return True
    return False

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
        self.selected = sky_plus_utils.match_color(image, text_region, interactive_constants.YELLOW_BACKGROUND_RGB)


class MySkyMainMenu(FrameObject):
    """FrameObject class to analyze MySky main menu."""

    @property
    def is_visible(self):
        # pylint: disable=stbt-frame-object-missing-frame
        logo_visible = stbt.match(mysky_constants.SKY_TOP_LOGO, region=mysky_constants.MY_SKY_REGION)
        if logo_visible:
            text = sky_plus_utils.find_text(self._frame, mysky_constants.MAIN_MENU_LOADING_REGION)
            debug('[FIND LOADING] Text found: {0}'.format(text))
            loading_visible = (text == sky_plus_strings.LOADING)
            moving_balls = detect_moving_balls(self._frame)
            return not loading_visible and not moving_balls
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
        assert string == sky_plus_strings.YOUR_LOCAL_WEATHER, \
            '[Weather] Message should be [{0}], but is [{1}]'.format(sky_plus_strings.YOUR_LOCAL_WEATHER, string)

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

        return items

class SecretSceneMainMenu(FrameObject):
    """FrameObject class to analyze Secret Scene main menu."""

    @property
    def is_visible(self):
        # pylint: disable=stbt-frame-object-missing-frame
        logo_visible = stbt.match(mysky_constants.SKY_TOP_LOGO, region=mysky_constants.MY_SKY_REGION)
        if logo_visible:
            text = sky_plus_utils.find_text(self._frame, mysky_constants.SECRET_SCENE_TITLE_REGION)
            debug('[FIND Interactive My Sky] Text found: {0}'.format(text))
            title_visible = (text == sky_plus_strings.INTERACTIVE_MY_SKY)
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
            item.selected = sky_plus_utils.match_color(self._frame, text_region, interactive_constants.YELLOW_BACKGROUND_RGB)

        return items

class DeveloperMenuMenu(FrameObject):
    """FrameObject class to analyze Secret Scene Developer mode menu."""

    @property
    def is_visible(self):
        # pylint: disable=stbt-frame-object-missing-frame
        logo_visible = stbt.match(mysky_constants.SKY_TOP_LOGO, region=mysky_constants.MY_SKY_REGION)
        if logo_visible:
            text = sky_plus_utils.find_text(self._frame, mysky_constants.SS_DEV_MODE_TITLE_REGION)
            debug('[FIND VCN] Text found: {0}'.format(text))
            title_visible = (text == sky_plus_strings.SS_VCN)
            return title_visible
        return False

    @property
    def title(self):
        """Get title from top of the menu"""
        text = sky_plus_utils.find_text(self._frame, mysky_constants.SS_DEV_MODE_TITLE_REGION)
        return text
