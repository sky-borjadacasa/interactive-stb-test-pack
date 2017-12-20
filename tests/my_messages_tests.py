#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for My Messages
"""

from time import sleep
import stbt
import sky_plus_utils
from sky_plus_utils import clear_test, debug
from interactive_frame_objects import InteractiveMainMenu
import interactive_constants
import sky_plus_strings
import mysky_test_utils

def test_smoke_open_my_messages():
    """Open MySky app"""
    clear_test()
    try:
        sky_plus_utils.go_to_channel(interactive_constants.CHANNEL_SKY_ONE)
        open_and_basic_check_interactive_menu()
    finally:
        clear_test()

def open_and_basic_check_interactive_menu():
    """Open the My Messages app and make basic checks"""
    stbt.press('KEY_INTERACTIVE')
    sleep(1)
    menu = stbt.wait_until(InteractiveMainMenu)
    assert menu.is_visible, '[Interactive] Main menu is not visible'

    menu_items = menu.menu_items
    for item in menu_items:
        debug('Item text: {0}'.format(item.text))
        debug('Item selected: {0}'.format(item.selected))
    debug(len(menu_items))
    assert len(menu_items) == 9, '[Interactive] Main menu should have 9 items, but has {0}'.format(len(menu_items))
    return menu

# def test_acceptance_simple_open_mysky():
#     clear_test()
#     try:
#         sky_plus_utils.go_to_channel(interactive_constants.CHANNEL_SKY_ONE)
#         mysky_test_utils.open_and_check_mysky()

#         # Navigate menus:
#         stbt.press('KEY_DOWN')
#         assert stbt.wait_until(lambda: MySkyMainMenu().message == sky_plus_strings.MANAGE_YOUR_ACCOUNT), \
#             '[MySky] Selected item is not [{0}]'.format(sky_plus_strings.MANAGE_YOUR_ACCOUNT)
#         stbt.press('KEY_DOWN')
#         assert stbt.wait_until(lambda: MySkyMainMenu().message == sky_plus_strings.FIX_A_PROBLEM), \
#             '[MySky] Selected item is not [{0}]'.format(sky_plus_strings.FIX_A_PROBLEM)
#         stbt.press('KEY_UP')
#         assert stbt.wait_until(lambda: MySkyMainMenu().message == sky_plus_strings.MANAGE_YOUR_ACCOUNT), \
#             '[MySky] Selected item is not [{0}]'.format(sky_plus_strings.MANAGE_YOUR_ACCOUNT)
#         stbt.press('KEY_UP')
#         assert stbt.wait_until(lambda: MySkyMainMenu().message == sky_plus_strings.FIND_OUT_MORE), \
#             '[MySky] Selected item is not [{0}]'.format(sky_plus_strings.FIND_OUT_MORE)
#     finally:
#         clear_test()
