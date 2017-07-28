#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for MySky
"""

import time
from time import sleep
import datetime
import stbt
from stbt import FrameObject, match, MatchParameters, ocr, Region
import sky_plus_utils
import mysky_frame_objects
from mysky_frame_objects import MySkyMainMenu, MySkySkyQMenu
import mysky_constants

def test_yellow_button_exits():
    """Open MySky app"""
    try:
        go_to_channel(mysky_constants.CHANNEL_SKY_ONE)
        menu = open_and_check_mysky()

        # Press yellow button:
        stbt.press('KEY_YELLOW')
        assert stbt.wait_until(lambda: not MySkyMainMenu().is_visible)

    finally:
        clear_test()

def test_open_mysky():
    """Open MySky app"""
    try:
        go_to_channel(mysky_constants.CHANNEL_SKY_ONE)
        open_and_check_mysky()

        # Navigate menus:
        stbt.press('KEY_DOWN')
        assert stbt.wait_until(lambda: MySkyMainMenu().message == mysky_constants.STRING_MANAGE_YOUR_ACCOUNT)
        stbt.press('KEY_DOWN')
        assert stbt.wait_until(lambda: MySkyMainMenu().message == mysky_constants.STRING_FIX_A_PROBLEM)
        stbt.press('KEY_UP')
        assert stbt.wait_until(lambda: MySkyMainMenu().message == mysky_constants.STRING_MANAGE_YOUR_ACCOUNT)
        stbt.press('KEY_UP')
        assert stbt.wait_until(lambda: MySkyMainMenu().message == mysky_constants.STRING_FIND_OUT_MORE)
    finally:
        clear_test()

def test_mysky_weather():
    """Open MySky app"""
    try:
        go_to_channel(mysky_constants.CHANNEL_SKY_ONE)
        menu = open_and_check_mysky()

        # Check weather loaded correctly:
        menu.weather_loaded()

    finally:
        clear_test()

def test_sky_q_screen():
    """Open MySky app"""
    try:
        go_to_channel(mysky_constants.CHANNEL_SKY_ONE)
        menu = open_and_check_mysky()

        stbt.press('KEY_SELECT')

        # Check Sky Q page loaded correctly:
        skyq_screen = stbt.wait_until(MySkySkyQMenu)

    finally:
        clear_test()

# Utils:

def clear_test():
    """Close MySky app"""
    sleep(2)
    try:
        while stbt.wait_for_match(mysky_constants.SKY_TOP_LOGO):
            sleep(2)
            stbt.press('KEY_BACKUP')
    except:
        print 'Nothing to see here'

def greeting_string():
    """Get greeting string"""
    now = datetime.datetime.now()
    print 'Datetime now: {0}'.format(now)
    mid_day_string = "12:00:00"
    mid_day = datetime.datetime.strptime(mid_day_string, "%H:%M:%S")
    mid_day = now.replace(hour=mid_day.time().hour, minute=mid_day.time().minute, \
        second=mid_day.time().second, microsecond=0)

    if now > mid_day:
        return mysky_constants.STRING_GOOD_AFTERNOON
    else:
        return mysky_constants.STRING_GOOD_MORNING

def open_and_check_mysky():
    stbt.press('KEY_YELLOW')
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

    # Check images inside menu items:
    item = [x for x in menu_items if x.text == mysky_constants.STRING_FIND_OUT_MORE][0]
    match_result = match(mysky_constants.MENU_FIND_OUT_MORE, frame=menu._frame, region=item.region)
    print '## match_result: {0}{1}'.format(match_result.match, match_result.first_pass_result)
    assert match_result.match
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

def go_to_channel(channel):
    assert len(channel) == 3
    for c in channel:
        button = 'KEY_{0}'.format(c)
        stbt.press(button)
