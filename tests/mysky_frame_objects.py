#!/usr/bin/env python
"""
Test cases for MySky
"""

from time import sleep

import datetime
import stbt
from stbt import FrameObject, match, MatchParameters, ocr, Region
import sky_plus_utils
from sky_plus_utils import SkyPlusTestUtils

# Regions:
MY_SKY_REGION = Region(880, 0, width=400, height=720) # The 400 pixels to the right and the whole height of the screen

class MySkyMainMenu(object):

	def __init__(self):
		super(FrameObject, self).__init__()
        self.utils = SkyPlusTestUtils(super._frame)

	@property
	def is_visible(self):
		return stbt.match('images/SkyTopLogo.png', region=MY_SKY_REGION)

	@property
	def title(self):
	    return ocr(region=Region(396, 249, 500, 50), frame=self._frame)

	@property
	def message(self):
		text, _ = self.utils.find_text_in_box(sky_plus_utils.MY_SKY_GREETING_REGION)
		return text

	@property
	def _info(self):
	    return match('images/SkyTopLogo.png', frame=self._frame)