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
    """FrameObject class to analyze MySky main menu."""

    @property
    def is_visible(self):
        # pylint: disable=stbt-frame-object-missing-frame
        logo_visible = stbt.match(interactive_constants.INTERACTIVE_SKY_LOGO)
        if logo_visible:
            title = find_text(self._frame, interactive_constants.TITLE_REGION)
            debug('[INTERACTIVE] Text found: {0}'.format(title))
            title_visible = (title == sky_plus_strings.INTERACTIVE)

            help_title = find_text(self._frame, interactive_constants.HELP_TITLE_REGION)
            debug('[INTERACTIVE] Text found: {0}'.format(help_title))
            help_title_visible = (help_title == sky_plus_strings.HELP_AND_SUPPORT)

            # get_help = find_text(self._frame, interactive_constants.GET_HELP_REGION)
            # debug('[INTERACTIVE] Text found: {0}'.format(get_help))
            # get_help_visible = (get_help == sky_plus_strings.GET_HELP)

            return title_visible and help_title_visible and get_help_visible
        return False

    @property
    def message(self):
        """Get selected item text"""
        # TODO: Delte this:
        for item in self.menu_items:
            debug('Item text: {0}'.format(item.text))
            debug('Item selected: {0}'.format(item.selected))
        # XXX
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
