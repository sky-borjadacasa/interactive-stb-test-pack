#!/usr/bin/env python
"""
Test cases for MySky
"""

from time import sleep

import datetime
import stbt
from stbt import FrameObject, match, MatchParameters, ocr, Region
import sky_plus_utils
from sky_plus_utils import SkyPlusTestUtils, get_utils_region

# Regions:
MY_SKY_REGION = Region(880, 0, width=400, height=720) # The 400 pixels to the right and the whole height of the screen
MAIN_MENU_ITEM_RETION = Region(925, 130, width=300, height=450)

class MySkyMainMenu(FrameObject):

    @property
    def _utils(self):
        try:
            return self.utils
        except AttributeError:
            self.utils = SkyPlusTestUtils(self._frame)
        return self.utils

    @property
    def is_visible(self):
        return stbt.match('images/SkyTopLogo.png', region=MY_SKY_REGION)

    @property
    def title(self):
        text, _ = self._utils.find_text_in_box(sky_plus_utils.MY_SKY_GREETING_REGION)
        return text

    @property
    def message(self):
        # TODO: Return selected box text
        text, _ = self._utils.find_text_in_box(sky_plus_utils.MY_SKY_GREETING_REGION)
        return text

    @property
    def _info(self):
        return match('images/SkyTopLogo.png', frame=self._frame)

    @property
    def menu_items(self):
        region = get_utils_region(MAIN_MENU_ITEM_RETION)
        return self._utils.get_menu_items(region=region)