#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for Interactive menu
"""

import stbt
from stbt import FrameObject
from sky_plus_utils import debug, find_text, match_color
import interactive_constants
import sky_plus_strings

# pylint: disable=too-few-public-methods
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

    @property
    def menu_items(self):
        """Get menu items list"""
        items = []
        for region in interactive_constants.MAIN_MENU_ITEM_REGIONS:
            item = MenuItem(self._frame, region)
            items.append(item)

        return items

class MyMessagesMenu(FrameObject):
    """FrameObject class to analyze My Messages menu."""

    @property
    def is_visible(self):
        # pylint: disable=stbt-frame-object-missing-frame
        logo_visible = stbt.match(interactive_constants.INTERACTIVE_SKY_LOGO_SD)
        if logo_visible:
            title = find_text(self._frame, interactive_constants.MM_TITLE_REGION)
            debug('[MY MESSAGES] Text found: {0}'.format(title))
            title_visible = (title == sky_plus_strings.MY_MESSAGES)

            subtitle = find_text(self._frame, interactive_constants.MM_SUBTITLE_REGION)
            debug('[MY MESSAGES] Text found: {0}'.format(subtitle))
            subtitle_visible = (subtitle == sky_plus_strings.MM_SUBTITLE)

            return title_visible and subtitle_visible
        return False
