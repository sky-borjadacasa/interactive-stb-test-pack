#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for MySky
"""

from time import sleep
import stbt
from stbt import match
import sky_plus_strings
import sky_plus_utils
from sky_plus_utils import clear_test, debug
import mysky_frame_objects
from mysky_frame_objects import MySkyMainMenu, ManageYourAccountMenu
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
        stbt.press('KEY_DOWN')
        assert stbt.wait_until(lambda: MySkyMainMenu().message == sky_plus_strings.YOUR_FORECAST), \
            '[MySky] Selected item is not [{0}]'.format(sky_plus_strings.YOUR_FORECAST)
        stbt.press('KEY_UP')
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

def test_acceptance_simple_my_account_navigation():
    """Open My Account menu and navigate
    Automates: https://interactiveqa.testrail.net/index.php?/cases/view/26
    """
    clear_test()
    try:
        sky_plus_utils.go_to_channel(interactive_constants.CHANNEL_SKY_ONE)
        menu = mysky_frame_objects.open_and_basic_check_manage_your_account()

        # Navigate menus:
        stbt.press('KEY_DOWN')
        assert stbt.wait_until(lambda: ManageYourAccountMenu().message == sky_plus_strings.PACKAGE_AND_SETTINGS), \
            '[MySky] Selected item is not [{0}]'.format(sky_plus_strings.PACKAGE_AND_SETTINGS)
        stbt.press('KEY_DOWN')
        assert stbt.wait_until(lambda: ManageYourAccountMenu().message == sky_plus_strings.DETAILS_AND_MESSAGES), \
            '[MySky] Selected item is not [{0}]'.format(sky_plus_strings.DETAILS_AND_MESSAGES)
        stbt.press('KEY_DOWN')
        assert stbt.wait_until(lambda: ManageYourAccountMenu().message == sky_plus_strings.FIND_OUT_MORE), \
            '[MySky] Selected item is not [{0}]'.format(sky_plus_strings.FIND_OUT_MORE)
        stbt.press('KEY_UP')
        assert stbt.wait_until(lambda: ManageYourAccountMenu().message == sky_plus_strings.DETAILS_AND_MESSAGES), \
            '[MySky] Selected item is not [{0}]'.format(sky_plus_strings.DETAILS_AND_MESSAGES)
        stbt.press('KEY_UP')
        assert stbt.wait_until(lambda: ManageYourAccountMenu().message == sky_plus_strings.PACKAGE_AND_SETTINGS), \
            '[MySky] Selected item is not [{0}]'.format(sky_plus_strings.PACKAGE_AND_SETTINGS)
        stbt.press('KEY_UP')
        assert stbt.wait_until(lambda: ManageYourAccountMenu().message == sky_plus_strings.BILLS_AND_PAYMENTS), \
            '[MySky] Selected item is not [{0}]'.format(sky_plus_strings.BILLS_AND_PAYMENTS)

        # Check images:
        menu_items = menu.menu_items
        item = [x for x in menu_items if x.text == sky_plus_strings.BILLS_AND_PAYMENTS][0]
        match_result = match(interactive_constants.MYA_BILLS_PAYMENTS, frame=menu._frame, region=item.region)
        debug('match_result: {0}{1}'.format(match_result.match, match_result.first_pass_result))
        item = [x for x in menu_items if x.text == sky_plus_strings.PACKAGE_AND_SETTINGS][0]
        match_result = match(interactive_constants.MYA_PACKAGE_SETTINGS, frame=menu._frame, region=item.region)
        debug('match_result: {0}{1}'.format(match_result.match, match_result.first_pass_result))
        item = [x for x in menu_items if x.text == sky_plus_strings.DETAILS_AND_MESSAGES][0]
        match_result = match(interactive_constants.MYA_DETAILS_MESSAGES, frame=menu._frame, region=item.region)
        debug('match_result: {0}{1}'.format(match_result.match, match_result.first_pass_result))
        item = [x for x in menu_items if x.text == sky_plus_strings.FIND_OUT_MORE][0]
        match_result = match(interactive_constants.MYA_MY_OFFERS, frame=menu._frame, region=item.region)
        debug('match_result: {0}{1}'.format(match_result.match, match_result.first_pass_result))
    finally:
        clear_test()

def test_acceptance_simple_my_account_yellow_button():
    """Open My Account menu and go back to MySky main menu
    Automates: https://interactiveqa.testrail.net/index.php?/cases/view/27
    """
    clear_test()
    try:
        sky_plus_utils.go_to_channel(interactive_constants.CHANNEL_SKY_ONE)
        mysky_frame_objects.open_and_basic_check_manage_your_account()
        stbt.press('KEY_YELLOW')
        sleep(1)
        mysky_frame_objects.basic_check_mysky()
    finally:
        clear_test()
