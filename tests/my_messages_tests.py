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

def test_smoke_open_my_messages():
    """Open MySky app"""
    clear_test()
    try:
        sky_plus_utils.go_to_channel(interactive_constants.CHANNEL_SKY_ONE)
        open_and_basic_check_interactive_menu()

        # Navigate menus:
        stbt.press('KEY_DOWN')
        stbt.press('KEY_DOWN')
        stbt.press('KEY_DOWN')
        assert stbt.wait_until(lambda: InteractiveMainMenu().message == sky_plus_strings.MY_MESSAGES, timeout_secs=20), \
            '[Interactive] Selected item is not [{0}]'.format(sky_plus_strings.MY_MESSAGES)
        stbt.press('KEY_SELECT')
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
