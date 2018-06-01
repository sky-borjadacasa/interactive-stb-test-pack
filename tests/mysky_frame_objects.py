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
from mysky_test_utils import get_bottom_text_region, get_default_image_region
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


# pylint: disable=too-few-public-methods
class MySkyMenuItem(object):
    """Class to store the attributes of a MySky menu item"""

    text = ''
    selected = False
    frame = None
    region = None
    image_region = None
    text_region = None

    def __init__(self, frame, region, text_region_function=get_bottom_text_region,
                 image_region_function=get_default_image_region):
        self.frame = frame
        self.region = region
        if image_region_function is not None:
            self.image_region = image_region_function(region)
        if text_region_function is not None:
            self.text_region = text_region_function(region)
        # TODO: Refactor
        debug('REGION: {0}'.format(self.text_region))
        if self.text_region is not None:
            self.text = sky_plus_utils.find_text(frame, self.text_region)
            self.selected = sky_plus_utils.match_color(frame, self.text_region,
                                                       interactive_constants.YELLOW_BACKGROUND_RGB)


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
            light_is_green = ui_ready(self._frame)
            return not loading_visible and light_is_green
        return False

    @property
    def message(self):
        """Get selected item text"""
        selected_list = [x for x in self.menu_items if x.selected]
        return selected_list[0].text

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
        item = MySkyMenuItem(self._frame, mysky_constants.MAIN_MENU_ITEM_4_REGION)
        items.append(item)

        return items


class SecretSceneMainMenu(FrameObject):
    """FrameObject class to analyze Secret Scene main menu."""

    def __init__(self, frame=None):
        super(FrameObject, self).__init__(frame)
        self.items = []

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
        debug('[DEBUG_REFACTOR] Enter message -> len(self.items) = {0}'.format(len(self.items)))
        selected_list = [x for x in self.menu_items if x.selected]
        debug('[DEBUG_REFACTOR] Exit message -> len(self.items) = {0}'.format(len(self.items)))
        return selected_list[0].text

    def populate_items(self):
        """Load menu items list"""
        debug('[DEBUG_REFACTOR] Enter populate_items')
        # TODO: Refactor
        item = MySkyMenuItem(self._frame, mysky_constants.SS_MAIN_ITEM_1_REGION, image_region_function=None)
        self.items.append(item)
        item = MySkyMenuItem(self._frame, mysky_constants.SS_MAIN_ITEM_2_REGION, image_region_function=None)
        self.items.append(item)
        debug('[DEBUG_REFACTOR] Exit populate_items -> len(self.items) = {0}'.format(len(self.items)))

    @property
    # TODO: Refactor usage
    def menu_items(self):
        """Get menu items list"""
        debug('[DEBUG_REFACTOR] Enter menu_items -> len(self.items) = {0}'.format(len(self.items)))
        if not self.items:
            self.populate_items()
        debug('[DEBUG_REFACTOR] Exit menu_items -> len(self.items) = {0}'.format(len(self.items)))
        return self.items


class DeveloperModeMenu(FrameObject):
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

    @property
    def message(self):
        """Get selected item text"""
        selected_list = [x for x in self.menu_items if x.selected]
        return selected_list[0].text

    @property
    def menu_items(self):
        """Get menu items list"""
        items = []
        for region in mysky_constants.SS_DEV_MODE_ITEM_REGIONS:
            item = MySkyMenuItem(self._frame, region, image_region_function=None)
            items.append(item)
        return items


class ManageYourAccountMenu(FrameObject):
    """FrameObject class to analyze Manage Your Account menu."""

    @property
    def is_visible(self):
        # pylint: disable=stbt-frame-object-missing-frame
        logo_visible = stbt.match(mysky_constants.SKY_TOP_LOGO, region=mysky_constants.MY_SKY_REGION)
        if logo_visible:
            light_is_green = ui_ready(self._frame)
            text = sky_plus_utils.find_text(self._frame, mysky_constants.MYA_TITLE_REGION)
            return light_is_green and text == sky_plus_strings.MANAGE_YOUR_ACCOUNT
        return False

    @property
    def title(self):
        """Get greeting from top of the menu"""
        text = sky_plus_utils.find_text(self._frame, mysky_constants.MYA_TITLE_REGION)
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
        item = MySkyMenuItem(self._frame, mysky_constants.MYA_MENU_ITEM_1_REGION)
        items.append(item)
        item = MySkyMenuItem(self._frame, mysky_constants.MYA_MENU_ITEM_2_REGION)
        items.append(item)
        item = MySkyMenuItem(self._frame, mysky_constants.MYA_MENU_ITEM_3_REGION)
        items.append(item)
        item = MySkyMenuItem(self._frame, mysky_constants.MYA_MENU_ITEM_4_REGION)
        items.append(item)

        return items


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
    debug(len(menu_items))
    assert len(menu_items) == 4, '[MySky] Main menu should have 3 items, but has {0}'.format(len(menu_items))
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
    sky_plus_utils.go_to_channel(interactive_constants.CHANNEL_SKY_ONE_HD)
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
