#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for MySky
"""

from time import sleep
import datetime
import stbt
from stbt import match
import sky_plus_utils
from sky_plus_utils import debug
from mysky_frame_objects import MySkyMainMenu
import mysky_constants
from mysky_constants import MY_SKY_OPEN_TIMEOUT

def clear_test():
    """Close any app"""
    sleep(2)
    stbt.press('KEY_SKY')
    sleep(3)

def greeting_string():
    """Get greeting string"""
    now = datetime.datetime.now()
    debug('Datetime now: {0}'.format(now))
    mid_day_string = "12:00:00"
    mid_day = datetime.datetime.strptime(mid_day_string, "%H:%M:%S")
    mid_day = now.replace(hour=mid_day.time().hour, minute=mid_day.time().minute, \
        second=mid_day.time().second, microsecond=0)
    six_pm_string = "18:00:00"
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
    menu = stbt.wait_until(MySkyMainMenu, timeout_secs=MY_SKY_OPEN_TIMEOUT)
    assert menu.is_visible, '[MySky] Main menu is not visible'

    greeting = menu.title
    assert greeting == greeting_string(), '[MySky] Greeting is [{0}], but should be [{1}]'.format(greeting, greeting_string())

    menu_items = menu.menu_items
    for item in menu_items:
        debug('Item text: {0}'.format(item.text))
        debug('Item selected: {0}'.format(item.selected))
    debug(len(menu_items))
    assert len(menu_items) == 3, '[MySky] Main menu should have 3 items, but has {0}'.format(len(menu_items))
    return menu

def open_and_check_mysky():
    """Open the MySky app and make some checks"""
    menu = open_and_basic_check_mysky()
    menu_items = menu.menu_items

    # We can not know for sure which image to expect here
    # item = [x for x in menu_items if x.text == mysky_constants.STRING_FIND_OUT_MORE][0]
    # match_result = match(mysky_constants.MENU_FIND_OUT_MORE, frame=menu._frame, region=item.region)
    # debug('match_result: {0}{1}'.format(match_result.match, match_result.first_pass_result))
    # assert match_result.match, '[MySky] Could not find {0} menu'.format(mysky_constants.STRING_FIND_OUT_MORE)
    item = [x for x in menu_items if x.text == mysky_constants.STRING_MANAGE_YOUR_ACCOUNT][0]
    # match_result = match(mysky_constants.MENU_MANAGE_YOUR_ACCOUNT, frame=menu._frame, region=item.region)
    # debug('match_result: {0}{1}'.format(match_result.match, match_result.first_pass_result))
    # assert match_result.match, '[MySky] Could not find {0} menu'.format(mysky_constants.MENU_MANAGE_YOUR_ACCOUNT)
    item = [x for x in menu_items if x.text == mysky_constants.STRING_FIX_A_PROBLEM][0]
    match_result = match(mysky_constants.MENU_FIX_A_PROBLEM, frame=menu._frame, region=item.region)
    debug('match_result: {0}{1}'.format(match_result.match, match_result.first_pass_result))
    assert match_result.match, '[MySky] Could not find {0} menu'.format(mysky_constants.STRING_FIX_A_PROBLEM)

    message = menu.message
    debug('Item message: {0}'.format(message))
    assert message == mysky_constants.STRING_FIND_OUT_MORE, \
        '[MySky] Selected item should be [{0}], but is [{1}]'.format(mysky_constants.STRING_FIND_OUT_MORE, message)

    return menu

def button_exits_test(button):
    """Open MySky app and close it with the given button"""
    sky_plus_utils.go_to_channel(mysky_constants.CHANNEL_SKY_ONE)
    open_and_basic_check_mysky()

    # Press the button:
    stbt.press(button)
    assert stbt.wait_until(lambda: not MySkyMainMenu().is_visible), \
        '[MySky] MySky menu did not close'

def set_up_backend(backend_env):
    """Get the text fuzzy matched against our dictionary

    Args:
        text (str): Text to match

    Returns:
        Matched text
    """
