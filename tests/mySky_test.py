#!/usr/bin/env python
"""
Test cases for MySky
"""

from time import sleep

import stbt

def test_open_mysky():
    """Open MySky app"""
    try:
        stbt.press('KEY_YELLOW')
        assert stbt.wait_for_match('images/SkyTopLogo.png')
        sleep(10)
        region = stbt.Region(880, 0, width=400, height=720)
        # Just for testing:
        ocr_result = stbt.ocr(region=region)
        print ocr_result

        assert stbt.match_text("Good afternoon", region=region).match

        # Get selectedmenu item:
        stbt.match('images/SelectedBackground.png', region=region)
    finally:
        clear_test()

def clear_test():
    """Close MySky app"""
    sleep(2)
    try:
        while stbt.wait_for_match('images/SkyTopLogo.png'):
            sleep(2)
            stbt.press('KEY_BACKUP')
    except:
        print 'Nothing to see here'
