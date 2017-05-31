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
    finally:
        clear_test()

def test_open_mysky2():
    """Open MySky app"""
    try:
        stbt.press('KEY_YELLOW')
        sleep(10)
        match = stbt.match_text("Good afternoon")
        assert match.match
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
