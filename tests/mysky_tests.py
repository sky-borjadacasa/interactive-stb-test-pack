#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for MySky
"""

import stbt
import sky_plus_strings
import sky_plus_utils
from sky_plus_utils import clear_test
import mysky_frame_objects
from mysky_frame_objects import MySkyMainMenu
import interactive_constants

def test_smoke_open_mysky():
    """Open MySky app"""
    clear_test()
    try:
        sky_plus_utils.go_to_channel(interactive_constants.CHANNEL_SKY_ONE)
        mysky_frame_objects.open_and_basic_check_mysky()
    finally:
        clear_test()

def test_acceptance_simple_open_mysky():
    """Open MySky app and navigate
    Automates: https://interactiveqa.testrail.net/index.php?/cases/view/20
    Automates: https://interactiveqa.testrail.net/index.php?/cases/view/22
    """
    clear_test()
    try:
        sky_plus_utils.go_to_channel(interactive_constants.CHANNEL_SKY_ONE)
        mysky_frame_objects.open_and_check_mysky()

        # Navigate menus:
        stbt.press('KEY_DOWN')
        assert stbt.wait_until(lambda: MySkyMainMenu().message == sky_plus_strings.MANAGE_YOUR_ACCOUNT), \
            '[MySky] Selected item is not [{0}]'.format(sky_plus_strings.MANAGE_YOUR_ACCOUNT)
        stbt.press('KEY_DOWN')
        assert stbt.wait_until(lambda: MySkyMainMenu().message == sky_plus_strings.FIX_A_PROBLEM), \
            '[MySky] Selected item is not [{0}]'.format(sky_plus_strings.FIX_A_PROBLEM)
        stbt.press('KEY_UP')
        assert stbt.wait_until(lambda: MySkyMainMenu().message == sky_plus_strings.MANAGE_YOUR_ACCOUNT), \
            '[MySky] Selected item is not [{0}]'.format(sky_plus_strings.MANAGE_YOUR_ACCOUNT)
        stbt.press('KEY_UP')
        assert stbt.wait_until(lambda: MySkyMainMenu().message == sky_plus_strings.FIND_OUT_MORE), \
            '[MySky] Selected item is not [{0}]'.format(sky_plus_strings.FIND_OUT_MORE)
    finally:
        clear_test()

def test_acceptance_simple_yellow_button_exits():
    """Open MySky app and close it with the yellow button"""
    clear_test()
    try:
        mysky_frame_objects.button_exits_test('KEY_YELLOW')
    finally:
        clear_test()

def test_acceptance_simple_backup_button_exits():
    """Open MySky app and close it with the back up button
    Automates: https://interactiveqa.testrail.net/index.php?/cases/view/23
    """
    clear_test()
    try:
        mysky_frame_objects.button_exits_test('KEY_BACKUP')
    finally:
        clear_test()

def test_timed_greeting_good_morning():
    """Open MySky app and check that the greeting is Good morning
    Automates: https://interactiveqa.testrail.net/index.php?/cases/view/4
    NOTE: This test must run between midnight and midday
    """
    clear_test()
    try:
        mysky_frame_objects.open_and_check_greeting(sky_plus_strings.GOOD_MORNING)
    finally:
        clear_test()

def test_timed_greeting_good_afternoon():
    """Open MySky app and check that the greeting is Good afternoon
    Automates: https://interactiveqa.testrail.net/index.php?/cases/view/5
    NOTE: This test must run between midday and 18.00
    """
    clear_test()
    try:
        mysky_frame_objects.open_and_check_greeting(sky_plus_strings.GOOD_AFTERNOON)
    finally:
        clear_test()

def test_timed_greeting_good_evening():
    """Open MySky app and check that the greeting is Good evening
    Automates: https://interactiveqa.testrail.net/index.php?/cases/view/6
    NOTE: This test must run between 18.00 and midnight
    """
    clear_test()
    try:
        mysky_frame_objects.open_and_check_greeting(sky_plus_strings.GOOD_EVENING)
    finally:
        clear_test()

def test_acceptance_simple_my_account_navigation():
    """Open My Account menu and navigate
    Automates: https://interactiveqa.testrail.net/index.php?/cases/view/26
    """
    clear_test()
    try:
        sky_plus_utils.go_to_channel(interactive_constants.CHANNEL_SKY_ONE)
        mysky_frame_objects.open_and_basic_check_mysky()

        # Navigate menus:
        stbt.press('KEY_DOWN')
        assert stbt.wait_until(lambda: MySkyMainMenu().message == sky_plus_strings.MANAGE_YOUR_ACCOUNT), \
            '[MySky] Selected item is not [{0}]'.format(sky_plus_strings.MANAGE_YOUR_ACCOUNT)
        stbt.press('KEY_SELECT')
    finally:
        clear_test()
