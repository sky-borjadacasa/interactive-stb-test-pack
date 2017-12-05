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
import mysky_test_utils

def test_smoke_open_mysky():
    """Open MySky app"""
    mysky_test_utils.clear_test()
    try:
        sky_plus_utils.go_to_channel(mysky_constants.CHANNEL_SKY_ONE)
        mysky_test_utils.open_and_basic_check_mysky()
    finally:
        mysky_test_utils.clear_test()

def test_yellow_button_exits():
    """Open MySky app"""
    mysky_test_utils.clear_test()
    try:
        sky_plus_utils.go_to_channel(mysky_constants.CHANNEL_SKY_ONE)
        mysky_test_utils.open_and_check_mysky()

        # Press yellow button:
        stbt.press('KEY_YELLOW')
        assert stbt.wait_until(lambda: not MySkyMainMenu().is_visible)

    finally:
        mysky_test_utils.clear_test()

def test_open_mysky():
    """Open MySky app"""
    mysky_test_utils.clear_test()
    try:
        sky_plus_utils.go_to_channel(mysky_constants.CHANNEL_SKY_ONE)
        mysky_test_utils.open_and_check_mysky()

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
        mysky_test_utils.clear_test()

def test_mysky_weather():
    """Open MySky app"""
    mysky_test_utils.clear_test()
    try:
        sky_plus_utils.go_to_channel(mysky_constants.CHANNEL_SKY_ONE)
        menu = mysky_test_utils.open_and_check_mysky()

        # Check weather loaded correctly:
        menu.weather_loaded()

    finally:
        mysky_test_utils.clear_test()
