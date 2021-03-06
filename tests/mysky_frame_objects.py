#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for MySky
"""

import time
import cv2
import stbt
from stbt import Region, match
import sky_plus_utils
from sky_plus_utils import debug, IMAGE_DEBUG_MODE
import mysky_constants
from mysky_constants import MY_SKY_OPEN_TIMEOUT
import mysky_test_utils
import interactive_constants
import interactive_test_utils as itu
import sky_plus_strings
from interactive_frame_objects import ImageMenuItem, InteractiveFrameObject

# ##################### #
# ##### Constants ##### #
# ##################### #

# MySky constants:
MY_SKY_REGION = Region(880, 0, width=400, height=720)  # The 400 pixels to the right and the whole height of the screen
MAIN_MENU_LOADING_REGION = Region(1015, 280, width=140, height=50)
MAIN_MENU_REGIONS = [Region(930, 95, width=300, height=150),
                     Region(930, 255, width=300, height=130),
                     Region(930, 395, width=300, height=130),
                     Region(930, 535, width=300, height=130)]

# Secret Scene constants:
SECRET_SCENE_TITLE_REGION = Region(970, 120, width=230, height=40)
SS_MAIN_REGIONS = [Region(940, 425, width=280, height=40),
                   Region(940, 475, width=280, height=40)]

# Developer mode constants:
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

# Manage Your Account constants:
MYA_TITLE_REGION = Region(950, 90, width=300, height=35)
MYA_MENU_ITEM_REGIONS = [Region(930, 135, width=300, height=130),
                         Region(930, 275, width=300, height=130),
                         Region(930, 415, width=300, height=130),
                         Region(930, 555, width=300, height=130)]


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
    if IMAGE_DEBUG_MODE:
        cv2.imwrite('traffic_light_{0}.jpg'.format(time.time()), frame)
    return is_green


# ######################### #
# ##### Frame Objects ##### #
# ######################### #


class MySkyMainMenu(InteractiveFrameObject):
    """FrameObject class to analyze MySky main menu."""

    def __init__(self):
        super(MySkyMainMenu, self).__init__(MAIN_MENU_REGIONS, item_class=ImageMenuItem)

    @property
    def is_visible(self):
        # pylint: disable=stbt-frame-object-missing-frame
        logo_visible = stbt.match(mysky_constants.SKY_TOP_LOGO, region=MY_SKY_REGION)
        debug('[MYSKY MAIN] Logo visible: {0}'.format(logo_visible))
        if logo_visible:
            text = sky_plus_utils.find_text(self._frame, MAIN_MENU_LOADING_REGION)
            debug('[MYSKY MAIN] Text found: {0}'.format(text))
            loading_visible = (text == sky_plus_strings.LOADING)
            light_is_green = ui_ready(self._frame)
            return not loading_visible and light_is_green
        return False


class SecretSceneMainMenu(InteractiveFrameObject):
    """FrameObject class to analyze Secret Scene main menu."""

    def __init__(self):
        super(SecretSceneMainMenu, self).__init__(SS_MAIN_REGIONS)

    @property
    def is_visible(self):
        # pylint: disable=stbt-frame-object-missing-frame
        logo_visible = stbt.match(mysky_constants.SKY_TOP_LOGO, region=MY_SKY_REGION)
        debug('[SECRET_SCENE] Logo visible: {0}'.format(logo_visible))
        if logo_visible:
            text = sky_plus_utils.find_text(self._frame, SECRET_SCENE_TITLE_REGION)
            debug('[SECRET_SCENE] Text found: {0}'.format(text))
            title_visible = (text == sky_plus_strings.INTERACTIVE_MY_SKY)
            return title_visible
        return False

    @property
    def title(self):
        """Get title from top of the menu"""
        text = sky_plus_utils.find_text(self._frame, SECRET_SCENE_TITLE_REGION)
        return text


class DeveloperModeMenu(InteractiveFrameObject):
    """FrameObject class to analyze Secret Scene Developer mode menu."""

    def __init__(self):
        super(DeveloperModeMenu, self).__init__(SS_DEV_MODE_ITEM_REGIONS)

    @property
    def is_visible(self):
        # pylint: disable=stbt-frame-object-missing-frame
        logo_visible = stbt.match(mysky_constants.SKY_TOP_LOGO, region=MY_SKY_REGION)
        if logo_visible:
            text = sky_plus_utils.find_text(self._frame, SS_DEV_MODE_TITLE_REGION)
            debug('[FIND VCN] Text found: {0}'.format(text))
            title_visible = (text == sky_plus_strings.SS_VCN)
            return title_visible
        return False

    @property
    def title(self):
        """Get title from top of the menu"""
        text = sky_plus_utils.find_text(self._frame, SS_DEV_MODE_TITLE_REGION)
        return text


class ManageYourAccountMenu(InteractiveFrameObject):
    """FrameObject class to analyze Manage Your Account menu."""

    def __init__(self):
        super(ManageYourAccountMenu, self).__init__(MYA_MENU_ITEM_REGIONS, item_class=ImageMenuItem)

    @property
    def is_visible(self):
        # pylint: disable=stbt-frame-object-missing-frame
        logo_visible = stbt.match(mysky_constants.SKY_TOP_LOGO, region=MY_SKY_REGION)
        if logo_visible:
            light_is_green = ui_ready(self._frame)
            text = sky_plus_utils.find_text(self._frame, MYA_TITLE_REGION)
            return light_is_green and text == sky_plus_strings.MANAGE_YOUR_ACCOUNT
        return False

    @property
    def title(self):
        """Get greeting from top of the menu"""
        text = sky_plus_utils.find_text(self._frame, MYA_TITLE_REGION)
        return text


# ################# #
# ##### Utils ##### #
# ################# #


def basic_check_mysky():
    """Make basic checks for MySKy"""
    menu = stbt.wait_until(MySkyMainMenu, timeout_secs=MY_SKY_OPEN_TIMEOUT)
    assert menu.is_visible, '[MySky] Main menu is not visible'

    menu_items = menu.menu_items
    for item in menu_items:
        debug('Item text: {0}'.format(item.text))
        debug('Item selected: {0}'.format(item.selected))
    # TODO: Check problems with weather:
    assert len(menu_items) == 3 or len(menu_items) == 4, '[MySky] Main menu should have 3 or 4 items, but has {0}'.format(len(menu_items))
    return menu


def open_and_basic_check_mysky():
    """Open the MySky app and make basic checks"""
    stbt.press('KEY_YELLOW')
    menu = basic_check_mysky()
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
    assert message == sky_plus_strings.EXPLORE_MORE, \
        '[MySky] Selected item should be [{0}], but is [{1}]'.format(sky_plus_strings.EXPLORE_MORE, message)

    return menu


def button_exits_test(button):
    """Open MySky app and close it with the given button"""
    itu.go_to_channel(interactive_constants.CHANNEL_SKY_ONE_HD)
    open_and_basic_check_mysky()

    # Press the button:
    stbt.press(button)
    assert stbt.wait_until(lambda: not MySkyMainMenu().is_visible), \
        '[MySky] MySky menu did not close'


def open_and_basic_check_manage_your_account():
    """Open the Manage your account menu and make basic checks"""
    open_and_basic_check_mysky()

    # Open menu:
    stbt.press('KEY_DOWN')
    assert stbt.wait_until(lambda: MySkyMainMenu().message == sky_plus_strings.MANAGE_YOUR_ACCOUNT), \
        '[MySky] Selected item is not [{0}]'.format(sky_plus_strings.MANAGE_YOUR_ACCOUNT)
    stbt.press('KEY_SELECT')

    menu = stbt.wait_until(ManageYourAccountMenu)
    assert menu.is_visible, '[ManageYourAccount] Menu is not visible'
    return menu
