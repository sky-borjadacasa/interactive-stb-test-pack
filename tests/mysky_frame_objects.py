#!/usr/bin/env python
"""
Test cases for MySky
"""

from time import sleep

import datetime
import stbt
import sky_plus_utils

class MySkyMainMenu(FrameObject):
	@property
	def is_visible(self):
	    return bool(self._info)

	@property
	def title(self):
	    return ocr(region=Region(396, 249, 500, 50), frame=self._frame)

	@property
	def message(self):
	    right_of_info = Region(
	        x=self._info.region.right, y=self._info.region.y,
	        width=390, height=self._info.region.height)
	    return ocr(region=right_of_info, frame=self._frame) \
	           .replace('\n', ' ')

	@property
	def _info(self):
	    return match('images/SkyTopLogo.png', frame=self._frame)