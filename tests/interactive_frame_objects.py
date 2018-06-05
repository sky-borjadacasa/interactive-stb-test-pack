#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for Interactive menu
"""

import stbt
from stbt import FrameObject, Region
from sky_plus_utils import debug, find_text, match_color
import interactive_constants
import sky_plus_strings


# ##################### #
# ##### Constants ##### #
# ##################### #

MAIN_MENU_ITEM_REGIONS = [Region(100, 338, width=530, height=32),
                          Region(100, 374, width=530, height=32),
                          Region(100, 410, width=530, height=32),
                          Region(100, 446, width=530, height=32),
                          Region(100, 482, width=530, height=32),
                          Region(100, 518, width=530, height=32),
                          Region(100, 554, width=530, height=32),
                          Region(100, 590, width=530, height=32),
                          Region(647, 338, width=530, height=32)]


# pylint: disable=too-few-public-methods
# TODO: Refactor?
class MenuItem(object):
    """Class to store the attributes of a MySky menu item"""

    text = ''
    selected = False
    image = None
    region = None

    def __init__(self, image, region):
        self.image = image
        self.text = find_text(image, region)
        self.selected = match_color(image, region, interactive_constants.YELLOW_BACKGROUND_RGB)


class InteractiveMainMenu(FrameObject):
    """FrameObject class to analyze Interactive main menu."""

    def __init__(self, frame=None):
        if frame is None:
            frame = stbt.get_frame()
        super(InteractiveMainMenu, self).__init__(frame)
        self.items = []

    @property
    def is_visible(self):
        # pylint: disable=stbt-frame-object-missing-frame
        logo_visible = stbt.match(interactive_constants.INTERACTIVE_SKY_LOGO)
        if logo_visible:
            title = find_text(self._frame, interactive_constants.TITLE_REGION)
            debug('[INTERACTIVE] Text found: {0}'.format(title))
            title_visible = (title == sky_plus_strings.INTERACTIVE)

            return title_visible
        return False

    @property
    def message(self):
        """Get selected item text"""
        selected_list = [x for x in self.menu_items if x.selected]
        return selected_list[0].text

    def populate_items(self):
        """Load menu items list"""
        for region in MAIN_MENU_ITEM_REGIONS:
            item = MenuItem(self._frame, region)
            self.items.append(item)

    @property
    def menu_items(self):
        """Get menu items list"""
        if not self.items:
            self.populate_items()
        return self.items

class MyMessagesMenu(FrameObject):
    """FrameObject class to analyze My Messages menu."""

    @property
    def is_visible(self):
        # pylint: disable=stbt-frame-object-missing-frame
        logo_visible = stbt.match(interactive_constants.INTERACTIVE_SKY_LOGO_SD)
        if logo_visible:
            title = find_text(self._frame, interactive_constants.MM_TITLE_REGION)
            debug('[MY MESSAGES] Title found: {0}'.format(title))
            title_visible = (title == sky_plus_strings.MY_MESSAGES)

            subtitle = find_text(self._frame, interactive_constants.MM_SUBTITLE_REGION)
            debug('[MY MESSAGES] Subtitle found: {0}'.format(subtitle))
            subtitle_visible = (subtitle == sky_plus_strings.MM_SUBTITLE)

            pin_visible = stbt.match(interactive_constants.MM_PIN_ENTRY)

            return title_visible and subtitle_visible and pin_visible
        return False

class MyAccountMenu(FrameObject):
    """FrameObject class to analyze My Account menu."""

    @property
    def is_visible(self):
        # pylint: disable=stbt-frame-object-missing-frame
        logo_visible = stbt.match(interactive_constants.INTERACTIVE_SKY_LOGO_SD)
        if logo_visible:
            title = find_text(self._frame, interactive_constants.MA_TITLE_REGION)
            debug('[MY ACCOUNT] Title found: {0}'.format(title))
            title_visible = (title == sky_plus_strings.MY_ACCOUNT)

            background_visible = stbt.match(interactive_constants.MA_BACKGROUND, region=interactive_constants.MA_BACKGROUND_REGION)

            return title_visible and background_visible
        return False
