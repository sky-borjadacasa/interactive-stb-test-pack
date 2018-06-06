#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for MySky
"""

from time import sleep
import stbt
from stbt import Region, wait_for_match
import cv2
import interactive_constants
import interactive_test_utils as itu

TRIGGER_REGION = Region(931, 42, width=244, height=35)
TRIGGER_IMAGE = 'images/Trigger.png'


def test_smoke_trigger_open():
    """Open MySky app"""
    itu.clear_test()
    try:
        itu.go_to_channel(interactive_constants.CHANNEL_SKY_ONE_HD)
        match_result = wait_for_match(TRIGGER_IMAGE, timeout_secs=15, region=TRIGGER_REGION)
        assert match_result.match, '[Trigger] Could not find trigger icon'
        stbt.press('KEY_GREEN')
        sleep(5)
        for i in range(10):
            frame = stbt.get_frame()
            # Save image for testing manually later
            cv2.imwrite('trigger_screen_{0}.jpg'.format(i), frame)
    finally:
        itu.clear_test()
