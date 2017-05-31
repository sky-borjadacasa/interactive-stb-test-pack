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
        parameters = stbt.MatchParameters(confirm_method='normed-absdiff', match_threshold=0.8)
        match = stbt.wait_for_match('images/SelectedBackground.png', region=region, match_parameters=parameters)
        print 'TESTING ------'
        print 'Match: {0}, {1}'.format(match.match, match.first_pass_result)
        print 'TESTING ++++++'
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
