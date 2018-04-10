#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for MySky
"""

from time import sleep
import stbt
from stbt import Region, wait_for_match
import cv2
import sky_plus_utils
from sky_plus_utils import clear_test
import interactive_constants

TRIGGER_REGION = Region(931, 42, width=244, height=35)
TRIGGER_IMAGE = 'images/Trigger.png'

def test_smoke_trigger_open():
    """Open MySky app"""
    clear_test()
    try:
        sky_plus_utils.go_to_channel(interactive_constants.CHANNEL_SKY_ONE_HD)
        match_result = wait_for_match(TRIGGER_IMAGE, timeout_secs=15, region=TRIGGER_REGION)
        assert match_result.match, '[Trigger] Could not find trigger icon'
        stbt.press('KEY_GREEN')
        sleep(5)
        for i in range(10):
            frame = stbt.get_frame()
            # Save image for testing manually later
            cv2.imwrite('trigger_screen_{0}.jpg'.format(i), frame)
    finally:
        clear_test()
