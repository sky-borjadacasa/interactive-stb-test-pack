#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for MySky
"""

import time
import cv2
import stbt
from stbt import FrameObject, Region, match
import sky_plus_utils
from sky_plus_utils import debug, IMAGE_DEBUG_MODE
import mysky_constants
from mysky_constants import MY_SKY_OPEN_TIMEOUT
import mysky_test_utils
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

# DEPRECATED: Use traffic lights better
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

def ui_locked_or_refreshing(frame):
    """Detect if traffic lights are red (ui locked) or yellow (ui refreshing) in the given frame

    Args:
        frame (stbt.Frame): Frame to search

    Returns:
        True if ui is locked or refreshing, False otherwise
    """
    is_red = mysky_test_utils.traffic_light_is_red(frame)
    is_yellow = mysky_test_utils.traffic_light_is_yellow(frame)
    return is_red or is_yellow

def ui_ready(frame):
    """Detect if traffic lights are green in the given frame

    Args:
        frame (stbt.Frame): Frame to search

    Returns:
        True if ui is ready, False otherwise
    """
    is_green = mysky_test_utils.traffic_light_is_green(frame)
    return is_green

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
            light_is_green = mysky_test_utils.traffic_light_is_green(self._frame)
            return not loading_visible and light_is_green
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
        # TODO: Check icons and temperature
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

def open_and_basic_check_mysky():
    """Open the MySky app and make basic checks"""
    stbt.press('KEY_YELLOW')
    menu = stbt.wait_until(MySkyMainMenu, timeout_secs=MY_SKY_OPEN_TIMEOUT)
    assert menu.is_visible, '[MySky] Main menu is not visible'

    greeting = menu.greeting
    assert greeting == mysky_test_utils.greeting_string(), '[MySky] Greeting is [{0}], but should be [{1}]'.format(greeting, mysky_test_utils.greeting_string())

    menu_items = menu.menu_items
    for item in menu_items:
        debug('Item text: {0}'.format(item.text))
        debug('Item selected: {0}'.format(item.selected))
    debug(len(menu_items))
    assert len(menu_items) == 3, '[MySky] Main menu should have 3 items, but has {0}'.format(len(menu_items))
    return menu

def open_and_check_mysky():
    """Open the MySky app and make some checks"""
    menu = open_and_basic_check_mysky()
    menu_items = menu.menu_items

    item = [x for x in menu_items if x.text == sky_plus_strings.MANAGE_YOUR_ACCOUNT][0]
    match_result = match(mysky_constants.MENU_MANAGE_YOUR_ACCOUNT, frame=menu._frame, region=item.region)
    debug('match_result: {0}{1}'.format(match_result.match, match_result.first_pass_result))
    if sky_plus_utils.IMAGE_DEBUG_MODE:
        cv2.imwrite('matching_menu_{0}.jpg'.format(time.time()), sky_plus_utils.crop_image(menu._frame, item.region))
    assert match_result.match, '[MySky] Could not find {0} menu'.format(mysky_constants.MENU_MANAGE_YOUR_ACCOUNT)
    item = [x for x in menu_items if x.text == sky_plus_strings.FIX_A_PROBLEM][0]
    match_result = match(mysky_constants.MENU_FIX_A_PROBLEM, frame=menu._frame, region=item.region)
    debug('match_result: {0}{1}'.format(match_result.match, match_result.first_pass_result))
    assert match_result.match, '[MySky] Could not find {0} menu'.format(sky_plus_strings.FIX_A_PROBLEM)

    message = menu.message
    debug('Item message: {0}'.format(message))
    assert message == sky_plus_strings.FIND_OUT_MORE, \
        '[MySky] Selected item should be [{0}], but is [{1}]'.format(sky_plus_strings.FIND_OUT_MORE, message)

    return menu

def button_exits_test(button):
    """Open MySky app and close it with the given button"""
    sky_plus_utils.go_to_channel(interactive_constants.CHANNEL_SKY_ONE)
    open_and_basic_check_mysky()

    # Press the button:
    stbt.press(button)
    assert stbt.wait_until(lambda: not MySkyMainMenu().is_visible), \
        '[MySky] MySky menu did not close'
