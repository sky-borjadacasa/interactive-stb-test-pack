#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for Interactive menu
"""

import numpy as np
import stbt
from stbt import FrameObject, Region
import sky_plus_utils
from sky_plus_utils import debug, find_text, match_color
import interactive_constants
import sky_plus_strings
from mysky_test_utils import get_bottom_text_region, get_default_image_region


# ##################### #
# ##### Constants ##### #
# ##################### #

INTERACTIVE_SKY_LOGO = 'images/InteractiveSkyLogo.png'
MM_PIN_ENTRY = 'images/PinEntry.png'
MA_BACKGROUND = 'images/MyAccountBackground.png'

# Colors:
YELLOW_BACKGROUND_RGB = np.array([235, 189, 0])

TITLE_REGION = Region(45, 30, width=170, height=45)

MAIN_MENU_ITEM_REGIONS = [Region(100, 338, width=530, height=32),
                          Region(100, 374, width=530, height=32),
                          Region(100, 410, width=530, height=32),
                          Region(100, 446, width=530, height=32),
                          Region(100, 482, width=530, height=32),
                          Region(100, 518, width=530, height=32),
                          Region(100, 554, width=530, height=32),
                          Region(100, 590, width=530, height=32),
                          Region(647, 338, width=530, height=32)]

# My Messages Regions:
MM_TITLE_REGION = Region(90, 60, width=180, height=40)
MM_SUBTITLE_REGION = Region(310, 185, width=670, height=45)
MA_BACKGROUND_REGION = Region(600, 110, width=680, height=610)

# My Account Regions:
MA_TITLE_REGION = Region(120, 65, width=160, height=40)


# ############################# #
# ##### Menu Item classes ##### #
# ############################# #



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
        self.selected = match_color(image, region, YELLOW_BACKGROUND_RGB)


# pylint: disable=too-few-public-methods
class ImageMenuItem(object):
    """Class to store the attributes of a MySky menu item"""

    text = ''
    selected = False
    frame = None
    region = None
    image_region = None
    text_region = None

    def __init__(self, frame, region):
        self.frame = frame
        self.region = region
        self.text_region = get_bottom_text_region(region)
        self.image_region = get_default_image_region(region)
        debug('REGION: {0}'.format(self.text_region))
        if self.text_region is not None:
            self.text = sky_plus_utils.find_text(frame, self.text_region)
            self.selected = sky_plus_utils.match_color(frame, self.text_region, YELLOW_BACKGROUND_RGB)


# pylint: disable=too-few-public-methods
class CustomMenuItem(object):
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
        debug('REGION: {0}'.format(self.text_region))
        if self.text_region is not None:
            self.text = sky_plus_utils.find_text(frame, self.text_region)
            self.selected = sky_plus_utils.match_color(frame, self.text_region, YELLOW_BACKGROUND_RGB)


# ######################### #
# ##### Frame Objects ##### #
# ######################### #


class InteractiveFrameObject(FrameObject):
    """FrameObject class to be extended for other Interactive Frame Objects."""

    def __init__(self, menu_regions, item_class=MenuItem, frame=None):
        if frame is None:
            frame = stbt.get_frame()
        super(InteractiveFrameObject, self).__init__(frame)
        self.menu_regions = menu_regions
        self.item_class = item_class
        self.items = []

    items = []

    @property
    def is_visible(self):
        raise NotImplementedError('Objects deriving from InteractiveFrameObject must define an is_visible property')

    @property
    def message(self):
        """Get selected item text"""
        selected_list = [x for x in self.menu_items if x.selected]
        return selected_list[0].text

    def populate_items(self):
        """Load menu items list"""
        for region in self.menu_regions:
            item = self.item_class(self._frame, region)
            if item.text:
                self.items.append(item)

    @property
    # TODO: Refactor usage
    def menu_items(self):
        """Get menu items list"""
        if not self.items:
            self.populate_items()
        return self.items


class InteractiveMainMenu(InteractiveFrameObject):
    """FrameObject class to analyze Interactive main menu."""

    def __init__(self):
        super(InteractiveMainMenu, self).__init__(MAIN_MENU_ITEM_REGIONS)

    @property
    def is_visible(self):
        # pylint: disable=stbt-frame-object-missing-frame
        logo_visible = stbt.match(INTERACTIVE_SKY_LOGO)
        debug('[INTERACTIVE] Logo visible: {0}'.format(logo_visible))
        if logo_visible:
            title = find_text(self._frame, TITLE_REGION)
            debug('[INTERACTIVE] Text found: {0}'.format(title))
            title_visible = (title == sky_plus_strings.INTERACTIVE)

            return title_visible
        return False


class MyMessagesMenu(InteractiveFrameObject):
    """FrameObject class to analyze My Messages menu."""

    def __init__(self):
        super(MyMessagesMenu, self).__init__([])

    @property
    def is_visible(self):
        # pylint: disable=stbt-frame-object-missing-frame
        logo_visible = stbt.match(interactive_constants.INTERACTIVE_SKY_LOGO_SD)
        debug('[MY MESSAGES] Logo visible: {0}'.format(logo_visible))
        if logo_visible:
            title = find_text(self._frame, MM_TITLE_REGION)
            debug('[MY MESSAGES] Title found: {0}'.format(title))
            title_visible = (title == sky_plus_strings.MY_MESSAGES)

            subtitle = find_text(self._frame, MM_SUBTITLE_REGION)
            debug('[MY MESSAGES] Subtitle found: {0}'.format(subtitle))
            subtitle_visible = (subtitle == sky_plus_strings.MM_SUBTITLE)

            pin_visible = stbt.match(MM_PIN_ENTRY)

            return title_visible and subtitle_visible and pin_visible
        return False


class MyAccountMenu(InteractiveFrameObject):
    """FrameObject class to analyze My Account menu."""

    def __init__(self):
        super(MyAccountMenu, self).__init__([])

    @property
    def is_visible(self):
        # pylint: disable=stbt-frame-object-missing-frame
        logo_visible = stbt.match(interactive_constants.INTERACTIVE_SKY_LOGO_SD)
        debug('[MY ACCOUNT] Logo visible: {0}'.format(logo_visible))
        if logo_visible:
            title = find_text(self._frame, MA_TITLE_REGION)
            debug('[MY ACCOUNT] Title found: {0}'.format(title))
            title_visible = (title == sky_plus_strings.MY_ACCOUNT)

            background_visible = stbt.match(MA_BACKGROUND, region=MA_BACKGROUND_REGION)

            return title_visible and background_visible
        return False
