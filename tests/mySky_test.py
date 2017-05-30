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
        # Find the loading text:
        loading_region = stbt.Region(930, 0, width=350, height=150)
        assert stbt.wait_for_match('images/Loading.png', region=loading_region)
        assert stbt.wait_for_match('images/SkyTopLogo.png')
        sleep(10)
        match = stbt.match_text("Good afternoon")
        assert match.match
        print stbt.ocr()
    finally:
        clear_test()

def clear_test():
    """Close MySky app"""
    sleep(2)
    while stbt.wait_for_match('images/SkyTopLogo.png'):
        stbt.press('KEY_BACKUP')
