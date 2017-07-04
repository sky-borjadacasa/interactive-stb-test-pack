#!/usr/bin/env python
"""
Test cases for MySky
"""

from time import sleep

import datetime
import stbt
from stbt import FrameObject, match, MatchParameters, ocr, Region
import sky_plus_utils
import mysky_frame_objects
from mysky_frame_objects import MySkyMainMenu

def test_open_mysky():
    """Open MySky app"""
    try:
        stbt.press('KEY_YELLOW')
        menu = stbt.wait_until(MySkyMainMenu)
        assert menu.is_visible
        print 'MySky menu is visible'
        
        sleep(10)

        greeting = menu.title
        print 'Greeting: {0}'.format(greeting)
        assert greeting == greeting_string()

        menu_items = menu.menu_items
        for item in menu_items:
            print 'Item text: {0}'.format(item.text)
            print 'Item selected: {0}'.format(item.selected)
        print len(menu_items)
        assert len(menu_items) == 3

        message = menu.message
        print 'Item message: {0}'.format(message)
        assert message == 'Find out more'

        return 0



        region = stbt.Region(880, 0, width=400, height=720)
        # Just for testing:
        ocr_params = {'language_model_penalty_non_dict_word': 0.5}
        ocr_result = stbt.ocr(region=region, tesseract_config=ocr_params)
        print ocr_result

        assert stbt.match_text(greeting_string(), region=region).match

        # Get selectedmenu item:
        parameters = stbt.MatchParameters(confirm_method='normed-absdiff', match_threshold=0.8) # Is this relevant?
        match = stbt.match('images/SelectedBackground.png', region=region, match_parameters=parameters)
        print 'TESTING ------'
        print 'Match: {0}, {1}'.format(match.match, match.first_pass_result)
        print 'TESTING ++++++'
        assert match.first_pass_result >= 0.9

        # Get text from selected menu
        region = match.region
        ocr_result = stbt.ocr(region=region, tesseract_config=ocr_params)
        print ocr_result

        # Find all unselected items:
        parameters = stbt.MatchParameters(confirm_method='none', match_threshold=0.8) # Is this relevant?
        match = stbt.match('images/NotSelectedBackground.png', region=region, match_parameters=parameters)
        print 'TESTING_2 ------'
        print 'Match: {0}, {1}'.format(match.match, match.first_pass_result)
        print 'TESTING_2 ++++++'

        # Get text from selected menu
        region = match.region
        ocr_result = stbt.ocr(region=region, tesseract_config=ocr_params)
        print ocr_result
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

def greeting_string():
    """Get greeting string"""
    now = datetime.datetime.now()
    mid_day_string = "12:00:00"
    mid_day = datetime.datetime.strptime(mid_day_string, "%H:%M:%S")
    mid_day = now.replace(hour=mid_day.time().hour, minute=mid_day.time().minute, \
        second=mid_day.time().second, microsecond=0)

    if now > mid_day:
        return 'Good Afternoon'
    else:
        return 'Good Morning'
