#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for MySky
"""

import time
from time import sleep
import datetime
import stbt
from stbt import FrameObject, match, MatchParameters, ocr, Region, MatchTimeout
import sky_plus_utils
import mysky_frame_objects
from mysky_frame_objects import MySkyMainMenu
import mysky_constants

#####################
# Utility functions #
#####################
def clear_test():
    """Close any app"""
    sleep(2)
    stbt.press('KEY_SKY')
    sleep(3)

def greeting_string():
    """Get greeting string"""
    now = datetime.datetime.now()
    print 'Datetime now: {0}'.format(now)
    mid_day_string = "12:00:00"
    mid_day = datetime.datetime.strptime(mid_day_string, "%H:%M:%S")
    mid_day = now.replace(hour=mid_day.time().hour, minute=mid_day.time().minute, \
        second=mid_day.time().second, microsecond=0)
    six_pm_string = "18.00.00"
    six_pm = datetime.datetime.strptime(six_pm_string, "%H:%M:%S")
    six_pm = now.replace(hour=six_pm.time().hour, minute=six_pm.time().minute, \
        second=six_pm.time().second, microsecond=0)

    if now < mid_day:
        return mysky_constants.STRING_GOOD_MORNING
    elif now < six_pm:
        return mysky_constants.STRING_GOOD_AFTERNOON
    else:
        return mysky_constants.STRING_GOOD_EVENING

def open_and_basic_check_mysky():
    """Open the MySky app and make basic checks"""
    stbt.press('KEY_YELLOW')
    sleep(5) # The menu can be quite slow opening
    menu = stbt.wait_until(MySkyMainMenu)
    assert menu.is_visible

    greeting = menu.title
    assert greeting == greeting_string()

    menu_items = menu.menu_items
    for item in menu_items:
        print 'Item text: {0}'.format(item.text)
        print 'Item selected: {0}'.format(item.selected)
    print len(menu_items)
    assert len(menu_items) == 3
    return menu

def open_and_check_mysky():
    """Open the MySky app and make some checks"""
    menu = open_and_basic_check_mysky()
    menu_items = menu.menu_items

    # Check images inside menu items:
    # This check is disabled for now, until we can know which image is going to be there for sure
    # item = [x for x in menu_items if x.text == mysky_constants.STRING_FIND_OUT_MORE][0]
    # match_result = match(mysky_constants.MENU_FIND_OUT_MORE, frame=menu._frame, region=item.region)
    # print '## match_result: {0}{1}'.format(match_result.match, match_result.first_pass_result)
    # assert match_result.match
    item = [x for x in menu_items if x.text == mysky_constants.STRING_MANAGE_YOUR_ACCOUNT][0]
    match_result = match(mysky_constants.MENU_MANAGE_YOUR_ACCOUNT, frame=menu._frame, region=item.region)
    print '## match_result: {0}{1}'.format(match_result.match, match_result.first_pass_result)
    assert match_result.match
    item = [x for x in menu_items if x.text == mysky_constants.STRING_FIX_A_PROBLEM][0]
    match_result = match(mysky_constants.MENU_FIX_A_PROBLEM, frame=menu._frame, region=item.region)
    print '## match_result: {0}{1}'.format(match_result.match, match_result.first_pass_result)
    assert match_result.match

    message = menu.message
    print 'Item message: {0}'.format(message)
    assert message == mysky_constants.STRING_FIND_OUT_MORE

    return menu

def set_up_backend(backend_env):
    """Get the text fuzzy matched against our dictionary

    Args:
        text (str): Text to match

    Returns:
        Matched text
    """
